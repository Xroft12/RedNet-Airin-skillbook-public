from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional
from datetime import datetime, timezone
import json
import uuid


class JsonlMemory:
    """Simple append-only memory for events, decisions and traces."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def append(self, event_type: str, data: Dict[str, Any], tags: Optional[Iterable[str]] = None) -> Dict[str, Any]:
        record = {
            "id": uuid.uuid4().hex,
            "ts": datetime.now(timezone.utc).isoformat(),
            "event_type": event_type,
            "tags": list(tags or []),
            "data": data,
        }
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
        return record

    def load(self) -> List[Dict[str, Any]]:
        if not self.path.exists():
            return []
        items = []
        with self.path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    items.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
        return items

    def search(self, query: str = "", tags: Optional[Iterable[str]] = None, limit: int = 20) -> List[Dict[str, Any]]:
        tagset = set(tags or [])
        q = query.lower().strip()
        results = []
        for item in reversed(self.load()):
            if tagset and not tagset.intersection(set(item.get("tags") or [])):
                continue
            if q and q not in json.dumps(item, ensure_ascii=False).lower():
                continue
            results.append(item)
            if len(results) >= limit:
                break
        return results


@dataclass
class GraphNode:
    id: str
    kind: str
    label: str
    data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class GraphEdge:
    source: str
    target: str
    relation: str
    weight: float = 1.0
    data: Dict[str, Any] = field(default_factory=dict)


class GraphMemory:
    """Tiny in-memory graph for criteria, decisions, skills and branches."""

    def __init__(self) -> None:
        self.nodes: Dict[str, GraphNode] = {}
        self.edges: List[GraphEdge] = []

    def add_node(self, kind: str, label: str, data: Optional[Dict[str, Any]] = None, node_id: Optional[str] = None) -> GraphNode:
        node_id = node_id or uuid.uuid4().hex[:12]
        node = GraphNode(id=node_id, kind=kind, label=label, data=data or {})
        self.nodes[node.id] = node
        return node

    def add_edge(self, source: str, target: str, relation: str, weight: float = 1.0, data: Optional[Dict[str, Any]] = None) -> GraphEdge:
        edge = GraphEdge(source=source, target=target, relation=relation, weight=weight, data=data or {})
        self.edges.append(edge)
        return edge

    def neighbors(self, node_id: str, relation: Optional[str] = None) -> List[GraphNode]:
        ids = []
        for e in self.edges:
            if e.source == node_id and (relation is None or e.relation == relation):
                ids.append(e.target)
            elif e.target == node_id and (relation is None or e.relation == relation):
                ids.append(e.source)
        return [self.nodes[i] for i in ids if i in self.nodes]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "nodes": {k: v.__dict__ for k, v in self.nodes.items()},
            "edges": [e.__dict__ for e in self.edges],
        }


class ProcessTrace:
    """Process trace visible for debugging and audit, not hidden chain-of-thought."""

    def __init__(self) -> None:
        self.events: List[Dict[str, Any]] = []

    def record(self, process: str, note: str, **data: Any) -> Dict[str, Any]:
        event = {
            "id": uuid.uuid4().hex[:12],
            "ts": datetime.now(timezone.utc).isoformat(),
            "process": process,
            "note": note,
            "data": data,
        }
        self.events.append(event)
        return event

    def to_list(self) -> List[Dict[str, Any]]:
        return list(self.events)

    def clear(self) -> None:
        self.events.clear()
