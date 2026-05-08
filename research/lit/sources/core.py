"""CORE API adapter. Free key required (https://core.ac.uk/services/api).

Skips silently with a notice if CORE_API_KEY is unset.
Docs: https://api.core.ac.uk/docs/v3
"""
from __future__ import annotations

import os
import time

import requests

from lit.schema import Paper

BASE = "https://api.core.ac.uk/v3/search/works"


def search(query: str, year_from: int, year_to: int, max_results: int) -> list[Paper]:
    key = os.environ.get("CORE_API_KEY")
    if not key:
        print("[core] CORE_API_KEY not set — skipping (free key from core.ac.uk).")
        return []

    headers = {"Authorization": f"Bearer {key}"}
    out: list[Paper] = []
    offset = 0
    page_size = 100
    # CORE supports a Lucene-style query; restrict by year range and language
    full_q = f"({query}) AND yearPublished>={year_from} AND yearPublished<={year_to} AND language.code:en"

    while len(out) < max_results:
        params = {
            "q": full_q,
            "limit": min(page_size, max_results - len(out)),
            "offset": offset,
        }
        resp = requests.get(BASE, params=params, headers=headers, timeout=60)
        if resp.status_code == 429:
            time.sleep(5)
            resp = requests.get(BASE, params=params, headers=headers, timeout=60)
        resp.raise_for_status()
        body = resp.json()
        results = body.get("results") or []
        if not results:
            break
        for w in results:
            authors = [a.get("name", "") for a in (w.get("authors") or [])]
            paper: Paper = {
                "title": w.get("title") or "",
                "authors": authors,
                "year": w.get("yearPublished"),
                "abstract": w.get("abstract") or "",
                "doi": w.get("doi"),
                "source": "core",
                "url": w.get("downloadUrl") or w.get("sourceFulltextUrls", [None])[0],
                "citation_count": w.get("citationCount"),
                "venue": (w.get("publisher") or w.get("journals", [{}])[0].get("title") if w.get("journals") else None),
                "open_access": True,  # CORE indexes OA full text
            }
            out.append(paper)
            if len(out) >= max_results:
                return out
        offset += page_size
        if offset >= body.get("totalHits", 0):
            break
        time.sleep(0.3)
    return out
