RELAX_THEME = """
/* =========================
   MOTYW RELAKSACYJNY (NATURE)
   ========================= */

QMainWindow {
    background-color: #B7C7A3;
}

QDialog {
    background-color: #B7C7A3;
    color: #2F3E36;
}

/* =========================
   RAMKI / PANELE
   ========================= */
QFrame {
    background-color: #E7E3D8;
    border: 1px solid #7FA37B;
}

/* =========================
   TEKST
   ========================= */
QLabel {
    color: #2F3E36;
}

QLabel[secondary="true"] {
    color: #6B7F72;
}

/* =========================
   PRZYCISKI
   ========================= */
QPushButton {
    padding: 8px 14px;
    background-color: #E7E3D8;
    border: 1px solid #7FA37B;
    border-radius: 6px;
    color: #2F3E36;
}

QPushButton:hover {
    background-color: #F2EFE7;
}

QPushButton:pressed {
    background-color: #D7D3C8;
}

QPushButton:disabled {
    background-color: #C9D2BE;
    color: #6B7F72;
    border: 1px solid #7FA37B;
}

/* =========================
   PRZYCISK WYKONAJ (AKCENT)
   ========================= */
QPushButton#runButton {
    background-color: #6A9C6B;
    border: none;
    color: #FFFFFF;
}

QPushButton#runButton:hover {
    background-color: #8FBF8F;
}

QPushButton#runButton:pressed {
    background-color: #4F7A52;
}

/* =========================
   SUWAK SKALI
   ========================= */
QSlider::groove:horizontal {
    height: 6px;
    background: #E7E3D8;
    border-radius: 3px;
}

QSlider::handle:horizontal {
    background: #6A9C6B;
    width: 16px;
    margin: -5px 0;
    border-radius: 8px;
}

QSlider::sub-page:horizontal {
    background: #4F7A52;
    border-radius: 3px;
}

QSlider::add-page:horizontal {
    background: #E7E3D8;
    border-radius: 3px;
}

/* =========================
   KONTROLKI FORMULARZY
   ========================= */
QComboBox {
    background-color: #F0EDE5; /* Karta robocza */
    color: #2F3E36;
    border: 1px solid #7FA37B;
    padding: 4px;
}

QComboBox::drop-down {
    border: none;
}

QListView, QTreeView {
    background-color: #F0EDE5;
    color: #2F3E36;
    border: 1px solid #7FA37B;
    outline: none;
}

QTreeView::item:selected, QListView::item:selected {
    background-color: #6A9C6B;
    color: #FFFFFF;
}

QHeaderView::section {
    background-color: #E7E3D8;
    color: #2F3E36;
    border: none;
    padding: 4px;
}

QLineEdit {
    background-color: #F0EDE5;
    color: #2F3E36;
    border: 1px solid #7FA37B;
    border-radius: 4px;
}

/* =========================
   NARZĘDZIA
   ========================= */
QToolButton {
    background-color: transparent;
    border: none;
    border-radius: 4px;
    color: #2F3E36;
    padding: 4px;
}

QToolButton:hover {
    background-color: #E7E3D8;
}

QToolButton:pressed {
    background-color: #D7D3C8;
}
"""

DROP_ZONE = """
    QLabel {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 rgba(106, 156, 107, 0.25), stop:1 rgba(106, 156, 107, 0.05));
        border: 2px dashed #6A9C6B;
        border-radius: 10px;
        color: #6A9C6B;
        font-size: 18px;
    }
"""