<!-- SPDX-License-Identifier: MIT -->
---
name: Session v1.6.1 runtime auto-discovery + SOTA — 2026-04-19
description: First PATCH on v1.6.x line. Closes v1.6.0 priced-in axis caps (Best-at-date 8.7 no-R8 ; Pain-driven 9.2 paper-trace-only) via (a) 326+ line SOTA R8 entry `anthropic-prompt-engineering_2026-04-19.md` with canonical Anthropic migration guide primary citation, (b) 5 surgical template patches (C1 sampling-params 4.7 model-gated / C2 cache_control placement / C3 MCP ServerName:tool_name / L1 Phase 1 Q2 effort-acquisition / L2 Q1 metrics task-adaptive), (c) runtime evidence from fresh Claude Code session in Aurum sibling cwd (non-Genesis, plugin not installed) validating Layer 0 pépite surface fires cleanly. Honest re-rating 9.18/10 (vs projected 9.26, Self-contained dropped 0.3 on reviewer-driven P2 bundling + plan-writing discipline acknowledgement). Cross-skill-pattern #4 eighth data-point (orthogonal meta-skill PATCH zero-ripple). Pattern #1 depth update on v1.6.0 fourth data-point (no new ordinal).
type: project
version: v1.6.1
pr: "#43"
merge_commit: 2d634b9
tag: v1.6.1
predecessor: v1.6.0 (0e20462)
---

# Session v1.6.1 — Runtime auto-discovery + Anthropic prompt-eng SOTA grounding — 2026-04-19

## What shipped

**Tag v1.6.1** (PR #43 squash-merged as `2d634b9`). **First PATCH on v1.6.x line.** Closes the two priced-in honest axis caps of v1.6.0 (Best-at-date 8.7 no-R8 ; Pain-driven 9.2 paper-trace only) in one PATCH.

**8 commits in feat tranche** (squash-merged) :

1. **Spec commit `6fbce7b`** — initial spec (147 l, 3 goals, 11 ACs, 3 brainstorming Qs resolved, 7 hypotheses, axis projections).
2. **Spec-polish commit `93a3db4`** — 3 P1 + 4 P2 fixes from spec-reviewer pass, including canonical Anthropic migration guide cross-check and R8 primary citation swap for sampling-removal claim.
3. **Plan commit `c61c952`** — initial plan (468 l, 13 tasks across 5 phases, idempotency discipline).
4. **Plan-polish commit `5c197a3`** — 6 P1 + 5 P2 fixes from plan-reviewer pass (edit-target precision corrections for A5/A6 dual-location shape, A2 phantom line, A3 shell-escape, A11 zero-ripple probe rewrite, expanded idempotency table, Phase C ordering, E1 branch name, B3 placeholder discipline, running-avg math reference, ship-gate granularity, new A9.5 task for pattern #4).
5. **Feat-core commit `5cc6e83`** — 6 files +97/-10 (R8 INDEX row + 5 template patches + SKILL.md gate sentence + plugin.json bump + master.md depth updates + tests/ runbook stub). Zero Layer A / Layer B ripple verified via 4 git-diff probes.
6. **Feat-runtime commit `d59a09c`** — runtime evidence filled in `tests/runtime_auto_discovery_v1_6_1.md`. AC#7 Option A (binding rule stays non-pinned). Evidence source : fresh Claude Code session in sibling Aurum cwd (frozen read-only, Genesis plugin NOT installed). Trigger phrase `"aide-moi à drafter un prompt pour claude opus 4.7 pour un agent extracteur"`. Claude cited Layer 0 binding rule and pépite verbatim.
7. **Reviewer-driven P2 fix commit `682f522`** — code-quality reviewer flagged R8 § "What this challenges" item 1 citation order inconsistency (claudefa.st leading while TL;DR was canonical Anthropic). One-line in-place swap. Pattern matches v1.6.0 `a7b0740` precedent.

**Phase D (Layer 0 sync, post-merge, NOT in repo)** :

- `~/.claude/memory/layer0/pepite_promptor_template_anthropic_prompt_engineering.md` — 5 template patches applied verbatim (C1/C2/C3/L1/L2 — single XML `<output_template>` location in pépite, unlike skill's dual location). Synced-cache header marker bumped `v1.6.0 @ 2026-04-19` → `v1.6.1 @ 2026-04-19`.
- `~/.claude/memory/layer0/feedback_invoke_promptor_for_production_anthropic_prompts.md` — § "The rule" Skill-first preference preamble gains "runtime-validated 2026-04-19 v1.6.1 on Layer 0 pépite surface" marker. Pinning decision explicit AC#7 Option A (non-pinned). Runtime evidence scope explicitly narrows to Layer 0 pépite surface ; Skill-tool plugin-installed path deferred to v1.6.2+.
- Sentinel file `_v1_6_1_layer0_sync_DONE_2026-04-19.md` written for next-session `test -f` check.

## Why — closing v1.6.0 priced-in debt

v1.6.0 shipped at honest 9.02 with two axis caps priced in at spec time : Pain-driven 9.2 (H1 skill auto-discovery paper-trace only — confirmed via frontmatter verbatim grep, not runtime observation) and Best-at-date 8.7 (no R8 entry backed template's XML / two-phase / KV-cache / density choices against current Anthropic canon).

The "close the current minor line before stacking new features" discipline is the same reflex that made v1.5.1 → v1.5.0 honesty correction work. Two axis caps closing in one ship is more efficient than two separate ships. SOTA commissioning is blocking for the template patches (can't ship "SOTA-grounded edits" without the SOTA being shipped first) ; runtime validation is blocking for the binding-rule pinning decision.

## Architecture decisions (3 brainstorming questions resolved)

**Q1 — Patch scope: Option A (P1 only) / Option B (P1 + P2) / Option C (P1 + P2 + structured-outputs section for Part B)** → **Option B selected**.

Rationale : Option A leaves known low-risk polish items unaddressed (PATCH debt). Option C re-opens Anthropic structured-outputs vs free-form XML decision without empirical grounding — defer to pain-driven v1.6.2. Option B ships all SOTA-confirmed surgical edits (3 critical + 2 polish) in one PATCH.

**Q2 — Runtime evidence capture: Option A (screenshot + transcript paste to spec) / Option B (structured runbook at `tests/` + evidence log) / Option C (journal entry only)** → **Option B selected**.

Rationale : Option A couples evidence to spec file (becomes stale once merged). Option C puts validation in journal but makes it un-rediscoverable for future v1.6.x dogfood cycles. Option B creates reusable runbook (future v1.6.x releases repeat validation cheaply) + versioned evidence trail. Aligns with v1.5.1 dogfood-first discipline.

**Q3 — Binding-rule pinning approach: deferred to runtime evidence** (resolved at AC#7).

Runtime evidence from sibling Aurum cwd (non-Genesis, plugin not installed) confirmed Layer 0 pépite + binding-rule surface fires cleanly via trigger-phrase frontmatter match. Skill-tool plugin-installed path NOT exercised in this evidence run (by construction — sibling was non-Genesis). AC#7 Option A (non-pinned) landed on Layer 0 binding rule with scope-narrowing note ("runtime-validated 2026-04-19 v1.6.1 on Layer 0 pépite surface").

## Spec + plan reviewer P1 + P2 fixes summary

- **Spec reviewer (pre-spec-polish commit)** : 3 P1 + 4 P2 fixes.
  - P1.1 : AC#7 named the binding-rule file (`~/.claude/memory/layer0/feedback_invoke_promptor_for_production_anthropic_prompts.md § "The rule"`) as canonical owner of pinning decision — avoids orphan across AC#7/AC#8.
  - P1.2 : Pre-registered H5 (post-ship drift-count hypothesis) demoted from table to Out-of-scope NG3 — it had no observable outcome within the v1.6.1 ship window.
  - P1.3 : Canonical Anthropic migration guide cross-check commissioned via WebFetch. R8 entry primary citation for 4.7 sampling-removal claim swapped from claudefa.st (community) to `platform.claude.com/docs/en/about-claude/models/migrating-to-claude-4` (canonical). Additional canonical findings added for extended-thinking removal, thinking.display default, tokenizer change, task budgets beta.
  - P2.1 : AC#6 sibling-project defined precisely (Aurum read-only acceptable per scope-lock additive-only clause).
  - P2.2 : AC#11 gains explicit running-average delta requirement matching v1.6.0 precedent.
  - P2.3 : Template patches relabeled C1/C2/C3 + L1/L2 (was P1-a/b/c + P2-a/b) to avoid collision with reviewer P1/P2 severity labels.
  - P2.4 : AC#10 + § cross-skill-pattern #1 clarified as depth update on v1.6.0 fourth data-point, no new ordinal.

- **Plan reviewer (pre-plan-polish commit)** : 6 P1 + 5 P2 fixes.
  - P1.1 : A5/A6 split into A5a+A5b / A6a+A6b per verified dual edit-target shapes (plain-text wrapped vs XML single-line) — plan originally claimed identical source text in 2 locations which was false.
  - P1.2 : A2 `old_string` reduced to actual 2 content bullets present at template.md lines 58-60 (phantom `stop_sequences` line removed).
  - P1.3 : A3 verify grep switched from double-quote-backtick (cmd substitution) to single-quote form preserving literal backticks.
  - P1.4 : A11 4th zero-ripple probe rewritten with `--name-only | grep -vE | wc -l == 0` whitelist pattern (original grep inversion was silently broken).
  - P1.5 : D1 edit target corrected to actual pépite header format (`Synced cache from <repo>/skills/promptor/SKILL.md v1.6.0 @ 2026-04-19.`) rather than the non-existent "Last sync:" format.
  - P1.6 : Idempotency discipline expanded from 6 tasks to all 18 Edit/Write tasks across Phase A + D + E with per-task marker-grep table.
  - P2.1 : Plan-polish moved to run BEFORE Phase A (standard gate-then-execute pattern).
  - P2.2 : E1 chore branch name `chore/v1.6.1-session` to match v1.6.0 convention.
  - P2.3 : B3 commit message template flags explicit pre-commit placeholder substitution discipline.
  - P2.4 : Running-avg math reference added.
  - P2.5 : Ship-gate checklist split into edit-tasks / verify-tasks / commit-task granularity.
  - Bonus gap closed : new Task A9.5 lands master.md pattern #4 eighth data-point (spec required but original plan had no task).

- **Code-quality reviewer (pre-PR open)** : 0 P1, 1 P2.
  - P2 : R8 entry § "What this challenges" item 1 citation-order inconsistency (claudefa.st leading narrative while TL;DR and Findings § 1 had been swapped to canonical Anthropic). Bundled as reviewer-driven commit `682f522` a7b0740-style. Honest Self-contained axis deduction accepted.

## Self-rating — honest post-feat (5-axis)

**Initial projection 9.26/10. Honest post-feat re-evaluation lands at 9.18/10** (-0.08 from projection).

| Axis | Projected | Honest | Delta | Notes |
|---|---|---|---|---|
| Pain-driven | 9.4 | 9.3 | −0.1 | Runtime evidence confirmed Layer 0 pépite surface cleanly (trigger-phrase firing + artifact-naming verbatim) ; Skill-tool plugin-installed path NOT exercised (deferred to v1.6.2+ re-run with a plugin-installed sibling). Partial H1 closure, not full. Honest deduction. |
| Prose cleanliness | 9.2 | 9.2 | 0.0 | Template patches integrate without voice drift. R9 language policy respected (FR in user-facing template content, EN in dev prose). Net-positive delta on clarity via model-gating. |
| Best-at-date | 9.3 | 9.3 | 0.0 | R8 entry 326+ lines, 42+ citations, canonical Anthropic primary for load-bearing sampling-removal claim (spec-polish + code-reviewer citation-order fix both landed). Cap 9.3 (not 9.5) — R8 open question 2 (Simon Willison reverse-engineered system prompt) stays community-derived but not load-bearing for the template patches. |
| Self-contained | 9.3 | 9.0 | **−0.3** | Two honest deductions : (a) reviewer-driven P2 bundling (a7b0740-style, -0.2 per v1.6.0 precedent) ; (b) plan-reviewer caught 6 P1 vs v1.6.0's 3 P1 — plan-writing discipline weaker on first pass (-0.1). Both are honest self-assessments ; the 6 P1s were all concrete Edit-target precision issues caught pre-feat, which is the reviewer-gate working correctly, but higher P1 count on first-pass plan reflects a discipline gap. |
| Anti-Frankenstein | 9.1 | 9.1 | 0.0 | 5 patches map 1:1 to R8 § "What this challenges" items 1-5. No preemptive enumeration. Runtime runbook strict-scope. |
| **Mean** | **9.26** | **9.18** | **−0.08** | **Streak ≥ 9.0 advances to 3 consecutive** (v1.5.1 = 9.12, v1.6.0 = 9.02, v1.6.1 = 9.18). |

**Running average** : v1.6.0 post-ship = 8.88 (17 ratings). v1.6.1 = 18th. New running = (8.88 × 17 + 9.18) / 18 = 160.14 / 18 ≈ **8.90 (+0.02)**.

## Cross-skill-pattern data-points added

- **Pattern #1 (1:1 mirror discipline) — depth update on v1.6.0 fourth data-point, no new ordinal.** Both surfaces (skill + synced-cache pépite) now carry the same SOTA-validated edits from `sota/anthropic-prompt-engineering_2026-04-19.md`, demonstrating 1:1 mirror discipline survives external-canon rev-up without schema change.
- **Pattern #2 (concentrated privilege map) — unchanged.** Promptor remains privilege-class `none`. Template edits are content ; no new privilege, no new mitigation.
- **Pattern #4 (zero-ripple) — eighth data-point.** v1.6.1 PATCH on `promptor` ships with zero edits to any Layer A (`genesis-drop-zone`) or Layer B (6 skills) — verified via 4 git-diff probes (`skills/genesis-drop-zone/`, `skills/genesis-protocol/`, other Layer B skills combined, `.claude-plugin/` with `plugin.json` whitelisted) all emitting `0`. Extends v1.6.0 seventh data-point "orthogonal meta-skill ships without rippling either layer" to "orthogonal meta-skill PATCH revisions stay zero-ripple under SOTA-driven template rework".

## Hypothesis outcomes

| H | Pre-registered | Outcome |
|---|---|---|
| H1 | Skill engine surfaces `promptor` on verbatim trigger phrase in sibling project | **Partially confirmed** — Layer 0 pépite + binding-rule surface fires cleanly on trigger phrases (runtime evidence run 1, Aurum sibling). Skill-tool plugin-installed path NOT exercised (sibling was non-Genesis by design per runbook step 1). Deferred closure to v1.6.2+. |
| H2 | Bare `promptor` works ; namespace optional back-compat | **N/A in this evidence run** — sibling was non-Genesis, skill not installed, invocation-form question didn't apply. Deferred. |
| H3 | Template patches (C1/C2/C3) self-validate against R8 | **Confirmed** — code-quality reviewer mapped each patch to an R8 Findings section cleanly. |
| H4 | Anti-Frankenstein gate holds : 5 patches proportional to 5 R8 challenges | **Confirmed** — no orphan edits. |
| H5 | CHANGELOG re-rating moves Best-at-date 8.7 → 9.2+ and Pain-driven 9.2 → 9.4+ | **Partially confirmed** — Best-at-date 8.7 → 9.3 honest ✅ ; Pain-driven 9.2 → 9.3 honest (not 9.4 — partial closure only). |
| H6 | Runtime evidence file re-runnable | **Confirmed** — runbook has explicit spawn / trigger / observe / redact sections, additional § "Re-run guidance" documents triggers for future re-runs. |

## Out-of-scope follow-ups (for v1.6.2 or later)

- **Skill-tool plugin-installed auto-discovery runtime evidence** (H1 full closure) — spawn fresh Claude Code session in a sibling where the `project-genesis` plugin IS installed (user-scope or `--plugin-dir`). Re-run the runbook, capture Skill-tool invocation form evidence. Route AC#7 decision to Option A / B / C per observation.
- **Structured-outputs migration path in Part B XML payload** (R8 open question 5) — pain-triggered ; first reported production friction triggers v1.6.2 spec.
- **Trigger-phrase redundancy expansion** (community under-triggering finding) — if runtime validation shows misses on alternate phrasings, v1.6.2 spec.
- **Automated pépite ↔ skill sync script** (NG3) — first observed drift between v1.6.0 merge and any subsequent release triggers a v1.6.2 spec.
- **1M context + effort interaction empirical benchmark** (R8 open question 4) — tied to Aurum multi-LLM eventual work, not standalone Genesis PATCH scope.
- **Thinking + cache composition test prompt measurement** (R8 open question 1) — needs a test harness ; post-v2 work.
- **Plugin slash-command pinning stability** (R8 open question 3, GitHub issue #34144) — monitor upstream fix ; if resolved, revisit AC#7 Option A feasibility.
- **v1.5.2 runtime dogfood** of Phase 0.4 / 0.5 / archive / halt cards (still queued from v1.5.1 resume, now 2 cycles deep).
- **v1.5.3 Friction #3 retirement-trigger semantics** for Phase 0.4 (lower urgency).

## What's next

Next session candidates (in suggested priority order) :

1. **v1.6.2 — Skill-tool plugin-installed auto-discovery runtime evidence** (~1-2h). Closes H1 full closure. Requires sibling where plugin is installed. Lifts Pain-driven axis cap from 9.3 → 9.4+ if evidence holds. Smallest, most-targeted follow-up on v1.6.x line.
2. **v1.5.2 — Runtime dogfood** (~2-3h). Queued 2 cycles from v1.5.1. Strengthens v1.5.x line.
3. **v1.5.3 — Friction #3 retirement semantics** (~4-5h). Lower urgency.
4. **v1.7.0 — new skill ship** (if user has a clear candidate) — lower priority until v1.6.x line is fully closed.

## PR + tag state

- Branch `feat/v1.6.1-runtime-and-sota` PR #43 squash-merged as `2d634b9`.
- Tag `v1.6.1` pushed.
- Worktree `C:/Dev/Claude_cowork/project-genesis/.claude/worktrees/feat_2026-04-19_v1_6_1_runtime_and_sota/` retained per R2.5 forensic.
- Chore worktree `C:/Dev/Claude_cowork/project-genesis/.claude/worktrees/chore_2026-04-19_v1_6_1_session/` for this chore commit.
- Tag chain: … v1.5.0 → v1.5.1 → v1.6.0 → **v1.6.1**. 18 tagged versions total (v1.0.0 through v1.6.1).
- Phase D Layer 0 sync sentinel : `~/.claude/memory/layer0/_v1_6_1_layer0_sync_DONE_2026-04-19.md` exists.

## R2.3.1 observation

Mid-session `gh` active-account flip-back reproduced the historic pattern (Active account drifts back to `myconciergerieavelizy-cloud`). Resolved via `gh auth switch -u myconciergerie-prog` + **`GH_TOKEN` env override** on the `gh pr create` call — the switch by itself was not sufficient for write API calls on this session. This is a second data-point confirming the resume's R2.3.1 warning and the Layer 0 `workflow_github_and_tooling.md` GH_TOKEN-env-override pattern. Candidate for amplification if the pattern repeats : encode the `GH_TOKEN=$(gh auth token -u myconciergerie-prog)` prefix as mandatory pre-flight before any write gh call.
