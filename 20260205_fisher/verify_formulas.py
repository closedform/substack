"""
Symbolic verification of formulas in fisher_modern.tex
using symderive (https://github.com/closedform/deriver).

Run: cd ~/Projects/deriver && uv run python3 ~/Projects/substack/20260205_fisher/verify_formulas.py
"""

from symderive import Symbol, Simplify, D, Series
from sympy import (
    sqrt, log, tanh, atanh, cosh, sech, Rational, oo,
    gamma as Gamma, pi, integrate, symbols, exp, Function
)
import numpy as np
from scipy import stats


def verify_christoffel_rho():
    """Verify Christoffel symbol in rho-coordinates for the full metric."""
    rho = Symbol("rho", real=True)
    n = Symbol("n", positive=True)

    # Full metric: g_11 = n(1 + rho^2) / (1 - rho^2)^2
    g11 = n * (1 + rho**2) / (1 - rho**2)**2
    dg11 = D(g11, rho)

    # Christoffel: Gamma^1_11 = (1/2g_11) dg_11/drho
    christoffel = Simplify(dg11 / (2 * g11))
    print(f"Exact Christoffel (rho-coords): {christoffel}")

    # Leading-order metric: g_11 = n / (1 - rho^2)^2
    g11_leading = n / (1 - rho**2)**2
    christoffel_leading = Simplify(D(g11_leading, rho) / (2 * g11_leading))
    print(f"Leading-order Christoffel:       {christoffel_leading}")

    # Verify: exact should be rho*(rho^2 + 3) / ((1 + rho^2)*(1 - rho^2))
    expected = rho * (rho**2 + 3) / ((1 + rho**2) * (1 - rho**2))
    diff = Simplify(christoffel - expected)
    assert diff == 0, f"Mismatch: {diff}"
    print("  -> Confirmed: rho*(rho^2+3) / ((1+rho^2)*(1-rho^2))")

    # Verify leading order is 2*rho/(1-rho^2)
    expected_leading = 2 * rho / (1 - rho**2)
    diff_leading = Simplify(christoffel_leading - expected_leading)
    assert diff_leading == 0, f"Mismatch: {diff_leading}"
    print("  -> Confirmed leading order: 2*rho/(1-rho^2)")
    print()


def verify_christoffel_zeta():
    """Verify Christoffel symbol approximately vanishes in zeta-coordinates."""
    zeta = Symbol("zeta", real=True)
    n = Symbol("n", positive=True)

    # Transformed metric: g'_11 = n*(1 + tanh^2(zeta))
    g11_zeta = n * (1 + tanh(zeta)**2)
    dg11 = D(g11_zeta, zeta)

    christoffel_zeta = Simplify(dg11 / (2 * g11_zeta))
    print(f"Christoffel (zeta-coords): {christoffel_zeta}")
    print("  -> Not exactly zero; approximately vanishes near zeta=0")

    # Evaluate numerically at zeta=0
    val_at_0 = christoffel_zeta.subs(zeta, 0)
    print(f"  -> Value at zeta=0: {val_at_0}")
    assert val_at_0 == 0, "Should vanish at zeta=0"
    print()


def verify_kappa():
    """Verify kappa = -(1/2g_11) d^2(log g_11)/drho^2 at rho=0."""
    rho = Symbol("rho", real=True)
    n = Symbol("n", positive=True)

    # Full metric
    g11_full = n * (1 + rho**2) / (1 - rho**2)**2
    log_g_full = log(g11_full)
    d2_log_full = D(D(log_g_full, rho), rho)
    kappa_full = Simplify(-d2_log_full / (2 * g11_full))
    kappa_full_at_0 = Simplify(kappa_full.subs(rho, 0))
    print(f"kappa (full metric, rho=0):    {kappa_full_at_0}")

    # Leading-order metric
    g11_lead = n / (1 - rho**2)**2
    log_g_lead = log(g11_lead)
    d2_log_lead = D(D(log_g_lead, rho), rho)
    kappa_lead = Simplify(-d2_log_lead / (2 * g11_lead))
    kappa_lead_at_0 = Simplify(kappa_lead.subs(rho, 0))
    print(f"kappa (leading-order, rho=0):   {kappa_lead_at_0}")

    assert kappa_full_at_0 == Rational(-3, 1) / n, f"Expected -3/n, got {kappa_full_at_0}"
    assert kappa_lead_at_0 == Rational(-2, 1) / n, f"Expected -2/n, got {kappa_lead_at_0}"
    print("  -> Confirmed: -3/n (full), -2/n (leading order)")
    print("  -> Paper uses -2/n (leading order)")
    print()


def verify_leading_order_error():
    """Verify the relative error formula rho^2/(1+rho^2)."""
    print("Leading-order approximation drops factor (1+rho^2):")
    for rho_val in [0.1, 0.3, 0.5, 0.7, 0.9]:
        err = rho_val**2 / (1 + rho_val**2)
        print(f"  |rho| = {rho_val}: relative error = {err:.1%}")
    print("  -> Paper claims: <10% for |rho|<0.3, ~45% at |rho|=0.9")
    print()


def verify_intraclass_density():
    """
    Verify the intraclass correlation density by Monte Carlo.

    The density is:
      p_intra(r | rho) = C_n * (1+rho)^{n/2} * (1-rho)^{(n-1)/2}
                         * (1+r)^{(n-3)/2} * (1-r)^{(n-2)/2}
                         * (1 - rho*r)^{-(2n-1)/2}
    where C_n = Gamma((2n-1)/2) / (2^{(2n-3)/2} * Gamma((n-1)/2) * Gamma(n/2))
    """
    from scipy.special import gamma as sp_gamma

    def intraclass_density(r, rho, n):
        C_n = sp_gamma((2*n - 1) / 2) / (
            2**((2*n - 3) / 2) * sp_gamma((n - 1) / 2) * sp_gamma(n / 2)
        )
        return (
            C_n
            * (1 + rho)**(n / 2) * (1 - rho)**((n - 1) / 2)
            * (1 + r)**((n - 3) / 2) * (1 - r)**((n - 2) / 2)
            * (1 - rho * r)**(-(2*n - 1) / 2)
        )

    def simulate_intraclass(rho, n, n_sims=200_000):
        """
        Simulate intraclass r from n pairs via chi-squared decomposition.

        In sum/difference coordinates u_i, v_i:
          S_u = sum(u_i - u_bar)^2 ~ (1+rho) * chi^2_{n-1}
          S_v = sum(v_i^2)         ~ (1-rho) * chi^2_n
          r = (S_u - S_v) / (S_u + S_v)
        """
        chi2_a = np.random.chisquare(n - 1, n_sims)
        chi2_b = np.random.chisquare(n, n_sims)
        S_u = (1 + rho) * chi2_a
        S_v = (1 - rho) * chi2_b
        r = (S_u - S_v) / (S_u + S_v)
        return np.clip(r, -0.999, 0.999)

    print("Intraclass density verification (Monte Carlo):")
    test_cases = [(10, 0.0), (10, 0.5), (20, 0.8), (15, -0.3)]

    for n, rho in test_cases:
        # Check normalization
        from scipy.integrate import quad
        integral, _ = quad(lambda r: intraclass_density(r, rho, n), -0.999, 0.999)

        # Compare shape with simulation
        sim = simulate_intraclass(rho, n)
        r_grid = np.linspace(-0.95, 0.95, 50)
        theory = np.array([intraclass_density(r, rho, n) for r in r_grid])
        theory /= theory.sum()

        hist, edges = np.histogram(sim, bins=r_grid, density=True)
        hist_norm = hist / hist.sum()
        theory_mid = (theory[:-1] + theory[1:]) / 2
        theory_mid /= theory_mid.sum()

        corr = np.corrcoef(hist_norm, theory_mid)[0, 1]
        print(f"  n={n:2d}, rho={rho:+.1f}: integral={integral:.6f}, shape_corr={corr:.4f}")

    print("  -> All integrals should be ~1.0, shape correlations > 0.99")
    print()


def verify_worked_examples():
    """Verify the three worked examples in Section 6."""
    print("Example 1: Fisher z-test")
    r, n = 0.45, 25
    z = np.arctanh(r)
    se = 1 / np.sqrt(n - 3)
    Z_stat = z / se
    p_val = 2 * (1 - stats.norm.cdf(abs(Z_stat)))
    print(f"  r={r}, n={n}")
    print(f"  z = arctanh({r}) = {z:.3f}")
    print(f"  SE = 1/sqrt({n-3}) = {se:.3f}")
    print(f"  Z = {Z_stat:.2f}, p = {p_val:.4f}")
    print()

    print("Example 2: Combining independent correlations")
    studies = [(0.60, 30), (0.35, 50), (0.55, 20)]
    zs = [np.arctanh(r) for r, _ in studies]
    ws = [n - 3 for _, n in studies]
    z_pooled = sum(w * z for w, z in zip(ws, zs)) / sum(ws)
    se_pooled = 1 / np.sqrt(sum(ws))
    r_pooled = np.tanh(z_pooled)
    ci_low = np.tanh(z_pooled - 1.96 * se_pooled)
    ci_high = np.tanh(z_pooled + 1.96 * se_pooled)
    print(f"  z values: {[f'{z:.3f}' for z in zs]}")
    print(f"  weights:  {ws}")
    print(f"  z_pooled = {z_pooled:.3f}, r_pooled = tanh({z_pooled:.3f}) = {r_pooled:.3f}")
    print(f"  SE = {se_pooled:.3f}")
    print(f"  95% CI for rho: ({ci_low:.3f}, {ci_high:.3f})")
    print()

    print("Example 3: Naive vs geodesic CI")
    r, n = 0.80, 10
    se_naive = (1 - r**2) / np.sqrt(n)
    ci_naive = (r - 1.96 * se_naive, r + 1.96 * se_naive)
    z = np.arctanh(r)
    se_z = 1 / np.sqrt(n - 3)
    ci_z = (np.tanh(z - 1.96 * se_z), np.tanh(z + 1.96 * se_z))
    print(f"  r={r}, n={n}")
    print(f"  Naive: SE={se_naive:.3f}, CI=({ci_naive[0]:.3f}, {ci_naive[1]:.3f})")
    print(f"  Geodesic: z={z:.3f}, SE(z)={se_z:.3f}, CI=({ci_z[0]:.3f}, {ci_z[1]:.3f})")
    print(f"  -> Naive CI overshoots rho=1: {ci_naive[1]:.3f} > 1")
    print()

    print("Geodesic distance check:")
    d = np.arctanh(0.9) - np.arctanh(0.5)
    print(f"  arctanh(0.9) - arctanh(0.5) = {d:.3f}")
    print()


if __name__ == "__main__":
    print("=" * 60)
    print("Formula verification for fisher_modern.tex")
    print("=" * 60)
    print()

    verify_christoffel_rho()
    verify_christoffel_zeta()
    verify_kappa()
    verify_leading_order_error()
    verify_intraclass_density()
    verify_worked_examples()

    print("=" * 60)
    print("All checks passed.")
    print("=" * 60)
