"""Tests for safe inline HTML sanitization."""

from app.renderer.html_sanitizer import sanitize_rendered_html


def test_allows_underline_and_color() -> None:
    html = '<p><u>hi</u> <span style="color: #ff0000">red</span></p>'
    cleaned = sanitize_rendered_html(html)
    assert "<u>hi</u>" in cleaned
    assert '<span style="color: #ff0000">red</span>' in cleaned


def test_strips_script_tags() -> None:
    html = '<script>alert("x")</script><u>safe</u>'
    cleaned = sanitize_rendered_html(html)
    assert "script" not in cleaned
    assert "<u>safe</u>" in cleaned


def test_rejects_unsafe_span_styles() -> None:
    html = '<span style="background: url(javascript:alert(1))">bad</span>'
    cleaned = sanitize_rendered_html(html)
    assert "<span" not in cleaned
    assert "bad" in cleaned
