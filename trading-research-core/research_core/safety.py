"""Safety — 11 forbidden operations with structural RuntimeError enforcement."""
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
    "execution_bypass",
])

class ResearchCoreBlocked(RuntimeError):
    """Raised when a forbidden operation is attempted."""
    pass

def enforce(operation: str) -> None:
    if operation in FORBIDDEN:
        raise ResearchCoreBlocked(f"FORBIDDEN: {operation} — research-only platform")

def is_forbidden(operation: str) -> bool:
    return operation in FORBIDDEN

def all_forbidden() -> list:
    return sorted(FORBIDDEN)

def audit() -> dict:
    return {
        "total_blocked": len(FORBIDDEN),
        "operations": all_forbidden(),
        "enforcement": "RuntimeError",
        "platform": "research_only",
        "advisory_only": True,
    }
