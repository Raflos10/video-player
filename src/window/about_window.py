from PySide6 import QtWidgets
from PySide6.QtWidgets import QWidget

LINK_URL = "https://github.com/Raflos10/video-player"


class AboutDialog(QtWidgets.QDialog):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("About")
        self.setModal(True)

        layout = QtWidgets.QVBoxLayout(self)

        app_label = QtWidgets.QLabel("Video Player")
        app_label.setStyleSheet("font-size: 14px;")
        layout.addWidget(app_label)

        layout.addSpacing(10)

        maker_label = QtWidgets.QLabel("Made by Raflos")
        maker_label.setStyleSheet("font-size: 14px;")
        layout.addWidget(maker_label)

        layout.addSpacing(10)

        link_label = QtWidgets.QLabel(
            f"<a href='{LINK_URL}'>Video Player on Github</a>"
        )
        link_label.setOpenExternalLinks(True)
        link_label.setStyleSheet("font-size: 14px;")
        layout.addWidget(link_label)

        layout.addSpacing(10)

        button_box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.StandardButton.Ok
        )
        button_box.accepted.connect(self.accept)
        layout.addWidget(button_box)
