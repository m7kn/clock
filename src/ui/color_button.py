from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QColor

class ColorButton(QPushButton):
    """A custom button for color selection."""

    def __init__(self, color):
        super().__init__()
        self.setColor(color)
        self.setMinimumSize(100, 25)

    def setColor(self, color):
        """Set the button's color and update its appearance."""
        self.color = color
        hex_color = color.name().upper()
        text_color = "#FFFFFF" if self.get_contrast_ratio(color) < 4.5 else "#000000"
        self.setText(hex_color)
        self.setStyleSheet(f"""
            background-color: {hex_color};
            color: {text_color};
            border: 1px solid #bdc3c7;
            border-radius: 4px;
            padding: 5px;
            font-family: monospace;
            font-size: 12px;
        """)

    def get_contrast_ratio(self, color):
        """Calculate the contrast ratio for determining text color."""
        luminance = (0.299 * color.red() + 0.587 * color.green() + 0.114 * color.blue()) / 255
        return (luminance + 0.05) / 0.05 if luminance > 0.5 else 0.05 / (luminance + 0.05)
    