from collections.abc import Callable

from PySide6 import QtCore, QtGui, QtMultimedia, QtMultimediaWidgets, QtWidgets
from PySide6.QtGui import QEnterEvent, QMouseEvent, QResizeEvent
from PySide6.QtWidgets import QWidget

from media_controller import MediaController
from settings.setting_keys import SettingKeys
from settings.settings_manager import settings_manager
from subtitle.subtitle import Subtitle
from subtitle.subtitle_entry import SubtitleEntry
from subtitle.subtitle_graphics_item import SubtitleGraphicsItem


class VideoDisplay(QtWidgets.QGraphicsView):
    fullscreen_toggled = QtCore.Signal()
    file_dialog_requested = QtCore.Signal()
    play_toggled = QtCore.Signal()

    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)

        self.mediaStatus = (
            QtMultimedia.QMediaPlayer.MediaStatus.NoMedia
        )  # TODO: is it necessary?

        self.graphics_scene = QtWidgets.QGraphicsScene(self)
        self.setScene(self.graphics_scene)

        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setStyleSheet("background-color: black;")

        self.video_item = QtMultimediaWidgets.QGraphicsVideoItem()
        self.graphics_scene.addItem(self.video_item)

        self.center_text = QtWidgets.QGraphicsTextItem("Click here to load a video")
        self.center_text.setDefaultTextColor(QtCore.Qt.GlobalColor.white)
        self.center_text.setFont(QtGui.QFont("Arial", 20))
        self.graphics_scene.addItem(self.center_text)

        self.subtitle_item = SubtitleGraphicsItem()
        self.current_subtitle_entries = []
        self.graphics_scene.addItem(self.subtitle_item)

        # self.busyProxy = QtWidgets.QGraphicsProxyWidget()
        # self.busyIndicator = QtWidgets.QProgressBar()
        # self.busyIndicator.setRange(0, 0)  # Indeterminate
        # self.busyIndicator.setStyleSheet(
        #   "background-color: rgba(0,0,0,128); color: white;"
        # )
        # self.busyProxy.setWidget(self.busyIndicator)
        # self.graphics_scene.addItem(self.busyProxy)

        self.video_item.setZValue(0)
        self.center_text.setZValue(1)
        self.subtitle_item.setZValue(2)

        self.cursor_hide_timer = QtCore.QTimer(self)
        self.cursor_hide_timer.timeout.connect(self.hide_cursor)
        self.cursor_hide_timer.setSingleShot(True)
        self.cursor_visible = True

    def connect_signals(
        self,
        media_controller: MediaController,
        toggle_fullscreen: Callable,
        file_dialog_handler: Callable,
    ) -> None:
        settings_manager.settings_changed.connect(self.on_settings_changed)

        self.fullscreen_toggled.connect(toggle_fullscreen)
        self.file_dialog_requested.connect(file_dialog_handler)
        self.play_toggled.connect(media_controller.toggle_playback)

    def on_settings_changed(self, key: str, value: bool) -> None:
        if key == SettingKeys.ENABLE_SUBTITLES:
            self.subtitle_item.setVisible(value)

    def update_subtitle(self, position_ms: int, subtitles: Subtitle) -> None:
        if subtitles:
            entries = subtitles.get_all_at_time(position_ms)
            if entries != self.current_subtitle_entries:
                self.on_new_subtitles(entries)

    def on_new_subtitles(self, entries: list[SubtitleEntry]) -> None:
        enable_subtitles = settings_manager.value(SettingKeys.ENABLE_SUBTITLES)
        if len(entries) == 0 or not enable_subtitles:
            self.subtitle_item.setVisible(False)
            self.current_subtitle_entries = []
            return

        # TODO: loop
        self.current_subtitle_entries = entries
        entry = entries[0]
        self.subtitle_item.setPlainText(entry.text)
        self.update_scene_rect()

    def set_media_status(self, status: QtMultimedia.QMediaPlayer.MediaStatus) -> None:
        self.mediaStatus = status
        self.center_text.setVisible(
            status == QtMultimedia.QMediaPlayer.MediaStatus.NoMedia
        )
        self.update_scene_rect()

    def update_scene_rect(self) -> None:
        self.graphics_scene.setSceneRect(0, 0, self.width(), self.height())
        self.video_item.setSize(QtCore.QSizeF(self.width(), self.height()))

        center_x = self.width() / 2
        center_y = self.height() / 2

        self.center_text.setPos(
            center_x - self.center_text.boundingRect().width() / 2,
            center_y - self.center_text.boundingRect().height() / 2,
        )

        subtitle_max_width = self.width() * 0.9
        self.subtitle_item.setTextWidth(subtitle_max_width)

        self.subtitle_item.set_view_height(self.height())
        self.subtitle_item.setPos(
            center_x - self.subtitle_item.boundingRect().width() / 2,
            (self.height() * 0.95) - self.subtitle_item.boundingRect().height(),
        )

        # self.busyProxy.setPos(
        #   center_x - self.busyProxy.boundingRect().width() / 2,
        #   center_y - self.busyProxy.boundingRect().height() / 2
        # )

    def hide_cursor(self) -> None:
        self.setCursor(QtCore.Qt.CursorShape.BlankCursor)
        self.cursor_visible = False

    def show_cursor(self) -> None:
        self.unsetCursor()
        self.cursor_visible = True

    def restart_cursor_timer(self) -> None:
        if not self.cursor_visible:
            self.show_cursor()

        self.cursor_hide_timer.start(3000)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:  # noqa: N802
        self.restart_cursor_timer()
        super().mouseMoveEvent(event)

    def mousePressEvent(self, event: QMouseEvent) -> None:  # noqa: N802
        self.restart_cursor_timer()

        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            if self.mediaStatus == QtMultimedia.QMediaPlayer.MediaStatus.NoMedia:
                self.file_dialog_requested.emit()
            else:
                self.play_toggled.emit()
        super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:  # noqa: N802
        self.restart_cursor_timer()

        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.fullscreen_toggled.emit()
        super().mouseDoubleClickEvent(event)

    def enterEvent(self, event: QEnterEvent) -> None:  # noqa: N802
        self.restart_cursor_timer()
        super().enterEvent(event)

    def leaveEvent(self, event: QMouseEvent) -> None:  # noqa: N802
        self.cursor_hide_timer.stop()
        if not self.cursor_visible:
            self.show_cursor()
        super().leaveEvent(event)

    def resizeEvent(self, event: QResizeEvent) -> None:  # noqa: N802
        super().resizeEvent(event)
        self.update_scene_rect()
