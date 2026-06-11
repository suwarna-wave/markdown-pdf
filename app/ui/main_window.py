"""Main application window."""

from pathlib import Path

from PySide6.QtCore import Qt, QTimer, QUrl
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWebEngineCore import QWebEngineSettings
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (
    QFileDialog,
    QLabel,
    QMainWindow,
    QMessageBox,
    QSplitter,
    QStatusBar,
    QToolBar,
)

from app.pdf.pdf_exporter import export_to_pdf
from app.renderer.html_template import build_html_document
from app.renderer.markdown_renderer import render_markdown
from app.ui.editor_panel import EditorPanel
from app.ui.preview_panel import PreviewPanel

DEFAULT_MARKDOWN = """# Welcome to Markdown PDF Studio

This is a simple Markdown editor with live preview and PDF export.

## Features

- Write Markdown
- Preview live
- Save files
- Export to PDF
- **Bold**, *italic*, <u>underline</u>, and <span style="color: #0969da">colored text</span>

## Example Code

```python
print("Hello Markdown PDF Studio")
```

## Example Table

| Feature      | Status      |
| ------------ | ----------- |
| Live Preview | Working     |
| PDF Export   | Ready       |

> Start writing your Markdown on the left side.
"""

PREVIEW_DEBOUNCE_MS = 300
_STYLESHEET_PATH = Path(__file__).resolve().parent.parent / "assets" / "styles" / "app.qss"


class MainWindow(QMainWindow):
    """Primary window with editor, preview, and file actions."""

    def __init__(self) -> None:
        super().__init__()
        self._current_file: Path | None = None
        self._dirty = False
        self._live_preview_enabled = True
        self._last_dialog_dir = str(Path.home())
        self._preview_timer = QTimer(self)
        self._preview_timer.setSingleShot(True)
        self._preview_timer.timeout.connect(self._refresh_preview)

        self._editor_panel = EditorPanel()
        self._editor = self._editor_panel.editor

        self._preview = QWebEngineView()
        preview_settings = self._preview.settings()
        preview_settings.setAttribute(
            QWebEngineSettings.WebAttribute.JavascriptEnabled, False
        )
        preview_settings.setAttribute(
            QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls, True
        )
        self._preview_panel = PreviewPanel(self._preview)

        self._apply_stylesheet()
        self._build_ui()
        self._connect_signals()
        self._editor.set_text_silent(DEFAULT_MARKDOWN)
        self._update_window_title()
        self._update_word_count()
        self._refresh_preview()

    def _apply_stylesheet(self) -> None:
        if _STYLESHEET_PATH.exists():
            self.setStyleSheet(_STYLESHEET_PATH.read_text(encoding="utf-8"))

    def _build_ui(self) -> None:
        self.setWindowTitle("Markdown PDF Studio")
        self.resize(1280, 820)

        toolbar = QToolBar("Main", self)
        toolbar.setMovable(False)
        toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextOnly)
        self.addToolBar(toolbar)

        self._action_new = QAction("New", self)
        self._action_new.setShortcut(QKeySequence.StandardKey.New)
        self._action_new.setStatusTip("Create a new document")
        toolbar.addAction(self._action_new)

        self._action_open = QAction("Open", self)
        self._action_open.setShortcut(QKeySequence.StandardKey.Open)
        self._action_open.setStatusTip("Open a Markdown file")
        toolbar.addAction(self._action_open)

        self._action_save = QAction("Save", self)
        self._action_save.setShortcut(QKeySequence.StandardKey.Save)
        self._action_save.setStatusTip("Save the current document")
        toolbar.addAction(self._action_save)

        self._action_save_as = QAction("Save As", self)
        self._action_save_as.setShortcut(QKeySequence("Ctrl+Shift+S"))
        self._action_save_as.setStatusTip("Save the document to a new file")
        toolbar.addAction(self._action_save_as)

        toolbar.addSeparator()

        self._action_export_pdf = QAction("Export PDF", self)
        self._action_export_pdf.setShortcut(QKeySequence("Ctrl+P"))
        self._action_export_pdf.setStatusTip("Export the preview as a PDF")
        toolbar.addAction(self._action_export_pdf)

        self._action_refresh = QAction("Refresh", self)
        self._action_refresh.setShortcut(QKeySequence("Ctrl+R"))
        self._action_refresh.setStatusTip("Refresh the preview panel")
        toolbar.addAction(self._action_refresh)

        self._action_toggle_preview = QAction("Live Preview", self)
        self._action_toggle_preview.setCheckable(True)
        self._action_toggle_preview.setChecked(True)
        self._action_toggle_preview.setStatusTip("Enable or disable live preview updates")
        toolbar.addAction(self._action_toggle_preview)

        splitter = QSplitter(self)
        splitter.addWidget(self._editor_panel)
        splitter.addWidget(self._preview_panel)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 1)
        splitter.setSizes([620, 660])
        self.setCentralWidget(splitter)

        status = QStatusBar(self)
        self._status_file = QLabel("Untitled")
        self._status_save = QLabel("Saved")
        self._status_words = QLabel("0 words")
        status.addWidget(self._status_file, 1)
        status.addPermanentWidget(self._status_save)
        status.addPermanentWidget(self._status_words)
        self.setStatusBar(status)

    def _connect_signals(self) -> None:
        self._action_new.triggered.connect(self._new_file)
        self._action_open.triggered.connect(self._open_file)
        self._action_save.triggered.connect(self._save_file)
        self._action_save_as.triggered.connect(self._save_file_as)
        self._action_export_pdf.triggered.connect(self._export_pdf)
        self._action_refresh.triggered.connect(self._refresh_preview)
        self._action_toggle_preview.toggled.connect(self._toggle_live_preview)
        self._editor.textChanged.connect(self._on_editor_changed)

    def _dialog_start_dir(self) -> str:
        if self._current_file:
            return str(self._current_file.parent)
        return self._last_dialog_dir

    def _remember_dialog_dir(self, file_path: str) -> None:
        self._last_dialog_dir = str(Path(file_path).parent)

    def _preview_base_url(self) -> QUrl:
        if self._current_file:
            return QUrl.fromLocalFile(str(self._current_file.parent.resolve()) + "/")
        return QUrl("about:blank")

    def _build_preview_html(self) -> str:
        body_html = render_markdown(self._editor.get_text())
        return build_html_document(body_html)

    def _on_editor_changed(self) -> None:
        if not self._dirty:
            self._dirty = True
            self._update_window_title()
            self._status_save.setText("Unsaved")

        self._update_word_count()

        if self._live_preview_enabled:
            self._preview_timer.start(PREVIEW_DEBOUNCE_MS)

    def _update_word_count(self) -> None:
        text = self._editor.get_text().strip()
        count = 0 if not text else len(text.split())
        self._status_words.setText(f"{count} word{'s' if count != 1 else ''}")

    def _toggle_live_preview(self, enabled: bool) -> None:
        self._live_preview_enabled = enabled
        if enabled:
            self._refresh_preview()

    def _refresh_preview(self) -> None:
        html = self._build_preview_html()
        self._preview.setHtml(html, self._preview_base_url())

    def _load_preview_then(self, callback) -> None:
        """Render preview HTML and run callback after the page has loaded."""

        def on_load_finished(ok: bool) -> None:
            self._preview.loadFinished.disconnect(on_load_finished)
            callback(ok)

        self._preview.loadFinished.connect(on_load_finished)
        html = self._build_preview_html()
        self._preview.setHtml(html, self._preview_base_url())

    def _update_window_title(self) -> None:
        name = self._current_file.name if self._current_file else "Untitled"
        dirty_marker = " *" if self._dirty else ""
        self.setWindowTitle(f"{name}{dirty_marker} — Markdown PDF Studio")
        self._status_file.setText(name)

    def _mark_saved(self) -> None:
        self._dirty = False
        self._status_save.setText("Saved")
        self._update_window_title()

    def _confirm_unsaved_changes(self) -> bool:
        """Return True if the user wants to proceed, False to cancel."""
        if not self._dirty:
            return True

        dialog = QMessageBox(self)
        dialog.setIcon(QMessageBox.Icon.Warning)
        dialog.setWindowTitle("Unsaved Changes")
        dialog.setText("The document has unsaved changes.")
        dialog.setInformativeText("Do you want to save your changes before continuing?")

        save_button = dialog.addButton("Save", QMessageBox.ButtonRole.AcceptRole)
        discard_button = dialog.addButton("Discard", QMessageBox.ButtonRole.DestructiveRole)
        cancel_button = dialog.addButton("Cancel", QMessageBox.ButtonRole.RejectRole)
        dialog.setDefaultButton(save_button)

        dialog.exec()
        clicked = dialog.clickedButton()

        if clicked == cancel_button:
            return False
        if clicked == discard_button:
            return True
        if clicked == save_button:
            if self._current_file is None:
                self._save_file_as()
            else:
                self._write_file(self._current_file)
            return not self._dirty

        return False

    def _new_file(self) -> None:
        if not self._confirm_unsaved_changes():
            return
        self._current_file = None
        self._editor.set_text_silent("")
        self._mark_saved()
        self._update_word_count()
        self._refresh_preview()

    def _open_file(self) -> None:
        if not self._confirm_unsaved_changes():
            return
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Markdown File",
            self._dialog_start_dir(),
            "Markdown Files (*.md *.markdown);;All Files (*)",
        )
        if not file_path:
            return
        self._remember_dialog_dir(file_path)
        self._load_file(Path(file_path))

    def _load_file(self, file_path: Path) -> None:
        try:
            content = file_path.read_text(encoding="utf-8")
        except OSError as exc:
            QMessageBox.critical(self, "Open Failed", f"Could not open file:\n{exc}")
            return
        self._current_file = file_path
        self._editor.set_text_silent(content)
        self._mark_saved()
        self._update_word_count()
        self._refresh_preview()

    def _save_file(self) -> bool:
        if self._current_file is None:
            return self._save_file_as()
        return self._write_file(self._current_file)

    def _save_file_as(self) -> bool:
        start_name = "document.md"
        if self._current_file:
            start_name = self._current_file.name

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Markdown File",
            str(Path(self._dialog_start_dir()) / start_name),
            "Markdown Files (*.md);;All Files (*)",
        )
        if not file_path:
            return False

        path = Path(file_path)
        if path.suffix.lower() not in {".md", ".markdown"}:
            path = path.with_suffix(".md")

        self._remember_dialog_dir(str(path))
        return self._write_file(path)

    def _write_file(self, file_path: Path) -> bool:
        try:
            file_path.write_text(self._editor.get_text(), encoding="utf-8")
        except OSError as exc:
            QMessageBox.critical(self, "Save Failed", f"Could not save file:\n{exc}")
            return False
        self._current_file = file_path
        self._mark_saved()
        return True

    def _export_pdf(self) -> None:
        default_name = "document.pdf"
        if self._current_file:
            default_name = f"{self._current_file.stem}.pdf"

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export PDF",
            str(Path(self._dialog_start_dir()) / default_name),
            "PDF Files (*.pdf);;All Files (*)",
        )
        if not file_path:
            return
        if not file_path.lower().endswith(".pdf"):
            file_path += ".pdf"

        self._remember_dialog_dir(file_path)
        self._action_export_pdf.setEnabled(False)
        self.statusBar().showMessage("Preparing PDF export…")

        def on_success(saved_path: str) -> None:
            self._action_export_pdf.setEnabled(True)
            self.statusBar().showMessage(f"PDF exported to {saved_path}", 5000)
            QMessageBox.information(
                self,
                "Export Successful",
                f"PDF exported successfully:\n{saved_path}",
            )

        def on_error(message: str) -> None:
            self._action_export_pdf.setEnabled(True)
            self.statusBar().showMessage("PDF export failed", 5000)
            QMessageBox.critical(self, "Export Failed", message)

        def start_export(load_ok: bool) -> None:
            if not load_ok:
                self._action_export_pdf.setEnabled(True)
                self.statusBar().showMessage("PDF export failed", 5000)
                QMessageBox.critical(
                    self,
                    "Export Failed",
                    "Could not render the preview before exporting.",
                )
                return
            export_to_pdf(
                self._preview,
                file_path,
                on_success=on_success,
                on_error=on_error,
            )

        self._load_preview_then(start_export)

    def closeEvent(self, event) -> None:  # noqa: N802
        if self._confirm_unsaved_changes():
            event.accept()
        else:
            event.ignore()
