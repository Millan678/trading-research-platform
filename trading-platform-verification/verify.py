#!/usr/bin/env python3
"""Full verification suite for Phase 64 Platform Verification."""
import json, os, sys, tempfile, subprocess

errors = []

print("=" * 60)
print("PHASE 64 — PLATFORM VERIFICATION TEST SUITE")
print("=" * 60)

# ─── CHECK 1: All modules import successfully ───
print("\n[1/11] All modules import successfully")
try:
    from platform_verification import (
        SafetyValidator, BackupManager, Storage,
        VerificationRegistry, ValidationEngine,
        IntegrationValidator, DependencyValidator, InterfaceValidator, BridgeValidator,
        DeterminismValidator, ReproducibilityValidator, ConsistencyValidator, IntegrityValidator,
        StressTestEngine, LoadTestEngine, ScalabilityValidator,
        FaultInjection, FailureRecoveryValidator,
        ConfigurationValidator, StorageValidator, BackupValidator,
        SecurityValidator, ComplianceValidator,
        PlatformAuditor, AcceptanceEngine, CertificationEngine,
        DashboardBridge, Reports,
        PlatformVerificationPlatform,
        FORBIDDEN, enforce, is_forbidden, all_forbidden, audit,
        PlatformVerificationBlocked,
        VALIDATION_DOMAINS, CERTIFICATION_METRICS, REQUIRED_REPORTS, DASHBOARD_PAGES,
        CertificationLevel,
    )
    print("  ✓ All 33+ symbols imported")
except Exception as e:
    errors.append(f"CHECK 1: Import failed: {e}")
    print(f"  ✗ Import failed: {e}")

# ─── CHECK 2: SQLite backend functions ───
print("\n[2/11] SQLite backend functions")
try:
    with tempfile.TemporaryDirectory() as td:
        s = Storage(td)
        s.append("test", "key1", {"value": 42})
        records = s.read("test")
        assert len(records) == 1
        assert records[0]["value"] == 42
        print("  ✓ SQLite write/read works")
except Exception as e:
    errors.append(f"CHECK 2: SQLite failed: {e}")
    print(f"  ✗ SQLite failed: {e}")

# ─── CHECK 3: JSON mirror functions ───
print("\n[3/11] JSON mirror functions")
try:
    with tempfile.TemporaryDirectory() as td:
        s = Storage(td)
        s.append("mirror_test", "key1", {"mirror": True})
        mirror_file = os.path.join(td, "json_mirror", "mirror_test", "key1.json")
        assert os.path.isfile(mirror_file), f"Mirror file not found: {mirror_file}"
        with open(mirror_file) as f:
            data = json.load(f)
        # data is a list of entries, each with {"data": {...}, "sha256": ..., "created_at": ...}
        assert isinstance(data, list) and len(data) >= 1
        assert data[0]["data"]["mirror"] is True
        print("  ✓ JSON mirror write/read works")
except Exception as e:
    errors.append(f"CHECK 3: JSON mirror failed: {e}")
    print(f"  ✗ JSON mirror failed: {e}")

# ─── CHECK 4: PostgreSQL fallback is graceful ───
print("\n[4/11] PostgreSQL fallback is graceful")
try:
    with tempfile.TemporaryDirectory() as td:
        s = Storage(td, pg_url="postgresql://invalid:***@nonexistent:5432/fake")
        s.append("pg_test", "key1", {"pg_fallback": True})
        # Should not crash — graceful fallback to SQLite
        records = s.read("pg_test")
        assert len(records) == 1
        pg_status = s.try_postgresql()
        assert "fallback" in pg_status.get("status", "")
        print("  ✓ PostgreSQL graceful fallback works")
except Exception as e:
    errors.append(f"CHECK 4: PG fallback failed: {e}")
    print(f"  ✗ PG fallback failed: {e}")

# ─── CHECK 5: Backup integrity passes SHA-256 ───
print("\n[5/11] Backup integrity passes SHA-256")
try:
    with tempfile.TemporaryDirectory() as td:
        bm = BackupManager(td)
        info = bm.create_backup()
        assert "sha256" in info
        assert bm.verify_backup(info)
        print(f"  ✓ Backup SHA-256 verified: {info['sha256'][:16]}...")
except Exception as e:
    errors.append(f"CHECK 5: Backup failed: {e}")
    print(f"  ✗ Backup failed: {e}")

# ─── CHECK 6: CLI commands exit successfully ───
print("\n[6/11] CLI commands exit successfully")
try:
    cli_cmds = ["status", "verify", "integrity", "determinism", "reproducibility",
                "stress", "certify", "health", "report"]
    for cmd in cli_cmds:
        r = subprocess.run(
            [sys.executable, "-m", "platform_verification.cli", cmd],
            capture_output=True, timeout=30,
            cwd="/root/projects/trading-platform-verification"
        )
        if r.returncode != 0:
            raise RuntimeError(f"CLI '{cmd}' exited {r.returncode}: {r.stderr.decode()[:200]}")
    print(f"  ✓ All {len(cli_cmds)} CLI commands exit 0")
except Exception as e:
    errors.append(f"CHECK 6: CLI failed: {e}")
    print(f"  ✗ CLI failed: {e}")

# ─── CHECK 7: Determinism validation passes ───
print("\n[7/11] Determinism validation passes")
try:
    with tempfile.TemporaryDirectory() as td:
        s = Storage(td)
        dv = DeterminismValidator(s, seed=42)
        r1 = dv.validate_all(seed=42)
        dv2 = DeterminismValidator(s, seed=42)
        r2 = dv2.validate_all(seed=42)
        assert r1["integrity_hash"] == r2["integrity_hash"], \
            f"Hashes differ: {r1['integrity_hash']} vs {r2['integrity_hash']}"
        print(f"  ✓ Determinism verified: {r1['integrity_hash']}")
except Exception as e:
    errors.append(f"CHECK 7: Determinism failed: {e}")
    print(f"  ✗ Determinism failed: {e}")

# ─── CHECK 8: Reproducibility validation passes ───
print("\n[8/11] Reproducibility validation passes")
try:
    with tempfile.TemporaryDirectory() as td:
        s = Storage(td)
        rv = ReproducibilityValidator(s, seed=42)
        r1 = rv.validate_all(seed=42)
        rv2 = ReproducibilityValidator(s, seed=42)
        r2 = rv2.validate_all(seed=42)
        assert r1["integrity_hash"] == r2["integrity_hash"]
        print(f"  ✓ Reproducibility verified: {r1['integrity_hash']}")
except Exception as e:
    errors.append(f"CHECK 8: Reproducibility failed: {e}")
    print(f"  ✗ Reproducibility failed: {e}")

# ─── CHECK 9: Stress tests complete successfully ───
print("\n[9/11] Stress tests complete successfully")
try:
    with tempfile.TemporaryDirectory() as td:
        s = Storage(td)
        se = StressTestEngine(s, seed=42)
        r = se.run_all(seed=42)
        assert r["tests_run"] == 8
        print(f"  ✓ {r['tests_run']} stress tests completed")
except Exception as e:
    errors.append(f"CHECK 9: Stress tests failed: {e}")
    print(f"  ✗ Stress tests failed: {e}")

# ─── CHECK 10: Dashboard JSON validates ───
print("\n[10/11] Dashboard JSON validates")
try:
    base = "/tmp/p64_verify_dash"
    os.makedirs(base, exist_ok=True)
    db = DashboardBridge(base)
    db.export({"test": {"advisory_only": True}})
    assert db.validate()
    assert db.count() == 10
    print(f"  ✓ {db.count()} dashboard pages validate")
except Exception as e:
    errors.append(f"CHECK 10: Dashboard failed: {e}")
    print(f"  ✗ Dashboard failed: {e}")

# ─── CHECK 11: Reports generate successfully ───
print("\n[11/11] Reports generate successfully")
try:
    base = "/tmp/p64_verify_rpt"
    os.makedirs(base, exist_ok=True)
    rpt = Reports(base)
    result = rpt.generate_all({"test": True})
    assert result["total_generated"] == 8
    for rid in REQUIRED_REPORTS:
        slug = rid.lower()
        jpath = os.path.join(base, "reports", f"{slug}.json")
        mpath = os.path.join(base, "reports", f"{slug}.md")
        assert os.path.isfile(jpath), f"Missing JSON: {jpath}"
        assert os.path.isfile(mpath), f"Missing MD: {mpath}"
        with open(jpath) as f:
            json.load(f)
    print(f"  ✓ {result['total_generated']} reports generated (JSON + MD)")
except Exception as e:
    errors.append(f"CHECK 11: Reports failed: {e}")
    print(f"  ✗ Reports failed: {e}")

# ─── SAFETY: 8 forbidden ops raise RuntimeError ───
print("\n[BONUS] Safety: all forbidden operations raise RuntimeError")
try:
    forbidden_ops = [
        "live_trading", "broker_execution", "order_placement",
        "automatic_deployment", "production_modification",
        "automatic_strategy_approval", "governance_bypass", "evaluation_bypass",
    ]
    blocked = 0
    for op in forbidden_ops:
        try:
            enforce(op)
        except PlatformVerificationBlocked:
            blocked += 1
    assert blocked == len(forbidden_ops), f"Only {blocked}/{len(forbidden_ops)} blocked"
    print(f"  ✓ {blocked}/{len(forbidden_ops)} forbidden operations raise RuntimeError")
except Exception as e:
    errors.append(f"SAFETY: {e}")
    print(f"  ✗ Safety failed: {e}")

# ─── RESULTS ───
print("\n" + "=" * 60)
if not errors:
    print("ALL 11/11 CHECKS PASSED ✅")
    print("SAFETY: 8/8 FORBIDDEN OPERATIONS BLOCKED ✅")
else:
    for e in errors:
        print(f"  FAIL: {e}")
    print(f"\n{len(errors)} CHECK(S) FAILED ❌")
    sys.exit(1)
print("=" * 60)
