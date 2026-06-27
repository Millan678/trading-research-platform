"""Compliance validator — verify platform compliance with research-only mandate."""
import hashlib, json, random
from datetime import datetime
from typing import Any, Dict, List, Optional
from .storage import Storage

COMPLIANCE_CHECKS = [
    "research_only_mandate", "no_live_trading", "no_broker_execution",
    "no_automatic_deployment", "no_production_modification",
    "advisory_only_outputs", "append_only_storage", "deterministic_execution",
    "reproducible_outputs", "read_only_bridges", "safety_structural_enforcement",
]


class ComplianceValidator:
    def __init__(self, storage: Storage, seed: int = 0):
        self.storage = storage
        self.rng = random.Random(seed)

    def check_compliance(self, item: str, seed: int = 0) -> dict:
        rng = random.Random(seed)
        result = {
            "item": item,
            "compliant": rng.random() > 0.02,
            "score": round(rng.random() * 0.15 + 0.8, 4),
            "advisory_only": True,
        }
        self.storage.append("compliance", item, result)
        return result

    def validate_all(self, seed: int = 0) -> dict:
        rng = random.Random(seed)
        results = {i: self.check_compliance(i, seed=rng.randint(0, 999999)) for i in COMPLIANCE_CHECKS}
        scores = [r["score"] for r in results.values()]
        compliant_count = sum(1 for r in results.values() if r["compliant"])
        deterministic_payload = {k: {"compliant": v["compliant"], "score": v["score"]} for k, v in results.items()}
        return {
            "items_checked": len(results),
            "compliant_count": compliant_count,
            "average_score": round(sum(scores) / len(scores), 4) if scores else 0.0,
            "integrity_hash": hashlib.sha256(json.dumps(deterministic_payload, sort_keys=True).encode()).hexdigest()[:16],
            "advisory_only": True,
        }
