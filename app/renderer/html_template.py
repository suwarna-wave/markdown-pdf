"""Wrap rendered Markdown HTML in a full document with styles."""

from pathlib import Path

_CSS_PATH = Path(__file__).resolve().parent.parent / "assets" / "styles" / "preview.css"
_css_cache: str | None = None

_EMPTY_PREVIEW = (
    '<p class="empty-preview">Start writing Markdown to see a live preview.</p>'
)


def _load_css() -> str:
    global _css_cache
    if _css_cache is None:
        _css_cache = _CSS_PATH.read_text(encoding="utf-8")
    return _css_cache


def build_html_document(body_html: str) -> str:
    """Return a complete HTML document for preview and PDF export."""
    content = body_html.strip() if body_html else ""
    if not content:
        content = _EMPTY_PREVIEW

    css = _load_css()
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Preview</title>
  <style>
{css}
  </style>
</head>
<body>
  <article class="markdown-body">
{content}
  </article>
</body>
</html>
"""
