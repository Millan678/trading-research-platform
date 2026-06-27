# CLI Reference

Command-line interfaces for the three unification phases (62–64).

---

## Phase 62 — Research Core

```bash
python -m research_core.cli <command>
```

| Command | Description |
|---------|-------------|
| `status` | Platform status overview |
| `validate` | Run cross-phase validation |
| `bridge` | Bridge health check |
| `health` | System health report |
| `report` | Generate research reports |

---

## Phase 63 — Platform Finalization

```bash
python -m platform_finalization.cli <command>
```

| Command | Description |
|---------|-------------|
| `status` | Platform status |
| `architecture` | Architecture completeness |
| `dependencies` | Dependency validation |
| `optimization` | Optimization report |
| `documentation` | Documentation coverage |
| `certification` | Certification status |
| `health` | Health check |
| `report` | Generate reports |

---

## Phase 64 — Platform Verification

```bash
python -m platform_verification.cli <command>
```

| Command | Description |
|---------|-------------|
| `status` | Verification status |
| `verify` | Full verification suite |
| `integrity` | Integrity validation |
| `determinism` | Determinism verification |
| `reproducibility` | Reproducibility check |
| `stress` | Stress testing |
| `certify` | Certification |
| `health` | Health check |
| `report` | Generate reports |

---

## Common Options

All CLIs support:
- `--seed <int>` — Set random seed (default: 42)
- `--output <dir>` — Output directory
- `--verbose` — Verbose output
- `--json` — JSON-formatted output

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Verification failure |
| 2 | Safety violation |
| 3 | Import error |
