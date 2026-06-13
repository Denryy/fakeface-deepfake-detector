# Annotation Guideline (shared)

> SKELETON — coordination doc for all students. Contracts below are **verbatim
> references** to `the project spec`. Do not redesign them here;
> this file only collects the rules annotators must follow.

## Unified record schema
Every labeled row MUST conform to the unified JSONL record in **spec §5**
(`data/processed/ai_media_watch_dataset.jsonl`). Each student first writes to
their own `data/processed/*.jsonl`, then rows are merged into the unified file.

## Labels (spec §6)
| label | When |
|---|---|
| `legit` | normal content, official warning, educational video |
| `spam` | mass advertising without clear fraud |
| `scam` | signs of deception, pressure, phishing, pyramid, fake authority |
| `unclear` | not enough data — needs manual review |

## fraud_type (spec §7)
`illegal_gambling_promo`, `fake_egov_delivery_call`, `fake_bank_call`,
`fake_government_call`, `investment_scam`, `crypto_scam`, `phishing`,
`money_mule_or_drop`, `fake_seller`, `fake_credit`, `deepfake_financial_promo`,
`legit_finance`, `anti_fraud_education`, `ordinary_spam`.

## risk_level (spec §8) and risk_score (spec §11)
`0–24 low | 25–49 medium | 50–79 high | 80–100 critical` (capped at 100).
`risk_score` / `risk_level` are computed by Student 7's `risk_engine.py` — do
not hand-assign final scores; annotators set signals/evidence.

## risk_signals (spec §9)
Use only names from the canonical list in **spec §9** (also enumerated in
`src/extraction/signal_extractor.py::RISK_SIGNALS`).

## Workflow fields
- `annotator`: `student_01` … `student_08` (Student 6 uses `student_06`).
- `review_status`: `draft` → `approved` after self-check.

## Safety (spec §0)
Risk scoring only — never a legal accusation. No real card numbers / ИИН /
SMS codes / passwords / CVV / ЭЦП. Store only masked or hashed requisites.
