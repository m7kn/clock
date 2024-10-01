from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QMenu, QMessageBox
from PyQt5.QtCore import Qt, QPoint, QRect
from PyQt5.QtGui import QColor
from clock_widget import ClockWidget
from settings_window import SettingsWindow
from utils import rgba_to_string

class MainWindow(QMainWindow):
    """The main window of the desktop clock application."""

    def __init__(self, config_manager):
        """Initialize the main window."""
        super().__init__()
        self.config_manager = config_manager
        self.draggable = False
        self.offset = QPoint()
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.init_ui()
    
    def init_ui(self):
        """Set up the user interface for the main window."""
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
        """Update the style of the main window based on the current configuration."""
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
        self.show()  # Necessary to apply changes
        if config['main_window']['frameless']:
            self.setCursor(Qt.OpenHandCursor)  # Change cursor to indicate movability
        else:
            self.setCursor(Qt.ArrowCursor)  # Reset to default cursor

    def show_context_menu(self, position):
        """Show the context menu when right-clicking on the window."""
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
        """Open the settings window."""
        settings_window = SettingsWindow(self.config_manager)
        settings_window.settings_changed.connect(self.update_style)
        settings_window.exec_()

    def show_about_dialog(self):
        """Show the about dialog."""
        QMessageBox.about(self, "About", "Desktop Clock\n\nCreated by Norbert Molnár\nVersion 0.1")

    def mousePressEvent(self, event):
        """Handle mouse press events for window dragging."""
        if event.button() == Qt.LeftButton:
            self.draggable = True
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        """Handle mouse move events for window dragging."""
        if self.draggable and self.config_manager.get_config()['main_window']['frameless']:
            self.move(self.mapToGlobal(event.pos() - self.offset))

    def mouseReleaseEvent(self, event):
        """Handle mouse release events for window dragging."""
        if event.button() == Qt.LeftButton:
            self.draggable = False

    def closeEvent(self, event):
        """Handle the window close event."""
        config = self.config_manager.get_config()
        config['main_window']['geometry'] = self.geometry().getRect()
        self.config_manager.save_config()
        event.accept()
        
    def load_geometry(self):
        """Load the window geometry from the configuration."""
        config = self.config_manager.get_config()
        geometry = config['main_window']['geometry']
        if geometry:
            self.setGeometry(QRect(*geometry))
            