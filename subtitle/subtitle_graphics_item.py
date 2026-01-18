from typing import Optional

from PySide6 import QtWidgets, QtGui, QtCore
from setting_keys import SettingKeys
from settings_manager import settings_manager


class SubtitleGraphicsItem(QtWidgets.QGraphicsTextItem):
    def __init__(self):
        super().__init__()
        self.setVisible(False)
        self.update_subtitle_style()

        self.connect_signals()

    def connect_signals(self):
        settings_manager.settings_changed.connect(self.on_settings_changed)

    def set_text(self, text: Optional[str]):
        self.setPlainText(text)
        self.setVisible(bool(text))

    def on_settings_changed(self, key: str):
        if key == SettingKeys.SUBTITLE_FONT_SIZE:
            self.update_subtitle_style()

    def update_subtitle_style(self, font_size=None):
        font = self.font()

        if font_size:
            font.setPointSize(font_size)
        else:
            font.setPointSize(int(settings_manager.value(SettingKeys.SUBTITLE_FONT_SIZE)))

        font.setBold(True)
        self.setFont(font)

        self.setDefaultTextColor(QtGui.QColor("white"))

    def paint(self, painter, option, widget=None):
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        path = QtGui.QPainterPath()
        path.addText(0, 0, self.font(), self.toPlainText())

        painter.setPen(QtGui.QPen(QtCore.Qt.GlobalColor.black, 5))
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        painter.drawPath(path)

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(QtCore.Qt.GlobalColor.white)
        painter.drawPath(path)
