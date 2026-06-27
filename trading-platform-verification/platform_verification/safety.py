"""Safety — 8 forbidden operations with structural RuntimeError enforcement."""
import hashlib, json
from datetime import datetime
from typing import Any, Dict, List


class PlatformVerificationBlocked(RuntimeError):
    """Raised when a forbidden operation is attempted."""
    pass


FORBIDDEN = [
    "live_trading",
    "broker_execution",
    "order_placement",
    "automatic_deployment",
    "production_modification",
    "automatic_strategy_approval",
    "governance_bypass",
    "evaluation_bypass",
]


def enforce(operation: str) -> None:
    if operation in FORBIDDEN:
        raise PlatformVerificationBlocked(
            f"FORBIDDEN: {operation} — platform verification is research-only"
        )


def is_forbidden(operation: str) -> bool:
    return operation in FORBIDDEN


def all_forbidden() -> List[str]:
    return list(FORBIDDEN)


def audit() -> Dict[str, Any]:
    blocked_ops = []
    for op in FORBIDDEN:
        try:
            enforce(op)
        except PlatformVerificationBlocked:
            blocked_ops.append(op)
    return {
        "total_forbidden": len(FORBIDDEN),
        "total_blocked": len(blocked_ops),
        "all_blocked": len(blocked_ops) == len(FORBIDDEN),
        "advisory_only": True,
        "audited_at": datetime.utcnow().isoformat(),
    }
