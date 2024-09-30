from PyQt5.QtWidgets import QSpinBox, QFontComboBox, QColorDialog, QCheckBox

SETTINGS = {
    'main_window': {
        'geometry': {
            'type': 'list',
            'default': [100, 100, 300, 200],
            'widget': None  # Ez egy speciális eset, nem jelenik meg a beállítások ablakban
        },
        'frameless': {
            'type': 'bool',
            'default': False,
            'widget': QCheckBox,
            'label': 'Frameless Window'
        },
        'transparent': {
            'type': 'bool',
            'default': False,
            'widget': QCheckBox,
            'label': 'Transparent Background'
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
            'default': [0, 0, 0, 200],
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
            'default': 5,
            'widget': QSpinBox,
            'label': 'Horizontal Padding',
            'min': 0,
            'max': 100
        },
        'padding_vertical': {
            'type': 'int',
            'default': 5,
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
    