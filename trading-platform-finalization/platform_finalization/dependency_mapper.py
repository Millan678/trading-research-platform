"""Dependency mapper — map cross-phase dependencies."""
import hashlib, json, random
from datetime import datetime
from typing import Any, Dict, List, Optional
from .storage import Storage


class DependencyMapper:
    def __init__(self, storage: Storage, seed: int = 0):
        self.storage = storage
        self.rng = random.Random(seed)
        self._edges: List[dict] = []

    def map_dependencies(self, phase_count: int = 62, seed: int = 0) -> dict:
        rng = random.Random(seed)
        # Build a sequential dependency chain (P1->P2->...->P62)
        edges = []
        for i in range(1, phase_count):
            edges.append({"from": f"P{i:02d}", "to": f"P{i+1:02d}", "type": "sequential"})
        # Add some cross-dependencies
        for _ in range(10):
            src = rng.randint(1, phase_count)
            tgt = rng.randint(1, phase_count)
            if src != tgt:
                edges.append({"from": f"P{src:02d}", "to": f"P{tgt:02d}", "type": "cross"})
        self._edges = edges
        result = {
            "total_edges": len(edges),
            "sequential": sum(1 for e in edges if e["type"] == "sequential"),
            "cross": sum(1 for e in edges if e["type"] == "cross"),
            "dependency_hash": hashlib.sha256(json.dumps(edges, sort_keys=True, default=str).encode()).hexdigest()[:16],
            "mapped_at": datetime.utcnow().isoformat(),
            "advisory_only": True,
        }
        self.storage.append("dep_map", "dependency_map", result)
        return result

    def summary(self, seed: int = 0) -> dict:
        return self.map_dependencies(seed=seed)
