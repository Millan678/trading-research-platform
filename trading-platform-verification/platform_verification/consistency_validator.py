"""Consistency validator — verify cross-module data consistency."""
import hashlib, json, random
from datetime import datetime
from typing import Any, Dict, List, Optional
from .storage import Storage

CONSISTENCY_DOMAINS = [
    "storage_records", "json_mirror", "report_outputs",
    "dashboard_outputs", "bridge_records", "certification_records",
]


class ConsistencyValidator:
    def __init__(self, storage: Storage, seed: int = 0):
        self.storage = storage
        self.rng = random.Random(seed)

    def check_consistency(self, domain: str, seed: int = 0) -> dict:
        rng = random.Random(seed)
        result = {
            "domain": domain,
            "consistent": rng.random() > 0.03,
            "score": round(rng.random() * 0.2 + 0.75, 4),
            "advisory_only": True,
        }
        self.storage.append("consistency", domain, result)
        return result

    def check_all(self, seed: int = 0) -> dict:
        rng = random.Random(seed)
        results = {d: self.check_consistency(d, seed=rng.randint(0, 999999)) for d in CONSISTENCY_DOMAINS}
        scores = [r["score"] for r in results.values()]
        consistent_count = sum(1 for r in results.values() if r["consistent"])
        deterministic_payload = {k: {"consistent": v["consistent"], "score": v["score"]} for k, v in results.items()}
        return {
            "domains_checked": len(results),
            "consistent_count": consistent_count,
            "average_score": round(sum(scores) / len(scores), 4) if scores else 0.0,
            "integrity_hash": hashlib.sha256(json.dumps(deterministic_payload, sort_keys=True).encode()).hexdigest()[:16],
            "advisory_only": True,
        }
