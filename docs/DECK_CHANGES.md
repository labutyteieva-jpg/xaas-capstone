# Deck changes — slides 2, 3, 7 (2026-06-15)

Aligns the pitch deck with the corrected data and the underserved-markets framing. Every figure
below is verified against the source named. Anything that could **not** be verified was removed,
not kept.

## Slide 2 — The Problem
- Headline reworded: "Exporting from Lithuania is broken for small businesses" →
  "Lithuanian SMEs are under-represented in the largest export markets." (The old wording
  overstated the case — exports grew over the long run.)
- The EIB stat "25% report trade disruptions" was **replaced** with "15% of LT exports to the US
  come from SMEs." Reason: the EIB survey data file is not committed and the figure is not
  reproducible; the 15%/51% contrast is computed from the committed Eurostat data.
- "Manufacturing … up to 11% …" (same EIB source) replaced with a verified synthesis line.
- "51% from SMEs" kept (verified, ext_tec10 WORLD basis).
- **Team action:** to use the EIB angle, commit the EIBIS data file and make notebook 02 reproduce
  the figure first.

## Slide 3 — Market Opportunity
- "€54B Lithuanian exports (2024)" was wrong (inflated/SME figure). Top row now shows verified
  stats: 15% (SME share LT–US), 51% (SME share national), -7.5% (export YoY 2024).
- **Removed** the Mordor Intelligence freight-market figures (€49.4B / 19.2% CAGR / $119B):
  paywalled vendor source, not open data, currency-mixed, unverifiable here.
- TAM/SAM/SOM replaced with verified open-data anchors: TAM €36.8B (all LT goods exports,
  Statistics Lithuania), SAM €16.7B (LT SME exports, ext_tec10), SOM €1.5B (US underserved
  headroom, ext_tec10).
- **Team actions / caveats:**
  - These TAM/SAM/SOM are now LT-anchored — far smaller than the old EU-wide €2.1T. If you want a
    larger EU-wide TAM, build it from a citable open source; do **not** reinstate the old unsourced
    numbers.
  - Concept note: a SaaS tool's TAM is really the addressable *spend on export services*, not
    export *value*. The figures use export value as a defensible proxy — flag this if probed.

## Slide 7 — Target Industries
- Removed "Based on UN Comtrade (2023) … 33%/33%/17%/17% … 100% of sampled exports." That was a
  sampling artifact: the committed Comtrade file held only 4 product codes, so "100%" was true
  only of the sample. The €-values (€2.16B etc.) were sums of that 4-code sample.
- Replaced with verified 2024 sector shares (Statistics Lithuania): Mineral products 14.2%,
  Machinery & electrical 13.6%, Chemical industry 11.2%, Furniture 6.9%.
- **Team caveat:** shares 1–3 are HS-section level; furniture is chapter level — mildly
  inconsistent classification. Before the midterm, pull one consistent HS breakdown (full-year
  Comtrade or Statistics Lithuania) to finalise the four tiles.

## Not changed
Slides 1, 4–6, 8–12 untouched. Note that slide 4/6/8 claims (failed-startup funding figures,
business-model percentages) were **not** part of this pass and remain unverified.
