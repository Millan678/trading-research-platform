"""Capability router — route capabilities to subsystems without auto-execution."""
import hashlib, json, random
from datetime import datetime
from typing import Any, Dict, List, Optional
from .contracts import CapabilityStatus
from .storage import Storage


class CapabilityRouter:
    def __init__(self, storage: Storage, seed: int = 0):
        self.storage = storage
        self.rng = random.Random(seed)
        self._caps: Dict[str, dict] = {}

    def register(self, cap_id: str, subsystem: str = "core", seed: int = 0) -> dict:
        rng = random.Random(seed)
        rec = {
            "capability_id": cap_id,
            "subsystem": subsystem,
            "status": CapabilityStatus.AVAILABLE.value,
            "auto_execution": False,
            "auto_approval": False,
            "production_modification": False,
            "advisory_only": True,
        }
        self._caps[cap_id] = rec
        self.storage.append(f"cr_{cap_id}", "capability_route", rec)
        return rec

    def route(self, cap_id: str, seed: int = 0) -> dict:
        rng = random.Random(seed)
        cap = self._caps.get(cap_id)
        if not cap:
            return {"routed": False, "reason": "capability_not_found", "advisory_only": True}
        return {
            "routed": True,
            "capability_id": cap_id,
            "subsystem": cap["subsystem"],
            "execution_approved": False,
            "requires_manual_review": True,
            "advisory_only": True,
        }

    def capability_count(self) -> int:
        return len(self._caps)

    def summary(self, seed: int = 0) -> dict:
        rng = random.Random(seed)
        return {
            "total_capabilities": self.capability_count(),
            "routing_coverage": round(rng.random() * 0.2 + 0.7, 4),
            "advisory_only": True,
        }
