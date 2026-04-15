<!-- SPDX-License-Identifier: MIT -->
---
name: Session v0.7.0 — Pépite flagging skill + R8 slug rule correction (2026-04-15)
description: Session that picked up the v0.6.0 → v0.7.0 handoff, confirmed Option A (pepite-flagging), and shipped skills/pepite-flagging/ as a 1:1 mirror of the canonical spec — the last independent skill stub. R8 claude-code-session-jsonl-format entry amended in-place for the underscore + forward slash slug rule correction (first live-dogfood amend, not a supersede chain). Tagged v0.7.0 at self-rating 8.8/10.
type: project
session_date: 2026-04-15
shipped_version: v0.7.0
self_rating: 8.8
---

# Session v0.7.0 — Pépite flagging skill + R8 slug rule correction

## Context

Sixth full skill-implementation session of Project Genesis. Picked up the v0.6.0 → v0.7.0 resume prompt, confirmed the suggested Option A (`pepite-flagging` skill) with the 5-minute R8 research-entry refresh bundled in as a side-fix, and delivered both in a single feat branch.

The session is notable for three things:

1. **Last independent skill stub shipped.** With `pepite-flagging/` live, the only remaining stub is `genesis-protocol/` — the orchestrator that composes the five shipped skills into the 7-phase protocol from the master vision. The next session is the v1.0.0 ship candidate.
2. **Second 1:1 spec mirror.** After `journal-system` in v0.4.0, this is the second time a skill ships as a strict mirror of a canonical spec. The discipline is cheap and defensible: every file explicitly commits to tracking the spec, drift is a merge-blocker.
3. **First in-place R8 amend after live-dogfood correction.** The v0.6.0 session flagged the slug underscore rule as a latent gap in the `claude-code-session-jsonl-format_2026-04-15` R8 entry. The code was fixed immediately, but the research entry stayed wrong on disk for one session. v0.7.0 closes that gap in-place (not via supersede chain, because the correction is a bug fix, not new research) and adds forward slash `/` as well to cover git-bash-style cwd strings on Windows. Note about the correction is recorded inline in the entry with a pointer to `memory/journal/2026-04-15_slug-rule-live-dogfood-correction.md` for the epistemic context.

## The pepite-flagging skill

Six files under `skills/pepite-flagging/`, ~936 lines total, pure Markdown + YAML. No Python runtime — detection and flagging happen inside Claude's own research operations via the built-in Write tool; no external dependencies, no pip, no binaries.

| File | Lines | Purpose |
|---|---|---|
| `SKILL.md` | 141 | Entry point, automatic + manual trigger phrases, five-step flow (detect → create → surface → act → INDEX), hard rules, anti-Frankenstein scope locks |
| `trigger-criteria.md` | 129 | The six red-light criteria with rationale, calibration example, and anti-noise guard per criterion. "Two or more" scoring table with worked examples. Anti-over-flagging and anti-under-flagging discipline |
| `pepite-format.md` | 220 | 14-field frontmatter schema, body section order, slug derivation, status transition table, idempotency rules, one illustrative example marked as non-real |
| `cross-project-routing.md` | 214 | Pointer file template, per-target consent (never batched silently), v1 hard-coded machine map, cold-read protocol for consumers, v2 deferral list |
| `install-manifest.yaml` | 150 | Idempotent `memory/pepites/` + `INDEX.md` creation with `create_if_missing_only` guard, three verification checks, no runtime dependency |
| `verification.md` | 232 | Two-mode health card with 13 checks, halt-on-RED on missing required fields, illegal transitions, or cross-project consent bypass |

Every file references the canonical spec `.claude/docs/superpowers/specs/v1_pepite_discovery_flagging.md` and explicitly commits to the 1:1 mirror discipline.

## The consent floor

The cross-project pointer write is the only privileged operation in this skill. Like `session-post-processor`'s halt-on-leak gate, it is a **single concentrated privilege** that exists for one specific reason and must never happen without explicit per-invocation, per-target consent. Parallels:

| Skill | Privileged operation | Consent gate | Failure mode |
|---|---|---|---|
| `session-post-processor` | Delete archive file on leak detection | N/A — the gate is defensive and triggered by the skill's own verification | RED card + file deletion + non-zero exit |
| `pepite-flagging` | Write pointer file to sibling project auto-memory | Per-target user yes (never batched, silence is skip) | RED card + pointer deletion + consent bypass incident |

Concentrating privilege in one place per skill is the anti-Frankenstein discipline applied to write surfaces. The rest of each skill is read-only or writes only inside its own project's memory.

## The R8 slug rule correction

The v0.6.0 session discovered that the R8 `claude-code-session-jsonl-format_2026-04-15` entry listed `\`, `:`, and space as the cwd-to-slug replacement characters, but the real rule also includes underscore (`C:\Dev\Claude_cowork\project-genesis` → `C--Dev-Claude-cowork-project-genesis`, not `C--Dev-Claude_cowork-project-genesis`). Code was fixed in `slugify_cwd()` at v0.6 shipping time; the research entry stayed wrong.

In this session the entry is amended in place:

- Full replacement set now: `\`, `/`, `:`, `_`, space
- Inline note: *"Correction 2026-04-15 (live dogfood): the original 2026-04-15 draft of this entry listed only `\`, `:`, and space..."*
- Pointer to `memory/journal/2026-04-15_slug-rule-live-dogfood-correction.md` for the epistemic notes
- Forward slash `/` added to cover git-bash cwd strings (e.g. `/c/Dev/Claude_cowork/project-genesis`)
- TTL left unchanged (still `expires_at: 2026-04-16` because the correction is a bug fix, not a confidence-reset)

This is the **first time** an R8 entry has been amended in place after a live-dogfood correction rather than moved to `archive/` and replaced via a new successor entry. The justification is that the correction is a bug fix (character-class omission), not new research. If the entry's substance changed, a supersede chain would be correct; because only the typo changed, in-place edit preserves the supersede history cleanly.

Recording this as precedent: **in-place amend is acceptable for R8 entries when the correction is a documented bug fix with a clear single-character or single-line scope. Anything larger goes through `archive/` + successor.**

## Granular commits (9 in the feat branch)

1. `fix(research): R8 slug rule correction — underscore + forward slash`
2. `feat(pepite-flagging): add SKILL.md entry point with 5-step flow`
3. `feat(pepite-flagging): add trigger-criteria.md — six red-light rules`
4. `feat(pepite-flagging): add pepite-format.md — frontmatter schema + status transitions`
5. `feat(pepite-flagging): add cross-project-routing.md — pointer file mechanism`
6. `feat(pepite-flagging): add install-manifest.yaml — idempotent directory + INDEX seed`
7. `feat(pepite-flagging): add verification.md — halt-on-RED consent floor`
8. `chore: bump plugin.json to 0.7.0 + add pepite-flagging keyword`
9. `docs(changelog): v0.7.0 entry with 8.8/10 self-rating`

Three of the nine commit messages lost their newlines due to a bash heredoc quoting issue, but squash-merge flattened them on `5955a47`, so main's log is clean. The feat branch remnants are forensic only.

Squashed via `GH_TOKEN="$GH_TOKEN" gh pr merge 12 --squash`, tag `v0.7.0` pushed to origin.

## Anti-Frankenstein discipline applied

Things the session **deliberately did not do**:

- **No runtime code** in pepite-flagging. Detection is a judgement call inside Claude's own turn, not a deterministic pipeline. A Python implementation would either duplicate the LLM or under-serve the detection
- **No slash commands** (`/pepite list`, `/pepite propagate`, `/pepite status`) — v2 target, deferred
- **No auto-propagation** even when `relevance.specific_projects` is set — v2 target
- **No pépite TTL** — seeds do not expire, user decides when to archive
- **No cross-pépite synthesis** — clustering and similarity are v2 targets
- **No pépite ranking** — no priority field, no effort estimate, no ROI calculator
- **No auto-discovery of sibling projects** — the v1 machine map is hard-coded in `cross-project-routing.md`. Walking `~/.claude/projects/*/` + `C:\Dev\*\` is a v2 target
- **No pre-seeded example pépite** — the illustrative DuckDB+VSS example in `pepite-format.md` is explicitly marked non-real. The first real pépite will be detected during v0.7+ research sessions, not synthesised now
- **No pepite-flagging detection on this session** — the session is implementation work, not research, so no pépites were flagged. The skill's first real use happens in a future research-heavy session

## Self-rating — v0.7.0

| Axis | Rating | Rationale |
|---|---|---|
| Pain-driven coverage | 9/10 | Every file maps to a spec section or consent concern. Trigger criteria calibration reflects anti-over-flagging and anti-under-flagging pains. R8 slug rule fix closes v0.6 latent debt. Zero speculative features. |
| Prose cleanliness | 8/10 | Six files, ~936 lines. Each file has a clear job with minimal overlap. Tables throughout for criteria, transitions, checks. Hard-coded machine map in `cross-project-routing.md` is prose-ugly but v1-honest. |
| Best-at-date alignment | 9/10 | Criteria 3 (emerging tech) and 6 (highest potential) directly operationalise the Layer 0 best-practice-at-date rule. Cross-project routing is first operational component of Meta-Memory Layer 3 (stepping stone to Path B). Pointer file format uses current `type: reference` convention. |
| Self-contained | 9/10 | Pure Markdown + YAML. Zero runtime dependencies. Install step touches only `memory/pepites/` inside target project. Cross-project pointers are additive auto-memory writes, never touch git state. |
| Anti-Frankenstein | 9/10 | Explicit v2 deferral list in multiple files. The skill's surface is exactly six files mirroring a frozen spec. Manual force-flag path exists but primary mode is auto-detection because that's where the pain is. Pre-seeded example marked non-real to prevent false provenance. |
| **Average** | **8.8/10** | Clears 8.0/10 floor by 0.8. Ties v0.4.0 (journal-system, also 8.8/10) as highest single-version rating. Above v0.6.0 (8.6/10) because the 1:1 spec mirror is a cleaner rating surface than first-runnable-code. |

Running average v0.2 → v0.7 = (7.6 + 8.2 + 8.8 + 8.4 + 8.6 + 8.8) / 6 = **8.40/10**. On track for v1 target 8.5/10 — the last milestone (`genesis-protocol`) needs to land at ≥ 9.1 to reach it. Tight but achievable because the orchestrator's rating ceiling depends on how cleanly it composes the five shipped skills — and cleanly composing proven components is exactly the shape of a high rating.

## Gaps logged for v0.8.0

- **`genesis-protocol` orchestrator** — the last remaining stub. Composes all five shipped skills into the 7-phase protocol from the master vision. This is the v1.0.0 ship target.
- **Dogfood run 3 for `session-post-processor`** — still pending. Needs either a future Genesis session or the first Aurum session after the freeze lifts. Hook wiring stays deferred until run 3 lands CLEAN.
- **Multi-slug YELLOW warning in `run.py`** — v0.5 gap, still deferred.
- **Test vector harness for redaction patterns** — v0.5 gap.
- **Allow-list for `generic_long_base64` false positives** — v0.6 gap.
- **First real pépite detection** — no pépites flagged in this session because it's implementation, not research. First real flag happens in a v0.7+ research session.
- **Auto-discovery of sibling projects** for cross-project routing (v2 target, hard-coded map suffices for v1).

## Disciplines reinforced

- **Granular commits inside the feat branch** — sixth consecutive session with the discipline. Default now, not new.
- **R8 in-place amend for bug-fix corrections** — new precedent this session. Scope: single-line or single-character fixes only; larger changes go through `archive/` + successor.
- **1:1 spec mirror discipline** — second application (first was journal-system). Cheap and defensible.
- **Consent floor per privileged operation** — pepite-flagging's cross-project pointer write joins session-post-processor's halt-on-leak gate as the second example of the "concentrated privilege" pattern. Each skill has at most one privileged write operation, gated explicitly.
- **PAT via `GH_TOKEN` env override** — sixth consecutive session, additive auth preserved.
- **SSH for git, `GH_TOKEN` for API** — same split as v0.2 → v0.6.
- **Worktree discipline R2.1** — feat worktree created first, all edits inside, no merge-to-main shortcuts.

## Forward map

- **v0.8.0 = v1.0.0 candidate** — `genesis-protocol` orchestrator. Alternative: small maintenance version (hook wiring for session-post-processor, test vector harness, allow-list) if the user wants to reduce debt before the ship. The anti-Frankenstein discipline says ship first, polish after.
- **After v1.0.0** — public announcement, marketplace submission (self-hosted first, official Anthropic marketplace deferred), README polish, downstream project bootstrap to prove the recursive loop from scratch.
- **v1.1.0 / v1.2.0** — backlog paydown: hook wiring, test harness, allow-list, multi-slug warning, auto-discovery for cross-project routing.
- **v2.x** — Meta-Memory Path B session (graph tooling, cross-project search, backlinks, promote). See Layer 0 `~/.claude/CLAUDE.md` for the design.

## PR and tag

- **PR**: [#12](https://github.com/myconciergerie-prog/project-genesis/pull/12) — "feat(pepite-flagging): last independent skill stub + R8 slug rule fix [v0.7.0]"
- **Merge commit**: `5955a47`
- **Tag**: `v0.7.0` on `5955a47`, pushed to origin
