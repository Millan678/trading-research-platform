"""Context manager — coordinate context lifecycle and transitions."""
import hashlib, json, random
from datetime import datetime
from typing import Any, Dict, List, Optional
from .contracts import GLOBAL_CONTEXT_CATEGORIES
from .storage import Storage


class ContextManager:
    def __init__(self, storage: Storage, seed: int = 0):
        self.storage = storage
        self.rng = random.Random(seed)
        self._transitions: List[dict] = []
        self._contexts: Dict[str, dict] = {}

    def create_context(self, context_id: str, domains: List[str] = None, seed: int = 0) -> dict:
        domains = domains or GLOBAL_CONTEXT_CATEGORIES[:4]
        rng = random.Random(seed)
        rec = {
            "context_id": context_id,
            "domains": domains,
            "status": "active",
            "coherence_score": round(rng.random() * 0.3 + 0.6, 4),
            "created_at": datetime.utcnow().isoformat(),
            "advisory_only": True,
        }
        self._contexts[context_id] = rec
        self.storage.append(f"cctx_{context_id}", "context", rec)
        return rec

    def transition(self, from_ctx: str, to_ctx: str, trigger: str = "auto", seed: int = 0) -> dict:
        rng = random.Random(seed)
        rec = {
            "from": from_ctx,
            "to": to_ctx,
            "trigger": trigger,
            "transition_score": round(rng.random() * 0.3 + 0.5, 4),
            "created_at": datetime.utcnow().isoformat(),
            "advisory_only": True,
        }
        self._transitions.append(rec)
        self.storage.append(f"trans_{len(self._transitions)}", "context_transition", rec)
        return rec

    def context_count(self) -> int:
        return len(self._contexts)

    def transition_count(self) -> int:
        return len(self._transitions)

    def summary(self, seed: int = 0) -> dict:
        rng = random.Random(seed)
        return {
            "total_contexts": self.context_count(),
            "total_transitions": self.transition_count(),
            "coherence_index": round(rng.random() * 0.2 + 0.6, 4),
            "advisory_only": True,
        }
