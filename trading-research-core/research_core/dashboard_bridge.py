"""Dashboard bridge — export 10 JSON dashboard pages."""
import json, os, hashlib
from typing import Any, Dict, List, Optional
from .contracts import DASHBOARD_PAGES


class DashboardBridge:
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        self.pages_dir = os.path.join(output_dir, "dashboard")
        os.makedirs(self.pages_dir, exist_ok=True)

    def export(self, platform_data: dict) -> dict:
        exported = []
        for i, title in enumerate(DASHBOARD_PAGES):
            safe = title.lower().replace(" ", "_")
            page = {
                "page_id": i,
                "title": title,
                "slug": safe,
                "data": platform_data.get(safe, {"advisory_only": True}),
                "advisory_only": True,
            }
            path = os.path.join(self.pages_dir, f"{safe}.json")
            with open(path, "w") as f:
                json.dump(page, f, indent=2, default=str)
            exported.append(safe)
        return {"pages_exported": len(exported), "pages": exported}

    def validate(self) -> bool:
        if not os.path.isdir(self.pages_dir):
            return False
        for title in DASHBOARD_PAGES:
            safe = title.lower().replace(" ", "_")
            path = os.path.join(self.pages_dir, f"{safe}.json")
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
