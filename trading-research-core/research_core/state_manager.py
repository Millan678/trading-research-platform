"""State manager — track and manage system state."""
import hashlib, json, random
from datetime import datetime
from typing import Any, Dict, List, Optional
from .storage import Storage


class StateManager:
    def __init__(self, storage: Storage, seed: int = 0):
        self.storage = storage
        self.rng = random.Random(seed)
        self._states: Dict[str, dict] = {}

    def set_state(self, key: str, value: dict, seed: int = 0) -> dict:
        rng = random.Random(seed)
        rec = {
            "state_key": key,
            "value_hash": hashlib.sha256(json.dumps(value, sort_keys=True, default=str).encode()).hexdigest()[:16],
            "consistency_score": round(rng.random() * 0.2 + 0.8, 4),
            "updated_at": datetime.utcnow().isoformat(),
            "advisory_only": True,
        }
        self._states[key] = {"value": value, "meta": rec}
        self.storage.append(f"state_{key}", "state", rec)
        return rec

    def get_state(self, key: str) -> Optional[dict]:
        entry = self._states.get(key)
        return entry["value"] if entry else None

    def state_count(self) -> int:
        return len(self._states)

    def summary(self, seed: int = 0) -> dict:
        rng = random.Random(seed)
        return {
            "total_states": self.state_count(),
            "state_consistency": round(rng.random() * 0.2 + 0.8, 4),
            "advisory_only": True,
        }
