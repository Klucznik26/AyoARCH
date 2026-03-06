import os
import sys
import subprocess
import zipfile
import json
import re
try:
    import py7zr
except ImportError:
    py7zr = None
try:
    import rarfile
except ImportError:
    rarfile = None
from PySide6.QtWidgets import (QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, 
                             QWidget, QPushButton, QFileDialog, QSpacerItem, 
                             QSizePolicy, QTreeWidget, QTreeWidgetItem, QMessageBox,
                             QApplication, QFrame, QGraphicsDropShadowEffect,
                             QTreeView, QTableView, QDialog, QListWidget, QListWidgetItem,
                             QAbstractItemView)
from PySide6.QtGui import QPixmap, QImage, QDragEnterEvent, QDropEvent, QCursor, QColor, QIcon
from PySide6.QtCore import Qt, QTranslator, QLocale, QLibraryInfo, QSettings, QTimer, QSize
from styles import (MAIN_STYLE, LIGHT_STYLE, RELAX_THEME, SYSTEM_THEME,
                   DROP_ZONE_STYLE, DROP_ZONE_STYLE_LIGHT, DROP_ZONE_STYLE_RELAX, 
                   DROP_ZONE_STYLE_SYSTEM, CREATIVE_THEME, DROP_ZONE_STYLE_CREATIVE,
                   LOGO_STYLE_MISSING)
from settings import SettingsWindow

class AyoArch(QMainWindow):
    APP_VERSION = "1.5.0"

    def __init__(self):
        super().__init__()
        # Konfiguracja okna
        self.setWindowTitle(f"Ayo Arch v {self.APP_VERSION} - Archive Viewer")
        self.setMinimumSize(1000, 700)
        
        # Konfiguracja ustawień (trwała pamięć)
        self.settings = QSettings("AyoArch", "Config")
        
        # Włączenie obsługi przeciągania plików
        self.setAcceptDrops(True)

        # Zmienna do przechowywania oryginalnego obrazu (do skalowania)
        self.current_pixmap = None
        self.current_zip_path = None

        # Okno ustawień
        self.settings_window = None

        # Inicjalizacja tłumacza Qt (dla okien systemowych)
        self.qt_translator = QTranslator()
        if QApplication.instance():
            QApplication.instance().installTranslator(self.qt_translator)

        # Domyślny język (z ustawień)
        saved_lang = self.settings.value("language", "pl")
        self.load_language(saved_lang)

        # Główny kontener
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Główny layout (Poziomy: Sidebar | Content)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        self.setup_sidebar(main_layout)
        self.setup_content(main_layout)

        # Domyślny motyw (startujemy z zapisanym lub Ciemnym)
        saved_theme = self.settings.value("theme", "dark")
        self.apply_theme(saved_theme)

        # Aplikuj teksty po utworzeniu UI
        self.update_texts()

    def load_language(self, lang_code):
        self.current_lang = lang_code
        self.settings.setValue("language", lang_code)
        self.strings = {}
        try:
            i18n_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "i18n", f"{lang_code}.json")
            if os.path.exists(i18n_path):
                with open(i18n_path, "r", encoding="utf-8") as f:
                    self.strings = json.load(f)
        except Exception as e:
            print(f"Błąd ładowania języka {lang_code}: {e}")
        
        # Odśwież teksty jeśli UI już istnieje
        if hasattr(self, 'btn_open'):
            self.update_texts()
            if self.settings_window:
                self.settings_window.update_texts(self.strings)

        # Ładowanie tłumaczeń Qt (qtbase)
        if hasattr(self, 'qt_translator'):
            path = QLibraryInfo.path(QLibraryInfo.TranslationsPath)
            if not self.qt_translator.load(QLocale(lang_code), "qtbase", "_", path):
                print(f"Info: Nie znaleziono tłumaczeń Qt dla '{lang_code}' w {path}")

    def setup_sidebar(self, layout):
        # --- LEWY PANEL (SIDEBAR) ---
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setSpacing(10)

        # Przyciski górne
        self.btn_open = QPushButton("Otwórz archiwum")
        self.btn_open.clicked.connect(self.load_zip_dialog)
        self.btn_open.setObjectName("runButton")
        
        sidebar_layout.addWidget(self.btn_open)

        self.btn_create = QPushButton("Utwórz archiwum")
        self.btn_create.clicked.connect(self.open_create_dialog)
        self.btn_create.setObjectName("runButton")
        sidebar_layout.addWidget(self.btn_create)

        # Etykieta z nazwą archiwum (domyślnie ukryta)
        self.archive_name_label = QLabel()
        self.archive_name_label.setVisible(False)
        sidebar_layout.addWidget(self.archive_name_label)

        # Drzewo plików (domyślnie ukryte)
        self.file_tree = QTreeWidget()
        self.file_tree.setHeaderHidden(False)
        self.file_tree.setVisible(False)
        self.file_tree.itemClicked.connect(self.on_tree_item_clicked)
        sidebar_layout.addWidget(self.file_tree)

        # Spacer (rozpychacz - dopycha dolne przyciski do dołu)
        self.sidebar_spacer = QWidget()
        self.sidebar_spacer.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        sidebar_layout.addWidget(self.sidebar_spacer)

        # Przyciski dolne
        self.btn_settings = QPushButton("Ustawienia")
        self.btn_close = QPushButton("Zamknij")
        self.btn_settings.clicked.connect(self.open_settings)
        self.btn_close.clicked.connect(self.close)

        sidebar_layout.addWidget(self.btn_settings)
        sidebar_layout.addWidget(self.btn_close)

        # Kontener dla sidebara (aby ustalić stałą szerokość)
        sidebar_container = QFrame()
        sidebar_container.setObjectName("leftPanel")
        sidebar_container.setLayout(sidebar_layout)
        sidebar_container.setFixedWidth(200)
        
        # Cień pod panelem
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setOffset(0, 6)
        shadow.setColor(QColor(0, 0, 0, 60))
        sidebar_container.setGraphicsEffect(shadow)
        
        layout.addWidget(sidebar_container)

    def setup_content(self, layout):
        # --- CENTRUM (PODGLĄD + LOGO) ---
        content_container = QFrame()
        content_container.setObjectName("rightPanel")
        
        content_layout = QHBoxLayout(content_container)
        content_layout.setContentsMargins(10, 10, 10, 10)
        content_layout.setSpacing(10)

        # Obszar podglądu
        self.image_label = QLabel("Przeciągnij i upuść archiwum tutaj")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet(DROP_ZONE_STYLE)
        self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        content_layout.addWidget(self.image_label)

        self.logo_label = QLabel()
        
        # Stylizacja logo (ramka i tło)
        self.logo_label.setStyleSheet("""
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 10px;
            background-color: rgba(255, 255, 255, 0.05);
        """)
        
        # Cień dla logo
        logo_shadow = QGraphicsDropShadowEffect()
        logo_shadow.setBlurRadius(20)
        logo_shadow.setOffset(0, 5)
        logo_shadow.setColor(QColor(0, 0, 0, 70))
        self.logo_label.setGraphicsEffect(logo_shadow)

        self.load_logo()
        content_layout.addWidget(self.logo_label, 0, Qt.AlignBottom)

        # Cień pod panelem
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setOffset(0, 6)
        shadow.setColor(QColor(0, 0, 0, 60))
        content_container.setGraphicsEffect(shadow)

        layout.addWidget(content_container)

    def load_logo(self):
        # Szukanie logo
        assets_dir = os.path.join(os.path.dirname(__file__), "assets")
        logo_found = False
        
        # Lista potencjalnych nazw plików (uwzględniając wielkość liter dla Linuxa)
        possible_names = ["AyoARCH.png", "AyoArch.png", "ayoarch.png", 
                          "AyoARCH.jpg", "AyoArch.jpg", "ayoarch.jpg"]
        
        for name in possible_names:
            logo_path = os.path.join(assets_dir, name)
            if os.path.exists(logo_path):
                self.logo_label.setPixmap(QPixmap(logo_path).scaledToHeight(150, Qt.SmoothTransformation))
                logo_found = True
                break
                
        if not logo_found:
            self.logo_label.setText("Ayo ARCH")
            self.logo_label.setStyleSheet(LOGO_STYLE_MISSING)

    # --- Obsługa Drag & Drop ---
    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        if files:
            # Bierzemy pierwszy plik z rzutu
            file_path = files[0]
            if file_path.lower().endswith(('.zip', '.cbz', '.7z', '.rar', '.cbr')):
                self.display_first_image(file_path)
            else:
                self.image_label.setText(self.strings.get("not_zip_error", "To nie jest obsługiwane archiwum!"))

    # --- Obsługa zmiany rozmiaru okna ---
    def resizeEvent(self, event):
        # Przeskaluj obraz, jeśli okno zmienia rozmiar i mamy co wyświetlać
        if self.current_pixmap:
            self.update_image_display()
        super().resizeEvent(event)

    def update_texts(self):
        s = self.strings
        title = s.get("app_title", f"Ayo Arch v {self.APP_VERSION} - Archive Viewer")
        # Wymuś spójną wersję w tytule niezależnie od pliku językowego.
        title = re.sub(r"v\s*\d+\.\d+\.\d+", f"v {self.APP_VERSION}", title)
        self.setWindowTitle(title)
        self.btn_open.setText(s.get("open_archive", "Otwórz"))
        self.btn_create.setText(s.get("create_archive", "Utwórz archiwum"))
        self.btn_settings.setText(s.get("settings", "Ustawienia"))
        self.btn_close.setText(s.get("close", "Zamknij"))
        if not self.current_pixmap:
            self.image_label.setText(s.get("drop_zone_text", "..."))
        self.file_tree.setHeaderLabels([s.get("file_name", "File Name")])

    def open_settings(self):
        if self.settings_window is None:
            self.settings_window = SettingsWindow(self)
            self.settings_window.language_changed.connect(self.load_language)
            self.settings_window.theme_changed.connect(self.apply_theme)
        
        self.settings_window.update_texts(self.strings)
        
        # Ustawienie aktualnego języka w combo
        current_lang = getattr(self, 'current_lang', 'pl')
        lang_index = self.settings_window.combo_lang.findData(current_lang)
        if lang_index >= 0:
            self.settings_window.combo_lang.blockSignals(True)
            self.settings_window.combo_lang.setCurrentIndex(lang_index)
            self.settings_window.combo_lang.blockSignals(False)
        
        # Ustawienie aktualnego motywu w combo
        current_theme = getattr(self, 'current_theme', 'dark')
        theme_index = self.settings_window.combo_theme.findData(current_theme)
        if theme_index >= 0:
            self.settings_window.combo_theme.setCurrentIndex(theme_index)
            
        self.settings_window.show()

    def open_create_dialog(self):
        dialog = CreateArchiveDialog(self, self.strings)
        # Przekazanie stylu z głównego okna
        dialog.setStyleSheet(self.styleSheet())
        # Przekazanie stylu drop zone (zależnego od motywu)
        dialog.set_drop_zone_style(self.image_label.styleSheet())
        dialog.exec()

    def apply_theme(self, theme_code):
        self.current_theme = theme_code
        self.settings.setValue("theme", theme_code)
        
        if theme_code == "system":
            self.setStyleSheet(SYSTEM_THEME)
            self.image_label.setStyleSheet(DROP_ZONE_STYLE_SYSTEM)
            if self.settings_window:
                self.settings_window.setStyleSheet(SYSTEM_THEME)
        elif theme_code == "dark":
            self.setStyleSheet(MAIN_STYLE)
            self.image_label.setStyleSheet(DROP_ZONE_STYLE)
            if self.settings_window:
                self.settings_window.setStyleSheet(MAIN_STYLE)
        elif theme_code == "light":
            self.setStyleSheet(LIGHT_STYLE)
            self.image_label.setStyleSheet(DROP_ZONE_STYLE_LIGHT)
            if self.settings_window:
                self.settings_window.setStyleSheet(LIGHT_STYLE)
        elif theme_code == "relax":
            self.setStyleSheet(RELAX_THEME)
            self.image_label.setStyleSheet(DROP_ZONE_STYLE_RELAX)
            if self.settings_window:
                self.settings_window.setStyleSheet(RELAX_THEME)
        elif theme_code == "creative":
            self.setStyleSheet(CREATIVE_THEME)
            self.image_label.setStyleSheet(DROP_ZONE_STYLE_CREATIVE)
            if self.settings_window:
                self.settings_window.setStyleSheet(CREATIVE_THEME)

    # --- Logika aplikacji ---
    def load_zip_dialog(self):
        dialog = QFileDialog(self, self.strings.get("open_archive", "Wybierz archiwum"), "")
        dialog.setNameFilter("Archives (*.zip *.cbz *.7z *.rar *.cbr)")
        dialog.setFileMode(QFileDialog.ExistingFile)
        dialog.setOption(QFileDialog.DontUseNativeDialog, True)
        dialog.setStyleSheet(self.styleSheet())
        self.localize_file_dialog(dialog)
        dialog.directoryEntered.connect(lambda _: self.localize_file_dialog(dialog))
        QTimer.singleShot(0, lambda: self.localize_file_dialog(dialog))
        
        if dialog.exec():
            selected = dialog.selectedFiles()
            if selected:
                self.display_first_image(selected[0])

    def localize_file_dialog(self, dialog):
        s = self.strings
        labels = {
            "Look in:": s.get("fd_look_in", "Look in:"),
            "File name:": s.get("fd_file_name", "File name:"),
            "Files of type:": s.get("fd_files_of_type", "Files of type:"),
            "Open": s.get("fd_open", s.get("open_archive", "Open")),
            "Cancel": s.get("fd_cancel", s.get("cancel", "Cancel")),
            "Computer": s.get("fd_computer", "Computer"),
            "Name": s.get("fd_name", "Name"),
            "Size": s.get("fd_size", "Size"),
            "Type": s.get("fd_type", "Type"),
            "Date Modified": s.get("fd_date_modified", "Date Modified")
        }

        for widget in dialog.findChildren(QWidget):
            text_getter = getattr(widget, "text", None)
            text_setter = getattr(widget, "setText", None)
            if callable(text_getter) and callable(text_setter):
                try:
                    source = text_getter()
                except TypeError:
                    continue
                target = labels.get(source)
                if target:
                    text_setter(target)

        for view in dialog.findChildren(QTreeView) + dialog.findChildren(QTableView):
            model = view.model()
            if not model:
                continue
            model.setHeaderData(0, Qt.Horizontal, labels["Name"])
            model.setHeaderData(1, Qt.Horizontal, labels["Size"])
            model.setHeaderData(2, Qt.Horizontal, labels["Type"])
            model.setHeaderData(3, Qt.Horizontal, labels["Date Modified"])

    def display_first_image(self, zip_path):
        self.current_zip_path = zip_path
        try:
            self.archive_name_label.setText(os.path.basename(zip_path))
            self.archive_name_label.setVisible(True)
            self.sidebar_spacer.setVisible(False)
            
            file_list = []
            if zip_path.lower().endswith('.7z'):
                global py7zr
                if py7zr is None:
                    reply = QMessageBox.question(
                        self, 
                        self.strings.get("dep_install_title", "Wymagany dodatek"), 
                        self.strings.get("dep_install_question", "Obsługa plików .7z wymaga biblioteki 'py7zr'.\nCzy chcesz, aby program pobrał i zainstalował ją teraz automatycznie?"),
                        QMessageBox.Yes | QMessageBox.No
                    )
                    
                    if reply == QMessageBox.Yes:
                        self.image_label.setText(self.strings.get("dep_installing", "Instalowanie biblioteki py7zr... Proszę czekać."))
                        QApplication.setOverrideCursor(Qt.WaitCursor)
                        QApplication.processEvents()
                        try:
                            subprocess.check_call([sys.executable, "-m", "pip", "install", "py7zr"])
                            import py7zr as lib
                            py7zr = lib
                        except Exception as e:
                            self.image_label.setText(f"{self.strings.get('dep_install_error', 'Błąd instalacji: ')}{e}")
                            QApplication.restoreOverrideCursor()
                            return
                        finally:
                            QApplication.restoreOverrideCursor()
                    else:
                        self.image_label.setText(self.strings.get("dep_install_cancel", "Anulowano. Biblioteka py7zr jest wymagana dla plików .7z."))
                        return

                with py7zr.SevenZipFile(zip_path, mode='r') as z:
                    file_list = z.getnames()
            elif zip_path.lower().endswith(('.rar', '.cbr')):
                global rarfile
                if rarfile is None:
                    reply = QMessageBox.question(
                        self, 
                        self.strings.get("dep_install_title", "Wymagany dodatek"), 
                        self.strings.get("dep_install_question_rar", "Obsługa plików .rar wymaga biblioteki 'rarfile'.\nCzy chcesz, aby program pobrał i zainstalował ją teraz automatycznie?"),
                        QMessageBox.Yes | QMessageBox.No
                    )
                    
                    if reply == QMessageBox.Yes:
                        self.image_label.setText(self.strings.get("dep_installing_rar", "Instalowanie biblioteki rarfile... Proszę czekać."))
                        QApplication.setOverrideCursor(Qt.WaitCursor)
                        QApplication.processEvents()
                        try:
                            subprocess.check_call([sys.executable, "-m", "pip", "install", "rarfile"])
                            import rarfile as lib
                            rarfile = lib
                        except Exception as e:
                            self.image_label.setText(f"{self.strings.get('dep_install_error', 'Błąd instalacji: ')}{e}")
                            QApplication.restoreOverrideCursor()
                            return
                        finally:
                            QApplication.restoreOverrideCursor()
                    else:
                        self.image_label.setText(self.strings.get("dep_install_cancel_rar", "Anulowano. Biblioteka rarfile jest wymagana dla plików .rar."))
                        return

                with rarfile.RarFile(zip_path, mode='r') as z:
                    file_list = z.namelist()
            else:
                with zipfile.ZipFile(zip_path, 'r') as z:
                    file_list = z.namelist()

            # Wypełnij drzewo plików
            self.populate_tree(file_list)
            self.file_tree.setVisible(True)

            # Szukamy plików graficznych
            valid_exts = ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.tif', '.ico', '.webp')
            images = [f for f in file_list if f.lower().endswith(valid_exts)]
            
            if images:
                # Sortujemy, aby mieć pewność kolejności (np. page_01, page_02)
                images.sort()
                self.load_image_from_zip(images[0])
                self.setWindowTitle(f"Ayo Arch v {self.APP_VERSION} - {zip_path}")
            else:
                self.image_label.setText(self.strings.get("no_images_error", "Brak obrazów!"))
                self.current_pixmap = None
        except Exception as e:
            self.image_label.setText(f"{self.strings.get('error_prefix', 'Błąd: ')}{str(e)}")
            self.current_pixmap = None

    def update_image_display(self):
        if self.current_pixmap:
            # Skalowanie do aktualnego rozmiaru labela
            scaled = self.current_pixmap.scaled(
                self.image_label.size(), 
                Qt.KeepAspectRatio, 
                Qt.SmoothTransformation
            )
            self.image_label.setPixmap(scaled)

    def populate_tree(self, file_list):
        self.file_tree.clear()
        
        for name in sorted(file_list):
            parts = name.rstrip('/').split('/')
            parent = self.file_tree.invisibleRootItem()
            
            for part in parts:
                # Sprawdzamy czy taki węzeł już istnieje
                found = False
                for i in range(parent.childCount()):
                    child = parent.child(i)
                    if child.text(0) == part:
                        parent = child
                        found = True
                        break
                if not found:
                    item = QTreeWidgetItem(parent)
                    item.setText(0, part)
                    parent = item

    def on_tree_item_clicked(self, item, column):
        if not self.current_zip_path:
            return

        # Rekonstrukcja ścieżki z drzewa
        path_parts = []
        curr = item
        while curr is not None:
            path_parts.insert(0, curr.text(0))
            curr = curr.parent()
        
        full_path = "/".join(path_parts)

        # Sprawdź rozszerzenie
        valid_exts = ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.tif', '.ico', '.webp')
        if full_path.lower().endswith(valid_exts):
            self.load_image_from_zip(full_path)

    def load_image_from_zip(self, filename):
        try:
            data = None
            if self.current_zip_path.lower().endswith('.7z'):
                if py7zr:
                    with py7zr.SevenZipFile(self.current_zip_path, mode='r') as z:
                        data_map = z.read(targets=[filename])
                        data = data_map[filename].read()
            elif self.current_zip_path.lower().endswith(('.rar', '.cbr')):
                if rarfile:
                    with rarfile.RarFile(self.current_zip_path, mode='r') as z:
                        with z.open(filename) as f:
                            data = f.read()
            else:
                with zipfile.ZipFile(self.current_zip_path, 'r') as z:
                    with z.open(filename) as f:
                        data = f.read()
            
            if data:
                img = QImage.fromData(data)
                self.current_pixmap = QPixmap.fromImage(img)
                self.update_image_display()
        except Exception as e:
            self.image_label.setText(f"{self.strings.get('error_prefix', 'Błąd: ')}{str(e)}")

class CreateArchiveDialog(QDialog):
    def __init__(self, parent=None, strings=None):
        super().__init__(parent)
        self.strings = strings or {}
        self.setWindowTitle(self.strings.get("create_archive_title", "Kreator Archiwum"))
        self.setMinimumSize(500, 400)
        self.setAcceptDrops(True)
        self.files_to_archive = []

        layout = QVBoxLayout(self)

        # Drop Zone
        self.drop_label = QLabel(self.strings.get("drop_images_create", "Przeciągnij obrazy do stworzenia archiwum"))
        self.drop_label.setAlignment(Qt.AlignCenter)
        self.drop_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(self.drop_label)

        # Lista plików
        self.file_list_widget = QListWidget()
        self.file_list_widget.setViewMode(QListWidget.IconMode)
        self.file_list_widget.setIconSize(QSize(100, 100))
        self.file_list_widget.setResizeMode(QListWidget.Adjust)
        self.file_list_widget.setSpacing(10)
        self.file_list_widget.setSelectionMode(QAbstractItemView.NoSelection)
        self.file_list_widget.setVisible(False)
        layout.addWidget(self.file_list_widget)

        # Przyciski
        btn_layout = QHBoxLayout()
        self.btn_create = QPushButton(self.strings.get("create_confirm", "Utwórz ZIP"))
        self.btn_create.setObjectName("runButton")
        self.btn_create.clicked.connect(self.create_archive)
        self.btn_create.setEnabled(False)
        
        self.btn_cancel = QPushButton(self.strings.get("cancel", "Anuluj"))
        self.btn_cancel.clicked.connect(self.reject)

        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_create)
        btn_layout.addWidget(self.btn_cancel)
        layout.addLayout(btn_layout)

    def set_drop_zone_style(self, style):
        self.drop_label.setStyleSheet(style)
        self.file_list_widget.setStyleSheet(style.replace("QLabel", "QListWidget"))

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        valid_files = [f for f in files if os.path.isfile(f)]
        
        if valid_files:
            self.files_to_archive.extend(valid_files)
            self.update_file_list()

    def update_file_list(self):
        self.file_list_widget.clear()
        for f in self.files_to_archive:
            item = QListWidgetItem()
            item.setToolTip(os.path.basename(f))
            
            pixmap = QPixmap(f)
            if not pixmap.isNull():
                scaled = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                item.setIcon(QIcon(scaled))
            
            self.file_list_widget.addItem(item)
        
        count = len(self.files_to_archive)
        self.drop_label.setText(f"{self.strings.get('files_count', 'Plików: ')} {count}")
        self.file_list_widget.setVisible(True)
        self.drop_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.btn_create.setEnabled(count > 0)

    def create_archive(self):
        if not self.files_to_archive:
            return

        dialog = QFileDialog(self, self.strings.get("save", "Zapisz"), "")
        dialog.setAcceptMode(QFileDialog.AcceptSave)
        dialog.setFileMode(QFileDialog.AnyFile)
        dialog.setNameFilter("ZIP Archive (*.zip)")
        dialog.setDefaultSuffix("zip")
        dialog.selectFile("archive.zip")
        dialog.setOption(QFileDialog.DontUseNativeDialog, True)
        dialog.setStyleSheet(self.styleSheet())
        dialog.setLabelText(QFileDialog.Accept, self.strings.get("save", "Zapisz"))
        
        if self.parent() and hasattr(self.parent(), 'localize_file_dialog'):
            self.parent().localize_file_dialog(dialog)
            dialog.directoryEntered.connect(lambda _: self.parent().localize_file_dialog(dialog))
            QTimer.singleShot(0, lambda: self.parent().localize_file_dialog(dialog))

        if dialog.exec():
            selected = dialog.selectedFiles()
            if selected:
                save_path = os.path.abspath(os.path.expanduser(selected[0]))
                if os.path.isdir(save_path):
                    QMessageBox.warning(
                        self,
                        self.strings.get("error_prefix", "Błąd"),
                        self.strings.get("save_path_is_dir", "Wskaż nazwę pliku, a nie folder.")
                    )
                    return

                if not save_path.lower().endswith(".zip"):
                    save_path += ".zip"

                try:
                    added_files = 0
                    with zipfile.ZipFile(save_path, "w", compression=zipfile.ZIP_DEFLATED) as zipf:
                        for file in self.files_to_archive:
                            if os.path.isfile(file):
                                zipf.write(file, os.path.basename(file))
                                added_files += 1

                    if added_files == 0:
                        QMessageBox.warning(
                            self,
                            self.strings.get("error_prefix", "Błąd"),
                            self.strings.get("no_files_to_archive", "Brak plików do spakowania.")
                        )
                        return
                except Exception as e:
                    QMessageBox.critical(
                        self,
                        self.strings.get("error_prefix", "Błąd"),
                        f"{self.strings.get('archive_create_error', 'Nie udało się utworzyć archiwum: ')}{e}"
                    )
                    return

                QMessageBox.information(
                    self,
                    self.strings.get("save", "Zapisz"),
                    f"{self.strings.get('archive_created', 'Archiwum utworzone:')} {save_path}"
                )
                self.accept()
