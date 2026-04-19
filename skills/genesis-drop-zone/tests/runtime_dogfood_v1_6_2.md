<!-- SPDX-License-Identifier: MIT -->
---
name: Runtime dogfood runbook — v1.6.2
description: Reusable runbook for spawning fresh Claude Code sessions per fixture, triggering `/genesis-drop-zone`, observing dispatch + card render + artefact write, and pasting redacted evidence back to the driver session. Shipped first for v1.6.2 and reusable for any future v1.x.y runtime-dogfood cycle by copying to `runtime_dogfood_v<new-version>.md` with fixture list updated.
---

# Runtime dogfood runbook — v1.6.2

## Pre-flight

Before spawning ANY fresh Claude Code session :

1. **Claude Code version check + plugin pointing — REVISED v1.6.2 post-runtime-evidence discovery (F1)** — `--plugin-dir <path>` alone is NOT sufficient to isolate the worktree plugin when a same-named plugin is user-scope installed. Runtime evidence at v1.6.2 (see `runtime_dogfood_evidence_v1_6_2.md` § Control runs) showed the stale v1.1.0 cached install's skill list surfaced despite both `--plugin-dir` and `claude plugin disable`. Three valid isolation paths :

   **Path A — full uninstall** (most reliable ; mildly destructive to user state) :
   ```
   claude plugin uninstall project-genesis@project-genesis-marketplace
   claude --plugin-dir C:/Dev/Claude_cowork/project-genesis/.claude/worktrees/feat_2026-04-19_v1_5_2_runtime_dogfood/
   # (post-runbook) reinstall user-scope if desired:
   # claude plugin install project-genesis@project-genesis-marketplace
   ```

   **Path B — `--bare` + ANTHROPIC_API_KEY** (non-destructive ; requires API key env) :
   ```
   export ANTHROPIC_API_KEY='sk-ant-...'
   claude --bare --plugin-dir <worktree> --add-dir <worktree> ...
   ```
   `--bare` skips plugin sync so the user-scope cache is not auto-loaded ; `--plugin-dir` provides the canonical source. Note : `--bare` requires explicit `ANTHROPIC_API_KEY` (OAuth disabled) and requires `--add-dir` to re-enable CLAUDE.md auto-discovery if you want Layer 0 context.

   **Path C — publish then update** (best for post-ship validation, not pre-ship) :
   ```
   # after v1.X.Y tagged + pushed :
   claude plugin update project-genesis@project-genesis-marketplace
   # then natural `claude` spawn exercises the new version
   ```

   After spawn by any path, verify `/genesis-drop-zone` AND `/promptor` both surface before proceeding with trigger-phrase runs. The cheapest check : ask Claude `"liste les skills genesis-* + promptor dans ton harness"` and confirm both skills appear.
2. **API key presence** — for the 4 happy-path fixtures (`scenario_first_write` / `scenario_retirement` / `scenario_halt_no_sdk` + `alexandre_windows`), `ANTHROPIC_API_KEY` MUST be exported in the shell env where `claude` is invoked. For `scenario_halt_no_key` (EXIT_NO_KEY test), explicitly `unset ANTHROPIC_API_KEY` before `claude` spawn.
3. **Git status clean in fixture cwd** — `cd <fixture>` → `ls -la` shows ONLY the intended fixture artefacts, no stale `drop_zone_intent.md` or archive. If present, check whether this is a planned re-run (v1.5.0 dryrun fixtures may contain prior paper-trace artefacts — keep them) or accidental pollution (delete before spawn).
4. **Driver session state** — this runbook is consumed by the driver session (the one doing v1.6.2 ship). The driver session MUST be in Phase A complete state (feat-core commit landed, evidence log stub at `skills/genesis-drop-zone/tests/runtime_dogfood_evidence_v1_6_2.md` with 5 TBD fixture sections) before fresh sessions spawn.

## Per-fixture spawn + trigger + observe

For each of the 5 fixtures, execute the following 5 steps in a dedicated PowerShell / git-bash shell :

### Step 1 — cd to fixture cwd

```
cd C:/tmp/genesis-v1.5.0-dryrun/scenario_halt_no_key/       # or scenario_first_write / scenario_retirement / scenario_halt_no_sdk
# OR
cd C:/tmp/genesis-v1.6.2-alexandre/
```

Verify `pwd` matches expectation.

### Step 2 — ensure API key env matches fixture class

**`scenario_halt_no_key` (EXIT_NO_KEY test)** — MUST be unset :
```
unset ANTHROPIC_API_KEY
echo "key present? ${ANTHROPIC_API_KEY:+yes}${ANTHROPIC_API_KEY:-NO}"
```
Expected : `key present? NO`.

**All other fixtures** — MUST be present :
```
echo "key present? ${ANTHROPIC_API_KEY:+yes}"
```
Expected : `key present? yes`.

### Step 3 — spawn fresh Claude Code session with `--plugin-dir` pointing at worktree

```
claude --plugin-dir C:/Dev/Claude_cowork/project-genesis/.claude/worktrees/feat_2026-04-19_v1_5_2_runtime_dogfood
```

Do NOT spawn bare `claude` — that would load the stale user-scope v1.1.0 plugin cache, invalidating the runtime evidence. `--plugin-dir` flag is session-local and repeatable.

### Step 4 — type a natural trigger phrase

The trigger phrase should be organically chosen — no cheat-sheet. Examples to vary across fixtures :

- "aide-moi à bootstrap ce projet depuis ce dossier"
- "j'ai préparé quelques artefacts ici, lance le drop-zone"
- "démarre genesis-drop-zone sur mon drop ici"
- "regarde ce dossier et lance le protocole de bootstrap"
- "I've got some files here for Genesis to start a new project, can you begin the drop-zone flow"

Record the verbatim phrase used (for the evidence log H1 row).

### Step 5 — observe + capture

Observe until the first Phase 0 card renders (welcome) OR an error / halt occurs. Capture (screenshot or copy-paste transcript) :

- The verbatim Skill invocation message (if visible) — this answers AC6 H1 "invocation form observed" (bare `genesis-drop-zone` / namespaced `project-genesis:genesis-drop-zone` / something else).
- The welcome card (verbatim or summarized — ≤ 40 lines).
- For the full-happy-path fixture (alexandre_windows only) : proceed through Phase 0.1 → 0.2 → 0.3 → 0.4 arbitration card → Phase 0.5 consent → `drop_zone_intent.md` write. Record arbitration `arbitrated_fields` list for H2, Phase 0.5 Path observed for H3.
- For `scenario_halt_no_key` (EXIT_NO_KEY) : record the halt card rendered and its error message (redacted per § Redaction rules).
- After session closes : `ls -la <fixture>` to see artefacts written (AC evidence).

## Redaction rules

The evidence log is committed to git. Before pasting ANY transcript excerpt, strip :

- **ANTHROPIC_API_KEY values** — regex `sk-ant-[a-zA-Z0-9-_]+` → `sk-ant-REDACTED`
- **Other API tokens / bearer tokens** — regex `(?i)(api[_-]?key|token|bearer)[=: ]+['"\s]*[a-zA-Z0-9-_\.]{20,}` → redacted
- **Absolute user paths outside fixture** — regex `C:/Users/[^/]+/` → `C:/Users/REDACTED/`
- **Email addresses** — regex `[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}` → `<email-redacted>`
- **Anthropic Console deep-link tokens** — regex `/sessions/[a-zA-Z0-9-_]+` → `/sessions/REDACTED`
- **Anthropic request-id in stderr** — regex `req_[a-zA-Z0-9]+` → `req_REDACTED`
- **Stderr token-count lines with request-specific opaque identifiers** — scrub the identifier, keep the token count if useful.

If in doubt, redact rather than ship. These rules mirror spec § 4.2 #6 verbatim.

## Re-run guidance

If a class-A friction is surfaced and fixed in Phase B (per spec § 4.3 hybrid gate), the runbook is re-runnable :

1. **Re-run only the fixture(s) affected by the fix.** Not all 5 — the scope is the subset that exercised the buggy code path.
2. **Append new evidence** to the evidence log with a `### Fixture <name> — run 2 (post-fix-class-a #N)` section. Do NOT overwrite run 1.
3. **Keep redaction rules unchanged** — they apply to every run.
4. **After re-run confirms fix** : update H1-H5 rows to reflect the latest observation ; add a note explaining "run 2 supersedes run 1 for fixture <name>" in the evidence log.

## Source of truth

This runbook is canonical ; if it contradicts the spec `.claude/docs/superpowers/specs/v1_6_2_runtime_dogfood.md`, the spec wins and the runbook is wrong — file a class-A fix to realign.
