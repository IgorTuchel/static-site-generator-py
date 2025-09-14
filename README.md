# Static Site Generator (Python)

A lightweight, configurable static site generator written in Python that converts Markdown files into HTML using customizable templates.

## Features

- **Markdown to HTML Conversion**: Converts Markdown files to HTML with full support for:

  - Headers (H1-H6)
  - Bold and italic text formatting
  - Code blocks and inline code
  - Links and images
  - Ordered and unordered lists
  - Blockquotes
  - Paragraphs

- **Template System**: Uses HTML templates with placeholder variables (`{{ Title }}` and `{{ Content }}`)

- **Static Asset Handling**: Automatically copies static files (CSS, images, etc.) from source to destination

- **Configuration Management**: INI-based configuration system for managing paths and settings

- **Recursive Processing**: Processes nested directory structures while maintaining folder hierarchy

- **CLI Interface**: Command-line interface with argparse for easy operation

## Project Structure

```
src/
├── main.py              # Entry point and CLI handling
├── config.py            # Configuration management system
├── copystatic.py        # Static file copying and page generation
├── htmlnode.py          # HTML node classes (HTMLNode, LeafNode, ParentNode)
├── textnode.py          # Text node representation and HTML conversion
├── inline.py            # Inline markdown parsing (bold, italic, links, images)
├── markdown_blocks.py   # Block-level markdown parsing
└── test_*.py           # Unit tests for various components
```

## Installation

1. Clone the repository:

```bash
git clone https://github.com/IgorTuchel/static-site-generator-py.git
cd static-site-generator-py
```

2. Ensure you have Python 3.12+ installed (as specified in `uv.lock`)

## Usage

### Initial Setup

Create a configuration file with default paths:

```bash
python src/main.py --create
```

This creates a `config.ini` file and default directory structure:

- `../bin/static/` - Static assets (CSS, images, etc.)
- `../bin/content/` - Markdown content files
- `../bin/public/` - Generated HTML output
- `../bin/template.html` - HTML template file

### Configuration

Update configuration paths as needed:

```bash
python src/main.py --static_path /path/to/static --public_path /path/to/output --content_path /path/to/content --template_path /path/to/template.html --update
```

### Generate Site

Run the static site generator:

```bash
python src/main.py --run
```

This will:

1. Copy all static assets to the public directory
2. Process all Markdown files in the content directory
3. Generate HTML files using the specified template
4. Maintain the directory structure in the output

## Template Format

The HTML template uses simple variable substitution:

```html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{{ Title }}</title>
    <link href="/index.css" rel="stylesheet" />
  </head>

  <body>
    <article>{{ Content }}</article>
  </body>
</html>
```

- `{{ Title }}` - Replaced with the first H1 header from the Markdown file
- `{{ Content }}` - Replaced with the converted HTML content
- `<link>` - Plan to add support for better css linkage

## Markdown Support

### Text Formatting

- **Bold text**: `**bold**` or `__bold__`
- _Italic text_: `*italic*` or `_italic_`
- `Inline code`: `` `code` ``

### Links and Images

- Links: `[link text](url)`
- Images: `![alt text](image-url)`

### Headers

```markdown
# Header 1

## Header 2

### Header 3

#### Header 4

##### Header 5

###### Header 6
```

### Lists

```markdown
- Unordered list item
- Another item

1. Ordered list item
2. Another numbered item
```

### Code Blocks

```
code block content
```

### Blockquotes

```markdown
> This is a blockquote
> Multiple lines supported
```

## Architecture

The generator uses a modular architecture:

1. **TextNode**: Represents different types of text content (plain, bold, italic, code, links, images)
2. **HTMLNode**: Base class for HTML representation
   - **LeafNode**: Self-closing or simple HTML tags
   - **ParentNode**: HTML tags with children
3. **Block Parsing**: Converts Markdown blocks to HTML nodes
4. **Inline Parsing**: Handles inline formatting within blocks

## Development

The project includes unit tests:

```bash
python src/test_htmlnode.py
python src/test_textnode.py
python src/test_inline_markdown.py
python src/test_markdown_blocks.py
```

## Requirements

- Python 3.12+
- Standard library modules only (no external dependencies)

## CLI Options

| Option            | Description                                          |
| ----------------- | ---------------------------------------------------- |
| `--create`        | Create initial configuration and directory structure |
| `--update`        | Update existing configuration                        |
| `--run`           | Generate the static site                             |
| `--static_path`   | Set path to static assets                            |
| `--public_path`   | Set output path for generated HTML                   |
| `--content_path`  | Set path to Markdown content                         |
| `--template_path` | Set path to HTML template                            |

## Made By

Igor Tuchel
ITuchel@pm.me
