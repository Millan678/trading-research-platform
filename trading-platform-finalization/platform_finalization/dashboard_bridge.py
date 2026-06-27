"""Dashboard bridge — export 10 JSON dashboard pages."""
import json, os
from datetime import datetime
from typing import Any, Dict, List, Optional
from .contracts import DASHBOARD_PAGES
from .storage import Storage


class DashboardBridge:
    def __init__(self, base_dir: str):
        self.base_dir = base_dir
        self.dashboard_dir = os.path.join(base_dir, "dashboard")
        os.makedirs(self.dashboard_dir, exist_ok=True)

    def export(self, data: dict) -> dict:
        results = {}
        for page in DASHBOARD_PAGES:
            slug = page.lower().replace(" ", "_")
            page_data = {
                "page": page,
                "slug": slug,
                "data": data.get(slug, {"advisory_only": True}),
                "exported_at": datetime.utcnow().isoformat(),
                "advisory_only": True,
            }
            path = os.path.join(self.dashboard_dir, f"{slug}.json")
            with open(path, "w") as f:
                json.dump(page_data, f, indent=2, default=str)
            results[page] = page_data
        return {"pages_exported": len(results), "advisory_only": True}

    def validate(self) -> bool:
        for page in DASHBOARD_PAGES:
            slug = page.lower().replace(" ", "_")
            path = os.path.join(self.dashboard_dir, f"{slug}.json")
            if not os.path.isfile(path):
                return False
            try:
                with open(path) as f:
                    json.load(f)
            except Exception:
                return False
        return True

    def count(self) -> int:
        return len(DASHBOARD_PAGES)
