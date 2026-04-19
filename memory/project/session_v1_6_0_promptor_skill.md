<!-- SPDX-License-Identifier: MIT -->
---
name: Session v1.6.0 promptor skill — 2026-04-19
description: First MINOR on v1.6.x line. Promotes Layer 0 Promptor pépite into standalone Genesis skill at skills/promptor/. 8th skill, 2nd privilege-`none` skill, first orthogonal meta-skill (neither Layer A nor Layer B). Skill canonical, Layer 0 pépite demoted to synced cache. Honest re-rating 9.02/10 (vs projected 9.14, Self-contained dropped 0.2 on bundling-scope from in-feat code-quality reviewer fixes). Cross-skill-pattern #4 gains sixth (v1.5.1 reconciliation) + seventh (orthogonal meta-skill zero ripple) data-points.
type: project
version: v1.6.0
pr: "#41"
merge_commit: 0e20462
tag: v1.6.0
predecessor: v1.5.1 (eba3e46)
---

# Session v1.6.0 — Promptor skill — 2026-04-19

## What shipped

**Tag v1.6.0** (PR #41 squash-merged as `0e20462`). **MINOR** — first net-new skill ship since v1.3.0 opened the v1.3.x conversational-layer line. Promotes the Layer 0 Promptor pépite into a standalone Genesis skill at `skills/promptor/`. Skill becomes canonical source of truth ; Layer 0 pépite demoted to synced cache role.

**6 commits in feat tranche** (squash-merged) :

1. **Spec commit** — `.claude/docs/superpowers/specs/2026-04-19-v1.6.0-promptor-skill-design.md` (~177 lines). Initial design.
2. **Spec polish commit** — 5 P1 + 4 P2 fixes from spec-reviewer pass : forward-naming reservation for `skills/promptor/` namespace (template track vs v2 conversational track) ; binding rule non-pinned syntax language ; AC#5 read-only verification rewrite ; H6 + H7 hypotheses added (H7 refuted by construction) ; pépite § Cross-references tense fix added to cross-cutting changes ; sync-timestamp drift acknowledged in out-of-scope ; AC#2 tightened to verbatim ; Best-at-date axis dropped 9.0 → 8.7 honest deduction (no R8 SOTA grounding) ; privilege-none count corrected 4th → 2nd.
3. **Plan commit** — `.claude/docs/superpowers/plans/2026-04-19-v1.6.0-promptor-skill.md` (~1034 lines, 15 tasks across 3 phases).
4. **Plan polish commit** — 3 P1 + 5 P2 fixes from plan-reviewer pass : AC#2 verification with full verbatim binding-rule trigger strings (was substring-only) ; duplicate Step 2.2 fixed (renumbered 2.3-2.7) ; R2.3.1 pre-flight added before every gh write op + GH_TOKEN env override ; pre-Phase-A dogfood-first acknowledgement per Layer 0 v1.5.1 lesson (silence-is-omission) ; crash-window remediation + PR# capture mechanism + sentinel file for Phase B completion tracking ; idempotency discipline section + marker-grep before each append-style Edit (Tasks 3, 5, 8, 9) ; head -2 robust SPDX checks ; Step 5.4 atomicity warning re three sub-claims ; R1.1 ritual continuation-vs-new-session clarification at Task 10.
5. **Feat commits 1-5** — `skills/promptor/SKILL.md` (~80 l) + `skills/promptor/references/template.md` (~137 l) + `.claude-plugin/plugin.json` 1.5.1 → 1.6.0 + 3 keywords + `skills/README.md` entry + `memory/master.md` pattern data-points #1, #2, #4.
6. **Code-quality reviewer P1 fix commit `a7b0740`** — 2 reviewer-driven correctness fixes bundled as 6th commit : (a) `skills/README.md` preamble "All six skills are shipped as of v0.8.0" was stale (count off by 2 after v1.3.0 + v1.6.0 added 2 skills) → updated to "v1.6.0 (8 skills)" with brief shipping-history breakdown ; (b) `memory/master.md` pattern #4 ordinal sequence skipped from "Fifth data-point" (v1.5.0) directly to "Seventh data-point" (v1.6.0) → added missing **Sixth data-point** sentence reconciling v1.5.1 PATCH into the master.md narrative (the v1.5.1 PATCH never updated master.md), demonstrating zero-ripple holds under PATCH constraint as well as MINOR-level expansive ships.

**Phase B (Layer 0 sync, post-merge, NOT in repo)** :

- `~/.claude/memory/layer0/pepite_promptor_template_anthropic_prompt_engineering.md` — synced-cache header note added after frontmatter ; § "Cross-references" tense fix from "candidate" to past-tense "promotion".
- `~/.claude/memory/layer0/feedback_invoke_promptor_for_production_anthropic_prompts.md` — § "The rule" gains "Skill-first preference (added 2026-04-19, v1.6.0)" preamble with non-pinned skill-invocation syntax.
- Sentinel file `_v1_6_0_layer0_sync_DONE_2026-04-19.md` written for next-session `test -f` check.

## Why — cross-project utility for Anthropic prompt-engineering

The Promptor template was captured 2026-04-18 as a Layer 0 pépite (`pepite_promptor_template_anthropic_prompt_engineering.md`) + binding rule (`feedback_invoke_promptor_for_production_anthropic_prompts.md`). Together they cover **this user's machine** but **do not propagate to other machines** or to **new projects bootstrapped via Genesis**.

Cross-project pain is real and measured : every Anthropic-API-using project bootstrapped via Genesis (Aurum.ai runtime agents, Cyrano AI assistant, Myconciergerie ride-booking agent, future projects) needs production-grade prompt engineering. Without a Genesis-shipped skill, each new project would either (a) re-derive the template manually, (b) copy-paste the pépite from this user's Layer 0, or (c) skip the discipline and ship sub-calibrated prompts.

The 2026-04-19 Option C decision (recorded in v1.5.0 session context, re-confirmed in v1.5.1 resume) flagged Promptor skill promotion as the v1.6.0 target after v1.5.x line completion. v1.5.1 closed v1.5.0's three-gap honesty correction. v1.6.0 opens this new track.

## Architecture decisions (3 brainstorming questions resolved)

**Q1 — Source of truth : Option A (pépite canonical) / B (skill canonical, retire pépite) / C (skill canonical, pépite as synced cache)** → **Option C selected**.

Rationale : Option A would leave marketplace-shipped form vulnerable to per-machine drift, no clear authority for new-project bootstrap inheritance. Option B would break sessions opened outside Genesis-bootstrapped projects on this machine. Option C preserves both surfaces with explicit canonical/cache disambiguation, manual sync convention at expected frequency.

**Q2 — File layout : Option A (single SKILL.md) / B (SKILL.md + references/template.md split) / C (SKILL.md + references/ multiple files)** → **Option B selected**.

Rationale : SKILL.md as gate (when to invoke) + references/template.md as content (what to render) keeps invocation-time token cost minimal. Phase 1 standby reads SKILL.md only ; Phase 2 creation reads references/template.md. Option C (multiple reference files) overkill at 1 template.

**Q3 — Surfacing : Option A (skill description only) / B (slash command `/promptor`) / C (both)** → **Option A selected**.

Rationale : All 7 prior Genesis skills surface via skill-description match. Adding a slash command for Promptor only would be a structural anomaly. Marginal UX gain not worth the precedent cost. Direct invocation remains available via the `Skill` tool.

## Spec + plan reviewer P1 + P2 fixes summary

- **Spec reviewer** : 5 P1 + 4 P2 fixes — forward-naming reservation, non-pinned binding rule syntax, AC#5 read-only rewrite, H6+H7 hypotheses (H7 refuted by construction), pépite tense fix, sync-timestamp drift in out-of-scope, AC#2 verbatim tightening, Best-at-date 9.0 → 8.7 honest deduction, privilege-none count 4th → 2nd correction.
- **Plan reviewer** : 3 P1 + 5 P2 fixes — AC#2 full verbatim grep -F, duplicate Step 2.2 renumbering, R2.3.1 pre-flight + GH_TOKEN env override before every gh write op, pre-Phase-A dogfood-first acknowledgement (Layer 0 v1.5.1 lesson), crash-window remediation + PR# capture + sentinel file, idempotency marker-grep discipline, head -2 robust SPDX checks, Step 5.4 atomicity warning, R1.1 continuation-vs-new-session clarification.
- **Code-quality reviewer (Phase A in-feat)** : 2 P1 fixes — README preamble stale count + master.md pattern #4 ordinal sequence skip (v1.5.1 sixth data-point missing). Both bundled as 6th feat commit `a7b0740`. Honest assessment : both directly traceable to v1.6.0 ship, not unrelated cleanup, but bundling stretched "self-contained" envelope → 0.2 deduction on Self-contained axis from projection.

## Self-rating — honest post-feat (5-axis)

| Axis | Projected | Honest | Delta | Notes |
|---|---|---|---|---|
| Pain-driven | 9.2 | 9.2 | 0.0 | Cross-project utility = real pain. Capped at 9.2 because runtime auto-discovery validation deferred to v1.6.1 (cannot exercise skill engine in same session that ships skill). |
| Prose cleanliness | 9.3 | 9.3 | 0.0 | Two focused files with crisp gate/template separation. Frontmatter triggers verbatim (single source). 1:1 mirror discipline declared in both files with sync metadata. |
| Best-at-date | 8.7 | 8.7 | 0.0 | Honest deduction priced in at spec time per P2.3 reviewer feedback — cited R8 entry is about v2 drop-zone landscape, not Anthropic prompt-engineering SOTA. v1.6.1 candidate to commission fresh `sota/anthropic-prompt-engineering_<date>.md`. |
| Self-contained | 9.5 | 9.3 | **−0.2** | **Honest deduction.** Phase A bundled 2 reviewer-driven prose fixes as 6th commit `a7b0740` (README preamble + master.md pattern #4). Both fixes directly traceable to v1.6.0 ship, not unrelated cleanup, but bundling them in same feat tranche rather than separate PATCH stretched "self-contained" envelope. |
| Anti-Frankenstein | 9.0 | 9.0 | 0.0 | Net new = 2 skill files + 3 keywords + Layer 0 sync notes (manual, no script) + 2 in-feat correctness fixes. Reviewer ceremony proportional. Five anti-pattern rejections documented (pre-cooked examples / slash command / auto-sync script / Layer M / retiring pépite outright / pépite-as-canonical). |
| **Mean** | **9.14** | **9.02** | **−0.12** | **Streak ≥ 9.0 advances to 2 consecutive** (v1.5.1 = 9.12, v1.6.0 = 9.02). |

Running average post-v1.6.0 honest: ≈ **8.88/10** (+0.01 vs v1.5.1 running 8.87). MINOR tranche restoring the +0.01 increment cadence.

## Cross-skill-pattern data-points added

- **Pattern #1 (1:1 mirror discipline) — fourth data-point.** `promptor` SKILL.md + references/template.md mirror Layer 0 pépite. Per master.md count (which includes self-mirror), this is the fourth data-point. Drift = merge-blocker per declared sync convention.
- **Pattern #2 (concentrated privilege map) — 8th skill data-point.** Privilege class `none` (no disk write, no network, no subprocess). 2nd none-class skill (joins `journal-system`). Cleanest possible map entry — no mitigations needed since no privilege.
- **Pattern #4 (Layer A/B + zero-ripple) — sixth + seventh data-points.**
  - **Sixth data-point** : v1.5.1 PATCH was tracked in CHANGELOG but never updated `master.md` — v1.6.0 reconciles by adding the missing sentence. Demonstrates zero-ripple holds under PATCH constraint as well as MINOR expansion.
  - **Seventh data-point** : v1.6.0 promptor ships as orthogonal meta-skill, neither Layer A nor Layer B, with zero edits to any Layer A or Layer B skill. Only cross-cutting touches are `master.md` (data-points + orthogonal note) and `skills/README.md` (entry). **Extends zero-ripple principle from "Layer A grows / corrects / opt-in renders without rippling Layer B" to "new orthogonal meta-skill ships without rippling either layer".**

Per anti-Frankenstein : no third "Layer M" (meta) category introduced for one skill ; will emerge naturally if a 2nd meta-skill arrives.

## Hypothesis outcomes (spec pre-registered H1-H7)

| H | Pre-registered | Outcome |
|---|---|---|
| H1 | Skill description triggers auto-discovery on binding rule trigger phrases | **Confirmed (paper-trace)** via frontmatter description verbatim grep ; runtime confirmation deferred to v1.6.1 |
| H2 | Pattern #4 zero-ripple holds for orthogonal meta-skills | **Confirmed** by grep on 7 existing skill directories — zero diff |
| H3 | Pattern #2 accommodates 8th skill privilege `none` cleanly | **Confirmed** — no mitigation table required, map entry degenerate |
| H4 | Layer 0 pépite + binding rule continue to function unchanged for non-Genesis sessions | **Confirmed** — header note additive, body untouched, binding rule update additive prepend |
| H5 | Single-source-of-truth model avoids drift in v1.6.0 → v1.6.x evolution | **Cannot be confirmed in v1.6.0 ship** — requires future content evolution. Tentatively confirmed by existence of explicit sync convention. |
| H6 | Verbatim trigger phrase list yields better skill auto-discovery match than abstract description | **Cannot be confirmed in v1.6.0 ship** — requires controlled comparison in future v1.6.x A/B. Defaulting to verbatim per binding rule's explicit triggers. |
| H7 | Layer 0 binding rule update propagates to other devices automatically | **Refuted by construction** — Layer 0 lives at `~/.claude/memory/layer0/` per machine ; v1.6.0 update is single-machine. Cross-device sync explicitly out of scope. |

## Out-of-scope follow-ups (for v1.6.x or later)

- **v1.6.1 — Runtime auto-discovery validation** : spawn fresh Claude Code session in any Genesis-bootstrapped sibling project, type one of the trigger phrases, observe skill engine surfacing `promptor` (~3-4h with R8 grounding below)
- **v1.6.1 — Anthropic prompt-engineering 2026-04 SOTA grounding** : commission fresh `sota/anthropic-prompt-engineering_<date>.md` R8 entry, re-anchor template's choices, lift Best-at-date axis ceiling above 8.7 cap
- **v1.5.2 — Runtime (not paper-trace) dogfood** of Phase 0.4 / 0.5 / archive / halt cards : still queued from v1.5.1 resume (~2-3h)
- **v1.5.3 — Friction #3 retirement-trigger semantics** for Phase 0.4 (~4-5h)
- **Domain adaptation examples** : if user reports re-deriving same adaptation pattern multiple times across projects, capture as `references/adaptations/<domain>.md`. Pain-driven, not preemptive.
- **Auto-sync script for pépite** : if Layer 0 pépite ↔ skill drift becomes real (observed > 0 times), write `scripts/sync_layer0_pepite.sh`. Pain-driven. Pain-trigger = first observed drift event.
- **Promptor v2 conversational pipeline** : separate v2 spec (`v2_vision_promptor_fusion.md`). Independent track. Forward-naming reservation for v2's skill name(s) in Non-goal #1.
- **Cross-link skill to v2 vision spec** : once v2 lands, add `## Related skills` to SKILL.md.
- **Cross-device Layer 0 sync (multidevice scenario)** — H7 refuted by construction ; future Layer 0 hygiene work, separate from v1.6.x line.

## What's next

Next session candidates (in suggested priority order) :

1. **v1.6.1 — Runtime auto-discovery + Anthropic prompt-eng SOTA R8 grounding** (~3-4h). Closes Best-at-date axis cap (8.7 → 9.2+) + validates H1 with runtime evidence + lifts honest mean from 9.02 to ~9.20 projected. Strongest follow-on for v1.6.x line continuity.
2. **v1.5.2 — Runtime (not paper-trace) dogfood** of Phase 0.4 / 0.5 / archive / halt cards (~2-3h). Still queued from v1.5.1 resume. Strengthens Pain-driven axis on v1.5.x line.
3. **v1.5.3 — Friction #3 retirement-trigger semantics** for Phase 0.4 (~4-5h). Lower urgency.

## PR + tag state

- Branch `feat/v1.6.0-promptor-skill` PR #41 squash-merged as `0e20462`.
- Tag `v1.6.0` pushed.
- Worktree `C:/Dev/Claude_cowork/project-genesis/.claude/worktrees/feat_2026-04-19_v1_6_0_promptor_skill/` retained per R2.5 forensic.
- Chore worktree `C:/Dev/Claude_cowork/project-genesis/.claude/worktrees/chore_2026-04-19_v1_6_0_session/` for this chore commit.
- Tag chain: … v1.4.2 → v1.5.0 → v1.5.1 → **v1.6.0**.
- Phase B Layer 0 sync sentinel : `~/.claude/memory/layer0/_v1_6_0_layer0_sync_DONE_2026-04-19.md` exists.
