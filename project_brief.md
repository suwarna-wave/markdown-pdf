# PROJECT BRIEF: Markdown PDF Studio

## 1. Project Name

**Markdown PDF Studio**

## 2. What I Want to Build

I want to build a simple desktop platform where users can write or open Markdown files, preview them live, and export the final rendered version as a PDF.

The main problem I want to solve is this:

Many people edit Markdown files, but they cannot easily see how the final document will look. I want a simple tool where the user can edit Markdown on the left side, see the rendered preview on the right side, and download/export the final result as a PDF.

This should feel like a clean Markdown writing and PDF export studio.

---

## 3. Core Goal

Build a Python desktop application that allows users to:

1. Create a new Markdown file.
2. Open an existing `.md` file.
3. Edit Markdown text.
4. See live rendered preview while typing.
5. Save the Markdown file.
6. Use Save As for a new file.
7. Export the rendered Markdown preview as a PDF.
8. See a clean professional PDF output.

---

## 4. Preferred Tech Stack

Use Python for the MVP.

Use this stack:

* Python 3.10+
* PySide6 for the desktop GUI
* PySide6 QtWebEngineWidgets / QWebEngineView for the preview area
* markdown-it-py for converting Markdown to HTML
* mdit-py-plugins if needed
* Pygments for code block highlighting if needed
* QTimer for debounced live preview
* QFileDialog for file open/save/export
* QWebEngineView.printToPdf() for PDF export

Do not use Django, Flask, FastAPI, React, or any web framework for the MVP.

This should first be a desktop app.

---

## 5. Main UI Design

The app should have one main window.

The layout should be:

```txt
 ---------------------------------------------------------
| Toolbar: New | Open | Save | Save As | Export PDF       |
 ---------------------------------------------------------
| Markdown Editor              | Rendered Preview         |
| Left Side                    | Right Side               |
|                              |                          |
 ---------------------------------------------------------
| Status Bar: file status, saved/unsaved, word count      |
 ---------------------------------------------------------
```

Use a horizontal splitter so the user can resize the editor and preview sections.

---

## 6. Toolbar Features

The toolbar should have:

* New
* Open
* Save
* Save As
* Export PDF
* Refresh Preview
* Toggle Live Preview if easy

---

## 7. Keyboard Shortcuts

Add these shortcuts:

* `Ctrl+N` = New file
* `Ctrl+O` = Open Markdown file
* `Ctrl+S` = Save
* `Ctrl+Shift+S` = Save As
* `Ctrl+P` = Export PDF
* `Ctrl+R` = Refresh Preview

---

## 8. Live Preview Behavior

When the user types Markdown:

1. Wait around 300ms using a debounce timer.
2. Convert Markdown to HTML.
3. Wrap the HTML inside a full HTML template.
4. Apply CSS styling.
5. Show the rendered output in QWebEngineView.

Do not refresh instantly on every keystroke without delay because that may become slow for large files.

---

## 9. Markdown Features Required

The Markdown renderer should support:

* Headings
* Paragraphs
* Bold text
* Italic text
* Ordered lists
* Unordered lists
* Blockquotes
* Inline code
* Code blocks
* Tables
* Links
* Images
* Horizontal rules
* Task lists if easy
* Footnotes if easy

The preview should look clean and professional, similar to a GitHub-style Markdown document.

---

## 10. PDF Export Behavior

When the user clicks **Export PDF**:

1. Ask the user where to save the PDF.
2. Render the latest Markdown content.
3. Load it into the preview if needed.
4. Export the preview to PDF using `QWebEngineView.printToPdf()`.
5. Show a success message after export.
6. Show an error message if export fails.

The exported PDF should match the preview as closely as possible.

Use clean A4 print styling.

---

## 11. PDF Styling Requirements

The exported PDF should have:

* A4 page size
* Clean margins
* Professional typography
* Proper heading spacing
* Readable paragraphs
* Styled code blocks
* Styled tables
* Proper image scaling
* White background
* Print-friendly CSS

---

## 12. Security Rules

Markdown may contain raw HTML.

For the MVP:

* Do not execute JavaScript from Markdown.
* Avoid unsafe raw HTML rendering.
* Do not inject arbitrary scripts.
* Local images can be allowed.
* Remote images can be ignored or left optional.

---

## 13. Suggested Project Structure

Create this structure:

```txt
markdown-pdf-studio/
├── PROJECT_BRIEF.md
├── README.md
├── requirements.txt
├── main.py
├── app/
│   ├── __init__.py
│   ├── ui/
│   │   ├── __init__.py
│   │   └── main_window.py
│   ├── editor/
│   │   ├── __init__.py
│   │   └── markdown_editor.py
│   ├── renderer/
│   │   ├── __init__.py
│   │   ├── markdown_renderer.py
│   │   └── html_template.py
│   ├── pdf/
│   │   ├── __init__.py
│   │   └── pdf_exporter.py
│   └── assets/
│       └── styles/
│           └── preview.css
└── tests/
    └── test_markdown_renderer.py
```

---

## 14. File Responsibilities

### main.py

Responsible for:

* Starting the QApplication
* Creating the main window
* Running the app loop

### app/ui/main_window.py

Responsible for:

* Main app window
* Toolbar
* Splitter layout
* File actions
* Save/open/export logic
* Window title updates
* Dirty state tracking
* Connecting editor changes to preview updates

### app/editor/markdown_editor.py

Responsible for:

* Markdown text editor widget
* Should use QPlainTextEdit
* Should provide simple methods like:

  * `get_text()`
  * `set_text(text)`

### app/renderer/markdown_renderer.py

Responsible for:

* Converting Markdown to HTML
* Using markdown-it-py
* Supporting tables and common Markdown features
* Passing HTML body to the HTML template

### app/renderer/html_template.py

Responsible for:

* Wrapping rendered Markdown body into a full HTML document
* Loading CSS from `preview.css`
* Returning final HTML string

### app/pdf/pdf_exporter.py

Responsible for:

* Exporting preview to PDF
* Using QWebEngineView.printToPdf()
* Handling success and failure callbacks if possible

### app/assets/styles/preview.css

Responsible for:

* Preview styling
* Print styling
* Markdown document styling
* Tables
* Code blocks
* Blockquotes
* Headings
* Images

---

## 15. MVP Features

Build these features first:

1. App opens with `python main.py`.
2. Main window appears.
3. Left side has Markdown editor.
4. Right side has rendered preview.
5. Default sample Markdown appears on startup.
6. Live preview works.
7. Open `.md` file works.
8. Save file works.
9. Save As works.
10. Export PDF works.
11. PDF looks like the preview.
12. Empty Markdown does not crash the app.

Do not build advanced features before MVP is working.

---

## 16. Future Features

Only after MVP is stable, we may add:

* Markdown syntax highlighting
* Line numbers
* Multiple tabs
* Recent files
* Drag and drop file opening
* Dark mode
* Theme selector
* Export to HTML
* Export to DOCX
* Table of contents
* Mermaid diagram support
* LaTeX math support
* Document templates
* Installer for Windows/Linux/macOS
* Web app version

Do not implement these future features now.

---

## 17. Development Phases

### Phase 1: Basic App and Live Preview

Build:

* Project structure
* requirements.txt
* main.py
* MainWindow
* Markdown editor
* Preview panel
* Markdown renderer
* HTML template
* CSS file
* Default sample Markdown
* Live preview with debounce

### Phase 2: File Handling

Add:

* New file
* Open `.md`
* Save
* Save As
* Dirty state
* Unsaved changes indicator
* Window title update

### Phase 3: PDF Export

Add:

* Export PDF button
* Save PDF dialog
* Export current rendered preview as PDF
* Success/error message

### Phase 4: Styling Improvement

Improve:

* Preview CSS
* Print CSS
* Tables
* Code blocks
* Images
* Blockquotes
* Headings
* A4 page layout

### Phase 5: Tests

Add:

* Basic tests for Markdown rendering
* Empty Markdown test
* Heading rendering test
* Table rendering test
* Code block rendering test

---

## 18. Coding Rules

Follow these rules:

* Keep the code modular.
* Do not put everything inside `main.py`.
* Separate UI, rendering, editor, and PDF logic.
* Use readable and beginner-friendly code.
* Use clear class and function names.
* Handle errors with message boxes.
* Avoid over-engineering.
* Do not add login, database, cloud, or AI features.
* The app must run with:

```bash
python main.py
```

---

## 19. Dependencies

Create `requirements.txt` with suitable packages like:

```txt
PySide6
PySide6-QtWebEngine
markdown-it-py
mdit-py-plugins
Pygments
pytest
```

If some package names are incorrect or unnecessary, fix them while implementing.

---

## 20. Default Sample Markdown

Use this sample text when the app opens:

````md
# Welcome to Markdown PDF Studio

This is a simple Markdown editor with live preview and PDF export.

## Features

- Write Markdown
- Preview live
- Save files
- Export to PDF

## Example Code

```python
print("Hello Markdown PDF Studio")
````

## Example Table

| Feature      | Status      |
| ------------ | ----------- |
| Live Preview | Working     |
| PDF Export   | Coming Soon |

> Start writing your Markdown on the left side.

````

---

## 21. Acceptance Criteria

The project is successful when:

- I can run `python main.py`.
- A desktop window opens.
- I can write Markdown on the left.
- I can see rendered preview on the right.
- Preview updates live while typing.
- I can open an existing Markdown file.
- I can save the Markdown file.
- I can export the preview as a PDF.
- The PDF looks clean and professional.
- The code is easy to understand and extend.

---

## 22. Cursor Instructions

Cursor, read this file carefully and build the project phase by phase.

Start with **Phase 1 only**.

Do not implement everything at once.

After finishing each phase, explain:

1. What files were created or changed.
2. How to run the app.
3. What was completed.
4. What I should test manually.
5. What phase should come next.

Start now with Phase 1.

---

## 23. First Task for Cursor

Build Phase 1:

- Create the project structure.
- Create `requirements.txt`.
- Create `main.py`.
- Create `app/ui/main_window.py`.
- Create `app/editor/markdown_editor.py`.
- Create `app/renderer/markdown_renderer.py`.
- Create `app/renderer/html_template.py`.
- Create `app/assets/styles/preview.css`.
- Create a working desktop window.
- Add Markdown editor on the left.
- Add live preview on the right.
- Add default sample Markdown.
- Use debounce for live preview.
- Make the app runnable with:

```bash
python main.py
````

Do not build PDF export yet.

