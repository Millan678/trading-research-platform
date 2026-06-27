"""Reports — generate Markdown + JSON reports."""
import json, os, hashlib
from datetime import datetime
from typing import Any, Dict, List, Optional
from .contracts import REQUIRED_REPORTS


class Reports:
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        self.reports_dir = os.path.join(output_dir, "reports")
        os.makedirs(self.reports_dir, exist_ok=True)

    def generate_all(self, data: dict = None) -> dict:
        data = data or {}
        reports = []
        for report_id in REQUIRED_REPORTS:
            slug = report_id.lower()
            content = {
                "report_id": report_id,
                "generated_at": datetime.utcnow().isoformat(),
                "data": data,
                "advisory_only": True,
            }
            json_path = os.path.join(self.reports_dir, f"{slug}.json")
            with open(json_path, "w") as f:
                json.dump(content, f, indent=2, default=str)
            gen_at = content["generated_at"]
            md_content = f"# {report_id}\n\nGenerated: {gen_at}\n\nStatus: advisory_only\n"
            md_path = os.path.join(self.reports_dir, f"{slug}.md")
            with open(md_path, "w") as f:
                f.write(md_content)
            reports.append(report_id)
        return {"reports_generated": len(reports), "reports": reports}
