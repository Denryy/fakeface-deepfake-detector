"""
asr_whisper.py — ASR (speech-to-text) via Whisper.

OWNER:  Student 4 (ASR / OCR)
STATUS: SKELETON — interface + contract only. No implementation logic here.
        Student 4 owns the body. Do NOT add business logic in the scaffold.

Responsibility (spec §2.2, §13):
  Transcribe audio / extracted video audio into `transcript` text consumed by
  the unified record (spec §5) and by Student 6's FakeFace stub.

Inputs:
  - audio file path (.wav / extracted from video)
Outputs:
  - data/processed/audio_transcripts.jsonl   (id -> transcript, spec §13)

Contract: produces the `transcript` field other modules read (Student 6, 7).
"""

from __future__ import annotations


def transcribe(audio_path: str, *, language: str | None = None) -> str:
    """Return the transcript for one audio file.

    SKELETON: implementation owned by Student 4. Intentionally not implemented.
    """
    raise NotImplementedError("Student 4 owns the Whisper ASR implementation.")
