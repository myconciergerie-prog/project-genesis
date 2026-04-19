<!-- SPDX-License-Identifier: MIT -->
---
name: Runtime dogfood evidence log — v1.6.2
description: Per-fixture runtime observations from 5 fresh Claude Code sessions (4 v1.5.0 dryrun fixtures dispatch-only + 1 new alexandre_windows full happy-path). Filled in Phase B after user spawns sessions per runbook `runtime_dogfood_v1_6_2.md`. Stub committed in Phase A with TBD placeholders ; final fill in feat-runtime commit.
---

# Runtime dogfood evidence log — v1.6.2

**Driver session** : v1.6.2 feat branch `feat/v1.6.2-runtime-dogfood`.
**Phase A commit** : created this stub with 5 fixture sections + H1-H5 table with TBD values.
**Phase B commit** : fills the TBD values based on redacted user-pasted evidence.

---

## Per-fixture observations

### Fixture fixture_A (EXIT_NO_KEY test — `C:/tmp/genesis-v1.5.0-dryrun/fixture_A/`)

- **Trigger phrase used :** TBD at runtime
- **Invocation form observed :** TBD
- **Cards rendered :** TBD
- **Artefacts written :** TBD
- **Frictions found :** TBD

### Fixture fixture_B (multi-file happy-start dispatch — `C:/tmp/genesis-v1.5.0-dryrun/fixture_B/`)

- **Trigger phrase used :** TBD at runtime
- **Invocation form observed :** TBD
- **Cards rendered :** TBD
- **Artefacts written :** TBD
- **Frictions found :** TBD

### Fixture fixture_C (re-run / supersession scenario — `C:/tmp/genesis-v1.5.0-dryrun/fixture_C/`)

- **Trigger phrase used :** TBD at runtime
- **Invocation form observed :** TBD
- **Cards rendered :** TBD
- **Artefacts written :** TBD
- **Frictions found :** TBD

### Fixture fixture_D (SDK-absent edge — now generic internal-error per v1.5.1 — `C:/tmp/genesis-v1.5.0-dryrun/fixture_D/`)

- **Trigger phrase used :** TBD at runtime
- **Invocation form observed :** TBD
- **Cards rendered :** TBD
- **Artefacts written :** TBD
- **Frictions found :** TBD

### Fixture alexandre_windows (full happy-path — `C:/tmp/genesis-v1.6.2-alexandre/`)

- **Trigger phrase used :** TBD at runtime
- **Invocation form observed :** TBD
- **Cards rendered :** TBD (expected: welcome → Phase 0.1 → 0.2 → 0.3 → 0.4 arbitration → 0.5 consent)
- **Artefacts written :** TBD (expected: drop_zone_intent.md with arbitrated_fields list from multi-source FR + PL drop)
- **Frictions found :** TBD

---

## H1 — dispatch evidence table

| Fixture | Dispatch | Invocation form (verbatim) |
|---|---|---|
| fixture_A | TBD (confirmed / failed / deferred) | TBD |
| fixture_B | TBD (confirmed / failed / deferred) | TBD |
| fixture_C | TBD (confirmed / failed / deferred) | TBD |
| fixture_D | TBD (confirmed / failed / deferred) | TBD |
| alexandre_windows | TBD (confirmed / failed / deferred) | TBD |

## H2-H5 global hypothesis rows

| H | Hypothesis | Observation |
|---|---|---|
| H2 | Phase 0.4 arbitration on alexandre_windows renders `arbitrated_fields` list non-empty | TBD |
| H3 | Phase 0.5 Path 2a (first-write empty-divergences) renders v1.3.2 consent card on at least 1 fixture | TBD |
| H4 | Fixture A with ANTHROPIC_API_KEY unset renders EXIT_NO_KEY halt card | TBD |
| H5 | AC10 grep pipeline returns 0 (zero Layer B ripple) | TBD (expected 0, filled post Task A6 + B4 runs) |

## Friction triage (§ 4.3 hybrid gate)

| Friction # | Class (A/B/C) | Description | Disposition |
|---|---|---|---|
| _(none yet ; populate per Phase B observations)_ | | | |

## Deferred-friction queue (B + C → v1.6.3+)

| Friction # | Proposed ship | Reason for defer |
|---|---|---|
| _(empty at Phase A stub time)_ | | |
