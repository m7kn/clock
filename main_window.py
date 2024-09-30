from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QMenu, QMessageBox
from PyQt5.QtCore import Qt, QPoint, QRect
from PyQt5.QtGui import QColor
from clock_widget import ClockWidget
from settings_window import SettingsWindow
from utils import rgba_to_string

class MainWindow(QMainWindow):
    def __init__(self, config_manager):
        super().__init__()
        self.config_manager = config_manager
        self.draggable = False
        self.offset = QPoint()
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.init_ui()
    
    def init_ui(self):
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.clock_widget = ClockWidget(self.config_manager)
        layout.addWidget(self.clock_widget)
        
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
        
        self.load_geometry()
        self.update_style()

    def update_style(self):
        config = self.config_manager.get_config()
        if config['main_window']['frameless']:
            self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        else:
            self.setWindowFlags(self.windowFlags() & ~Qt.FramelessWindowHint)
        
        bg_color = QColor(*config['main_window']['background_color'])
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {rgba_to_string(bg_color.getRgb())};
            }}
            QWidget#centralWidget {{
                background-color: {rgba_to_string(bg_color.getRgb())};
            }}
            QMenu {{
                background-color: white;
                color: black;
            }}
            QMenu::item:selected {{
                background-color: #0078d7;
                color: white;
            }}
        """)
        
        self.central_widget.setObjectName("centralWidget")
        self.clock_widget.update_config()
        self.show()  # Szükséges a változások érvényesítéséhez
        if config['main_window']['frameless']:
            self.setCursor(Qt.OpenHandCursor)  # Változtassa meg a kurzort, hogy jelezze a mozgathatóságot
        else:
            self.setCursor(Qt.ArrowCursor)  # Állítsa vissza az alapértelmezett kurzort

    def show_context_menu(self, position):
        menu = QMenu(self)
        settings_action = menu.addAction("Settings")
        about_action = menu.addAction("About")
        exit_action = menu.addAction("Exit")
        
        action = menu.exec_(self.mapToGlobal(position))
        if action == settings_action:
            self.open_settings()
        elif action == about_action:
            self.show_about_dialog()
        elif action == exit_action:
            self.close()

    def open_settings(self):
        settings_window = SettingsWindow(self.config_manager)
        settings_window.settings_changed.connect(self.update_style)
        settings_window.exec_()

    def show_about_dialog(self):
        QMessageBox.about(self, "About", "Desktop Clock\n\nCreated by [Your Name]\nVersion 1.0")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.draggable = True
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.draggable and self.config_manager.get_config()['main_window']['frameless']:
            self.move(self.mapToGlobal(event.pos() - self.offset))

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.draggable = False

    def closeEvent(self, event):
        config = self.config_manager.get_config()
        config['main_window']['geometry'] = self.geometry().getRect()
        self.config_manager.save_config()
        event.accept()
        
    def load_geometry(self):
        config = self.config_manager.get_config()
        geometry = config['main_window']['geometry']
        if geometry:
            self.setGeometry(QRect(*geometry))        