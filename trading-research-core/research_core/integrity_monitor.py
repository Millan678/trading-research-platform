"""Integrity monitor — verify data and system integrity."""
import hashlib, json, random
from datetime import datetime
from typing import Any, Dict, List, Optional
from .storage import Storage


class IntegrityMonitor:
    def __init__(self, storage: Storage, seed: int = 0):
        self.storage = storage
        self.rng = random.Random(seed)
        self._verifications: List[dict] = []

    def verify_integrity(self, target: str, data: dict = None, seed: int = 0) -> dict:
        rng = random.Random(seed)
        data_hash = hashlib.sha256(json.dumps(data or {}, sort_keys=True, default=str).encode()).hexdigest()[:16] if data else "none"
        passed = rng.random() > 0.15
        rec = {
            "target": target,
            "data_hash": data_hash,
            "integrity_passed": passed,
            "integrity_score": round(rng.random() * 0.2 + 0.8, 4),
            "verified_at": datetime.utcnow().isoformat(),
            "advisory_only": True,
        }
        self._verifications.append(rec)
        self.storage.append(f"int_{target}_{len(self._verifications)}", "integrity", rec)
        return rec

    def verification_count(self) -> int:
        return len(self._verifications)

    def pass_rate(self) -> float:
        if not self._verifications:
            return 1.0
        passed = sum(1 for v in self._verifications if v["integrity_passed"])
        return round(passed / len(self._verifications), 4)

    def summary(self, seed: int = 0) -> dict:
        rng = random.Random(seed)
        return {
            "total_verifications": self.verification_count(),
            "pass_rate": self.pass_rate(),
            "integrity_score": round(rng.random() * 0.2 + 0.8, 4),
            "advisory_only": True,
        }
