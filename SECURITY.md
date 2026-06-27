# Security Policy

## Research-Only Limitations

**This platform is permanently research-only.** It does not and will never support:

- Live trading
- Broker execution
- Order placement
- Automatic deployment
- Production modification
- Governance bypass
- Evaluation bypass
- Real financial transactions of any kind

All outputs are advisory-only. No component of this platform should ever be used as the basis for real financial decisions.

---

## Reporting Security Vulnerabilities

### Responsible Disclosure

We take security seriously. If you discover a vulnerability, please report it responsibly:

1. **Do not** open a public GitHub issue for security vulnerabilities
2. **Do** email the maintainers directly or use GitHub's private security advisory feature
3. **Include** a clear description of the vulnerability, steps to reproduce, and potential impact
4. **Allow** reasonable time for a response and fix before any public disclosure

### What Counts as a Security Issue

- **Safety bypass:** Any mechanism that circumvents the forbidden-operations enforcement (e.g., enabling live trading, broker execution, or governance bypass)
- **Data integrity:** Modifications to append-only historical records or SHA-256 integrity verification systems
- **Determinism violation:** Non-deterministic behavior that could produce different results for the same inputs
- **Authentication:** Unauthorized access to research data or stored results
- **Injection:** Code injection or arbitrary code execution via research inputs

### What Does NOT Count as a Security Issue

- Feature requests for new research capabilities
- Performance issues in stress testing
- Documentation typos or unclear prose
- Breakage due to missing optional dependencies (PostgreSQL, etc.)

---

## Safety Architecture

The platform enforces safety structurally, not via configuration:

```python
FORBIDDEN = {
    "live_trading",           # RuntimeError on call
    "broker_execution",       # RuntimeError on call
    "order_placement",        # RuntimeError on call
    "automatic_deployment",   # RuntimeError on call
    "production_modification",# RuntimeError on call
    "automatic_strategy_approval", # RuntimeError on call
    "governance_bypass",      # RuntimeError on call
    "evaluation_bypass",      # RuntimeError on call
}
```

**Warning-based enforcement is NOT used. RuntimeError is structural and immediate.**

---

## Supported Versions

| Version | Phase Coverage | Status |
|---------|---------------|--------|
| 1.0.x | Phases 1–64 | Active |
| <1.0 | Phases 1–63 | Superseded |

---

## Security Update Process

1. Vulnerability reported via responsible disclosure
2. Maintainers acknowledge within 48 hours
3. Fix developed and tested within 7 days
4. Security advisory published via GitHub Security tab
5. Patch release issued
6. CVE requested if applicable

---

## No Live Trading Support

To be absolutely clear: **this platform will never support live trading.** Even if a vulnerability were found that somehow bypassed safety enforcement, the platform has no broker connections, no order routing, and no means to execute trades. The safety architecture is defense-in-depth — multiple independent layers must all fail simultaneously for any real-world impact.
