# Contributing to the Trading Research Platform

Thank you for your interest in contributing! This document outlines the process and standards for contributing to this research-only platform.

---

## Research-Only Commitment

**All contributions must preserve the research-only nature of the platform.** No contribution that introduces or enables live trading, broker execution, order placement, automatic deployment, production modification, or governance bypass will be accepted.

---

## Branch Naming

| Type | Format | Example |
|------|--------|---------|
| Feature | `feature/<phase>-<description>` | `feature/p65-bayesian-validation` |
| Bugfix | `fix/<description>` | `fix/determinism-hash-timestamp` |
| Documentation | `docs/<description>` | `docs/phase-index-update` |
| Research | `research/<description>` | `research/causal-inference-benchmark` |
| Safety | `safety/<description>` | `safety/add-forbidden-operation` |

---

## Commit Format

Use [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types:** `feat`, `fix`, `docs`, `test`, `refactor`, `perf`, `chore`, `safety`

**Examples:**
```
feat(p65): add Bayesian validation engine
fix(determinism): exclude timestamps from integrity hashes
docs(phase-index): update phase coverage table
safety(core): add order_placement to forbidden operations
```

---

## Coding Standards

- **Python 3.10+** — use type hints, dataclasses, and modern syntax
- **No external dependencies** for core modules (stdlib-only)
- **Structural safety** — forbidden operations must raise `RuntimeError`, never warn
- **Deterministic** — same seed + input = same output, always
- **Append-only storage** — never modify historical records
- **SHA-256 integrity** — all critical outputs must be hash-verified
- **Read-only bridges** — bridge modules adapt previous phases without modifying them
- **Advisory-only** — all recommendations are advisory, never prescriptive

### Linting

Before submitting, ensure code passes:
- `ruff check .`
- `black --check .`
- `isort --check-only .`

---

## Testing Requirements

Every contribution must:

1. **Not break existing tests** — run `python scripts/verify.py`
2. **Add new tests** for new functionality
3. **Verify determinism** — same seed produces same results
4. **Verify safety** — new forbidden operations raise `RuntimeError`
5. **Verify storage** — SQLite + JSON mirror + PG graceful fallback

---

## Pull Request Process

1. **Fork** the repository
2. **Create** a feature branch from `main`
3. **Implement** your changes with tests
4. **Run** `python scripts/verify.py` locally
5. **Submit** PR with description linking to relevant issue
6. **CI must pass** — all GitHub Actions workflows green
7. **Review** — at least one approval required
8. **Squash merge** to `main`

### PR Checklist

- [ ] No live trading functionality introduced
- [ ] No broker execution capability added
- [ ] All forbidden operations raise `RuntimeError`
- [ ] Deterministic execution verified
- [ ] Existing tests still pass
- [ ] New tests added for new functionality
- [ ] Documentation updated
- [ ] Advisory-only outputs preserved

---

## Reporting Issues

- **Bug reports:** Use the Bug Report template
- **Feature requests:** Use the Feature Request template
- **Security vulnerabilities:** See [SECURITY.md](SECURITY.md)

---

## Code of Conduct

See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md). Be respectful, constructive, and research-focused.
