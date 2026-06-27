"""Safety — 10 forbidden operations with structural RuntimeError enforcement."""
FORBIDDEN = frozenset([
    "live_trading",
    "broker_execution",
    "order_execution",
    "automatic_strategy_creation",
    "automatic_strategy_deployment",
    "automatic_strategy_approval",
    "production_modification",
    "governance_bypass",
    "evaluation_bypass",
    "research_history_modification",
])


class PlatformFinalizationBlocked(RuntimeError):
    """Raised when a forbidden operation is attempted."""
    pass


def enforce(operation: str):
    """Raise RuntimeError immediately if operation is forbidden."""
    if operation in FORBIDDEN:
        raise PlatformFinalizationBlocked(
            f"FORBIDDEN: {operation} — Platform Finalization is research-only"
        )


def is_forbidden(operation: str) -> bool:
    return operation in FORBIDDEN


def all_forbidden() -> list:
    return sorted(FORBIDDEN)


def audit() -> dict:
    checks = {op: is_forbidden(op) for op in FORBIDDEN}
    return {
        "total_forbidden": len(FORBIDDEN),
        "total_blocked": sum(1 for v in checks.values() if v),
        "checks": checks,
        "advisory_only": True,
    }
