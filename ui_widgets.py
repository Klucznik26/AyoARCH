from PySide6.QtWidgets import QPushButton
from PySide6.QtGui import QPainter, QPen, QColor
from PySide6.QtCore import Qt, Signal


class HoverButton(QPushButton):
    hovered = Signal(str, str, str) # flag, native_name, code
    left = Signal()

    def __init__(self, flag, native_name, code, parent=None):
        super().__init__("", parent)
        self.flag = flag
        self.native_name = native_name
        self.code = code
        self._hovered = False
        self._tile_size = 56
        self._normal_font_px = 46
        self._hover_font_px = 60
        self.setFixedSize(72, 72)
        self.setFlat(True)
        self.setStyleSheet("background: transparent; border: none;")
        self.setCursor(Qt.PointingHandCursor)

    def enterEvent(self, event):
        self._hovered = True
        self.raise_()
        self.update()
        self.hovered.emit(self.flag, self.native_name, self.code)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._hovered = False
        self.update()
        self.left.emit()
        super().leaveEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        try:
            painter.setRenderHint(QPainter.Antialiasing, True)

            tile_color = QColor(255, 255, 255, 80 if self._hovered else 62)
            border_color = QColor(255, 255, 255, 190 if self._hovered else 148)

            x = (self.width() - self._tile_size) // 2
            y = (self.height() - self._tile_size) // 2
            tile_rect = self.rect().adjusted(
                x,
                y,
                -(self.width() - self._tile_size - x),
                -(self.height() - self._tile_size - y)
            )

            painter.setBrush(tile_color)
            painter.setPen(QPen(border_color, 1))
            painter.drawRoundedRect(tile_rect, 12, 12)

            font = self.font()
            font.setPixelSize(self._hover_font_px if self._hovered else self._normal_font_px)
            font.setBold(False)
            painter.setFont(font)
            painter.setPen(self.palette().color(self.foregroundRole()))
            painter.drawText(self.rect(), Qt.AlignCenter, self.flag)
        finally:
            painter.end()
