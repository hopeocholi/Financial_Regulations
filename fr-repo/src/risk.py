"""
Portfolio risk: parametric and historical Value-at-Risk and Expected Shortfall.

The parametric measures assume normally distributed portfolio returns and scale
one-day volatility to the risk horizon by the square-root-of-time rule. The
historical measures read the empirical return distribution directly. Both are
used in Q6(ii) and cross-checked against the Excel formulas and an R script.
"""

from __future__ import annotations

import numpy as np
from scipy.stats import norm


def portfolio_volatility(weights, cov_matrix):
    """Daily portfolio volatility from weights and a covariance matrix."""
    weights = np.asarray(weights, dtype=float)
    cov = np.asarray(cov_matrix, dtype=float)
    return float(np.sqrt(weights @ cov @ weights))


def parametric_var(portfolio_value, port_vol, port_mean, confidence=0.99, horizon=10):
    """Parametric (variance-covariance) Value-at-Risk over a horizon.

    Uses the normal quantile and square-root-of-time scaling, netting the
    expected drift over the horizon.
    """
    z = norm.ppf(confidence)
    return portfolio_value * (
        z * port_vol * np.sqrt(horizon) - port_mean * horizon
    )


def parametric_cvar(portfolio_value, port_vol, port_mean, confidence=0.99, horizon=10):
    """Parametric Conditional Value-at-Risk (Expected Shortfall).

    Uses the closed-form normal-tail expectation ``phi(z) / (1 - c)``.
    """
    z = norm.ppf(confidence)
    phi_z = norm.pdf(z)
    tail = phi_z / (1 - confidence)
    return portfolio_value * (
        tail * port_vol * np.sqrt(horizon) - port_mean * horizon
    )


def historical_var(port_returns, portfolio_value, confidence=0.99):
    """One-day historical Value-at-Risk from the empirical return series."""
    port_returns = np.asarray(port_returns, dtype=float)
    pct = (1 - confidence) * 100
    return -np.percentile(port_returns, pct) * portfolio_value


def historical_cvar(port_returns, portfolio_value, confidence=0.99):
    """One-day historical Conditional Value-at-Risk (Expected Shortfall)."""
    port_returns = np.asarray(port_returns, dtype=float)
    pct = (1 - confidence) * 100
    threshold = np.percentile(port_returns, pct)
    tail = port_returns[port_returns <= threshold]
    return -tail.mean() * portfolio_value
