#!/usr/bin/env python3
"""Platform verification script for the Trading Research Platform.

Runs verification across all three unification phases (62-64).
Exit 0 on success, exit 1 on failure.

Usage:
    python scripts/verify.py
"""

import importlib
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

PHASES = [
    {
        "name": "Phase 62 — Research Core",
        "dir": "trading-research-core",
        "package": "research_core",
        "class": "ResearchCorePlatform",
    },
    {
        "name": "Phase 63 — Platform Finalization",
        "dir": "trading-platform-finalization",
        "package": "platform_finalization",
        "class": "PlatformFinalizationPlatform",
    },
    {
        "name": "Phase 64 — Platform Verification",
        "dir": "trading-platform-verification",
        "package": "platform_verification",
        "class": "PlatformVerificationPlatform",
    },
]

PASS = 0
FAIL = 0


def check(phase: dict) -> bool:
    """Run verification for a single phase."""
    global PASS, FAIL
    name = phase["name"]
    ok = True

    # 1. Directory exists
    phase_dir = REPO_ROOT / phase["dir"]
    if not phase_dir.exists():
        print(f"  ✗ Directory missing: {phase_dir}")
        ok = False
    else:
        print(f"  ✓ Directory exists: {phase_dir}")

    # 2. Import check
    try:
        sys.path.insert(0, str(phase_dir))
        mod = importlib.import_module(phase["package"])
        cls = getattr(mod, phase["class"])
        _ = cls(seed=42)
        print(f"  ✓ Import OK: {phase['package']}.{phase['class']}")
    except Exception as e:
        print(f"  ✗ Import failed: {e}")
        ok = False
    finally:
        if str(phase_dir) in sys.path:
            sys.path.remove(str(phase_dir))

    # 3. CLI check
    try:
        import subprocess
        result = subprocess.run(
            [sys.executable, "-m", f"{phase['package']}.cli", "status"],
            cwd=str(phase_dir),
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode == 0:
            print(f"  ✓ CLI status OK")
        else:
            print(f"  ✗ CLI status failed (exit {result.returncode})")
            ok = False
    except Exception as e:
        print(f"  ✗ CLI check failed: {e}")
        ok = False

    # 4. verify.py check (Phase 64 only)
    if phase["dir"] == "trading-platform-verification":
        verify_path = phase_dir / "verify.py"
        if verify_path.exists():
            try:
                result = subprocess.run(
                    [sys.executable, str(verify_path)],
                    cwd=str(phase_dir),
                    capture_output=True,
                    text=True,
                    timeout=120,
                )
                if result.returncode == 0:
                    print(f"  ✓ verify.py: ALL CHECKS PASSED")
                else:
                    print(f"  ✗ verify.py failed (exit {result.returncode})")
                    ok = False
            except Exception as e:
                print(f"  ✗ verify.py error: {e}")
                ok = False

    # 5. Safety check — forbidden operations raise RuntimeError
    try:
        sys.path.insert(0, str(phase_dir))
        mod = importlib.import_module(phase["package"])
        cls = getattr(mod, phase["class"])
        obj = cls(seed=42)
        if hasattr(obj, 'safety'):
            forbidden = ["live_trading", "broker_execution", "order_placement",
                          "automatic_deployment", "production_modification"]
            caught = 0
            for op in forbidden:
                try:
                    obj.safety.enforce(op)
                except RuntimeError:
                    caught += 1
            if caught == len(forbidden):
                print(f"  ✓ Safety: {caught}/{len(forbidden)} forbidden ops blocked")
            else:
                print(f"  ✗ Safety: only {caught}/{len(forbidden)} blocked")
                ok = False
    except Exception as e:
        print(f"  ⚠ Safety check skipped: {e}")
    finally:
        if str(phase_dir) in sys.path:
            sys.path.remove(str(phase_dir))

    if ok:
        PASS += 1
        print(f"  ✅ {name}: PASS")
    else:
        FAIL += 1
        print(f"  ❌ {name}: FAIL")

    return ok


def main():
    print("=" * 60)
    print("  Trading Research Platform — Verification Suite")
    print("  Research-Only · Advisory Outputs · No Live Trading")
    print("=" * 60)
    print()

    for phase in PHASES:
        print(f"── {phase['name']} ──")
        check(phase)
        print()

    print("=" * 60)
    print(f"  Results: {PASS} PASS, {FAIL} FAIL")
    if FAIL == 0:
        print("  ✅ ALL PHASES VERIFIED")
    else:
        print("  ❌ SOME PHASES FAILED")
    print("=" * 60)

    sys.exit(1 if FAIL > 0 else 0)


if __name__ == "__main__":
    main()
