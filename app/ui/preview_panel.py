"""Preview panel with header and rendered HTML view."""

from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout, QWidget
from PySide6.QtWebEngineWidgets import QWebEngineView


class PreviewPanel(QWidget):
    """Right-side live preview panel."""

    def __init__(self, web_view: QWebEngineView, parent=None) -> None:
        super().__init__(parent)
        self._preview = web_view
        self._build_ui()

    @property
    def web_view(self) -> QWebEngineView:
        return self._preview

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        header = QFrame()
        header.setObjectName("panelHeader")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(12, 8, 12, 8)

        title = QLabel("Preview")
        title.setObjectName("panelTitle")
        header_layout.addWidget(title)
        header_layout.addStretch()

        preview_frame = QFrame()
        preview_frame.setObjectName("previewFrame")
        preview_layout = QVBoxLayout(preview_frame)
        preview_layout.setContentsMargins(0, 0, 0, 0)
        preview_layout.addWidget(self._preview)

        root.addWidget(header)
        root.addWidget(preview_frame, 1)
