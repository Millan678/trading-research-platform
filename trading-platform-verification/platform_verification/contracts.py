"""Contracts — enums, constants, and shared types."""
from enum import Enum
from typing import Any, Dict, List


class ValidationStatus(Enum):
    PASS = "pass"
    WARN = "warn"
    FAIL = "fail"


class CertificationLevel(Enum):
    NOT_CERTIFIED = "NOT CERTIFIED"
    CERTIFIED_WITH_OBSERVATIONS = "CERTIFIED WITH OBSERVATIONS"
    CERTIFIED = "CERTIFIED"


VALIDATION_DOMAINS = [
    "imports", "interfaces", "dependencies", "storage", "backups",
    "dashboards", "reports", "cli", "cross_phase", "configuration",
    "data_integrity", "historical_integrity", "determinism", "reproducibility",
    "stress", "safety", "compliance", "security",
]

CERTIFICATION_METRICS = [
    "platform_integrity", "platform_stability", "determinism",
    "reproducibility", "reliability", "maintainability",
    "scalability", "documentation_quality", "safety_compliance",
    "scientific_readiness", "overall_acceptance",
]

REQUIRED_REPORTS = [
    "PHASE64_PLATFORM_VERIFICATION_READINESS_REPORT",
    "PLATFORM_AUDIT_REPORT",
    "DETERMINISM_REPORT",
    "REPRODUCIBILITY_REPORT",
    "SAFETY_REPORT",
    "STRESS_TEST_REPORT",
    "CERTIFICATION_REPORT",
    "PLATFORM_ACCEPTANCE_REPORT",
]

DASHBOARD_PAGES = [
    "Platform Verification", "Integration Status", "Determinism",
    "Reproducibility", "Stress Tests", "Safety",
    "Certification", "Acceptance", "Platform Audit", "Overall Health",
]
