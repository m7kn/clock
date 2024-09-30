from PyQt5.QtGui import QColor

def rgba_to_string(color):
    return f'rgba({color[0]}, {color[1]}, {color[2]}, {color[3]/255})'

def string_to_rgba(color_string):
    color = QColor(color_string)
    return [color.red(), color.green(), color.blue(), int(color.alpha() * 255)]