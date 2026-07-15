# Model notes

This note documents each model, its parameters, and the Excel-Python reconciliation.

## Q5(i) Present value of an annuity

Ordinary annuity and annuity due. Parameters: payment €1,250, nominal annual rate 6.4%, 12 years, quarterly. The due value equals the ordinary value times `(1 + r/freq)`, a check the notebook prints explicitly. Reconciles at €41,658.67.

## Q5(ii) Bond pricing and duration

A 7-year, 5.8% semi-annual coupon bond priced at a 6.2% yield. Reports price (€977.56), Macaulay duration (5.8360 years), modified duration (5.6605 years) and DV01. Includes a Hopewell & Kaufman (1973) duration table across coupon and maturity combinations, illustrating that duration lengthens as the coupon falls because more weight sits on the final principal.

## Q5(iii) Yield to maturity by bisection

Solves for the yield that reprices a bond quoted at €978.40 (4.75% coupon, 6 years). The bisection loop is reproduced as a full iteration table so the convergence path can be checked against Excel row by row. Converges to about 5.1734%.

## Q5(iv) Mortgage repayment

A €335,000 loan at 4.65% over 25 years, monthly. The level payment is €1,890.68. The amortisation schedule shows the interest share falling and the principal share rising over the life of the loan, and supports an optional prepayment.

## Q5(v) Term structure

Continuously compounded spot rates recovered from discount factors as `-ln(DF) / T`, fitted with a straight line, with implied forward rates between consecutive maturities. The 10-year spot rate is 4.2251%.

## Q6(i) Black (1976)

European options on a bond futures contract: futures 108.20, strike 107.00, 3.25% rate, 0.75 years, 17% volatility. Call €6.7652, put €5.5941, satisfying put-call parity `C - P = e^(-rT)(F - K)` to machine precision.

## Q6(ii) Portfolio VaR and CVaR

A €2,500,000 equally weighted portfolio of ten stocks (AMZN, CCL, MARA, NFLX, NIO, NOK, NVDA, RIG, SNAP, U) over one year of daily log returns. Parametric measures assume normal returns and scale one-day volatility by the square root of the ten-day horizon; historical measures read the empirical tail. An R script provides a third, independent check. The parametric 10-day 99% VaR is about €317,773 and CVaR about €367,855 on the snapshot used.

## Q6(iii) Employee stock options

Hull-White (2004) fair value: a Black-Scholes-Merton value at the expected exercise life (6.5 years), scaled by the probability of surviving the 3-year vesting period at a 3.5% annual forfeiture rate. Parameters: share €42, strike €40, rate 3.1%, dividend yield 1.2%, volatility 34%.

### Reconciliation note

The Black-Scholes-Merton component is €15.2899, matching Excel exactly. The survival scaling is `(1 - 0.035)^3 = 0.898632`, so the ESO fair value is `0.898632 x 15.2899 = 13.7400`. The notebook's summary table quotes €13.7659 for this row, which does not follow from the same survival convention; the Python library follows the documented function and returns €13.7400. This is the only figure in the cross-verification table that does not reconcile to four decimal places, and the discrepancy is in the summary cell rather than the model.
