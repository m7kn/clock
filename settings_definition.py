from PyQt5.QtWidgets import QSpinBox, QFontComboBox, QColorDialog, QCheckBox

# Define the settings structure for the application
SETTINGS = {
    'main_window': {
        'geometry': {
            'type': 'list',
            'default': [100, 100, 300, 150],
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
            'default': [77, 103, 220, 100],  # Partially transparent blue
            'widget': QColorDialog,
            'label': 'Background Color'
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
            'default': 64,
            'widget': QSpinBox,
            'label': 'Font Size',
            'min': 1,
            'max': 200
        },
        'color': {
            'type': 'color',
            'default': [255, 255, 255, 255],
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
            'default': 20,
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
    }
}

def get_default_config():
    """Generate a default configuration based on the SETTINGS structure."""
    return {section: {key: setting['default'] for key, setting in items.items()}
            for section, items in SETTINGS.items()}
