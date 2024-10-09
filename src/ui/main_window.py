from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QMenu, QMessageBox, QSizeGrip
from PyQt5.QtCore import Qt, QPoint, QRect
from PyQt5.QtGui import QColor, QGuiApplication
from .clock_widget import ClockWidget
from .settings_window import SettingsWindow
from utils.utils import rgba_to_string

class MainWindow(QMainWindow):
    """The main window of the desktop clock application."""

    def __init__(self, config_manager):
        """Initialize the main window."""
        super().__init__()
        self.config_manager = config_manager
        self.draggable = False
        self.offset = QPoint()
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resizable = False
        self.size_grip = None
        self.init_ui()
    
    def init_ui(self):
        """Set up the user interface for the main window."""
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        
        self.clock_widget = ClockWidget(self.config_manager)
        self.main_layout.addWidget(self.clock_widget)
        
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
        corner_radius = config['main_window']['corner_radius']
        background_margin = config['main_window']['background_margin']
        
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {rgba_to_string(bg_color.getRgb())};
                border-radius: {corner_radius}px;
            }}
            QWidget#centralWidget {{
                background-color: {rgba_to_string(bg_color.getRgb())};
                border-radius: {corner_radius}px;
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
        self.main_layout.setContentsMargins(background_margin, background_margin, background_margin, background_margin)
        self.clock_widget.update_config()
        self.show()  # Necessary to apply changes
        
        # Update cursor based on frameless mode and resizability
        self.update_cursor()
        
        # Update size grip visibility
        self.update_size_grip()

    def update_cursor(self):
        """Update the cursor based on the current window state."""
        config = self.config_manager.get_config()
        if config['main_window']['frameless']:
            self.setCursor(Qt.OpenHandCursor if not self.resizable else Qt.ArrowCursor)
        else:
            self.setCursor(Qt.ArrowCursor)

    def update_size_grip(self):
        """Update the size grip based on the current window state."""
        if self.resizable:
            if not self.size_grip:
                self.size_grip = QSizeGrip(self)
            self.size_grip.show()
            self.size_grip.raise_()
        else:
            if self.size_grip:
                self.size_grip.hide()

    def show_context_menu(self, position):
        """Show the context menu when right-clicking on the window."""
        menu = QMenu(self)
        settings_action = menu.addAction("Settings")
        about_action = menu.addAction("About")
        
        # Add toggle resize action
        config = self.config_manager.get_config()
        if config['main_window']['frameless']:
            resize_action = menu.addAction("Enable Resizing" if not self.resizable else "Disable Resizing")
        
        exit_action = menu.addAction("Exit")
        
        action = menu.exec_(self.mapToGlobal(position))
        if action == settings_action:
            self.open_settings()
        elif action == about_action:
            self.show_about_dialog()
        elif config['main_window']['frameless'] and action == resize_action:
            self.toggle_resize()
        elif action == exit_action:
            self.close()

    def toggle_resize(self):
        """Toggle the resizability of the window."""
        config = self.config_manager.get_config()
        
        if config['main_window']['frameless']:
            self.resizable = not self.resizable            
            if self.resizable:
                self.setWindowFlags(self.windowFlags() & ~Qt.FramelessWindowHint)
            else:
                self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        
            self.update_style()
            self.show()  # Necessary to apply changes after updating window flags

    def open_settings(self):
        """Open the settings window."""
        settings_window = SettingsWindow(self.config_manager)
        settings_window.settings_changed.connect(self.update_style)
        settings_window.exec_()

    def show_about_dialog(self):
        """Show the about dialog."""
        QMessageBox.about(self, "About", "Desktop Clock\n\nCreated by Norbert Molnár\nVersion 0.3")

    def mousePressEvent(self, event):
        """Handle mouse press events for window dragging."""
        if event.button() == Qt.LeftButton:
            self.draggable = True
            self.offset = event.pos()
            if self.config_manager.get_config()['main_window']['frameless'] and not self.resizable:
                self.setCursor(Qt.ClosedHandCursor)  # Change cursor to indicate grabbing

    def mouseMoveEvent(self, event):
        """Handle mouse move events for window dragging."""
        if self.draggable and self.config_manager.get_config()['main_window']['frameless'] and not self.resizable:
            config = self.config_manager.get_config()
            corner_radius = config['main_window']['corner_radius']
            background_margin = config['main_window']['background_margin']
            
            # Calculate the total offset including corner radius and background margin
            total_offset_x = corner_radius + background_margin
            total_offset_y = corner_radius + background_margin
            
            new_pos = self.mapToGlobal(event.pos() - self.offset)
            screen_geo = QGuiApplication.primaryScreen().geometry()
            
            # Adjust the position to account for the corner radius and background margin
            new_pos.setX(max(total_offset_x, min(new_pos.x(), screen_geo.width() - self.width() + total_offset_x)))
            new_pos.setY(max(total_offset_y, min(new_pos.y(), screen_geo.height() - self.height() + total_offset_y)))
            
            self.move(new_pos)

    def mouseReleaseEvent(self, event):
        """Handle mouse release events for window dragging."""
        if event.button() == Qt.LeftButton:
            self.draggable = False
            self.update_cursor()

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