# How to tell if a stock is undervalued: 14 years of SEC filings, tested

Code and summary tables for the video **"How to Tell If a Stock Is Undervalued (I Tested 14 Years of Data)"** on [I'm A Doctor Not A Quant](https://www.youtube.com/@ImADoctorNotAQuant).

NVIDIA's P/E is about half its usual level, yet it's more expensive than 80% of US stocks. So which kind of "cheap" actually predicts returns? This repo tests the ratios people use to call a stock undervalued on point-in-time SEC fundamentals for about 900 US stocks a month, July 2012 to September 2026, after trading costs.

**Short answer:** a low ratio tells you a stock is cheap. It doesn't tell you it's undervalued. Over this sample, cheap stocks were no more likely to beat the market than expensive ones, and they carried more risk.

## Key results (v7 run, 171 months, July 2012 – September 2026)

### Cheapest fifth minus most expensive fifth, equal-weighted, after 10 bps per side

| Value measure | Cheap − expensive (%/yr) |
|---|---|
| Earnings yield (inverse P/E) | −2.1 |
| Book-to-price | −3.3 |
| Sales-to-price | +0.7 |
| Free-cash-flow yield | +2.0 |
| EBIT/EV | −2.7 |
| Graham number | −3.7 |
| **Composite (average of 5 ranks)** | **−1.6 (t = −0.3)** |

No measure is statistically different from zero (largest |t| = 1.1; all q ≈ 0.86). The composite weighted by market cap: +1.8%/yr (t = 0.3).

### Did cheap stocks beat the market over the next 12 months?

| Group | Share that beat the US market |
|---|---|
| Cheapest fifth | 43.7% |
| Most expensive fifth | 44.5% |
| All eligible stocks | 44.2% |
| Cheapest vs their own 3-year history | 43.1% |
| Most expensive vs their own history | 43.5% |
| Cheap on both yardsticks | 43.7% |

Cheapest minus most expensive: −0.8 points (t = −0.2). Expensive stocks rose less often (59.7% vs 62.2%), but their winners were bigger (top contributors: TSLA, NVDA, NFLX, AMD, MRNA).

### Risk: cheapest fifth vs the market

| | Cheapest fifth | Market |
|---|---|---|
| Sharpe ratio | 0.58 | 0.91 |
| Beta | 1.20 | 1.00 |
| Max drawdown | −40% | −25% |

Sharpe difference 95% CI: −0.62 to −0.05. Alpha vs a same-beta mix: −4.1%/yr (t = −1.3). FF5 + momentum alpha: −1.4%/yr (t = −1.1).

### Things that didn't rescue value

- **Patience.** Composite EW at 1 / 3 / 6 / 12-month holds: −1.6 / −1.7 / −1.4 / −1.2%/yr. VW: +1.8 / +2.7 / +6.3 (t = 1.1) / +1.4%/yr.
- **Cheap vs its own history** (each ratio vs its own 3-year median): −4.8%/yr monthly (t = −1.5); −2.5% held 12 months (t = −0.9).
- **Piotroski F-score** (8 of 9 signals) within the cheapest third: strong − weak −3.3%/yr (t = −0.8), with a weak group of about 9 stocks a month.
- **Quality** (gross profit / assets) within cheap: high − low −1.4%/yr (t = −0.6).
- **A forecasting model** (walk-forward Fama–MacBeth in the style of Lewellen 2015; 9 signals; trained only on completed years): out-of-sample rank IC −0.021 (t = −0.5) at 12 months. Its top picks beat the market 39.6% of the time vs 41.9% for all stocks. It learned a negative weight on book-to-market (−1.76% per SD) in 2012–2020, just before value recovered.

### The one signal with a pulse

Free-cash-flow yield, cap-weighted, held 12 months: +5.7%/yr (t = 1.5); 6 months +8.6% (t = 1.7). But ranked within industry it's −6.2%/yr (t = −1.2), so most of it is an industry tilt. One of dozens of tests: interesting, not proven.

### Long view (Ken French, book-to-market, cheap 30% − expensive 30%)

+3.9%/yr since 1926 (t = 2.5); −5.6%/yr 2007–2020 (t = −1.5); +7.5%/yr since 2021 (t = 1.1).

Value spread now (B/M, cheapest fifth vs most expensive): 4.9×, about the 59th percentile since 2012.

## Method

- **Fundamentals:** SEC EDGAR XBRL company facts from 10-K and 10-Q filings since 2011. Each number is used as first reported and only from the day after it was filed (no look-ahead). Companies whose company-facts data lagged were filled from the filings' own XBRL.
- **Prices:** Yahoo Finance, adjusted for splits and dividends.
- **Universe each month:** US common stocks over $5, above the NYSE 20th size percentile (no microcaps), at least $1M a day traded, no financials (banks, insurers, BDCs). Median 912 eligible stocks a month.
- **Portfolios:** monthly fifths (quintiles), equal- and value-weighted, 10 bps per side. Holding-period tests use overlapping cohorts with drift.
- **Statistics:** Newey–West t-statistics; Benjamini–Hochberg q-values across the value measures; bootstrap CI for the Sharpe difference.
- **Checks:** the notebook runs 22 consistency checks (all pass in v7). Our own 2×3 HML correlates 0.70 with Ken French's.

## Limits

- **Survivorship.** The stock list is today's listed companies, so firms that went bankrupt or were acquired are missing. Every result is also compared with the average stock in the same list, which removes much of that bias but not all. Ken French's portfolios include delisted firms and give the long history.
- **Many tests.** Dozens of sorts were run. Treat the free-cash-flow result as a hypothesis.
- **Sample.** 14 years, most of it a period when value lagged. This says little about whether value works over a century.

## Repo layout

```
notebook/   undervalued_stocks_v7.ipynb (SEC contact email removed)
tables/     summary tables from the v7 run (CSV)
figures/    charts used in the video (1920 x 1080)
screen/     the Oct 16, 2026 screen and the 24-stock watchlist
```

Raw price and SEC data are not included. The notebook downloads them.

## Running it

```bash
pip install -r requirements.txt
jupyter lab notebook/undervalued_stocks_v7.ipynb
```

Set your own contact email in the SEC `User-Agent` cell first (the SEC requires one). The first run downloads SEC company facts and Yahoo prices for every stock, which takes a while. Later runs use the local cache.

## Sources

- Kenneth R. French Data Library: https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html
- SEC EDGAR XBRL company facts: https://www.sec.gov/edgar/sec-api-documentation
- Fama & French (1992), The Cross-Section of Expected Stock Returns, *Journal of Finance*
- Piotroski (2000), Value Investing: The Use of Historical Financial Statement Information to Separate Winners from Losers, *Journal of Accounting Research*
- Lewellen (2015), The Cross-Section of Expected Stock Returns, *Critical Finance Review*
- Bessembinder (2018), Do Stocks Outperform Treasury Bills?, *Journal of Financial Economics*
- Novy-Marx (2013), The Other Side of Value, *Journal of Financial Economics*
- Greenblatt (2006), *The Little Book That Beats the Market*
- Graham (1949), *The Intelligent Investor*

## Disclaimer

Research and education only. Not financial advice. Past results don't guarantee future returns.
