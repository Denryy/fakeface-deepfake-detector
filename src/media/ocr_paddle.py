"""
ocr_paddle.py — OCR (frame text) via PaddleOCR.

OWNER:  Student 4 (ASR / OCR)
STATUS: SKELETON — interface + contract only. No implementation logic here.
        Student 4 owns the body. Do NOT add business logic in the scaffold.

Responsibility (spec §1.2, §13):
  Extract on-screen text from video frames (site, promo code, Telegram) into
  the `ocr_text` field of the unified record (spec §5).

Inputs:
  - image / frame path(s)
Outputs:
  - data/processed/video_ocr.jsonl   (id -> ocr_text, spec §13)

Contract: produces the `ocr_text` field other modules read (Student 6, 7).
"""

from __future__ import annotations


def ocr_frames(frame_paths: list[str]) -> str:
    """Return concatenated OCR text for a set of frames.

    SKELETON: implementation owned by Student 4. Intentionally not implemented.
    """
    raise NotImplementedError("Student 4 owns the PaddleOCR implementation.")
