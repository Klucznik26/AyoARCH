from themes.dark import DARK_THEME, DROP_ZONE as DROP_ZONE_DARK
from themes.light import LIGHT_THEME, DROP_ZONE as DROP_ZONE_LIGHT
from themes.creative import CREATIVE_THEME as CREATIVE_THEME_BASE, DROP_ZONE as DROP_ZONE_CREATIVE_BASE
from themes.relax import RELAX_THEME as RELAX_THEME_BASE, DROP_ZONE as DROP_ZONE_RELAX_BASE
from themes.system import SYSTEM_THEME as SYSTEM_THEME_BASE, DROP_ZONE as DROP_ZONE_SYSTEM_BASE

# Styl dla panelu bocznego
SIDEBAR_STYLE = """
    QFrame#leftPanel, QFrame#rightPanel {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 rgba(255, 255, 255, 0.20), stop:1 rgba(255, 255, 255, 0.08));
        border-radius: 14px;
        border: 1px solid rgba(255,255,255,0.40);
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