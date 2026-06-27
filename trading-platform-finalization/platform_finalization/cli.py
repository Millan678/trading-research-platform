"""CLI — command-line interface for the Platform Finalization layer."""
import argparse, sys, json


def _status(args):
    from .safety import FORBIDDEN, all_forbidden, audit
    print("Status: ACTIVE")
    print(f"  Forbidden: {len(FORBIDDEN)}")
    a = audit()
    print(f"  Blocked: {a['total_blocked']}")
    print(f"  Advisory only: True")


def _architecture(args):
    from .storage import Storage
    from .architecture_validator import ArchitectureValidator
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        s = Storage(td)
        av = ArchitectureValidator(s, seed=42)
        r = av.validate_all(seed=42)
        print(json.dumps(r, indent=2, default=str))


def _dependencies(args):
    from .storage import Storage
    from .dependency_validator import DependencyValidator
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        s = Storage(td)
        dv = DependencyValidator(s, seed=42)
        r = dv.validate_all(seed=42)
        print(json.dumps(r, indent=2, default=str))


def _optimization(args):
    from .storage import Storage
    from .optimization_engine import OptimizationEngine
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        s = Storage(td)
        oe = OptimizationEngine(s, seed=42)
        r = oe.analyze_all(seed=42)
        print(json.dumps(r, indent=2, default=str))


def _documentation(args):
    from .storage import Storage
    from .documentation_generator import DocumentationGenerator
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        s = Storage(td)
        dg = DocumentationGenerator(s, seed=42)
        r = dg.generate_all(seed=42)
        print(json.dumps(r, indent=2, default=str))


def _certification(args):
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
    from .health_monitor import HealthMonitor
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        s = Storage(td)
        hm = HealthMonitor(s, seed=42)
        r = hm.check_all(seed=42)
        print(json.dumps(r, indent=2, default=str))


def _report(args):
    print(json.dumps({"phase": 63, "type": "platform_finalization", "advisory_only": True}, indent=2))


COMMANDS = {
    "status": _status,
    "architecture": _architecture,
    "dependencies": _dependencies,
    "optimization": _optimization,
    "documentation": _documentation,
    "certification": _certification,
    "health": _health,
    "report": _report,
}


def main():
    p = argparse.ArgumentParser(description="Phase 63 Platform Finalization CLI")
    p.add_argument("command", choices=list(COMMANDS.keys()))
    args = p.parse_args()
    COMMANDS[args.command](args)


if __name__ == "__main__":
    main()
