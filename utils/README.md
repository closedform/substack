# doc2substack

Convert LaTeX documents to Substack-friendly HTML.

## Features

- **Supports LaTeX and Markdown**: Accepts `.tex` or `.md` files as input
- **Unicode inline math**: Simple expressions like `$\alpha$`, `$w^i$`, `$g_{ij}$` are converted to Unicode (α, wⁱ, gᵢⱼ) for natural text flow
- **High-DPI equation images**: Complex display math (`$$...$$`) renders as sharp images via CodeCogs
- **Automatic cleanup**: Removes pandoc artifacts, fixes environments, cleans formatting

## Requirements

- Python 3.11+
- [pandoc](https://pandoc.org/) installed and on PATH

## Usage

```bash
# LaTeX input
uv run doc2substack.py article.tex

# Markdown input
uv run doc2substack.py article.md

# Custom output file
uv run doc2substack.py article.tex --output article_substack.html

# Higher DPI for sharper equations
uv run doc2substack.py article.tex --dpi 300

# With custom title
uv run doc2substack.py article.tex --title "My Article Title"
```

## How It Works

1. **LaTeX to Markdown**: Uses pandoc to extract content
2. **Cleanup**: Removes custom block environments, fixes equation wrappers
3. **Unicode conversion**: Converts simple inline math to Unicode characters
4. **HTML generation**: Uses pandoc with webtex for display equations

## Workflow

For your Substack article:
1. Write in LaTeX
2. Run `uv run doc2substack.py article.tex`
3. Open the HTML in a browser
4. Select all (Cmd+A) and copy (Cmd+C)
5. Paste into Substack editor
