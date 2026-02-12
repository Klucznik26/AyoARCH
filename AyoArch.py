import sys
import zipfile
from io import BytesIO
from PySide6.QtWidgets import (QApplication, QMainWindow, QLabel, 
                             QVBoxLayout, QWidget, QPushButton, QFileDialog)
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt

class AyoArch(QMainWindow):
    def __init__(self):
        super().__init__()
        # Nazwa projektu zgodna z Twoim pomysłem
        self.setWindowTitle("Ayo Arch v0.0.1 - Archive Viewer")
        self.setMinimumSize(800, 600)

        # Interfejs
        self.layout = QVBoxLayout()
        self.image_label = QLabel("Przeciągnij tutaj plik .zip lub użyj przycisku")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("border: 2px dashed #666; color: #aaa;")
        
        self.btn_open = QPushButton("Otwórz Archiwum ZIP")
        self.btn_open.clicked.connect(self.load_zip)

        self.layout.addWidget(self.image_label)
        self.layout.addWidget(self.btn_open)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def load_zip(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Wybierz archiwum", "", "Archives (*.zip)")
        if file_path:
            self.display_first_image(file_path)

    def display_first_image(self, zip_path):
        try:
            with zipfile.ZipFile(zip_path, 'r') as z:
                # Szukamy plików graficznych
                images = [f for f in z.namelist() if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
                if images:
                    with z.open(images[0]) as f:
                        data = f.read()
                        img = QImage.fromData(data)
                        pixmap = QPixmap.fromImage(img)
                        # Skalowanie do okna
                        scaled = pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                        self.image_label.setPixmap(scaled)
                else:
                    self.image_label.setText("Brak obrazów w ZIP!")
        except Exception as e:
            self.image_label.setText(f"Błąd: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AyoArch()
    window.show()
    sys.exit(app.exec())