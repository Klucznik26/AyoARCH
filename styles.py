from themes.dark import DARK_THEME, DROP_ZONE as DROP_ZONE_DARK
from themes.light import LIGHT_THEME, DROP_ZONE as DROP_ZONE_LIGHT
from themes.creative import CREATIVE_THEME as CREATIVE_THEME_BASE, DROP_ZONE as DROP_ZONE_CREATIVE_BASE
from themes.relax import RELAX_THEME as RELAX_THEME_BASE, DROP_ZONE as DROP_ZONE_RELAX_BASE
from themes.arctic import ARCTIC_THEME as ARCTIC_THEME_BASE, DROP_ZONE as DROP_ZONE_ARCTIC_BASE
from themes.system import SYSTEM_THEME as SYSTEM_THEME_BASE, DROP_ZONE as DROP_ZONE_SYSTEM_BASE

# Styl dla panelu bocznego
SIDEBAR_STYLE = """
    QFrame#leftPanel, QFrame#rightPanel {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 rgba(255, 255, 255, 0.20), stop:1 rgba(255, 255, 255, 0.08));
        border-radius: 14px;
        border: 1px solid rgba(255,255,255,0.40);
    }
    QFrame#narrowPanel {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 rgba(0, 0, 0, 0.25), stop:1 rgba(0, 0, 0, 0.15));
        border-radius: 14px;
        border: 1px solid rgba(255,255,255,0.1);
    }
    QPushButton#iconButton {
        background-color: transparent;
        border: none;
        font-size: 24px;
        padding: 8px;
        color: rgba(255, 255, 255, 0.85);
    }
    QPushButton#iconButton:hover {
        background-color: rgba(255, 255, 255, 0.15);
        border-radius: 10px;
    }
    QPushButton#iconButton[danger="true"] {
        color: #ff5a5a;
    }
    QPushButton#iconButton[danger="true"]:hover {
        color: #ff7a7a;
        background-color: rgba(255, 90, 90, 0.18);
        border-radius: 10px;
    }
"""

# --- GŁÓWNE STYLE ---
MAIN_STYLE = DARK_THEME + SIDEBAR_STYLE
DROP_ZONE_STYLE = DROP_ZONE_DARK

# --- STYLE DLA INNYCH MOTYWÓW ---

# Light
LIGHT_STYLE = LIGHT_THEME + SIDEBAR_STYLE
DROP_ZONE_STYLE_LIGHT = DROP_ZONE_LIGHT

# Relax
RELAX_THEME = RELAX_THEME_BASE + SIDEBAR_STYLE
DROP_ZONE_STYLE_RELAX = DROP_ZONE_RELAX_BASE

# Creative
CREATIVE_THEME = CREATIVE_THEME_BASE + SIDEBAR_STYLE
DROP_ZONE_STYLE_CREATIVE = DROP_ZONE_CREATIVE_BASE

# Arctic
ARCTIC_SIDEBAR_STYLE = """
    QFrame#leftPanel, QFrame#rightPanel {
        background: qlineargradient(
            x1:0, y1:0, x2:1, y2:1,
            stop:0 rgba(220, 245, 255, 0.26),
            stop:1 rgba(120, 210, 255, 0.10)
        );
        border-radius: 14px;
        border: 1px solid rgba(140, 225, 255, 0.45);
    }
    QFrame#narrowPanel {
        background: qlineargradient(
            x1:0, y1:0, x2:0, y2:1,
            stop:0 rgba(120, 220, 255, 0.30),
            stop:0.55 rgba(80, 170, 220, 0.22),
            stop:1 rgba(40, 120, 175, 0.32)
        );
        border-radius: 14px;
        border: 1px solid rgba(165, 236, 255, 0.55);
    }
    QPushButton#iconButton {
        background-color: transparent;
        border: none;
        font-size: 24px;
        padding: 8px;
        color: #E7FBFF;
    }
    QPushButton#iconButton:hover {
        background-color: rgba(165, 236, 255, 0.24);
        border-radius: 10px;
    }
    QPushButton#iconButton[danger="true"] {
        color: #ff5a5a;
    }
    QPushButton#iconButton[danger="true"]:hover {
        color: #ff7a7a;
        background-color: rgba(255, 90, 90, 0.18);
        border-radius: 10px;
    }
"""
ARCTIC_THEME = ARCTIC_THEME_BASE + ARCTIC_SIDEBAR_STYLE
DROP_ZONE_STYLE_ARCTIC = DROP_ZONE_ARCTIC_BASE

# System (pusty styl, Qt użyje systemowego)
SYSTEM_THEME = SYSTEM_THEME_BASE + SIDEBAR_STYLE
DROP_ZONE_STYLE_SYSTEM = DROP_ZONE_SYSTEM_BASE

# Styl dla brakującego logo
LOGO_STYLE_MISSING = """
    QLabel {
        color: #888;
        font-weight: bold;
        font-size: 24px;
        border: 2px solid #555;
        border-radius: 10px;
        padding: 10px;
    }
"""
