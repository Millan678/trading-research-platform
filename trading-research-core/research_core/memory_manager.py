"""Memory manager — coordinate all memory subsystems."""
import hashlib, json, random
from datetime import datetime
from typing import Any, Dict, List, Optional
from .contracts import MemoryType
from .storage import Storage


class MemoryManager:
    def __init__(self, storage: Storage, seed: int = 0):
        self.storage = storage
        self.rng = random.Random(seed)
        self._memories: Dict[str, dict] = {}
        self._index: Dict[str, List[str]] = {}
        self._consolidations: int = 0

    def store(self, memory_id: str, mtype: str, content: dict, seed: int = 0) -> dict:
        rng = random.Random(seed)
        rec = {
            "memory_id": memory_id,
            "type": mtype,
            "content_hash": hashlib.sha256(json.dumps(content, sort_keys=True, default=str).encode()).hexdigest()[:16],
            "retrievability_score": round(rng.random() * 0.3 + 0.6, 4),
            "provenance": content.get("source", "core"),
            "consolidated": False,
            "created_at": datetime.utcnow().isoformat(),
            "advisory_only": True,
        }
        self._memories[memory_id] = rec
        if mtype not in self._index:
            self._index[mtype] = []
        self._index[mtype].append(memory_id)
        self.storage.append(f"mem_{memory_id}", "memory", rec)
        return rec

    def retrieve(self, memory_id: str) -> Optional[dict]:
        return self._memories.get(memory_id)

    def query_by_type(self, mtype: str) -> List[dict]:
        ids = self._index.get(mtype, [])
        return [self._memories[i] for i in ids if i in self._memories]

    def consolidate(self, seed: int = 0) -> dict:
        rng = random.Random(seed)
        count = 0
        for mid, mem in self._memories.items():
            if not mem.get("consolidated"):
                mem["consolidated"] = True
                count += 1
        self._consolidations += 1
        return {
            "consolidated_count": count,
            "total_consolidations": self._consolidations,
            "memory_health": round(rng.random() * 0.2 + 0.7, 4),
            "advisory_only": True,
        }

    def memory_count(self) -> int:
        return len(self._memories)

    def health(self, seed: int = 0) -> dict:
        rng = random.Random(seed)
        return {
            "total_memories": self.memory_count(),
            "types_indexed": len(self._index),
            "consolidation_events": self._consolidations,
            "memory_health_score": round(rng.random() * 0.2 + 0.7, 4),
            "advisory_only": True,
        }

    def compute_stable_hash(self, seed: int = 0) -> str:
        payload = json.dumps({
            "memories": sorted(self._memories.keys()),
            "seed": seed,
        }, sort_keys=True)
        return "0x" + hashlib.sha256(payload.encode()).hexdigest()
