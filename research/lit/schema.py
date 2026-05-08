"""Normalized Paper schema returned by every source adapter."""
from typing import TypedDict


class Paper(TypedDict, total=False):
    title: str
    authors: list[str]
    year: int | None
    abstract: str
    doi: str | None
    source: str            # 'openalex' | 'semantic_scholar' | 'core' | 'scopus' | 'sciencedirect'
    url: str | None
    citation_count: int | None
    venue: str | None      # journal/conference name
    open_access: bool | None


REQUIRED_FIELDS = ("title", "authors", "year", "abstract", "source")
