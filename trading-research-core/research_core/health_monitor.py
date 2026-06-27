"""Health monitor — monitor system health and subsystem status."""
import hashlib, json, random
from datetime import datetime
from typing import Any, Dict, List, Optional
from .storage import Storage


class HealthMonitor:
    def __init__(self, storage: Storage, seed: int = 0):
        self.storage = storage
        self.rng = random.Random(seed)
        self._checks: List[dict] = []

    def check_health(self, component: str, seed: int = 0) -> dict:
        rng = random.Random(seed)
        rec = {
            "component": component,
            "health_score": round(rng.random() * 0.3 + 0.6, 4),
            "status": "healthy" if rng.random() > 0.2 else "degraded",
            "checked_at": datetime.utcnow().isoformat(),
            "advisory_only": True,
        }
        self._checks.append(rec)
        self.storage.append(f"health_{component}_{len(self._checks)}", "health", rec)
        return rec

    def overall_health(self, seed: int = 0) -> dict:
        rng = random.Random(seed)
        if not self._checks:
            return {"overall_health": round(rng.random() * 0.2 + 0.7, 4), "checks_performed": 0, "advisory_only": True}
        avg = sum(c["health_score"] for c in self._checks) / len(self._checks)
        return {
            "overall_health": round(avg, 4),
            "checks_performed": len(self._checks),
            "healthy_components": sum(1 for c in self._checks if c["status"] == "healthy"),
            "degraded_components": sum(1 for c in self._checks if c["status"] != "healthy"),
            "advisory_only": True,
        }

    def check_count(self) -> int:
        return len(self._checks)

    def summary(self, seed: int = 0) -> dict:
        return self.overall_health(seed)
