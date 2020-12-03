from PySide2.QtCore import Property, QPropertyAnimation
from PySide2.QtGui import QColor
from PySide2.QtWidgets import QHBoxLayout, QLabel, QPushButton, QWidget


class LabelButton(QWidget):
    def __init__(self, label_text, button_text):
        super().__init__()

        layout = QHBoxLayout(self)

        self.label = QLabel(label_text)
        self.button = QPushButton(button_text)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.label)
        layout.addWidget(self.button)


class BlinkLabel(QLabel):
    def __init__(self, *args, **kwargs):
        blink_color = kwargs.get('blink_color') or QColor(0, 255, 0)
        kwargs.pop('blink_color')
        super().__init__(*args, **kwargs)

        self.animation = QPropertyAnimation(self, b"color")
        self.animation.setDuration(300)
        self.animation.setStartValue(self.color)
        self.animation.setEndValue(self.color)
        self.animation.setKeyValueAt(0.5, blink_color)

    def blink(self):
        self.animation.start()

    def get_color(self):
        return self.palette().text()

    def set_color(self, color):
        palette = self.palette()
        palette.setColor(self.foregroundRole(), color)
        self.setPalette(palette)

    color = Property(QColor, get_color, set_color)
