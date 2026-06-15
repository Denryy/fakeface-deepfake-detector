# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

This is **Student 6's** work package inside a larger hackathon project, **Media Fraud Watch + Shadow Graph**. The original scope: a labeled dataset of deepfake/real financial-promo videos plus a heuristic *stub* detector filling `media_anomalies` so the team demo runs end-to-end. It has since grown a **real** ML detector (`fakeface_detector_real.py`, GPU ensemble — see Architecture below), but that is an **MVP, not production**: it uses off-the-shelf models with limited accuracy. Never claim production-grade detection — output is a **risk signal for human review**, not a verdict.

Project language is Russian (README, reports, and dataset `note`/`transcript` fields are in Russian). Code, identifiers, and this file are in English.

## Core design principle (do not violate)

The system never asserts "this is a deepfake" or "person X is a fraudster". It only emits **risk signals** (`possible_deepfake`, `synthetic_voice_suspected`, `lip_sync_anomaly`) with explanations, and defers the decision to a human analyst. Keep this framing in any output, report text, or naming.

Hard constraints from the README's safety rules:
- No deepfakes of real public figures; no real personal data in the repo.
- Heavy video files are **never** committed — only links/IDs/metadata and labels live in git.
- Synthetic examples use neutral/consented faces and TTS voices only.

## Commands

Run the stub detector (parses `SOURCES.md`, writes labeled JSONL):
```bash
python src/media/fakeface_detector_stub.py --input data/raw/deepfake/SOURCES.md --out data/processed/deepfake_examples.jsonl
```

Use as a library:
```python
from src.media.fakeface_detector_stub import analyze_media, media_risk_signals
anomalies = analyze_media(is_fake_hint=True, transcript="я инвестировал...", has_voice=True)
```

Validate that every output line is valid JSON (one JSON object per line):
```bash
python -c "import json,sys; [json.loads(l) for l in open('data/processed/deepfake_examples.jsonl',encoding='utf-8')]"
```

There is no build system, dependency file, or test suite — this is a single-file Python tool plus data and docs. Python standard library only (`argparse`, `json`, `re`).

## Architecture & data flow

A single record flows through several students' tools; Student 6 owns only the media stage:

```
SOURCES.md (id | origin | path | is_fake | note)
  → fakeface_detector_stub.py  → media_anomalies + media risk_signals
  → [ASR/OCR] ASR/Whisper + OCR → transcript / ocr_text   (consumed, not produced here)
  → [entity/risk] entity regex + risk_engine → entities, risk_score, risk_level
  → [Shadow Graph] Shadow Graph (face → video → domain → telegram)
  → one line in deepfake_examples.jsonl
```

`fakeface_detector_stub.py` has three parts:
1. **`analyze_media(...)`** — produces the four `media_anomalies` booleans. Key rule: explicit `*_hint` arguments (from the source label / manual annotation) **always override** the text heuristics — the annotator is the source of truth, the heuristics are only a fallback.
2. **`media_risk_signals(...)`** — maps anomalies + financial-CTA text markers to the risk signal list. It does **not** compute `risk_score`/`risk_level`; those are left at `0`/`"low"` and recomputed downstream by the downstream risk engine.
3. **CLI / `_parse_sources` / `_row_to_record`** — reads the pipe-delimited `SOURCES.md` table (header rows and non-matching lines are skipped) and emits full JSONL records with `review_status: "draft"`.

Beyond the stub there is a **real** detector `fakeface_detector_real.py` that actually analyzes video: OpenCV face detection + an **ensemble of 5 models** for `possible_deepfake` (3 ViT + NPR for generated faces + DFDC EfficientNet-B7 ×7 for face-swap, taking the **max**) and a Wav2Vec2 anti-spoofing model for `synthetic_voice_suspected`. NPR/DFDC architectures are reimplemented as **our own code** in `npr_model.py`/`dfdc_model.py` (weights loaded with `weights_only=True`); their weights are local (`vendor/`, gitignored) — absent → that model is skipped. `detector_server.py` is a small FastAPI web UI for uploading a video. Same `media_anomalies` contract as the stub; runs in a uv venv (`pyproject.toml`).

## Conventions that cross file boundaries

These field values are a contract with the rest of the team — keep them stable:
- `annotator` is always `"student_06"`; `review_status` goes `"draft"` → `"approved"` after manual check.
- `risk_score` thresholds (computed downstream): `0–24 low | 25–49 medium | 50–79 high | 80–100 critical` (sum capped at 100).
- Canonical risk signals for this case: `possible_deepfake (+25)`, `synthetic_voice_suspected (+25)`, `lip_sync_anomaly (+20)`, plus `financial_call_to_action`, `unknown_investment_platform`, `telegram_contact`, `casino_domain_found`.
- The full per-record JSON schema lives in `docs/fakeface_findings.md` and the README "Контракт данных" section — match it exactly when generating or editing records.

The stub only seeds **draft** `media_anomalies`. The README workflow requires every field to be manually reviewed afterward, so do not treat stub output as final ground truth.
