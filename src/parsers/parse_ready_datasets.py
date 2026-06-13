"""
parse_ready_datasets.py — ready-made dataset normalizer.

OWNER:  Student 3 (Ready datasets)
STATUS: SKELETON — interface + contract only. No implementation logic here.
        Student 3 owns the body. Do NOT add business logic in the scaffold.

Responsibility (spec §3.3, §13):
  Normalize public datasets — ScamSpot, ealvaradob/phishing-dataset,
  CryptoScamDB, "Telegram Spam or Ham" — into unified rows.

Inputs:
  - data/raw/scamspot/*, data/raw/phishing/*, data/raw/crypto/*   (raw dumps)
Outputs:
  - data/processed/ready_dataset_examples.jsonl    (unified schema, spec §5)
  - docs/dataset_sources.md                        (provenance write-up)

See docs/dataset_sources.md for source licensing / access notes (spec §3.3).
"""

from __future__ import annotations

# Source identifiers expected in the unified `source` field (spec §3.3, §5):
KNOWN_SOURCES = ("scamspot", "phishing_dataset", "cryptoscamdb", "telegram_spam_or_ham")


def load_dataset(source: str, path: str) -> list[dict]:
    """Load one ready dataset by `source` id into raw rows.

    SKELETON: implementation owned by Student 3. Intentionally not implemented.
    """
    raise NotImplementedError("Student 3 owns the ready-dataset loaders.")


def to_unified_records(source: str, raw_rows: list[dict]) -> list[dict]:
    """Map raw dataset rows to unified §5 JSONL records.

    SKELETON: implementation owned by Student 3.
    """
    raise NotImplementedError("Student 3 owns the ready-dataset normalization.")
