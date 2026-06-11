"""Convert Markdown source to HTML body content."""

from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import TextLexer, get_lexer_by_name, guess_lexer
from pygments.util import ClassNotFound

from markdown_it import MarkdownIt
from markdown_it.token import Token
from mdit_py_plugins.footnote import footnote_plugin
from mdit_py_plugins.gfm import gfm_plugin
from mdit_py_plugins.tasklists import tasklists_plugin

from app.renderer.html_sanitizer import sanitize_rendered_html

_HIGHLIGHT_FORMATTER = HtmlFormatter(nowrap=True, cssclass="highlight")


def _highlight_code(code: str, language: str) -> str:
    try:
        lexer = get_lexer_by_name(language, stripall=True) if language else guess_lexer(code)
    except ClassNotFound:
        lexer = TextLexer()
    return highlight(code, lexer, _HIGHLIGHT_FORMATTER)


def _render_fence(
    renderer: MarkdownIt,
    tokens: list[Token],
    index: int,
    options: dict,
    env: dict,
) -> str:
    token = tokens[index]
    info = token.info.strip().split()[0] if token.info else ""
    code = token.content.rstrip("\n")
    highlighted = _highlight_code(code, info)
    lang_class = f'language-{info}' if info else ""
    if lang_class:
        return f'<pre class="highlight"><code class="{lang_class}">{highlighted}</code></pre>\n'
    return f'<pre class="highlight"><code>{highlighted}</code></pre>\n'


def _create_markdown_parser() -> MarkdownIt:
    parser = (
        MarkdownIt("commonmark", {"html": True, "linkify": True})
        .use(gfm_plugin)
        .use(footnote_plugin)
        .use(tasklists_plugin)
    )
    parser.add_render_rule("fence", _render_fence)
    parser.add_render_rule("code_block", _render_fence)
    return parser


_parser = _create_markdown_parser()


def render_markdown(markdown_text: str) -> str:
    """Render Markdown to an HTML body fragment."""
    if not markdown_text or not markdown_text.strip():
        return ""
    return sanitize_rendered_html(_parser.render(markdown_text))
