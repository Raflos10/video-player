class Theme:
    DARK = """
    QWidget {
        background-color: #2d2d2d;
        color: #ffffff;
        font-family: 'Segoe UI', Arial, sans-serif;
    }

    QMenuBar {
        background-color: #1e1e1e;
        color: #ffffff;
        border-bottom: 1px solid #3d3d3d;
    }

    QMenuBar::item {
        background-color: transparent;
        padding: 4px 12px;
    }

    QMenuBar::item:selected {
        background-color: #3d3d3d;
    }

    QMenu {
        background-color: #2d2d2d;
        border: 1px solid #3d3d3d;
    }

    QMenu::item:selected {
        background-color: #3d3d3d;
    }

    QPushButton {
        background-color: #3d3d3d;
        border: 1px solid #4d4d4d;
        border-radius: 4px;
        padding: 6px 16px;
        min-width: 60px;
    }

    QPushButton:hover {
        background-color: #4d4d4d;
    }

    QPushButton:pressed {
        background-color: #5d5d5d;
    }

    QPushButton:disabled {
        background-color: #252525;
        color: #666666;
    }

    QSlider::groove:horizontal {
        border: 1px solid #3d3d3d;
        height: 6px;
        background-color: #1e1e1e;
        border-radius: 3px;
    }

    QSlider::handle:horizontal {
        background-color: #ffffff;
        border: 1px solid #3d3d3d;
        width: 14px;
        margin: -5px 0;
        border-radius: 7px;
    }

    QSlider::handle:horizontal:hover {
        background-color: #cccccc;
    }

    QSlider::handle:horizontal:disabled {
        background-color: #666666;
    }

    QSlider::sub-page:horizontal {
        background-color: #0078d4;
        border-radius: 3px;
    }

    QLabel {
        background-color: transparent;
        color: #ffffff;
    }

    QProgressBar {
        border: 2px solid #3d3d3d;
        border-radius: 5px;
        text-align: center;
        background-color: #1e1e1e;
    }

    QProgressBar::chunk {
        background-color: #0078d4;
        border-radius: 3px;
    }
    """
