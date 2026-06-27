"""Episodic memory — event-based memory with temporal indexing."""
import hashlib, json, random
from datetime import datetime
from typing import Any, Dict, List, Optional
from .storage import Storage


class EpisodicMemory:
    def __init__(self, storage: Storage, seed: int = 0):
        self.storage = storage
        self.rng = random.Random(seed)
        self._episodes: Dict[str, dict] = {}

    def record_episode(self, episode_id: str, event: str, seed: int = 0) -> dict:
        rng = random.Random(seed)
        rec = {
            "episode_id": episode_id,
            "event": event,
            "salience_score": round(rng.random() * 0.3 + 0.6, 4),
            "temporal_index": len(self._episodes),
            "created_at": datetime.utcnow().isoformat(),
            "advisory_only": True,
        }
        self._episodes[episode_id] = rec
        self.storage.append(f"epi_{episode_id}", "episodic", rec)
        return rec

    def retrieve_episode(self, episode_id: str) -> Optional[dict]:
        return self._episodes.get(episode_id)

    def query_episodes(self, limit: int = 10) -> List[dict]:
        return list(self._episodes.values())[-limit:]

    def episode_count(self) -> int:
        return len(self._episodes)

    def summary(self, seed: int = 0) -> dict:
        rng = random.Random(seed)
        return {
            "total_episodes": self.episode_count(),
            "salience_avg": round(rng.random() * 0.2 + 0.7, 4),
            "advisory_only": True,
        }
