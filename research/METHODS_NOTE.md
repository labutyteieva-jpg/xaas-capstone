# Methods note — Eurostat `ext_tec10` aggregation correction

**Date:** 2026-06-15
**Affects:** `research/notebooks/01_eurostat_trade_analysis.ipynb` and the charts in `research/reports/`.

## What was wrong

The earlier version of notebook 01 computed Lithuania's national export totals by summing the
`TOTAL` enterprise-size class across **every** `partner` row in `ext_tec10`. That dataset stores,
as separate rows, the `WORLD` aggregate, regional aggregates (EU27, etc.) **and** each individual
partner country. Summing them together multi-counts the same trade.

| Quantity (2024, exports) | Earlier (sum over all partners) | Corrected (partner = `WORLD`) |
|---|---|---|
| LT total exports | EUR 105.8 bn | **EUR 32.5 bn** |
| Inflation factor | — | 3.26× |

The inflated total propagated into the SME-share denominator and into the pitch deck
("€54B Lithuanian exports (2024)").

## Correction rules applied

1. **National totals** use `partner == 'WORLD'` only — never a sum across partners.
2. **Per-market** figures use individual ISO-2 partners, excluding all aggregates
   (`WORLD`, `EU27_2020`, `EA*`, `EFTA`).
3. The national SME-share benchmark used for the underserved-markets comparison is the
   clean WORLD figure (**51.5%**, 2024), stated explicitly on every chart.

## Important caveat to state in the midterm

`ext_tec10` is *Trade by enterprise characteristics (TEC)*. It covers only trade that can be
attributed to enterprises by size class, so its `WORLD` total **under-counts** relative to
Lithuania's headline goods-export figure. The corrected TEC total (~EUR 32.5 bn, 2024) is the
right basis for the **by-size and by-market decomposition**, but it is **not** the headline
national export figure. For the latter, cite **Eurostat Comext** or **Statistics Lithuania**.
(The commonly cited ~EUR 40 bn national figure is *unverified in this repo* and must be confirmed
against Comext before use.)

## Corrected headline findings

- **Trend (context):** TEC-covered exports peaked at EUR 36.8 bn (2022), then fell to
  EUR 32.9 bn (2023, −10.5%) and EUR 32.5 bn (2024, −1.4%). Long-run (2015→2024) exports still
  roughly doubled from EUR 18.1 bn. Both the recent decline and the long-run growth must be shown.
- **SME participation:** SMEs are ~51% of LT exports (2024, WORLD basis); broadly stable, not
  declining. The earlier "54.1% → 46.6% decline" used the multi-counted denominator and does not
  reproduce.
- **Underserved markets (headline):** In large, distant markets SMEs are far below the 51.5%
  benchmark. The United States is the standout — SME share 15.3% on ~EUR 1.74 bn of LT exports,
  with large firms supplying ~EUR 1.47 bn; the gap has persisted across 2015–2024.

## Stale artifacts still in `research/reports/` (regenerate or remove in a follow-up commit)

These reflect the **old** methodology and should not be reused until rebuilt on the corrected basis:
`lt_export_growth.png` (uses 2019 base, hides post-2022 decline),
`lt_sme_gap_trend.png`, `lt_sme_gap_trend_clean.png`, `lt_underserved_markets_clean.png`
(carry the 54.1%→46.6% / 46.6%-benchmark figures),
`lt_sme_destinations.png`, `lt_market_diversification.png` (not yet re-derived on WORLD basis).
