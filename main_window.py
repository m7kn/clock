from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QMenu, QAction, QMessageBox
from PyQt5.QtCore import Qt, QPoint
from clock_widget import ClockWidget
from settings_window import SettingsWindow

class MainWindow(QMainWindow):
    def __init__(self, config_manager):
        super().__init__()
        self.config_manager = config_manager
        self.draggable = False
        self.offset = QPoint()
        self.init_ui()
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.config_manager.get_config()['main_window']['frameless']:
            self.draggable = True
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.draggable and event.buttons() & Qt.LeftButton:
            self.move(self.mapToGlobal(event.pos() - self.offset))

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.draggable = False        

    def init_ui(self):
        self.setWindowTitle('Digital Desktop Clock')
        central_widget = QWidget()
        layout = QVBoxLayout()
        self.clock_widget = ClockWidget(self.config_manager)
        layout.addWidget(self.clock_widget)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.load_window_state()
        self.update_style()

        # Jobb kattintásos menü hozzáadása
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def load_window_state(self):
        config = self.config_manager.get_config()
        self.setGeometry(*config['main_window']['geometry'])

    def update_style(self):
        config = self.config_manager.get_config()
        if config['main_window']['frameless']:
            self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        else:
            self.setWindowFlags(self.windowFlags() & ~Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, config['main_window']['transparent'])
        self.clock_widget.update_config()
        self.show()  # Szükséges a változások érvényesítéséhez
        if config['main_window']['frameless']:
            self.setCursor(Qt.OpenHandCursor)  # Változtassa meg a kurzort, hogy jelezze a mozgathatóságot
        else:
            self.setCursor(Qt.ArrowCursor)  # Állítsa vissza az alapértelmezett kurzort

    def closeEvent(self, event):
        self.save_window_state()
        super().closeEvent(event)

    def save_window_state(self):
        config = self.config_manager.get_config()
        config['main_window']['geometry'] = self.geometry().getRect()
        self.config_manager.save_config()

    def show_settings(self):
        settings_window = SettingsWindow(self.config_manager)
        settings_window.settings_changed.connect(self.update_style)
        settings_window.setWindowModality(Qt.ApplicationModal)
        settings_window.exec_()  # Az exec_() metódust használjuk a show() helyett

    def show_context_menu(self, pos):
        context_menu = QMenu(self)

        config_action = QAction("Config", self)
        config_action.triggered.connect(self.show_settings)
        context_menu.addAction(config_action)

        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        context_menu.addAction(about_action)

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        context_menu.addAction(exit_action)

        context_menu.exec_(self.mapToGlobal(pos))

    def show_about(self):
        QMessageBox.about(self, "About Digital Desktop Clock",
                          "Digital Desktop Clock\n\n"
                          "Version 1.0\n"
                          "Created by Your Name\n\n"
                          "A simple, customizable desktop clock application.")
        