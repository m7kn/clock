from PyQt5.QtWidgets import QSpinBox, QFontComboBox, QColorDialog, QCheckBox, QSlider, QComboBox
from PyQt5.QtCore import Qt

# Define the settings structure for the application
SETTINGS = {
    'main_window': {
        'geometry': {
            'type': 'list',
            'default': [186, 122, 480, 155],
            'widget': None  # Special case, not shown in settings window
        },
        'frameless': {
            'type': 'bool',
            'default': True,
            'widget': QCheckBox,
            'label': 'Frameless Window'
        },    
        'background_color': {
            'type': 'color',
            'default': [220, 220, 220, 0],  # Partially transparent blue
            'widget': QColorDialog,
            'label': 'Background Color'
        },
        'corner_radius': {
            'type': 'int',
            'default': 30,
            'widget': QSpinBox,
            'label': 'Corner Radius',
            'min': 0,
            'max': 50
        },        
    },
    'clock': {
        'use_custom_fonts': {
            'type': 'bool',
            'default': True,
            'widget': QCheckBox,
            'label': 'Use Custom Fonts'
        },        
        'font': {
            'type': 'str',
            'default': 'Digital Display',
            'widget': QFontComboBox,
            'label': 'Font'
        },
        'font_size': {
            'type': 'int',
            'default': 81,
            'widget': QSpinBox,
            'label': 'Font Size',
            'min': 1,
            'max': 200
        },
        'seconds_font_size': {
            'type': 'int',
            'default': 81,  # Same as the main font size by default
            'widget': QSpinBox,
            'label': 'Seconds Font Size',
            'min': 1,
            'max': 200
        },
        'seconds_alignment': {
            'type': 'str',
            'default': 'center',
            'widget': QComboBox,
            'label': 'Seconds Alignment',
            'options': ['top', 'center', 'bottom']
        },        
        'color': {
            'type': 'color',
            'default': [209, 209, 209, 255],
            'widget': QColorDialog,
            'label': 'Text Color'
        },
        'background_color': {
            'type': 'color',          
            'default': [32, 18, 223, 200],
            'widget': QColorDialog,
            'label': 'Background Color'
        },
        'show_seconds': {
            'type': 'bool',
            'default': True,
            'widget': QCheckBox,
            'label': 'Show Seconds'
        },
        'padding_horizontal': {
            'type': 'int',
            'default': 17,
            'widget': QSpinBox,
            'label': 'Horizontal Padding',
            'min': 0,
            'max': 100
        },
        'padding_vertical': {
            'type': 'int',
            'default': 16,
            'widget': QSpinBox,
            'label': 'Vertical Padding',
            'min': 0,
            'max': 100
        },
        'lcd_background_opacity': {
            'type': 'int',
            'default': 189,
            'widget': QSlider,
            'label': 'LCD Background Opacity',
            'min': 0,
            'max': 255,
            'orientation': Qt.Horizontal
        },             
    }
}

def get_default_config():
    """Generate a default configuration based on the SETTINGS structure."""
    return {section: {key: setting['default'] for key, setting in items.items()}
            for section, items in SETTINGS.items()}
