LIGHT_THEME = """
/* =========================
   MOTYW JASNY (BEŻOWY)
   ========================= */

QMainWindow {
    background-color: #EFE6D6;
}

QDialog {
    background-color: #EFE6D6;
}

/* =========================
   RAMKI / PANELE
   ========================= */
QFrame {
    background-color: #F6F0E6;
    border: 1px solid #B8A890;
}

/* =========================
   TEKST
   ========================= */
QLabel {
    color: #3A2E24;
}

QLabel[secondary="true"] {
    color: #7D6E5F;
}

/* =========================
   PRZYCISKI
   ========================= */
QPushButton {
    padding: 8px 14px;
    background-color: #E3D8C6;
    border: 1px solid #B8A890;
    border-radius: 6px;
    color: #3A2E24;
}

QPushButton:hover {
    background-color: #D6C9B5;
}

QPushButton:pressed {
    background-color: #CBBDA7;
}

QPushButton:disabled {
    background-color: #E0D6C8;
    color: #9C8F80;
    border-color: #C9BCA8;
}

/* =========================
   PRZYCISK WYKONAJ (AKCENT)
   ========================= */
QPushButton#runButton {
    background-color: #8C5E3C; /* Ciepły brąz */
    border: none;
    color: #F6F0E6;
}

QPushButton#runButton:hover {
    background-color: #A3704C;
}

QPushButton#runButton:pressed {
    background-color: #754C30;
}

/* =========================
   SUWAK SKALI
   ========================= */
QSlider::groove:horizontal {
    height: 6px;
    background: #D6C9B5;
    border-radius: 3px;
}

QSlider::handle:horizontal {
    background: #8C5E3C;
    width: 16px;
    margin: -5px 0;
    border-radius: 8px;
}

QSlider::sub-page:horizontal {
    background: #6B462B;
    border-radius: 3px;
}

QSlider::add-page:horizontal {
    background: #D6C9B5;
    border-radius: 3px;
}

/* =========================
   KONTROLKI FORMULARZY
   ========================= */
QComboBox {
    background-color: #E3D8C6;
    color: #3A2E24;
    border: 1px solid #B8A890;
    padding: 4px;
}

QComboBox::drop-down {
    border: none;
}

QListView, QTreeView {
    background-color: #F6F0E6;
    color: #3A2E24;
    border: 1px solid #B8A890;
    outline: none;
}

QTreeView::item:selected, QListView::item:selected {
    background-color: #8C5E3C;
    color: #F6F0E6;
}

QHeaderView::section {
    background-color: #E3D8C6;
    color: #3A2E24;
    border: none;
    padding: 4px;
}

QLineEdit {
    background-color: #F6F0E6;
    color: #3A2E24;
    border: 1px solid #B8A890;
    border-radius: 4px;
}

/* =========================
   NARZĘDZIA
   ========================= */
QToolButton {
    background-color: transparent;
    border: none;
    border-radius: 4px;
    color: #3A2E24;
    padding: 4px;
}

QToolButton:hover {
    background-color: #D6C9B5;
}

QToolButton:pressed {
    background-color: #CBBDA7;
}
"""

DROP_ZONE = """
    QLabel {
        border: 2px dashed #B8A890;
        border-radius: 8px;
        color: #3A2E24;
        font-size: 16px;
        background-color: #F6F0E6;
    }
"""