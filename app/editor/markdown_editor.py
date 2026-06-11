"""Markdown text editor widget."""

from PySide6.QtGui import QFont, QTextCursor
from PySide6.QtWidgets import QPlainTextEdit

from app.editor.formatting import TextFormat, toggle_wrap


class MarkdownEditor(QPlainTextEdit):
    """Plain-text editor for Markdown content."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        font = QFont("Monospace")
        font.setStyleHint(QFont.StyleHint.Monospace)
        font.setPointSize(11)
        self.setFont(font)
        self.setTabStopDistance(self.fontMetrics().horizontalAdvance(" ") * 4)
        self.setPlaceholderText("Write Markdown here…")

    def get_text(self) -> str:
        return self.toPlainText()

    def set_text(self, text: str) -> None:
        self.setPlainText(text)

    def set_text_silent(self, text: str) -> None:
        """Set editor text without emitting change signals."""
        self.blockSignals(True)
        self.setPlainText(text)
        self.blockSignals(False)

    def _selected_plain_text(self) -> str:
        cursor = self.textCursor()
        if not cursor.hasSelection():
            return ""
        return cursor.selectedText().replace("\u2029", "\n")

    def apply_format(self, fmt: TextFormat, placeholder: str = "text") -> None:
        """Wrap the current selection with a format, or insert a placeholder."""
        cursor = self.textCursor()
        if cursor.hasSelection():
            selected = self._selected_plain_text()
            cursor.insertText(toggle_wrap(selected, fmt))
        else:
            wrapped = f"{fmt.before}{placeholder}{fmt.after}"
            cursor.insertText(wrapped)
            start = cursor.position() - len(fmt.after) - len(placeholder)
            cursor.setPosition(start)
            cursor.setPosition(start + len(placeholder), QTextCursor.MoveMode.KeepAnchor)
            self.setTextCursor(cursor)
        self.setFocus()
