"""
Option-pricing models: Black (1976) futures options and Hull-White (2004) ESOs.

The Black (1976) functions price European options on a bond futures contract.
The employee-stock-option (ESO) valuation follows the Hull-White adjustment:
a Black-Scholes-Merton value under a continuous dividend yield, scaled by the
probability of surviving the vesting period. All mirror the VBA UDFs in the
workbook (``Black76Call``, ``BlackScholesCall``, ``ESOFairValue``).
"""

from __future__ import annotations

from math import exp, log, sqrt

from scipy.stats import norm


def black76_call(F, K, r, T, sigma):
    """Black (1976) European call on a futures price ``F``."""
    d1 = (log(F / K) + 0.5 * sigma ** 2 * T) / (sigma * sqrt(T))
    d2 = d1 - sigma * sqrt(T)
    return exp(-r * T) * (F * norm.cdf(d1) - K * norm.cdf(d2))


def black76_put(F, K, r, T, sigma):
    """Black (1976) European put on a futures price ``F``."""
    d1 = (log(F / K) + 0.5 * sigma ** 2 * T) / (sigma * sqrt(T))
    d2 = d1 - sigma * sqrt(T)
    return exp(-r * T) * (K * norm.cdf(-d2) - F * norm.cdf(-d1))


def bsm_call_dividend(S, K, r, q, sigma, T):
    """Black-Scholes-Merton European call with a continuous dividend yield."""
    d1 = (log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * sqrt(T))
    d2 = d1 - sigma * sqrt(T)
    return S * exp(-q * T) * norm.cdf(d1) - K * exp(-r * T) * norm.cdf(d2)


def eso_fair_value(S, K, r, q, sigma, expected_life, vesting_years, forfeiture_rate):
    """Hull-White (2004) employee-stock-option fair value.

    Applies the survival probability over the vesting period to a
    Black-Scholes-Merton value computed at the expected exercise life rather
    than the contractual maturity.

    Returns
    -------
    tuple[float, float, float]
        (eso_value, black_scholes_value, survival_probability).
    """
    survival = (1 - forfeiture_rate) ** vesting_years
    bs_val = bsm_call_dividend(S, K, r, q, sigma, expected_life)
    return survival * bs_val, bs_val, survival
