# Architecture

## System Architecture

The Trading Research Platform follows a layered, read-only-bridge architecture where each phase builds upon previous phases through strictly read-only adapters.

---

## Layer Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Layer 6: Validation                    │
│  Phase 64 — End-to-end verification, certification,       │
│  acceptance. Bridges P1–P63 (read-only).                  │
│  Determinism · Reproducibility · Safety · Compliance     │
├─────────────────────────────────────────────────────────┤
│                   Layer 5: Finalization                   │
│  Phase 63 — Unified platform, optimization, certification │
│  Bridges P1–P62 (read-only).                              │
├─────────────────────────────────────────────────────────┤
│                   Layer 4: Unification                    │
│  Phase 62 — Core research ecosystem                       │
│  Bridges P1–P61 (read-only).                              │
├─────────────────────────────────────────────────────────┤
│                  Layer 3: Scientific                      │
│  Phases 20–39 — Causal inference, bias detection,        │
│  scientific discovery, consensus, impact, institution     │
├─────────────────────────────────────────────────────────┤
│                  Layer 2: Intelligence                    │
│  Phases 10–19 — Backtesting, risk, performance,          │
│  alpha discovery, knowledge, simulation, research OS      │
├─────────────────────────────────────────────────────────┤
│                  Layer 1: Foundation                      │
│  Phases 1–9 — Engine, signals, data, broker, AI,          │
│  governance, observability, learning                      │
└─────────────────────────────────────────────────────────┘
```

---

## Safety Architecture

All 8 forbidden operations are enforced at the **structural level**:

```
enforce(operation) → RuntimeError (immediate, no bypass)
```

- No configuration-based enforcement
- No warning-only mode
- No governance override
- RuntimeError is raised at the call site
- Cannot be caught and suppressed (by design)

---

## Storage Architecture

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  PostgreSQL   │    │   SQLite     │    │  JSON Mirror │
│  (optional)  │───▶│  (primary)   │───▶│  (shadow)    │
│  graceful     │    │  append-only │    │  per-record  │
│  fallback     │    │  sha256      │    │  sha256      │
└──────────────┘    └──────────────┘    └──────────────┘
```

- **PostgreSQL**: Optional — if unavailable, gracefully falls back to SQLite
- **SQLite**: Primary storage — append-only, SHA-256 per record
- **JSON Mirror**: Shadow copy — one file per record, for offline audit

---

## Bridge Architecture

```
Phase N (consumer)
     │
     ▼
p{nn}_bridge.py ─── read-only adapter ───▶ Phase NN (source)
```

- Bridges are **strictly read-only**
- No source modification via bridges
- Each bridge exposes: `info()`, `status()`, `data()` methods
- Bridge count: 63 in Phase 64 (covers P1–P63)

---

## Determinism Architecture

- All computations use seeded RNG (`random.Random(seed)`)
- Integrity hashes exclude timestamps
- Same seed + input → same output (verified)
- Two-run hash comparison validates determinism

---

## Backup Architecture

- Timestamped directories (never overwrite)
- SHA-256 manifest of all files
- Excludes: `backups/`, `.git/`, `venv/`, `node_modules/`, `__pycache__/`
- Never recursively backs up `backups/`
