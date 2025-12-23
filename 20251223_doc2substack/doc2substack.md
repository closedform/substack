# doc2substack: A Bridge for Mathematical Writing

If you write about physics, math, or quantitative finance, you know the pain of moving from your writing environment to the web.

You have a beautiful LaTeX document or a Markdown file full of carefully crafted equations. You want to publish it on Substack. But when you paste it in, the math breaks. Superscripts detach, logic symbols vanish, and complex equations turn into garbage.

**doc2substack** is a lightweight, open-source utility that converts your technical documents into clean, Substack-ready HTML. It preserves your prose, converts inline math to native Unicode for smooth reading, and renders complex display math as crisp, high-DPI images.

## Where to Get It

The utility is open source and available directly in the repository:

[https://github.com/closedform/substack/tree/main/utils](https://github.com/closedform/substack/tree/main/utils)

## How to Use It

The script is a single Python file with no complex dependencies (just standard Python + `pandoc`).

1.  **Write naturally:** Create your post in LaTeX (`.tex`) or Markdown (`.md`).
2.  **Run the converter:**
    ```bash
    python substack/utils/doc2substack.py my_post.md
    ```
3.  **Publish:** Open the generated `.html` file, copy everything, and paste it into the Substack editor.

## Example: The Heat Equation

The following section demonstrates `doc2substack` by rendering a standard PDE derivation. It mixes prose, inline Unicode math, and standard LaTeX display blocks.

---

Consider the one-dimensional heat equation for a function u(x,t) representing temperature distribution over a rod:

$$ \frac{\partial u}{\partial t} = \alpha \frac{\partial^2 u}{\partial x^2} $$

where α is the thermal diffusivity constant. The goal is to find a solution using the method of separation of variables. Let u(x,t) = X(x)T(t). Substituting this form into the PDE yields:

$$ \frac{1}{\alpha T} \frac{dT}{dt} = \frac{1}{X} \frac{d^2X}{dx^2} = -\lambda $$

Here, λ is the separation constant. This splits the problem into two ordinary differential equations. The temporal component decays exponentially as T(t) ∝ e^{-λαt}, while the spatial component satisfies:

$$ X''(x) + \lambda X(x) = 0 $$

For physical boundary conditions (e.g., Dirichlet conditions u(0,t) = u(L,t) = 0), the eigenvalues are discrete, given by λₙ = (nπ/L)². The general solution is a superposition of these modes:

$$ u(x,t) = \sum_{n=1}^{\infty} B_n \sin\left(\frac{n\pi x}{L}\right) e^{-\alpha \left(\frac{n\pi}{L}\right)^2 t} $$

The coefficients Bₙ are determined by the initial condition u(x,0) via Fourier sine series orthogonality.


## Feedback

If you find a bug or have a feature request, please [open an issue on GitHub](https://github.com/closedform/substack/issues). Or, just drop a comment below.

Cheers,
