"""CLI — command-line interface for the research core platform."""
import argparse, sys, json


def _status(args):
    from .safety import FORBIDDEN, all_forbidden, audit
    print("Status: ACTIVE")
    print("Mode: RESEARCH_ONLY")
    print("Forbidden operations: {}".format(len(FORBIDDEN)))
    for f in sorted(FORBIDDEN):
        print("  BLOCKED: {}".format(f))
    all_ok = all_forbidden()
    print("All forbidden enforced: {}".format(len(all_ok) == len(FORBIDDEN)))
    audit_result = audit()
    print("Audit: {} blocked / enforcement={}".format(audit_result["total_blocked"], audit_result["enforcement"]))


def _context(args):
    from .contracts import GLOBAL_CONTEXT_CATEGORIES
    print("Global Context Categories: {}".format(len(GLOBAL_CONTEXT_CATEGORIES)))
    for cat in GLOBAL_CONTEXT_CATEGORIES:
        print("  - {}".format(cat))


def _memory(args):
    from .contracts import MemoryType
    print("Memory Types: {}".format(len(MemoryType)))
    for mt in MemoryType:
        print("  - {}".format(mt.value))


def _capabilities(args):
    from .contracts import CapabilityStatus
    print("Capability Statuses: {}".format(len(CapabilityStatus)))
    for cs in CapabilityStatus:
        print("  - {}".format(cs.value))


def _sync(args):
    from .synchronization_engine import SYNC_CHECKS
    print("Synchronization Checks: {}".format(len(SYNC_CHECKS)))
    for sc in SYNC_CHECKS:
        print("  - {}".format(sc))


def _health(args):
    from .safety import audit
    r = audit()
    print("Platform: {}".format(r["platform"]))
    print("Blocked operations: {}".format(r["total_blocked"]))
    print("Enforcement: {}".format(r["enforcement"]))


def _history(args):
    from .contracts import REQUIRED_REPORTS
    print("Required Reports: {}".format(len(REQUIRED_REPORTS)))
    for r in REQUIRED_REPORTS:
        print("  - {}".format(r))


def _report(args):
    from .contracts import REQUIRED_REPORTS
    print("Report Templates: {}".format(len(REQUIRED_REPORTS)))
    for r in REQUIRED_REPORTS:
        print("  - {}".format(r))


CMDS = {
    "status": _status,
    "context": _context,
    "memory": _memory,
    "capabilities": _capabilities,
    "sync": _sync,
    "health": _health,
    "history": _history,
    "report": _report,
}


def main():
    p = argparse.ArgumentParser(prog="research_core.cli")
    p.add_argument("command", choices=sorted(CMDS.keys()))
    args = p.parse_args()
    CMDS[args.command](args)


if __name__ == "__main__":
    main()
