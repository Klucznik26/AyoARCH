from PySide6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QComboBox, 
                             QPushButton)
from PySide6.QtCore import Signal, Qt
from styles import MAIN_STYLE

class SettingsWindow(QDialog):
    language_changed = Signal(str)
    theme_changed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowModality(Qt.WindowModal)
        self.setObjectName("SettingsWindow") # Dla stylizacji tła
        self.setAttribute(Qt.WA_StyledBackground, True) # Wymuszenie rysowania tła z CSS
        self.setWindowTitle("Ustawienia")
        self.setMinimumSize(400, 300)
        self.setStyleSheet(MAIN_STYLE)
        
        # Layout
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(15)
        
        # Sekcja Motywu
        self.lbl_theme = QLabel("Motyw kolorystyczny:")
        self.combo_theme = QComboBox()
        # Kolejność: Systemowy, Ciemny, Jasny
        self.combo_theme.addItems(["Systemowy", "Ciemny", "Jasny", "Relaksacyjny", "Kreatywny"])
        self.combo_theme.currentIndexChanged.connect(self.on_theme_change)
        
        self.layout.addWidget(self.lbl_theme)
        self.layout.addWidget(self.combo_theme)
        
        # Sekcja Języka
        self.lbl_lang = QLabel("Język:")
        self.combo_lang = QComboBox()
        langs = ["Polski", "English", "Português", "Čeština", 
                 "Українська", "Latviešu", "Lietuvių", "Eesti"]
        self.combo_lang.addItems(langs)
        self.combo_lang.currentIndexChanged.connect(self.on_language_change)
        
        self.layout.addWidget(self.lbl_lang)
        self.layout.addWidget(self.combo_lang)
        
        self.layout.addStretch()
        
        self.btn_close = QPushButton("Zamknij")
        self.btn_close.clicked.connect(self.close)
        self.layout.addWidget(self.btn_close)
        
        self.setLayout(self.layout)

    def on_language_change(self, index):
        # Mapowanie indeksów na kody plików (pl.py, en.py, lt.py itd.)
        codes = ["pl", "en", "pt", "cs", "uk", "lv", "lt", "et"]
        if 0 <= index < len(codes):
            self.language_changed.emit(codes[index])

    def on_theme_change(self, index):
        # Mapowanie indeksów na kody motywów
        codes = ["system", "dark", "light", "relax", "creative"]
        if 0 <= index < len(codes):
            self.theme_changed.emit(codes[index])

    def update_texts(self, strings):
        self.setWindowTitle(strings.get("settings", "Ustawienia"))
        self.lbl_theme.setText(strings.get("theme_label", "Motyw:"))
        self.lbl_lang.setText(strings.get("lang_label", "Język:"))
        self.btn_close.setText(strings.get("close", "Zamknij"))

        # Aktualizacja nazw motywów
        self.combo_theme.setItemText(0, strings.get("theme_system", "Systemowy"))
        self.combo_theme.setItemText(1, strings.get("theme_dark", "Ciemny"))
        self.combo_theme.setItemText(2, strings.get("theme_light", "Jasny"))
        self.combo_theme.setItemText(3, strings.get("theme_relax", "Relaksacyjny"))
        self.combo_theme.setItemText(4, strings.get("theme_creative", "Kreatywny"))