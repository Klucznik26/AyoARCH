DARK_THEME = """
/* =========================
   MOTYW CIEMNY (DARK)
   ========================= */

QMainWindow {
    background-color: #1E1F22;
}

QDialog {
    background-color: #1E1F22;
    color: #E6E6E6;
}

/* =========================
   RAMKI / PANELE
   ========================= */
QFrame {
    background-color: #2A2C30;
    border: 1px solid #44474E;
}

/* =========================
   TEKST
   ========================= */
QLabel {
    color: #E6E6E6;
}

QLabel[secondary="true"] {
    color: #A7A9AC;
}

/* =========================
   PRZYCISKI
   ========================= */
QPushButton {
    padding: 8px 14px;
    background-color: #34363B;
    border: 1px solid #44474E;
    border-radius: 8px;
    color: #E6E6E6;
}

QPushButton:hover {
    background-color: #3E4045;
}

QPushButton:pressed {
    background-color: #2B2D32;
}

QPushButton:disabled {
    background-color: #2A2C30;
    color: #A7A9AC;
    border-color: #44474E;
}

/* =========================
   PRZYCISK WYKONAJ (AKCENT)
   ========================= */
QPushButton#runButton {
    background-color: #C96A3A;
    border: none;
    color: #FFFFFF;
}

QPushButton#runButton:hover {
    background-color: #D47B4B;
}

QPushButton#runButton:pressed {
    background-color: #A8552F;
}

/* =========================
   SUWAK SKALI
   ========================= */
QSlider::groove:horizontal {
    height: 6px;
    background: #34363B;
    border-radius: 3px;
}

QSlider::handle:horizontal {
    background: #C96A3A;
    width: 16px;
    margin: -5px 0;
    border-radius: 8px;
}

QSlider::sub-page:horizontal {
    background: #A8552F;
    border-radius: 3px;
}

QSlider::add-page:horizontal {
    background: #34363B;
    border-radius: 3px;
}

/* =========================
   KONTROLKI FORMULARZY
   ========================= */
QComboBox {
    background-color: #34363B;
    color: #E6E6E6;
    border: 1px solid #44474E;
    padding: 4px;
}

QComboBox::drop-down {
    border: none;
}

QListView, QTreeView {
    background-color: #2A2C30;
    color: #E6E6E6;
    border: 1px solid #44474E;
    outline: none;
}

QTreeView::item:selected, QListView::item:selected {
    background-color: #C96A3A;
    color: #FFFFFF;
}

QHeaderView::section {
    background-color: #34363B;
    color: #E6E6E6;
    border: none;
    padding: 4px;
}

QLineEdit {
    background-color: #34363B;
    color: #E6E6E6;
    border: 1px solid #44474E;
    border-radius: 4px;
}

/* =========================
   NARZĘDZIA
   ========================= */
QToolButton {
    background-color: transparent;
    border: none;
    border-radius: 4px;
    color: #E6E6E6;
    padding: 4px;
}

QToolButton:hover {
    background-color: #34363B;
}

QToolButton:pressed {
    background-color: #2A2C30;
}
"""

DROP_ZONE = """
    QLabel {
        border: 2px dashed #44474E;
        border-radius: 8px;
        color: #E6E6E6;
        font-size: 16px;
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 rgba(255, 255, 255, 0.15), stop:1 rgba(255, 255, 255, 0.02));
    }
"""