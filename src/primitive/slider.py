from collections.abc import Callable

from PySide6.QtCore import Qt
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QSlider, QStyle, QStyleOptionSlider, QToolTip, QWidget


class ClickableSlider(QSlider):
    def __init__(
        self, orientation: Qt.Orientation, parent: QWidget | None = None
    ) -> None:
        super().__init__(orientation, parent)
        self.setMouseTracking(True)
        self._format_callback: Callable[[int], str] | None = None

    def set_tooltip_formatter(self, callback: Callable[[int], str]) -> None:
        self._format_callback = callback

    def mousePressEvent(self, event: QMouseEvent) -> None:  # noqa: N802
        if event.button() == Qt.MouseButton.LeftButton:
            opt = QStyleOptionSlider()
            self.initStyleOption(opt)
            groove = self.style().subControlRect(
                QStyle.ComplexControl.CC_Slider,
                opt,
                QStyle.SubControl.SC_SliderGroove,
                self,
            )
            handle = self.style().subControlRect(
                QStyle.ComplexControl.CC_Slider,
                opt,
                QStyle.SubControl.SC_SliderHandle,
                self,
            )

            if self.orientation() == Qt.Orientation.Horizontal:
                slider_length = groove.width() - handle.width()
                slider_min = groove.x() + handle.width() // 2
                pos = event.position().x() - slider_min
            else:
                slider_length = groove.height() - handle.height()
                slider_min = groove.y() + handle.height() // 2
                pos = event.position().y() - slider_min

            value = QStyle.sliderValueFromPosition(
                self.minimum(), self.maximum(), int(pos), slider_length
            )

            self.setValue(value)

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:  # noqa: N802
        opt = QStyleOptionSlider()
        self.initStyleOption(opt)
        groove = self.style().subControlRect(
            QStyle.ComplexControl.CC_Slider,
            opt,
            QStyle.SubControl.SC_SliderGroove,
            self,
        )
        handle = self.style().subControlRect(
            QStyle.ComplexControl.CC_Slider,
            opt,
            QStyle.SubControl.SC_SliderHandle,
            self,
        )

        if self.orientation() == Qt.Orientation.Horizontal:
            slider_length = groove.width() - handle.width()
            slider_min = groove.x() + handle.width() // 2
            pos = event.position().x() - slider_min
        else:
            slider_length = groove.height() - handle.height()
            slider_min = groove.y() + handle.height() // 2
            pos = event.position().y() - slider_min

        value = QStyle.sliderValueFromPosition(
            self.minimum(), self.maximum(), int(pos), slider_length
        )

        if self._format_callback:
            tooltip_text = self._format_callback(value)
        else:
            tooltip_text = str(value)

        QToolTip.showText(event.globalPosition().toPoint(), tooltip_text, self)

        super().mouseMoveEvent(event)
