"""Tests for Markdown rendering."""

from app.renderer.html_template import build_html_document
from app.renderer.markdown_renderer import render_markdown


def test_empty_markdown_returns_empty_html() -> None:
    assert render_markdown("") == ""
    assert render_markdown("   ") == ""


def test_empty_document_shows_placeholder() -> None:
    document = build_html_document("")
    assert "empty-preview" in document
    assert "Start writing Markdown" in document


def test_heading_rendering() -> None:
    html = render_markdown("# Hello World")
    assert "<h1>Hello World</h1>" in html


def test_bold_and_italic_rendering() -> None:
    html = render_markdown("**bold** and *italic*")
    assert "<strong>bold</strong>" in html
    assert "<em>italic</em>" in html


def test_underline_and_color_rendering() -> None:
    html = render_markdown(
        '<u>underline</u> and <span style="color: #0969da">blue</span>'
    )
    assert "<u>underline</u>" in html
    assert '<span style="color: #0969da">blue</span>' in html


def test_blockquote_rendering() -> None:
    html = render_markdown("> A quote")
    assert "<blockquote>" in html
    assert "A quote" in html


def test_link_rendering() -> None:
    html = render_markdown("[Example](https://example.com)")
    assert '<a href="https://example.com"' in html
    assert "Example</a>" in html


def test_table_rendering() -> None:
    markdown = "| A | B |\n| - | - |\n| 1 | 2 |"
    html = render_markdown(markdown)
    assert "<table>" in html
    assert "<td>1</td>" in html
    assert "<td>2</td>" in html


def test_code_block_rendering() -> None:
    markdown = "```python\nprint('hi')\n```"
    html = render_markdown(markdown)
    assert '<pre class="highlight">' in html
    assert "<code" in html
    assert "language-python" in html


def test_code_block_has_syntax_highlighting() -> None:
    markdown = "```python\nprint('hi')\n```"
    html = render_markdown(markdown)
    assert '<span class="nb">print</span>' in html
    assert '<span class="s1">' in html


def test_task_list_rendering() -> None:
    markdown = "- [x] Done\n- [ ] Todo"
    html = render_markdown(markdown)
    assert "task-list" in html
    assert 'type="checkbox"' in html


def test_build_html_document_wraps_body() -> None:
    document = build_html_document("<p>Test</p>")
    assert "<!DOCTYPE html>" in document
    assert '<article class="markdown-body">' in document
    assert "<p>Test</p>" in document
    assert "markdown-body" in document
