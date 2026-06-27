"""Contracts — shared types, enumerations, and constants for Phase 62."""
from enum import Enum
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


class CouncilStatus(Enum):
    ACTIVE = "active"
    IN_REVIEW = "in_review"
    RATIFIED = "ratified"
    AMENDED = "amended"
    ARCHIVED = "archived"

class MemoryType(Enum):
    EPISODIC = "episodic"
    SEMANTIC = "semantic"
    PROCEDURAL = "procedural"
    WORKING = "working"
    LONG_TERM = "long_term"

class GoalStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class CapabilityStatus(Enum):
    AVAILABLE = "available"
    DEGRADED = "degraded"
    UNAVAILABLE = "unavailable"

class SyncStatus(Enum):
    SYNCHRONIZED = "synchronized"
    DEGRADED = "degraded"
    FAILED = "failed"

CONTEXT_DOMAINS = [
    "research", "reasoning", "evidence", "knowledge", "discovery",
    "governance", "evaluation", "benchmarking", "calibration", "consensus",
    "institution", "observatory", "digital_twin", "scientific_impact",
    "constitution", "platform_intelligence",
]

CONSTITUTION_ARTICLES = [
    "research_integrity", "scientific_method", "peer_review",
    "transparency", "reproducibility", "ethical_compliance",
    "advisory_only", "no_live_trading", "no_production_modification",
    "immutable_history",
]

GLOBAL_CONTEXT_CATEGORIES = [
    "research", "reasoning", "evidence", "knowledge", "discovery",
    "governance", "evaluation", "benchmarking", "calibration", "consensus",
    "institution", "observatory", "digital_twin", "scientific_impact",
    "constitution", "platform_intelligence",
]

REQUIRED_REPORTS = [
    "PHASE62_RESEARCH_CORE_READINESS_REPORT",
    "GLOBAL_CONTEXT_REPORT",
    "MEMORY_REPORT",
    "CAPABILITY_REPORT",
    "SYNCHRONIZATION_REPORT",
    "CORE_HEALTH_REPORT",
    "RESEARCH_STATE_REPORT",
    "PLATFORM_FOUNDATION_REPORT",
]

DASHBOARD_PAGES = [
    "Research Core", "Global Context", "Memory", "Capabilities",
    "Planning", "Synchronization", "Subsystem Health", "Recommendations",
    "Knowledge State", "System Health",
]
