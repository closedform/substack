"""
Task 2: 3-parameter Fisher metric for (m, sigma, rho) on the bivariate normal
with equal means and variances.
"""
import sys
sys.path.insert(0, "/Users/bd/Projects/deriver/src")

from symderive import (
    Symbol, symbols, Metric, TeXForm, Simplify, D, Rational, Matrix,
)
from symderive.core.math_api import sp

m = Symbol("m")
sigma = Symbol("sigma", positive=True)
rho = Symbol("rho")
n = Symbol("n", positive=True)

print("=" * 70)
print("TASK 2: 3-parameter Fisher Metric for (m, sigma, rho)")
print("=" * 70)

# Fisher information metric for bivariate normal with equal means and variances
# Coordinates: (m, sigma, rho)
g_components = [
    [n * 2 / (sigma**2 * (1 + rho)),    0,                                      0],
    [0,                                   n * 4 / sigma**2,                      -n * 2 * rho / (sigma * (1 - rho**2))],
    [0,                                   -n * 2 * rho / (sigma * (1 - rho**2)),  n * (1 + rho**2) / (1 - rho**2)**2],
]

g = Metric([m, sigma, rho], g_components)

print("\n--- Metric g_ab ---")
for i in range(3):
    for j in range(3):
        val = g[i, j]
        if val != 0:
            coord_names = ["m", "sigma", "rho"]
            print(f"  g_{{{coord_names[i]},{coord_names[j]}}} = {val}")
            print(f"    LaTeX: {TeXForm(val)}")

print("\n--- Full metric matrix (LaTeX) ---")
print(f"g_{{ab}} = {TeXForm(g.g)}")

# ---- Inverse metric g^{ab} ----
print("\n--- Inverse Metric g^{{ab}} ---")
g_inv = g.inverse
print(f"g^{{ab}} = {TeXForm(g_inv)}")

# Print non-zero components
coord_names = ["m", "sigma", "rho"]
for i in range(3):
    for j in range(i, 3):
        val = Simplify(g_inv[i, j])
        if val != 0:
            print(f"  g^{{{coord_names[i]},{coord_names[j]}}} = {val}")
            print(f"    LaTeX: {TeXForm(val)}")

# ---- Verify g_23 != 0 (non-orthogonality of sigma and rho) ----
print("\n--- Non-orthogonality check ---")
g23 = g[1, 2]  # 0-indexed: sigma=1, rho=2
print(f"g_{{sigma,rho}} = {g23}")
print(f"LaTeX: g_{{\\sigma\\rho}} = {TeXForm(g23)}")
print(f"g_{{sigma,rho}} != 0: {g23 != 0}")

# ---- Transformed (3,3) component under rho -> zeta = arctanh(rho) ----
print("\n--- Jacobian cancellation for g_33 under rho -> zeta = arctanh(rho) ---")
zeta = Symbol("zeta")
rho_of_zeta = sp.tanh(zeta)
drho_dzeta = D(rho_of_zeta, zeta)
drho_dzeta_simplified = Simplify(drho_dzeta)
print(f"drho/dzeta = {drho_dzeta_simplified}")
print(f"LaTeX: \\frac{{d\\rho}}{{d\\zeta}} = {TeXForm(drho_dzeta_simplified)}")

# g_zeta_zeta = g_rho_rho * (drho/dzeta)^2
g33_rho = g[2, 2]  # g_rho_rho
g33_zeta = Simplify(g33_rho.subs(rho, rho_of_zeta) * drho_dzeta**2)
print(f"\ng_{{rho,rho}} = {g33_rho}")
print(f"LaTeX: g_{{\\rho\\rho}} = {TeXForm(g33_rho)}")
print(f"\ng_{{zeta,zeta}} = g_{{rho,rho}} * (drho/dzeta)^2 = {g33_zeta}")
print(f"LaTeX: g_{{\\zeta\\zeta}} = {TeXForm(g33_zeta)}")

print("\n--- Summary (all LaTeX) ---")
print(f"Metric matrix: {TeXForm(g.g)}")
print(f"Inverse metric: {TeXForm(g_inv)}")
print(f"g_{{sigma,rho}} = {TeXForm(g23)}")
print(f"g_{{zeta,zeta}} = {TeXForm(g33_zeta)}")
