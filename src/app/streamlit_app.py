"""
streamlit_app.py — analyst dashboard (UI shell).

OWNER:  Student 8 (Shadow Graph + UI)
STATUS: SKELETON — UI shell only. No widgets, data loading, or business logic.
        Student 8 owns the body. Do NOT implement the dashboard in the scaffold.
        Run target (for Student 8, later): `streamlit run src/app/streamlit_app.py`.

Responsibility (spec §13, §18):
  Render the explainable analyst view for the demo scenarios (§18):
    content -> ASR/OCR -> entities -> risk_signals -> Shadow Graph -> report.

Planned panels (placeholders only):
  1. Upload / select a unified record (data/processed/ai_media_watch_dataset.jsonl).
  2. Show transcript / ocr_text / combined_text.
  3. Show extracted entities (spec §5) and media_anomalies (spec §5, Student 6).
  4. Show triggered risk_signals + risk_score / risk_level (Student 7).
  5. Render the Shadow Graph cluster (Student 8, src/graph).
"""

from __future__ import annotations


def main() -> None:
    """Entry point for the Streamlit dashboard.

    SKELETON: implementation owned by Student 8. Intentionally not implemented.
    """
    raise NotImplementedError("Student 8 owns the Streamlit dashboard implementation.")


if __name__ == "__main__":
    main()
