"""Recommendation engine — advisory-only recommendations for research."""
import hashlib, json, random
from datetime import datetime
from typing import Any, Dict, List, Optional
from .storage import Storage

RECOMMENDATION_TYPES = [
    "research_direction", "methodology", "review_priority",
    "resource_allocation", "collaboration", "risk_mitigation",
]


class RecommendationEngine:
    def __init__(self, storage: Storage, seed: int = 0):
        self.storage = storage
        self.rng = random.Random(seed)
        self._recommendations: Dict[str, dict] = {}

    def generate(self, rec_id: str, rtype: str = "research_direction", seed: int = 0) -> dict:
        rng = random.Random(seed)
        rec = {
            "recommendation_id": rec_id,
            "type": rtype,
            "confidence": round(rng.random() * 0.3 + 0.5, 4),
            "priority": round(rng.random() * 0.3 + 0.5, 4),
            "advisory_only": True,
            "auto_execution": False,
            "requires_review": True,
            "created_at": datetime.utcnow().isoformat(),
        }
        self._recommendations[rec_id] = rec
        self.storage.append(f"rec_{rec_id}", "recommendation", rec)
        return rec

    def get_recommendation(self, rec_id: str) -> Optional[dict]:
        return self._recommendations.get(rec_id)

    def recommendation_count(self) -> int:
        return len(self._recommendations)

    def by_type(self, rtype: str) -> List[dict]:
        return [r for r in self._recommendations.values() if r["type"] == rtype]

    def summary(self, seed: int = 0) -> dict:
        rng = random.Random(seed)
        return {
            "total_recommendations": self.recommendation_count(),
            "recommendation_confidence_avg": round(rng.random() * 0.2 + 0.6, 4),
            "advisory_only": True,
        }
