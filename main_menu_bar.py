from PySide6 import QtWidgets, QtGui


class MainMenuBar(QtWidgets.QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)

        file_menu = self.addMenu("File")
        view_menu = self.addMenu("View")
        options_menu = self.addMenu("Options")
        help_menu = self.addMenu("Help")

        self.open_action = file_menu.addAction("Open File")
        self.open_action.setShortcut(QtGui.QKeySequence.StandardKey.Open)
        exit_action = file_menu.addAction("Exit")
        exit_action.setShortcut(QtGui.QKeySequence.StandardKey.Quit)

        self.fullscreen_action = view_menu.addAction("Fullscreen")
        self.fullscreen_action.setCheckable(True)

        self.settings_action = options_menu.addAction("Settings")

        exit_action.triggered.connect(QtWidgets.QApplication.quit)

    def connect_signals(self, file_dialog_handler, toggle_fullscreen_handler, settings_handler):
        self.open_action.triggered.connect(file_dialog_handler)
        self.fullscreen_action.triggered.connect(toggle_fullscreen_handler)
        self.settings_action.triggered.connect(settings_handler)
