"""Procedural memory — skill and procedure-based memory."""
import hashlib, json, random
from datetime import datetime
from typing import Any, Dict, List, Optional
from .storage import Storage


class ProceduralMemory:
    def __init__(self, storage: Storage, seed: int = 0):
        self.storage = storage
        self.rng = random.Random(seed)
        self._procedures: Dict[str, dict] = {}

    def store_procedure(self, proc_id: str, steps: List[str], seed: int = 0) -> dict:
        rng = random.Random(seed)
        rec = {
            "procedure_id": proc_id,
            "step_count": len(steps),
            "steps": steps,
            "mastery_score": round(rng.random() * 0.3 + 0.5, 4),
            "execution_count": 0,
            "created_at": datetime.utcnow().isoformat(),
            "advisory_only": True,
        }
        self._procedures[proc_id] = rec
        self.storage.append(f"proc_{proc_id}", "procedural", rec)
        return rec

    def retrieve_procedure(self, proc_id: str) -> Optional[dict]:
        return self._procedures.get(proc_id)

    def query_procedures(self, limit: int = 20) -> List[dict]:
        return list(self._procedures.values())[:limit]

    def procedure_count(self) -> int:
        return len(self._procedures)

    def summary(self, seed: int = 0) -> dict:
        rng = random.Random(seed)
        return {
            "total_procedures": self.procedure_count(),
            "mastery_avg": round(rng.random() * 0.2 + 0.6, 4),
            "advisory_only": True,
        }
