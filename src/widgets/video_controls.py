from PySide6 import QtCore, QtWidgets, QtMultimedia
from primitive.slider import ClickableSlider
from utils.helpers import format_time


class VideoControls(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFixedHeight(80)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        top_row = QtWidgets.QHBoxLayout()
        top_row.setSpacing(10)

        self.current_time_label = QtWidgets.QLabel("0:00")
        top_row.addWidget(self.current_time_label)

        self.seek_slider = ClickableSlider(QtCore.Qt.Orientation.Horizontal)
        self.seek_slider.setRange(0, 1000)
        top_row.addWidget(self.seek_slider)

        self.duration_label = QtWidgets.QLabel("0:00")
        top_row.addWidget(self.duration_label)

        main_layout.addLayout(top_row)

        bottom_row = QtWidgets.QHBoxLayout()
        bottom_row.setSpacing(10)

        self.play_button = QtWidgets.QPushButton("Play")
        bottom_row.addWidget(self.play_button)

        self.stop_button = QtWidgets.QPushButton("Stop")
        bottom_row.addWidget(self.stop_button)

        bottom_row.addStretch()

        volume_label = QtWidgets.QLabel("Volume")
        bottom_row.addWidget(volume_label)

        self.volume_slider = ClickableSlider(QtCore.Qt.Orientation.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(100)
        self.volume_slider.setFixedWidth(150)
        bottom_row.addWidget(self.volume_slider)

        self.mute_button = QtWidgets.QPushButton("Mute")
        bottom_row.addWidget(self.mute_button)

        main_layout.addLayout(bottom_row)

        self.set_enabled(False)

    def connect_signals(self, media_controller):
        self.seek_slider.sliderReleased.connect(
            lambda: media_controller.mediaPlayer.setPosition(self.seek_slider.value())
        )
        self.play_button.clicked.connect(media_controller.toggle_playback)
        self.stop_button.clicked.connect(lambda: media_controller.mediaPlayer.stop())
        self.volume_slider.valueChanged.connect(
            lambda v: media_controller.audioOutput.setVolume(v / 100.0)
        )
        self.mute_button.clicked.connect(
            lambda: media_controller.audioOutput.setMuted(
                not media_controller.audioOutput.isMuted()
            )
        )

    def set_current_time(self, time):
        self.current_time_label.setText(format_time(time))
        if not self.seek_slider.isSliderDown():
            self.seek_slider.setValue(int(time * 1000))

    def set_duration(self, duration):
        self.duration_label.setText(format_time(duration))
        self.seek_slider.setMaximum(int(duration * 1000))

    def set_playback_status(self, status):
        if status == QtMultimedia.QMediaPlayer.PlaybackState.PlayingState:
            self.play_button.setText("Pause")
        else:
            self.play_button.setText("Play")

    def set_enabled(self, is_enabled):
        self.play_button.setEnabled(is_enabled)
        self.stop_button.setEnabled(is_enabled)
        self.seek_slider.setEnabled(is_enabled)
        self.volume_slider.setEnabled(is_enabled)
        self.mute_button.setEnabled(is_enabled)
