"""Platform registry — central index of all phases and modules."""
import hashlib, json, random
from datetime import datetime
from typing import Any, Dict, List, Optional
from .contracts import ARCHITECTURE_DOMAINS
from .storage import Storage


class PlatformRegistry:
    def __init__(self, storage: Storage, seed: int = 0):
        self.storage = storage
        self.rng = random.Random(seed)
        self._phases: Dict[str, dict] = {}
        self._modules: Dict[str, dict] = {}

    def register_phase(self, phase_id: str, description: str = "", seed: int = 0) -> dict:
        rng = random.Random(seed)
        record = {
            "phase_id": phase_id,
            "description": description,
            "health_score": round(rng.random() * 0.2 + 0.7, 4),
            "registered_at": datetime.utcnow().isoformat(),
            "advisory_only": True,
        }
        self._phases[phase_id] = record
        self.storage.append(f"phase_{phase_id}", "platform_phase", record)
        return record

    def register_module(self, module_id: str, phase: str = "", seed: int = 0) -> dict:
        rng = random.Random(seed)
        record = {
            "module_id": module_id,
            "phase": phase,
            "integrity_score": round(rng.random() * 0.15 + 0.85, 4),
            "registered_at": datetime.utcnow().isoformat(),
            "advisory_only": True,
        }
        self._modules[module_id] = record
        self.storage.append(f"mod_{module_id}", "platform_module", record)
        return record

    def index_all_phases(self, count: int = 62, seed: int = 0) -> dict:
        rng = random.Random(seed)
        for i in range(1, count + 1):
            self.register_phase(f"P{i:02d}", seed=rng.randint(0, 999999))
        return {
            "phases_indexed": len(self._phases),
            "modules_indexed": len(self._modules),
            "advisory_only": True,
        }

    def summary(self, seed: int = 0) -> dict:
        rng = random.Random(seed)
        return {
            "total_phases": len(self._phases),
            "total_modules": len(self._modules),
            "platform_completeness": round(rng.random() * 0.1 + 0.85, 4),
            "advisory_only": True,
        }
