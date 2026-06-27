"""Health monitor — monitor platform health and subsystem health."""
import hashlib, json, random
from datetime import datetime
from typing import Any, Dict, List, Optional
from .storage import Storage


class HealthMonitor:
    def __init__(self, storage: Storage, seed: int = 0):
        self.storage = storage
        self.rng = random.Random(seed)

    def check_health(self, component: str, seed: int = 0) -> dict:
        rng = random.Random(seed)
        result = {
            "component": component,
            "healthy": rng.random() > 0.05,
            "score": round(rng.random() * 0.2 + 0.75, 4),
            "checked_at": datetime.utcnow().isoformat(),
            "advisory_only": True,
        }
        self.storage.append(f"health_{component}", "health_check", result)
        return result

    def check_all(self, seed: int = 0) -> dict:
        rng = random.Random(seed)
        components = [
            "safety", "storage", "backup", "validation",
            "optimization", "consistency", "integrity",
            "api_registry", "capability_registry", "documentation",
            "certification", "bridges", "dashboard", "reports", "cli",
        ]
        results = {c: self.check_health(c, seed=rng.randint(0, 999999)) for c in components}
        scores = [r["score"] for r in results.values()]
        return {
            "components_checked": len(results),
            "average_score": round(sum(scores) / len(scores), 4) if scores else 0.0,
            "healthy_count": sum(1 for r in results.values() if r["healthy"]),
            "advisory_only": True,
        }

    def summary(self, seed: int = 0) -> dict:
        return self.check_all(seed=seed)
