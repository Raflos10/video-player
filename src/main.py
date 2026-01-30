import logging
import sys

from PySide6 import QtWidgets
from PySide6.QtGui import QIcon

from theme import Theme
from utils.audio_check import check_audio_with_prompt
from window.application_window import ApplicationWindow

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s",
)


def main() -> None:
    app = QtWidgets.QApplication([])
    app.setWindowIcon(
        QIcon.fromTheme("untitled-video-player", QIcon("assets/icon.svg"))
    )
    app.setStyleSheet(Theme.DARK)

    if not check_audio_with_prompt():
        sys.exit(1)

    file_path = sys.argv[1] if len(sys.argv) > 1 else None
    main_window = ApplicationWindow(file_path)
    main_window.resize(1280, 720)
    main_window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
