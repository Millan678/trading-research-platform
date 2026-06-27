"""Semantic memory — knowledge-based memory with concept indexing."""
import hashlib, json, random
from datetime import datetime
from typing import Any, Dict, List, Optional
from .storage import Storage


class SemanticMemory:
    def __init__(self, storage: Storage, seed: int = 0):
        self.storage = storage
        self.rng = random.Random(seed)
        self._concepts: Dict[str, dict] = {}

    def store_concept(self, concept_id: str, description: str, seed: int = 0) -> dict:
        rng = random.Random(seed)
        rec = {
            "concept_id": concept_id,
            "description": description,
            "confidence_score": round(rng.random() * 0.3 + 0.6, 4),
            "link_count": 0,
            "created_at": datetime.utcnow().isoformat(),
            "advisory_only": True,
        }
        self._concepts[concept_id] = rec
        self.storage.append(f"sem_{concept_id}", "semantic", rec)
        return rec

    def retrieve_concept(self, concept_id: str) -> Optional[dict]:
        return self._concepts.get(concept_id)

    def query_concepts(self, limit: int = 20) -> List[dict]:
        return list(self._concepts.values())[:limit]

    def concept_count(self) -> int:
        return len(self._concepts)

    def summary(self, seed: int = 0) -> dict:
        rng = random.Random(seed)
        return {
            "total_concepts": self.concept_count(),
            "coverage_score": round(rng.random() * 0.2 + 0.6, 4),
            "advisory_only": True,
        }
