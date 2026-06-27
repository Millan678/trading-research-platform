"""Main — orchestrate the full Platform Verification pipeline."""
import hashlib, json, os, random, time
from datetime import datetime
from typing import Any, Dict, List, Optional

from .safety import enforce, audit, is_forbidden, PlatformVerificationBlocked
from .backup import BackupManager
from .contracts import VALIDATION_DOMAINS, CERTIFICATION_METRICS, REQUIRED_REPORTS, DASHBOARD_PAGES, CertificationLevel
from .storage import Storage
from .verification_registry import VerificationRegistry
from .validation_engine import ValidationEngine
from .integration_validator import IntegrationValidator
from .dependency_validator import DependencyValidator
from .interface_validator import InterfaceValidator
from .bridge_validator import BridgeValidator
from .determinism_validator import DeterminismValidator
from .reproducibility_validator import ReproducibilityValidator
from .consistency_validator import ConsistencyValidator
from .integrity_validator import IntegrityValidator
from .stress_test_engine import StressTestEngine
from .load_test_engine import LoadTestEngine
from .scalability_validator import ScalabilityValidator
from .fault_injection import FaultInjection
from .failure_recovery_validator import FailureRecoveryValidator
from .configuration_validator import ConfigurationValidator
from .storage_validator import StorageValidator
from .backup_validator import BackupValidator
from .security_validator import SecurityValidator
from .safety_validator import SafetyValidator
from .compliance_validator import ComplianceValidator
from .platform_auditor import PlatformAuditor
from .acceptance_engine import AcceptanceEngine
from .certification_engine import CertificationEngine
from .dashboard_bridge import DashboardBridge
from .reports import Reports


class PlatformVerificationPlatform:
    """End-to-End Autonomous Research Platform Validation, Verification & Scientific Acceptance Suite."""

    def __init__(self, base_dir: str, seed: int = 42):
        self.seed = seed
        self.rng = random.Random(seed)
        self.base_dir = base_dir
        os.makedirs(base_dir, exist_ok=True)

        # Safety check
        enforce("initialization_check")

        # Storage
        self.storage = Storage(base_dir)

        # Backup
        self.backup = BackupManager(base_dir)
        self.backup.create_backup()

        # Registry
        self.registry = VerificationRegistry(self.storage, seed=seed)

        # Core validators
        self.validation_engine = ValidationEngine(self.storage, seed=seed)
        self.integration_validator = IntegrationValidator(self.storage, seed=seed)
        self.dependency_validator = DependencyValidator(self.storage, seed=seed)
        self.interface_validator = InterfaceValidator(self.storage, seed=seed)
        self.bridge_validator = BridgeValidator(self.storage, seed=seed)

        # Determinism / reproducibility
        self.determinism_validator = DeterminismValidator(self.storage, seed=seed)
        self.reproducibility_validator = ReproducibilityValidator(self.storage, seed=seed)
        self.consistency_validator = ConsistencyValidator(self.storage, seed=seed)
        self.integrity_validator = IntegrityValidator(self.storage, seed=seed)

        # Stress / load / scalability
        self.stress_test_engine = StressTestEngine(self.storage, seed=seed)
        self.load_test_engine = LoadTestEngine(self.storage, seed=seed)
        self.scalability_validator = ScalabilityValidator(self.storage, seed=seed)

        # Fault injection / recovery
        self.fault_injection = FaultInjection(self.storage, seed=seed)
        self.failure_recovery_validator = FailureRecoveryValidator(self.storage, seed=seed)

        # Configuration / storage / backup validation
        self.configuration_validator = ConfigurationValidator(self.storage, seed=seed)
        self.storage_validator = StorageValidator(self.storage, seed=seed)
        self.backup_validator = BackupValidator(self.storage, seed=seed)

        # Security / safety / compliance
        self.security_validator = SecurityValidator(self.storage, seed=seed)
        self.safety_validator = SafetyValidator(self.storage, seed=seed)
        self.compliance_validator = ComplianceValidator(self.storage, seed=seed)

        # Audit / acceptance / certification
        self.platform_auditor = PlatformAuditor(self.storage, seed=seed)
        self.acceptance_engine = AcceptanceEngine(self.storage, seed=seed)
        self.certification_engine = CertificationEngine(self.storage, seed=seed)

        # Output
        self.dashboard = DashboardBridge(base_dir)
        self.reports = Reports(base_dir)

    def run(self, seed: int = 42) -> dict:
        """Execute the full verification pipeline."""
        rng = random.Random(seed)

        # Phase 1: Core validation
        validation = self.validation_engine.validate_all(seed=seed)

        # Phase 2: Integration validation
        integration = self.integration_validator.validate_all(seed=seed)

        # Phase 3: Dependency validation
        dependency = self.dependency_validator.validate_all(seed=seed)

        # Phase 4: Interface validation
        interface = self.interface_validator.validate_all(seed=seed)

        # Phase 5: Bridge validation
        bridge = self.bridge_validator.validate_all(phases=63, seed=seed)

        # Phase 6: Determinism
        determinism = self.determinism_validator.validate_all(seed=seed)

        # Phase 7: Reproducibility
        reproducibility = self.reproducibility_validator.validate_all(seed=seed)

        # Phase 8: Consistency
        consistency = self.consistency_validator.check_all(seed=seed)

        # Phase 9: Integrity
        integrity = self.integrity_validator.check_all(seed=seed)

        # Phase 10: Stress testing
        stress = self.stress_test_engine.run_all(seed=seed)

        # Phase 11: Load testing
        load = self.load_test_engine.run_all(seed=seed)

        # Phase 12: Scalability
        scalability = self.scalability_validator.validate_all(seed=seed)

        # Phase 13: Fault injection
        faults = self.fault_injection.inject_all(seed=seed)

        # Phase 14: Failure recovery
        recovery = self.failure_recovery_validator.validate_all(seed=seed)

        # Phase 15: Configuration
        config = self.configuration_validator.validate_all(seed=seed)

        # Phase 16: Storage validation
        storage_val = self.storage_validator.validate_all(seed=seed)

        # Phase 17: Backup validation
        backup_val = self.backup_validator.validate_all(seed=seed)

        # Phase 18: Security
        security = self.security_validator.validate_all(seed=seed)

        # Phase 19: Safety
        safety = self.safety_validator.validate_all(seed=seed)

        # Phase 20: Compliance
        compliance = self.compliance_validator.validate_all(seed=seed)

        # Phase 21: Platform audit
        audit_result = self.platform_auditor.audit_all(seed=seed)

        # Phase 22: Certification
        certification = self.certification_engine.compute_all(seed=seed)

        # Phase 23: Acceptance
        acceptance = self.acceptance_engine.compute_acceptance(seed=seed)

        # Compute deterministic overall hash (exclude all timestamps)
        all_scores = {
            "validation": validation.get("average_score", 0),
            "integration": integration.get("average_score", 0),
            "dependency": dependency.get("average_score", 0),
            "interface": interface.get("average_score", 0),
            "bridge": bridge.get("bridge_health_score", 0),
            "determinism": determinism.get("determinism_score", 0),
            "reproducibility": reproducibility.get("reproducibility_score", 0),
            "consistency": consistency.get("average_score", 0),
            "integrity": integrity.get("average_score", 0),
            "stress": stress.get("average_score", 0),
            "load": load.get("average_throughput", 0),
            "scalability": scalability.get("average_score", 0),
            "faults": faults.get("recovery_count", 0) / max(faults.get("faults_injected", 1), 1),
            "recovery": recovery.get("average_recovery_score", 0),
            "config": config.get("average_score", 0),
            "storage_val": storage_val.get("average_score", 0),
            "backup_val": backup_val.get("average_score", 0),
            "security": security.get("average_score", 0),
            "safety": 1.0 if safety.get("all_blocked") else 0.0,
            "compliance": compliance.get("average_score", 0),
            "audit": audit_result.get("average_score", 0),
            "certification": certification.get("platform_quality_score", 0),
            "acceptance": acceptance.get("overall_acceptance_score", 0),
        }
        overall_hash = hashlib.sha256(json.dumps(all_scores, sort_keys=True).encode()).hexdigest()[:16]

        # Assemble results
        results = {
            "platform_verification_results": True,
            "seed": seed,
            "phases_validated": 63,
            "modules_validated": 94,
            "bridges_validated": 63,
            "validation": validation,
            "integration": integration,
            "dependency": dependency,
            "interface": interface,
            "bridge": bridge,
            "determinism": determinism,
            "reproducibility": reproducibility,
            "consistency": consistency,
            "integrity": integrity,
            "stress": stress,
            "load": load,
            "scalability": scalability,
            "faults": faults,
            "recovery": recovery,
            "config": config,
            "storage_validation": storage_val,
            "backup_validation": backup_val,
            "security": security,
            "safety": safety,
            "compliance": compliance,
            "audit": audit_result,
            "certification": certification,
            "acceptance": acceptance,
            "overall_hash": overall_hash,
            "advisory_only": True,
        }

        # Dashboard
        dashboard_data = {k.replace("_", " "): v for k, v in all_scores.items()}
        dashboard_data["platform_verification"] = all_scores
        self.dashboard.export(dashboard_data)

        # Reports
        report_content = {
            "phases_validated": 63,
            "modules_validated": 94,
            "overall_scores": all_scores,
            "certification_level": certification.get("certification_level"),
            "advisory_only": True,
        }
        self.reports.generate_all(report_content)

        # Final backup
        self.backup.create_backup()

        return results

    def summary(self, seed: int = 42) -> dict:
        results = self.run(seed=seed)
        cert = results.get("certification", {})
        accept = results.get("acceptance", {})
        return {
            "phase": 64,
            "phases_validated": results["phases_validated"],
            "modules_validated": results["modules_validated"],
            "bridges_validated": results["bridges_validated"],
            "determinism_score": results["determinism"].get("determinism_score", 0),
            "reproducibility_score": results["reproducibility"].get("reproducibility_score", 0),
            "certification_level": cert.get("certification_level", "UNKNOWN"),
            "acceptance_score": accept.get("overall_acceptance_score", 0),
            "overall_hash": results["overall_hash"],
            "advisory_only": True,
        }
