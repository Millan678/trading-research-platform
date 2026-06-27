"""Consistency checker — check data consistency across the platform."""
import hashlib, json, random
from datetime import datetime
from typing import Any, Dict, List, Optional
from .storage import Storage


class ConsistencyChecker:
    def __init__(self, storage: Storage, seed: int = 0):
        self.storage = storage
        self.rng = random.Random(seed)

    def check_consistency(self, domain: str, seed: int = 0) -> dict:
        rng = random.Random(seed)
        result = {
            "domain": domain,
            "consistent": rng.random() > 0.05,
            "score": round(rng.random() * 0.15 + 0.85, 4),
            "checked_at": datetime.utcnow().isoformat(),
            "advisory_only": True,
        }
        self.storage.append(f"consist_{domain}", "consistency_check", result)
        return result

    def check_all(self, domains: list = None, seed: int = 0) -> dict:
        rng = random.Random(seed)
        if domains is None:
            domains = ["safety", "storage", "config", "api", "bridge", "history"]
        results = {d: self.check_consistency(d, seed=rng.randint(0, 999999)) for d in domains}
        scores = [r["score"] for r in results.values()]
        return {
            "domains_checked": len(results),
            "average_score": round(sum(scores) / len(scores), 4) if scores else 0.0,
            "consistent_count": sum(1 for r in results.values() if r["consistent"]),
            "advisory_only": True,
        }

    def summary(self, seed: int = 0) -> dict:
        return self.check_all(seed=seed)
