import os
from PyQt5.QtGui import QFontDatabase, QFont
from PyQt5.QtCore import QFileInfo

class FontManager:
    def __init__(self):
        self.custom_fonts = {}
        self.font_ids = []

    def load_custom_fonts(self):
        fonts_dir = 'fonts'
        if not os.path.exists(fonts_dir):
            print(f"Warning: {fonts_dir} directory not found.")
            return

        for family_dir in os.listdir(fonts_dir):
            family_path = os.path.join(fonts_dir, family_dir)
            if os.path.isdir(family_path):
                for font_file in os.listdir(family_path):
                    if font_file.lower().endswith(('.ttf', '.otf')):
                        font_path = os.path.join(family_path, font_file)
                        self.load_single_font(font_path)

    def load_single_font(self, font_path):
        try:
            if not QFileInfo(font_path).isReadable():
                print(f"Warning: Font file is not readable: {font_path}")
                return

            font_id = QFontDatabase.addApplicationFont(font_path)
            if font_id != -1:
                self.font_ids.append(font_id)
                font_families = QFontDatabase.applicationFontFamilies(font_id)
                if font_families:
                    font_family = font_families[0]
                    self.custom_fonts[font_family] = font_path
                    print(f"Loaded custom font: {font_family}")
                else:
                    print(f"Warning: Could not load font families for {font_path}")
            else:
                print(f"Warning: Failed to load font {font_path}")
        except Exception as e:
            print(f"Error loading font {font_path}: {str(e)}")

    def get_custom_fonts(self):
        return list(self.custom_fonts.keys())

    def get_system_fonts(self):
        return QFontDatabase().families()

    def get_font(self, font_name, use_custom_fonts):
        if use_custom_fonts and font_name in self.custom_fonts:
            return QFont(font_name)
        return QFont(font_name)

font_manager = FontManager()
