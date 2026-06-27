"""Fault injection — simulated fault injection testing (research-only)."""
import hashlib, json, random
from datetime import datetime
from typing import Any, Dict, List, Optional
from .storage import Storage


class FaultInjection:
    def __init__(self, storage: Storage, seed: int = 0):
        self.storage = storage
        self.rng = random.Random(seed)

    def inject_fault(self, fault_type: str, seed: int = 0) -> dict:
        rng = random.Random(seed)
        result = {
            "fault_type": fault_type,
            "detected": True,
            "recovered": rng.random() > 0.1,
            "recovery_score": round(rng.random() * 0.25 + 0.7, 4),
            "advisory_only": True,
        }
        self.storage.append("faults", fault_type, result)
        return result

    def inject_all(self, seed: int = 0) -> dict:
        rng = random.Random(seed)
        faults = [
            "storage_corruption", "bridge_failure", "config_mismatch",
            "memory_pressure", "disk_full", "network_timeout",
            "concurrent_write_conflict", "schema_drift",
        ]
        results = {f: self.inject_fault(f, seed=rng.randint(0, 999999)) for f in faults}
        recovery_count = sum(1 for r in results.values() if r["recovered"])
        deterministic_payload = {k: {"detected": v["detected"], "recovered": v["recovered"]} for k, v in results.items()}
        return {
            "faults_injected": len(results),
            "recovery_count": recovery_count,
            "all_recovered": all(r["recovered"] for r in results.values()),
            "integrity_hash": hashlib.sha256(json.dumps(deterministic_payload, sort_keys=True).encode()).hexdigest()[:16],
            "advisory_only": True,
        }
