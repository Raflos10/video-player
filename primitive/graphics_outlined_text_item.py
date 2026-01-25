from PySide6 import QtWidgets, QtGui, QtCore


class GraphicsOutlinedTextItem(QtWidgets.QGraphicsTextItem):
    def __init__(self, outline_width=2, outline_color=None, text_color=None):
        super().__init__()

        self.outline_width = outline_width
        self.outline_color = outline_color or QtGui.QColor("black")
        self.text_color = text_color or QtGui.QColor("white")

    def setPlainText(self, text):
        super().setPlainText(text)
        if text:
            self.apply_outline_format()

    def set_outline_width(self, outline_width):
        self.outline_width = outline_width
        if self.toPlainText():
            self.apply_outline_format()

    def set_outline_color(self, color):
        self.outline_color = color
        if self.toPlainText():
            self.apply_outline_format()

    def set_text_color(self, color):
        self.text_color = color
        if self.toPlainText():
            self.apply_outline_format()

    def apply_outline_format(self):
        cursor = QtGui.QTextCursor(self.document())
        cursor.select(QtGui.QTextCursor.SelectionType.Document)

        outline_format = QtGui.QTextCharFormat()
        outline_format.setForeground(self.text_color)

        outline_pen = QtGui.QPen(
            self.outline_color,
            self.outline_width,
            QtCore.Qt.PenStyle.SolidLine,
            QtCore.Qt.PenCapStyle.RoundCap,
            QtCore.Qt.PenJoinStyle.RoundJoin
        )
        outline_format.setTextOutline(outline_pen)
        cursor.mergeCharFormat(outline_format)
