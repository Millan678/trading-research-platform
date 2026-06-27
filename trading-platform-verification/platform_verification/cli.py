"""CLI — command-line interface for the Platform Verification suite."""
import argparse, sys, json


def _status(args):
    from .safety import FORBIDDEN, all_forbidden, audit
    print("Status: ACTIVE")
    print(f"  Forbidden: {len(FORBIDDEN)}")
    a = audit()
    print(f"  Blocked: {a['total_blocked']}")
    print(f"  Advisory only: True")


def _verify(args):
    from .storage import Storage
    from .validation_engine import ValidationEngine
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        s = Storage(td)
        ve = ValidationEngine(s, seed=42)
        r = ve.validate_all(seed=42)
        print(json.dumps(r, indent=2, default=str))


def _integrity(args):
    from .storage import Storage
    from .integrity_validator import IntegrityValidator
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        s = Storage(td)
        iv = IntegrityValidator(s, seed=42)
        r = iv.check_all(seed=42)
        print(json.dumps(r, indent=2, default=str))


def _determinism(args):
    from .storage import Storage
    from .determinism_validator import DeterminismValidator
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        s = Storage(td)
        dv = DeterminismValidator(s, seed=42)
        r = dv.validate_all(seed=42)
        print(json.dumps(r, indent=2, default=str))


def _reproducibility(args):
    from .storage import Storage
    from .reproducibility_validator import ReproducibilityValidator
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        s = Storage(td)
        rv = ReproducibilityValidator(s, seed=42)
        r = rv.validate_all(seed=42)
        print(json.dumps(r, indent=2, default=str))


def _stress(args):
    from .storage import Storage
    from .stress_test_engine import StressTestEngine
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        s = Storage(td)
        se = StressTestEngine(s, seed=42)
        r = se.run_all(seed=42)
        print(json.dumps(r, indent=2, default=str))


def _certify(args):
    from .storage import Storage
    from .certification_engine import CertificationEngine
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        s = Storage(td)
        ce = CertificationEngine(s, seed=42)
        r = ce.compute_all(seed=42)
        print(json.dumps(r, indent=2, default=str))


def _health(args):
    from .storage import Storage
    from .bridge_validator import BridgeValidator
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        s = Storage(td)
        bv = BridgeValidator(s, seed=42)
        r = bv.validate_all(phases=63, seed=42)
        print(json.dumps(r, indent=2, default=str))


def _report(args):
    print(json.dumps({"phase": 64, "type": "platform_verification", "advisory_only": True}, indent=2))


COMMANDS = {
    "status": _status,
    "verify": _verify,
    "integrity": _integrity,
    "determinism": _determinism,
    "reproducibility": _reproducibility,
    "stress": _stress,
    "certify": _certify,
    "health": _health,
    "report": _report,
}


def main():
    p = argparse.ArgumentParser(description="Phase 64 Platform Verification CLI")
    p.add_argument("command", choices=list(COMMANDS.keys()))
    args = p.parse_args()
    COMMANDS[args.command](args)


if __name__ == "__main__":
    main()
