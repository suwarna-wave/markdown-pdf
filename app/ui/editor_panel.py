"""Editor panel with formatting toolbar and Markdown text area."""

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QColor, QKeySequence
from PySide6.QtWidgets import (
    QColorDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from app.editor.formatting import BOLD, ITALIC, UNDERLINE, color_format
from app.editor.markdown_editor import MarkdownEditor


class EditorPanel(QWidget):
    """Left-side editor with a compact formatting toolbar."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._editor = MarkdownEditor()
        self._last_color = "#0969da"
        self._build_ui()

    @property
    def editor(self) -> MarkdownEditor:
        return self._editor

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        header = QFrame()
        header.setObjectName("panelHeader")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(12, 8, 12, 8)

        title = QLabel("Editor")
        title.setObjectName("panelTitle")
        header_layout.addWidget(title)
        header_layout.addStretch()

        format_bar = QFrame()
        format_bar.setObjectName("formatBar")
        format_layout = QHBoxLayout(format_bar)
        format_layout.setContentsMargins(6, 4, 6, 4)
        format_layout.setSpacing(4)

        self._btn_bold = self._make_format_button("B", "Bold (Ctrl+B)")
        self._btn_bold.setObjectName("formatBold")
        self._btn_italic = self._make_format_button("I", "Italic (Ctrl+I)")
        self._btn_italic.setObjectName("formatItalic")
        self._btn_underline = self._make_format_button("U", "Underline (Ctrl+U)")
        self._btn_underline.setObjectName("formatUnderline")
        self._btn_color = self._make_format_button("A", "Text color")
        self._btn_color.setObjectName("formatColor")
        self._update_color_button(self._last_color)

        format_layout.addWidget(self._btn_bold)
        format_layout.addWidget(self._btn_italic)
        format_layout.addWidget(self._btn_underline)

        separator = QFrame()
        separator.setObjectName("formatSeparator")
        separator.setFixedWidth(1)
        separator.setFixedHeight(20)
        format_layout.addWidget(separator)

        format_layout.addWidget(self._btn_color)

        header_layout.addWidget(format_bar)

        editor_frame = QFrame()
        editor_frame.setObjectName("editorFrame")
        editor_layout = QVBoxLayout(editor_frame)
        editor_layout.setContentsMargins(0, 0, 0, 0)
        editor_layout.addWidget(self._editor)

        root.addWidget(header)
        root.addWidget(editor_frame, 1)

        self._btn_bold.clicked.connect(lambda: self._editor.apply_format(BOLD))
        self._btn_italic.clicked.connect(lambda: self._editor.apply_format(ITALIC))
        self._btn_underline.clicked.connect(lambda: self._editor.apply_format(UNDERLINE))
        self._btn_color.clicked.connect(self._pick_color)

        self._action_bold = QAction(self)
        self._action_bold.setShortcut(QKeySequence.StandardKey.Bold)
        self._action_bold.triggered.connect(lambda: self._editor.apply_format(BOLD))
        self.addAction(self._action_bold)

        self._action_italic = QAction(self)
        self._action_italic.setShortcut(QKeySequence.StandardKey.Italic)
        self._action_italic.triggered.connect(lambda: self._editor.apply_format(ITALIC))
        self.addAction(self._action_italic)

        self._action_underline = QAction(self)
        self._action_underline.setShortcut(QKeySequence("Ctrl+U"))
        self._action_underline.triggered.connect(lambda: self._editor.apply_format(UNDERLINE))
        self.addAction(self._action_underline)

    def _make_format_button(self, label: str, tooltip: str) -> QToolButton:
        button = QToolButton()
        button.setText(label)
        button.setToolTip(tooltip)
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.setAutoRaise(True)
        return button

    def _update_color_button(self, hex_color: str) -> None:
        self._btn_color.setToolTip(f"Text color ({hex_color})")
        self._btn_color.setStyleSheet(
            f"color: {hex_color}; font-weight: 700; text-decoration: underline;"
        )

    def _pick_color(self) -> None:
        color = QColorDialog.getColor(QColor(self._last_color), self, "Choose text color")
        if not color.isValid():
            return
        hex_color = color.name()
        self._last_color = hex_color
        self._update_color_button(hex_color)
        self._editor.apply_format(color_format(hex_color), placeholder="colored text")
