#!/usr/bin/env python3
"""Full verification suite for Phase 62 Unified Research Core Platform."""
import json, os, sys, tempfile

errors = []

print("=" * 60)
print("CHECK 1: All modules import successfully")
print("=" * 60)
try:
    from research_core import (
        FORBIDDEN, enforce, is_forbidden, all_forbidden, audit, ResearchCoreBlocked,
        BackupManager, Storage,
        CouncilStatus, MemoryType, GoalStatus, CapabilityStatus, SyncStatus,
        GLOBAL_CONTEXT_CATEGORIES, REQUIRED_REPORTS, DASHBOARD_PAGES,
        CoreRegistry, GlobalContext, ContextManager,
        MemoryManager, EpisodicMemory, SemanticMemory, ProceduralMemory,
        Planner, GoalManager, ObjectiveManager,
        ReasoningRouter, CapabilityRouter,
        WorkflowManager, LifecycleManager,
        StateManager, SynchronizationEngine,
        ExecutionCoordinator, ResourceCoordinator,
        CapabilityCatalog, SubsystemRegistry,
        HealthMonitor, IntegrityMonitor, RecommendationEngine,
        DashboardBridge, Reports,
    )
    # Lazy-bridge spot check
    for phase in [1, 30, 61]:
        mod = __import__("research_core.p{:02d}_bridge".format(phase), fromlist=["level"])
        cls = getattr(mod, f"Phase{phase:02d}Bridge")
        cls.__name__
    print("  ALL IMPORTS OK (26 direct + 3 bridge spot-checks)")
except Exception as e:
    errors.append(f"Import: {e}")
    print(f"  FAIL: {e}")

print()
print("=" * 60)
print("CHECK 2: SQLite backend functions")
print("=" * 60)
try:
    with tempfile.TemporaryDirectory() as td:
        s = Storage(td)
        s.append("test_sqlite", "verification", {"sqlite": True})
        records = s.read("test_sqlite")
        assert len(records) > 0, "No records returned"
        print(f"  OK — {len(records)} record(s)")
except Exception as e:
    errors.append(f"SQLite: {e}")
    print(f"  FAIL: {e}")

print()
print("=" * 60)
print("CHECK 3: JSON mirror functions")
print("=" * 60)
try:
    with tempfile.TemporaryDirectory() as td:
        s = Storage(td)
        s.append("test_json", "mirror_type", {"mirror": True})
        json_dir = os.path.join(td, "json_mirror")
        assert os.path.isdir(json_dir), f"JSON dir missing: {json_dir}"
        json_files = []
        for root, dirs, files in os.walk(json_dir):
            json_files.extend(f for f in files if f.endswith(".json"))
        assert len(json_files) > 0, "No JSON mirror files found"
        print(f"  OK — {len(json_files)} JSON file(s)")
except Exception as e:
    errors.append(f"JSON mirror: {e}")
    print(f"  FAIL: {e}")

print()
print("=" * 60)
print("CHECK 4: PostgreSQL fallback is graceful")
print("=" * 60)
try:
    with tempfile.TemporaryDirectory() as td:
        s = Storage(td, pg_url="postgresql://nonexistent:5432/fakedb")
        pg_status = s.try_postgresql()
        assert pg_status["status"] == "graceful_fallback", f"Unexpected: {pg_status}"
        print(f"  OK — status={pg_status['status']}")
except Exception as e:
    errors.append(f"PG fallback: {e}")
    print(f"  FAIL: {e}")

print()
print("=" * 60)
print("CHECK 5: Backup integrity passes SHA-256")
print("=" * 60)
try:
    with tempfile.TemporaryDirectory() as td:
        from research_core import BackupManager
        bm = BackupManager(td)
        # Create a file to back up
        with open(os.path.join(td, "test_data.txt"), "w") as f:
            f.write("verification data")
        manifest = bm.create_backup()
        assert bm.verify_backup(manifest), "Backup verification failed"
        assert "sha256" in manifest, "Missing SHA-256 in manifest"
        print(f"  OK — SHA-256 verified, entries={len(manifest.get('entries', []))}")
except Exception as e:
    errors.append(f"Backup: {e}")
    print(f"  FAIL: {e}")

print()
print("=" * 60)
print("CHECK 6: CLI commands exit successfully")
print("=" * 60)
try:
    import subprocess
    cmds = ["status", "context", "memory", "capabilities", "sync", "health", "history", "report"]
    for cmd in cmds:
        r = subprocess.run(
            [sys.executable, "-m", "research_core.cli", cmd],
            capture_output=True, timeout=10,
            cwd="/root/projects/trading-research-core",
        )
        assert r.returncode == 0, f"CLI {cmd} failed: {r.returncode}"
    print(f"  OK — {len(cmds)}/{len(cmds)} commands passed")
except Exception as e:
    errors.append(f"CLI: {e}")
    print(f"  FAIL: {e}")

print()
print("=" * 60)
print("CHECK 7: Global context is deterministic")
print("=" * 60)
try:
    with tempfile.TemporaryDirectory() as td1, tempfile.TemporaryDirectory() as td2:
        from research_core import GlobalContext, Storage
        s1 = Storage(td1); s2 = Storage(td2)
        gc1 = GlobalContext(s1, seed=42); gc2 = GlobalContext(s2, seed=42)
        r1 = gc1.update_domain("test", {"v": 1}, seed=42)
        r2 = gc2.update_domain("test", {"v": 1}, seed=42)
        assert r1 == r2, f"Global context not deterministic: {r1} != {r2}"
        print(f"  OK — deterministic hash={r1.get('integrity_hash', 'N/A')}")
except Exception as e:
    errors.append(f"Global context: {e}")
    print(f"  FAIL: {e}")

print()
print("=" * 60)
print("CHECK 8: Memory retrieval is deterministic")
print("=" * 60)
try:
    with tempfile.TemporaryDirectory() as td1, tempfile.TemporaryDirectory() as td2:
        from research_core import MemoryManager, Storage
        s1 = Storage(td1); s2 = Storage(td2)
        mm1 = MemoryManager(s1, seed=42); mm2 = MemoryManager(s2, seed=42)
        r1 = mm1.store("m1", "episodic", {"k": "v"}, seed=42)
        r2 = mm2.store("m1", "episodic", {"k": "v"}, seed=42)
        # Compare deterministic fields only (timestamps differ across instances)
        det_fields = {k: v for k, v in r1.items() if k != "created_at"}
        det_fields2 = {k: v for k, v in r2.items() if k != "created_at"}
        assert det_fields == det_fields2, f"Memory not deterministic: {det_fields} != {det_fields2}"
        print(f"  OK — deterministic confidence={r1.get('confidence', 'N/A')}")
except Exception as e:
    errors.append(f"Memory: {e}")
    print(f"  FAIL: {e}")

print()
print("=" * 60)
print("CHECK 9: Synchronization is deterministic")
print("=" * 60)
try:
    with tempfile.TemporaryDirectory() as td1, tempfile.TemporaryDirectory() as td2:
        from research_core import SynchronizationEngine, Storage
        s1 = Storage(td1); s2 = Storage(td2)
        se1 = SynchronizationEngine(s1, seed=42); se2 = SynchronizationEngine(s2, seed=42)
        r1 = se1.run_all_checks(seed=42)
        r2 = se2.run_all_checks(seed=42)
        assert r1 == r2, f"Sync not deterministic: {r1} != {r2}"
        print(f"  OK — sync_score={r1.get('sync_score', 'N/A')}")
except Exception as e:
    errors.append(f"Synchronization: {e}")
    print(f"  FAIL: {e}")

print()
print("=" * 60)
print("CHECK 10: Dashboard JSON validates")
print("=" * 60)
try:
    with tempfile.TemporaryDirectory() as td:
        from research_core import DashboardBridge
        db = DashboardBridge(td)
        db.export({t.lower().replace(" ", "_"): {"advisory_only": True} for t in DASHBOARD_PAGES})
        assert db.validate(), "Dashboard validation failed"
        print(f"  OK — {db.count()} pages validated")
except Exception as e:
    errors.append(f"Dashboard: {e}")
    print(f"  FAIL: {e}")

print()
print("=" * 60)
print("CHECK 11: Reports generate successfully")
print("=" * 60)
try:
    with tempfile.TemporaryDirectory() as td:
        from research_core import Reports
        rp = Reports(td)
        result = rp.generate_all({"test": True})
        assert len(result["reports"]) == len(REQUIRED_REPORTS), f"Reports mismatch: {len(result['reports'])} != {len(REQUIRED_REPORTS)}"
        # Check files exist
        for report_id in REQUIRED_REPORTS:
            slug = report_id.lower()
            jpath = os.path.join(td, "reports", f"{slug}.json")
            mpath = os.path.join(td, "reports", f"{slug}.md")
            assert os.path.isfile(jpath), f"Missing JSON: {jpath}"
            assert os.path.isfile(mpath), f"Missing MD: {mpath}"
        print(f"  OK — {len(result['reports'])} reports generated")
except Exception as e:
    errors.append(f"Reports: {e}")
    print(f"  FAIL: {e}")

print()
print("=" * 60)
print("CHECK 12: Safety enforcement (11 forbidden operations)")
print("=" * 60)
try:
    from research_core import enforce, ResearchCoreBlocked
    assert len(FORBIDDEN) == 11, f"Expected 11 forbidden, got {len(FORBIDDEN)}"
    triggered = 0
    for op in FORBIDDEN:
        try:
            enforce(op)
        except ResearchCoreBlocked:
            triggered += 1
    assert triggered == 11, f"Only {triggered}/11 triggered RuntimeError"
    print(f"  OK — {triggered}/11 RuntimeError raised")
except Exception as e:
    errors.append(f"Safety: {e}")
    print(f"  FAIL: {e}")

print()
print("=" * 60)
print("CHECK 13: All 61 bridges import and instantiate")
print("=" * 60)
try:
    with tempfile.TemporaryDirectory() as td:
        s = Storage(td)
        bridge_count = 0
        for phase in range(1, 62):
            import importlib
            mod = importlib.import_module(f"research_core.p{phase:02d}_bridge")
            cls_name = f"Phase{phase:02d}Bridge"
            cls = getattr(mod, cls_name)
            bridge = cls(s, seed=0)
            status = bridge.status(seed=0)
            assert status["bridge_type"] == "read_only", f"P{phase} not read_only"
            bridge_count += 1
        assert bridge_count == 61, f"Only {bridge_count} bridges"
        print(f"  OK — {bridge_count}/61 bridges verified read-only")
except Exception as e:
    errors.append(f"Bridges: {e}")
    print(f"  FAIL: {e}")

print()
print("=" * 60)
summary = "ALL 13 CHECKS PASSED" if not errors else f"{len(errors)} CHECK(S) FAILED"
print(f"RESULT: {summary}")
if errors:
    for e in errors:
        print(f"  FAILED: {e}")
    sys.exit(1)
else:
    print("  Phase 62 verification complete.")
