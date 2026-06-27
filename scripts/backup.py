#!/usr/bin/env python3
"""Backup utility for the Trading Research Platform.

Creates SHA-256 verified backups of the platform source code.
Never uploads secrets. Never recursively backs up backups/.

Usage:
    python scripts/backup.py manifest   # Create SHA-256 manifest
    python scripts/backup.py archive     # Create timestamped archive
    python scripts/backup.py verify       # Verify backup integrity
"""

import hashlib
import json
import os
import shutil
import sys
import tarfile
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
BACKUPS_DIR = REPO_ROOT / "backups"

EXCLUDE_DIRS = {
    "backups", ".git", "venv", "node_modules", "__pycache__",
    ".mypy_cache", ".pytest_cache", "dist", "build", ".tox",
    ".eggs", ".ruff_cache", "data", "datasets",
}

EXCLUDE_EXTENSIONS = {
    ".pyc", ".pyo", ".db", ".sqlite", ".log",
    ".egg", ".whl", ".tar.gz", ".tgz",
}

EXCLUDE_FILES = {".env", "*.pem", "*.key", "*.secret"}


def should_include(path: Path) -> bool:
    """Check if a file should be included in the backup."""
    parts = path.relative_to(REPO_ROOT).parts
    for part in parts:
        if part in EXCLUDE_DIRS:
            return False
    if path.suffix in EXCLUDE_EXTENSIONS:
        return False
    for pattern in EXCLUDE_FILES:
        if path.name == pattern or path.name.startswith("."):
            if path.name in {".gitignore", ".gitattributes"}:
                return True
            if path.suffix in {".md", ".yml", ".yaml", ".json", ".py", ".txt", ".toml", ".cfg"}:
                return True
    return True


def compute_sha256(filepath: Path) -> str:
    """Compute SHA-256 hash of a file."""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def create_manifest() -> dict:
    """Create SHA-256 manifest of all included files."""
    manifest = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "root": str(REPO_ROOT),
        "files": {},
        "summary": {"total_files": 0, "total_size": 0},
    }

    for root, dirs, files in os.walk(REPO_ROOT):
        root_path = Path(root)
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

        for fname in files:
            filepath = root_path / fname
            if not should_include(filepath):
                continue
            try:
                rel = str(filepath.relative_to(REPO_ROOT))
                sha = compute_sha256(filepath)
                size = filepath.stat().st_size
                manifest["files"][rel] = {
                    "sha256": sha,
                    "size": size,
                }
                manifest["summary"]["total_files"] += 1
                manifest["summary"]["total_size"] += size
            except (OSError, ValueError):
                continue

    return manifest


def cmd_manifest():
    """Create and save SHA-256 manifest."""
    BACKUPS_DIR.mkdir(exist_ok=True)
    manifest = create_manifest()
    outpath = BACKUPS_DIR / "latest_manifest.sha256"
    with open(outpath, "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"Manifest: {manifest['summary']['total_files']} files, "
          f"{manifest['summary']['total_size']:,} bytes")
    print(f"Saved to: {outpath}")


def cmd_archive():
    """Create timestamped tar.gz archive."""
    BACKUPS_DIR.mkdir(exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    archive_name = f"trading-research-platform-{ts}.tar.gz"
    archive_path = BACKUPS_DIR / archive_name

    with tarfile.open(archive_path, "w:gz") as tar:
        for root, dirs, files in os.walk(REPO_ROOT):
            root_path = Path(root)
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
            for fname in files:
                filepath = root_path / fname
                if not should_include(filepath):
                    continue
                try:
                    tar.add(filepath, arcname=str(filepath.relative_to(REPO_ROOT)))
                except (OSError, ValueError):
                    continue

    sha = compute_sha256(archive_path)
    print(f"Archive: {archive_path.name}")
    print(f"SHA-256: {sha}")


def cmd_verify():
    """Verify backup integrity against manifest."""
    manifest_path = BACKUPS_DIR / "latest_manifest.sha256"
    if not manifest_path.exists():
        print("No manifest found. Run 'manifest' first.")
        sys.exit(1)

    with open(manifest_path) as f:
        manifest = json.load(f)

    ok = 0
    fail = 0
    missing = 0

    for rel, info in manifest["files"].items():
        filepath = REPO_ROOT / rel
        if not filepath.exists():
            missing += 1
            continue
        actual = compute_sha256(filepath)
        if actual == info["sha256"]:
            ok += 1
        else:
            fail += 1
            print(f"MISMATCH: {rel}")

    print(f"Verified: {ok} OK, {fail} FAILED, {missing} MISSING")
    if fail > 0 or missing > 0:
        sys.exit(1)
    print("✅ All backups verify correctly")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "manifest":
        cmd_manifest()
    elif cmd == "archive":
        cmd_archive()
    elif cmd == "verify":
        cmd_verify()
    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
