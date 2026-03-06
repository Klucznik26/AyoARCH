SYSTEM_THEME = """
/* =========================
   MOTYW SYSTEMOWY
   (Pozostawiamy puste, aby zachować natywny wygląd OS)
   ========================= */

/* QMainWindow - System default */
/* QDialog - System default */

/* =========================
   RAMKI / PANELE
   ========================= */
/* QFrame - System default */

/* =========================
   TEKST
   ========================= */
/* QLabel - System default */

/* =========================
   PRZYCISKI
   ========================= */
/* QPushButton - System default */

/* =========================
   PRZYCISK WYKONAJ (AKCENT)
   ========================= */
/* QPushButton#runButton - System default */

/* =========================
   SUWAK SKALI
   ========================= */
/* QSlider - System default */

/* =========================
   KONTROLKI FORMULARZY
   ========================= */
/* QComboBox - System default */
/* QListView, QTreeView - System default */
/* QHeaderView - System default */
/* QLineEdit - System default */

/* =========================
   NARZĘDZIA
   ========================= */
/* QToolButton - System default */
"""

DROP_ZONE = """
    QLabel {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 rgba(128, 128, 128, 0.2), stop:1 rgba(128, 128, 128, 0.05));
        border: 2px dashed palette(mid);
        border-radius: 8px;
        color: palette(text);
        font-size: 16px;
    }
"""