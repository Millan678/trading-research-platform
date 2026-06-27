"""API registry — catalog of all platform APIs."""
import hashlib, json, random
from datetime import datetime
from typing import Any, Dict, List, Optional
from .storage import Storage


class APIRegistry:
    def __init__(self, storage: Storage, seed: int = 0):
        self.storage = storage
        self.rng = random.Random(seed)
        self._apis: Dict[str, dict] = {}

    def register_api(self, api_name: str, api_type: str = "query", seed: int = 0) -> dict:
        rng = random.Random(seed)
        record = {
            "api_name": api_name,
            "api_type": api_type,
            "stability": round(rng.random() * 0.15 + 0.85, 4),
            "registered_at": datetime.utcnow().isoformat(),
            "advisory_only": True,
        }
        self._apis[api_name] = record
        self.storage.append(f"api_{api_name}", "api_registration", record)
        return record

    def register_standard_apis(self, seed: int = 0) -> dict:
        standard = [
            ("safety.enforce", "guard"), ("safety.audit", "query"),
            ("storage.append", "mutation"), ("storage.query", "query"),
            ("backup.create", "mutation"), ("backup.verify", "query"),
            ("cli.status", "query"), ("cli.report", "query"),
            ("dashboard.export", "mutation"), ("reports.generate", "mutation"),
            ("health.monitor", "query"), ("certification.compute", "query"),
            ("architecture.validate", "query"), ("optimization.analyze", "query"),
            ("documentation.generate", "mutation"),
        ]
        for name, atype in standard:
            self.register_api(name, atype, seed=seed)
        return {
            "apis_registered": len(self._apis),
            "advisory_only": True,
        }

    def summary(self, seed: int = 0) -> dict:
        return {
            "total_apis": len(self._apis),
            "advisory_only": True,
        }
