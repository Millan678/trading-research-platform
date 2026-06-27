"""Safety validator — verify all forbidden actions raise RuntimeError."""
import hashlib, json, random
from datetime import datetime
from typing import Any, Dict, List, Optional
from .storage import Storage
from .safety import FORBIDDEN, enforce, PlatformVerificationBlocked


class SafetyValidator:
    def __init__(self, storage: Storage, seed: int = 0):
        self.storage = storage
        self.rng = random.Random(seed)

    def validate_safety(self, operation: str, seed: int = 0) -> dict:
        try:
            enforce(operation)
            result = {"operation": operation, "blocked": False, "correct": False, "advisory_only": True}
        except PlatformVerificationBlocked:
            result = {"operation": operation, "blocked": True, "correct": True, "advisory_only": True}
        self.storage.append("safety_val", operation, result)
        return result

    def validate_all(self, seed: int = 0) -> dict:
        results = {op: self.validate_safety(op) for op in FORBIDDEN}
        blocked_count = sum(1 for r in results.values() if r["blocked"])
        deterministic_payload = {k: {"blocked": v["blocked"], "correct": v["correct"]} for k, v in results.items()}
        return {
            "operations_tested": len(results),
            "all_blocked": blocked_count == len(results),
            "blocked_count": blocked_count,
            "integrity_hash": hashlib.sha256(json.dumps(deterministic_payload, sort_keys=True).encode()).hexdigest()[:16],
            "advisory_only": True,
        }
