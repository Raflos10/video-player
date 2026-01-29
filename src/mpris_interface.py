from pathlib import Path
from typing import TYPE_CHECKING

import dbus
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop
from PySide6.QtMultimedia import QMediaPlayer

if TYPE_CHECKING:
    from media_controller import MediaController


class MPRISInterface(dbus.service.Object):
    MPRIS_PATH = "/org/mpris/MediaPlayer2"
    MPRIS_IFACE = "org.mpris.MediaPlayer2"
    PLAYER_IFACE = "org.mpris.MediaPlayer2.Player"
    PROPERTIES_IFACE = "org.freedesktop.DBus.Properties"

    def __init__(
        self, media_controller: MediaController, app_name: str = "VideoPlayer"
    ) -> None:
        DBusGMainLoop(set_as_default=True)
        bus_name = dbus.service.BusName(
            f"org.mpris.MediaPlayer2.{app_name}", bus=dbus.SessionBus()
        )
        super().__init__(bus_name, self.MPRIS_PATH)

        self.media_controller = media_controller
        self.app_name = app_name
        self._current_file = ""

        player = media_controller.mediaPlayer
        player.playbackStateChanged.connect(self._on_playback_state_changed)
        player.durationChanged.connect(lambda: self._notify_property("Metadata"))

    # noinspection PyUnusedLocal
    def _on_playback_state_changed(self, state: QMediaPlayer.PlaybackState) -> None:  # noqa: ARG002
        self._notify_property("PlaybackStatus", "CanPause", "CanPlay")

    def _notify_property(self, *properties: str) -> None:
        changed = {prop: getattr(self, prop) for prop in properties}
        self.PropertiesChanged(self.PLAYER_IFACE, changed, [])

    def update_metadata(self, file_path: str) -> None:
        self._current_file = file_path
        self._notify_property("Metadata")

    # org.mpris.MediaPlayer2 methods
    @dbus.service.method(dbus_interface=MPRIS_IFACE)
    def Raise(self) -> None:  # noqa: N802
        pass

    @dbus.service.method(dbus_interface=MPRIS_IFACE)
    def Quit(self) -> None:  # noqa: N802
        pass

    # org.mpris.MediaPlayer2.Player methods
    @dbus.service.method(dbus_interface=PLAYER_IFACE)
    def Play(self) -> None:  # noqa: N802
        if (
            self.media_controller.mediaPlayer.playbackState()
            != QMediaPlayer.PlaybackState.PlayingState
        ):
            self.media_controller.mediaPlayer.play()

    @dbus.service.method(dbus_interface=PLAYER_IFACE)
    def Pause(self) -> None:  # noqa: N802
        if (
            self.media_controller.mediaPlayer.playbackState()
            == QMediaPlayer.PlaybackState.PlayingState
        ):
            self.media_controller.mediaPlayer.pause()

    @dbus.service.method(dbus_interface=PLAYER_IFACE)
    def PlayPause(self) -> None:  # noqa: N802
        self.media_controller.toggle_playback()

    @dbus.service.method(dbus_interface=PLAYER_IFACE)
    def Stop(self) -> None:  # noqa: N802
        self.media_controller.mediaPlayer.stop()

    @dbus.service.method(dbus_interface=PLAYER_IFACE)
    def Next(self) -> None:  # noqa: N802
        pass

    @dbus.service.method(dbus_interface=PLAYER_IFACE)
    def Previous(self) -> None:  # noqa: N802
        pass

    @dbus.service.method(dbus_interface=PLAYER_IFACE, in_signature="x")
    def Seek(self, offset_microseconds: int) -> None:  # noqa: N802
        player = self.media_controller.mediaPlayer
        current_pos = player.position() * 1000
        player.setPosition(int((current_pos + offset_microseconds) / 1000))

    # noinspection PyUnusedLocal
    @dbus.service.method(dbus_interface=PLAYER_IFACE, in_signature="ox")
    def SetPosition(self, track_id: object, position_microseconds: int) -> None:  # noqa: N802, ARG002
        self.media_controller.mediaPlayer.setPosition(int(position_microseconds / 1000))

    @dbus.service.method(dbus_interface=PLAYER_IFACE, in_signature="s")
    def OpenUri(self, uri: str) -> None:  # noqa: N802
        pass

    # Properties
    @property
    def Identity(self) -> str:  # noqa: N802
        return self.app_name

    @property
    def SupportedUriSchemes(self) -> list[str]:  # noqa: N802
        return ["file"]

    @property
    def SupportedMimeTypes(self) -> list[str]:  # noqa: N802
        return [
            "video/mp4",
            "video/x-matroska",
            "video/avi",
            "video/quicktime",
            "video/webm",
        ]

    @property
    def PlaybackStatus(self) -> str:  # noqa: N802
        state = self.media_controller.mediaPlayer.playbackState()
        if state == QMediaPlayer.PlaybackState.PlayingState:
            return "Playing"
        if state == QMediaPlayer.PlaybackState.PausedState:
            return "Paused"
        return "Stopped"

    @property
    def Metadata(self) -> dict:  # noqa: N802
        metadata = {"mpris:trackid": dbus.ObjectPath("/org/mpris/MediaPlayer2/Track/0")}

        duration = self.media_controller.mediaPlayer.duration()
        if duration > 0:
            metadata["mpris:length"] = dbus.Int64(duration * 1000)

        if self._current_file:
            metadata["xesam:title"] = Path(self._current_file).name
            metadata["xesam:url"] = f"file://{self._current_file}"

        return dbus.Dictionary(metadata, signature="sv")

    @property
    def Volume(self) -> float:  # noqa: N802
        return self.media_controller.audioOutput.volume()

    @property
    def Position(self) -> int:  # noqa: N802
        return dbus.Int64(self.media_controller.mediaPlayer.position() * 1000)

    @property
    def CanPlay(self) -> bool:  # noqa: N802
        return (
            self.media_controller.mediaPlayer.playbackState()
            != QMediaPlayer.PlaybackState.PlayingState
        )

    @property
    def CanPause(self) -> bool:  # noqa: N802
        return (
            self.media_controller.mediaPlayer.playbackState()
            == QMediaPlayer.PlaybackState.PlayingState
        )

    @property
    def CanSeek(self) -> bool:  # noqa: N802
        return self.media_controller.mediaPlayer.isSeekable()

    @property
    def CanControl(self) -> bool:  # noqa: N802
        return True

    # D-Bus Properties interface
    # noinspection PyUnusedLocal
    @dbus.service.method(
        dbus_interface=PROPERTIES_IFACE, in_signature="ss", out_signature="v"
    )
    def Get(self, interface: str, property_name: str) -> object:  # noqa: ARG002, N802
        return getattr(self, property_name, None)

    @dbus.service.method(
        dbus_interface=PROPERTIES_IFACE, in_signature="s", out_signature="a{sv}"
    )
    def GetAll(self, interface: str) -> dict:  # noqa: N802
        if interface == self.PLAYER_IFACE:
            return dbus.Dictionary(
                {
                    "PlaybackStatus": self.PlaybackStatus,
                    "Metadata": self.Metadata,
                    "Volume": self.Volume,
                    "Position": self.Position,
                    "CanPlay": self.CanPlay,
                    "CanPause": self.CanPause,
                    "CanSeek": self.CanSeek,
                    "CanControl": self.CanControl,
                },
                signature="sv",
            )
        return dbus.Dictionary(
            {
                "Identity": self.Identity,
                "SupportedUriSchemes": self.SupportedUriSchemes,
                "SupportedMimeTypes": self.SupportedMimeTypes,
            },
            signature="sv",
        )

    @dbus.service.method(dbus_interface=PROPERTIES_IFACE, in_signature="ssv")
    def Set(self, interface: str, property_name: str, value: float | int | str) -> None:  # noqa: N802
        if interface == self.PLAYER_IFACE and property_name == "Volume":
            self.media_controller.audioOutput.setVolume(float(value))

    @dbus.service.signal(dbus_interface=PROPERTIES_IFACE, signature="sa{sv}as")
    def PropertiesChanged(  # noqa: N802
        self, interface: str, changed: dict, invalidated: list
    ) -> None:
        pass
