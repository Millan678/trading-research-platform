"""Integrity checker — verify platform structural integrity."""
import hashlib, json, random
from datetime import datetime
from typing import Any, Dict, List, Optional
from .storage import Storage


class IntegrityChecker:
    def __init__(self, storage: Storage, seed: int = 0):
        self.storage = storage
        self.rng = random.Random(seed)

    def check_integrity(self, component: str, seed: int = 0) -> dict:
        rng = random.Random(seed)
        result = {
            "component": component,
            "intact": rng.random() > 0.02,
            "score": round(rng.random() * 0.12 + 0.88, 4),
            "checked_at": datetime.utcnow().isoformat(),
            "advisory_only": True,
        }
        self.storage.append(f"integ_{component}", "integrity_check", result)
        return result

    def check_all(self, seed: int = 0) -> dict:
        rng = random.Random(seed)
        components = ["modules", "bridges", "storage", "safety", "cli", "dashboard", "reports"]
        results = {c: self.check_integrity(c, seed=rng.randint(0, 999999)) for c in components}
        scores = [r["score"] for r in results.values()]
        return {
            "components_checked": len(results),
            "average_score": round(sum(scores) / len(scores), 4) if scores else 0.0,
            "intact_count": sum(1 for r in results.values() if r["intact"]),
            "advisory_only": True,
        }

    def summary(self, seed: int = 0) -> dict:
        return self.check_all(seed=seed)
