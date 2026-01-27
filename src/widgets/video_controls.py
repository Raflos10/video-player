from PySide6 import QtCore, QtWidgets, QtMultimedia
from PySide6.QtCore import QPoint

from media_controller import MediaController
from primitive.slider import ClickableSlider
from utils.helpers import format_time

MOUSE_NEAR_THRESHOLD = 50


class VideoControls(QtWidgets.QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFixedHeight(40)

        self.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.setStyleSheet("""
            QFrame { 
                background-color: rgb(35, 35, 35); 
                border-top: 1px solid rgb(60, 60, 60);
            }
            QPushButton {
                background-color: transparent;
                border: none;
                border-radius: 4px;
                padding: 4px;
                color: rgb(220, 220, 220);
            }
            QPushButton:hover {
                background-color: rgb(60, 60, 60);
            }
            QPushButton:pressed {
                background-color: rgb(80, 80, 80);
            }
            QPushButton:disabled {
                color: rgb(100, 100, 100);
            }
        """)

        main_layout = QtWidgets.QHBoxLayout(self)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(10)

        style = self.style()

        # Play/Pause button with icon
        self.play_button = QtWidgets.QPushButton()
        self.play_button.setIcon(style.standardIcon(QtWidgets.QStyle.StandardPixmap.SP_MediaPlay))
        self.play_button.setIconSize(QtCore.QSize(18, 18))
        self.play_button.setFixedSize(24, 24)
        self.play_button.setToolTip("Play")
        main_layout.addWidget(self.play_button)

        # Current time label
        self.current_time_label = QtWidgets.QLabel("0:00")
        self.current_time_label.setMinimumWidth(36)
        self.current_time_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.current_time_label)

        # Seek slider
        self.seek_slider = ClickableSlider(QtCore.Qt.Orientation.Horizontal)
        self.seek_slider.setRange(0, 1000)
        main_layout.addWidget(self.seek_slider, 1)  # Stretch factor of 1

        # Duration label
        self.duration_label = QtWidgets.QLabel("0:00")
        self.duration_label.setMinimumWidth(36)
        self.duration_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.duration_label)

        # Volume slider
        self.volume_slider = ClickableSlider(QtCore.Qt.Orientation.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(100)
        self.volume_slider.setFixedWidth(100)
        main_layout.addWidget(self.volume_slider)

        # Mute button with icon
        self.mute_button = QtWidgets.QPushButton()
        self.mute_button.setIcon(style.standardIcon(QtWidgets.QStyle.StandardPixmap.SP_MediaVolume))
        self.mute_button.setIconSize(QtCore.QSize(20, 20))
        self.mute_button.setFixedSize(24, 24)
        self.mute_button.setToolTip("Mute")
        main_layout.addWidget(self.mute_button)

        # Store icons for state changes
        self.play_icon = style.standardIcon(QtWidgets.QStyle.StandardPixmap.SP_MediaPlay)
        self.pause_icon = style.standardIcon(QtWidgets.QStyle.StandardPixmap.SP_MediaPause)
        self.volume_icon = style.standardIcon(QtWidgets.QStyle.StandardPixmap.SP_MediaVolume)
        self.mute_icon = style.standardIcon(QtWidgets.QStyle.StandardPixmap.SP_MediaVolumeMuted)

        self.set_enabled(False)

    def connect_signals(self, media_controller: MediaController):
        self.seek_slider.sliderReleased.connect(
            lambda: media_controller.mediaPlayer.setPosition(self.seek_slider.value())
        )
        self.play_button.clicked.connect(media_controller.toggle_playback)
        self.volume_slider.valueChanged.connect(
            lambda v: media_controller.audioOutput.setVolume(v / 100.0)
        )
        self.mute_button.clicked.connect(
            lambda: media_controller.audioOutput.setMuted(not media_controller.audioOutput.isMuted()))

    def set_current_time(self, time):
        self.current_time_label.setText(format_time(time))
        if not self.seek_slider.isSliderDown():
            self.seek_slider.setValue(int(time * 1000))

    def set_duration(self, duration):
        self.duration_label.setText(format_time(duration))
        self.seek_slider.setMaximum(int(duration * 1000))

    def set_playback_status(self, status):
        if status == QtMultimedia.QMediaPlayer.PlaybackState.PlayingState:
            self.play_button.setIcon(self.pause_icon)
            self.play_button.setToolTip("Pause")
        else:
            self.play_button.setIcon(self.play_icon)
            self.play_button.setToolTip("Play")

    def set_muted_value(self, is_muted: bool):
        if is_muted:
            self.mute_button.setIcon(self.mute_icon)
            self.mute_button.setToolTip("Unmute")
        else:
            self.mute_button.setIcon(self.volume_icon)
            self.mute_button.setToolTip("Mute")

    def set_enabled(self, is_enabled):
        self.play_button.setEnabled(is_enabled)
        self.seek_slider.setEnabled(is_enabled)
        self.volume_slider.setEnabled(is_enabled)
        self.mute_button.setEnabled(is_enabled)

    def is_mouse_near(self, mouse_position: QPoint):
        return mouse_position.y() >= self.y() - MOUSE_NEAR_THRESHOLD
