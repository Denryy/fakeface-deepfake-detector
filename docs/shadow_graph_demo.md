# Shadow Graph Demo

> OWNER: Student 8 (Shadow Graph + UI). SKELETON.
> Schema is verbatim from `the project spec §12`
> (see `src/graph/graph_schema.cypher`). Demo flow from spec §18.

## What the graph must do (spec §12.3)
1. Same domain across different videos.
2. Same Telegram handle across different posts.
3. Same promo code across different bloggers.
4. Same wallet across different sources.
5. Render the cluster: `blogger → video → site → telegram → risk_signal`.

## Export contract
`src/graph/build_graph.py` reads `data/processed/ai_media_watch_dataset.jsonl`
(spec §5) and writes `data/processed/entities_nodes.csv` /
`entities_edges.csv`. CSV column layout is Student 8's to finalize (kept empty
in the scaffold) and should map onto the §12 node labels / relationship types.

## Demo scenarios (spec §18)
- Демо 1 — blogger advertises online casino: video → Whisper/OCR → entities →
  Risk Engine HIGH/CRITICAL → graph `blogger → video → casino domain → promo`.
- Демо 2 — eGov → КНБ → safe-account call: audio → transcript → stage split →
  `sms_code_request`, `fake_authority`, `safe_account`, `do_not_tell_anyone` → critical.
- Демо 3 — deepfake financial promo: video → FakeFace `possible_deepfake`
  (Student 6) → ASR/OCR financial CTA → entities → `possible_deepfake +
  financial_call_to_action` = high/critical.

## TODO (Student 8)
- [ ] Finalize node/edge CSV columns.
- [ ] Streamlit panels (`src/app/streamlit_app.py`).
