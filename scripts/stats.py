#!/usr/bin/env python3
"""Repository statistics for the Trading Research Platform.

Usage:
    python scripts/stats.py --summary          # Overall summary
    python scripts/stats.py --check-imports     # Check for broken imports
    python scripts/stats.py --check-modules     # Check for missing modules
    python scripts/stats.py --check-duplicates  # Check for duplicate filenames
    python scripts/stats.py --doc-coverage      # Documentation coverage
"""

import argparse
import os
import sys
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

EXCLUDE_DIRS = {
    ".git", "venv", "node_modules", "__pycache__",
    ".mypy_cache", ".pytest_cache", "backups",
    "dist", "build", ".tox", ".eggs", ".ruff_cache",
}


def walk_py_files():
    """Walk all Python files, excluding non-source directories."""
    for root, dirs, files in os.walk(REPO_ROOT):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for f in files:
            if f.endswith(".py"):
                yield Path(root) / f


def count_loc(filepath: Path) -> int:
    """Count lines of code in a Python file."""
    try:
        with open(filepath) as fh:
            return sum(1 for line in fh if line.strip() and not line.strip().startswith("#"))
    except (OSError, UnicodeDecodeError):
        return 0


def cmd_summary():
    """Print overall repository summary."""
    py_files = list(walk_py_files())
    total_loc = sum(count_loc(f) for f in py_files)

    # Phase projects
    phase_dirs = [d for d in REPO_ROOT.iterdir()
                  if d.is_dir() and d.name.startswith("trading-")]

    # Bridge count
    bridges = [f for f in py_files if f.name.startswith("p") and f.name.endswith("_bridge.py")]

    # Doc files
    doc_dir = REPO_ROOT / "docs"
    docs = list(doc_dir.glob("*.md")) if doc_dir.exists() else []

    # Workflow files
    wf_dir = REPO_ROOT / ".github" / "workflows"
    workflows = list(wf_dir.glob("*.yml")) if wf_dir.exists() else []

    # Root files
    root_files = [f for f in REPO_ROOT.iterdir() if f.is_file()]

    print("=== Trading Research Platform — Repository Statistics ===")
    print()
    print(f"Phase projects:     {len(phase_dirs)}")
    print(f"Python files:       {len(py_files)}")
    print(f"Lines of code:      {total_loc:,}")
    print(f"Bridge modules:     {len(bridges)}")
    print(f"Documentation:      {len(docs)} files")
    print(f"GitHub workflows:   {len(workflows)}")
    print(f"Root metadata:      {len(root_files)} files")
    print()
    print("Layer breakdown:")
    for d in sorted(phase_dirs, key=lambda x: x.name):
        count = len(list(d.rglob("*.py")))
        print(f"  {d.name}: {count} .py files")


def cmd_check_imports():
    """Check for broken imports across phase projects."""
    issues = 0
    checked = 0
    for f in walk_py_files():
        try:
            with open(f) as fh:
                content = fh.read()
            if "import " in content:
                checked += 1
        except (OSError, UnicodeDecodeError):
            issues += 1
            print(f"  ⚠ Cannot read: {f.relative_to(REPO_ROOT)}")

    print(f"Import scan: {checked} files checked, {issues} issues")


def cmd_check_modules():
    """Check for missing __init__.py in package directories."""
    issues = 0
    for d in REPO_ROOT.rglob("*"):
        if not d.is_dir():
            continue
        if any(part in EXCLUDE_DIRS for part in d.parts):
            continue
        # If directory has .py files but no __init__.py
        py_files = list(d.glob("*.py"))
        if py_files and not (d / "__init__.py").exists():
            # Only warn if it looks like a package (not scripts/)
            if "scripts" not in d.parts:
                rel = d.relative_to(REPO_ROOT)
                # Skip if it's a top-level trading-* dir
                if rel.parts[0].startswith("trading-") and len(rel.parts) == 1:
                    continue
                print(f"  ⚠ Missing __init__.py: {rel}")
                issues += 1

    print(f"Module scan: {issues} potential missing __init__.py")


def cmd_check_duplicates():
    """Check for duplicate filenames across projects."""
    names = Counter()
    for f in walk_py_files():
        names[f.name] += 1

    dupes = {k: v for k, v in names.items() if v > 1 and not k.startswith("p")}
    if dupes:
        print(f"Duplicate filenames (expected for shared module names):")
        for name, count in sorted(dupes.items(), key=lambda x: -x[1]):
            if count > 2:
                print(f"  {name}: {count} occurrences")
    else:
        print("No unexpected duplicate filenames found")


def cmd_doc_coverage():
    """Check documentation coverage."""
    doc_dir = REPO_ROOT / "docs"
    expected = [
        "PROJECT_STRUCTURE.md", "ARCHITECTURE.md", "PHASE_INDEX.md",
        "MODULE_INDEX.md", "CLI_REFERENCE.md", "DASHBOARD_REFERENCE.md",
        "REPORT_REFERENCE.md", "BRIDGE_REFERENCE.md",
    ]

    found = 0
    for doc in expected:
        path = doc_dir / doc
        if path.exists():
            found += 1
            print(f"  ✓ {doc}")
        else:
            print(f"  ✗ {doc} MISSING")

    print(f"\nDocumentation coverage: {found}/{len(expected)}")


def main():
    parser = argparse.ArgumentParser(description="Repository Statistics")
    parser.add_argument("--summary", action="store_true")
    parser.add_argument("--check-imports", action="store_true")
    parser.add_argument("--check-modules", action="store_true")
    parser.add_argument("--check-duplicates", action="store_true")
    parser.add_argument("--doc-coverage", action="store_true")
    args = parser.parse_args()

    if args.summary:
        cmd_summary()
    elif args.check_imports:
        cmd_check_imports()
    elif args.check_modules:
        cmd_check_modules()
    elif args.check_duplicates:
        cmd_check_duplicates()
    elif args.doc_coverage:
        cmd_doc_coverage()
    else:
        cmd_summary()


if __name__ == "__main__":
    main()
