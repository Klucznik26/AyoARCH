from PySide6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QComboBox, 
                             QPushButton, QHBoxLayout, QWidget)
from PySide6.QtCore import Signal, Qt

class SettingsWindow(QDialog):
    # Sygnały do komunikacji z głównym oknem
    language_changed = Signal(str)
    theme_changed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setModal(True)
        self.setMinimumWidth(300)

        layout = QVBoxLayout()
        self.setLayout(layout)

        # --- Wybór języka ---
        self.lbl_lang = QLabel("Language:")
        layout.addWidget(self.lbl_lang)

        self.combo_lang = QComboBox()
        # Kod języka, Nazwa wyświetlana
        self.languages = [
            ("pl", "🇵🇱 Polski"),
            ("en", "🇬🇧 English"),
            ("bg", "🇧🇬 Български"),
            ("cs", "🇨🇿 Čeština"),
            ("da", "🇩🇰 Dansk"),
            ("de", "🇩🇪 Deutsch"),
            ("es", "🇪🇸 Español"),
            ("et", "🇪🇪 Eesti"),
            ("fi", "🇫🇮 Suomi"),
            ("fr", "🇫🇷 Français"),
            ("hu", "🇭🇺 Magyar"),
            ("is", "🇮🇸 Íslenska"),
            ("it", "🇮🇹 Italiano"),
            ("lt", "🇱🇹 Lietuvių"),
            ("lv", "🇱🇻 Latviešu"),
            ("nl", "🇳🇱 Nederlands"),
            ("no", "🇳🇴 Norsk"),
            ("pt", "🇵🇹 Português"),
            ("ro", "🇷🇴 Română"),
            ("sk", "🇸🇰 Slovenčina"),
            ("sv", "🇸🇪 Svenska"),
            ("uk", "🇺🇦 Українська"),
            ("el", "🇬🇷 Ελληνικά"),
            ("ka", "🇬🇪 ქართული")
        ]
        
        for code, name in self.languages:
            self.combo_lang.addItem(name, code)

        self.combo_lang.currentIndexChanged.connect(self.on_language_change)
        layout.addWidget(self.combo_lang)

        # --- Wybór motywu ---
        self.lbl_theme = QLabel("Theme:")
        layout.addWidget(self.lbl_theme)

        self.combo_theme = QComboBox()
        # Kod motywu, Nazwa (klucze muszą pasować do apply_theme w ui.py)
        self.themes = [
            ("system", "System"),
            ("dark", "Dark"),
            ("light", "Light"),
            ("relax", "Relax"),
            ("creative", "Creative")
        ]

        for code, name in self.themes:
            self.combo_theme.addItem(name, code)

        self.combo_theme.currentIndexChanged.connect(self.on_theme_change)
        layout.addWidget(self.combo_theme)

        layout.addStretch()

        # Przycisk zamknięcia
        self.btn_close = QPushButton("Close")
        self.btn_close.clicked.connect(self.close)
        layout.addWidget(self.btn_close)

    def on_language_change(self, index):
        lang_code = self.combo_lang.currentData()
        self.language_changed.emit(lang_code)

    def on_theme_change(self, index):
        theme_code = self.combo_theme.currentData()
        self.theme_changed.emit(theme_code)

    def update_texts(self, strings):
        self.setWindowTitle(strings.get("settings", "Settings"))
        self.lbl_lang.setText(strings.get("lang_label", "Language:"))
        self.lbl_theme.setText(strings.get("theme_label", "Theme:"))
        self.btn_close.setText(strings.get("close", "Close"))

        theme_labels = {
            "system": strings.get("theme_system", "System"),
            "dark": strings.get("theme_dark", "Dark"),
            "light": strings.get("theme_light", "Light"),
            "relax": strings.get("theme_relax", "Relax"),
            "creative": strings.get("theme_creative", "Creative"),
        }
        for index in range(self.combo_theme.count()):
            code = self.combo_theme.itemData(index)
            self.combo_theme.setItemText(index, theme_labels.get(code, self.combo_theme.itemText(index)))
