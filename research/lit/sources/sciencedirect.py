"""ScienceDirect Search API adapter.

Requires ELSEVIER_API_KEY. Returns [] with a notice when unset.
Docs: https://dev.elsevier.com/documentation/ScienceDirectSearchAPI.wadl
"""
from __future__ import annotations

import os
import time

import requests

from lit.schema import Paper

BASE = "https://api.elsevier.com/content/search/sciencedirect"


def search(query: str, year_from: int, year_to: int, max_results: int) -> list[Paper]:
    key = os.environ.get("ELSEVIER_API_KEY")
    if not key:
        print("[sciencedirect] ELSEVIER_API_KEY not set — skipping. "
              "Same key as Scopus; apply at https://dev.elsevier.com.")
        return []

    headers = {"X-ELS-APIKey": key, "Accept": "application/json"}
    out: list[Paper] = []
    offset = 0
    page_size = 100  # ScienceDirect PUT search supports up to 100

    while len(out) < max_results:
        body = {
            "qs": query,
            "date": f"{year_from}-{year_to}",
            "display": {"offset": offset, "show": min(page_size, max_results - len(out))},
            "filters": {"openAccess": False},  # mix of OA + paywall
        }
        resp = requests.put(BASE, json=body, headers=headers, timeout=60)
        if resp.status_code == 429:
            time.sleep(5)
            resp = requests.put(BASE, json=body, headers=headers, timeout=60)
        if resp.status_code != 200:
            print(f"[sciencedirect] HTTP {resp.status_code}: {resp.text[:200]}")
            break
        data = resp.json()
        results = data.get("results") or []
        if not results:
            break
        for r in results:
            authors = [a.get("name", "") for a in (r.get("authors") or [])]
            paper: Paper = {
                "title": r.get("title") or "",
                "authors": authors,
                "year": int(r["publicationDate"][:4]) if r.get("publicationDate") else None,
                "abstract": "",  # ScienceDirect search response does not include abstracts;
                                  # fetch via Article Retrieval API per-DOI if needed.
                "doi": r.get("doi"),
                "source": "sciencedirect",
                "url": (r.get("uri") or {}).get("self"),
                "citation_count": None,  # not exposed on search endpoint
                "venue": r.get("sourceTitle"),
                "open_access": r.get("openAccess"),
            }
            out.append(paper)
            if len(out) >= max_results:
                return out
        offset += len(results)
        time.sleep(0.3)
    return out
