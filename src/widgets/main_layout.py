from PySide6 import QtWidgets, QtCore, QtGui

from widgets.video_controls import VideoControls
from widgets.video_display import VideoDisplay


class MainLayout(QtWidgets.QWidget):
    def __init__(self, parent, video_display: VideoDisplay, video_controls: VideoControls, is_fullscreen: bool):
        super().__init__(parent)
        self.is_fullscreen = is_fullscreen
        QtWidgets.QApplication.instance().installEventFilter(self)

        self.video_controls = video_controls
        self.video_display = video_display

        self.overlay_container = QtWidgets.QWidget(self)
        overlay_layout = QtWidgets.QVBoxLayout(self.overlay_container)
        overlay_layout.setContentsMargins(0, 0, 0, 0)
        overlay_layout.setSpacing(0)

        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.main_layout.addWidget(self.overlay_container)

        overlay_layout.addWidget(video_display)

        self.is_overlay_mode = is_fullscreen
        self.set_overlay_mode(is_fullscreen)

    def connect_signals(self, fullscreen_toggled: QtCore.Signal(bool)):
        fullscreen_toggled.connect(self.on_fullscreen_toggle)

    def set_overlay_mode(self, value: bool):
        if value:
            self.main_layout.removeWidget(self.video_controls)
            self.video_controls.setParent(self.overlay_container)
            self.position_controls_at_bottom()
        else:
            self.video_controls.setParent(self)
            self.main_layout.addWidget(self.video_controls)
        self.is_overlay_mode = value

    def position_controls_at_bottom(self):
        if not self.is_overlay_mode:
            return

        display_rect = self.video_display.rect()
        controls_size = self.video_controls.size()
        controls_hint = self.video_controls.sizeHint()

        controls_height = max(controls_size.height(), controls_hint.height())

        y_pos = display_rect.height() - controls_height

        self.video_controls.setGeometry(
            0, y_pos,
            display_rect.width(),
            controls_height
        )
        self.video_controls.raise_()

    def eventFilter(self, obj, event):
        if self.is_fullscreen and event.type() == QtCore.QEvent.Type.MouseMove:
            global_pos = QtGui.QCursor.pos()
            local_pos = self.mapFromGlobal(global_pos)

            if self.rect().contains(local_pos):
                if self.video_controls.is_mouse_near(local_pos):
                    self.video_controls.show()
                else:
                    self.video_controls.hide()

        return super().eventFilter(obj, event)

    def resizeEvent(self, event):
        """Reposition controls when window resizes in overlay mode"""
        super().resizeEvent(event)
        if self.is_overlay_mode:
            self.position_controls_at_bottom()

    def on_fullscreen_toggle(self, is_fullscreen: bool):
        self.is_fullscreen = is_fullscreen
        self.video_controls.setVisible(not is_fullscreen)
        self.set_overlay_mode(is_fullscreen)
