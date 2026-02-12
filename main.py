import sys
import os

# Dodajemy katalog projektu do ścieżki systemowej
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PySide6.QtWidgets import QApplication
from ui import AyoArch

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AyoArch()
    window.show()
    sys.exit(app.exec())