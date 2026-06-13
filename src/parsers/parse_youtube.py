"""
parse_youtube.py — YouTube / Shorts metadata parser.

OWNER:  Student 1 (YouTube / Shorts)
STATUS: SKELETON — interface + contract only. No implementation logic here.
        Student 1 owns the body. Do NOT add business logic in the scaffold.

Responsibility (spec §1.3, §13):
  Collect video metadata for gambling / investment / crypto queries via the
  YouTube Data API `search.list` (or a manual fallback), then emit cleaned rows.

Inputs:
  - Search queries — see docs/youtube_search_queries.md (spec §1.3).
Outputs:
  - data/raw/youtube/*.csv                       (raw search.list rows)
  - data/processed/youtube_candidates_clean.jsonl (unified schema, spec §5)

Downstream contract: every emitted record MUST conform to the unified JSONL
record in the project spec §5.
"""

from __future__ import annotations

# Raw CSV columns defined verbatim by spec §1.3 (CONTRACT — do not rename):
RAW_CSV_COLUMNS = [
    "source", "platform", "query", "video_id", "url",
    "title", "description", "channel_title", "published_at", "thumbnail_url",
]


def search_youtube(query: str, *, max_results: int = 50) -> list[dict]:
    """Call YouTube Data API `search.list` for one query and return raw rows.

    SKELETON: implementation owned by Student 1. Intentionally not implemented.
    """
    raise NotImplementedError("Student 1 owns the YouTube search implementation.")


def to_unified_records(raw_rows: list[dict]) -> list[dict]:
    """Map raw YouTube rows to unified §5 JSONL records.

    SKELETON: implementation owned by Student 1.
    """
    raise NotImplementedError("Student 1 owns the YouTube normalization implementation.")
