# doc2substack: A Bridge for Mathematical Writing

If you write about physics, math, or quantitative finance, you know the pain of moving from your writing environment to the web.

You have a beautiful LaTeX document or a Markdown file full of carefully crafted equations. You want to publish it on Substack. But when you paste it in, the math breaks. Superscripts detach, logic symbols vanish, and complex equations turn into garbage.

We built **doc2substack** to solve this.

It is a lightweight, open-source utility that converts your technical documents into clean, Substack-ready HTML. It preserves your prose, converts inline math to native Unicode for smooth reading, and renders complex display math as crisp, high-DPI images.

## Where to Get It

The utility is open source and available directly in our repository:

[https://github.com/closedform/substack/tree/main/utils](https://github.com/closedform/substack/tree/main/utils)

## How to Use It

The script is a single Python file with no complex dependencies (just standard Python + `pandoc`).

1.  **Write naturally:** Create your post in LaTeX (`.tex`) or Markdown (`.md`).
2.  **Run the converter:**
    ```bash
    python substack/utils/doc2substack.py my_post.md
    ```
3.  **Publish:** Open the generated `.html` file, copy everything, and paste it into the Substack editor.

## The Full Example

Here is a demonstration of what `doc2substack` can do. We will mix prose, inline math, and display equations.

### 1. Unified Inline Math
We automatically convert simple LaTeX expressions into Unicode characters so they flow naturally with the text.

*   **Input:** `Let $\alpha$ be the learning rate, $\sigma$ the volatility, and $w^t$ be the weights at time $t$. We verify that $\alpha > 0$ and $\nabla f \approx 0$.`
*   **Output:** Let α be the learning rate, σ the volatility, and wᵗ be the weights at time t. We verify that α > 0 and ∇f ≈ 0.

This keeps sentences readable without those jagged, misaligned images breaking your paragraph's line height.

### 2. Complex Display Math
For rigorous derivations, we need proper rendering. The tool detects display blocks (like `$$...$$`) and renders them as high-quality images.

Consider the Gaussian integral:
$$ \int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi} $$

Or the definition of the Christoffel symbols in terms of the metric tensor $g_{ij}$:
$$ \Gamma^k_{ij} = \frac{1}{2}g^{km}\left(\frac{\partial g_{mj}}{\partial x^i} + \frac{\partial g_{mi}}{\partial x^j} - \frac{\partial g_{ij}}{\partial x^m}\right) $$

These images are generated at 200 DPI (configurable) to look sharp on retina displays, and are automatically centered.

### 3. Structural Cleanup
The tool also handles:
*   **Smart Quotes:** Converts "straight quotes" to “curly quotes” (or vice versa depending on your preference settings).
*   **Layout:** Removes artifacts from pandoc conversions to ensure a clean paste.

## Why We Built This

Honestly, I was just tired of the screenshot workflow.

I write everything in VS Code. I have my `$$` macros set up, my snippets ready, and my git history clean. Moving to Substack felt like stepping back into the Stone Age—manually screenshotting equations, cropping them, and hoping they aligned with the text.

I wanted something that let me write in the environment I love (LaTeX/Markdown) and just *push* to the platform I publish on. `doc2substack` is my little bridge between those two worlds. It's not perfect, but it sure beats `Cmd+Shift+4`.

Happy writing.
