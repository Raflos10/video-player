from typing import cast
from PySide6 import QtCore, QtWidgets

from setting_keys import SettingKeys

DEFAULTS = {
    SettingKeys.SHOW_MENU_BAR: True,
    SettingKeys.SEEK_STEP: 10,
    SettingKeys.SAVE_POSITION_ON_EXIT: False,
}


class SettingsWindow(QtWidgets.QDialog):

    def __init__(self, settings: QtCore.QSettings, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setModal(True)
        self.resize(400, 300)

        self.settings = settings

        # Main layout
        layout = QtWidgets.QVBoxLayout(self)

        # Tab widget for sections
        self.tab_widget = QtWidgets.QTabWidget()
        layout.addWidget(self.tab_widget)

        # Appearance tab
        appearance_tab = QtWidgets.QWidget()
        appearance_layout = QtWidgets.QVBoxLayout(appearance_tab)
        self.show_menu_bar_checkbox = QtWidgets.QCheckBox("Show Menu Bar")
        appearance_layout.addWidget(self.show_menu_bar_checkbox)
        appearance_layout.addStretch()
        self.tab_widget.addTab(appearance_tab, "Appearance")

        # Behavior tab
        behavior_tab = QtWidgets.QWidget()
        behavior_layout = QtWidgets.QVBoxLayout(behavior_tab)
        seek_step_label = QtWidgets.QLabel("Seek Step (seconds):")
        self.seek_step_spinbox = QtWidgets.QSpinBox()
        self.seek_step_spinbox.setRange(1, 60)
        self.save_position_checkbox = QtWidgets.QCheckBox("Save position on exit")
        behavior_layout.addWidget(seek_step_label)
        behavior_layout.addWidget(self.seek_step_spinbox)
        behavior_layout.addWidget(self.save_position_checkbox)
        behavior_layout.addStretch()
        self.tab_widget.addTab(behavior_tab, "Behavior")

        # Buttons
        button_box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.StandardButton.Ok |
            QtWidgets.QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        # Load settings
        self.load_settings()

    def load_settings(self):
        show_menu_bar = self.settings.value(SettingKeys.SHOW_MENU_BAR, DEFAULTS[SettingKeys.SHOW_MENU_BAR])
        self.show_menu_bar_checkbox.setChecked(bool(show_menu_bar))

        seek_step = self.settings.value(SettingKeys.SEEK_STEP, DEFAULTS[SettingKeys.SEEK_STEP])
        self.seek_step_spinbox.setValue(int(cast(int, seek_step)))

        save_position = self.settings.value(SettingKeys.SAVE_POSITION_ON_EXIT,
                                            DEFAULTS[SettingKeys.SAVE_POSITION_ON_EXIT])
        self.save_position_checkbox.setChecked(bool(save_position))

    def save_settings(self):
        self.settings.setValue(SettingKeys.SHOW_MENU_BAR, self.show_menu_bar_checkbox.isChecked())
        self.settings.setValue(SettingKeys.SEEK_STEP, self.seek_step_spinbox.value())
        self.settings.setValue(SettingKeys.SAVE_POSITION_ON_EXIT, self.save_position_checkbox.isChecked())
        self.settings.sync()

    def accept(self):
        self.save_settings()
        super().accept()
