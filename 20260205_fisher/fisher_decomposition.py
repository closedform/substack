"""
Orthogonal decomposition figure: x = projection onto L + deviation in W.
Tufte-style: high data-ink ratio, no chartjunk, direct labeling.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches

plt.rcParams.update({
    "font.size": 12,
    "axes.labelsize": 14,
    "text.usetex": True,
    "font.family": "serif",
    "figure.dpi": 150,
})

fig, ax = plt.subplots(figsize=(5.5, 5))

# Coordinates
m_x = 1.0       # true mean on L
xbar_x = 2.2    # sample mean on L
d_y = 2.0        # deviation height

# L axis (horizontal)
ax.annotate("", xy=(4.0, 0), xytext=(-0.3, 0),
            arrowprops=dict(arrowstyle="->", color="black", lw=1.2))
ax.text(4.1, 0, r"$L$", fontsize=14, va="center")

# W axis (vertical)
ax.annotate("", xy=(0, 3.2), xytext=(0, -0.3),
            arrowprops=dict(arrowstyle="->", color="black", lw=1.2))
ax.text(0, 3.35, r"$W$", fontsize=14, ha="center")

# True mean on L
ax.plot(m_x, 0, "o", color="firebrick", markersize=6, zorder=5)
ax.text(m_x, -0.25, r"$m$", fontsize=13, ha="center", va="top",
        color="firebrick")

# Sample mean on L
ax.plot(xbar_x, 0, "o", color="black", markersize=6, zorder=5)
ax.text(xbar_x, -0.25, r"$\bar{x}$", fontsize=13, ha="center", va="top")

# Horizontal dotted line between m and xbar
ax.plot([m_x, xbar_x], [0, 0], ":", color="firebrick", lw=1.5)
ax.text((m_x + xbar_x) / 2, -0.55, r"$\sqrt{n}\,(\bar{x} - m)$",
        fontsize=10, ha="center", va="top", color="firebrick")

# Sample point
ax.plot(xbar_x, d_y, "o", color="black", markersize=6, zorder=5)
ax.text(xbar_x + 0.15, d_y + 0.1, r"$\mathbf{x}$", fontsize=14,
        va="bottom")

# Deviation vector (vertical arrow)
ax.annotate("", xy=(xbar_x, d_y - 0.08), xytext=(xbar_x, 0.08),
            arrowprops=dict(arrowstyle="-|>", color="black", lw=1.8))
ax.text(xbar_x - 0.25, d_y / 2, r"$d^i$", fontsize=13, ha="right",
        va="center")

# Radius label on right
ax.text(xbar_x + 0.35, d_y / 2, r"$R = \sqrt{n}\,\hat\sigma_2$",
        fontsize=10, ha="left", va="center", color="gray")

# Sufficiency sphere (dashed arc)
theta = np.linspace(0, np.pi / 2, 80)
arc_r = d_y
arc_x = xbar_x + arc_r * np.cos(theta)
arc_y = arc_r * np.sin(theta)
ax.plot(arc_x, arc_y, "--", color="gray", lw=0.9, alpha=0.7)

# Clean up axes
ax.set_xlim(-0.5, 4.5)
ax.set_ylim(-0.9, 3.5)
ax.set_aspect("equal")
ax.axis("off")

fig.tight_layout()
fig.savefig("/Users/bd/Projects/math/fisher_decomposition.pdf",
            bbox_inches="tight")
plt.close(fig)
print("Saved: fisher_decomposition.pdf")
