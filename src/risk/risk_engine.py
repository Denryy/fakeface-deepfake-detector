"""
risk_engine.py — risk scoring and level assignment.

OWNER:  Student 7 (Entity + Risk)
STATUS: SKELETON — the score weights and thresholds are CONTRACT (verbatim spec
        §11 / §8); the scoring FUNCTION is owned by Student 7 and intentionally
        not implemented. Do NOT add the scoring algorithm in the scaffold.

Responsibility (spec §8, §11, §13):
  Compute `risk_score` (0–100, capped) and `risk_level` for a unified record
  from its `risk_signals` (and graph reuse). Student 6's stub leaves
  risk_score=0 / risk_level="low" for this engine to recompute (see CLAUDE.md).

Result framing (spec §0): risk scoring only — never a legal accusation.
"""

from __future__ import annotations

# --- Per-signal score weights, verbatim spec §11 (CONTRACT — do not alter) -----
SCORE_WEIGHTS: dict[str, int] = {
    "casino_domain_found": 25,
    "promo_code_found": 20,
    "registration_instruction": 20,
    "fake_winner_claim": 20,
    "sms_code_request": 45,
    "fake_government_employee": 30,
    "safe_account": 45,
    "do_not_tell_anyone": 30,
    "remote_access_request": 45,
    "guaranteed_income": 25,
    "referral_scheme": 25,
    "phishing_url": 40,
    "crypto_wallet_found": 20,
    "possible_deepfake": 25,
    "synthetic_voice_suspected": 25,
    "lip_sync_anomaly": 20,
    "graph_entity_reuse": 25,
}

# Score is capped at this maximum (spec §11):
SCORE_CAP = 100

# --- risk_level thresholds, verbatim spec §11 (CONTRACT — do not alter) ---------
# 0–24 low | 25–49 medium | 50–79 high | 80–100 critical
RISK_THRESHOLDS: tuple[tuple[int, str], ...] = (
    (0, "low"),
    (25, "medium"),
    (50, "high"),
    (80, "critical"),
)


def compute_risk(risk_signals: list[str], *, graph_entity_reuse: bool = False) -> dict:
    """Return {"risk_score": int, "risk_level": str} for a record.

    SKELETON: implementation owned by Student 7. Intentionally not implemented.
    """
    raise NotImplementedError("Student 7 owns the risk-scoring implementation.")
