"""
regex_extractors.py — entity extraction patterns.

OWNER:  Student 7 (Entity + Risk)
STATUS: SKELETON — patterns are CONTRACT (verbatim spec §10); extraction
        FUNCTIONS are owned by Student 7 and intentionally not implemented.
        Do NOT add extraction logic in the scaffold.

Responsibility (spec §10, §13):
  Extract entities (urls, domains, telegram_usernames, phones, promo_codes,
  crypto_wallets, money_amounts, organizations) into the `entities` object of
  the unified record (spec §5).
"""

from __future__ import annotations

# --- Regex patterns defined verbatim by spec §10 (CONTRACT — do not alter) ----
PATTERNS: dict[str, str] = {
    "telegram_username": r"@[A-Za-z0-9_]{5,32}",
    "url": r"https?:\/\/[^\s]+|www\.[^\s]+",
    "phone_kz": r"(\+7|8)\s?\(?7\d{2}\)?\s?\d{3}[-\s]?\d{2}[-\s]?\d{2}",
    "money_amount": r"\d[\d\s]{2,}\s?(₸|тг|тенге|KZT|USDT|\$)",
    "promo_code": r"(?i)(промокод|promo|код)\s*[:\-]?\s*([A-Z0-9]{4,20})",
    "crypto_keywords": r"USDT|BTC|ETH|TRC20|ERC20|BEP20|крипта|биткоин|эфир|майнинг",
    "btc_address": r"\b(bc1|[13])[a-zA-HJ-NP-Z0-9]{25,39}\b",
    "eth_address": r"0x[a-fA-F0-9]{40}",
}

# Keys of the unified `entities` object (spec §5 — do not rename):
ENTITY_KEYS = (
    "urls", "domains", "telegram_usernames", "phones",
    "promo_codes", "crypto_wallets", "money_amounts", "organizations",
)


def extract_entities(text: str) -> dict:
    """Extract the unified `entities` object from `combined_text`.

    SKELETON: implementation owned by Student 7. Intentionally not implemented.
    Returns an object keyed by ENTITY_KEYS (spec §5).
    """
    raise NotImplementedError("Student 7 owns the entity-extraction implementation.")
