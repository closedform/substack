#!/usr/bin/env python3
"""
doc2substack: Convert LaTeX or Markdown documents to Substack-friendly HTML.

Handles:
- Simple inline math: converted to Unicode for natural text flow
- Complex display math: converted to high-DPI images via CodeCogs
- Prose cleanup: removes raw LaTeX fragments, fixes subscripts/superscripts

Usage:
    uv run doc2substack.py input.tex [--output output.html] [--dpi 200]
"""
import argparse
import re
import subprocess
import tempfile
from pathlib import Path

from mappings import GREEK, SYMBOLS, SUPER, SUB

def is_complex_math(latex: str) -> bool:
    """Check if LaTeX expression is too complex for Unicode conversion."""
    complex_patterns = [
        r'\\frac\{',      # Fractions
        r'\\sqrt\{',      # Square roots with content
        r'\\begin\{',     # Environments
        r'\\sum_',        # Summation with limits
        r'\\int_',        # Integrals with limits
        r'\\langle',      # Angle brackets (bra-ket)
        r'\\underbrace',  # Underbraces
        r'\\overbrace',   # Overbraces
        r'\\matrix',      # Matrices
        r'\\pmatrix',     # Matrices
        r'\\bmatrix',     # Matrices
    ]
    for p in complex_patterns:
        if re.search(p, latex):
            return True
    return False


def latex_to_unicode(latex: str) -> str | None:
    """
    Convert simple LaTeX to Unicode.
    Returns None if the expression is too complex.
    """
    s = latex.strip()
    
    if is_complex_math(s):
        return None
    
    result = s
    
    # Replace Greek letters
    for name, uni in GREEK.items():
        result = re.sub(r'\\' + name + r'(?![a-zA-Z])', uni, result)
    
    # Replace symbols
    for tex, uni in SYMBOLS.items():
        result = result.replace(tex, uni)
    
    # Replace \mathbb{X} with special chars
    result = re.sub(r'\\mathbb\{E\}', '𝔼', result)
    result = re.sub(r'\\mathbb\{R\}', 'ℝ', result)
    result = re.sub(r'\\mathbb\{N\}', 'ℕ', result)
    result = re.sub(r'\\mathbb\{Z\}', 'ℤ', result)
    result = re.sub(r'\\mathbb\{C\}', 'ℂ', result)
    
    # Replace \mathcal{X} with script chars
    result = re.sub(r'\\mathcal\{([A-Z])\}', lambda m: chr(ord('𝒜') + ord(m.group(1)) - ord('A')), result)
    
    # Handle \text{...}
    result = re.sub(r'\\text\{([^}]+)\}', r'\1', result)
    result = re.sub(r'\\textit\{([^}]+)\}', r'\1', result)
    result = re.sub(r'\\textbf\{([^}]+)\}', r'\1', result)
    
    # Handle superscripts: ^{...} or ^x
    def super_replace(m):
        content = m.group(1) if m.group(1) else m.group(2)
        return ''.join(SUPER.get(c, c) for c in content)
    result = re.sub(r'\^\{([^}]+)\}', super_replace, result)
    result = re.sub(r'\^([a-zA-Z0-9αβγδθφ])', super_replace, result)
    
    # Handle subscripts: _{...} or _x
    def sub_replace(m):
        content = m.group(1) if m.group(1) else m.group(2)
        return ''.join(SUB.get(c, c) for c in content)
    result = re.sub(r'_\{([^}]+)\}', sub_replace, result)
    result = re.sub(r'_([a-zA-Z0-9])', sub_replace, result)
    
    # Handle hat: \hat{x} -> x̂
    result = re.sub(r'\\hat\{([a-zA-Z])\}', r'\1̂', result)
    result = re.sub(r'\\hat([a-zA-Z])', r'\1̂', result)
    
    # Handle bar: \bar{x} -> x̄
    result = re.sub(r'\\bar\{([a-zA-Z])\}', r'\1̄', result)
    result = re.sub(r'\\bar([a-zA-Z])', r'\1̄', result)
    
    # Handle tilde: \tilde{x} -> x̃
    result = re.sub(r'\\tilde\{([a-zA-Z])\}', r'\1̃', result)
    result = re.sub(r'\\tilde([a-zA-Z])', r'\1̃', result)
    
    # Handle \| for norm
    result = result.replace(r'\|', '‖')
    
    # Remove remaining braces
    result = result.replace('{', '').replace('}', '')
    
    # Remove remaining unknown commands but keep the content after
    result = re.sub(r'\\[a-zA-Z]+', '', result)
    result = result.replace('\\', '')
    
    # Clean up extra spaces
    result = ' '.join(result.split())
    
    return result.strip() if result.strip() else None


def convert_inline_math_to_unicode(content: str) -> str:
    """Convert inline math ($...$) to Unicode where possible."""
    def replace_inline(match):
        latex = match.group(1)
        unicode_result = latex_to_unicode(latex)
        if unicode_result:
            return unicode_result
        else:
            # Keep as-is for pandoc --webtex to handle
            return match.group(0)
    
    # Pattern: $ not preceded or followed by $
    content = re.sub(r'(?<!\$)\$(?!\$)([^\$\n]+?)\$(?!\$)', replace_inline, content)
    return content


def tex_to_markdown(tex_path: Path) -> str:
    """Convert LaTeX to Markdown using pandoc."""
    result = subprocess.run(
        ['pandoc', str(tex_path), '-t', 'markdown', '--wrap=none'],
        capture_output=True,
        text=True,
        check=True
    )
    return result.stdout


def clean_markdown(md_content: str) -> str:
    """Clean up pandoc markdown output."""
    content = md_content
    
    # Remove ::: fenced divs (pandoc custom environments)
    content = re.sub(r'^:::\s*\{[^}]*\}\s*$', '', content, flags=re.MULTILINE)
    content = re.sub(r'^:::\s*$', '', content, flags=re.MULTILINE)
    
    # Remove \begin{equation} / \end{equation} inside $$ blocks
    content = re.sub(r'\$\$\s*\\begin\{equation\}', '$$', content)
    content = re.sub(r'\\end\{equation\}\s*\$\$', '$$', content)
    
    # Replace \begin{align} with \begin{aligned} inside $$
    content = content.replace(r'\begin{align}', r'\begin{aligned}')
    content = content.replace(r'\end{align}', r'\end{aligned}')
    
    # Clean up escaped characters in footnotes
    content = re.sub(r'\\\.', '.', content)
    content = re.sub(r'\\"', '"', content)
    
    return content


def markdown_to_html(md_path: Path, output_path: Path, dpi: int = 200, title: str = "") -> None:
    """Convert Markdown to HTML with webtex for display math."""
    webtex_url = f'https://latex.codecogs.com/png.latex?\\dpi{{{dpi}}}'
    
    cmd = [
        'pandoc', str(md_path),
        '-s',
        f'--webtex={webtex_url}',
        '-V', 'maxwidth=100%',
        '-o', str(output_path)
    ]
    
    if title:
        cmd.extend(['--metadata', f'title={title}'])
    
    subprocess.run(cmd, check=True)



def post_process_html(html_path: Path) -> None:
    """
    Post-process the generated HTML to match Substack requirements.
    - Wraps display math images in centered paragraphs
    - Replaces curly quotes
    - Cleans up empty paragraphs
    """
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Replace curly quotes with straight quotes (Substack prefers standard ones)
    content = content.replace('‘', "'").replace('’', "'")
    content = content.replace('“', '"').replace('”', '"')

    # 2. Wrap display math images in centered paragraphs
    # Pandoc generates <img class="math display" ... /> (or similar depending on version/css)
    # We want to extract them to their own block
    
    # Pattern to find the display math image. 
    # Pandoc 3+ often outputs: <span class="math display">...<img ...>...</span> or just <img class="math display">
    # The build.sh used: r'(<img[^>]*class="math display"[^>]*/>)'
    
    # Let's be robust and look for the image tag with class="math display"
    pattern = r'(<img[^>]*class="math display"[^>]*>)'
    
    def replace_display(match):
        img_tag = match.group(1)
        # Ensure it's closed properly if strictly needed, but browsers are lenient.
        # Substack typically wants clean blocks.
        return f'</p><p style="text-align:center;">{img_tag}</p><p>'

    content = re.sub(pattern, replace_display, content)

    # 3. Clean up empty paragraphs created by the splitting
    content = content.replace('<p></p>', '')
    content = content.replace('<p> </p>', '')
    content = re.sub(r'<p>\s*</p>', '', content)
    
    # 4. Handle any remaining artifacts
    # (Optional: Add specific mappings if needed, but Unicode is generally preferred)

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(content)


def convert_to_substack(
    input_path: Path,
    output_path: Path | None = None,
    dpi: int = 200,
    title: str = ""
) -> Path:
    """
    Full pipeline: LaTeX/Markdown -> Markdown -> Unicode cleanup -> HTML with webtex -> Post-process.
    
    Args:
        input_path: Path to input .tex or .md file
        output_path: Path for output .html file (default: same name as input)
        dpi: DPI for equation images (default: 200)
        title: HTML document title
    
    Returns:
        Path to generated HTML file
    """
    input_path = Path(input_path)
    if output_path is None:
        output_path = input_path.with_suffix('.html')
    else:
        output_path = Path(output_path)
    
    print(f"Converting {input_path.name} -> {output_path.name}")
    
    # Step 1: Input Processing
    if input_path.suffix.lower() == '.tex':
        print("  [1/5] Converting LaTeX to Markdown...")
        md_content = tex_to_markdown(input_path)
    elif input_path.suffix.lower() == '.md':
        print("  [1/5] Reading Markdown input...")
        with open(input_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
    else:
        raise ValueError(f"Unsupported file extension: {input_path.suffix}")
    
    # Step 2: Clean up Markdown
    print("  [2/5] Cleaning and normalizing Markdown...")
    md_content = clean_markdown(md_content)
    
    # Step 3: Convert simple inline math to Unicode
    print("  [3/5] Converting inline math to Unicode...")
    md_content = convert_inline_math_to_unicode(md_content)
    
    # Write intermediate markdown
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write(md_content)
        temp_md = Path(f.name)
    
    # Step 4: Markdown -> HTML with webtex for display math
    print(f"  [4/5] Generating HTML with {dpi}dpi equations...")
    try:
        markdown_to_html(temp_md, output_path, dpi=dpi, title=title)
        
        # Step 5: Post-process HTML for Substack layout
        print("  [5/5] Post-processing for Substack layout...")
        post_process_html(output_path)
        
    finally:
        # Clean up temp file
        if temp_md.exists():
            temp_md.unlink()
    
    print(f"Done! Output: {output_path}")
    return output_path


import shutil

def check_dependencies():
    """Check if required system dependencies are installed."""
    if not shutil.which('pandoc'):
        print("Error: 'pandoc' is not installed or not on PATH.")
        print("  Please install pandoc: https://pandoc.org/installing.html")
        exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='Convert LaTeX or Markdown documents to Substack-friendly HTML',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python doc2substack.py article.tex
    python doc2substack.py article.md
    python doc2substack.py article.tex --output article_substack.html
        """
    )
    parser.add_argument('input', type=Path, help='Input file (.tex or .md)')
    parser.add_argument('-o', '--output', type=Path, help='Output HTML file (default: input.html)')
    parser.add_argument('--dpi', type=int, default=200, help='DPI for equation images (default: 200)')
    parser.add_argument('--title', type=str, default='', help='HTML document title')
    
    args = parser.parse_args()
    
    check_dependencies()
    
    if not args.input.exists():
        print(f"Error: Input file not found: {args.input}")
        return 1
    
    if args.input.suffix.lower() not in ['.tex', '.md']:
        print(f"Warning: Input file does not have .tex or .md extension: {args.input}")
    
    try:
        convert_to_substack(
            args.input,
            args.output,
            dpi=args.dpi,
            title=args.title
        )
        return 0
    except subprocess.CalledProcessError as e:
        print(f"Error running pandoc: {e}")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == '__main__':
    exit(main())
