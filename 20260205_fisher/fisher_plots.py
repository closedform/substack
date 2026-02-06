"""
Task 3: Generate matplotlib plots for Fisher information metric visualization.

(a) fisher_metric_stretching.pdf - g_11(rho) = (1+rho^2)/(1-rho^2)^2
(b) equal_zeta_points.pdf - Equal zeta-spacing mapped to rho via tanh
(c) z_transform_distributions.pdf - Sampling distributions of r vs z = arctanh(r)
"""
import sys
sys.path.insert(0, "/Users/bd/Projects/deriver/src")

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats
from scipy.special import gammaln

OUTPUT_DIR = "/Users/bd/Projects/math"

# Use a clean style
plt.rcParams.update({
    "font.size": 12,
    "axes.labelsize": 14,
    "axes.titlesize": 14,
    "xtick.labelsize": 11,
    "ytick.labelsize": 11,
    "text.usetex": False,
    "font.family": "serif",
    "figure.dpi": 150,
})


# =========================================================================
# (a) Fisher metric stretching: g_11(rho) = (1+rho^2)/(1-rho^2)^2
# =========================================================================
def plot_fisher_metric_stretching():
    fig, ax = plt.subplots(figsize=(7, 5))

    rho = np.linspace(-0.995, 0.995, 2000)
    g11 = (1 + rho**2) / (1 - rho**2)**2

    ax.plot(rho, g11, color="navy", linewidth=2)

    # Mark some reference points
    for r_val in [-0.9, -0.5, 0, 0.5, 0.9]:
        g_val = (1 + r_val**2) / (1 - r_val**2)**2
        if g_val < 50:
            ax.plot(r_val, g_val, "o", color="firebrick", markersize=5, zorder=5)
            ax.annotate(
                f"$\\rho={r_val}$",
                (r_val, g_val),
                textcoords="offset points",
                xytext=(8, 8),
                fontsize=9,
            )

    ax.set_xlabel(r"$\rho$")
    ax.set_ylabel(r"$g_{\rho\rho}(\rho)\;/\;n$")
    ax.set_title(
        r"Fisher metric component $g_{\rho\rho} = n\,(1+\rho^2)/(1-\rho^2)^2$"
    )
    ax.set_xlim(-1, 1)
    ax.set_ylim(0, 60)
    ax.axvline(x=-1, color="gray", linestyle="--", alpha=0.5, linewidth=0.8)
    ax.axvline(x=1, color="gray", linestyle="--", alpha=0.5, linewidth=0.8)
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    path = f"{OUTPUT_DIR}/fisher_metric_stretching.pdf"
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {path}")


# =========================================================================
# (b) Equal zeta-spacing mapped back to rho = tanh(zeta)
# =========================================================================
def plot_equal_zeta_points():
    fig, ax = plt.subplots(figsize=(8, 3))

    # Draw the rho interval
    ax.plot([-1, 1], [0, 0], color="black", linewidth=2)
    ax.plot([-1, -1], [-0.02, 0.02], color="black", linewidth=2)
    ax.plot([1, 1], [-0.02, 0.02], color="black", linewidth=2)

    # Positive zeta values and their negatives
    zeta_vals = np.array([0, 0.5, 1.0, 1.5, 2.0])
    all_zeta = np.concatenate([-zeta_vals[::-1][:-1], zeta_vals])
    rho_vals = np.tanh(all_zeta)

    colors = plt.cm.viridis(np.linspace(0.2, 0.9, len(all_zeta)))

    for i, (z, r) in enumerate(zip(all_zeta, rho_vals)):
        ax.plot(r, 0, "|", color=colors[i], markersize=25, markeredgewidth=2.5)
        label_y = 0.06 if (i % 2 == 0) else -0.08
        va = "bottom" if label_y > 0 else "top"
        ax.annotate(
            f"$\\zeta={z:.1f}$\n$\\rho={r:.3f}$",
            (r, 0),
            textcoords="offset points",
            xytext=(0, 18 if label_y > 0 else -18),
            ha="center",
            va=va,
            fontsize=8,
            color=colors[i],
        )

    ax.set_xlabel(r"$\rho = \tanh(\zeta)$")
    ax.set_title(
        r"Equal $\zeta$-spacing mapped to $\rho$: the ``rubber ruler'' effect"
    )
    ax.set_xlim(-1.15, 1.15)
    ax.set_ylim(-0.22, 0.22)
    ax.set_yticks([])
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)

    fig.tight_layout()
    path = f"{OUTPUT_DIR}/equal_zeta_points.pdf"
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {path}")


# =========================================================================
# (c) z-transform distributions: r vs z = arctanh(r)
# =========================================================================
def plot_z_transform_distributions():
    """
    For the sample correlation r from a bivariate normal with true
    correlation rho and sample size n, the exact density of r is known
    (a Beta-type distribution). We use the approximation based on the
    exact density:

        f(r) ~ (1-r^2)^{(n-4)/2} * (1-rho*r)^{-(n-1)+1/2}
               * hypergeometric correction

    For simplicity we use scipy's approach: the exact distribution of r
    can be obtained via a transformation of the F or Beta distribution.
    We'll use a direct numerical approach with the known density.

    For z = arctanh(r), the approximate distribution is
        z ~ N(arctanh(rho) + rho/(2(n-1)), 1/(n-3))
    """
    n_sample = 20
    rho_values = [0, 0.3, 0.6, 0.9]
    colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"]

    fig, axes = plt.subplots(2, 1, figsize=(9, 7), sharex=False)

    # Top panel: distribution of r
    ax_r = axes[0]
    r_grid = np.linspace(-0.99, 0.99, 1000)

    for rho_true, color in zip(rho_values, colors):
        # Exact density of sample correlation coefficient
        # f(r; rho, n) = (n-2) * Gamma(n-1) / (sqrt(2*pi) * Gamma(n-1/2))
        #   * (1-rho^2)^{(n-1)/2} * (1-r^2)^{(n-4)/2} / (1-rho*r)^{n-3/2}
        #   * 2F1(1/2, 1/2; (2n-1)/2; (1+rho*r)/2)
        # We'll use a simpler but accurate approximation via the integral form
        # or just use the known density formula directly

        log_density = np.zeros_like(r_grid)
        nn = n_sample
        for idx, r_val in enumerate(r_grid):
            if abs(r_val) >= 0.999:
                log_density[idx] = -np.inf
                continue
            # Use the exact formula (without hypergeometric for speed,
            # which is close to 1 for moderate n)
            log_c = (
                np.log(nn - 2)
                + gammaln(nn - 1)
                - 0.5 * np.log(2 * np.pi)
                - gammaln(nn - 0.5)
            )
            log_f = (
                log_c
                + 0.5 * (nn - 1) * np.log(1 - rho_true**2)
                + 0.5 * (nn - 4) * np.log(1 - r_val**2)
                - (nn - 1.5) * np.log(1 - rho_true * r_val)
            )
            log_density[idx] = log_f

        density = np.exp(log_density - np.max(log_density))
        # Normalize
        dr = r_grid[1] - r_grid[0]
        density = density / (np.sum(density) * dr)

        ax_r.plot(
            r_grid,
            density,
            color=color,
            linewidth=2,
            label=f"$\\rho = {rho_true}$",
        )

    ax_r.set_xlabel(r"Sample correlation $r$")
    ax_r.set_ylabel("Density")
    ax_r.set_title(
        f"Sampling distribution of $r$ ($n = {n_sample}$)"
    )
    ax_r.legend(loc="upper left", fontsize=10)
    ax_r.set_xlim(-1, 1)
    ax_r.grid(True, alpha=0.3)

    # Bottom panel: distribution of z = arctanh(r)
    ax_z = axes[1]
    z_grid = np.linspace(-2.5, 3.5, 1000)
    var_z = 1.0 / (n_sample - 3)
    std_z = np.sqrt(var_z)

    for rho_true, color in zip(rho_values, colors):
        # Fisher's approximation: z ~ N(arctanh(rho) + rho/(2(n-1)), 1/(n-3))
        mu_z = np.arctanh(rho_true) + rho_true / (2 * (n_sample - 1))
        density_z = stats.norm.pdf(z_grid, loc=mu_z, scale=std_z)

        ax_z.plot(
            z_grid,
            density_z,
            color=color,
            linewidth=2,
            label=f"$\\rho = {rho_true}$, $\\mu_z = {mu_z:.3f}$",
        )

    ax_z.set_xlabel(r"Fisher $z = \mathrm{arctanh}(r)$")
    ax_z.set_ylabel("Density")
    ax_z.set_title(
        f"Sampling distribution of $z = \\mathrm{{arctanh}}(r)$"
        f"  ($n = {n_sample}$, $\\mathrm{{Var}}(z) \\approx 1/(n-3) = {var_z:.4f}$)"
    )
    ax_z.legend(loc="upper left", fontsize=9)
    ax_z.grid(True, alpha=0.3)

    fig.tight_layout()
    path = f"{OUTPUT_DIR}/z_transform_distributions.pdf"
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {path}")


if __name__ == "__main__":
    plot_fisher_metric_stretching()
    plot_equal_zeta_points()
    plot_z_transform_distributions()
    print("\nAll plots saved successfully.")
