from PySide6 import QtCore, QtWidgets, QtMultimedia, QtMultimediaWidgets, QtGui

from settings.settings_manager import settings_manager
from subtitle.subtitle_graphics_item import SubtitleGraphicsItem
from settings.setting_keys import SettingKeys


class VideoDisplay(QtWidgets.QGraphicsView):
    fullscreenToggled = QtCore.Signal()
    fileDialogRequested = QtCore.Signal()
    playToggled = QtCore.Signal()

    def __init__(self, parent=None):
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
        # self.busyIndicator.setStyleSheet("background-color: rgba(0,0,0,128); color: white;")
        # self.busyProxy.setWidget(self.busyIndicator)
        # self.graphics_scene.addItem(self.busyProxy)

        self.video_item.setZValue(0)
        self.center_text.setZValue(1)
        self.subtitle_item.setZValue(2)
        # self.busyProxy.setZValue(3)

        self.setMouseTracking(True)

    def connect_signals(self, media_controller, toggle_fullscreen, file_dialog_handler):
        settings_manager.settings_changed.connect(self.on_settings_changed)

        self.fullscreenToggled.connect(toggle_fullscreen)
        self.fileDialogRequested.connect(file_dialog_handler)
        self.playToggled.connect(media_controller.toggle_playback)

    def on_settings_changed(self, key: str, value):
        if key == SettingKeys.ENABLE_SUBTITLES:
            self.subtitle_item.setVisible(value)

    def update_subtitle(self, position_ms, subtitles):
        if subtitles:
            entries = subtitles.get_all_at_time(position_ms)
            if entries != self.current_subtitle_entries:
                self.on_new_subtitles(entries)

    def on_new_subtitles(self, entries):
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

    def set_media_status(self, status):
        self.mediaStatus = status
        # self.busyProxy.setVisible(status == QtMultimedia.QMediaPlayer.MediaStatus.LoadingMedia)
        self.center_text.setVisible(
            status == QtMultimedia.QMediaPlayer.MediaStatus.NoMedia
        )
        self.update_scene_rect()

    def update_scene_rect(self):
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

        self.subtitle_item.setPos(
            center_x - self.subtitle_item.boundingRect().width() / 2,
            self.height() - self.subtitle_item.boundingRect().height() - 20,
        )
        # self.busyProxy.setPos(center_x - self.busyProxy.boundingRect().width() / 2, center_y - self.busyProxy.boundingRect().height() / 2)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            if self.mediaStatus == QtMultimedia.QMediaPlayer.MediaStatus.NoMedia:
                self.fileDialogRequested.emit()
            else:
                self.playToggled.emit()
        super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.fullscreenToggled.emit()
        super().mouseDoubleClickEvent(event)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_scene_rect()
