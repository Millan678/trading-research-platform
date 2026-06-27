"""Reports — generate all 8 required Markdown + JSON reports."""
import json, os
from datetime import datetime
from typing import Any, Dict, List, Optional
from .contracts import REQUIRED_REPORTS
from .storage import Storage


class Reports:
    def __init__(self, base_dir: str):
        self.base_dir = base_dir
        self.reports_dir = os.path.join(base_dir, "reports")
        os.makedirs(self.reports_dir, exist_ok=True)

    def generate_report(self, report_id: str, content: dict) -> dict:
        slug = report_id.lower()
        json_path = os.path.join(self.reports_dir, f"{slug}.json")
        md_path = os.path.join(self.reports_dir, f"{slug}.md")
        gen_at = datetime.utcnow().isoformat()
        report_data = {"report_id": report_id, "generated_at": gen_at, "advisory_only": True, **content}
        with open(json_path, "w") as f:
            json.dump(report_data, f, indent=2, default=str)
        md_content = f"# {report_id}\n\nGenerated: {gen_at}\n\nStatus: advisory_only\n"
        with open(md_path, "w") as f:
            f.write(md_content)
        return {"report_id": report_id, "generated": True, "advisory_only": True}

    def generate_all(self, content: dict = None) -> dict:
        if content is None:
            content = {}
        results = {}
        for report_id in REQUIRED_REPORTS:
            results[report_id] = self.generate_report(report_id, content)
        return {"reports": results, "total_generated": len(results), "advisory_only": True}
