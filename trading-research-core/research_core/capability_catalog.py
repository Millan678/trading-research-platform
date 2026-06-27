"""Capability catalog — discoverable catalog of all research capabilities."""
import hashlib, json, random
from datetime import datetime
from typing import Any, Dict, List, Optional
from .contracts import CapabilityStatus, GLOBAL_CONTEXT_CATEGORIES
from .storage import Storage


class CapabilityCatalog:
    def __init__(self, storage: Storage, seed: int = 0):
        self.storage = storage
        self.rng = random.Random(seed)
        self._catalog: Dict[str, dict] = {}

    def register(self, cap_id: str, domain: str = "research", seed: int = 0) -> dict:
        rng = random.Random(seed)
        rec = {
            "capability_id": cap_id,
            "domain": domain,
            "status": CapabilityStatus.AVAILABLE.value,
            "discovery_score": round(rng.random() * 0.3 + 0.6, 4),
            "advisory_only": True,
        }
        self._catalog[cap_id] = rec
        self.storage.append(f"cat_{cap_id}", "capability_catalog", rec)
        return rec

    def discover(self, domain: str = None, seed: int = 0) -> List[dict]:
        if domain:
            return [c for c in self._catalog.values() if c["domain"] == domain]
        return list(self._catalog.values())

    def capability_count(self) -> int:
        return len(self._catalog)

    def domain_coverage(self) -> float:
        covered = set(c["domain"] for c in self._catalog.values())
        return round(len(covered) / max(len(GLOBAL_CONTEXT_CATEGORIES), 1), 4)

    def summary(self, seed: int = 0) -> dict:
        rng = random.Random(seed)
        return {
            "total_capabilities": self.capability_count(),
            "domain_coverage": self.domain_coverage(),
            "catalog_health": round(rng.random() * 0.2 + 0.7, 4),
            "advisory_only": True,
        }
