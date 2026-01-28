from PySide6 import QtGui, QtWidgets
from PySide6.QtWidgets import QWidget

from settings.setting_keys import DEFAULTS, SettingKeys
from settings.settings_manager import settings_manager


def _create_key_sequence_edit() -> QtWidgets.QKeySequenceEdit:
    edit = QtWidgets.QKeySequenceEdit()
    edit.setClearButtonEnabled(True)
    return edit


def _load_shortcut(edit: QtWidgets.QKeySequenceEdit, key: str) -> None:
    shortcut = settings_manager.get_str(key)
    edit.setKeySequence(QtGui.QKeySequence.fromString(shortcut))


def _save_shortcut(edit: QtWidgets.QKeySequenceEdit, key: str) -> None:
    settings_manager.set_value(key, edit.keySequence().toString())


class SettingsWindow(QtWidgets.QDialog):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setModal(True)
        self.resize(400, 300)

        layout = QtWidgets.QVBoxLayout(self)
        self.tab_widget = QtWidgets.QTabWidget()
        layout.addWidget(self.tab_widget)

        self._create_appearance_tab()
        self._create_behavior_tab()
        self._create_keyboard_tab()
        self._create_buttons(layout)

        self.refresh_ui()

    def _create_appearance_tab(self) -> None:
        tab = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(tab)

        self.show_menu_bar_checkbox = QtWidgets.QCheckBox("Show Menu Bar")
        layout.addWidget(self.show_menu_bar_checkbox)

        self.enable_subtitles_checkbox = QtWidgets.QCheckBox("Enable Subtitles")
        layout.addWidget(self.enable_subtitles_checkbox)

        # Subtitle font scale
        scale_layout = QtWidgets.QHBoxLayout()
        scale_layout.addWidget(QtWidgets.QLabel("Subtitle Size (% of screen):"))
        self.subtitle_scale_spinbox = QtWidgets.QDoubleSpinBox()
        self.subtitle_scale_spinbox.setRange(2.0, 7.0)
        self.subtitle_scale_spinbox.setSingleStep(0.1)
        self.subtitle_scale_spinbox.setDecimals(1)
        self.subtitle_scale_spinbox.setSuffix("%")
        scale_layout.addWidget(self.subtitle_scale_spinbox)
        layout.addLayout(scale_layout)

        layout.addStretch()
        self.tab_widget.addTab(tab, "Appearance")

    def _create_behavior_tab(self) -> None:
        tab = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(tab)

        seek_step_label = QtWidgets.QLabel("Seek Step (seconds):")
        self.seek_step_spinbox = QtWidgets.QSpinBox()
        self.seek_step_spinbox.setRange(1, 60)

        self.save_position_checkbox = QtWidgets.QCheckBox("Save position on exit")

        layout.addWidget(seek_step_label)
        layout.addWidget(self.seek_step_spinbox)
        layout.addWidget(self.save_position_checkbox)
        layout.addStretch()

        self.tab_widget.addTab(tab, "Behavior")

    def _create_keyboard_tab(self) -> None:
        tab = QtWidgets.QWidget()
        main_layout = QtWidgets.QVBoxLayout(tab)

        # Instructions
        instructions = QtWidgets.QLabel(
            "Click on a field and press the desired key combination.\n"
            "Press Backspace or Delete to clear a shortcut."
        )
        instructions.setWordWrap(True)
        instructions.setStyleSheet("color: gray; margin-bottom: 10px;")
        main_layout.addWidget(instructions)

        # Shortcuts form
        form_layout = QtWidgets.QFormLayout()
        form_layout.setFieldGrowthPolicy(
            QtWidgets.QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow
        )

        self.play_pause_edit = _create_key_sequence_edit()
        self.seek_forward_edit = _create_key_sequence_edit()
        self.seek_backward_edit = _create_key_sequence_edit()
        self.toggle_mute_edit = _create_key_sequence_edit()
        self.fullscreen_edit = _create_key_sequence_edit()
        self.toggle_subtitles_edit = _create_key_sequence_edit()

        form_layout.addRow("Play/Pause:", self.play_pause_edit)
        form_layout.addRow("Seek Forward:", self.seek_forward_edit)
        form_layout.addRow("Seek Backward:", self.seek_backward_edit)
        form_layout.addRow("Toggle Mute:", self.toggle_mute_edit)
        form_layout.addRow("Toggle Fullscreen:", self.fullscreen_edit)
        form_layout.addRow("Toggle Subtitles:", self.toggle_subtitles_edit)

        main_layout.addLayout(form_layout)
        main_layout.addStretch()

        # Reset button
        reset_btn = QtWidgets.QPushButton("Reset to Defaults")
        reset_btn.clicked.connect(self.reset_shortcuts_to_defaults)
        main_layout.addWidget(reset_btn)

        self.tab_widget.addTab(tab, "Keyboard Shortcuts")

    def _create_buttons(self, layout: QtWidgets.QVBoxLayout) -> None:
        button_box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.StandardButton.Ok
            | QtWidgets.QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def refresh_ui(self) -> None:
        self.show_menu_bar_checkbox.setChecked(
            settings_manager.get_bool(SettingKeys.SHOW_MENU_BAR)
        )
        self.enable_subtitles_checkbox.setChecked(
            settings_manager.get_bool(SettingKeys.ENABLE_SUBTITLES)
        )
        self.subtitle_scale_spinbox.setValue(
            settings_manager.get_float(SettingKeys.SUBTITLE_FONT_SCALE)
        )
        self.seek_step_spinbox.setValue(settings_manager.get_int(SettingKeys.SEEK_STEP))
        self.save_position_checkbox.setChecked(
            settings_manager.get_bool(SettingKeys.SAVE_POSITION_ON_EXIT)
        )

        _load_shortcut(self.play_pause_edit, SettingKeys.PLAY_PAUSE_SHORTCUT)
        _load_shortcut(self.seek_forward_edit, SettingKeys.SEEK_FORWARD_SHORTCUT)
        _load_shortcut(self.seek_backward_edit, SettingKeys.SEEK_BACKWARD_SHORTCUT)
        _load_shortcut(self.toggle_mute_edit, SettingKeys.TOGGLE_MUTE_SHORTCUT)
        _load_shortcut(self.fullscreen_edit, SettingKeys.FULLSCREEN_SHORTCUT)
        _load_shortcut(
            self.toggle_subtitles_edit, SettingKeys.TOGGLE_SUBTITLES_SHORTCUT
        )

    def reset_shortcuts_to_defaults(self) -> None:
        shortcuts = {
            self.play_pause_edit: SettingKeys.PLAY_PAUSE_SHORTCUT,
            self.seek_forward_edit: SettingKeys.SEEK_FORWARD_SHORTCUT,
            self.seek_backward_edit: SettingKeys.SEEK_BACKWARD_SHORTCUT,
            self.toggle_mute_edit: SettingKeys.TOGGLE_MUTE_SHORTCUT,
            self.fullscreen_edit: SettingKeys.FULLSCREEN_SHORTCUT,
            self.toggle_subtitles_edit: SettingKeys.TOGGLE_SUBTITLES_SHORTCUT,
        }

        for edit, key in shortcuts.items():
            default_value = DEFAULTS[key]
            edit.setKeySequence(QtGui.QKeySequence.fromString(str(default_value)))

    def accept(self) -> None:
        settings_manager.set_value(
            SettingKeys.SHOW_MENU_BAR, self.show_menu_bar_checkbox.isChecked()
        )
        settings_manager.set_value(
            SettingKeys.ENABLE_SUBTITLES, self.enable_subtitles_checkbox.isChecked()
        )
        settings_manager.set_value(
            SettingKeys.SUBTITLE_FONT_SCALE, self.subtitle_scale_spinbox.value()
        )
        settings_manager.set_value(
            SettingKeys.SEEK_STEP, self.seek_step_spinbox.value()
        )
        settings_manager.set_value(
            SettingKeys.SAVE_POSITION_ON_EXIT,
            self.save_position_checkbox.isChecked(),
        )

        _save_shortcut(self.play_pause_edit, SettingKeys.PLAY_PAUSE_SHORTCUT)
        _save_shortcut(self.seek_forward_edit, SettingKeys.SEEK_FORWARD_SHORTCUT)
        _save_shortcut(self.seek_backward_edit, SettingKeys.SEEK_BACKWARD_SHORTCUT)
        _save_shortcut(self.toggle_mute_edit, SettingKeys.TOGGLE_MUTE_SHORTCUT)
        _save_shortcut(self.fullscreen_edit, SettingKeys.FULLSCREEN_SHORTCUT)
        _save_shortcut(
            self.toggle_subtitles_edit, SettingKeys.TOGGLE_SUBTITLES_SHORTCUT
        )

        super().accept()
