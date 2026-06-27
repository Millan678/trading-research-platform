"""Resource coordinator — advisory resource allocation."""
import hashlib, json, random
from datetime import datetime
from typing import Any, Dict, List, Optional
from .storage import Storage


class ResourceCoordinator:
    def __init__(self, storage: Storage, seed: int = 0):
        self.storage = storage
        self.rng = random.Random(seed)
        self._allocations: Dict[str, dict] = {}

    def allocate(self, resource_id: str, subsystem: str = "core", amount: float = 1.0, seed: int = 0) -> dict:
        rng = random.Random(seed)
        rec = {
            "resource_id": resource_id,
            "subsystem": subsystem,
            "amount": amount,
            "utilization_score": round(rng.random() * 0.3 + 0.5, 4),
            "advisory_only": True,
        }
        self._allocations[resource_id] = rec
        self.storage.append(f"res_{resource_id}", "resource", rec)
        return rec

    def resource_count(self) -> int:
        return len(self._allocations)

    def summary(self, seed: int = 0) -> dict:
        rng = random.Random(seed)
        return {
            "total_resources": self.resource_count(),
            "utilization_efficiency": round(rng.random() * 0.2 + 0.6, 4),
            "advisory_only": True,
        }
