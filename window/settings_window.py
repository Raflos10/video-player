from typing import cast
from PySide6 import QtCore, QtWidgets, QtGui

from setting_keys import SettingKeys, DEFAULTS


class SettingsWindow(QtWidgets.QDialog):

    settings_updated = QtCore.Signal()

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
        self.enable_subtitles_checkbox = QtWidgets.QCheckBox("Enable Subtitles")
        appearance_layout.addWidget(self.enable_subtitles_checkbox)
        subtitle_font_layout = QtWidgets.QHBoxLayout()
        subtitle_font_layout.addWidget(QtWidgets.QLabel("Subtitle Font Size:"))
        self.subtitle_font_spinbox = QtWidgets.QSpinBox()
        self.subtitle_font_spinbox.setRange(12, 48)
        subtitle_font_layout.addWidget(self.subtitle_font_spinbox)
        appearance_layout.addLayout(subtitle_font_layout)
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

        # Keyboard Shortcuts tab
        keyboard_tab = QtWidgets.QWidget()
        keyboard_layout = QtWidgets.QFormLayout(keyboard_tab)
        self.play_pause_edit = QtWidgets.QKeySequenceEdit()
        self.seek_forward_edit = QtWidgets.QKeySequenceEdit()
        self.seek_backward_edit = QtWidgets.QKeySequenceEdit()
        self.fullscreen_edit = QtWidgets.QKeySequenceEdit()
        keyboard_layout.addRow("Play/Pause:", self.play_pause_edit)
        keyboard_layout.addRow("Seek Forward:", self.seek_forward_edit)
        keyboard_layout.addRow("Seek Backward:", self.seek_backward_edit)
        keyboard_layout.addRow("Toggle Fullscreen:", self.fullscreen_edit)
        self.tab_widget.addTab(keyboard_tab, "Keyboard Shortcuts")

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

        enable_subtitles = self.settings.value(SettingKeys.ENABLE_SUBTITLES, DEFAULTS[SettingKeys.ENABLE_SUBTITLES])
        self.enable_subtitles_checkbox.setChecked(bool(enable_subtitles))

        subtitle_font_size = self.settings.value(SettingKeys.SUBTITLE_FONT_SIZE, DEFAULTS[SettingKeys.SUBTITLE_FONT_SIZE])
        self.subtitle_font_spinbox.setValue(int(cast(int, subtitle_font_size)))

        seek_step = self.settings.value(SettingKeys.SEEK_STEP, DEFAULTS[SettingKeys.SEEK_STEP])
        self.seek_step_spinbox.setValue(int(cast(int, seek_step)))

        save_position = self.settings.value(SettingKeys.SAVE_POSITION_ON_EXIT,
                                              DEFAULTS[SettingKeys.SAVE_POSITION_ON_EXIT])
        self.save_position_checkbox.setChecked(bool(save_position))

        play_pause_shortcut = self.settings.value(SettingKeys.PLAY_PAUSE_SHORTCUT, DEFAULTS[SettingKeys.PLAY_PAUSE_SHORTCUT])
        self.play_pause_edit.setKeySequence(QtGui.QKeySequence.fromString(str(play_pause_shortcut)))

        seek_forward_shortcut = self.settings.value(SettingKeys.SEEK_FORWARD_SHORTCUT, DEFAULTS[SettingKeys.SEEK_FORWARD_SHORTCUT])
        self.seek_forward_edit.setKeySequence(QtGui.QKeySequence.fromString(str(seek_forward_shortcut)))

        seek_backward_shortcut = self.settings.value(SettingKeys.SEEK_BACKWARD_SHORTCUT, DEFAULTS[SettingKeys.SEEK_BACKWARD_SHORTCUT])
        self.seek_backward_edit.setKeySequence(QtGui.QKeySequence.fromString(str(seek_backward_shortcut)))

        fullscreen_shortcut = self.settings.value(SettingKeys.FULLSCREEN_SHORTCUT, DEFAULTS[SettingKeys.FULLSCREEN_SHORTCUT])
        self.fullscreen_edit.setKeySequence(QtGui.QKeySequence.fromString(str(fullscreen_shortcut)))

    def save_settings(self):
        self.settings.setValue(SettingKeys.SHOW_MENU_BAR, self.show_menu_bar_checkbox.isChecked())
        self.settings.setValue(SettingKeys.ENABLE_SUBTITLES, self.enable_subtitles_checkbox.isChecked())
        self.settings.setValue(SettingKeys.SUBTITLE_FONT_SIZE, self.subtitle_font_spinbox.value())
        self.settings.setValue(SettingKeys.SEEK_STEP, self.seek_step_spinbox.value())
        self.settings.setValue(SettingKeys.SAVE_POSITION_ON_EXIT, self.save_position_checkbox.isChecked())
        self.settings.setValue(SettingKeys.PLAY_PAUSE_SHORTCUT, self.play_pause_edit.keySequence().toString())
        self.settings.setValue(SettingKeys.SEEK_FORWARD_SHORTCUT, self.seek_forward_edit.keySequence().toString())
        self.settings.setValue(SettingKeys.SEEK_BACKWARD_SHORTCUT, self.seek_backward_edit.keySequence().toString())
        self.settings.setValue(SettingKeys.FULLSCREEN_SHORTCUT, self.fullscreen_edit.keySequence().toString())
        self.settings.sync()

    def accept(self):
        self.save_settings()
        self.settings_updated.emit()
        super().accept()
