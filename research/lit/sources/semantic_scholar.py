"""Semantic Scholar adapter. Free; key bumps you from 100 req/min to 1000 req/min.

Docs: https://api.semanticscholar.org/api-docs/graph#tag/Paper-Data-API/operation/get_graph_paper_relevance_search
"""
from __future__ import annotations

import os
import time

import requests

from lit.schema import Paper

BASE = "https://api.semanticscholar.org/graph/v1/paper/search"
FIELDS = ",".join([
    "title", "abstract", "year", "authors", "venue",
    "externalIds", "citationCount", "openAccessPdf", "url",
])


def search(query: str, year_from: int, year_to: int, max_results: int) -> list[Paper]:
    headers = {}
    if key := os.environ.get("SEMANTIC_SCHOLAR_API_KEY"):
        headers["x-api-key"] = key

    out: list[Paper] = []
    offset = 0
    page_size = 100
    while len(out) < max_results:
        params = {
            "query": query,
            "year": f"{year_from}-{year_to}",
            "limit": min(page_size, max_results - len(out)),
            "offset": offset,
            "fields": FIELDS,
        }
        # SS aggressively throttles unkeyed traffic. Try up to 4 times with
        # exponential backoff on 429.
        resp = None
        for attempt in range(4):
            resp = requests.get(BASE, params=params, headers=headers, timeout=60)
            if resp.status_code != 429:
                break
            time.sleep(2 ** attempt * 3)  # 3, 6, 12, 24 seconds
        if resp is None or resp.status_code == 429:
            print("[semantic_scholar] persistent 429 — set SEMANTIC_SCHOLAR_API_KEY to fix.")
            break
        resp.raise_for_status()
        body = resp.json()
        data = body.get("data", [])
        if not data:
            break
        for p in data:
            ext = p.get("externalIds") or {}
            paper: Paper = {
                "title": p.get("title") or "",
                "authors": [a.get("name", "") for a in (p.get("authors") or [])],
                "year": p.get("year"),
                "abstract": p.get("abstract") or "",
                "doi": ext.get("DOI"),
                "source": "semantic_scholar",
                "url": p.get("url"),
                "citation_count": p.get("citationCount"),
                "venue": p.get("venue"),
                "open_access": bool(p.get("openAccessPdf")),
            }
            out.append(paper)
            if len(out) >= max_results:
                return out
        # Pagination via "next" offset; SS caps total results around 1000
        if "next" not in body:
            break
        offset = body["next"]
        time.sleep(0.5)  # polite default; lower if you have a key
    return out
