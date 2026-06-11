"""Tests for editor formatting helpers."""

from app.editor.formatting import BOLD, ITALIC, UNDERLINE, color_format, toggle_wrap


def test_toggle_wrap_adds_formatting() -> None:
    assert toggle_wrap("hello", BOLD) == "**hello**"


def test_toggle_wrap_removes_formatting() -> None:
    assert toggle_wrap("**hello**", BOLD) == "hello"


def test_color_format_uses_hex_color() -> None:
    fmt = color_format("#ff0000")
    assert fmt.before == '<span style="color: #ff0000">'
    assert fmt.after == "</span>"


def test_underline_format() -> None:
    assert toggle_wrap("text", UNDERLINE) == "<u>text</u>"


def test_italic_format() -> None:
    assert toggle_wrap("text", ITALIC) == "*text*"
