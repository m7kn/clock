from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont, QColor
import datetime

class ClockWidget(QWidget):
    def __init__(self, config_manager):
        super().__init__()
        self.config_manager = config_manager
        self.init_ui()
        self.start_timer()

    def init_ui(self):
        layout = QVBoxLayout()
        self.time_label = QLabel()
        layout.addWidget(self.time_label, alignment=Qt.AlignCenter)
        self.setLayout(layout)
        self.update_style()

    def start_timer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # Update every second

    def update_time(self):
        config = self.config_manager.get_config()
        if config['clock']['show_seconds']:
            time_format = '%H:%M:%S'
        else:
            time_format = '%H:%M'
        current_time = datetime.datetime.now().strftime(time_format)
        self.time_label.setText(current_time)

    def update_style(self):
        config = self.config_manager.get_config()
        font = QFont(config['clock']['font'], config['clock']['font_size'])
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
        
        self.setStyleSheet(f'background-color: transparent;')
        
        # Ha mindkét padding 0, akkor állítsuk be a layout margóját 0-ra
        if padding_h == 0 and padding_v == 0:
            self.layout().setContentsMargins(0, 0, 0, 0)
        else:
            self.layout().setContentsMargins(padding_h, padding_v, padding_h, padding_v)        

    def update_config(self):
        self.update_style()
        self.update_time()
        