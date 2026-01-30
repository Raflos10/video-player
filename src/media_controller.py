import logging
from collections.abc import Callable
from typing import TYPE_CHECKING

from PySide6 import QtCore, QtMultimedia
from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtMultimediaWidgets import QGraphicsVideoItem
from PySide6.QtWidgets import QApplication

from subtitle.subtitle import Subtitle
from subtitle.subtitle_loader import load_subtitles

logger = logging.getLogger(__name__)

try:
    from mpris_interface import MPRISInterface

    MPRIS_AVAILABLE = True
except ImportError:
    MPRISInterface = None

    MPRIS_AVAILABLE = False
    logger.info(
        "MPRIS interface not available. Install dbus-python for Linux media controls."
    )

if TYPE_CHECKING:
    from widgets.video_controls import VideoControls
    from widgets.video_display import VideoDisplay


class MediaController:
    def __init__(self, video_item: QGraphicsVideoItem) -> None:
        self.mediaPlayer = QtMultimedia.QMediaPlayer()
        self.audioOutput = QtMultimedia.QAudioOutput()
        self.audioOutput.setVolume(1.0)
        self.mediaPlayer.setAudioOutput(self.audioOutput)
        self.mediaPlayer.setVideoOutput(video_item)
        self.subtitles = None

        self.mpris = None
        if MPRIS_AVAILABLE:
            try:
                self.mpris = MPRISInterface(self, app_name="VideoPlayer")
                logger.info("MPRIS interface initialized successfully")
            except Exception as e:
                logger.info("Failed to initialize MPRIS: %s", e)

    def connect_signals(
        self,
        video_controls: VideoControls,
        video_display: VideoDisplay,
        set_main_window_title: Callable[str],
    ) -> None:
        self.mediaPlayer.mediaStatusChanged.connect(
            lambda status: video_display.set_media_status(status)
        )
        self.mediaPlayer.positionChanged.connect(
            lambda pos: video_display.update_subtitle(pos, self.subtitles)
        )
        self.mediaPlayer.positionChanged.connect(
            lambda pos: video_controls.set_current_time(pos / 1000)
        )
        self.mediaPlayer.durationChanged.connect(
            lambda dur: video_controls.set_duration(dur / 1000)
        )
        self.mediaPlayer.playbackStateChanged.connect(
            lambda status: video_controls.set_playback_status(status)
        )
        self.mediaPlayer.mediaStatusChanged.connect(
            lambda status: video_controls.set_enabled(self.is_media_loaded(status))
        )
        self.audioOutput.mutedChanged.connect(video_controls.set_muted_value)

        self.mediaPlayer.metaDataChanged.connect(
            lambda: self.on_metadata_update(set_main_window_title)
        )

    def load_media(self, file_path: str) -> None:
        self.mediaPlayer.setSource(QtCore.QUrl.fromLocalFile(file_path))
        subs_content = load_subtitles(file_path)
        if subs_content:
            self.subtitles = Subtitle(subs_content)

        if self.mpris:
            self.mpris.update_metadata(file_path)

        self.mediaPlayer.play()

    def on_metadata_update(self, set_main_window_title: Callable[str]) -> None:
        title = (
            self.mediaPlayer.metaData().value(QtMultimedia.QMediaMetaData.Key.Title)
            or QApplication.applicationName()
        )
        set_main_window_title(title)

    def toggle_playback(self) -> None:
        if (
            self.mediaPlayer.playbackState()
            == QtMultimedia.QMediaPlayer.PlaybackState.PlayingState
        ):
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    @staticmethod
    def is_media_loaded(status: QMediaPlayer.MediaStatus) -> bool:
        return status in (
            QtMultimedia.QMediaPlayer.MediaStatus.LoadedMedia,
            QtMultimedia.QMediaPlayer.MediaStatus.BufferedMedia,
            QtMultimedia.QMediaPlayer.MediaStatus.BufferingMedia,
        )
