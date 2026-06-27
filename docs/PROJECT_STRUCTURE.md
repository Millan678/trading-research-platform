# Project Structure

The Trading Research Platform is organized as a monorepo with 47 independent project directories, each spanning one or more development phases.

---

## Directory Layout

```
trading-research-platform/
│
├── .github/                           # GitHub configuration
│   ├── workflows/                      # CI/CD pipelines
│   │   ├── verify.yml                 # Import + CLI verification
│   │   ├── lint.yml                   # Ruff + Black + isort
│   │   ├── backup.yml                 # Weekly SHA-256 backup
│   │   └── repository-health.yml      # Repo health checks
│   ├── ISSUE_TEMPLATE/                # Issue templates
│   └── PULL_REQUEST_TEMPLATE.md       # PR template
│
├── docs/                              # This documentation directory
│   ├── PROJECT_STRUCTURE.md          # This file
│   ├── ARCHITECTURE.md               # System architecture
│   ├── PHASE_INDEX.md                # Phase-by-phase index
│   ├── MODULE_INDEX.md               # Module-level index
│   ├── CLI_REFERENCE.md              # CLI command reference
│   ├── DASHBOARD_REFERENCE.md        # Dashboard page reference
│   ├── REPORT_REFERENCE.md           # Report format reference
│   └── BRIDGE_REFERENCE.md           # Bridge module reference
│
├── scripts/                           # Utility scripts
│   ├── backup.py                     # Backup with SHA-256 manifest
│   ├── verify.py                     # Full platform verification
│   └── stats.py                      # Repository statistics
│
├── backups/                           # SHA-256 verified backups
│
├── .gitignore                         # Comprehensive ignore rules
├── .gitattributes                     # Line ending normalization
├── LICENSE                            # MIT License
├── README.md                          # Project overview
├── CONTRIBUTING.md                    # Contribution guide
├── CHANGELOG.md                       # Semantic version history
├── CODE_OF_CONDUCT.md                # Community standards
├── SECURITY.md                        # Security policy
│
├── trading-ai-copilot/                # Phases 1–3
├── trading-broker-layer/             # Phase 4
├── trading-ai-runtime/               # Phases 5–6
├── trading-governance/               # Phase 7
├── trading-observability/            # Phase 8
├── trading-learning-platform/        # Phase 9
├── trading-benchmark-platform/       # Phases 10–12
├── trading-evaluation-framework/     # Phases 13–14
├── trading-alpha-discovery/          # Phase 15
├── trading-knowledge/                # Phase 16–17
├── trading-research-corpus/          # Phase 18
├── trading-research-simulator/       # Phase 19
├── trading-scientific-consensus/     # Phases 19–20
├── trading-temporal-intelligence/    # Phase 20
├── trading-digital-twin/             # Phase 21
├── trading-self-improvement/         # Phase 22
├── trading-paper-engine/             # Phase 23
├── trading-reality-calibration/      # Phase 24
├── trading-collaboration/            # Phase 25
├── trading-scientific-council/       # Phase 26
├── trading-scientific-impact/        # Phase 27
├── trading-distributed-research/     # Phase 28
├── trading-research-program-manager/ # Phase 29
├── trading-causal-intelligence/      # Phase 30
├── trading-scientific-discovery/     # Phase 31
├── trading-scientific-institution/   # Phase 32
├── trading-benchmark-platform/       # Phase 33
├── trading-meta-research/            # Phase 34
├── trading-digital-scientist/        # Phase 35
├── trading-research-coordinator/    # Phase 36
├── trading-research-observatory/     # Phase 37
├── trading-platform-intelligence/   # Phases 38–39
├── trading-platform-packaging/       # Phase 40
├── trading-platform-web/            # Phase 41
├── trading-platform-docs/           # Phase 42
├── trading-platform-ops/            # Phase 43
├── trading-autonomous-research/      # Phase 44
├── trading-knowledge-graph/         # Phase 45
├── trading-live-monitor/            # Phase 47
├── trading-research-foresight/      # Phase 48
├── trading-research-core/           # Phase 62 (bridges P1–P61)
├── trading-platform-finalization/   # Phase 63 (bridges P1–P62)
└── trading-platform-verification/   # Phase 64 (bridges P1–P63)
```

---

## Naming Convention

- Project directories: `trading-<domain>/`
- Package directories: `<domain>/` (inside project)
- Bridge modules: `p{NN}_bridge.py`
- Reports: `PHASE{NN}_<DOMAIN>_<TYPE>_REPORT.{json,md}`
- Dashboard pages: `<page_name>.json`
