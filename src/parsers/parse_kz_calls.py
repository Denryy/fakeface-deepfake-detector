"""
parse_kz_calls.py — KZ synthetic-call script / transcript parser.

OWNER:  Student 5 (KZ calls)
STATUS: SKELETON — interface + contract only. No implementation logic here.
        Student 5 owns the body. Do NOT add business logic in the scaffold.

Responsibility (spec §2.3, §13):
  Turn synthetic eGov / КНБ / bank call scripts (based on official warnings)
  into unified rows. Real victim recordings are forbidden (spec §0, §2.3).

Inputs:
  - data/raw/kz_calls/kz_call_scripts.csv          (authored scripts)
  - data/raw/kz_calls/*.wav                        (TTS / volunteer audio, optional)
Outputs:
  - data/processed/kz_call_transcripts.jsonl       (unified schema, spec §5)

See docs/kz_call_scenarios.md for the scenario stages and keyword lists (§2.4).
"""

from __future__ import annotations

# Call scenario stages defined by spec §2.2 (CONTRACT — do not rename):
CALL_STAGES = (
    "egov_delivery",      # 1. доставка / eGov
    "sms_code",           # 2. SMS-код
    "fake_authority",     # 3. КНБ / полиция / Нацбанк
    "loan_threat",        # 4. кредит / угроза
    "safe_account",       # 5. безопасный счёт / перевод
)


def load_scripts(path: str) -> list[dict]:
    """Load authored call scripts (CSV) into raw dicts.

    SKELETON: implementation owned by Student 5. Intentionally not implemented.
    """
    raise NotImplementedError("Student 5 owns the KZ call-script loader.")


def to_unified_records(scripts: list[dict]) -> list[dict]:
    """Map call scripts / transcripts to unified §5 JSONL records.

    SKELETON: implementation owned by Student 5.
    """
    raise NotImplementedError("Student 5 owns the KZ call normalization implementation.")
