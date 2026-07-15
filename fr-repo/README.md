# Financial Regulations: Quantitative Models and Regulatory Analysis

A three-part MSc FinTech submission pairing a written analysis of EU financial regulation with a fully cross-verified quantitative toolkit implemented three ways: Excel/VBA, Python, and an R check.

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Excel VBA](https://img.shields.io/badge/Excel-VBA%20UDFs-217346)
![Tests](https://img.shields.io/badge/tests-pytest-green)
![Cross--verified](https://img.shields.io/badge/Excel%E2%86%94Python-4dp%20match-brightgreen)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

Author: **Hope Eneojo Ocholi**

---

## Overview

The project has two halves that reinforce each other.

**A regulatory analysis** ([`report/`](report/)) covering four themes: the evolution of bank capital regulation from Basel I to Basel III and Solvency II (CRD IV, CRR, ICAAP); securitization and credit derivatives and their role in the financial crisis; the post-crisis architecture for OTC derivatives (EMIR, MiFID II/MiFIR, CCPs); and the EU AI Act as applied to high-risk credit-scoring systems.

**A quantitative toolkit** ([`src/`](src/), [`workbook/`](workbook/), [`notebooks/`](notebooks/)) implementing eight finance models from first principles. Every model is computed independently in Excel formulas, custom VBA functions, and Python, and the three agree to at least four decimal places.

## Cross-verification results

Every quantitative task is computed in Excel/VBA and again in Python. The two implementations reconcile to at least four decimal places.

| Model | Excel value | Python value | Match |
|---|---|---|---|
| Q5(i) Annuity present value | €41,658.67 | €41,658.67 | ✓ |
| Q5(ii) Bond price | €977.56 | €977.56 | ✓ |
| Q5(ii) Macaulay duration | 5.8360 yrs | 5.8360 yrs | ✓ |
| Q5(ii) Modified duration | 5.6605 yrs | 5.6605 yrs | ✓ |
| Q5(iii) Converged YTM | 5.1742% | 5.1734% | ✓ |
| Q5(iv) Monthly mortgage payment | €1,890.68 | €1,890.68 | ✓ |
| Q5(v) 10-year spot rate | 4.2251% | 4.2251% | ✓ |
| Q6(i) Black-76 call | €6.7652 | €6.7652 | ✓ |
| Q6(i) Black-76 put | €5.5941 | €5.5941 | ✓ |
| Q6(ii) 10-day VaR (99%) | €317,773.14 | €317,773.14 | ✓ |
| Q6(ii) 10-day CVaR (99%) | €367,854.88 | €367,854.88 | ✓ |
| Q6(iii) Black-Scholes value | €15.2899 | €15.2899 | ✓ |

![Bond price-yield curve](figures/bond_price_yield.png)

![Term structure](figures/term_structure.png)

## The models

Eight models span fixed income, options and portfolio risk. Each is a first-principles implementation with a matching VBA user-defined function in the workbook.

- **Present value of an annuity** — ordinary and annuity-due, with rate and tenor sensitivity.
- **Bond pricing and duration** — Macaulay and modified duration, DV01, and a Hopewell & Kaufman (1973) duration-table replication.
- **Yield to maturity** — solved by bisection with a full auditable convergence table.
- **Mortgage repayment** — level-payment amortisation with prepayment and rate sensitivity.
- **Term structure** — continuously compounded spot rates from discount factors, a linear fit, and implied forward rates.
- **Black (1976)** — European options on a bond futures contract, with put-call parity check.
- **Portfolio VaR and CVaR** — parametric and historical, on one year of real returns for a ten-stock portfolio.
- **Employee stock options** — Hull-White (2004) fair value with vesting-survival scaling.

![Mortgage amortisation](figures/mortgage_amortization.png)

## Repository layout

```
.
├── src/                     # First-principles Python library (tested)
│   ├── fixed_income.py      # Annuity, bond, duration, YTM, mortgage, term structure
│   ├── options.py           # Black (1976) and Hull-White ESO valuation
│   └── risk.py              # Parametric and historical VaR / CVaR
├── notebooks/               # Python verification notebook (mirrors every sheet)
├── workbook/                # Excel/VBA master workbook (.xlsm, macros enabled)
├── report/                  # Written regulatory analysis (Word)
├── figures/                 # Summary charts generated from the models
├── tests/                   # pytest cross-verification suite (18 tests)
├── data/                    # Placeholder for exported return data
├── docs/                    # Model notes and workbook guide
├── requirements.txt
└── README.md
```

## Quickstart

```bash
git clone https://github.com/<your-username>/financial-regulations-quant.git
cd financial-regulations-quant

python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# run the cross-verification tests
pytest -q

# open the verification notebook
jupyter lab notebooks/H9FR2_CA1_verification.ipynb
```

### Using the library directly

```python
from src.fixed_income import bond_price, macaulay_duration, bisection_ytm
from src.options import black76_call
from src.risk import parametric_var

bond_price(face=1000, coupon_rate=0.058, ytm=0.062, years=7, freq=2)   # 977.56
macaulay_duration(1000, 0.058, 0.062, 7, 2)                            # 5.8360
black76_call(F=108.20, K=107.00, r=0.0325, T=0.75, sigma=0.17)         # 6.7652
```

## The Excel/VBA workbook

`workbook/H9FR2_CA1_models.xlsm` contains one sheet per task plus a navigation menu, and a set of custom VBA functions (`PVAnnuity`, `BondPrice`, `BondDuration`, `YTMBisection`, `MortgagePayment`, `ContSpotRate`, `Black76Call`, `BlackScholesCall`, `ESOFairValue`). Because it carries macros, your spreadsheet application will prompt to enable content on open. See [`docs/WORKBOOK.md`](docs/WORKBOOK.md) for the sheet-by-sheet guide.

## Notes and honest caveats

The Python library reproduces the workbook's VBA functions faithfully. One figure in the notebook's own summary table (the Q6(iii) ESO fair value) is quoted as €13.7659, whereas the documented Hull-White survival scaling `(1 - 0.035)^3` applied to the €15.2899 Black-Scholes value yields €13.7400; the library follows the function, and this reconciliation is recorded in [`docs/MODELS.md`](docs/MODELS.md). The portfolio-risk figures depend on a one-year snapshot of daily returns for ten named tickers, so re-downloading fresh data will shift the VaR and CVaR slightly.

## License

Code is released under the MIT License. See [`LICENSE`](LICENSE). The written report is the author's academic work and is included for portfolio reference.
