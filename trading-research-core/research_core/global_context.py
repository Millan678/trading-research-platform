"""Global context — unified context spanning all research domains."""
import hashlib, json, random
from datetime import datetime
from typing import Any, Dict, List, Optional
from .contracts import GLOBAL_CONTEXT_CATEGORIES, CONTEXT_DOMAINS
from .storage import Storage


class GlobalContext:
    def __init__(self, storage: Storage, seed: int = 0):
        self.storage = storage
        self.rng = random.Random(seed)
        self._domains: Dict[str, dict] = {}
        for cat in GLOBAL_CONTEXT_CATEGORIES:
            self._domains[cat] = {
                "domain": cat,
                "active": True,
                "context_records": 0,
                "last_updated": None,
                "advisory_only": True,
            }

    def update_domain(self, domain: str, data: dict, seed: int = 0) -> dict:
        if domain not in self._domains:
            self._domains[domain] = {"domain": domain, "active": True, "context_records": 0, "last_updated": None, "advisory_only": True}
        entry = self._domains[domain]
        entry["context_records"] += 1
        entry["last_updated"] = datetime.utcnow().isoformat()
        rng = random.Random(seed)
        rec = {
            "domain": domain,
            "summary": data.get("summary", f"{domain} context update"),
            "relevance_score": round(rng.random() * 0.3 + 0.6, 4),
            "integrity_hash": hashlib.sha256(json.dumps(data, sort_keys=True, default=str).encode()).hexdigest()[:16],
            "advisory_only": True,
        }
        cr = entry["context_records"]
        self.storage.append(f"ctx_{domain}_{cr}", "global_context", rec)
        return rec

    def get_domain(self, domain: str) -> Optional[dict]:
        return self._domains.get(domain)

    def domain_count(self) -> int:
        return len(self._domains)

    def active_domains(self) -> int:
        return sum(1 for d in self._domains.values() if d.get("active"))

    def snapshot(self, seed: int = 0) -> dict:
        rng = random.Random(seed)
        return {
            "total_domains": self.domain_count(),
            "active_domains": self.active_domains(),
            "domains": {k: v for k, v in self._domains.items()},
            "global_relevance": round(rng.random() * 0.2 + 0.7, 4),
            "advisory_only": True,
        }

    def compute_stable_hash(self, seed: int = 0) -> str:
        payload = json.dumps({
            "domains": sorted(self._domains.keys()),
            "seed": seed,
        }, sort_keys=True)
        return "0x" + hashlib.sha256(payload.encode()).hexdigest()
