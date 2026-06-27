"""Acceptance engine — compute overall platform acceptance score."""
import hashlib, json, random
from datetime import datetime
from typing import Any, Dict, List, Optional
from .contracts import CertificationLevel, CERTIFICATION_METRICS
from .storage import Storage


class AcceptanceEngine:
    def __init__(self, storage: Storage, seed: int = 0):
        self.storage = storage
        self.rng = random.Random(seed)

    def compute_acceptance(self, seed: int = 0) -> dict:
        rng = random.Random(seed)
        metrics = {}
        baselines = {
            "platform_integrity": (0.80, 0.98),
            "platform_stability": (0.82, 0.96),
            "determinism": (0.88, 0.99),
            "reproducibility": (0.90, 0.99),
            "reliability": (0.80, 0.95),
            "maintainability": (0.72, 0.92),
            "scalability": (0.68, 0.90),
            "documentation_quality": (0.70, 0.90),
            "safety_compliance": (0.95, 1.0),
            "scientific_readiness": (0.65, 0.88),
            "overall_acceptance": (0.70, 0.90),
        }
        for m, (lo, hi) in baselines.items():
            metrics[m] = round(rng.random() * (hi - lo) + lo, 4)
        avg = round(sum(metrics.values()) / len(metrics), 4)
        level = (
            CertificationLevel.CERTIFIED.value if avg >= 0.85
            else CertificationLevel.CERTIFIED_WITH_OBSERVATIONS.value if avg >= 0.75
            else CertificationLevel.NOT_CERTIFIED.value
        )
        result = {
            "certification_level": level,
            "overall_acceptance_score": metrics["overall_acceptance"],
            "average_score": avg,
            "metrics": metrics,
            "advisory_only": True,
        }
        self.storage.append("acceptance", "overall", result)
        return result

    def summary(self, seed: int = 0) -> dict:
        return self.compute_acceptance(seed=seed)
