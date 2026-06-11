"""Entry point for Markdown PDF Studio."""

import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

from app.ui.main_window import MainWindow


def main() -> int:
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    app = QApplication(sys.argv)
    app.setApplicationName("Markdown PDF Studio")
    app.setOrganizationName("Markdown PDF Studio")
    app.setApplicationDisplayName("Markdown PDF Studio")

    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
