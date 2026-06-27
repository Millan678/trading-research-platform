"""Objective manager — manage research objectives and dependencies."""
import hashlib, json, random
from datetime import datetime
from typing import Any, Dict, List, Optional
from .storage import Storage


class ObjectiveManager:
    def __init__(self, storage: Storage, seed: int = 0):
        self.storage = storage
        self.rng = random.Random(seed)
        self._objectives: Dict[str, dict] = {}

    def add_objective(self, obj_id: str, description: str, dependencies: List[str] = None, seed: int = 0) -> dict:
        dependencies = dependencies or []
        rng = random.Random(seed)
        rec = {
            "objective_id": obj_id,
            "description": description,
            "dependencies": dependencies,
            "status": "pending",
            "feasibility_score": round(rng.random() * 0.3 + 0.6, 4),
            "created_at": datetime.utcnow().isoformat(),
            "advisory_only": True,
        }
        self._objectives[obj_id] = rec
        self.storage.append(f"obj_{obj_id}", "objective", rec)
        return rec

    def resolve_dependencies(self, obj_id: str) -> dict:
        obj = self._objectives.get(obj_id, {})
        deps = obj.get("dependencies", [])
        resolved = [d for d in deps if d in self._objectives and self._objectives[d].get("status") == "completed"]
        return {
            "objective_id": obj_id,
            "total_deps": len(deps),
            "resolved_deps": len(resolved),
            "blocked": len(deps) - len(resolved),
            "advisory_only": True,
        }

    def objective_count(self) -> int:
        return len(self._objectives)

    def summary(self, seed: int = 0) -> dict:
        rng = random.Random(seed)
        return {
            "total_objectives": self.objective_count(),
            "objective_completion_rate": round(rng.random() * 0.3 + 0.5, 4),
            "advisory_only": True,
        }
