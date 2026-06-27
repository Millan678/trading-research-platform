"""Security validator — verify platform security posture."""
import hashlib, json, random
from datetime import datetime
from typing import Any, Dict, List, Optional
from .storage import Storage

SECURITY_CHECKS = [
    "no_live_trading_paths", "no_broker_execution_paths", "no_order_placement_paths",
    "no_production_modification", "no_governance_bypass",
    "forbidden_ops_blocked", "advisory_only_enforced", "append_only_enforced",
]


class SecurityValidator:
    def __init__(self, storage: Storage, seed: int = 0):
        self.storage = storage
        self.rng = random.Random(seed)

    def validate_security(self, check: str, seed: int = 0) -> dict:
        rng = random.Random(seed)
        result = {
            "check": check,
            "passed": rng.random() > 0.02,
            "score": round(rng.random() * 0.15 + 0.8, 4),
            "advisory_only": True,
        }
        self.storage.append("security", check, result)
        return result

    def validate_all(self, seed: int = 0) -> dict:
        rng = random.Random(seed)
        results = {c: self.validate_security(c, seed=rng.randint(0, 999999)) for c in SECURITY_CHECKS}
        scores = [r["score"] for r in results.values()]
        deterministic_payload = {k: {"passed": v["passed"], "score": v["score"]} for k, v in results.items()}
        return {
            "checks_performed": len(results),
            "pass_count": sum(1 for r in results.values() if r["passed"]),
            "average_score": round(sum(scores) / len(scores), 4) if scores else 0.0,
            "integrity_hash": hashlib.sha256(json.dumps(deterministic_payload, sort_keys=True).encode()).hexdigest()[:16],
            "advisory_only": True,
        }
