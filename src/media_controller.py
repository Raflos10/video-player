from PySide6 import QtCore, QtMultimedia

from subtitle.subtitle import Subtitle
from subtitle.subtitle_loader import load_subtitles


class MediaController:
    def __init__(self, video_item):
        self.mediaPlayer = QtMultimedia.QMediaPlayer()
        self.audioOutput = QtMultimedia.QAudioOutput()
        self.audioOutput.setVolume(1.0)
        self.mediaPlayer.setAudioOutput(self.audioOutput)
        self.mediaPlayer.setVideoOutput(video_item)
        self.subtitles = None

    def connect_signals(self, video_controls, video_display):
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

    def load_media(self, file_path):
        self.mediaPlayer.setSource(QtCore.QUrl.fromLocalFile(file_path))
        subs_content = load_subtitles(file_path)
        if subs_content:
            self.subtitles = Subtitle(subs_content)
        self.mediaPlayer.play()

    def toggle_playback(self):
        if (
            self.mediaPlayer.playbackState()
            == QtMultimedia.QMediaPlayer.PlaybackState.PlayingState
        ):
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    @staticmethod
    def is_media_loaded(status):
        return status in (
            QtMultimedia.QMediaPlayer.MediaStatus.LoadedMedia,
            QtMultimedia.QMediaPlayer.MediaStatus.BufferedMedia,
            QtMultimedia.QMediaPlayer.MediaStatus.BufferingMedia,
        )
