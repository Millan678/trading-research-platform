# Pull Request

## Description

Brief description of changes.

## Research-Only Checklist

- [ ] Does NOT introduce live trading functionality
- [ ] Does NOT introduce broker execution capability
- [ ] Does NOT enable order placement
- [ ] Does NOT enable automatic deployment
- [ ] Does NOT modify production systems
- [ ] Does NOT introduce governance bypass
- [ ] Does NOT introduce evaluation bypass
- [ ] All outputs remain advisory-only

## Safety Checklist

- [ ] All forbidden operations raise `RuntimeError`
- [ ] Deterministic execution verified (same seed → same output)
- [ ] No warning-only enforcement introduced
- [ ] Append-only storage preserved
- [ ] SHA-256 integrity maintained

## Testing Checklist

- [ ] Existing tests still pass (`python scripts/verify.py`)
- [ ] New tests added for new functionality
- [ ] All CLI commands exit successfully
- [ ] Import verification passes

## Documentation Checklist

- [ ] README updated (if applicable)
- [ ] CHANGELOG updated
- [ ] Docs updated (if applicable)
- [ ] Module index updated (if new modules)

## Phase Scope

Which phases are affected?

## Type of Change

- [ ] Bug fix
- [ ] New feature
- [ ] Safety enhancement
- [ ] Documentation update
- [ ] Refactoring
- [ ] Performance improvement

## Additional Notes

Any other relevant information for reviewers.
