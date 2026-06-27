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

    def create_backup(self) -> dict:
        ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        tag = f"core_backup_{ts}"
        dest = os.path.join(self.backup_dir, tag)
        if os.path.exists(dest):
            shutil.rmtree(dest)
        os.makedirs(dest, exist_ok=True)
        sha256_parts = []
        file_count = 0
        for root, dirs, files in os.walk(self.base_dir):
            dirs[:] = [d for d in dirs if d not in _EXCLUDE]
            for f in sorted(files):
                if not f.endswith(".py"):
                    continue
                src = os.path.join(root, f)
                rel = os.path.relpath(src, self.base_dir)
                dst = os.path.join(dest, rel)
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                content = open(src, "rb").read()
                sha256_parts.append(hashlib.sha256(content).hexdigest())
                file_count += 1
                with open(dst, "wb") as out:
                    out.write(content)
        composite = hashlib.sha256("|".join(sha256_parts).encode()).hexdigest()
        manifest = {
            "tag": tag,
            "timestamp": ts,
            "file_count": file_count,
            "sha256": composite,
            "advisory_only": True,
        }
        with open(os.path.join(dest, "manifest.json"), "w") as mf:
            json.dump(manifest, mf, indent=2)
        return manifest

    def verify_backup(self, manifest: dict) -> bool:
        tag = manifest.get("tag", "")
        dest = os.path.join(self.backup_dir, tag)
        if not os.path.isdir(dest):
            return False
        sha256_parts = []
        for root, dirs, files in os.walk(dest):
            dirs[:] = [d for d in dirs if d not in _EXCLUDE]
            for f in sorted(files):
                if f == "manifest.json":
                    continue
                if not f.endswith(".py"):
                    continue
                src = os.path.join(root, f)
                content = open(src, "rb").read()
                sha256_parts.append(hashlib.sha256(content).hexdigest())
        composite = hashlib.sha256("|".join(sha256_parts).encode()).hexdigest()
        return composite == manifest.get("sha256", "")
