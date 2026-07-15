"""
Cross-verification tests.

Each test asserts that a first-principles Python implementation reproduces the
Excel/VBA reference value from the assessment to at least four decimal places,
which is the reconciliation the notebook's summary table documents.
"""

import numpy as np
import pytest

from src.fixed_income import (
    bisection_ytm,
    bond_price,
    continuous_spot_rate,
    fit_term_structure,
    macaulay_duration,
    modified_duration,
    mortgage_payment,
    pv_annuity,
)
from src.options import black76_call, black76_put, bsm_call_dividend, eso_fair_value
from src.risk import (
    historical_cvar,
    historical_var,
    parametric_cvar,
    parametric_var,
    portfolio_volatility,
)


# --- Q5(i) Annuity -------------------------------------------------------
def test_annuity_pv_matches_excel():
    pv = pv_annuity(1250, 0.064, 12, 4, due=False)
    assert pv == pytest.approx(41658.67, abs=0.01)


def test_annuity_due_premium():
    ord_pv = pv_annuity(1250, 0.064, 12, 4, due=False)
    due_pv = pv_annuity(1250, 0.064, 12, 4, due=True)
    assert due_pv / ord_pv == pytest.approx(1 + 0.064 / 4, abs=1e-9)


# --- Q5(ii) Bond pricing and duration -----------------------------------
def test_bond_price_matches_excel():
    assert bond_price(1000, 0.058, 0.062, 7, 2) == pytest.approx(977.56, abs=0.01)


def test_macaulay_duration_matches_excel():
    assert macaulay_duration(1000, 0.058, 0.062, 7, 2) == pytest.approx(5.8360, abs=1e-4)


def test_modified_duration_matches_excel():
    assert modified_duration(1000, 0.058, 0.062, 7, 2) == pytest.approx(5.6605, abs=1e-4)


def test_lower_coupon_gives_longer_duration():
    """Hopewell & Kaufman (1973): lower coupon -> longer duration."""
    low = macaulay_duration(1000, 0.01, 0.062, 10, 2)
    high = macaulay_duration(1000, 0.12, 0.062, 10, 2)
    assert low > high


# --- Q5(iii) YTM bisection ----------------------------------------------
def test_ytm_bisection_matches_excel():
    ytm, iters = bisection_ytm(1000, 0.0475, 978.40, 6, 2)
    assert ytm * 100 == pytest.approx(5.1734, abs=1e-3)
    # price at the converged yield reprices the market price
    assert bond_price(1000, 0.0475, ytm, 6, 2) == pytest.approx(978.40, abs=1e-2)


# --- Q5(iv) Mortgage -----------------------------------------------------
def test_mortgage_payment_matches_excel():
    assert mortgage_payment(335000, 0.0465, 25, 12) == pytest.approx(1890.68, abs=0.01)


# --- Q5(v) Term structure ------------------------------------------------
def test_continuous_spot_rate():
    assert continuous_spot_rate(0.6554, 10) == pytest.approx(0.042251, abs=1e-5)


def test_term_structure_fit():
    ts = fit_term_structure(
        [0.5, 1, 2, 3, 5, 7, 10],
        [0.981, 0.9608, 0.9222, 0.8869, 0.8167, 0.7558, 0.6554],
    )
    assert ts["spot_rates"][-1] == pytest.approx(0.042251, abs=1e-5)
    assert len(ts["forward_rates"]) == 6


# --- Q6(i) Black (1976) --------------------------------------------------
def test_black76_call_matches_excel():
    assert black76_call(108.20, 107.00, 0.0325, 0.75, 0.17) == pytest.approx(6.7652, abs=1e-4)


def test_black76_put_matches_excel():
    assert black76_put(108.20, 107.00, 0.0325, 0.75, 0.17) == pytest.approx(5.5941, abs=1e-4)


def test_put_call_parity_black76():
    import math

    F, K, r, T = 108.20, 107.00, 0.0325, 0.75
    call = black76_call(F, K, r, T, 0.17)
    put = black76_put(F, K, r, T, 0.17)
    assert call - put == pytest.approx(math.exp(-r * T) * (F - K), abs=1e-8)


# --- Q6(iii) ESO ---------------------------------------------------------
def test_bsm_call_matches_excel():
    bs = bsm_call_dividend(42, 40, 0.031, 0.012, 0.34, 6.5)
    assert bs == pytest.approx(15.2899, abs=1e-4)


def test_eso_survival_scaling():
    eso, bs, surv = eso_fair_value(42, 40, 0.031, 0.012, 0.34, 6.5, 3.0, 0.035)
    assert surv == pytest.approx((1 - 0.035) ** 3, abs=1e-9)
    assert eso == pytest.approx(surv * bs, abs=1e-9)


# --- Q6(ii) Risk ---------------------------------------------------------
def test_parametric_var_positive_and_ordered():
    var = parametric_var(2_500_000, 0.012, 0.0005, 0.99, 10)
    cvar = parametric_cvar(2_500_000, 0.012, 0.0005, 0.99, 10)
    assert cvar > var > 0  # expected shortfall exceeds VaR


def test_historical_var_cvar():
    rng = np.random.default_rng(0)
    returns = rng.normal(0, 0.01, 2000)
    var = historical_var(returns, 1_000_000, 0.99)
    cvar = historical_cvar(returns, 1_000_000, 0.99)
    assert cvar >= var > 0


def test_portfolio_volatility_diagonal():
    cov = np.diag([0.04, 0.09])  # vols 0.2 and 0.3
    w = np.array([0.5, 0.5])
    expected = np.sqrt(0.25 * 0.04 + 0.25 * 0.09)
    assert portfolio_volatility(w, cov) == pytest.approx(expected, abs=1e-9)
