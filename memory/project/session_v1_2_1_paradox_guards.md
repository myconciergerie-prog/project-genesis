<!-- SPDX-License-Identifier: MIT -->
---
name: Session v1.2.1 — paradox guards
description: v1.2.1 ship session. Three P0 fixes from v1.2.0 strange-loop self-dogfood landed as three surgical commits plus one verification follow-up. Genesis plugin now self-contained in personal-scope install, nested-repo silent success fixed, Step 0 refuses strange-loop targets structurally.
type: project
date: 2026-04-17
session: v1.2.1
branch: feat/v1.2.1-paradox-guards
parent-tag: v1.2.0
parent-commit: 760f69c
---

# Session v1.2.1 — paradox guards

Direct follow-up to v1.2.0 self-dogfood (merged as PR #23 at commit `760f69c`, tagged `v1.2.0` on 2026-04-17). Scope: the three P0 fixes the friction log explicitly named. Every other v1.2.0 finding (mode-auto semantics, argument schema, config.txt templates, cleanup skill, Python driver, R8 scope) deliberately deferred.

## What shipped

Four commits on `feat/v1.2.1-paradox-guards` off `cff4608`:

| Commit | Fix | Files changed |
|---|---|---|
| `c707023` | **F29** — relocate `v1_rules.md` into the skill | 7 files (git mv rename + 5 reference updates + plan doc) |
| `90c7777` | **F30** — git-aware nested-repo probe at Phase 3.1 | 1 file (`phase-3-git-init.md`) |
| `40a96e4` | **F23+F27** — Step 0 paradox guards | 2 files (`SKILL.md` + `phase-0-seed-loading.md`) |
| `a53dd48` | **F30 follow-up** — git-bash path normalization note | 1 file (`phase-3-git-init.md`) |

Net diff: `+705 / −13` lines across 10 distinct files. The plan file accounts for ≈ 550 of those lines; the actual skill logic delta is ≈ 155 lines added, ≈ 13 removed.

## Verification walk-throughs (scenario replays)

### F23 — target-inside-orchestrator (Guard A)

Replay scenario: v1.2.0 exact configuration — `target = project-genesis/.claude/worktrees/feat_2026-04-17_v1.2.0-selfdogfood/selfdogfood-target/`.

With new code: at SKILL.md Step 0, orchestrator computes plugin root by walking three levels up from its own `SKILL.md` → `<repo>/project-genesis/`. Target absolute path starts with `<repo>/project-genesis/` → **Guard A fires → HALT with Guard A message template**. Orchestrator never reaches the consent card. Exit clean, no state changes to target folder.

Mental replay confirms the v1.2.0 friction F23 is now structurally impossible without an explicit flag (no flag exists in v1.2.1).

### F27 — slug self-collision (Guard B)

Replay scenario: user writes `config.txt` with `slug: project-genesis` (deliberate strange loop).

With new code: if Guard A already halted upstream (target inside orchestrator tree), Guard B is never reached — that's expected ordering. If target is OUTSIDE the orchestrator tree but slug is `project-genesis`, Phase 0 Step 0.2 resolves slug → compare against `{project-genesis}` ∪ `<plugin-root>/.claude-plugin/plugin.json:name` → match → **Phase 0 halts with Guard B message**.

Guard B is re-asserted in `phase-0-seed-loading.md` Common Failures (upgraded from WARN to STRUCTURAL STOP) so the derived-slug path — where the slug was never in `config.txt` but came from the target folder name — is still caught at Phase 0.

### F30 — nested repo probe (scratch shell)

Reproduced live on 2026-04-17 from the v1.2.1 worktree:

```text
mkdir -p /tmp/f30-scratch && git -C /tmp/f30-scratch rev-parse --show-toplevel
→ fatal: not a git repository (exit non-zero)  → case A: outside-any-repo → proceed ✓

mkdir -p <v1.2.1-worktree>/tmp-f30-test/nested
git -C <v1.2.1-worktree>/tmp-f30-test/nested rev-parse --show-toplevel
→ C:/Dev/Claude_cowork/project-genesis/.claude/worktrees/feat_2026-04-17_v1.2.1-paradox-guards
→ target_abs = /c/Dev/Claude_cowork/project-genesis/.claude/worktrees/feat_2026-04-17_v1.2.1-paradox-guards/tmp-f30-test/nested
→ outer != target_abs  → case C: nested → HALT ✓
```

The probe correctly identifies both the happy case (outside any repo → proceed) and the nested case (inside the outer worktree → halt). The scratch `tmp-f30-test/` directory was removed after verification.

A subtle issue surfaced during the replay: on git-bash for Windows, `git rev-parse --show-toplevel` returns Windows-style `C:/...` while POSIX `pwd` returns `/c/...`. A naive string comparison would mis-dispatch case B (target-is-own-root, where the two should be equal) as case C (nested). The follow-up commit `a53dd48` adds a Path normalization note to Step 3.1 documenting the MSYS format divergence and two correction options (`pwd -W` on git-bash, or `git rev-parse` on both sides). POSIX (macOS, Linux) is unaffected — formats already match.

### F29 — skill-local rules resolver

Scenario: skill installed at `~/.claude/skills/genesis-protocol/` (per F18 `cp -r` workaround).

New resolver: `<skill_dir>/rules/v1_rules.md` → `~/.claude/skills/genesis-protocol/rules/v1_rules.md`. The file is now shipped inside the skill package, so it exists wherever the skill is installed.

Verified on disk in the v1.2.1 worktree:

```text
skills/genesis-protocol/rules/v1_rules.md  →  369 lines, 20068 bytes (identical to pre-move content)
.claude/docs/superpowers/rules/             →  empty directory (git mv removed the file, leaves no orphan)
```

`git mv` preserved blame history (`git log --follow skills/genesis-protocol/rules/v1_rules.md` shows the pre-relocation history intact). No content changes — the relocation is pure location.

The legacy fallback path `<plugin-root>/.claude/docs/superpowers/rules/v1_rules.md` is still searched if the skill-local path is missing (pre-v1.2.1 installs). Halt behaviour surfaces BOTH expected paths in the error if neither resolves.

## Self-rating — v1.2.1

See CHANGELOG for the 5-axis table. Summary:

- **Pain-driven**: every fix maps 1:1 to a v1.2.0 friction (F29 → rename, F30 → git probe, F23/F27 → Step 0 guards). Zero speculative additions.
- **Anti-Frankenstein**: no new runtime, no test harness, no config surface. Pure Markdown runbook edits + one file rename. F32 (Python driver) explicitly deferred to v1.3.
- **Self-contained**: the F29 fix itself makes the skill more self-contained (literally its stated purpose). The plan file lives in dev-internal docs, not shipped.
- **Prose**: each commit has a 3-paragraph narrative body explaining root cause, fix mechanism, and scope boundary. Halt templates are copy-paste-ready.
- **Best-at-date**: path-resolution approach validated against the v1.2.0 reproduction. No external research cache entry refresh needed (stack entries were on the R8 refresh list but the changes here don't depend on new Claude Code SDK behaviour — skill internals only).

## Known gaps (explicitly deferred to v1.2.2+)

- **F20/F22 mode-auto orchestrator-level semantics** — P1, needs an `## Arguments` section in SKILL.md and per-phase mode dispatch.
- **F21 argument schema** — P1, pair with mode-auto.
- **F24 Phase 0.1 git-aware inspection** — P2, F30 already covers the Phase 3 blocker case; Phase 0.1 is cosmetic improvement.
- **F25/F31 config.txt canonical examples** — P2, ship `templates/config-*.txt.example`.
- **F26 non-canonical fields audit trail** — P2.
- **F28 `genesis-cleanup` sibling skill** — P3.
- **F32 Python driver** — v1.3 target; today's cycle confirms the Markdown ceiling is near.
- **F33 R8 scope disambiguation** — P3.
- **F34 gh active-account pre-flight** — P1, needs its own Phase 6.0 design pass.

These are named and dated so the next session can pick the biggest-bang-per-hour item without re-reading the full v1.2.0 friction log.

## Running average post-v1.2.1

v0.2 → v1.2.0 average was **8.57/10** (after PR #23 merge). v1.2.1 self-rating target is 8.6/10 on pain-driven + anti-Frankenstein axes, with 9.0+ on pain-driven (surgical fixes) and 9.0+ on anti-Frankenstein (zero scope creep). Expected v1.2.1 average: **~8.8/10**, keeping the running average comfortably above the 8.5 v1 target.

## Next session entry point

`C:/Dev/Claude_cowork/project-genesis/.claude/docs/superpowers/resume/2026-04-17_v1_2_1_to_v1_2_2.md` — will be written at the end of this session as the resume artifact for v1.2.2. Resume prompt includes: friction triage order (F20/F22 mode-auto > F34 gh-account > F24 Phase 0.1 > F25/F31 templates > F28 cleanup), the Python-driver build order question (v1.3 or wait for more friction evidence?), and the v2 Étape 0 drop-zone hand-off from v1.2.0.
