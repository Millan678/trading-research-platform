"""Goal manager — track research goals and progress."""
import hashlib, json, random
from datetime import datetime
from typing import Any, Dict, List, Optional
from .contracts import GoalStatus
from .storage import Storage


class GoalManager:
    def __init__(self, storage: Storage, seed: int = 0):
        self.storage = storage
        self.rng = random.Random(seed)
        self._goals: Dict[str, dict] = {}

    def add_goal(self, goal_id: str, description: str, priority: str = "high", seed: int = 0) -> dict:
        rng = random.Random(seed)
        rec = {
            "goal_id": goal_id,
            "description": description,
            "priority": priority,
            "status": GoalStatus.PENDING.value,
            "progress_score": round(rng.random() * 0.3 + 0.3, 4),
            "created_at": datetime.utcnow().isoformat(),
            "advisory_only": True,
        }
        self._goals[goal_id] = rec
        self.storage.append(f"goal_{goal_id}", "goal", rec)
        return rec

    def update_goal(self, goal_id: str, status: str = None, seed: int = 0) -> Optional[dict]:
        if goal_id not in self._goals:
            return None
        g = self._goals[goal_id]
        if status:
            g["status"] = status
        rng = random.Random(seed)
        g["progress_score"] = min(1.0, g["progress_score"] + round(rng.random() * 0.2, 4))
        return g

    def goal_count(self) -> int:
        return len(self._goals)

    def active_goals(self) -> int:
        return sum(1 for g in self._goals.values() if g["status"] == GoalStatus.PENDING.value)

    def summary(self, seed: int = 0) -> dict:
        rng = random.Random(seed)
        return {
            "total_goals": self.goal_count(),
            "active_goals": self.active_goals(),
            "goal_achievement_rate": round(rng.random() * 0.3 + 0.5, 4),
            "advisory_only": True,
        }
