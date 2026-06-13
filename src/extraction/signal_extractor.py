"""
signal_extractor.py — risk-signal detection.

OWNER:  Student 7 (Entity + Risk)
STATUS: SKELETON — the risk-signal vocabulary is CONTRACT (verbatim spec §9);
        detection logic is owned by Student 7 and intentionally not implemented.
        Do NOT add detection logic in the scaffold.

Responsibility (spec §9, §13):
  Map text + extracted entities + media_anomalies to the `risk_signals` list of
  the unified record (spec §5).

Note: media-anomaly signals (possible_deepfake, synthetic_voice_suspected,
lip_sync_anomaly) are produced upstream by Student 6
(src/media/fakeface_detector_stub.py::media_risk_signals) — consume, do not
recompute them here.
"""

from __future__ import annotations

# --- Full risk-signal vocabulary, verbatim spec §9 (CONTRACT — do not rename) -
RISK_SIGNALS: tuple[str, ...] = (
    "guaranteed_income", "unrealistic_profit", "no_risk_claim", "urgency",
    "limited_slots", "telegram_contact", "whatsapp_contact",
    "direct_message_request", "referral_scheme", "crypto_payment",
    "crypto_wallet_found", "phishing_url", "suspicious_domain", "fake_authority",
    "fake_bank_employee", "fake_government_employee", "fake_egov_call",
    "safe_account", "sms_code_request", "remote_access_request",
    "do_not_tell_anyone", "loan_fear", "account_blocking_fear",
    "personal_data_request", "card_data_request", "egov_1414_code",
    "digital_signature_request", "possible_deepfake", "synthetic_voice_suspected",
    "lip_sync_anomaly", "financial_call_to_action", "illegal_gambling_promo",
    "casino_domain_found", "promo_code_found", "deposit_bonus",
    "registration_instruction", "fake_winner_claim", "money_mule_request",
    "third_party_payment", "p2p_payment", "frequent_requisites_change",
    "only_prepayment", "no_return_policy", "no_merchant_identity", "advance_fee",
    # Кейс-специфичные сигналы из §1.4 / §2.5 / §4.4 / §9.4, которые ОТСУТСТВУЮТ
    # в «Полном списке» §9 ТЗ (внутреннее расхождение ТЗ). Добавлены для полноты
    # контракта — иначе валидные кейс-сигналы выглядят как ошибка разметки.
    "easy_money_claim",            # §1.4 (Кейс 1)
    "psychological_pressure",      # §2.5 (Кейс 2)
    "unknown_investment_platform", # §4.4 (Кейс 4), §9.4 (Кейс 9 — зона Студента 6)
)


def detect_signals(combined_text: str, entities: dict, media_anomalies: dict) -> list[str]:
    """Return the list of triggered risk signals (subset of RISK_SIGNALS).

    SKELETON: implementation owned by Student 7. Intentionally not implemented.
    """
    raise NotImplementedError("Student 7 owns the signal-detection implementation.")
