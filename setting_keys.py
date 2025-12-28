class SettingKeys:
    SHOW_MENU_BAR = "appearance/show_menu_bar"
    SEEK_STEP = "behavior/seek_step"
    SAVE_POSITION_ON_EXIT = "behavior/save_position_on_exit"
    PLAY_PAUSE_SHORTCUT = "shortcuts/play_pause"
    SEEK_FORWARD_SHORTCUT = "shortcuts/seek_forward"
    SEEK_BACKWARD_SHORTCUT = "shortcuts/seek_backward"
    FULLSCREEN_SHORTCUT = "shortcuts/fullscreen"

DEFAULTS = {
    SettingKeys.SHOW_MENU_BAR: True,
    SettingKeys.SEEK_STEP: 10,
    SettingKeys.SAVE_POSITION_ON_EXIT: False,
    SettingKeys.PLAY_PAUSE_SHORTCUT: "Space",
    SettingKeys.SEEK_FORWARD_SHORTCUT: "Right",
    SettingKeys.SEEK_BACKWARD_SHORTCUT: "Left",
    SettingKeys.FULLSCREEN_SHORTCUT: "F",
}
