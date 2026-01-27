class SettingKeys:
    SHOW_MENU_BAR = "appearance/show_menu_bar"
    SEEK_STEP = "behavior/seek_step"
    SAVE_POSITION_ON_EXIT = "behavior/save_position_on_exit"
    PLAY_PAUSE_SHORTCUT = "shortcuts/play_pause"
    SEEK_FORWARD_SHORTCUT = "shortcuts/seek_forward"
    SEEK_BACKWARD_SHORTCUT = "shortcuts/seek_backward"
    TOGGLE_MUTE_SHORTCUT = "shortcuts/toggle_mute"
    FULLSCREEN_SHORTCUT = "shortcuts/toggle_fullscreen"
    TOGGLE_SUBTITLES_SHORTCUT = "shortcuts/toggle_subtitles"
    ENABLE_SUBTITLES = "subtitles/enable"
    SUBTITLE_FONT_SCALE = "subtitles/font_scale"
    SUBTITLE_OUTLINE_SIZE = "subtitles/outline_size"


DEFAULTS = {
    SettingKeys.SHOW_MENU_BAR: True,
    SettingKeys.SEEK_STEP: 10,
    SettingKeys.SAVE_POSITION_ON_EXIT: False,
    SettingKeys.PLAY_PAUSE_SHORTCUT: "Space",
    SettingKeys.SEEK_FORWARD_SHORTCUT: "Right",
    SettingKeys.SEEK_BACKWARD_SHORTCUT: "Left",
    SettingKeys.TOGGLE_MUTE_SHORTCUT: "M",
    SettingKeys.FULLSCREEN_SHORTCUT: "F",
    SettingKeys.TOGGLE_SUBTITLES_SHORTCUT: "S",
    SettingKeys.ENABLE_SUBTITLES: True,
    SettingKeys.SUBTITLE_FONT_SCALE: 4.0,
    SettingKeys.SUBTITLE_OUTLINE_SIZE: 5,
}
