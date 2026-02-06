"""
Task 1: 1D Fisher information metric on (-1,1) for the correlation parameter rho.
"""
import sys
sys.path.insert(0, "/Users/bd/Projects/deriver/src")

from symderive import (
    Symbol, symbols, Metric, TeXForm, Simplify, D, Rational,
    CoordinateTransformation,
)
from symderive.core.math_api import sp

rho = Symbol("rho")
n = Symbol("n", positive=True)

g11 = n * (1 + rho**2) / (1 - rho**2)**2

print("=" * 70)
print("TASK 1: 1D Fisher Metric for Correlation Parameter rho")
print("=" * 70)

g = Metric([rho], [[g11]])

print("\n--- Metric ---")
print(f"g_11 = {g[0, 0]}")
print(f"LaTeX: g_{{11}} = {TeXForm(g[0, 0])}")

christoffel = g.christoffel_second_kind()
gamma_111 = christoffel[0, 0, 0]

print("\n--- Christoffel Symbol ---")
print(f"Gamma^1_{{11}} = {gamma_111}")
print(f"LaTeX: Gamma^1_{{11}} = {TeXForm(gamma_111)}")

R = g.ricci_scalar()
print("\n--- Ricci Scalar (Gaussian Curvature) ---")
print(f"R = {R}")
print(f"LaTeX: R = {TeXForm(R)}")
print("(Note: All 1D Riemannian manifolds have zero intrinsic curvature.)")

print("\n--- Coordinate Change: zeta = arctanh(rho) ---")
zeta = Symbol("zeta")

rho_of_zeta = sp.tanh(zeta)
drho_dzeta = D(rho_of_zeta, zeta)
drho_dzeta_simplified = Simplify(drho_dzeta)
print("rho(zeta) = tanh(zeta)")
print(f"drho/dzeta = {drho_dzeta_simplified}")
print(f"LaTeX: drho/dzeta = {TeXForm(drho_dzeta_simplified)}")

g_zeta_zeta = Simplify(g11.subs(rho, rho_of_zeta) * drho_dzeta**2)
print(f"\ng_zeta_zeta = g_rho_rho * (drho/dzeta)^2")
print(f"g_zeta_zeta = {g_zeta_zeta}")
print(f"LaTeX: g_zeta_zeta = {TeXForm(g_zeta_zeta)}")

print("\n--- Verification via CoordinateTransformation ---")
transform = CoordinateTransformation(
    old_coords=[rho],
    new_coords=[zeta],
    transform_eqs={rho: sp.tanh(zeta)}
)

g_transformed = transform.transform_metric(g)
g_zz = g_transformed[0, 0]
print(f"g_zeta_zeta (via transform) = {g_zz}")
print(f"LaTeX: g_zeta_zeta = {TeXForm(g_zz)}")

# Further simplify Christoffel using factor/cancel
from symderive import Factor, Cancel
gamma_111_v2 = Simplify(sp.cancel(gamma_111))
gamma_111_v3 = sp.factor(gamma_111)
print("\n--- Christoffel (alternative forms) ---")
print(f"Gamma^1_11 (cancel) = {gamma_111_v2}")
print(f"LaTeX: {TeXForm(gamma_111_v2)}")
print(f"Gamma^1_11 (factor) = {gamma_111_v3}")
print(f"LaTeX: {TeXForm(gamma_111_v3)}")

# Simplify transformed metric using hyperbolic identities
# 1 + tanh^2(z) = 2 - sech^2(z) = 2 - (1 - tanh^2) = 1 + tanh^2
# Also: 1 + tanh^2(z) = (cosh^2(z) + sinh^2(z))/cosh^2(z) = cosh(2z)/cosh^2(z)
# Actually the simplest form: tanh^2(z) + 1 = 2*cosh^2(z)/(cosh^2(z)) is not right.
# Let's just use sp.simplify with trig:
from symderive import TrigSimplify
g_zeta_trig = TrigSimplify(g_zeta_zeta)
print("\n--- Transformed metric (trig simplified) ---")
print(f"g_zeta_zeta (trig) = {g_zeta_trig}")
print(f"LaTeX: {TeXForm(g_zeta_trig)}")

# Alternative: use rewrite
g_zeta_cosh = sp.simplify(g_zeta_zeta.rewrite(sp.cosh))
print(f"g_zeta_zeta (cosh form) = {g_zeta_cosh}")
print(f"LaTeX: {TeXForm(g_zeta_cosh)}")

print("\n" + "=" * 70)
print("SUMMARY: All LaTeX Expressions")
print("=" * 70)
print(f"g_{{rho,rho}} = {TeXForm(g11)}")
print(f"Gamma^rho_{{rho,rho}} = {TeXForm(gamma_111_v3)}")
print(f"R = {TeXForm(R)}")
print(f"drho/dzeta = {TeXForm(drho_dzeta_simplified)}")
print(f"g_{{zeta,zeta}} = {TeXForm(g_zeta_zeta)}")
print(f"g_{{zeta,zeta}} (simplified) = {TeXForm(g_zeta_cosh)}")
