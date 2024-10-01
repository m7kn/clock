import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from config_manager import ConfigManager
from main_window import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    config_manager = ConfigManager('config.yaml')
    main_window = MainWindow(config_manager)
    # Add a small delay before showing the main window
    QTimer.singleShot(100, main_window.show)
    sys.exit(app.exec_())