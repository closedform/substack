# doc2substack

Convert LaTeX documents to Substack-friendly HTML.

## Workflow

For your Substack article:
1. Write in LaTeX, Markdown, or any Pandoc-supported format (`.docx`, `.ipynb`, etc.)
2. Run `uv run doc2substack.py article.tex` (or `.md`)
3. Open the HTML in a browser
4. Select all (Cmd+A) and copy (Cmd+C)
5. Paste into Substack editor
6. **Check equation placement**: Scroll through to ensure display equations (`$$...$$`) are centered properly; occasionally Substack's editor might misalign them initially.

## Features

- **Supports Broad Input**: Accepts `.tex`, `.md`, `.docx`, `.ipynb` and other Pandoc formats
- **Unicode inline math**: Simple expressions like `$\alpha$`, `$w^i$`, `$g_{ij}$` are converted to Unicode (α, wⁱ, gᵢⱼ) for natural text flow
- **High-DPI equation images**: Complex display math (`$$...$$`) renders as sharp images via CodeCogs
- **Automatic cleanup**: Removes pandoc artifacts, fixes environments, cleans formatting


## Installation & Usage

Found in `substack/utils`. You can run this utility with `uv` (recommended) or standard Python.

### Option 1: Using `uv` (Recommended)

```bash
# LaTeX input
uv run doc2substack.py article.tex

# Markdown input
uv run doc2substack.py article.md
```

### Option 2: Standard Python

Since the script only uses the standard library (no `pip install` needed), you can run it directly if you have Python 3 installed.

```bash
python doc2substack.py article.tex
```

## Examples

Check the `examples/doc2substack/` directory for sample files:
- `math_example.tex`: Standard LaTeX document with inline and display math.
- `test_notebook.ipynb`: Jupyter notebook with code and math cells.

To run an example:
```bash
python doc2substack.py examples/doc2substack/math_example.tex
```

## Feedback
If you find a bug or have a feature request, please open an issue.

### Options

```bash
# Custom output file
python doc2substack.py article.tex --output article_substack.html

# Higher DPI for sharper equations
python doc2substack.py article.tex --dpi 300
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
