"""
build_graph.py — Shadow Graph builder (nodes + edges export).

OWNER:  Student 8 (Shadow Graph + UI)
STATUS: SKELETON — interface + contract only. No implementation logic here.
        Student 8 owns the body. Do NOT add graph-building logic in the scaffold.

Responsibility (spec §12, §13):
  Read the unified dataset + extracted entities and emit graph node/edge tables
  following the schema in src/graph/graph_schema.cypher (spec §12).

Inputs:
  - data/processed/ai_media_watch_dataset.jsonl   (unified records, spec §5)
Outputs:
  - data/processed/entities_nodes.csv             (graph nodes — columns owned by Student 8)
  - data/processed/entities_edges.csv             (graph edges — columns owned by Student 8)
"""

from __future__ import annotations


def build_nodes_and_edges(dataset_path: str) -> tuple[list[dict], list[dict]]:
    """Return (nodes, edges) derived from the unified dataset.

    SKELETON: implementation owned by Student 8. Intentionally not implemented.
    """
    raise NotImplementedError("Student 8 owns the Shadow Graph builder implementation.")


def export_csv(nodes: list[dict], edges: list[dict], out_dir: str) -> None:
    """Write nodes/edges to entities_nodes.csv / entities_edges.csv.

    SKELETON: implementation owned by Student 8.
    """
    raise NotImplementedError("Student 8 owns the graph CSV export implementation.")
