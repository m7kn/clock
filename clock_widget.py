from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont, QColor
import datetime
from font_manager import font_manager

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
        self.time_label = QLabel()
        layout.addWidget(self.time_label, alignment=Qt.AlignCenter)
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

    def update_style(self):
        """Update the style of the clock widget based on the current configuration."""
        config = self.config_manager.get_config()
        use_custom_fonts = config['clock']['use_custom_fonts']
        font_name = config['clock']['font']
        font_size = config['clock']['font_size']        
        font = font_manager.get_font(font_name, use_custom_fonts)
        font.setPointSize(font_size)
        self.time_label.setFont(font)
        color = QColor(*config['clock']['color'])
        bg_color = QColor(*config['clock']['background_color'])
        padding_h = config['clock']['padding_horizontal']
        padding_v = config['clock']['padding_vertical']
        
        self.time_label.setStyleSheet(f'''
            color: rgba{color.getRgb()};
            background-color: rgba{bg_color.getRgb()};
            padding: {padding_v}px {padding_h}px;
        ''')
        
        self.setStyleSheet('background-color: transparent;')
        
        # Set layout margins to 0 if both paddings are 0
        if padding_h == 0 and padding_v == 0:
            self.layout().setContentsMargins(0, 0, 0, 0)
        else:
            self.layout().setContentsMargins(padding_h, padding_v, padding_h, padding_v)
        
        # Set fixed size based on maximum possible time string
        # max_time = "00:00:00" if config['clock']['show_seconds'] else "00:00"
        # self.time_label.setText(max_time)
        # self.time_label.adjustSize()
        # size = self.time_label.sizeHint()
        # self.time_label.setFixedSize(size)
        # self.setFixedSize(size)      

    def update_config(self):
        """Update the widget's style and time display after a configuration change."""
        self.update_style()
        self.update_time()
        