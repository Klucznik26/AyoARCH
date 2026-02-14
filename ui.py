import os
import zipfile
import importlib
from PySide6.QtWidgets import (QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, 
                             QWidget, QPushButton, QFileDialog, QSpacerItem, 
                             QSizePolicy, QTreeWidget, QTreeWidgetItem)
from PySide6.QtGui import QPixmap, QImage, QDragEnterEvent, QDropEvent
from PySide6.QtCore import Qt
from styles import (MAIN_STYLE, LIGHT_STYLE, RELAX_THEME, SYSTEM_THEME,
                   DROP_ZONE_STYLE, DROP_ZONE_STYLE_LIGHT, DROP_ZONE_STYLE_RELAX, 
                   DROP_ZONE_STYLE_SYSTEM, CREATIVE_THEME, DROP_ZONE_STYLE_CREATIVE,
                   LOGO_STYLE_MISSING)
from settings import SettingsWindow

class AyoArch(QMainWindow):
    def __init__(self):
        super().__init__()
        # Konfiguracja okna
        self.setWindowTitle("Ayo Arch v 1.0.0 - Archive Viewer")
        self.setMinimumSize(1000, 700)
        
        # Włączenie obsługi przeciągania plików
        self.setAcceptDrops(True)

        # Zmienna do przechowywania oryginalnego obrazu (do skalowania)
        self.current_pixmap = None
        self.current_zip_path = None

        # Okno ustawień
        self.settings_window = None

        # Domyślny język
        self.load_language("pl")

        # Główny kontener
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Główny layout (Poziomy: Sidebar | Content)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        self.setup_sidebar(main_layout)
        self.setup_content(main_layout)

        # Domyślny motyw (startujemy z Ciemnym, ale w ustawieniach Systemowy jest pierwszy)
        self.apply_theme("dark")

        # Aplikuj teksty po utworzeniu UI
        self.update_texts()

    def load_language(self, lang_code):
        try:
            mod = importlib.import_module(f"i18n.{lang_code}")
            self.strings = mod.STRINGS
        except ImportError:
            # Jeśli folder i18n nie istnieje lub import się nie udał, spróbuj z głównego katalogu
            try:
                mod = importlib.import_module(lang_code)
                self.strings = mod.STRINGS
            except ImportError:
                print(f"Nie znaleziono pliku językowego dla: {lang_code}")
                self.strings = {}
        
        # Odśwież teksty jeśli UI już istnieje
        if hasattr(self, 'btn_open'):
            self.update_texts()
            if self.settings_window:
                self.settings_window.update_texts(self.strings)

    def setup_sidebar(self, layout):
        # --- LEWY PANEL (SIDEBAR) ---
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setSpacing(10)

        # Przyciski górne
        self.btn_open = QPushButton("Otwórz archiwum")
        self.btn_open.clicked.connect(self.load_zip_dialog)
        self.btn_open.setObjectName("runButton")
        
        sidebar_layout.addWidget(self.btn_open)

        # Etykieta z nazwą archiwum (domyślnie ukryta)
        self.archive_name_label = QLabel()
        self.archive_name_label.setVisible(False)
        sidebar_layout.addWidget(self.archive_name_label)

        # Drzewo plików (domyślnie ukryte)
        self.file_tree = QTreeWidget()
        self.file_tree.setHeaderHidden(True)
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
        sidebar_container = QWidget()
        sidebar_container.setObjectName("Sidebar")
        sidebar_container.setAttribute(Qt.WA_StyledBackground, True) # Wymuszenie rysowania tła z CSS
        sidebar_container.setLayout(sidebar_layout)
        sidebar_container.setFixedWidth(200)
        
        layout.addWidget(sidebar_container)

    def setup_content(self, layout):
        # --- CENTRUM (PODGLĄD + LOGO) ---
        content_layout = QHBoxLayout()
        content_layout.setSpacing(10)

        # Obszar podglądu
        self.image_label = QLabel("Przeciągnij i upuść archiwum tutaj")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet(DROP_ZONE_STYLE)
        self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        content_layout.addWidget(self.image_label)

        self.logo_label = QLabel()
        self.load_logo()
        content_layout.addWidget(self.logo_label, 0, Qt.AlignBottom)

        layout.addLayout(content_layout)

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
            if file_path.lower().endswith('.zip'):
                self.display_first_image(file_path)
            else:
                self.image_label.setText("To nie jest plik .zip!")

    # --- Obsługa zmiany rozmiaru okna ---
    def resizeEvent(self, event):
        # Przeskaluj obraz, jeśli okno zmienia rozmiar i mamy co wyświetlać
        if self.current_pixmap:
            self.update_image_display()
        super().resizeEvent(event)

    def update_texts(self):
        s = self.strings
        self.btn_open.setText(s.get("open_archive", "Otwórz"))
        self.btn_settings.setText(s.get("settings", "Ustawienia"))
        self.btn_close.setText(s.get("close", "Zamknij"))
        if not self.current_pixmap:
            self.image_label.setText(s.get("drop_zone_text", "..."))

    def open_settings(self):
        if self.settings_window is None:
            self.settings_window = SettingsWindow(self)
            self.settings_window.language_changed.connect(self.load_language)
            self.settings_window.theme_changed.connect(self.apply_theme)
            self.settings_window.update_texts(self.strings)
            # Ustawienie domyślnego wyboru w combo (Ciemny to index 1)
            self.settings_window.combo_theme.setCurrentIndex(1)
        self.settings_window.show()

    def apply_theme(self, theme_code):
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
        file_path, _ = QFileDialog.getOpenFileName(self, "Wybierz archiwum", "", "Archives (*.zip)")
        if file_path:
            self.display_first_image(file_path)

    def display_first_image(self, zip_path):
        self.current_zip_path = zip_path
        try:
            self.archive_name_label.setText(os.path.basename(zip_path))
            self.archive_name_label.setVisible(True)
            self.sidebar_spacer.setVisible(False)
            with zipfile.ZipFile(zip_path, 'r') as z:
                # Wypełnij drzewo plików
                self.populate_tree(z)
                self.file_tree.setVisible(True)

                # Szukamy plików graficznych (ignorujemy wielkość liter)
                # Rozszerzona lista formatów (TIFF, ICO, BMP, GIF, WEBP i inne)
                valid_exts = ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.tif', '.ico', '.webp')
                images = [f for f in z.namelist() if f.lower().endswith(valid_exts)]
                
                if images:
                    # Sortujemy, aby mieć pewność kolejności (np. page_01, page_02)
                    images.sort()
                    with z.open(images[0]) as f:
                        data = f.read()
                        img = QImage.fromData(data)
                        self.current_pixmap = QPixmap.fromImage(img)
                        self.update_image_display()
                        self.setWindowTitle(f"Ayo Arch - {zip_path}")
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

    def populate_tree(self, zfile):
        self.file_tree.clear()
        
        for name in sorted(zfile.namelist()):
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
            with zipfile.ZipFile(self.current_zip_path, 'r') as z:
                with z.open(filename) as f:
                    data = f.read()
                    img = QImage.fromData(data)
                    self.current_pixmap = QPixmap.fromImage(img)
                    self.update_image_display()
        except Exception as e:
            self.image_label.setText(f"{self.strings.get('error_prefix', 'Błąd: ')}{str(e)}")