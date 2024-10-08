from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont, QColor, QPainter
import datetime
from utils.font_manager import font_manager

class ClockWidget(QWidget):
    """A widget that displays a digital clock."""

    def __init__(self, config_manager):
        """Initialize the clock widget."""
        super().__init__()
        self.config_manager = config_manager
        self.init_ui()
        self.start_timer()

    def init_ui(self):
        """Set up the user interface for the clock widget."""
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.time_label = QLabel()
        self.time_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.time_label)
        self.setLayout(layout)
        self.update_style()

    def start_timer(self):
        """Start a timer to update the clock every second."""
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # Update every second

    def update_time(self):
        """Update the displayed time."""
        config = self.config_manager.get_config()
        time_format = '%H:%M:%S' if config['clock']['show_seconds'] else '%H:%M'
        current_time = datetime.datetime.now().strftime(time_format)
        self.time_label.setText(current_time)
        self.update()  # Force a repaint

    def update_style(self):
        """Update the style of the clock widget based on the current configuration."""
        config = self.config_manager.get_config()
        self.apply_font(config)
        self.apply_colors(config)
        self.apply_padding(config)

    def apply_font(self, config):
        """Apply font settings to the time label."""
        use_custom_fonts = config['clock']['use_custom_fonts']
        font_name = config['clock']['font']
        font_size = config['clock']['font_size']
        font = font_manager.get_font(font_name, use_custom_fonts)
        font.setPointSize(font_size)
        self.time_label.setFont(font)

    def apply_colors(self, config):
        """Apply color settings to the time label."""
        color = QColor(*config['clock']['color'])
        bg_color = QColor(*config['clock']['background_color'])
        self.time_label.setStyleSheet(f'''
            color: rgba{color.getRgb()};
            background-color: rgba{bg_color.getRgb()};
        ''')
        self.setStyleSheet('background-color: transparent;')

    def apply_padding(self, config):
        """Apply padding settings to the layout."""
        padding_h = config['clock']['padding_horizontal']
        padding_v = config['clock']['padding_vertical']
        if padding_h == 0 and padding_v == 0:
            self.layout().setContentsMargins(0, 0, 0, 0)
        else:
            self.layout().setContentsMargins(padding_h, padding_v, padding_h, padding_v)
        self.time_label.setStyleSheet(self.time_label.styleSheet() + f'''
            padding: {padding_v}px {padding_h}px;
        ''')

    def paintEvent(self, event):
        """Custom paint event to draw the LCD background if needed."""
        super().paintEvent(event)
        config = self.config_manager.get_config()
        if font_manager.is_lcd_font(config['clock']['font']):
            self.draw_lcd_background(config)

    def draw_lcd_background(self, config):
        """Draw the LCD background for the clock."""
        painter = QPainter(self)
        painter.setFont(self.time_label.font())
        color = QColor(*config['clock']['color'])
        lcd_opacity = config['clock']['lcd_background_opacity']
        painter.setPen(QColor(color.red(), color.green(), color.blue(), lcd_opacity))
        rect = self.time_label.geometry()
        painter.drawText(rect, Qt.AlignCenter, self.get_background_text(config))

    def get_background_text(self, config):
        """Get the background text for the LCD display."""
        return "88:88:88" if config['clock']['show_seconds'] else "88:88"

    def update_config(self):
        """Update the widget's style and time display after a configuration change."""
        self.update_style()
        self.update_time()
        