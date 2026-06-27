"""Backup — timestamped backup with SHA-256 integrity verification."""
import hashlib, json, os, shutil
from datetime import datetime
from typing import Any, Dict, List, Optional

_EXCLUDE = {"backups", ".git", "venv", "node_modules", "__pycache__"}


class BackupManager:
    def __init__(self, base_dir: str):
        self.base_dir = base_dir
        self.backup_dir = os.path.join(base_dir, "backups")
        os.makedirs(self.backup_dir, exist_ok=True)

    def _sha256_file(self, path: str) -> str:
        h = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()

    def _sha256_str(self, data: str) -> str:
        return hashlib.sha256(data.encode()).hexdigest()

    def _should_include(self, path: str) -> bool:
        parts = path.split(os.sep)
        return not any(p in _EXCLUDE for p in parts)

    def create_backup(self) -> dict:
        ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        dest = os.path.join(self.backup_dir, f"backup_{ts}")
        os.makedirs(dest, exist_ok=True)
        entries = []
        for root, dirs, files in os.walk(self.base_dir):
            dirs[:] = [d for d in dirs if d not in _EXCLUDE]
            for f in files:
                if not f.endswith(".py"):
                    continue
                src = os.path.join(root, f)
                rel = os.path.relpath(src, self.base_dir)
                if not self._should_include(rel):
                    continue
                dst = os.path.join(dest, rel)
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copy2(src, dst)
                entries.append({"path": rel, "sha256": self._sha256_file(src)})
        manifest = {
            "timestamp": ts,
            "entries": entries,
            "sha256": self._sha256_str(json.dumps(sorted(e["path"] for e in entries))),
            "advisory_only": True,
        }
        manifest_path = os.path.join(dest, "manifest.json")
        with open(manifest_path, "w") as mf:
            json.dump(manifest, mf, indent=2)
        return manifest

    def verify_backup(self, manifest: dict) -> bool:
        ts = manifest["timestamp"]
        dest = os.path.join(self.backup_dir, f"backup_{ts}")
        for entry in manifest["entries"]:
            path = os.path.join(dest, entry["path"])
            if not os.path.isfile(path):
                return False
            if self._sha256_file(path) != entry["sha256"]:
                return False
        return True
