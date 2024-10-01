import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtCore import QTimer
from config_manager import ConfigManager
from main_window import MainWindow
from font_manager import font_manager

def load_fonts():
    font_manager.load_custom_fonts()
    if not font_manager.get_custom_fonts():
        print("Warning: No custom fonts were loaded.")

if __name__ == '__main__':
    app = QApplication(sys.argv)       

    load_fonts()        
            
    config_manager = ConfigManager('config.yaml')
    main_window = MainWindow(config_manager)
    # Add a small delay before showing the main window
    QTimer.singleShot(100, main_window.show)
    sys.exit(app.exec_())
    