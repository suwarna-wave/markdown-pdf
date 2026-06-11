"""Helpers for applying Markdown and safe HTML formatting to selections."""

from dataclasses import dataclass


@dataclass(frozen=True)
class TextFormat:
    """A text wrapper applied around a selection."""

    before: str
    after: str


BOLD = TextFormat("**", "**")
ITALIC = TextFormat("*", "*")
UNDERLINE = TextFormat("<u>", "</u>")


def color_format(hex_color: str) -> TextFormat:
    normalized = hex_color.lower()
    if not normalized.startswith("#"):
        normalized = f"#{normalized}"
    return TextFormat(f'<span style="color: {normalized}">', "</span>")


def toggle_wrap(text: str, fmt: TextFormat) -> str:
    """Wrap text or remove the wrapper if already present."""
    if text.startswith(fmt.before) and text.endswith(fmt.after):
        return text[len(fmt.before) : -len(fmt.after)]
    return f"{fmt.before}{text}{fmt.after}"
