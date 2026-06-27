"""Subsystem registry — register and track all connected subsystems."""
import hashlib, json, random
from datetime import datetime
from typing import Any, Dict, List, Optional
from .contracts import CapabilityStatus
from .storage import Storage


class SubsystemRegistry:
    def __init__(self, storage: Storage, seed: int = 0):
        self.storage = storage
        self.rng = random.Random(seed)
        self._subsystems: Dict[str, dict] = {}

    def register(self, subsys_id: str, version: str = "1.0.0", seed: int = 0) -> dict:
        rng = random.Random(seed)
        rec = {
            "subsystem_id": subsys_id,
            "version": version,
            "status": CapabilityStatus.AVAILABLE.value,
            "health_score": round(rng.random() * 0.3 + 0.6, 4),
            "bridge_type": "read_only",
            "registered_at": datetime.utcnow().isoformat(),
            "advisory_only": True,
        }
        self._subsystems[subsys_id] = rec
        self.storage.append(f"ss_{subsys_id}", "subsystem", rec)
        return rec

    def get_subsystem(self, subsys_id: str) -> Optional[dict]:
        return self._subsystems.get(subsys_id)

    def subsystem_count(self) -> int:
        return len(self._subsystems)

    def active_subsystems(self) -> int:
        return sum(1 for s in self._subsystems.values() if s["status"] == CapabilityStatus.AVAILABLE.value)

    def summary(self, seed: int = 0) -> dict:
        rng = random.Random(seed)
        return {
            "total_subsystems": self.subsystem_count(),
            "active_subsystems": self.active_subsystems(),
            "bridge_integrity": round(rng.random() * 0.2 + 0.7, 4),
            "advisory_only": True,
        }
