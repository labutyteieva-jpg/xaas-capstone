"""OpenAlex adapter. Free, no key required; pass an email for the polite pool.

Docs: https://docs.openalex.org/api-entities/works/search-works
"""
from __future__ import annotations

import os
import time
from typing import Iterator

import requests

from lit.schema import Paper

BASE = "https://api.openalex.org/works"


def _reconstruct_abstract(inverted: dict | None) -> str:
    """OpenAlex returns inverted-index abstracts to comply with copyright. Reverse."""
    if not inverted:
        return ""
    positions: list[tuple[int, str]] = []
    for word, idxs in inverted.items():
        for i in idxs:
            positions.append((i, word))
    positions.sort()
    return " ".join(w for _, w in positions)


def _iter_pages(query: str, year_from: int, year_to: int, mailto: str | None) -> Iterator[dict]:
    cursor = "*"
    while cursor:
        params = {
            "search": query,
            "filter": f"from_publication_date:{year_from}-01-01,"
                       f"to_publication_date:{year_to}-12-31,"
                       f"language:en",
            "per-page": 200,
            "cursor": cursor,
        }
        if mailto:
            params["mailto"] = mailto
        resp = requests.get(BASE, params=params, timeout=60)
        resp.raise_for_status()
        body = resp.json()
        yield body
        cursor = body.get("meta", {}).get("next_cursor")
        if not cursor:
            return
        time.sleep(0.1)  # polite


def search(query: str, year_from: int, year_to: int, max_results: int) -> list[Paper]:
    mailto = os.environ.get("OPENALEX_EMAIL") or None
    out: list[Paper] = []
    for page in _iter_pages(query, year_from, year_to, mailto):
        for w in page.get("results", []):
            authors = [a["author"]["display_name"]
                       for a in w.get("authorships", [])
                       if a.get("author", {}).get("display_name")]
            paper: Paper = {
                "title": w.get("title") or "",
                "authors": authors,
                "year": w.get("publication_year"),
                "abstract": _reconstruct_abstract(w.get("abstract_inverted_index")),
                "doi": (w.get("doi") or "").replace("https://doi.org/", "") or None,
                "source": "openalex",
                "url": w.get("doi") or w.get("id"),
                "citation_count": w.get("cited_by_count"),
                "venue": (w.get("primary_location") or {}).get("source", {}).get("display_name"),
                "open_access": (w.get("open_access") or {}).get("is_oa"),
            }
            out.append(paper)
            if len(out) >= max_results:
                return out
    return out
