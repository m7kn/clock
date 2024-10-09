from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QSizePolicy
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont, QColor, QPainter
import datetime
from utils.font_manager import font_manager

class ClockWidget(QWidget):
    """A widget that displays a digital clock with separate elements."""

    def __init__(self, config_manager):
        """Initialize the clock widget."""
        super().__init__()
        self.config_manager = config_manager
        self.clock_elements = {
            'hours': {'label': QLabel(), 'format': '%H'},
            'separator1': {'label': QLabel(':'), 'format': ':'},
            'minutes': {'label': QLabel(), 'format': '%M'},
            'separator2': {'label': QLabel(':'), 'format': ':'},
            'seconds': {'label': QLabel(), 'format': '%S'}
        }
        self.init_ui()
        self.start_timer()

    def init_ui(self):
        """Set up the user interface for the clock widget."""
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        for key, element in self.clock_elements.items():
            label = element['label']
            label.setAlignment(Qt.AlignCenter)
            label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            layout.addWidget(label)
        
        self.setLayout(layout)
        self.update_style()

    def start_timer(self):
        """Start a timer to update the clock every second."""
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # Update every second

    def update_time(self):
        """Update the displayed time for each element."""
        current_time = datetime.datetime.now()
        config = self.config_manager.get_config()
        
        for key, element in self.clock_elements.items():
            if key == 'seconds' and not config['clock']['show_seconds']:
                element['label'].hide()
                self.clock_elements['separator2']['label'].hide()
            else:
                element['label'].setText(current_time.strftime(element['format']))
                element['label'].show()
                if key == 'minutes':
                    self.clock_elements['separator2']['label'].show()
        
        self.update()

    def update_style(self):
        """Update the style of each clock element based on the current configuration."""
        config = self.config_manager.get_config()
        for key, element in self.clock_elements.items():
            self.apply_font(config, element['label'], key)
            self.apply_colors(config, element['label'], key)
        self.apply_padding(config)
        self.adjust_layout()
        self.update()

    def apply_font(self, config, label, element_key):
        """Apply font settings to a specific clock element."""
        use_custom_fonts = config['clock']['use_custom_fonts']
        font_name = config['clock']['font']
        font_size = config['clock']['font_size']
        if element_key == 'seconds':
            font_size = config['clock']['seconds_font_size']
        font = font_manager.get_font(font_name, use_custom_fonts)
        font.setPointSize(font_size)
        label.setFont(font)

    def apply_colors(self, config, label, element_key):
        """Apply color settings to a specific clock element."""
        if element_key == 'seconds':
            color = QColor(*config['clock']['seconds_color'])
        else:
            color = QColor(*config['clock']['color'])
        bg_color = QColor(*config['clock']['background_color'])
        label.setStyleSheet(f'''
            color: rgba{color.getRgb()};
            background-color: rgba{bg_color.getRgb()};
        ''')

    def apply_padding(self, config):
        """Apply padding settings to the layout."""
        padding_h = config['clock']['padding_horizontal']
        padding_v = config['clock']['padding_vertical']
        self.layout().setContentsMargins(padding_h, padding_v, padding_h, padding_v)
        
        background_color = QColor(*config['clock']['background_color'])
        self.setStyleSheet(f'''
            QWidget {{
                background-color: rgba({background_color.red()}, {background_color.green()}, {background_color.blue()}, {background_color.alpha()});
            }}
        ''')

    def paintEvent(self, event):
        """Custom paint event to draw the LCD background if needed."""
        super().paintEvent(event)
        config = self.config_manager.get_config()
        if font_manager.is_lcd_font(config['clock']['font']):
            self.draw_lcd_background(config)

    def draw_lcd_background(self, config):
        """Draw the LCD background for each clock element."""
        painter = QPainter(self)
        lcd_opacity = config['clock']['lcd_background_opacity']
        
        for key, element in self.clock_elements.items():
            label = element['label']
            if label.isVisible():
                painter.setFont(label.font())
                color = QColor(*config['clock']['seconds_color'] if key == 'seconds' else config['clock']['color'])
                painter.setPen(QColor(color.red(), color.green(), color.blue(), lcd_opacity))
                rect = label.geometry()
                background_text = '88' if key in ['hours', 'minutes', 'seconds'] else ':'
                painter.drawText(rect, Qt.AlignCenter, background_text)

    def update_config(self):
        """Update the widget's style and time display after a configuration change."""
        self.update_style()
        self.update_time()

    def resizeEvent(self, event):
        """Handle the resize event and adjust layout."""
        super().resizeEvent(event)
        self.adjust_layout()

    def calculate_stretch_factors(self, show_seconds):
        char_widths = {'hours': 2, 'separator': 1, 'minutes': 2, 'seconds': 2}
        total_width = sum(char_widths.values()) + (1 if show_seconds else -2)  # -2 for removing seconds and one separator
        
        factors = {}
        factors['hours'] = int(char_widths['hours'] / total_width * 100)
        factors['separator1'] = int(char_widths['separator'] / total_width * 100)
        factors['minutes'] = int(char_widths['minutes'] / total_width * 100)
        
        if show_seconds:
            factors['separator2'] = int(char_widths['separator'] / total_width * 100)
            factors['seconds'] = int(char_widths['seconds'] / total_width * 100)
        else:
            factors['separator2'] = 0
            factors['seconds'] = 0
        
        return factors

    def adjust_layout(self):
        """
        Adjust the layout of clock elements to fit the widget size.
        
        This method sets the stretch factors for each element in the layout
        to ensure they maintain proper proportions and fill the entire width.
        """
        config = self.config_manager.get_config()
        show_seconds = config['clock']['show_seconds']

        stretch_factors = self.calculate_stretch_factors(show_seconds)

        layout = self.layout()
        for i, (key, element) in enumerate(self.clock_elements.items()):
            layout.setStretch(i, stretch_factors[key])

        self.update()
        