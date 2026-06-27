"""Execution coordinator — coordinate advisory execution without auto-approval."""
import hashlib, json, random
from datetime import datetime
from typing import Any, Dict, List, Optional
from .storage import Storage


class ExecutionCoordinator:
    def __init__(self, storage: Storage, seed: int = 0):
        self.storage = storage
        self.rng = random.Random(seed)
        self._tasks: Dict[str, dict] = {}

    def submit_task(self, task_id: str, description: str = "", seed: int = 0) -> dict:
        rng = random.Random(seed)
        rec = {
            "task_id": task_id,
            "description": description,
            "status": "pending_review",
            "auto_execution": False,
            "auto_approval": False,
            "requires_manual_review": True,
            "priority_score": round(rng.random() * 0.3 + 0.5, 4),
            "advisory_only": True,
        }
        self._tasks[task_id] = rec
        self.storage.append(f"exec_{task_id}", "execution", rec)
        return rec

    def review_task(self, task_id: str, approved: bool = False, seed: int = 0) -> dict:
        task = self._tasks.get(task_id)
        if not task:
            return {"reviewed": False, "reason": "not_found", "advisory_only": True}
        task["status"] = "approved" if approved else "rejected"
        return {"reviewed": True, "task_id": task_id, "status": task["status"], "advisory_only": True}

    def task_count(self) -> int:
        return len(self._tasks)

    def summary(self, seed: int = 0) -> dict:
        rng = random.Random(seed)
        return {
            "total_tasks": self.task_count(),
            "coordination_efficiency": round(rng.random() * 0.2 + 0.6, 4),
            "advisory_only": True,
        }
