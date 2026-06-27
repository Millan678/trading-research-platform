"""Platform Finalization - Phase 63 Autonomous Research Ecosystem Integration."""
from .safety import FORBIDDEN, enforce, is_forbidden, all_forbidden, audit, PlatformFinalizationBlocked
from .backup import BackupManager
from .contracts import (
    ValidationStatus, OptimizationType, CertificationLevel,
    ARCHITECTURE_DOMAINS, REQUIRED_REPORTS, DASHBOARD_PAGES,
    DOCUMENTATION_TYPES, CERTIFICATION_METRICS,
)
from .storage import Storage
from .platform_registry import PlatformRegistry
from .architecture_validator import ArchitectureValidator
from .dependency_validator import DependencyValidator
from .compatibility_validator import CompatibilityValidator
from .interface_validator import InterfaceValidator
from .optimization_engine import OptimizationEngine
from .performance_optimizer import PerformanceOptimizer
from .storage_optimizer import StorageOptimizer
from .memory_optimizer import MemoryOptimizer
from .consistency_checker import ConsistencyChecker
from .integrity_checker import IntegrityChecker
from .redundancy_detector import RedundancyDetector
from .api_registry import APIRegistry
from .capability_registry import CapabilityRegistry
from .documentation_generator import DocumentationGenerator
from .architecture_export import ArchitectureExport
from .dependency_mapper import DependencyMapper
from .benchmark_validator import BenchmarkValidator
from .certification_engine import CertificationEngine
from .release_validator import ReleaseValidator
from .health_monitor import HealthMonitor
from .readiness_engine import ReadinessEngine
from .dashboard_bridge import DashboardBridge
from .reports import Reports


def __getattr__(name):
    """Lazy import for bridge modules (62 phases)."""
    import re, importlib
    m = re.match(r"^Phase(\d+)Bridge$", name)
    if m:
        phase = int(m.group(1))
        if 1 <= phase <= 62:
            mod_name = f"platform_finalization.p{phase:02d}_bridge"
            mod = importlib.import_module(mod_name)
            cls = getattr(mod, f"Phase{phase:02d}Bridge")
            globals()[name] = cls
            return cls
    from .main import PlatformFinalizationPlatform
    if name == "PlatformFinalizationPlatform":
        globals()[name] = PlatformFinalizationPlatform
        return PlatformFinalizationPlatform
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
