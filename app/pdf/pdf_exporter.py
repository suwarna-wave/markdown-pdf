"""Export the preview panel to a PDF file."""

from collections.abc import Callable

from PySide6.QtCore import QMarginsF
from PySide6.QtGui import QPageLayout, QPageSize
from PySide6.QtWebEngineWidgets import QWebEngineView


def export_to_pdf(
    web_view: QWebEngineView,
    file_path: str,
    on_success: Callable[[str], None] | None = None,
    on_error: Callable[[str], None] | None = None,
) -> None:
    """Export the current QWebEngineView content to a PDF file.

    The caller must ensure the page has finished loading before calling this.
    """

    def handle_result(pdf_data) -> None:
        if pdf_data is None or (hasattr(pdf_data, "isEmpty") and pdf_data.isEmpty()):
            if on_error:
                on_error("PDF generation failed: no data returned.")
            return
        raw_bytes = pdf_data.data() if hasattr(pdf_data, "data") else pdf_data
        try:
            with open(file_path, "wb") as pdf_file:
                pdf_file.write(raw_bytes)
        except OSError as exc:
            if on_error:
                on_error(f"Could not save PDF: {exc}")
            return
        if on_success:
            on_success(file_path)

    page_layout = QPageLayout(
        QPageSize(QPageSize.PageSizeId.A4),
        QPageLayout.Orientation.Portrait,
        QMarginsF(20, 20, 20, 20),
        QPageLayout.Unit.Millimeter,
    )
    web_view.page().printToPdf(handle_result, page_layout)
