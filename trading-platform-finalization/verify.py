#!/usr/bin/env python3
"""Full verification suite for Phase 63 Platform Finalization."""
import json, os, sys, tempfile

errors = []

print("=" * 60)
print("CHECK 1: All modules import successfully")
print("=" * 60)
try:
    from platform_finalization import (
        FORBIDDEN, enforce, is_forbidden, all_forbidden, audit, PlatformFinalizationBlocked,
        BackupManager, Storage,
        ValidationStatus, OptimizationType, CertificationLevel,
        ARCHITECTURE_DOMAINS, REQUIRED_REPORTS, DASHBOARD_PAGES,
        DOCUMENTATION_TYPES, CERTIFICATION_METRICS,
        PlatformRegistry, ArchitectureValidator, DependencyValidator,
        CompatibilityValidator, InterfaceValidator,
        OptimizationEngine, PerformanceOptimizer, StorageOptimizer, MemoryOptimizer,
        ConsistencyChecker, IntegrityChecker, RedundancyDetector,
        APIRegistry, CapabilityRegistry,
        DocumentationGenerator, ArchitectureExport, DependencyMapper,
        BenchmarkValidator, CertificationEngine, ReleaseValidator,
        HealthMonitor, ReadinessEngine,
        DashboardBridge, Reports,
    )
    # Bridge spot-check
    for phase in [1, 30, 62]:
        import importlib
        mod = importlib.import_module(f"platform_finalization.p{phase:02d}_bridge")
        cls = getattr(mod, f"Phase{phase:02d}Bridge")
        cls.__name__
    print("  ALL IMPORTS OK (28 direct + 3 bridge spot-checks)")
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
        bm = BackupManager(td)
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
    cmds = ["status", "architecture", "dependencies", "optimization", "documentation", "certification", "health", "report"]
    for cmd in cmds:
        r = subprocess.run(
            [sys.executable, "-m", "platform_finalization.cli", cmd],
            capture_output=True, timeout=10,
            cwd="/root/projects/trading-platform-finalization",
        )
        assert r.returncode == 0, f"CLI {cmd} failed: {r.returncode}"
    print(f"  OK — {len(cmds)}/{len(cmds)} commands passed")
except Exception as e:
    errors.append(f"CLI: {e}")
    print(f"  FAIL: {e}")

print()
print("=" * 60)
print("CHECK 7: Architecture validation is deterministic")
print("=" * 60)
try:
    with tempfile.TemporaryDirectory() as td1, tempfile.TemporaryDirectory() as td2:
        s1 = Storage(td1); s2 = Storage(td2)
        av1 = ArchitectureValidator(s1, seed=42); av2 = ArchitectureValidator(s2, seed=42)
        r1 = av1.validate_all(seed=42)
        r2 = av2.validate_all(seed=42)
        assert r1 == r2, f"Architecture not deterministic: {r1} != {r2}"
        print(f"  OK — architecture_score={r1['architecture_score']}")
except Exception as e:
    errors.append(f"Architecture: {e}")
    print(f"  FAIL: {e}")

print()
print("=" * 60)
print("CHECK 8: Dependency analysis is deterministic")
print("=" * 60)
try:
    with tempfile.TemporaryDirectory() as td1, tempfile.TemporaryDirectory() as td2:
        s1 = Storage(td1); s2 = Storage(td2)
        dv1 = DependencyValidator(s1, seed=42); dv2 = DependencyValidator(s2, seed=42)
        r1 = dv1.validate_all(seed=42)
        r2 = dv2.validate_all(seed=42)
        assert r1 == r2, f"Dependency not deterministic: {r1} != {r2}"
        print(f"  OK — dependencies_validated={r1['dependencies_validated']}")
except Exception as e:
    errors.append(f"Dependency: {e}")
    print(f"  FAIL: {e}")

print()
print("=" * 60)
print("CHECK 9: Certification calculations are deterministic")
print("=" * 60)
try:
    with tempfile.TemporaryDirectory() as td1, tempfile.TemporaryDirectory() as td2:
        s1 = Storage(td1); s2 = Storage(td2)
        ce1 = CertificationEngine(s1, seed=42); ce2 = CertificationEngine(s2, seed=42)
        r1 = ce1.compute_all(seed=42)
        r2 = ce2.compute_all(seed=42)
        assert r1 == r2, f"Certification not deterministic"
        print(f"  OK — platform_quality_score={r1['platform_quality_score']}")
except Exception as e:
    errors.append(f"Certification: {e}")
    print(f"  FAIL: {e}")

print()
print("=" * 60)
print("CHECK 10: Dashboard JSON validates")
print("=" * 60)
try:
    with tempfile.TemporaryDirectory() as td:
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
        rp = Reports(td)
        result = rp.generate_all({"test": True})
        assert len(result["reports"]) == len(REQUIRED_REPORTS), f"Reports mismatch: {len(result['reports'])} != {len(REQUIRED_REPORTS)}"
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
print("CHECK 12: Safety enforcement (10 forbidden operations)")
print("=" * 60)
try:
    assert len(FORBIDDEN) == 10, f"Expected 10 forbidden, got {len(FORBIDDEN)}"
    triggered = 0
    for op in FORBIDDEN:
        try:
            enforce(op)
        except PlatformFinalizationBlocked:
            triggered += 1
    assert triggered == 10, f"Only {triggered}/10 triggered RuntimeError"
    print(f"  OK — {triggered}/10 RuntimeError raised")
except Exception as e:
    errors.append(f"Safety: {e}")
    print(f"  FAIL: {e}")

print()
print("=" * 60)
print("CHECK 13: All 62 bridges import and instantiate")
print("=" * 60)
try:
    with tempfile.TemporaryDirectory() as td:
        s = Storage(td)
        bridge_count = 0
        for phase in range(1, 63):
            import importlib
            mod = importlib.import_module(f"platform_finalization.p{phase:02d}_bridge")
            cls_name = f"Phase{phase:02d}Bridge"
            cls = getattr(mod, cls_name)
            bridge = cls(s, seed=0)
            status = bridge.status(seed=0)
            assert status["bridge_type"] == "read_only", f"P{phase} not read_only"
            bridge_count += 1
        assert bridge_count == 62, f"Only {bridge_count} bridges"
        print(f"  OK — {bridge_count}/62 bridges verified read-only")
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
    print("  Phase 63 verification complete.")
