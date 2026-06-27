"""Research Core - Phase 62 Unified Autonomous Scientific Research Foundation."""
from .safety import FORBIDDEN, enforce, is_forbidden, all_forbidden, audit, ResearchCoreBlocked
from .backup import BackupManager
from .contracts import (
    CouncilStatus, MemoryType, GoalStatus, CapabilityStatus, SyncStatus,
    CONTEXT_DOMAINS, CONSTITUTION_ARTICLES, GLOBAL_CONTEXT_CATEGORIES,
    REQUIRED_REPORTS, DASHBOARD_PAGES,
)
from .storage import Storage
from .core_registry import CoreRegistry
from .global_context import GlobalContext
from .context_manager import ContextManager
from .memory_manager import MemoryManager
from .episodic_memory import EpisodicMemory
from .semantic_memory import SemanticMemory
from .procedural_memory import ProceduralMemory
from .planner import Planner
from .goal_manager import GoalManager
from .objective_manager import ObjectiveManager
from .reasoning_router import ReasoningRouter
from .capability_router import CapabilityRouter
from .workflow_manager import WorkflowManager
from .lifecycle_manager import LifecycleManager
from .state_manager import StateManager
from .synchronization_engine import SynchronizationEngine, SYNC_CHECKS
from .execution_coordinator import ExecutionCoordinator
from .resource_coordinator import ResourceCoordinator
from .capability_catalog import CapabilityCatalog
from .subsystem_registry import SubsystemRegistry
from .health_monitor import HealthMonitor
from .integrity_monitor import IntegrityMonitor
from .recommendation_engine import RecommendationEngine
from .dashboard_bridge import DashboardBridge
from .reports import Reports


def __getattr__(name):
    """Lazy import for bridge modules (61 phases)."""
    import re
    m = re.match(r"^Phase(\d+)Bridge$", name)
    if m:
        phase = int(m.group(1))
        if 1 <= phase <= 61:
            mod_name = f"research_core.p{phase:02d}_bridge"
            import importlib
            mod = importlib.import_module(mod_name)
            cls = getattr(mod, f"Phase{phase:02d}Bridge")
            globals()[name] = cls
            return cls
    from .main import ResearchCorePlatform
    if name == "ResearchCorePlatform":
        globals()[name] = ResearchCorePlatform
        return ResearchCorePlatform
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
