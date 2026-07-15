# Data

The portfolio-risk task (Q6(ii)) uses one year of daily adjusted-close prices
for ten tickers: AMZN, CCL, MARA, NFLX, NIO, NOK, NVDA, RIG, SNAP, U.

The prices and their daily log returns are embedded in the workbook sheets
`Data_From_Collab` and `Q6_ii_RawData`. To regenerate them:

```python
import yfinance as yf, numpy as np
tickers = ['AMZN','CCL','MARA','NFLX','NIO','NOK','NVDA','RIG','SNAP','U']
data = yf.download(tickers, start='2023-05-25', end='2024-05-25', auto_adjust=True)
prices = data['Close'][tickers].dropna()
log_returns = np.log(prices).diff().dropna()
log_returns.to_excel('data/daily_log_returns.xlsx')
```

Exported files land here and are git-ignored because they are reproducible.
