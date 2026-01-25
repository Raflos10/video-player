from typing import Optional

from PySide6 import QtCore

from primitive.graphics_outlined_text_item import GraphicsOutlinedTextItem
from setting_keys import SettingKeys
from settings_manager import settings_manager


class SubtitleGraphicsItem(GraphicsOutlinedTextItem):
    def __init__(self):
        super().__init__()

        self.setVisible(False)
        self.update_subtitle_style()

        self.connect_signals()

    def connect_signals(self):
        settings_manager.settings_changed.connect(self.on_settings_changed)

    def setPlainText(self, text: Optional[str]):
        super().setPlainText(text)
        self.setVisible(bool(text))

    def on_settings_changed(self, key: str):
        if key == SettingKeys.SUBTITLE_FONT_SIZE:
            self.update_subtitle_style()

    def update_subtitle_style(self, font_size=None):
        font = self.font()

        text_option = self.document().defaultTextOption()
        text_option.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.document().setDefaultTextOption(text_option)

        if font_size:
            font.setPointSize(font_size)
        else:
            font.setPointSize(int(settings_manager.value(SettingKeys.SUBTITLE_FONT_SIZE)))

        font.setBold(True)
        self.setFont(font)

        if self.toPlainText():
            self.apply_outline_format()
