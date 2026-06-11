"""Sanitize rendered HTML while preserving Markdown structure."""

import re
from html import escape
from html.parser import HTMLParser

_COLOR_STYLE = re.compile(r"^color:\s*#[0-9a-fA-F]{3,8}$")

_ALLOWED_TAGS = frozenset({
    "a", "article", "b", "blockquote", "br", "code", "del", "div", "dl", "dt", "dd",
    "em", "footer", "h1", "h2", "h3", "h4", "h5", "h6", "hr", "i", "img", "input",
    "label", "li", "ol", "p", "pre", "section", "span", "strong", "sub", "sup",
    "table", "tbody", "td", "th", "thead", "tr", "u", "ul",
})

_DROP_TAGS = frozenset({"script", "style", "iframe", "object", "embed", "link", "meta"})

_ALLOWED_ATTRS: dict[str, frozenset[str]] = {
    "a": frozenset({"href", "title"}),
    "code": frozenset({"class"}),
    "div": frozenset({"class"}),
    "img": frozenset({"src", "alt", "title"}),
    "input": frozenset({"type", "checked", "disabled"}),
    "li": frozenset({"class"}),
    "pre": frozenset({"class"}),
    "span": frozenset({"class", "style"}),
    "td": frozenset({"align"}),
    "th": frozenset({"align"}),
    "ul": frozenset({"class"}),
}


def _is_safe_href(value: str) -> bool:
    lowered = value.strip().lower()
    return not lowered.startswith(("javascript:", "data:", "vbscript:"))


def _filter_attrs(tag: str, attrs: list[tuple[str, str | None]]) -> list[tuple[str, str]]:
    allowed = _ALLOWED_ATTRS.get(tag, frozenset())
    filtered: list[tuple[str, str]] = []
    for name, value in attrs:
        if value is None:
            continue
        attr = name.lower()
        if attr not in allowed:
            continue
        if attr == "href" and not _is_safe_href(value):
            continue
        if attr == "style" and not _COLOR_STYLE.match(value.strip()):
            continue
        if attr.startswith("on"):
            continue
        filtered.append((attr, value))
    return filtered


class _RenderSanitizer(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)
        self._parts: list[str] = []
        self._drop_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        if tag in _DROP_TAGS:
            self._drop_depth += 1
            return
        if self._drop_depth:
            return
        if tag not in _ALLOWED_TAGS:
            return
        safe_attrs = _filter_attrs(tag, attrs)
        if tag == "span" and any(name == "style" for name, _ in attrs if name) and not any(
            name == "style" for name, _ in safe_attrs
        ):
            return
        if safe_attrs:
            attrs_text = "".join(f' {name}="{escape(value, quote=True)}"' for name, value in safe_attrs)
            self._parts.append(f"<{tag}{attrs_text}>")
        else:
            self._parts.append(f"<{tag}>")

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in _DROP_TAGS:
            if self._drop_depth:
                self._drop_depth -= 1
            return
        if self._drop_depth:
            return
        if tag in _ALLOWED_TAGS:
            self._parts.append(f"</{tag}>")

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        if self._drop_depth or tag in _DROP_TAGS or tag not in _ALLOWED_TAGS:
            return
        safe_attrs = _filter_attrs(tag, attrs)
        if safe_attrs:
            attrs_text = "".join(f' {name}="{escape(value, quote=True)}"' for name, value in safe_attrs)
            self._parts.append(f"<{tag}{attrs_text} />")
        else:
            self._parts.append(f"<{tag} />")

    def handle_data(self, data: str) -> None:
        if self._drop_depth:
            return
        self._parts.append(data)

    def handle_entityref(self, name: str) -> None:
        if not self._drop_depth:
            self._parts.append(f"&{name};")

    def handle_charref(self, name: str) -> None:
        if not self._drop_depth:
            self._parts.append(f"&#{name};")

    def get_html(self) -> str:
        return "".join(self._parts)


def sanitize_rendered_html(html: str) -> str:
    """Remove unsafe tags and attributes from rendered Markdown HTML."""
    parser = _RenderSanitizer()
    parser.feed(html)
    parser.close()
    return parser.get_html()
