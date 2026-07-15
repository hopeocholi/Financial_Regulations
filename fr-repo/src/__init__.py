"""
Financial Regulations CA1 — quantitative finance library.

First-principles implementations of the models used across the Excel/VBA
workbook and the Python verification notebook. Each function mirrors a
worksheet in the master workbook so that Excel, VBA and Python agree to at
least four decimal places.

Modules
-------
fixed_income   Annuity PV, bond pricing, duration, YTM bisection, mortgages,
               term-structure estimation.
options        Black (1976) futures options and Hull-White (2004) ESO value.
risk           Parametric and historical portfolio VaR and CVaR.
"""

__version__ = "1.0.0"
__author__ = "Hope Eneojo Ocholi"

from .fixed_income import (
    pv_annuity,
    bond_price,
    macaulay_duration,
    modified_duration,
    bisection_ytm,
    mortgage_payment,
    continuous_spot_rate,
)
from .options import (
    black76_call,
    black76_put,
    bsm_call_dividend,
    eso_fair_value,
)
from .risk import (
    parametric_var,
    parametric_cvar,
    historical_var,
    historical_cvar,
)

__all__ = [
    "pv_annuity",
    "bond_price",
    "macaulay_duration",
    "modified_duration",
    "bisection_ytm",
    "mortgage_payment",
    "continuous_spot_rate",
    "black76_call",
    "black76_put",
    "bsm_call_dividend",
    "eso_fair_value",
    "parametric_var",
    "parametric_cvar",
    "historical_var",
    "historical_cvar",
    "__version__",
]
