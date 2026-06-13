"""
fakeface_detector_stub.py — заглушка детектора дипфейков (Студент 6).

НЕ настоящий ML-детектор. Это эвристический стаб, который выдаёт
правдоподобные media_anomalies, чтобы demo работало end-to-end.

Логика:
  - has_face                 берётся из подсказки/метаданных (или эвристики)
  - possible_deepfake        true, если источник помечен как fake (из датасета)
                             или сработали текстовые/медиа-эвристики
  - synthetic_voice_suspected true при признаках TTS/клонированного голоса
  - lip_sync_anomaly         true при подозрении на рассинхрон губ/звука

На MVP большинство решений приходит из метки источника (is_fake_hint)
и простых текстовых эвристик по transcript/combined_text.

Использование как библиотеки:
    from fakeface_detector_stub import analyze_media
    anomalies = analyze_media(is_fake_hint=True, transcript="я инвестировал...")

Использование из CLI (заполняет media_anomalies для строк JSONL):
    python fakeface_detector_stub.py --input SOURCES.md --out deepfake_examples.jsonl
"""

from __future__ import annotations

import argparse
import json
import re
from typing import Optional

# --- Текстовые маркеры -------------------------------------------------------

# Финансовый призыв -> косвенно повышает подозрение в deepfake-промо
FINANCIAL_CTA = [
    "инвестировал", "инвестируй", "переходите по ссылке", "переходи по ссылке",
    "получите доход", "получи доход", "гарантированный доход", "вложи",
    "депозит", "заработок", "прибыль", "вывести прибыль",
]

# Маркеры синтетического голоса (грубые эвристики для стаба)
SYNTHETIC_VOICE_HINTS = [
    "tts", "synthetic", "cloned", "клон", "синтез", "робот",
]


def _contains_any(text: str, needles: list[str]) -> bool:
    low = (text or "").lower()
    return any(n in low for n in needles)


def analyze_media(
    is_fake_hint: Optional[bool] = None,
    transcript: str = "",
    combined_text: str = "",
    has_voice: bool = True,
    has_face_hint: Optional[bool] = None,
    voice_is_tts_hint: Optional[bool] = None,
    lip_sync_hint: Optional[bool] = None,
) -> dict:
    """Вернуть словарь media_anomalies.

    Параметры *_hint — метки из источника/ручной разметки. Если они заданы,
    они имеют приоритет над эвристиками (источник истины — разметчик).
    """
    text = f"{transcript} {combined_text}".strip()

    # has_face: по подсказке, иначе считаем, что у видео-промо лицо обычно есть
    has_face = has_face_hint if has_face_hint is not None else True

    # synthetic voice
    if voice_is_tts_hint is not None:
        synthetic_voice = bool(voice_is_tts_hint and has_voice)
    else:
        synthetic_voice = bool(has_voice and _contains_any(text, SYNTHETIC_VOICE_HINTS))
        # если источник fake и есть голос — поднимаем подозрение
        if is_fake_hint and has_voice:
            synthetic_voice = True

    # lip sync anomaly
    if lip_sync_hint is not None:
        lip_sync = bool(lip_sync_hint)
    else:
        # стаб: рассинхрон коррелирует с синтетическим голосом на лице
        lip_sync = bool(has_face and synthetic_voice)

    # possible deepfake
    if is_fake_hint is not None:
        possible_deepfake = bool(is_fake_hint)
    else:
        possible_deepfake = bool(has_face and (synthetic_voice or lip_sync))

    return {
        "has_face": has_face,
        "possible_deepfake": possible_deepfake,
        "synthetic_voice_suspected": synthetic_voice,
        "lip_sync_anomaly": lip_sync,
    }


def media_risk_signals(anomalies: dict, text: str = "") -> list[str]:
    """Сигналы риска, относящиеся к медиа-аномалиям (для risk_engine)."""
    signals: list[str] = []
    if anomalies.get("possible_deepfake"):
        signals.append("possible_deepfake")
    if anomalies.get("synthetic_voice_suspected"):
        signals.append("synthetic_voice_suspected")
    if anomalies.get("lip_sync_anomaly"):
        signals.append("lip_sync_anomaly")
    if _contains_any(text, FINANCIAL_CTA):
        signals.append("financial_call_to_action")
    return signals


# --- CLI ---------------------------------------------------------------------

_SOURCES_LINE = re.compile(
    r"^\s*(?P<id>\S+)\s*\|\s*(?P<origin>\S+)\s*\|\s*(?P<path>\S+)\s*\|\s*"
    r"(?P<is_fake>true|false)\s*\|\s*(?P<note>.*)$",
    re.IGNORECASE,
)


def _parse_sources(path: str) -> list[dict]:
    """Прочитать SOURCES.md (строки вида: id | origin | path | is_fake | note)."""
    rows: list[dict] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            m = _SOURCES_LINE.match(line)
            if not m:
                continue
            if m.group("id").lower() in {"example_id", "id"}:
                continue  # заголовок
            rows.append({
                "id": m.group("id"),
                "origin": m.group("origin"),
                "path": m.group("path"),
                "is_fake": m.group("is_fake").lower() == "true",
                "note": m.group("note").strip(),
            })
    return rows


def _row_to_record(row: dict) -> dict:
    anomalies = analyze_media(is_fake_hint=row["is_fake"])
    signals = media_risk_signals(anomalies, text=row.get("note", ""))
    label = "scam" if row["is_fake"] else "legit"
    fraud_type = "deepfake_financial_promo" if row["is_fake"] else "legit_finance"
    return {
        "id": row["id"],
        "source": row["origin"],
        "platform": "dataset" if row["origin"] != "synthetic" else "synthetic",
        "modality": "video",
        "case_type": "deepfake_financial_promo",
        "language": "ru",
        "url": row["path"],
        "transcript": "",
        "ocr_text": "",
        "combined_text": row.get("note", ""),
        "entities": {
            "urls": [], "domains": [], "telegram_usernames": [], "phones": [],
            "promo_codes": [], "crypto_wallets": [], "money_amounts": [], "organizations": [],
        },
        "media_anomalies": anomalies,
        "risk_signals": signals,
        "evidence_spans": [],
        "label": label,
        "fraud_type": fraud_type,
        "risk_level": "low",        # пересчитает risk_engine (Студент 7)
        "risk_score": 0,            # пересчитает risk_engine
        "annotator": "student_06",
        "review_status": "draft",   # после ручной проверки -> approved
    }


def main() -> None:
    ap = argparse.ArgumentParser(description="FakeFace stub detector (Student 6)")
    ap.add_argument("--input", required=True, help="SOURCES.md с разметкой источников")
    ap.add_argument("--out", required=True, help="выходной JSONL")
    args = ap.parse_args()

    rows = _parse_sources(args.input)
    if not rows:
        print("[!] Не найдено строк в SOURCES.md (формат: id | origin | path | is_fake | note)")
        return

    with open(args.out, "w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(_row_to_record(row), ensure_ascii=False) + "\n")

    fakes = sum(1 for r in rows if r["is_fake"])
    print(f"[ok] записано {len(rows)} строк -> {args.out} (fake={fakes}, real={len(rows) - fakes})")
    print("[i] media_anomalies — черновые. Проверь руками и выставь review_status=approved.")


if __name__ == "__main__":
    main()
