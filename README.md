# Markdown PDF Studio

A simple desktop app for writing Markdown with live preview and PDF export.

## Features

- Split-pane editor with live rendered preview
- Open, save, and save-as for `.md` files
- Export preview to PDF (A4, print-friendly styling)
- GitHub-style Markdown rendering (tables, code blocks, task lists, footnotes)

## Requirements

- Python 3.10+
- Linux dependencies for Qt WebEngine (e.g. on Ubuntu: `libxcb-cursor0`)

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Ctrl+N | New file |
| Ctrl+O | Open file |
| Ctrl+S | Save |
| Ctrl+Shift+S | Save As |
| Ctrl+P | Export PDF |
| Ctrl+R | Refresh preview |

## Tests

```bash
pytest
```
