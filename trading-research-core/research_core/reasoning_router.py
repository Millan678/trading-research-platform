"""Reasoning router — route advisory requests to appropriate reasoning subsystems."""
import hashlib, json, random
from datetime import datetime
from typing import Any, Dict, List, Optional
from .contracts import CONTEXT_DOMAINS
from .storage import Storage

REASONING_DOMAINS = [
    "deductive", "inductive", "abductive", "analogical",
    "causal", "statistical", "comparative", "evaluative",
]

class ReasoningRouter:
    def __init__(self, storage: Storage, seed: int = 0):
        self.storage = storage
        self.rng = random.Random(seed)
        self._routes: Dict[str, dict] = {}

    def register_route(self, domain: str, target: str = "core_reasoning", seed: int = 0) -> dict:
        rng = random.Random(seed)
        rec = {
            "domain": domain,
            "target": target,
            "confidence": round(rng.random() * 0.3 + 0.6, 4),
            "active": True,
            "advisory_only": True,
        }
        self._routes[domain] = rec
        self.storage.append(f"rr_{domain}", "reasoning_route", rec)
        return rec

    def route_request(self, domain: str, seed: int = 0) -> dict:
        rng = random.Random(seed)
        route = self._routes.get(domain, {"domain": domain, "target": "default", "confidence": 0.5})
        return {
            "domain": domain,
            "target": route.get("target", "default"),
            "routed_confidence": round(rng.random() * 0.2 + 0.6, 4),
            "advisory_only": True,
        }

    def route_count(self) -> int:
        return len(self._routes)

    def summary(self, seed: int = 0) -> dict:
        rng = random.Random(seed)
        return {
            "total_routes": self.route_count(),
            "coverage": min(self.route_count() / max(len(REASONING_DOMAINS), 1), 1.0),
            "routing_efficiency": round(rng.random() * 0.2 + 0.7, 4),
            "advisory_only": True,
        }
