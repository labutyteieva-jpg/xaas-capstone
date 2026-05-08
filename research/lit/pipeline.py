"""Orchestrator: call every source adapter, normalize, dedupe, return DataFrame.

Usage:
    from lit.pipeline import run_search
    df = run_search(query, year_from=2015, year_to=2025, max_per_source=200)
"""
from __future__ import annotations

import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import pandas as pd

from lit.dedupe import dedupe
from lit.schema import Paper
from lit.sources import openalex, semantic_scholar, core, scopus, sciencedirect


@dataclass
class SourceResult:
    name: str
    raw_count: int
    elapsed_s: float
    error: str | None = None


SOURCES: dict[str, Callable[..., list[Paper]]] = {
    "openalex":      openalex.search,
    "semantic_scholar": semantic_scholar.search,
    "core":          core.search,
    "scopus":        scopus.search,
    "sciencedirect": sciencedirect.search,
}


def run_search(
    query: str,
    year_from: int = 2015,
    year_to: int = 2025,
    max_per_source: int = 500,
    sources: list[str] | None = None,
) -> tuple[pd.DataFrame, list[SourceResult]]:
    """Run search across requested sources and return (deduped DataFrame, per-source stats)."""
    use = sources or list(SOURCES.keys())
    all_papers: list[Paper] = []
    stats: list[SourceResult] = []

    for name in use:
        fn = SOURCES[name]
        t0 = time.time()
        try:
            results = fn(query, year_from, year_to, max_per_source)
            stats.append(SourceResult(name=name, raw_count=len(results),
                                       elapsed_s=round(time.time() - t0, 1)))
            all_papers.extend(results)
        except Exception as e:
            stats.append(SourceResult(name=name, raw_count=0,
                                       elapsed_s=round(time.time() - t0, 1),
                                       error=f"{type(e).__name__}: {e}"))

    deduped = dedupe(all_papers)
    df = pd.DataFrame(deduped)
    if len(df):
        df = df.sort_values(by=["citation_count", "year"],
                             ascending=[False, False], na_position="last").reset_index(drop=True)
    return df, stats


def save_csv(df: pd.DataFrame, path: str | Path) -> None:
    """Save with list-typed columns flattened to '|'-joined strings (CSV-friendly)."""
    out = df.copy()
    if "authors" in out.columns:
        out["authors"] = out["authors"].apply(
            lambda xs: "|".join(xs) if isinstance(xs, list) else (xs or "")
        )
    out.to_csv(path, index=False)
