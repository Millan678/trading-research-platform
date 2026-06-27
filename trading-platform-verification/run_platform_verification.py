#!/usr/bin/env python3
"""Run Phase 64 — End-to-End Autonomous Research Platform Validation, Verification & Scientific Acceptance Suite."""
import sys, os, json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from platform_verification.main import PlatformVerificationPlatform

def main():
    base_dir = sys.argv[1] if len(sys.argv) > 1 else "/tmp/p64_output"
    platform = PlatformVerificationPlatform(base_dir, seed=42)
    # Run once for main results
    results = platform.run(seed=42)
    # Run a second time with same seed for determinism check
    results2 = platform.run(seed=42)
    determinism_ok = results["overall_hash"] == results2["overall_hash"]
    # Build summary from first run
    cert = results.get("certification", {})
    accept = results.get("acceptance", {})
    summary = {
        "phase": 64,
        "phases_validated": results["phases_validated"],
        "modules_validated": results["modules_validated"],
        "bridges_validated": results["bridges_validated"],
        "determinism_score": results["determinism"].get("determinism_score", 0),
        "reproducibility_score": results["reproducibility"].get("reproducibility_score", 0),
        "certification_level": cert.get("certification_level", "UNKNOWN"),
        "acceptance_score": accept.get("overall_acceptance_score", 0),
        "overall_hash": results["overall_hash"],
        "determinism_verified": determinism_ok,
        "advisory_only": True,
    }
    print(json.dumps(summary, indent=2, default=str))

if __name__ == "__main__":
    main()
