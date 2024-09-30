from PyQt5.QtWidgets import QSpinBox, QFontComboBox, QColorDialog, QCheckBox

SETTINGS = {
    'main_window': {
        'geometry': {
            'type': 'list',
            'default': [100, 100, 300, 150],
            'widget': None  # Ez egy speciális eset, nem jelenik meg a beállítások ablakban
        },
        'frameless': {
            'type': 'bool',
            'default': True,
            'widget': QCheckBox,
            'label': 'Frameless Window'
        },    
        'background_color': {
            'type': 'color',
            'default': [77, 103, 220, 100],  # Teljesen átlátszó fekete
            'widget': QColorDialog,
            'label': 'Background Color'
        },
    },
    'clock': {
        'font': {
            'type': 'str',
            'default': 'Arial',
            'widget': QFontComboBox,
            'label': 'Font'
        },
        'font_size': {
            'type': 'int',
            'default': 48,
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
    return {section: {key: setting['default'] for key, setting in items.items()}
            for section, items in SETTINGS.items()}
    