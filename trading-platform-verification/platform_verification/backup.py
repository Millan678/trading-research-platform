"""Backup manager — SHA-256 verified timestamped backups."""
import hashlib, json, os, shutil
from datetime import datetime
from typing import Any, Dict, List


EXCLUDE = {"backups", ".git", "venv", "node_modules", "__pycache__"}


class BackupManager:
    def __init__(self, base_dir: str):
        self.base_dir = base_dir
        self.backup_dir = os.path.join(base_dir, "backups")
        os.makedirs(self.backup_dir, exist_ok=True)

    def create_backup(self) -> dict:
        ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        bp = os.path.join(self.backup_dir, f"backup_{ts}")
        os.makedirs(bp, exist_ok=True)
        entries = []
        for root, dirs, files in os.walk(self.base_dir):
            dirs[:] = [d for d in dirs if d not in EXCLUDE]
            for f in files:
                full = os.path.join(root, f)
                rel = os.path.relpath(full, self.base_dir)
                if rel.startswith("backups") or rel.startswith("."):
                    continue
                try:
                    h = hashlib.sha256(open(full, "rb").read()).hexdigest()
                    entries.append({"path": rel, "sha256": h})
                except Exception:
                    pass
        manifest = {
            "timestamp": ts,
            "entries": entries,
            "total_files": len(entries),
            "sha256": hashlib.sha256(json.dumps(entries, sort_keys=True).encode()).hexdigest(),
        }
        with open(os.path.join(bp, "manifest.json"), "w") as f:
            json.dump(manifest, f, indent=2)
        return manifest

    def verify_backup(self, manifest: dict) -> bool:
        current = {}
        for root, dirs, files in os.walk(self.base_dir):
            dirs[:] = [d for d in dirs if d not in EXCLUDE]
            for f in files:
                full = os.path.join(root, f)
                rel = os.path.relpath(full, self.base_dir)
                if rel.startswith("backups") or rel.startswith("."):
                    continue
                try:
                    current[rel] = hashlib.sha256(open(full, "rb").read()).hexdigest()
                except Exception:
                    pass
        for entry in manifest.get("entries", []):
            if entry["path"] not in current:
                return False
            if current[entry["path"]] != entry["sha256"]:
                return False
        return True
