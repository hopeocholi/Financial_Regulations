# Workbook guide

`workbook/H9FR2_CA1_models.xlsm` is a macro-enabled Excel workbook. Because it
contains VBA, your spreadsheet application will ask you to enable content when
you open it. The macros are custom finance functions only; there is no
auto-run code.

## Sheets

| Sheet | Purpose |
|---|---|
| `Menu` | Navigation and workbook overview. |
| `Colab_Links` | Links to the matching Python verification for each task. |
| `Q5_i_Annuity` | Annuity present value with rate and tenor sensitivity. |
| `Q5_ii_Bond_Duration` | Bond price, Macaulay and modified duration. |
| `Q5_iii_YTM` | Bisection yield-to-maturity with a convergence table. |
| `Q5_iv_Mortgage` | Mortgage payment and amortisation schedule. |
| `Q5_v_TermStructure` | Spot rates from discount factors and a linear fit. |
| `Q6_i_Black76` | Black (1976) option on a bond futures contract. |
| `Data_From_Collab` | Adjusted close prices downloaded for the risk task. |
| `Q6_ii_RawData` | Daily log returns for the ten-stock portfolio. |
| `Q6_ii_VaR_CVaR` | Portfolio covariance, VaR and CVaR. |
| `Q6_iii_ESO` | Employee stock option fair value and sensitivity. |

## Custom VBA functions

The workbook defines user-defined functions that can be called from any cell:

| Function | Signature |
|---|---|
| `PVAnnuity` | `(Pmt, AnnualRate, Years, PayPerYear, DueFlag)` |
| `BondPrice` | `(Face, CouponRate, YTM, Years, Freq)` |
| `BondDuration` | `(Face, CouponRate, YTM, Years, Freq)` |
| `YTMBisection` | `(Face, CouponRate, Price, Years, Freq)` |
| `MortgagePayment` | `(Principal, AnnualRate, Years, PayPerYear)` |
| `ContSpotRate` | `(DiscountFactor, Maturity)` |
| `Black76Call` | `(F, K, r, T, sigma)` |
| `BlackScholesCall` | `(S, K, r, q, sigma, T)` |
| `ESOFairValue` | `(S, K, r, q, sigma, ExpectedLife, VestingYears, ForfeitRate)` |

Each function has a direct Python counterpart in `src/`, which is how the
cross-verification in the README is produced.

## Viewing the macros without Excel

The VBA source can be extracted on any platform with `oletools`:

```bash
pip install oletools
olevba workbook/H9FR2_CA1_models.xlsm
```
