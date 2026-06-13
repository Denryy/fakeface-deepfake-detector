"""
parse_telegram_export.py — Telegram export / posts parser.

OWNER:  Student 2 (Telegram / posts)
STATUS: SKELETON — interface + contract only. No implementation logic here.
        Student 2 owns the body. Do NOT add business logic in the scaffold.

Responsibility (spec §3.3, §13):
  Ingest a Telegram export (or a ready Telegram dataset such as "Telegram Spam
  or Ham"), filter to relevant financial / scam examples, and emit unified rows.

Safety (spec §0): NEVER parse private chats; use only own/open test channels or
public datasets. Store only masked/hashed requisites.

Inputs:
  - data/raw/telegram/*                            (export or dataset dump)
Outputs:
  - data/processed/telegram_messages.jsonl         (unified schema, spec §5)
"""

from __future__ import annotations


def load_export(path: str) -> list[dict]:
    """Load a Telegram export / dataset file into raw message dicts.

    SKELETON: implementation owned by Student 2. Intentionally not implemented.
    """
    raise NotImplementedError("Student 2 owns the Telegram export loader.")


def to_unified_records(raw_messages: list[dict]) -> list[dict]:
    """Map raw Telegram messages to unified §5 JSONL records.

    SKELETON: implementation owned by Student 2.
    """
    raise NotImplementedError("Student 2 owns the Telegram normalization implementation.")
