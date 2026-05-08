"""Dedup logic: prefer DOI match, fall back to normalized-title match.

When duplicates are found across sources, keep the record with the most
populated abstract (since some sources omit abstracts).
"""
from __future__ import annotations

import re
import unicodedata
from typing import Iterable

from lit.schema import Paper


def _norm_title(t: str) -> str:
    """Strip punctuation, accents, casing for comparison. Empty if title <10 chars."""
    if not t:
        return ""
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode()
    t = re.sub(r"[^a-z0-9\s]+", " ", t.lower())
    t = re.sub(r"\s+", " ", t).strip()
    return t if len(t) >= 10 else ""


def _abstract_score(p: Paper) -> int:
    return len((p.get("abstract") or ""))


def dedupe(papers: Iterable[Paper]) -> list[Paper]:
    by_key: dict[str, Paper] = {}
    order: list[str] = []  # preserve first-seen order

    for p in papers:
        doi = (p.get("doi") or "").strip().lower() or None
        key = f"doi:{doi}" if doi else f"title:{_norm_title(p.get('title', ''))}"
        if not key or key in ("doi:", "title:"):
            # Untitled and no DOI — drop quietly, can't reliably dedupe
            continue
        if key in by_key:
            # Keep the record with the longer abstract; merge sources note
            existing = by_key[key]
            if _abstract_score(p) > _abstract_score(existing):
                p_merged = dict(p)
                p_merged["source"] = f"{existing['source']}+{p['source']}" \
                    if existing["source"] != p["source"] else p["source"]
                # Carry over higher citation_count if existing had one
                if (existing.get("citation_count") or 0) > (p_merged.get("citation_count") or 0):
                    p_merged["citation_count"] = existing.get("citation_count")
                by_key[key] = p_merged  # type: ignore[assignment]
            else:
                if existing["source"] != p["source"] and p["source"] not in existing["source"]:
                    existing["source"] = f"{existing['source']}+{p['source']}"
                if (p.get("citation_count") or 0) > (existing.get("citation_count") or 0):
                    existing["citation_count"] = p.get("citation_count")
        else:
            by_key[key] = dict(p)  # type: ignore[assignment]
            order.append(key)

    return [by_key[k] for k in order]
