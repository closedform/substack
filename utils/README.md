# doc2substack

Convert LaTeX documents to Substack-friendly HTML.

## Workflow

For your Substack article:
1. Write in LaTeX
2. Run `uv run doc2substack.py article.tex`
3. Open the HTML in a browser
4. Select all (Cmd+A) and copy (Cmd+C)
5. Paste into Substack editor
6. **Check equation placement**: Scroll through to ensure display equations (`$$...$$`) are centered properly; occasionally Substack's editor might misalign them initially.

## Features

- **Supports LaTeX and Markdown**: Accepts `.tex` or `.md` files as input
- **Unicode inline math**: Simple expressions like `$\alpha$`, `$w^i$`, `$g_{ij}$` are converted to Unicode (α, wⁱ, gᵢⱼ) for natural text flow
- **High-DPI equation images**: Complex display math (`$$...$$`) renders as sharp images via CodeCogs
- **Automatic cleanup**: Removes pandoc artifacts, fixes environments, cleans formatting

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

## Best Practices

**Keep inline math simple.**

The tool attempts to convert inline math (like `$\alpha$`) to Unicode characters. If an expression is too complex for Unicode (e.g., `$\frac{1}{2}$`, integrals, or nested structures), it will be rendered as an inline image or left as raw text, which often looks clunky on Substack.

*   **Good (Unicode-friendly):** `$\alpha$`, `$w^i$`, `$v_{ij}$`, `$\nabla f$`
*   **Bad for Inline:** `$\frac{\partial f}{\partial x}$`, `$\int_0^1 x dx$`

**Recommendation:** If an expression is complex, move it to a **display block** (`$$...$$` or `\begin{equation}...\end{equation}`). These are automatically rendered as beautiful, high-DPI images that center perfectly in your article.

## Requirements

- Python 3.11+
- [pandoc](https://pandoc.org/) installed and on PATH

## How It Works

1. **LaTeX to Markdown**: Uses pandoc to extract content
2. **Cleanup**: Removes custom block environments, fixes equation wrappers
3. **Unicode conversion**: Converts simple inline math to Unicode characters
4. **HTML generation**: Uses pandoc with webtex for display equations
