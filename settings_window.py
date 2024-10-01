from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, QFontComboBox, QCheckBox, QPushButton, QGroupBox, QColorDialog, QSlider
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QFont, QColor, QFontDatabase
from settings_definition import SETTINGS
from font_manager import font_manager

class ColorButton(QPushButton):
    """A custom button for color selection."""

    def __init__(self, color):
        super().__init__()
        self.setColor(color)

    def setColor(self, color):
        """Set the button's color and update its appearance."""
        self.color = color
        self.setStyleSheet(f"background-color: {color.name()}; min-width: 32px; min-height: 32px;")

class SettingsWindow(QDialog):
    """A window for editing application settings."""

    settings_changed = pyqtSignal()

    def __init__(self, config_manager):
        super().__init__()
        self.config_manager = config_manager
        self.setWindowTitle("Settings")
        self.init_ui()
        self.setMinimumSize(400, 300)

    def init_ui(self):
        """Set up the user interface for the settings window."""
        layout = QVBoxLayout()

        # Clock settings
        clock_group = QGroupBox("Clock Settings")
        clock_layout = QVBoxLayout()
        self.add_settings_to_layout(clock_layout, "clock")
        clock_group.setLayout(clock_layout)
        layout.addWidget(clock_group)

        # Main window settings
        main_window_group = QGroupBox("Main Window Settings")
        main_window_layout = QVBoxLayout()
        self.add_settings_to_layout(main_window_layout, "main_window")
        main_window_group.setLayout(main_window_layout)
        layout.addWidget(main_window_group)

        self.setLayout(layout)
        self.load_settings()

    def add_settings_to_layout(self, layout, section):
        """Add settings widgets to the given layout for the specified section."""
        for key, setting in SETTINGS[section].items():
            if setting['widget'] is not None:
                setting_layout = QHBoxLayout()
                label = QLabel(setting['label'])
                
                if setting['widget'] == QColorDialog:
                    widget = ColorButton(QColor(*self.config_manager.get_setting(section, key)))
                    widget.clicked.connect(lambda checked, s=section, k=key, w=widget: self.open_color_dialog(s, k, w))
                elif setting['widget'] == QFontComboBox:
                    widget = QFontComboBox()
                    self.update_font_list(widget)
                    widget.currentFontChanged.connect(lambda font, s=section, k=key: self.save_font_setting(s, k, font))
                elif setting['widget'] == QSlider:
                    widget = QSlider(setting['orientation'])
                    widget.setRange(setting['min'], setting['max'])
                    widget.valueChanged.connect(lambda value, s=section, k=key: self.save_setting(s, k, value))                    
                else:
                    widget = setting['widget']()
                    
                    if isinstance(widget, QSpinBox):
                        widget.setRange(setting.get('min', 0), setting.get('max', 100))
                        widget.valueChanged.connect(lambda value, s=section, k=key: self.save_setting(s, k, value))
                    elif isinstance(widget, QCheckBox):
                        widget.stateChanged.connect(lambda state, s=section, k=key: self.save_setting(s, k, bool(state)))
                        if key == 'use_custom_fonts':
                            widget.stateChanged.connect(self.update_font_combo)
                
                setattr(self, f"{section}_{key}_widget", widget)
                
                setting_layout.addWidget(label)
                setting_layout.addWidget(widget)
                layout.addLayout(setting_layout)

    def load_settings(self):
        """Load current settings into the UI widgets."""
        for section in SETTINGS:
            for key, setting in SETTINGS[section].items():
                if setting['widget'] is not None:
                    widget = getattr(self, f"{section}_{key}_widget")
                    value = self.config_manager.get_setting(section, key)
                    
                    if isinstance(widget, QSpinBox):
                        widget.setValue(value)
                    elif isinstance(widget, QFontComboBox):
                        widget.setCurrentFont(QFont(value))
                    elif isinstance(widget, ColorButton):
                        widget.setColor(QColor(*value))
                    elif isinstance(widget, QCheckBox):
                        widget.setChecked(value)
                    elif isinstance(widget, QSlider):
                        widget.setValue(value)                        

    def save_setting(self, section, key, value):
        """Save a setting and emit the settings_changed signal."""
        self.config_manager.set_setting(section, key, value)
        self.settings_changed.emit()

    def save_font_setting(self, section, key, font):
        font_family = font.family()
        self.config_manager.set_setting(section, key, font_family)
        is_lcd_font = font_manager.is_lcd_font(font_family)
        self.config_manager.set_setting(section, 'use_lcd_style', is_lcd_font)
        self.settings_changed.emit()

    def open_color_dialog(self, section, key, button):
        """Open a color dialog for color selection."""
        current_color = QColor(*self.config_manager.get_setting(section, key))
        color = QColorDialog.getColor(current_color, self, f"Choose {SETTINGS[section][key]['label']}", QColorDialog.ShowAlphaChannel)
        if color.isValid():
            button.setColor(color)
            self.save_setting(section, key, list(color.getRgb()))
            
    def update_font_list(self, widget):
        use_custom_fonts = self.config_manager.get_setting('clock', 'use_custom_fonts')
        current_font = widget.currentFont().family()
        widget.clear()
        if use_custom_fonts:
            for font in font_manager.get_custom_fonts():
                widget.addItem(font)
            if current_font not in font_manager.get_custom_fonts():
                current_font = font_manager.get_custom_fonts()[0] if font_manager.get_custom_fonts() else ""
        else:
            widget.setWritingSystem(QFontDatabase.Any)
            if current_font not in QFontDatabase().families():
                current_font = QFontDatabase().families()[0]
        
        widget.setCurrentFont(QFont(current_font))

    def update_font_combo(self):
        font_widget = getattr(self, "clock_font_widget")
        self.update_font_list(font_widget)
        current_font = self.config_manager.get_setting('clock', 'font')
        font_widget.setCurrentFont(QFont(current_font))
        