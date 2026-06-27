"""Core registry — central index of all subsystems and modules."""
import hashlib, json, random
from datetime import datetime
from typing import Any, Dict, List, Optional
from .contracts import (
    CapabilityStatus, GoalStatus, MemoryType, SyncStatus,
    CONTEXT_DOMAINS, CONSTITUTION_ARTICLES,
)
from .storage import Storage


class CoreRegistry:
    def __init__(self, storage: Storage, seed: int = 0):
        self.storage = storage
        self.rng = random.Random(seed)
        self._subsystems: Dict[str, dict] = {}
        self._capabilities: Dict[str, dict] = {}
        self._modules: Dict[str, dict] = {}

    def register_subsystem(self, name: str, version: str = "1.0.0") -> dict:
        rec = {
            "subsystem_id": name,
            "version": version,
            "registered_at": datetime.utcnow().isoformat(),
            "status": "active",
            "advisory_only": True,
        }
        self._subsystems[name] = rec
        self.storage.append(f"subsys_{name}", "subsystem", rec)
        return rec

    def register_capability(self, cap_id: str, domain: str = "research") -> dict:
        rec = {
            "capability_id": cap_id,
            "domain": domain,
            "status": CapabilityStatus.AVAILABLE.value,
            "advisory_only": True,
        }
        self._capabilities[cap_id] = rec
        self.storage.append(f"cap_{cap_id}", "capability", rec)
        return rec

    def register_module(self, module_id: str, category: str = "core") -> dict:
        rec = {
            "module_id": module_id,
            "category": category,
            "registered_at": datetime.utcnow().isoformat(),
            "advisory_only": True,
        }
        self._modules[module_id] = rec
        self.storage.append(f"mod_{module_id}", "module", rec)
        return rec

    def subsystem_count(self) -> int:
        return len(self._subsystems)

    def capability_count(self) -> int:
        return len(self._capabilities)

    def module_count(self) -> int:
        return len(self._modules)

    def summary(self, seed: int = 0) -> dict:
        rng = random.Random(seed)
        return {
            "total_subsystems": self.subsystem_count(),
            "total_capabilities": self.capability_count(),
            "total_modules": self.module_count(),
            "coverage_score": round(rng.random() * 0.3 + 0.5, 4),
            "advisory_only": True,
        }
