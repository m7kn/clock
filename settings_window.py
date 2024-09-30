from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, QFontComboBox, QCheckBox, QPushButton, QGroupBox, QColorDialog
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QFont, QColor
from settings_definition import SETTINGS

class ColorButton(QPushButton):
    def __init__(self, color):
        super().__init__()
        self.setColor(color)

    def setColor(self, color):
        self.color = color
        self.setStyleSheet(f"background-color: {color.name()}; min-width: 32px; min-height: 32px;")

class SettingsWindow(QDialog):
    settings_changed = pyqtSignal()

    def __init__(self, config_manager):
        super().__init__()
        self.config_manager = config_manager
        self.setWindowTitle("Settings")
        self.init_ui()
        self.setMinimumSize(400, 300)

    def init_ui(self):
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
        for key, setting in SETTINGS[section].items():
            if setting['widget'] is not None:
                setting_layout = QHBoxLayout()
                label = QLabel(setting['label'])
                
                if setting['widget'] == QColorDialog:
                    widget = ColorButton(QColor(*self.config_manager.get_setting(section, key)))
                    widget.clicked.connect(lambda checked, s=section, k=key, w=widget: self.open_color_dialog(s, k, w))
                else:
                    widget = setting['widget']()
                    
                    if isinstance(widget, QSpinBox):
                        widget.setRange(setting.get('min', 0), setting.get('max', 100))
                        widget.valueChanged.connect(lambda value, s=section, k=key: self.save_setting(s, k, value))
                    elif isinstance(widget, QFontComboBox):
                        widget.currentFontChanged.connect(lambda font, s=section, k=key: self.save_setting(s, k, font.family()))
                    elif isinstance(widget, QCheckBox):
                        widget.stateChanged.connect(lambda state, s=section, k=key: self.save_setting(s, k, bool(state)))
                
                setattr(self, f"{section}_{key}_widget", widget)
                
                setting_layout.addWidget(label)
                setting_layout.addWidget(widget)
                layout.addLayout(setting_layout)

    def load_settings(self):
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

    def save_setting(self, section, key, value):
        self.config_manager.set_setting(section, key, value)
        self.settings_changed.emit()

    def open_color_dialog(self, section, key, button):
        color = QColorDialog.getColor(button.color, self, f"Choose {SETTINGS[section][key]['label']}")
        if color.isValid():
            button.setColor(color)
            self.save_setting(section, key, list(color.getRgb()))
            