"""
Fixed-income models: annuities, bonds, duration, YTM, mortgages, term structure.

Every function is written from first principles to mirror the corresponding
worksheet and VBA user-defined function in the master workbook. Defaults match
the parameter values used in the assessment so the numbers reconcile exactly.
"""

from __future__ import annotations

import numpy as np


def pv_annuity(payment, annual_rate, years, freq, due=False):
    """Present value of an ordinary annuity or an annuity due.

    Parameters
    ----------
    payment : float
        Periodic payment amount.
    annual_rate : float
        Nominal annual discount rate.
    years : float
        Number of years.
    freq : int
        Payments per year.
    due : bool
        True for an annuity due (payments at period start), False for ordinary.

    Returns
    -------
    float
        Present value. Mirrors the VBA ``PVAnnuity`` UDF.
    """
    r = annual_rate / freq
    n = years * freq
    if r == 0:
        pv_ord = payment * n
    else:
        pv_ord = payment * (1 - (1 + r) ** (-n)) / r
    return pv_ord * (1 + r) if due else pv_ord


def bond_price(face, coupon_rate, ytm, years, freq=2):
    """Price a coupon bond by discounting its cash flows.

    Mirrors the VBA ``BondPrice`` UDF: level coupons plus face at maturity,
    each discounted at the per-period yield.
    """
    n = int(round(years * freq))
    c = face * coupon_rate / freq
    r = ytm / freq
    price = sum(c / (1 + r) ** t for t in range(1, n + 1))
    price += face / (1 + r) ** n
    return price


def macaulay_duration(face, coupon_rate, ytm, years, freq=2):
    """Macaulay duration in years (cash-flow-time-weighted present value)."""
    n = int(round(years * freq))
    c = face * coupon_rate / freq
    r = ytm / freq
    px = bond_price(face, coupon_rate, ytm, years, freq)
    weighted = sum((t / freq) * c / (1 + r) ** t for t in range(1, n + 1))
    weighted += years * face / (1 + r) ** n
    return weighted / px


def modified_duration(face, coupon_rate, ytm, years, freq=2):
    """Modified duration: Macaulay duration divided by (1 + y/freq)."""
    mac = macaulay_duration(face, coupon_rate, ytm, years, freq)
    return mac / (1 + ytm / freq)


def bisection_ytm(
    face,
    coupon_rate,
    market_price,
    years,
    freq=2,
    low=0.01,
    high=0.15,
    tol=1e-8,
    max_iter=30,
):
    """Yield to maturity by bisection.

    Mirrors the VBA ``YTMBisection`` routine. Returns the converged yield and
    the full iteration table so the convergence can be audited against Excel.

    Returns
    -------
    tuple[float, list]
        (converged_ytm, iterations) where each iteration row is
        ``[i, low, high, mid, price_at_mid, error, decision]``.
    """
    iterations = []
    mid = (low + high) / 2
    for i in range(1, max_iter + 1):
        mid = (low + high) / 2
        price_mid = bond_price(face, coupon_rate, mid, years, freq)
        error = price_mid - market_price
        if abs(error) < tol:
            decision = "Converged"
        elif error > 0:
            decision = "Low=Mid"
        else:
            decision = "High=Mid"
        iterations.append([i, low, high, mid, price_mid, error, decision])
        if abs(error) < tol:
            break
        if error > 0:
            low = mid
        else:
            high = mid
    return mid, iterations


def mortgage_payment(principal, annual_rate, years, freq=12):
    """Level mortgage payment (standard amortising loan formula).

    Mirrors the VBA ``MortgagePayment`` UDF.
    """
    r = annual_rate / freq
    n = years * freq
    return principal * r * (1 + r) ** n / ((1 + r) ** n - 1)


def amortization_schedule(principal, annual_rate, years, freq=12, extra=0.0):
    """Full amortisation schedule as a list of period dictionaries.

    Each row records the payment, the interest and principal split, any extra
    prepayment, and the remaining balance.
    """
    r = annual_rate / freq
    n = int(years * freq)
    pmt = mortgage_payment(principal, annual_rate, years, freq)
    balance = principal
    rows = []
    for period in range(1, n + 1):
        interest = balance * r
        principal_paid = pmt - interest + extra
        principal_paid = min(principal_paid, balance)
        balance -= principal_paid
        rows.append(
            {
                "period": period,
                "payment": pmt + extra,
                "interest": interest,
                "principal": principal_paid,
                "balance": max(balance, 0.0),
            }
        )
        if balance <= 0:
            break
    return rows


def continuous_spot_rate(discount_factor, maturity):
    """Continuously compounded spot rate from a discount factor.

    Mirrors the VBA ``ContSpotRate`` UDF: ``-ln(DF) / T``.
    """
    return -np.log(discount_factor) / maturity


def fit_term_structure(maturities, discount_factors):
    """Estimate a linear term structure of continuously compounded spot rates.

    Returns
    -------
    dict
        ``spot_rates``, ``slope``, ``intercept``, ``fitted`` and the forward
        rates implied between consecutive maturities.
    """
    maturities = np.asarray(maturities, dtype=float)
    discount_factors = np.asarray(discount_factors, dtype=float)
    spot_rates = -np.log(discount_factors) / maturities
    slope, intercept = np.polyfit(maturities, spot_rates, 1)
    fitted = intercept + slope * maturities

    forwards = []
    for i in range(len(maturities) - 1):
        f = (
            spot_rates[i + 1] * maturities[i + 1]
            - spot_rates[i] * maturities[i]
        ) / (maturities[i + 1] - maturities[i])
        forwards.append(f)

    return {
        "spot_rates": spot_rates,
        "slope": float(slope),
        "intercept": float(intercept),
        "fitted": fitted,
        "forward_rates": forwards,
    }
