import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from utils.config_manager import ConfigManager
from ui.main_window import MainWindow
from utils.font_manager import font_manager

def load_fonts():
    """Load custom fonts."""
    font_manager.load_custom_fonts()
    if not font_manager.get_custom_fonts():
        print("Warning: No custom fonts were loaded.")

def main():
    """Main function to run the application."""
    app = QApplication(sys.argv)       

    load_fonts()        
            
    config_manager = ConfigManager('config.yaml')
    main_window = MainWindow(config_manager)
    # Add a small delay before showing the main window
    QTimer.singleShot(100, main_window.show)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
    