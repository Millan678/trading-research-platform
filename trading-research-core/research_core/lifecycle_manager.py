"""Lifecycle manager — track component and subsystem lifecycles."""
import hashlib, json, random
from datetime import datetime
from typing import Any, Dict, List, Optional
from .storage import Storage

LIFECYCLE_STAGES = ["initialization", "active", "maintenance", "degraded", "retired"]


class LifecycleManager:
    def __init__(self, storage: Storage, seed: int = 0):
        self.storage = storage
        self.rng = random.Random(seed)
        self._components: Dict[str, dict] = {}

    def register_component(self, comp_id: str, stage: str = "initialization", seed: int = 0) -> dict:
        rng = random.Random(seed)
        rec = {
            "component_id": comp_id,
            "lifecycle_stage": stage,
            "health_score": round(rng.random() * 0.3 + 0.6, 4),
            "uptime_score": round(rng.random() * 0.2 + 0.8, 4),
            "advisory_only": True,
        }
        self._components[comp_id] = rec
        self.storage.append(f"lc_{comp_id}", "lifecycle", rec)
        return rec

    def transition_stage(self, comp_id: str, new_stage: str, seed: int = 0) -> dict:
        comp = self._components.get(comp_id)
        if not comp:
            return {"transitioned": False, "reason": "not_found", "advisory_only": True}
        old = comp["lifecycle_stage"]
        comp["lifecycle_stage"] = new_stage
        return {"transitioned": True, "from": old, "to": new_stage, "advisory_only": True}

    def component_count(self) -> int:
        return len(self._components)

    def active_components(self) -> int:
        return sum(1 for c in self._components.values() if c["lifecycle_stage"] == "active")

    def summary(self, seed: int = 0) -> dict:
        rng = random.Random(seed)
        return {
            "total_components": self.component_count(),
            "active_components": self.active_components(),
            "lifecycle_stability": round(rng.random() * 0.2 + 0.7, 4),
            "advisory_only": True,
        }
