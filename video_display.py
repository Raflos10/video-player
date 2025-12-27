from PySide6 import QtCore, QtWidgets, QtGui, QtMultimedia, QtMultimediaWidgets


class VideoDisplay(QtMultimediaWidgets.QVideoWidget):
    fullscreenToggled = QtCore.Signal()
    fileDialogRequested = QtCore.Signal()
    playToggled = QtCore.Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.mediaStatus = QtMultimedia.QMediaPlayer.MediaStatus.NoMedia

        self.busyIndicator = QtWidgets.QProgressBar(self)
        self.busyIndicator.setRange(0, 0)  # Indeterminate
        self.busyIndicator.setStyleSheet("background-color: transparent;")
        self.busyIndicator.setVisible(False)

        self.text = QtWidgets.QLabel("Click here to load a video", self)
        self.text.setStyleSheet("font-size: 20px; background-color: transparent;")
        self.text.setVisible(True)

        self.setMouseTracking(True)

    def connect_signals(self, media_controller, toggle_fullscreen, file_dialog_handler):
        self.fullscreenToggled.connect(toggle_fullscreen)
        self.fileDialogRequested.connect(file_dialog_handler)
        self.playToggled.connect(media_controller.toggle_playback)

    def set_media_status(self, status):
        self.mediaStatus = status
        self.busyIndicator.setVisible(status == QtMultimedia.QMediaPlayer.MediaStatus.LoadingMedia)
        self.text.setVisible(status == QtMultimedia.QMediaPlayer.MediaStatus.NoMedia)
        self.update()

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
        self.busyIndicator.move(self.width() // 2 - self.busyIndicator.width() // 2,
                                self.height() // 2 - self.busyIndicator.height() // 2)
        self.text.move(self.width() // 2 - self.text.width() // 2,
                        self.height() // 2 - self.text.height() // 2)
