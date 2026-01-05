from typing import Optional

from PySide6 import QtWidgets, QtGui, QtCore
from setting_keys import SettingKeys, DEFAULTS


class SubtitleGraphicsItem(QtWidgets.QGraphicsTextItem):
    def __init__(self):
        super().__init__()
        self.setVisible(False)
        self.update_subtitle_style()

    def set_text(self, text: Optional[str]):
        self.setPlainText(text)
        self.setVisible(bool(text))

    def update_subtitle_style(self, settings=None):
        if settings is None:
            settings = DEFAULTS

        font_size = settings.get(SettingKeys.SUBTITLE_FONT_SIZE, DEFAULTS[SettingKeys.SUBTITLE_FONT_SIZE])

        font = self.font()
        font.setPointSize(font_size)
        font.setBold(True)
        self.setFont(font)

        self.setDefaultTextColor(QtGui.QColor('white'))

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
