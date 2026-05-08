"""Scopus Search API adapter.

Requires ELSEVIER_API_KEY. Returns [] with a notice when unset.
Note: Elsevier ToS restricts caching abstracts beyond 24h; the pipeline treats
Scopus results as transient (re-fetched each run).

Docs: https://dev.elsevier.com/documentation/SCOPUSSearchAPI.wadl
"""
from __future__ import annotations

import os
import time

import requests

from lit.schema import Paper

BASE = "https://api.elsevier.com/content/search/scopus"


def search(query: str, year_from: int, year_to: int, max_results: int) -> list[Paper]:
    key = os.environ.get("ELSEVIER_API_KEY")
    if not key:
        print("[scopus] ELSEVIER_API_KEY not set — skipping. "
              "Apply at https://dev.elsevier.com.")
        return []

    headers = {"X-ELS-APIKey": key, "Accept": "application/json"}
    # Scopus query syntax: TITLE-ABS-KEY for full-text-relevant search
    scopus_q = f"TITLE-ABS-KEY({query}) AND PUBYEAR > {year_from - 1} AND PUBYEAR < {year_to + 1} AND LANGUAGE(english)"
    out: list[Paper] = []
    start = 0
    page_size = 25  # Scopus default; max 200 with right subscription tier

    while len(out) < max_results:
        params = {
            "query": scopus_q,
            "count": min(page_size, max_results - len(out)),
            "start": start,
            "view": "STANDARD",
        }
        resp = requests.get(BASE, params=params, headers=headers, timeout=60)
        if resp.status_code == 429:
            time.sleep(5)
            resp = requests.get(BASE, params=params, headers=headers, timeout=60)
        if resp.status_code != 200:
            print(f"[scopus] HTTP {resp.status_code}: {resp.text[:200]}")
            break
        body = resp.json()
        entries = body.get("search-results", {}).get("entry", [])
        if not entries:
            break
        for e in entries:
            authors_raw = e.get("dc:creator") or ""
            paper: Paper = {
                "title": e.get("dc:title") or "",
                "authors": [authors_raw] if authors_raw else [],
                "year": int(e["prism:coverDate"][:4]) if e.get("prism:coverDate") else None,
                "abstract": e.get("dc:description") or "",
                "doi": e.get("prism:doi"),
                "source": "scopus",
                "url": next((l["@href"] for l in e.get("link", []) if l.get("@ref") == "scopus"), None),
                "citation_count": int(e.get("citedby-count") or 0),
                "venue": e.get("prism:publicationName"),
                "open_access": e.get("openaccess") == "1",
            }
            out.append(paper)
            if len(out) >= max_results:
                return out
        start += len(entries)
        # Stop if we've exhausted the result set
        total = int(body.get("search-results", {}).get("opensearch:totalResults", 0))
        if start >= total:
            break
        time.sleep(0.3)
    return out
