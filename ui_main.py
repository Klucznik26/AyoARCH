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
                             QAbstractItemView, QGridLayout)
from PySide6.QtGui import QPixmap, QImage, QDragEnterEvent, QDropEvent, QCursor, QColor, QIcon, QPainter, QPen
from PySide6.QtCore import Qt, QTranslator, QLocale, QLibraryInfo, QSettings, QTimer, QSize, Signal
from styles import (MAIN_STYLE, LIGHT_STYLE, RELAX_THEME, ARCTIC_THEME, SYSTEM_THEME,
                   DROP_ZONE_STYLE, DROP_ZONE_STYLE_LIGHT, DROP_ZONE_STYLE_RELAX, 
                   DROP_ZONE_STYLE_ARCTIC, DROP_ZONE_STYLE_SYSTEM, CREATIVE_THEME, DROP_ZONE_STYLE_CREATIVE,
                   LOGO_STYLE_MISSING)
from ui_dialogs import CreateArchiveDialog, LanguageSelectionDialog, InfoDialog, ThemeSelectionDialog

class AyoArch(QMainWindow):
    APP_VERSION = "1.5.5"

    def __init__(self):
        super().__init__()
        # Konfiguracja okna
        self.setWindowTitle(f"Ayo Archi v {self.APP_VERSION} - Archive Viewer")
        self.setMinimumSize(1000, 700)
        
        # Konfiguracja ustawień (trwała pamięć)
        self.settings = QSettings("AyoArchi", "Config")
        
        # Włączenie obsługi przeciągania plików
        self.setAcceptDrops(True)

        # Zmienna do przechowywania oryginalnego obrazu (do skalowania)
        self.current_pixmap = None
        self.current_zip_path = None

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

        self.setup_narrow_panel(main_layout)
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

        # Ładowanie tłumaczeń Qt (qtbase)
        if hasattr(self, 'qt_translator'):
            path = QLibraryInfo.path(QLibraryInfo.TranslationsPath)
            if not self.qt_translator.load(QLocale(lang_code), "qtbase", "_", path):
                print(f"Info: Nie znaleziono tłumaczeń Qt dla '{lang_code}' w {path}")

    def setup_narrow_panel(self, layout):
        # --- WĄSKI PANEL (NARROW SIDEBAR) ---
        narrow_container = QFrame()
        narrow_container.setObjectName("narrowPanel")
        narrow_container.setFixedWidth(60)
        
        narrow_layout = QVBoxLayout(narrow_container)
        narrow_layout.setContentsMargins(0, 20, 0, 20)
        narrow_layout.setSpacing(20)
        
        # Logo na górze paska
        self.btn_narrow_logo = QPushButton()
        self.btn_narrow_logo.setObjectName("iconButton")
        self.btn_narrow_logo.setCursor(Qt.PointingHandCursor)
        
        assets_dir = os.path.join(os.path.dirname(__file__), "assets")
        logo_path = os.path.join(assets_dir, "AARCH.png")
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            if not pixmap.isNull():
                self.btn_narrow_logo.setIcon(QIcon(pixmap))
                self.btn_narrow_logo.setIconSize(QSize(40, 40))
        self.btn_narrow_logo.setToolTip(self.strings.get("app_info", "Information"))
        self.btn_narrow_logo.clicked.connect(self.open_info_dialog)
        narrow_layout.addWidget(self.btn_narrow_logo)
        
        # Spacer na górze (dopycha ikony do dołu)
        narrow_layout.addStretch()
        
        # Przycisk Języka (Globus)
        self.btn_narrow_lang = QPushButton("🌐\uFE0E")
        self.btn_narrow_lang.setToolTip("Język / Language")
        self.btn_narrow_lang.setObjectName("iconButton")
        self.btn_narrow_lang.setCursor(Qt.PointingHandCursor)
        self.btn_narrow_lang.clicked.connect(self.open_language_dialog)
        narrow_layout.addWidget(self.btn_narrow_lang)
        
        # Przycisk Motywu (Zębatka)
        self.btn_narrow_theme = QPushButton("⚙")
        self.btn_narrow_theme.setToolTip("Motyw / Theme")
        self.btn_narrow_theme.setObjectName("iconButton")
        self.btn_narrow_theme.setCursor(Qt.PointingHandCursor)
        self.btn_narrow_theme.clicked.connect(self.open_theme_dialog)
        narrow_layout.addWidget(self.btn_narrow_theme)
        
        # Przycisk Zamknij (Power)
        self.btn_narrow_close = QPushButton("⏻")
        self.btn_narrow_close.setToolTip("Zamknij / Close")
        self.btn_narrow_close.setObjectName("iconButton")
        self.btn_narrow_close.setProperty("danger", True)
        self.btn_narrow_close.setCursor(Qt.PointingHandCursor)
        self.btn_narrow_close.clicked.connect(self.close)
        narrow_layout.addWidget(self.btn_narrow_close)

        # Ujednolicenie rozmiaru ikon (język, motyw, wyłącz) do rozmiaru ikony języka.
        unified_font = self.btn_narrow_lang.font()
        if unified_font.pixelSize() > 0:
            unified_font.setPixelSize(unified_font.pixelSize())
        else:
            unified_font.setPointSize(24)
        for btn in (self.btn_narrow_lang, self.btn_narrow_theme, self.btn_narrow_close):
            btn.setFont(unified_font)
            btn.setFixedSize(44, 44)

        # Symbol zasilania wygląda optycznie mniejszy, więc podbijamy go o ~30%.
        close_font = self.btn_narrow_close.font()
        base_px = unified_font.pixelSize()
        if base_px > 0:
            close_font.setPixelSize(int(round(base_px * 1.3)))
        else:
            close_font.setPointSize(int(round(unified_font.pointSizeF() * 1.3)))
        self.btn_narrow_close.setFont(close_font)

        # Cień pod panelem
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setOffset(0, 6)
        shadow.setColor(QColor(0, 0, 0, 60))
        narrow_container.setGraphicsEffect(shadow)

        # Dodajemy na początek layoutu (lewa strona)
        layout.insertWidget(0, narrow_container)

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
            self.logo_label.setText("Ayo Archi")
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
        title = s.get("app_title", f"Ayo Archi v {self.APP_VERSION} - Archive Viewer")
        # Wymuś spójną wersję w tytule niezależnie od pliku językowego.
        title = re.sub(r"v\s*\d+\.\d+\.\d+", f"v {self.APP_VERSION}", title)
        self.setWindowTitle(title)
        self.btn_open.setText(s.get("open_archive", "Otwórz"))
        self.btn_create.setText(s.get("create_archive", "Utwórz archiwum"))
        self.btn_narrow_logo.setToolTip(s.get("app_info", "Information"))
        if not self.current_pixmap:
            self.image_label.setText(s.get("drop_zone_text", "..."))
        self.file_tree.setHeaderLabels([s.get("file_name", "File Name")])

    def open_language_dialog(self):
        dialog = LanguageSelectionDialog(self, self.strings)
        dialog.setStyleSheet(self.styleSheet())
        dialog.language_selected.connect(self.load_language)
        dialog.exec()

    def open_theme_dialog(self):
        dialog = ThemeSelectionDialog(self)
        dialog.setStyleSheet(self.styleSheet())
        dialog.theme_selected.connect(self.apply_theme)
        dialog.exec()

    def open_info_dialog(self):
        dialog = InfoDialog(self)
        dialog.setStyleSheet(self.styleSheet())
        dialog.exec()

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
        elif theme_code == "dark":
            self.setStyleSheet(MAIN_STYLE)
            self.image_label.setStyleSheet(DROP_ZONE_STYLE)
        elif theme_code == "light":
            self.setStyleSheet(LIGHT_STYLE)
            self.image_label.setStyleSheet(DROP_ZONE_STYLE_LIGHT)
        elif theme_code == "relax":
            self.setStyleSheet(RELAX_THEME)
            self.image_label.setStyleSheet(DROP_ZONE_STYLE_RELAX)
        elif theme_code == "arctic":
            self.setStyleSheet(ARCTIC_THEME)
            self.image_label.setStyleSheet(DROP_ZONE_STYLE_ARCTIC)
        elif theme_code == "creative":
            self.setStyleSheet(CREATIVE_THEME)
            self.image_label.setStyleSheet(DROP_ZONE_STYLE_CREATIVE)

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
                self.setWindowTitle(f"Ayo Archi v {self.APP_VERSION} - {zip_path}")
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
