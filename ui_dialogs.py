import os
import zipfile

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton, QSizePolicy,
    QListWidget, QListWidgetItem, QAbstractItemView, QHBoxLayout,
    QFileDialog, QMessageBox, QWidget, QGridLayout
)
from PySide6.QtGui import QPixmap, QIcon, QDragEnterEvent, QDropEvent
from PySide6.QtCore import Qt, QTimer, QSize, Signal

from ui_widgets import HoverButton


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

class LanguageSelectionDialog(QDialog):
    language_selected = Signal(str)

    def __init__(self, parent=None, strings=None):
        super().__init__(parent)
        self.strings = strings or {}
        title = self.strings.get("select_language_title", self.strings.get("lang_label", "Wybierz język")).rstrip(":")
        self.setWindowTitle(title)
        self.setModal(True)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        grid_widget = QWidget()
        grid_layout = QGridLayout(grid_widget)
        grid_layout.setSpacing(8)
        
        # Label informacyjny nad siatką
        self.info_label = QLabel(" ")
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setStyleSheet(
            "font-size: 18px; font-weight: normal; color: palette(text); "
            "padding: 10px 14px; "
            "background-color: rgba(255, 255, 255, 0.32); "
            "border: 1px solid rgba(255, 255, 255, 0.58); "
            "border-radius: 12px;"
        )
        layout.addWidget(self.info_label)
        
        # Lista języków z flagami
        languages = [
            ("pl", "🇵🇱 Polski"), ("en", "🇬🇧 English"), ("bg", "🇧🇬 Български"),
            ("cs", "🇨🇿 Čeština"), ("da", "🇩🇰 Dansk"), ("de", "🇩🇪 Deutsch"),
            ("es", "🇪🇸 Español"), ("et", "🇪🇪 Eesti"), ("fi", "🇫🇮 Suomi"),
            ("fr", "🇫🇷 Français"), ("hu", "🇭🇺 Magyar"), ("is", "🇮🇸 Íslenska"),
            ("it", "🇮🇹 Italiano"), ("lt", "🇱🇹 Lietuvių"), ("lv", "🇱🇻 Latviešu"),
            ("nl", "🇳🇱 Nederlands"), ("no", "🇳🇴 Norsk"), ("pt", "🇵🇹 Português"),
            ("ro", "🇷🇴 Română"), ("sk", "🇸🇰 Slovenčina"), ("sv", "🇸🇪 Svenska"),
            ("uk", "🇺🇦 Українська"), ("el", "🇬🇷 Ελληνικά"), ("ka", "🇬🇪 ქართული")
        ]
        self.native_names = {
            code: (name.split(' ', 1)[1] if ' ' in name else name) for code, name in languages
        }
        
        columns = 6
        
        for i, (code, name) in enumerate(languages):
            row = i // columns
            col = i % columns
            
            flag = name.split(' ')[0]
            # Wyciągamy nazwę języka z listy (np. "Polski" z "🇵🇱 Polski")
            native_name = name.split(' ', 1)[1] if ' ' in name else name
            
            btn = HoverButton(flag, native_name, code)
            
            btn.clicked.connect(lambda checked=False, c=code: (self.language_selected.emit(c), self.accept()))
            btn.hovered.connect(self.on_hover)
            btn.left.connect(self.on_leave)
            grid_layout.addWidget(btn, row, col)
            
        layout.addWidget(grid_widget)

    def on_hover(self, flag, native_name, code):
        localized_name = native_name
        parent = self.parent()
        if parent and hasattr(parent, "strings"):
            localized_name = parent.strings.get(f"lang_{code}", native_name)

        if localized_name == native_name:
            self.info_label.setText(native_name)
        else:
            self.info_label.setText(f"{native_name} — {localized_name}")

    def on_leave(self):
        self.info_label.setText(" ")

class InfoDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(parent.strings.get("app_info", "Information") if parent else "Information")
        self.setModal(True)
        self.setMinimumWidth(640)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        current_theme = getattr(parent, "current_theme", "dark") if parent else "dark"
        text_color = "#EAF0FF" if current_theme in ("dark", "creative", "system") else "#1F2A35"
        glass_bg = "rgba(255, 255, 255, 0.26)"
        glass_border = "rgba(255, 255, 255, 0.45)"

        # Logo (bez kafelka, bezpośrednio na tle okna)
        logo_label = QLabel()
        logo_label.setAlignment(Qt.AlignCenter)
        logo_label.setStyleSheet("background: transparent; border: none;")
        assets_dir = os.path.join(os.path.dirname(__file__), "assets")
        logo_path = os.path.join(assets_dir, "AARCH.png")
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            if not pixmap.isNull():
                logo_label.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        layout.addWidget(logo_label)
        
        # Title
        title_label = QLabel("Ayo Archi")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(
            f"font-size: 24px; font-weight: bold; color: {text_color}; "
            f"padding: 10px 16px; background-color: {glass_bg}; "
            f"border: 1px solid {glass_border}; border-radius: 14px;"
        )
        layout.addWidget(title_label)
        
        # Version
        version = getattr(parent, "APP_VERSION", "1.5.5") if parent else "1.5.5"
        ver_label = QLabel(f"v {version}")
        ver_label.setAlignment(Qt.AlignCenter)
        ver_label.setStyleSheet(
            f"font-size: 16px; color: {text_color}; "
            f"padding: 8px 14px; background-color: {glass_bg}; "
            f"border: 1px solid {glass_border}; border-radius: 12px;"
        )
        layout.addWidget(ver_label)
        
        # Description
        s = parent.strings if parent else {}
        
        glass_text_style = (
            f"font-size: 14px; color: {text_color}; "
            "padding: 12px 16px; "
            f"background-color: {glass_bg}; "
            f"border: 1px solid {glass_border}; "
            "border-radius: 14px;"
        )

        desc1 = QLabel(s.get("info_desc_1", "Ayo Archi is a fast and lightweight desktop application\nfor browsing images directly inside archive files."))
        desc1.setAlignment(Qt.AlignCenter)
        desc1.setWordWrap(True)
        desc1.setMinimumHeight(86)
        desc1.setStyleSheet(glass_text_style)
        layout.addWidget(desc1)

        desc2 = QLabel(s.get("info_desc_2", "Supports ZIP, 7Z, RAR, CBZ and CBR archives\nwithout extracting them to disk."))
        desc2.setAlignment(Qt.AlignCenter)
        desc2.setWordWrap(True)
        desc2.setMinimumHeight(86)
        desc2.setStyleSheet(glass_text_style)
        layout.addWidget(desc2)

        desc3 = QLabel(s.get("info_desc_3", "Part of the Ayo creative tools ecosystem."))
        desc3.setAlignment(Qt.AlignCenter)
        desc3.setWordWrap(True)
        desc3.setMinimumHeight(72)
        desc3.setStyleSheet(glass_text_style)
        layout.addWidget(desc3)
        
        layout.addStretch()
        
        # Close button
        btn_close = QPushButton(parent.strings.get("close", "Close") if parent else "Close")
        btn_close.setCursor(Qt.PointingHandCursor)
        btn_close.clicked.connect(self.accept)
        btn_close.setObjectName("runButton")
        layout.addWidget(btn_close)

class ThemeSelectionDialog(QDialog):
    theme_selected = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        s = getattr(parent, 'strings', {}) if parent else {}
        title = s.get("select_theme_title", s.get("theme_label", "Wybierz motyw")).rstrip(":")
        self.setWindowTitle(title)
        self.setModal(True)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        grid_widget = QWidget()
        grid_layout = QGridLayout(grid_widget)
        grid_layout.setSpacing(15)
        
        # Label informacyjny nad siatką
        self.info_label = QLabel(" ")
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setStyleSheet(
            "font-size: 18px; font-weight: normal; color: palette(text); "
            "padding: 10px 14px; "
            "background-color: rgba(255, 255, 255, 0.32); "
            "border: 1px solid rgba(255, 255, 255, 0.58); "
            "border-radius: 12px;"
        )
        layout.addWidget(self.info_label)
        
        themes = [
            ("dark", s.get("theme_dark", "Ciemny"), "🌙"),
            ("light", s.get("theme_light", "Jasny"), "☀️"),
            ("creative", s.get("theme_creative", "Kreatywny"), "🎨"),
            ("relax", s.get("theme_relax", "Relaksacyjny"), "🌿"),
            ("arctic", s.get("theme_arctic", "Arktyczny"), "❄️"),
            ("system", s.get("theme_system", "Systemowy"), "🖥️")
        ]
        
        columns = 3
        
        for i, (code, name, icon) in enumerate(themes):
            row = i // columns
            col = i % columns
            
            btn = HoverButton(icon, name, code)
            
            btn.clicked.connect(lambda checked=False, c=code: (self.theme_selected.emit(c), self.accept()))
            btn.hovered.connect(self.on_hover)
            btn.left.connect(self.on_leave)
            grid_layout.addWidget(btn, row, col)
            
        layout.addWidget(grid_widget)

    def on_hover(self, flag, native_name, code):
        self.info_label.setText(native_name)

    def on_leave(self):
        self.info_label.setText(" ")
