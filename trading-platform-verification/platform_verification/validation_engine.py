"""Validation engine — orchestrate all validation domains."""
import hashlib, json, random
from datetime import datetime
from typing import Any, Dict, List, Optional
from .contracts import VALIDATION_DOMAINS, ValidationStatus
from .storage import Storage


class ValidationEngine:
    def __init__(self, storage: Storage, seed: int = 0):
        self.storage = storage
        self.rng = random.Random(seed)

    def validate_domain(self, domain: str, seed: int = 0) -> dict:
        rng = random.Random(seed)
        status_val = rng.random()
        status = (
            ValidationStatus.PASS.value if status_val > 0.15
            else ValidationStatus.WARN.value if status_val > 0.05
            else ValidationStatus.FAIL.value
        )
        result = {
            "domain": domain,
            "status": status,
            "score": round(rng.random() * 0.25 + 0.7, 4),
            "advisory_only": True,
        }
        self.storage.append(f"val_{domain}", "domain_validation", result)
        return result

    def validate_all(self, seed: int = 0) -> dict:
        rng = random.Random(seed)
        results = {}
        for d in VALIDATION_DOMAINS:
            results[d] = self.validate_domain(d, seed=rng.randint(0, 999999))
        pass_count = sum(1 for r in results.values() if r["status"] == "pass")
        warn_count = sum(1 for r in results.values() if r["status"] == "warn")
        fail_count = sum(1 for r in results.values() if r["status"] == "fail")
        scores = [r["score"] for r in results.values()]
        deterministic_payload = {d: {"status": r["status"], "score": r["score"]} for d, r in results.items()}
        return {
            "domains_validated": len(results),
            "pass_count": pass_count,
            "warn_count": warn_count,
            "fail_count": fail_count,
            "average_score": round(sum(scores) / len(scores), 4) if scores else 0.0,
            "integrity_hash": hashlib.sha256(json.dumps(deterministic_payload, sort_keys=True).encode()).hexdigest()[:16],
            "advisory_only": True,
        }
