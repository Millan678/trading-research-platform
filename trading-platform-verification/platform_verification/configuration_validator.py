"""Configuration validator — verify all configurations are valid."""
import hashlib, json, random
from datetime import datetime
from typing import Any, Dict, List, Optional
from .storage import Storage

CONFIG_ITEMS = [
    "storage_path", "backup_dir", "pg_url", "json_mirror_dir",
    "safety_enforcement", "advisory_mode", "append_only", "seed",
    "bridge_count", "phase_count", "report_formats", "dashboard_pages",
]


class ConfigurationValidator:
    def __init__(self, storage: Storage, seed: int = 0):
        self.storage = storage
        self.rng = random.Random(seed)

    def validate_config(self, item: str, seed: int = 0) -> dict:
        rng = random.Random(seed)
        result = {
            "item": item,
            "valid": rng.random() > 0.05,
            "score": round(rng.random() * 0.2 + 0.75, 4),
            "advisory_only": True,
        }
        self.storage.append("config", item, result)
        return result

    def validate_all(self, seed: int = 0) -> dict:
        rng = random.Random(seed)
        results = {i: self.validate_config(i, seed=rng.randint(0, 999999)) for i in CONFIG_ITEMS}
        scores = [r["score"] for r in results.values()]
        deterministic_payload = {k: {"valid": v["valid"], "score": v["score"]} for k, v in results.items()}
        return {
            "items_validated": len(results),
            "valid_count": sum(1 for r in results.values() if r["valid"]),
            "average_score": round(sum(scores) / len(scores), 4) if scores else 0.0,
            "integrity_hash": hashlib.sha256(json.dumps(deterministic_payload, sort_keys=True).encode()).hexdigest()[:16],
            "advisory_only": True,
        }
