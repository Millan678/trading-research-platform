"""Planner — research planning with goals, objectives, and scheduling."""
import hashlib, json, random
from datetime import datetime
from typing import Any, Dict, List, Optional
from .contracts import GoalStatus
from .storage import Storage


class Planner:
    def __init__(self, storage: Storage, seed: int = 0):
        self.storage = storage
        self.rng = random.Random(seed)
        self._plans: Dict[str, dict] = {}
        self._milestones: List[dict] = []

    def create_plan(self, plan_id: str, goals: List[str] = None, seed: int = 0) -> dict:
        goals = goals or ["advisory_research", "scientific_integrity"]
        rng = random.Random(seed)
        rec = {
            "plan_id": plan_id,
            "goals": goals,
            "status": GoalStatus.PENDING.value,
            "priority_score": round(rng.random() * 0.3 + 0.6, 4),
            "milestones": len(goals),
            "created_at": datetime.utcnow().isoformat(),
            "advisory_only": True,
        }
        self._plans[plan_id] = rec
        self.storage.append(f"plan_{plan_id}", "plan", rec)
        return rec

    def add_milestone(self, plan_id: str, milestone: str, seed: int = 0) -> dict:
        rng = random.Random(seed)
        rec = {
            "plan_id": plan_id,
            "milestone": milestone,
            "completion_score": round(rng.random() * 0.3 + 0.5, 4),
            "status": "pending",
            "advisory_only": True,
        }
        self._milestones.append(rec)
        self.storage.append(f"ms_{plan_id}_{len(self._milestones)}", "milestone", rec)
        return rec

    def plan_count(self) -> int:
        return len(self._plans)

    def milestone_count(self) -> int:
        return len(self._milestones)

    def summary(self, seed: int = 0) -> dict:
        rng = random.Random(seed)
        return {
            "total_plans": self.plan_count(),
            "total_milestones": self.milestone_count(),
            "planning_efficiency": round(rng.random() * 0.2 + 0.6, 4),
            "advisory_only": True,
        }
