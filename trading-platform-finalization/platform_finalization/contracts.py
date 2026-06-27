"""Contracts — shared types, enumerations, and constants for Phase 63."""
from enum import Enum
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


class ValidationStatus(Enum):
    PASS = "pass"
    WARN = "warn"
    FAIL = "fail"


class OptimizationType(Enum):
    PERFORMANCE = "performance"
    MEMORY = "memory"
    STORAGE = "storage"
    REDUNDANCY = "redundancy"
    COMPLEXITY = "complexity"


class CertificationLevel(Enum):
    DRAFT = "draft"
    VALIDATED = "validated"
    CERTIFIED = "certified"
    FINAL = "final"


ARCHITECTURE_DOMAINS = [
    "module_dependencies", "import_integrity", "bridge_integrity",
    "storage_compatibility", "configuration_compatibility",
    "interface_compatibility", "historical_compatibility",
    "api_compatibility", "version_compatibility", "subsystem_compatibility",
]

REQUIRED_REPORTS = [
    "PHASE63_PLATFORM_FINALIZATION_READINESS_REPORT",
    "ARCHITECTURE_REPORT",
    "DEPENDENCY_REPORT",
    "COMPATIBILITY_REPORT",
    "OPTIMIZATION_REPORT",
    "DOCUMENTATION_REPORT",
    "CERTIFICATION_REPORT",
    "PLATFORM_HEALTH_REPORT",
]

DASHBOARD_PAGES = [
    "Platform Overview", "Architecture", "Dependencies",
    "Capabilities", "Optimization", "Documentation",
    "Certification", "Compatibility", "Subsystem Health",
    "Platform Health",
]

DOCUMENTATION_TYPES = [
    "Architecture Overview", "Dependency Graph", "Capability Catalog",
    "API Catalog", "Subsystem Catalog", "Bridge Catalog",
    "Storage Catalog", "Dashboard Catalog", "Report Catalog",
    "Platform Reference Manual",
]

CERTIFICATION_METRICS = [
    "architecture_completeness", "platform_stability",
    "research_readiness", "scientific_coverage",
    "safety_compliance", "documentation_coverage",
    "maintainability", "scalability",
    "reproducibility", "platform_quality",
]
