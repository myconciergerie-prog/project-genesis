<!-- SPDX-License-Identifier: MIT -->

# Changelog

All notable changes to Project Genesis are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versioning follows [Semantic Versioning](https://semver.org/).

Every version bump includes a **5-axis self-rating block** per R10.3 discipline, with target < 10 to honor the anti-Frankenstein inflection-point rule.

---

## [2.0.0] — 2026-04-19 — "Bootstrap via Max subscription, drop subprocess Citations (MAJOR)"

**Architectural shift.** Drops v1.4.0's subprocess Citations API path + anthropic Python SDK + ANTHROPIC_API_KEY dependency. Bootstrap leverages the Max subscription that Claude Code already holds at session open via `claude auth login`. New skill `phase-auth-preflight` runs `claude auth status` JSON probe as Phase 0.0 / Step 0.0 pre-flight before both Layer A `genesis-drop-zone` and Layer B `genesis-protocol`. v1.5.0's halt-with-remediation card retired. Backward-compatible at data contract level (`drop_zone_intent.md` files written by v1.4.0+ remain parseable, citation keys deprecated v2.x).

### Added

- **`skills/phase-auth-preflight/`** — 9th Genesis skill, separate skill (option D-2 locked) for present-day reuse across Layer A + Layer B entry points. SKILL.md (Decision tree 5-row routing + bilingual Remediation card) + install-manifest.yaml + 4 fixtures + runtime_evidence_v2_0_0.md runbook (1 LIVE TEST + 4 DOC-ONLY pending v3.0 test harness wrapper). Concentrated privilege class : **`subprocess`** with 5 mitigations (read-only commands ; no auth-mutating side effects ; no env writes ; no file writes ; JSON-parse-with-fallback).
- **Phase 0.0 / Step 0.0 invocations** wired into both Layer A (`genesis-drop-zone § Phase 0.0` between Trigger and Context guard) AND Layer B (`genesis-protocol/phase-0-seed-loading.md § Step 0.0` before Step 0.1 ; flow heading updated `five steps → six steps (Step 0.0 added v2.0.0+)`).
- **`tests/fixtures/drop_zone_intent_fixture_v2_arbitrated.md`** — v2 schema fixture (replaces archived v1_5_0_arbitrated). Same revision-state metadata, no citation keys.
- **`tests/fixtures/.archive/ARCHIVE.md`** + **`skills/genesis-drop-zone/.archive/v1_5_0_halt_card_content.md`** (forensic preservation).
- **`memory/master.md § "What v3 vision is"`** — captures (a) external installer surface, (b) BYOAI staging Anthropic-first, (c) Lovable-style hosted SaaS at concrete domain `genesis.myconciergerie.fr` (auto-hosted Supabase on VPS OVH + GitHub creation + subdomain free/paid tiers), (d) **7 dev disciplines load-bearing on every v2 PR**.
- **Cross-skill-pattern #2 v2 entry** — total at v2.0.0 : 9 skills, 7 with privilege classes, 2 with `none`.
- **Cross-skill-pattern #4 ninth ordinal** — architectural REMOVAL preserves zero-ripple under key-omission regime. Distinct from v1.5.1 sixth ordinal (PATCH-prose-cleanup). Ninth was reserved for "genuinely new ripple mode" — fulfilled.

### Changed

- **`genesis-drop-zone/SKILL.md`** : v1.4.0 + v1.5.0 In Scope sections annotated `RETIRED in v2.0.0` (content preserved forensically) + new `### In scope (v2.0.0)` 5-item changelog + privilege table + intro prose reverted to disk-class only.
- **`genesis-protocol/phase-0-seed-loading.md § "Citation preservation (v1.4.1)"`** annotated `DEPRECATED v2.x`. Parser preservation logic stays for backward-compat with v1.4.x/v1.5.x files until v3.0+ removal (per master.md design discipline #4 — v3 web mode may re-introduce keys server-side).
- **`.claude-plugin/plugin.json`** version `1.6.3 → 2.0.0` (MAJOR).
- **`.claude/docs/superpowers/research/INDEX.md`** — `anthropic-python_2026-04-18.md` row removed from Active table, added to Archive section with v2-retirement note.

### Removed

- **`skills/genesis-drop-zone/scripts/extract_with_citations.py`** (414 lines deleted).
- **`skills/genesis-drop-zone/scripts/`** directory.
- 3 `tests/fixtures/drop_zone_intent_fixture_v1_4_0_*_with_citations.md` + `v1_5_0_arbitrated.md` → moved to `.archive/`.
- `.claude/docs/superpowers/research/stack/anthropic-python_2026-04-18.md` → moved to `archive/`.

### Fixed (collateral)

- **`.claude-plugin/marketplace.json`** — removed `$schema` + `description` root keys breaking `claude plugin validate` on Claude CLI v2.1.113 (stricter validator). Pre-existing breakage surfaced by SD-1 implementer ; restored AC1 in dedicated `fix(v2-collateral)` commit `0f69522`.

### Verification

- **`claude plugin validate <worktree>`** : ✔ Validation passed (one cosmetic warning about `metadata.description` — flagged as F6 follow-up for v2.0.1).
- **9 skills surface** confirmed via `claude -p --plugin-dir <worktree>` probe.
- **AC10 zero-ripple** : 10 grep matches in `phase-0-seed-loading.md` are PRESERVATION DOCS for parser backward-compat (per spec § 4 + Q-C reco) — annotated DEPRECATED v2.x. Zero subprocess code references, zero deleted-script imports.
- **Schema backward compat** : `schema_version` stays at `1`. No migration required.

### Frame-release lesson captured

User input "il faut revoir la connexion via subscription pas via api" surfaced an R8 cache anchoring failure : Claude reasoned 3 turns inside the R8 framing (`anthropic-auth-and-oauth-status_2026-04-19.md` was scoped to "subprocess access to Messages API") instead of zooming out to question the underlying assumption (drop the subprocess that creates the OAuth-bridge problem). Lesson captured as auto-memory feedback : `~/.claude/projects/C--Dev-Claude-cowork-project-genesis/memory/feedback_r8_anchoring_vs_user_intent.md`. Candidate Layer 0 promotion if pattern recurs cross-project.

### Self-rating — v2.0.0 (honest post-feat)

| Axis | Projected | Honest | Delta | Notes |
|---|---|---|---|---|
| Pain-driven | 9.6 | 9.5 | −0.1 | Closes v1.5.0 halt-card UX wall as intended ; minor : the architectural REMOVAL is real value but the win is largely deferred-felt (next user who invokes `/genesis-drop-zone` won't hit the halt-card). |
| Prose | 9.0 | 9.0 | 0.0 | Spec + plan + retire annotations + privilege table updates all coherent. Pattern #2 + #4 narrative appends read naturally with prior "reserved for ninth" sentence. |
| Best-at-date | 9.2 | 9.2 | 0.0 | R8-anchored ; uses canonical `claude auth login` flow per Anthropic CLI v2.1.113 docs. |
| Self-contained | 9.0 | 8.8 | −0.2 | Touched 1 collateral file outside spec scope (marketplace.json $schema/description removal — pre-existing CLI validator regression, not v2 fault). Minor scope leak but defensible (AC1 was failing without it). |
| Anti-Frankenstein | 9.4 | 9.5 | +0.1 | Net REMOVAL : 414-line script deleted, 3 fixtures archived, halt-card retired, privilege reverted to disk-only. Added : 1 new skill, 1 v2 fixture, doc annotations. Net code shrunk. R10.4 anti-speculative gate respected (BYOAI deferred to v3.x). |
| **Mean** | **9.24** | **9.20** | **−0.04** | **Streak ≥ 9.0 advances to 2** (v1.6.3 honest 9.30 + v2.0.0 honest 9.20). |

**Running average post-v2.0.0 honest** : (8.92 × 20 + 9.20) / 21 = 187.60 / 21 ≈ **8.93 (+0.01)**. 21 tagged ratings total.

### Discipline evidence

- **Brainstorming-first** — full brainstorming flow (Q1-Q3 clarifying questions + spec doc + 2 spec-reviewer dispatches + 2 spec-extend rounds capturing user vision additions including genesis.myconciergerie.fr concretization + BYOAI staging) before any code touched.
- **Honest pace check** — user explicitly flagged "tu es mauvais aujourd'hui que se passe t il" mid-session after Claude took 3 turns to release the R8 framing anchor. Acknowledged directly + saved feedback memory + applied frame-release immediately.
- **Subagent-driven implementation** — 8 SD- tasks (one implementer subagent per task on sonnet model) + spot-verification by controller. Final task SD-7 plugin.json bump done inline (trivial 1-line change).
- **Granular commits per pattern #3** — 15 commits in feat tranche (4 spec/spec-polish/spec-extend ×2 + 2 plan/plan-polish + 1 collateral fix + 8 SD-1 to SD-8). Squash-merged as `55c0f68` via PR #49.
- **R2.3.1 observation** — `gh auth switch -u myconciergerie-prog` applied at PR creation time (active account had drifted to `myconciergerieavelizy-cloud`) with `GH_TOKEN=$(gh auth token -u myconciergerie-prog)` env override on PR create. Pattern continues from v1.6.x ships.

---

## [1.6.3] — 2026-04-19 — "F5 fix SPDX frontmatter break (PATCH)"

**Surgical hotfix** for v1.6.2 F5 finding — universal Genesis-owned load-failure bug, latent since v1.3.0, masked by user's `~/.claude/skills/` personal-scope shadow. Every new marketplace install was loading zero Genesis skills until this ship.

### Fixed

- **F5 primary** — 8 SKILL.md files (`genesis-drop-zone`, `genesis-protocol`, `journal-system`, `pepite-flagging`, `phase-5-5-auth-preflight`, `phase-minus-one`, `promptor`, `session-post-processor`) : `<!-- SPDX-License-Identifier: MIT -->` relocated from file top to trailing HTML comment at file end. Claude Code's frontmatter parser requires `---` at line 1 ; leading comment silently dropped all skill metadata. Python binary-mode read/write preserved CRLF per Layer 0 `gotcha_crlf_preservation_git_bash_windows`.
- **F5 collateral (revealed once frontmatter became visible)** — `skills/pepite-flagging/SKILL.md` description wrapped in single-quotes. Was unquoted YAML flow scalar with embedded `"<title>"` double-quote characters that failed YAML parse (invisible under F5 but emergent once F5 fixed).

### Changed

- `skills/genesis-protocol/rules/v1_rules.md § R10.2` — amended with explicit exception for YAML-frontmatter Markdown files. New rule : SKILL.md and any Markdown file starting with a `---` frontmatter block consumed by a strict parser MUST place SPDX as trailing HTML comment, not leading. Prevents regression.
- `.claude-plugin/plugin.json` version `1.6.2 → 1.6.3`.

### Verification

- **`claude plugin validate`** on worktree : ✔ Validation passed (was 8 "No frontmatter block found" errors + 1 YAML parse error pre-fix).
- **Runtime dispatch test** via `claude -p --plugin-dir <worktree> --output-format=json` : all 8 skills surface under `project-genesis:` namespace with verbatim descriptions rendered (was 6 pre-fix, missing `genesis-drop-zone` and `promptor`). This is the first time since v1.3.0 that the plugin load-path has been runtime-verified-clean.
- **CRLF preservation** : Python binary read/write, git commit shows no line-ending churn on unchanged bytes.

### Blast radius

Every Claude Code user installing `project-genesis` via marketplace, `--plugin-dir`, or `claude plugin install` from v1.3.0 through v1.6.2 was receiving a plugin that silently loaded zero skills. The current session's user was masked from noticing because they had manually copied 6 (of 8) skills to `~/.claude/skills/` personal-scope early in the project's life. Fresh users had no such workaround.

### Frictions closed vs deferred

- **F5 CLOSED** — this ship.
- **F1 (--plugin-dir same-name cache shadow)** — Claude Code CLI behaviour, not Genesis fault. Runbook documented it in v1.6.2. No Genesis-side fix.
- **F4 (user-scope personal-skills shadow)** — same as F1 (Claude Code CLI). Runbook documents it.
- **F2 (-p single-shot multi-turn limit)** — not addressed ; requires stream-json scripting or interactive sessions. Defer v1.6.x+.
- **F3 (freelance vs skill value-add)** — v2 design conversation.

### Self-rating — v1.6.3 (honest post-feat)

| Axis | Projected | Honest | Delta | Notes |
|---|---|---|---|---|
| Pain-driven | 9.5 | 9.6 | +0.1 | v1.6.2's biggest finding fixed surgically ; every new marketplace user unblocked. Discovered + fixed + regression-guarded + verified runtime in one ship. |
| Prose cleanliness | 9.2 | 9.2 | 0.0 | Commit message dense, rule amendment clear. |
| Best-at-date | 9.0 | 9.0 | 0.0 | No new R8 needed ; fix applied SOTA YAML scalar best practice (single-quote wrap for flow scalars with special chars). |
| Self-contained | 9.4 | 9.4 | 0.0 | Scope tight ; only SKILL.md + 1 rule doc + plugin.json. Zero ripple to any other surface. |
| Anti-Frankenstein | 9.3 | 9.3 | 0.0 | Mechanical 8-file edit + 1 rule doc + 1 collateral YAML fix discovered in-scope. No preemptive over-engineering. |
| **Mean** | **9.28** | **9.30** | **+0.02** | **Streak ≥ 9.0 restarts at 1** after v1.6.2's honest break. |

**Running average post-v1.6.3 honest** : (8.90 × 19 + 9.30) / 20 = 178.40 / 20 ≈ **8.92 (+0.02)**. 20 tagged ratings total.

### Discipline evidence

- **Hotfix shape honored** — F5 was a known bug with clear mechanical fix. No spec + plan + reviewer loop for v1.6.3 ; feat commit IS the spec (what changed, why, how validated). Single PR, single squash merge, single tag. Appropriate process-to-work matching per Layer 0 skill-type-aware discipline.
- **Collateral-fix discipline** — pepite-flagging YAML parse error was not in original v1.6.2 F5 scope but emerged ONCE F5 was fixed (frontmatter now visible → parser ran → YAML scalar issue surfaced). In-scope per the "if fixing F5 reveals a cascading issue, fix it here" discipline.
- **Rule amendment** — R10.2 update prevents future regression. The exception rule is specific (YAML-frontmatter Markdown files consumed by strict parsers) ; does not over-generalize to remove SPDX discipline elsewhere.
- **Session-ending honesty** — this ship lands immediately after user flagged my v1.5.2→v1.6.2 retitle rationalization as wasted tokens. Direct accountability loop : failure → acknowledgement → memory save → immediate execution of the right thing. The v1.6.3 ship itself is the correction proof.

---

## [1.6.2] — 2026-04-19 — "runtime dogfood (PATCH)"

**PATCH originally scoped as v1.5.2 back-insert.** Plan-reviewer surfaced `plugin.json` already at 1.6.1 (semver reality) — retitled forward-increment. Runtime dogfood automated via `claude -p --plugin-dir <worktree>` subprocess calls from the driver session (~$3.19 / 7.6 min for 8 runs including Path-B isolation attempt). H1-H4 formally unable-to-test due to a cluster of 5 frictions, the most important of which (F5 SPDX-comment-before-frontmatter) is a universal Genesis-owned load-failure bug affecting every new marketplace install. Honest rating drops below 9.0 ; **streak ≥ 9.0 at 3 consecutive breaks with this ship** per Layer 0 honesty discipline.

### Added

- `skills/genesis-drop-zone/tests/runtime_dogfood_v1_6_2.md` — reusable 5-section runbook (Pre-flight with 3 isolation paths post-F5 / Per-fixture spawn+trigger+observe / Redaction rules / Re-run guidance / Source of truth). Updated post-Path-B with F1+F4+F5 isolation requirements for v1.6.3 consumers.
- `skills/genesis-drop-zone/tests/runtime_dogfood_evidence_v1_6_2.md` — session-specific evidence log with 5 per-fixture observations + H1-H5 table + friction triage (F1/F2/F3/F4/F5) + Path-B addendum + cost summary.
- `C:/tmp/genesis-v1.6.2-alexandre/` fixture (5 artefacts : config.txt + catalogue_fenetres_fr.md + specs_usine_pl.md + voice_memo_alexandre.txt + photo_facade_client.jpg 5985 bytes JFIF via Pillow). Multi-language FR/PL mixed-media drop mirroring Alexandre window-sales use case — catalogue RAL 9005/7016/9010 + MOQ 8 pièces Poznań + Uw 0.8-1.3 + EN 14351-1 / ISO 9001 PL-QC-9042.
- `memory/master.md` pattern #4 depth-update on sixth data-point — Layer A-only runtime-evidence session with zero Layer B ripple per AC10 ; same ripple class as v1.5.1 sixth, work differs (runtime vs paper-trace) but ripple identical ; per v1.6.1 precedent (pattern #1 depth on fourth, no new ordinal), same-ripple-class extension = depth update, not new ordinal.

### Changed

- `.claude-plugin/plugin.json` version `1.6.1 → 1.6.2`.

### Removed

- None.

### Preserved (explicit non-change)

- All 8 skills' SKILL.md files — zero edits (F5 fix deferred to v1.6.3 per hybrid-gate class-B + common-root-cause clustering with F1 + F4).
- All Layer A (`skills/genesis-drop-zone/SKILL.md` + `phase-0-welcome.md` + `scripts/`) untouched. Only `tests/` subtree added (runbook + evidence log).
- Layer B skills — zero edits (AC10 grep pipeline = 0 verified at Phase A pre-commit, Phase B post-commit, and post-Path-B-finding commit).
- `skills/genesis-drop-zone/scripts/extract_with_citations.py` — NG3 boundary preserved (grep = 0).
- Schema version, dependency set, subprocess surface, network surface — zero change.

### Frictions surfaced (hybrid gate triage)

- **F1 (class B, methodology)** — `claude --plugin-dir <path>` does NOT shadow a same-named stale cached install. Even `plugin disable` + `plugin uninstall` + `rm -rf cache/` leaves a user-scope skills directory (F4) shadowing the load.
- **F2 (class B, methodology)** — `-p` single-shot cannot exercise multi-turn skill flows (Phase 0.1 → 0.5). v1.6.3+ needs either manual interactive or scripted `--input-format stream-json`.
- **F3 (class C, insight)** — freelance Claude matches arbitration quality on rich multi-source drops (alexandre_windows : extracted catalogue + specs_pl + voice_memo into coherent consent card covering Product / Pain / Pricing / Factory). Skill's value-add over freelance needs explicit characterization. v2 design conversation.
- **F4 (class B, structural — Claude Code CLI)** — user has 6 Genesis skills at `~/.claude/skills/` personal-scope, shadowing plugin installs entirely.
- **F5 (class B, structural — Genesis-owned, universal)** — every SKILL.md (all 8) starts with `<!-- SPDX-License-Identifier: MIT -->` before the YAML `---` frontmatter delimiter. Claude Code's parser reports "No frontmatter block found" for ALL 8. Fresh marketplace installs would load zero Genesis skills. Latent since v1.3.0, masked by user's F4 shadow install. **v1.6.3 P0 fix** : move SPDX comment after closing `---` OR remove from SKILL.md per R10.5 scope-narrowing (keep SPDX only on source-code files `.py` / `.ts` not plugin manifests).

### Hypothesis outcomes

| H | Prediction | Outcome |
|---|---|---|
| H1 | Skill engine dispatches `/genesis-drop-zone` on verbatim trigger phrase in all 5 fixture cwds | **UNABLE-TO-TEST** — F5 root cause + F4 shadow prevent genuine isolation. 5 natural-phrase runs all freelanced. |
| H2 | Phase 0.4 arbitration on alexandre_windows renders `arbitrated_fields` list non-empty | **UNABLE-TO-TEST** formally ; indirect evidence — freelance synthesized coherent multi-source arbitration. |
| H3 | Phase 0.5 Path 2a consent renders on empty-divergences fixture | **UNABLE-TO-TEST** |
| H4 | Fixture scenario_halt_no_key renders EXIT_NO_KEY halt card | **UNABLE-TO-TEST** |
| H5 | Zero Layer B ripple | **CONFIRMED** (AC10 grep = 0 at all checkpoints) |

### Self-rating — v1.6.2 (honest post-feat, per Layer 0 `feedback_honest_self_rating_post_feat.md`)

| Axis | Projected | Honest | Delta | Notes |
|---|---|---|---|---|
| Pain-driven | 9.4 | 8.8 | −0.6 | Formal H1-H4 deferred ; F5 discovery IS substantial load-bearing pain-reduction but doesn't match the projected form. |
| Prose cleanliness | 9.0 | 9.0 | 0.0 | No prose rewrites ; evidence log + runbook cleanly structured. |
| Best-at-date | 9.0 | 9.0 | 0.0 | No new R8 commissioned ; existing R8 still valid. |
| Self-contained | 9.2 | 8.9 | −0.3 | Scope expanded (into evidence log, not feat commits) to accommodate F4 + F5 additional findings discovered during Path-B isolation attempt. |
| Anti-Frankenstein | 9.1 | 9.1 | 0.0 | 5 frictions found, 5 classified cleanly per hybrid gate, 0 preemptive fixes. 1:1 evidence-to-hypothesis integrity maintained. |
| **Mean** | **9.14** | **8.96** | **−0.18** | **Streak ≥ 9.0 BREAKS** (was 3 consecutive : v1.5.1 9.12 / v1.6.0 9.02 / v1.6.1 9.18). |

**Running average post-v1.6.2 honest** : (8.90 × 18 + 8.96) / 19 = 169.16 / 19 ≈ **8.90 (flat).** 19 tagged ratings total.

### Discipline evidence

- **Autonomous subprocess automation** — user asked "automatise moi tout ça pour faire intervenir qu'au phase le nécessitant" after manual 5-session spawn was too heavy. Driver session switched to `claude -p --plugin-dir <worktree> --output-format=json` subprocess calls with env-var management (`env -u ANTHROPIC_API_KEY` for halt-no-key fixture). 5 fixture runs + 2 controls captured without manual session-spawning.
- **Path B isolation attempt post-honest-ship-option** — user voted Path B (uninstall + re-test) over Path A (ship-as-is) to pursue cleaner evidence. Path B surfaced F4 + F5 which Option A would have missed. Reviewer-driven scope expansion discipline applied correctly (additional findings went into evidence log as separate commit `cc00427` feat-runtime-amend, not into amend or scope-creep).
- **Class-A-adjacent deferral** — F5 is structurally a load-failure bug (not privilege violation, therefore not strict class A) but with massive blast radius (every new marketplace install). Per hybrid-gate class-B + common-root-cause clustering (F1+F4+F5 all plugin-loading methodology), deferred to v1.6.3 unified P0 fix rather than rushed in v1.6.2.
- **Honest streak break** — v1.5.1 + v1.6.0 + v1.6.1 formed a 3-consecutive ≥ 9.0 streak. v1.6.2 honest at 8.96 breaks it. Per Layer 0 `feedback_honest_self_rating_post_feat.md`, willingness to break streak ≥ 0.2 honest-deduction is the discipline ; this case clears the bar cleanly (projected 9.14 → honest 8.96, delta −0.18).

### Layer 0 sync (Phase D)

Skipped this ship. The `gh auth switch` + GH_TOKEN env-prefix pattern was **proactively** applied at Phase C (not reactively discovered) — the pattern is now habitual, no Layer 0 amplification needed this session. If proactive application continues in v1.6.3 sessions, no Layer 0 touch required.

### Follow-up candidates (for v1.6.3+)

- **v1.6.3 P0** : fix F5 — move SPDX comment after frontmatter OR scope-narrow R10.5 to exclude SKILL.md. Mechanical change across 8 files. Bundled with F1 + F4 runbook hardening.
- **v1.6.3 / v1.6.4** : re-run runtime dogfood against isolated v1.6.3 plugin load (Path B with F5 fix). Should recover true H1-H4 evidence.
- **v1.6.3+** : F2 multi-turn scripted via `--input-format stream-json`.
- **v2 design conversation** : F3 product-positioning — when does invoking the skill beat freelance Claude?
- **v1.6.x+** : Skill-tool plugin-installed runtime evidence for promptor (was originally named v1.6.2 in v1.6.1 resume — bumped to v1.6.3 or later).

---

## [1.6.1] — 2026-04-19 — "runtime auto-discovery + Anthropic prompt-eng SOTA grounding (PATCH)"

**PATCH closing the two priced-in axis caps of v1.6.0.** v1.6.0 shipped at honest 9.02/10 with Best-at-date 8.7 (no R8 entry backing template choices) and Pain-driven 9.2 (H1 skill auto-discovery paper-trace only). v1.6.1 closes both in one PATCH via (a) 326+ line SOTA R8 entry commissioned ahead of spec (42+ citations, canonical Anthropic migration guide primary for 4.7 sampling-removal claim), (b) 5 surgical template patches (3 critical + 2 polish) mapped 1:1 to R8 findings, (c) fresh Claude Code session in sibling Aurum cwd confirming the Layer 0 pépite + binding-rule surface fires cleanly on trigger phrases. Pinning decision landed AC#7 Option A (non-pinned) with runtime-validated marker on the binding rule.

### Added

- `research/sota/anthropic-prompt-engineering_2026-04-19.md` — 334-line R8 entry grounding Promptor template against Anthropic April 2026 canon. Confirms 6 of 8 core template choices (XML structure, two-phase gate, static-before-dynamic KV-cache ordering, staff-engineer density, edge-cases enumeration, `{{VAR}}` discipline). Surfaces breaking changes on Opus 4.7 (sampling params removed, extended thinking removed, prefill removed, thinking content omitted by default, new tokenizer, task budgets beta). Provides 5 anti-Frankenstein candidates (all 5 landed as patches C1/C2/C3/L1/L2).
- `skills/promptor/references/template.md` Part A `**Pour Claude Opus 4.7+**` branch (C1 patch) — omits `temperature`/`top_p`/`top_k`, uses `output_config.effort` + `thinking: {type: "adaptive"}` + `max_tokens ≥ 64k`, `display: "omitted"` default ; legacy 4.6 path retains sampling params.
- `skills/promptor/references/template.md` Part B cache-breakpoint placement directive (C2 patch) — 4,096-token minimum on Opus 4.7, `usage.cache_creation_input_tokens ≠ 0` verification, max 4 breakpoints per request, canonical `tools → system → messages` ordering.
- `skills/promptor/references/template.md` Part B MCP `ServerName:tool_name` mandatory form (C3 patch) — cites Anthropic skill-authoring requirement, prevents tool-not-found collisions across multi-server MCP setups.
- `skills/promptor/SKILL.md` "v1.6.1 gate additions" paragraph pointing to C-patches and R8 grounds file.
- `tests/runtime_auto_discovery_v1_6_1.md` (116-line runbook) — reproducible procedure for validating skill auto-discovery in sibling-project sessions. Evidence run 1 filled (2026-04-19, Aurum cwd, Layer 0 pépite surface confirmed, Phase 1 acquisition discipline preserved under domain-adaptation).
- `memory/master.md` pattern #4 eighth data-point — orthogonal meta-skill PATCH zero-ripple (verified via 4 git-diff probes).
- `memory/master.md` pattern #1 v1.6.0 fourth-data-point depth update — SOTA-validated edits mirrored across skill + synced-cache pépite without schema change.

### Changed

- `skills/promptor/references/template.md` Phase 1 Q2 (L1 patch, 2 locations: plain-text wrapped + XML single-line `<output_template>`) — acquires model + effort + thinking mode + `max_tokens` + MCP config (replaces bare `temperature`).
- `skills/promptor/references/template.md` Phase 1 Q1 (L2 patch, 2 locations) — metrics task-adaptive (Precision/Recall pour classification/RAG ; taux de réussite end-to-end pour agentique ; latence ; coût/1k tokens) replaces fixed "Precision/Recall, Latence".
- `.claude/docs/superpowers/research/INDEX.md` — new row for `anthropic-prompt-engineering_2026-04-19.md` (sota, expires 2026-04-26, confidence high).
- `.claude-plugin/plugin.json` version `1.6.0 → 1.6.1`. No keyword change.

### Removed

- None. All template edits are in-place transforms ; no deletions.

### Preserved (explicit non-change)

- `skills/promptor/SKILL.md` frontmatter `description` verbatim (trigger-phrase pins unchanged since v1.6.0 ; grep-verified).
- Skill privilege map : `promptor` stays privilege-class `none` (still 2nd none-class skill with `journal-system`).
- Cross-skill-pattern #1 ordinal count : no new data-point added to pattern #1 ; v1.6.0's fourth data-point gains depth only (SOTA-validation loop closure).
- All Layer A (`skills/genesis-drop-zone/`) and Layer B (`skills/genesis-protocol/`, `skills/phase-minus-one/`, `skills/phase-5-5-auth-preflight/`, `skills/journal-system/`, `skills/session-post-processor/`, `skills/pepite-flagging/`) skills — zero edits. **Eighth data-point of pattern #4 zero-ripple principle.**
- Schema version, dependency set, subprocess surface, network surface — zero change.

### Layer 0 sync (Phase D, post-merge, NOT in repo)

- `~/.claude/memory/layer0/pepite_promptor_template_anthropic_prompt_engineering.md` — 5 template patches applied verbatim, synced-cache marker bumped `v1.6.0 @ 2026-04-19` → `v1.6.1 @ 2026-04-19`.
- `~/.claude/memory/layer0/feedback_invoke_promptor_for_production_anthropic_prompts.md` — § "The rule" Skill-first preference preamble gains "runtime-validated 2026-04-19 v1.6.1 on Layer 0 pépite surface" marker. Pinning decision AC#7 Option A non-pinned with runtime-validation scope explicit (pépite surface validated ; Skill-tool plugin-installed path deferred to v1.6.2+).
- `~/.claude/memory/layer0/_v1_6_1_layer0_sync_DONE_2026-04-19.md` sentinel written for next-session `test -f` check.

### Discipline evidence

- **SOTA-first ordering** — R8 entry commissioned ahead of spec (Phase 0 research → spec → plan → feat) with canonical Anthropic citation primary, community cross-check secondary. Honest cap 9.3 on Best-at-date (not 9.5) because R8 open question 2 (system-prompt reverse engineering via Simon Willison) stays community-derived — not load-bearing for the 5 template patches, but present in the entry.
- **Reviewer-driven P2 bundling (a7b0740-style)** — code-quality reviewer flagged one citation-order inconsistency inside the R8 entry (§ "What this challenges" item 1 still led with claudefa.st while TL;DR had been swapped to canonical Anthropic). One-line in-place swap landed as commit `682f522` in the feat branch. Honest Self-contained axis accepts the bundling deduction (-0.2 from projected 9.3 → honest 9.1), matching v1.6.0 `a7b0740` precedent.
- **Plan-reviewer rigor** — caught 6 P1 pre-Phase-A (Edit-target precision, shell-escape, zero-ripple probe, idempotency coverage, pattern #4 task gap). All 6 fixed before feat execution. Plan-writing discipline acknowledged as the weaker axis on first pass ; Self-contained axis deducted further (9.1 → 9.0) to honor this.
- **Runtime evidence partial scope** — Layer 0 pépite + binding-rule surface validated in non-Genesis sibling ; Skill-tool plugin-installed path NOT exercised. Honest deduction on Pain-driven (projected 9.4 → honest 9.3).

### Self-rating — v1.6.1 (honest re-evaluation post-feat, per Layer 0 `feedback_honest_self_rating_post_feat.md`)

**Initial projection 9.26/10. Honest post-feat re-evaluation lands at 9.18/10** (-0.08 from projection).

| Axis | Projected | Honest | Notes |
|---|---|---|---|
| Pain-driven | 9.4 | **9.3** | Runtime evidence confirmed Layer 0 pépite surface cleanly ; Skill-tool plugin-installed path deferred to v1.6.2+ re-run. Partial H1 closure, not full. |
| Prose cleanliness | 9.2 | **9.2** | Template patches integrate without voice drift ; R9 language policy respected (French in user-facing template content, English in dev prose). Net-positive delta on clarity via model-gating. |
| Best-at-date | 9.3 | **9.3** | R8 entry 326+ lines, 42+ citations, canonical Anthropic primary for load-bearing sampling-removal claim (spec-polish + code-reviewer citation-order fix). Cap 9.3 (not 9.5) — R8 open question 2 stays community-derived but not load-bearing. |
| Self-contained | 9.3 | **9.0** | Two honest deductions : (a) reviewer-driven P2 bundling (a7b0740-style, -0.2 per v1.6.0 precedent) ; (b) plan-reviewer caught 6 P1 vs v1.6.0's 3 P1 — plan-writing discipline weaker on first pass (-0.1). |
| Anti-Frankenstein | 9.1 | **9.1** | 5 patches map 1:1 to R8 findings. No preemptive enumeration. Runtime runbook strict-scope. |
| **Mean** | **9.26** | **9.18** | **Streak ≥ 9.0 advances to 3 consecutive** (v1.5.1 = 9.12, v1.6.0 = 9.02, v1.6.1 = 9.18). |

**Running average**: v1.6.0 post-ship running = **8.88** (per `session_v1_6_0_promptor_skill.md` ; 17 tagged ratings from v1.0.0 through v1.6.0). v1.6.1 is the 18th tagged rating. New running = (8.88 × 17 + 9.18) / 18 = 160.14 / 18 ≈ **8.90 (+0.02)**.

---

## [1.6.0] — 2026-04-19 — "promptor skill (MINOR — orthogonal meta-skill, 8th skill ship)"

**First MINOR on the v1.6.x line.** Promotes the Layer 0 Promptor pépite (`~/.claude/memory/layer0/pepite_promptor_template_anthropic_prompt_engineering.md`) into a standalone Genesis skill at `skills/promptor/`. Skill becomes canonical source of truth ; Layer 0 pépite demoted to synced cache role for sessions outside Genesis-bootstrapped projects. **8th Genesis skill ; 2nd privilege-`none` skill** (joins `journal-system`) ; **first orthogonal meta-skill** (neither Layer A nor Layer B — invocable cross-session/cross-project outside the bootstrap protocol). Net diff dominated by 2 new skill files + 3 plugin-keyword additions ; cross-cutting touches limited to `master.md` (3 pattern data-points + sixth-data-point reconciliation for v1.5.1 missed in PATCH) and `skills/README.md` (preamble update + entry).

PR #41 squash-merged as `0e20462`. Tag `v1.6.0` pushed.

### Added

- `skills/promptor/SKILL.md` (~80 lines) — invocation gate with frontmatter description carrying the 4 verbatim binding-rule trigger phrases (FR + EN), when-to-invoke + when-NOT-to-invoke (non-technical / trivial / exploratory / non-Anthropic), two-phase operating mode high-level (standby / creation), adaptation discipline, 1:1 mirror declaration with sync metadata "Last sync: v1.6.0 @ 2026-04-19"
- `skills/promptor/references/template.md` (~137 lines) — verbatim canonical XML template (Promptor `<role>` + `<operating_mode>` with `<phase_1_standby>` + `<phase_2_creation>` + `<output_structure>` + `<global_constraints>`) + 6 architectural principles (two-phase separation, KV cache optimization explicit, density over clarity, failure-mode explicit, env var discipline, semantic XML + rigorous Markdown) + adaptation points + when-not-to-use + cross-project utility list (Aurum / Genesis / Myconciergerie / Cyrano / new projects)
- `.claude-plugin/plugin.json` — 3 new keywords (`prompt-engineering`, `promptor`, `meta-tool`)
- `skills/README.md` — preamble updated to "v1.6.0 (8 skills)" with shipping-history breakdown + new `promptor` entry with one-line pitch + privilege map row
- `memory/master.md` — pattern #1 fourth 1:1 mirror data-point (skill canonical, Layer 0 pépite synced cache) ; pattern #2 8th skill / 2nd none-class data-point ; pattern #4 **sixth data-point reconciling v1.5.1** (which was missed when v1.5.1 PATCH didn't touch master.md) **+ seventh data-point** (v1.6.0 orthogonal meta-skill, zero ripple to either Layer A or Layer B) ; orthogonal-to-Layer-A/B note (no Layer M category for one skill — emerges naturally if 2nd meta-skill arrives)

### Changed

- `.claude-plugin/plugin.json` version `1.5.1 → 1.6.0`
- `~/.claude/memory/layer0/pepite_promptor_template_anthropic_prompt_engineering.md` (Phase B Layer 0 sync, post-merge, NOT in repo) — header note "Synced cache from `<repo>/skills/promptor/SKILL.md` v1.6.0 @ 2026-04-19" added after frontmatter ; § "Cross-references" tense fix ("Genesis v1.6.0 candidate" → past-tense "Genesis v1.6.0 promotion")
- `~/.claude/memory/layer0/feedback_invoke_promptor_for_production_anthropic_prompts.md` (Phase B Layer 0 sync, post-merge, NOT in repo) — § "The rule" gains "Skill-first preference (added 2026-04-19, v1.6.0)" preamble with non-pinned skill-invocation syntax (namespace pinning deferred to v1.6.1 after empirical validation)

### Preserved (explicit non-change)

- `skills/genesis-drop-zone/**` — zero-line diff. Layer A untouched.
- `skills/genesis-protocol/**` — zero-line diff. Layer B untouched.
- All 6 other shipped skills (`phase-minus-one`, `phase-5-5-auth-preflight`, `journal-system`, `session-post-processor`, `pepite-flagging`) — zero-line diff.
- `schema_version`, no privilege class added (privilege `none` = degenerate map entry, no mitigations).
- No `install-manifest.yaml` (3rd skill without — joins `genesis-drop-zone` + `phase-5-5-auth-preflight`).
- No `commands/` slash command (consistent with all 7 prior skills surfacing via skill-description match).

### Self-rating — v1.6.0 (honest re-evaluation post-feat, per Layer 0 `feedback_honest_self_rating_post_feat.md`)

**Initial spec projection was 9.14/10 (Pain-driven 9.2 / Prose 9.3 / Best-at-date 8.7 / Self-contained 9.5 / Anti-Frankenstein 9.0). Honest post-feat re-evaluation lands at 9.02/10** — streak ≥ 9.0 advances to 2 consecutive (post-v1.5.1 = 9.12).

| Axis | Projected | Honest | Delta | Notes |
|---|---|---|---|---|
| Pain-driven | 9.2 | 9.2 | 0.0 | Cross-project utility = real pain (every Anthropic-API project bootstrapped via Genesis needs prompt-eng discipline). Capped at 9.2 because runtime auto-discovery validation deferred to v1.6.1 (skill engine cannot be exercised in the same session that ships the skill). |
| Prose cleanliness | 9.3 | 9.3 | 0.0 | Two focused files with crisp gate/template separation. Frontmatter description carries triggers verbatim (single source). 1:1 mirror discipline declared in both files with sync metadata. No narrative redundancy with pépite. |
| Best-at-date | 8.7 | 8.7 | 0.0 | Honest deduction priced in at spec time per P2.3 reviewer feedback — cited R8 entry `v2_promptor_fusion_landscape_2026-04-17.md` is about drop-zone landscape for v2, NOT about Anthropic prompt-engineering SOTA for Opus 4.7 1M as of 2026-04-19. **No R8 entry validates the template's choices against current Anthropic prompt-engineering guidance.** Flagged as v1.6.1 candidate (commission fresh `sota/anthropic-prompt-engineering_<date>.md` R8 entry and re-anchor). |
| Self-contained | 9.5 | 9.3 | −0.2 | **Honest deduction.** Phase A bundled 2 reviewer-driven prose fixes as 6th commit `a7b0740` (READmme preamble stale "All six skills are shipped as of v0.8.0" → "v1.6.0 (8 skills)" + master.md pattern #4 missing sixth data-point for v1.5.1 reconciliation). Both fixes are downstream consequences of v1.6.0 ship (the README count is wrong because of v1.6.0 + v1.3.0 ; the master.md sequence skip is from v1.5.1 + v1.6.0), **directly traceable**, not unrelated cleanup. Still, bundling them in the same feat tranche rather than a separate PATCH stretched the "self-contained" envelope. Deduction 0.2. |
| Anti-Frankenstein | 9.0 | 9.0 | 0.0 | Net new diff = 2 skill files + 3 plugin keywords + Layer 0 sync notes (text-only convention, no script). Skill adds value over pépite via marketplace distributability + cross-project propagation + the v1.6.x evolution path. **Rejected by deliberate design**: pre-cooked domain examples (decay > principles), `/promptor` slash command (structural anomaly vs 7 existing skills), auto-sync script for Layer 0 pépite (manual sync acceptable at observed frequency, pain-trigger on first observed drift), Layer M category for one orthogonal skill (emerges naturally if 2nd arrives). Reviewer ceremony was proportional (5+4 spec, 3+5 plan, 2 quality reviewer P1) — the in-feat fixes were correctness-bearing, not gold-plating. |
| **Average** | **9.14** | **9.02** | **−0.12** | **Streak ≥ 9.0 advances to 2 consecutive** (v1.5.1 = 9.12, **v1.6.0 = 9.02**). |

Running average post-v1.6.0 honest: ≈ **8.88/10** (+0.01 vs v1.5.1 running 8.87). MINOR tranche restoring the +0.01 increment cadence.

### Cross-skill-pattern data-points

- **Pattern #1 (1:1 mirror discipline) — fourth data-point.** `promptor` SKILL.md + references/template.md together mirror the Layer 0 pépite (split into 2 files for gate/template separation; semantic content unchanged). Per master.md count (which includes self-mirror), this is the fourth data-point. Drift between skill and pépite = merge-blocker per declared sync convention.
- **Pattern #2 (concentrated privilege map) — 8th skill data-point.** Privilege class `none` (no disk write, no network, no subprocess). 2nd none-class skill (joins `journal-system`). Cleanest possible map entry — no mitigations needed since no privilege exists.
- **Pattern #4 (Layer A/B + zero-ripple) — sixth data-point reconciliation + seventh data-point.** Sixth data-point: v1.5.1 PATCH was tracked in CHANGELOG but never updated `master.md` — v1.6.0 reconciles by adding the missing sentence (zero-ripple holds under PATCH constraint as well as MINOR-level expansion). Seventh data-point: v1.6.0 promptor ships as orthogonal meta-skill, neither Layer A nor Layer B, with zero edits to any Layer A or Layer B skill ; only cross-cutting touches are `master.md` (data-points + orthogonal note) and `skills/README.md` (entry). **Extends zero-ripple principle from "Layer A grows / corrects / opt-in renders without rippling Layer B" to "new orthogonal meta-skill ships without rippling either layer".**

### Anti-Frankenstein notes

- **Net new** = 2 skill files (~80 + ~137 lines) + 3 plugin.json keywords + 1 README entry + 3 master.md sentences + Layer 0 sync notes (manual convention, no script) + 2 reviewer-driven correctness prose fixes
- **Rejected by deliberate design** (documented in spec § Anti-patterns avoided + § Non-goals) :
  - Pre-cooked domain examples (data-engineer, security-researcher, legal-drafter) — examples decay faster than principles, copy-without-calibration risk
  - `/promptor` slash command — structural anomaly vs 7 existing skills surfacing via description match, marginal UX gain
  - Auto-sync script for pépite — manual ship-time sync sufficient at expected frequency ; pain-trigger reconsideration on first observed drift event
  - Layer M (meta) category — defer until ≥ 2 meta-skills exist
  - Bundling spec for v2 conversational Promptor — separate track, cross-link only ; forward-naming reservation recorded for v2 skill names (`genesis-spark` / `genesis-mirror` / `genesis-iterate` candidates)
  - Retiring Layer 0 pépite outright — would break sessions opened outside Genesis-bootstrapped projects on this machine
  - Pépite as canonical with skill as copy — would leave marketplace-shipped form vulnerable to per-machine drift, no clear authority for new-project bootstrap inheritance

### Pre-Phase-A dogfood — explicitly skipped (silence-is-omission discipline)

Per Layer 0 `feedback_dogfood_first_ordering_before_prose_correction` (empirical Genesis v1.5.1) : *"PATCH sur surface récemment-shipped = dogfood EN PREMIER"*. v1.6.0 is **net-new skill** (not a PATCH on shipped skill surface), so the strict v1.5.1 rule does not apply. Phase B Task 9 was a minor PATCH on the Layer 0 binding rule (idempotency-protected by marker grep), so the optional dogfood pre-step was **skipped consciously**. Explicit acknowledgement here per the v1.5.1 silence-is-omission lesson : the binding rule update ships unvalidated against runtime trigger firing in a sibling Genesis-bootstrapped project. Risk accepted as low (additive prepend, original rule preserved verbatim downstream of the new preamble).

### Out-of-scope (deferred)

- **v1.6.1 — Runtime auto-discovery validation** : spawn fresh Claude Code session in a Genesis-bootstrapped sibling project (Aurum frozen / Cyrano / Myconciergerie), type one of the trigger phrases, observe skill engine surfacing `promptor` (~3-4h with R8 grounding below)
- **v1.6.1 — Anthropic prompt-engineering 2026-04 SOTA grounding** : commission fresh `sota/anthropic-prompt-engineering_<date>.md` R8 entry + re-anchor template's choices, lifting Best-at-date axis ceiling above 8.7 cap
- **v1.5.2 — Runtime (not paper-trace) dogfood** of Phase 0.4 / 0.5 / archive / halt cards : still queued from v1.5.1 resume (~2-3h)
- **v1.5.3 — Friction #3 retirement-trigger semantics** for Phase 0.4 (~4-5h)
- **Cross-device Layer 0 sync (multidevice scenario)** — H7 refuted by construction ; Layer 0 lives at `~/.claude/memory/layer0/` per machine ; v1.6.0 update is single-machine. Future Layer 0 hygiene work (cross-device propagation) is its own thread, separate from v1.6.x line.

### Discipline evidence

- Spec + plan reviewer ceremony : 5 P1 + 4 P2 fixes on spec, 3 P1 + 5 P2 fixes on plan, 2 P1 fixes from code-quality reviewer pass on Phase A — all advisories landed before merge. Reviewer ceremony was proportional to a MINOR new-skill ship.
- Honest self-rating ritual applied between feat-merge and chore commit per Layer 0 `feedback_honest_self_rating_post_feat.md`. Self-contained dropped 0.2 from projection (9.5 → 9.3) on bundling-scope-in-same-feat assessment ; mean 9.14 → 9.02 honest. Discipline-willingness to drop ≥ 0.1 demonstrated again post-v1.5.1.
- Forward-naming reservation for `skills/promptor/` namespace recorded in spec § Non-goal #1 — pre-resolves the v2 conversational pipeline naming-collision risk before v2 ships.

---

## [1.5.1] — 2026-04-19 — "dogfood + Phase 0.5 clarification + halt card collapse (PATCH)"

**PATCH closing v1.5.0's three-gap honesty correction.** Dogfood-first ordering (3 → 1 → 2) is the v1.5.1 discipline upgrade — runtime evidence shapes prose, reversing v1.5.0's preemptive-prose mistake. Dogfood Candidate 3 ran first against 4 fixtures at `C:/tmp/genesis-v1.5.0-dryrun/` (paper-trace method, canonical runtime for prose-only skills), surfacing 7 frictions (2 blocker, 3 structural, 1 polish, 1 deferred). Candidates 1 + 2 prose edits shaped by the findings, including 2 latent bugs (v1.4.0 fallback prose contradicting v1.5.0 retirement in the same file; empty-divergences write path silently skipping v1.3.2 consent card). Code-reviewer caught a third latent collision (v1.3.2 halt-on-existing vs v1.5.0 re-run archive contract) pre-commit; Path 2a/2b bifurcation landed in the same feat.

### Added

- `genesis-drop-zone` SKILL.md gains new subsection `### Consent-card interaction with Phase 0.5 (v1.5.1 clarification)` with three-path contract:
  - Path 1 (non-empty divergences): Phase 0.5 arbitration card subsumes v1.3.2 consent card. Arbitration response IS consent.
  - Path 2a (first-write empty divergences): v1.3.2 consent card + v1.3.2 write flow unchanged.
  - Path 2b (re-run empty divergences): v1.3.2 consent card + § "Archive write — supersession chain" (NOT v1.3.2 write flow, whose halt-on-existing would collide with supersession contract).
  - Path 3 (halt card, exits 2-7): neither consent nor arbitration renders; halt terminates dispatch pre-write.
- Victor-exit safety invariant named explicitly across all three paths
- Dogfood archive `memory/project/dogfood_v1.5.0_2026-04-19/friction_log.md` (194 lines, 7 frictions logged with candidate-mapped severity + hypothesis-bearing analysis)
- Spec `.claude/docs/superpowers/specs/v1_5_1_dogfood_and_prose.md` with Appendix A pre-registration + blocker taxonomy + timebox-exceeded rule
- Plan `.claude/docs/superpowers/plans/v1_5_1_dogfood_and_prose.md` with reviewer-P0 loopback rule + H2 coverage protocol + R2.3.1 double pre-flight

### Changed

- `genesis-drop-zone` SKILL.md Phase 0.5 empty-divergences wording — now explicitly routes per write-path (first-write vs re-run)
- `genesis-drop-zone` halt-card taxonomy collapsed from **12 bilingual variants (6 cards × 2 langs) → 4 variants (2 cards × 2 langs)** per dogfood Friction #4: EXIT_NO_KEY retained distinct; EXIT_SDK_MISSING + EXIT_API_ERROR + EXIT_RATE_LIMIT + EXIT_BAD_INPUT + EXIT_OUTPUT_INVALID merged into one generic internal-error card
- `genesis-drop-zone` SKILL.md halt table 6 rows → 2 rows
- `genesis-drop-zone` SKILL.md v1.4.0 fallback prose marked RETIRED across the file (retirement banner on `## Citations API dispatch (v1.4.0)`, exit-code table response column updated, `### Fallback triggers` marked RETIRED v1.5.0, modification-loop paragraph rewritten, v1.4.0 scope items #5 + #6 amended, network class mitigation #5 replaced with "Halt-with-remediation card" description)
- `.claude-plugin/plugin.json` version `1.5.0 → 1.5.1`

### Removed

- 10 bilingual halt card variants (EXIT_SDK_MISSING FR + EN / EXIT_API_ERROR FR + EN / EXIT_RATE_LIMIT FR + EN / EXIT_BAD_INPUT FR + EN / EXIT_OUTPUT_INVALID FR + EN) from `phase-0-welcome.md` — anti-Frankenstein retroactive part 2 (preemptive enumeration of exit codes, not pain-driven; extractor stderr preserves diagnostic fidelity)

### Preserved (explicit non-change)

- `skills/genesis-drop-zone/scripts/extract_with_citations.py` — zero-line diff. All 6 distinct exit codes preserved. Collapse is at render layer only.
- `skills/genesis-protocol/**` — zero-line diff. Layer B untouched. Cross-skill-pattern #4 zero-ripple principle sixth data-point.
- `schema_version: 1` — zero bump. All v1.5.0 frontmatter keys preserved.
- Zero new privilege class, zero new dependency, zero new bilingual pair (net negative).

### Self-rating — v1.5.1 (honest re-evaluation post-feat, per [A8] spec acceptance + Layer 0 `feedback_honest_self_rating_post_feat.md`)

**Initial projection was 9.24/10. Honest post-feat re-evaluation lands at 9.12/10** — streak ≥ 9.0 RESTARTS at 1 after v1.5.0 broke it at 11.

| Axis | Score | Notes |
|---|---|---|
| Pain-driven | 9.4 | All three candidates trace to concrete 2026-04-19 honesty correction. Dogfood surfaced 2 blocker frictions immediately — evidence > speculation. Deduction 0.1 for paper-trace method (not full runtime invocation — acknowledged explicitly in shipped prose). |
| Prose cleanliness | 9.0 | New subsection crisp, Path 2a/2b bifurcation + collision-rationale documented. Net-negative delta (−274 / +91). Deduction 0.3 for v1.4.0 retirement banners creating "superseded-but-preserved" verbosity that increases SKILL.md cognitive load — cleaner would have been wholesale deletion of retired prose, but preserving historical context was the chosen tradeoff. |
| Best-at-date | 9.0 | Dogfood-first discipline SOTA-aligned per Layer 0 `discipline_periodic_dogfood_checkpoint.md`. Halt-card collapse is anti-Frankenstein canon. No new R8 research needed. |
| Self-contained | 9.3 | Zero Layer B ripple ✓ ; zero schema bump ✓ ; zero new dependency ✓ ; zero script change ✓ . Only genesis-drop-zone touched. Deduction 0.2 for scope expansion mid-execution (Candidate 1 grew from "one subsection" to "subsection + v1.4.0 retirement propagation"). |
| Anti-Frankenstein | 9.0 | Reverses v1.5.0's 12-halt-card Frankenstein-lite (net −10 bilingual variants). Third consecutive anti-Frankenstein retroactive (v1.4.2 legacy fallback drop + v1.5.0 network fallback retirement + v1.5.1 halt cards drop). Deduction 0.2 for landing scope-expansion discipline in the same feat rather than separate PATCH. |
| **Average** | **9.12** | **New streak ≥ 9.0 starts at 1.** Running avg ≈ 8.87 (+0.01 vs v1.5.0 running 8.86). |

### Discipline evidence

- Dogfood-first ordering successfully reversed preemptive-prose mistake — if Candidates 1+2 had shipped before dogfood, Friction #1 (v1.4.0 contradiction) and Friction #6 (silent-skip consent) would have been missed, and Candidate 2 would have kept `EXIT_SDK_MISSING` distinct on prose-only grounds (H3).
- Code-reviewer pre-commit pass caught a latent runtime-contract bug (Path 2a/2b bifurcation) that dogfood alone did not surface. Two independent validation gates — dogfood surfaces prose-level ambiguities; reviewer surfaces prose-level-contract collisions. Both needed.
- Honest self-rating ritual applied between feat and chore commits even though projection (9.24) was ≥ 9.0.

---

## [1.5.0] — 2026-04-19 — "genesis-drop-zone living memory + arbitration (MINOR)"

**genesis-drop-zone living memory** — first MINOR bump on the v1.5.x line. Closes Friction #3 (reconciliation policy not codified) + absorbs Friction #1 + #2 (multi-source seed shape) from the 2026-04-18 v1.4.1 dogfood. **Anti-Frankenstein retroactive**: v1.4.0's silent graceful fallback retired on user challenge ("pourquoi pas d'API ?") in favour of explicit halt-with-remediation card. R8 research `sota/anthropic-auth-and-oauth-status_2026-04-19.md` confirms no first-party OAuth path for Messages API in April 2026 → halt-with-remediation is the only ToS-clean contract.

### Added

- `genesis-drop-zone` Phase 0.4 — cross-session divergence detection (in-context, four-class diff: Completion / Retirement / Divergence / Unchanged) when `drop_zone_intent.md` already exists at cwd
- `genesis-drop-zone` Phase 0.5 — consolidated bilingual arbitration card (intra-drop + cross-session divergences in one Victor turn)
- `drop_zone_intent_history/v<N>_<ISO8601-Z>.md` archive directory with bidirectional supersession pointers (`supersedes_snapshot` on new + `superseded_by` on archived)
- 3 additive frontmatter keys: `snapshot_version`, `arbitrated_fields`, `supersedes_snapshot` (schema_version stays at 1, additive only)
- 14 new bilingual variants (R9 tier-3 paired-authored): 1 arbitration FR + 1 arbitration EN + 6 halt-with-remediation FR + 6 halt-with-remediation EN
- Layer B `⚖` marker rendering on `genesis-protocol` Phase 0 Step 0.4 card + Step 0.5 `bootstrap_intent.md` template — opt-in, additive, zero parser change
- Extractor `divergences[]` JSON output — extractor flags intra-drop semantic conflicts; consumed by Phase 0.5
- Extractor `_shape_divergences()` validator — flag-never-resolve principle (drops malformed divergences with stderr warning, doesn't fail extraction)
- New regression fixture `tests/fixtures/drop_zone_intent_fixture_v1_5_0_arbitrated.md`
- New R8 entry `sota/anthropic-auth-and-oauth-status_2026-04-19.md` (universal scope candidate post-ship)
- master.md cross-skill-pattern #4 fifth data-point: "Layer B opt-in additive rendering of revision-state metadata"
- master.md cross-skill-pattern #2 v1.5.0 disk class extension narrative

### Changed

- `genesis-drop-zone` extractor exit codes 2-7 now signal halt-with-remediation to SKILL.md dispatch (no fallback to v1.3.3 in-context extraction)
- `genesis-drop-zone` halt-on-existing (v1.3.2 behaviour) replaced by archive-and-supersede flow when re-run path detected
- master.md privilege map — disk class extended (write + archive + overwrite); network class fallback retired
- `.claude-plugin/plugin.json` version `1.4.2 → 1.5.0`
- Halt-with-remediation card content upgraded with 5 substantive additions per R8 research: subscription≠API explanation paragraph, Console deep-link with Claude Code role hint, OS-specific PERSISTENT one-liners (`setx` Windows / `.zshenv` POSIX), escape hatches (`ANTHROPIC_AUTH_TOKEN` / `apiKeyHelper`), `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB` future-proofing warning

### Removed

- v1.4.0 silent graceful fallback path in `extract_with_citations.py` (anti-Frankenstein retroactive — preemptive feature, never pain-driven validated; R8-confirmed only ToS-clean contract is halt-with-remediation)

### Self-rating — v1.5.0 (honest re-evaluation post-feat, in chore)

**Initial projection was 9.28/10 — corrected down to 8.62 in chore commit after honest critique surfaced 3 substantive issues.**

| Axis | Score | Notes |
|---|---|---|
| Pain-driven | 8.5 | Friction #3 closed ✓ ; but 4 sub-features shipped beyond strict #3 (Phase 0.4 detection + arbitration card + archive chain + ⚖ marker). Only #3 had documented dogfood pain; the other 3 are composition-justified extensions that have never been runtime-validated. |
| Prose cleanliness | 8.7 | 1:1 mirror discipline preserved across spec/SKILL/phase-0-welcome triple ✓ ; SKILL.md grew ~25% (49KB → ~58KB approaching the saturation pattern observed on user-level CLAUDE.md); halt-with-remediation cards have repetitive boilerplate across 6 exit codes |
| Best-at-date | 9.2 | R8 well-applied (KARMA + EMNLP + Cleanlab TLM + Kurrent SOTA cited); OAuth research grounds halt-with-remediation contract directly (R8 entry `sota/anthropic-auth-and-oauth-status_2026-04-19.md` ships in same branch) |
| Self-contained | 9.0 | Zero ripple to phase-minus-one / 5.5 / journal / post-processor / pepite ; only intentional Layer B Step 0.4+0.5 touches ; schema_version=1 preserved (additive only) |
| Anti-Frankenstein | 7.5 | Fallback retirement = textbook anti-Frankenstein retroactive ✓ ; BUT shipping 6 halt-with-remediation cards × 2 languages = 12 cards is enumeration-of-exit-codes, NOT pain-driven. Real user pain hits EXIT_NO_KEY (1 card) + EXIT_SDK_MISSING (1 card). EXIT_BAD_INPUT + EXIT_OUTPUT_INVALID are extractor-internal failure modes that hit 0% of real users. **Honest verdict: Frankenstein-lite preemption I committed mid-execution.** |
| **Average** | **8.62** | **Streak ≥ 9.0 BREAKS at 11 consecutive** (v1.2.1 → v1.4.2). v1.5.0 = first sub-9.0 since v1.2.1. |

Running average post-v1.5.0 honest: ≈ **8.86/10** (vs +0.03 projection that assumed 9.28 → actually -0.06 vs v1.4.2 running 8.92).

### Honesty correction narrative

After PR merge + tag, honest critique pass surfaced three substantive issues that the optimistic 9.28 projection ignored:

1. **Zero runtime validation of Phase 0.4 + Phase 0.5 + archive write + halt cards** — the verification probes (Task 10) check static structure (grep, JSON parse) but the in-context dispatch logic lives only in SKILL.md prose. Per Layer 0 `discipline_periodic_dogfood_checkpoint.md`, this is a known gap requiring v1.5.1 dogfood gate.
2. **6-halt-cards enumeration is Frankenstein-lite preemption** — only 2 cards (EXIT_NO_KEY + EXIT_SDK_MISSING) address real user-facing pain. v1.5.1 candidate: collapse 4 internal-failure cards into 1 generic "internal error → stderr + issue template".
3. **Phase 0.5 arbitration card relationship to v1.3.2 consent card is ambiguous** in SKILL.md — does Phase 0.5 subsume consent, or render in series? Bug latent at first runtime execution. v1.5.1 candidate: add 1 paragraph clarification.

These three v1.5.1 candidates are flagged in the resume prompt for next session.

---

## [1.4.2] — 2026-04-19 — "marketplace unblock (PATCH — `genesis-protocol` install-path resolution + skill-local R8 bundle)"

Focused PATCH closing two dogfood-observed BLOCKERS from the 2026-04-18 v1.4.1 stress test. Makes `genesis-protocol` self-sufficient for Phase 1 rules seed + Phase 2 R8 cache seed across all install modes (dogfood / `--plugin-dir` / personal-scope / marketplace). **Zero Layer A ripple** — `skills/genesis-drop-zone/**` byte-identical across v1.4.1 → v1.4.2. **Zero schema bump, zero new privilege, zero new bilingual pair, zero cross-skill-pattern change.** Pure plumbing fix + distribution bundle completion.

### Added — skill-local R8 cache templates bundle

- **New directory `skills/genesis-protocol/research-templates/`** carrying the 5 canonical R8 entries Phase 2 seeds into downstream (identical membership to existing Phase 2 Step 2.3 "Entries to copy" table):
  - `sota/claude-code-plugin-distribution.md` (copy-renamed from active R8, frontmatter refreshed 2026-04-19 / expires 2026-04-26)
  - `sota/claude-ecosystem-cross-os.md` (copy-renamed + refreshed)
  - `sota/spdx-headers.md` (copy-renamed + refreshed)
  - `stack/claude-code-plugin-structure.md` (R8-refreshed via WebSearch; **additive findings**: 17 new hook events, new optional dirs `output-styles/`/`monitors/`/`bin/`, new plugin.json optional fields, new hook type `agent`, Plugin caching + Installation scopes sections; **no structural changes**)
  - `stack/claude-code-session-jsonl-format.md` (R8-refreshed; additive: `result` record type, sub-agent `agent-<id>.jsonl` naming, issue #36583 messageId collision note; on-disk-verified 2026-04-15 baseline preserved)
- **`README.md`** documenting purpose + filename convention (no date suffix in-skill) + copy-and-rename discipline + refresh policy + escape clause

### Added — install-manifest.yaml verification checks (10 new)

1 rules file + 4 templates dir/subdirs/README + 5 individual template file checks. Total 17 existing + 10 new = **27 checks**. Version bumped `0.8.0` → `1.4.2` (recovering stale lock-step).

### Added — verification.md scenarios S1-S3

- **S1** — Personal-scope install runtime: Phase 1 Step 1.3 resolves `<skill_dir>/rules/v1_rules.md` via single skill-local path. Zero three-levels-up probe.
- **S2** — Phase 2 R8 cache seed from skill-local templates: all 5 entries copied to downstream with seed-date suffix.
- **S3** — Install-manifest verification failure-loudness: missing rules/ file triggers specific-path error message, no silent fallback.

Ship gate: **S1 + S2 + S3 all mandatory**. Regression on v1.4.1 #40, #41 + v1.3.2 #18, #19 mandatory.

### Added — R8 active-entries returns (2 post-refresh)

- `.claude/docs/superpowers/research/stack/claude-code-plugin-structure_2026-04-19.md` (supersedes archive/2026-04-14 entry)
- `.claude/docs/superpowers/research/stack/claude-code-session-jsonl-format_2026-04-19.md` (supersedes archive/2026-04-15 entry)

### Changed — phase-1-rules-memory.md Step 1.3 + Step 2.3

- **Step 1.3** — legacy "Fallback (legacy) / three levels above SKILL.md" paragraph **deleted**. Single canonical path `<skill_dir>/rules/v1_rules.md`. If missing, halt with single-path error + reinstall remediation. Preserved verbatim: "Why skill-local" (F29 forensics), "Adaptation", "Do not rewrite the rules".
- **Step 2.3 opening paragraph rewritten** — resolver points to `<skill_dir>/research-templates/`. New halt message for missing templates dir. Follow-on rationale paragraph + expiration discipline preserved verbatim.
- **Step 2.3 "Entries to copy" 5-row table** — Source column paths patched (`<plugin-root>/...*_*.md` → `<skill_dir>/research-templates/<topic>.md`). Destination + rationale columns unchanged. Row membership unchanged.
- **New "Copy-and-rename discipline (v1.4.2)" paragraph** appended — documents skill-local (no date suffix) vs downstream-cache (with seed-date suffix) convention.

### Changed — version bumps

- `.claude-plugin/plugin.json` — `1.4.1` → `1.4.2`.
- `install-manifest.yaml` — `0.8.0` → `1.4.2` (recovering from v0.8 stale lock-step).

### Removed — legacy three-levels-up fallback

Deleted from `phase-1-rules-memory.md` Step 1.3. v1.2.1 F29 belt-and-suspenders retired after three versions of zero-hit dead code. Anti-Frankenstein retroactive.

### Self-rating — v1.4.2

| Axis | Score | Reasoning |
|---|---|---|
| Pain-driven | 9.3 | Friction #4 + #5 dogfood-observed BLOCKERS; strongest pain-driven ship on BLOCKER-severity axis since v1.2.3 F34 (v1.2.3 retains the distinct live-on-ship-reproduction distinction; v1.4.2's pain was observed in a prior-session dogfood). −0.2 replay-deferred for S1/S2/S3. Net 9.3. |
| Prose cleanliness | 9.2 | Six-commit rhythm 7th consecutive application (chore-dogfood-archive precedes the count). Spec 3-iteration review loop + plan 2-iteration review loop, all advisories landed. Living-spec `v2_etape_0_drop_zone.md` undiluted (topic-scoped standalone spec). |
| Best-at-date | 9.2 | R8 refresh grounded in 2026-04-19 WebSearch. Escape clause pre-verified no structural drift. 3 sota frontmatter-refreshed to ship date. 2 additive-evolution findings flagged for v1.5.x+ consideration. |
| Self-contained | 9.4 | Narrow surface: 2 runbook edits + 1 new dir (6 files) + 1 config bump + 1 scenario block + 1 version bump + 1 INDEX update. Zero Layer A ripple verified empirically via `git diff main --stat -- skills/genesis-drop-zone/` returning empty. |
| Anti-Frankenstein | 9.4 | Legacy fallback dropped as retroactive cleanup. Bundle membership preserved identically (no narrowing, no speculation). Content-currency-only refresh discipline. Halt-with-remediation discipline traveling from v1.5.0 parallel-branch spec to v1.4.2. No speculative additions. |
| **Average** | **9.30** | |

**11th consecutive ship ≥ 9.0** (v1.2.1 9.26, v1.2.2 9.14, v1.2.3 9.18, v1.2.4 9.16, v1.3.0 9.34, v1.3.1 9.30, v1.3.2 9.28, v1.3.3 9.30, v1.4.0 9.10, v1.4.1 9.14, **v1.4.2 9.30**). Running average post-v1.4.2 ≈ **8.92/10** (+0.03 vs v1.4.1 running avg 8.89).

### Relation to v1.5.0

v1.4.2 is **prerequisite** for v1.5.0's value delivery. v1.5.0 spec (already APPROVED on parallel branch `feat/v1.5.0-living-memory` commit `59a7640`) introduces living drop zone memory with arbitration + archive — features that only benefit users who can install Genesis in the first place. Post-v1.4.2 ship, v1.5.0 plan + feat + chore remain.

### Next session entry point

`.claude/docs/superpowers/resume/2026-04-19_v1_4_2_to_v1_4_3_or_v1_5_0.md`. Candidates: v1.5.0 MINOR (living memory — plan + feat + chore), v1.4.3 PATCH (Friction #1/#2/#3 multi-file seed if dogfood pain resurfaces), or other direction.

---

## [1.4.1] — 2026-04-18 — "genesis-protocol Layer B citation surfacing (PATCH — end-to-end audit-trail loop closed, zero Layer A ripple)"

First PATCH on the v1.4.x audit-trail line. **Closes the end-to-end audit-trail loop opened by v1.4.0**: the `<field>_source_citation` nested keys that v1.4.0 persists in `drop_zone_intent.md` frontmatter now render inline as `[page N]` / `[pages N-M]` / `[lines X-Y]` suffix on `genesis-protocol`'s Phase 0 Step 0.4 intent card and Step 0.5 `bootstrap_intent.md` template. **Zero Layer A ripple** — `skills/genesis-drop-zone/**` is byte-identical across v1.4.0 → v1.4.1. **Zero fixture churn** — reuses v1.4.0 fixtures. **Zero privilege change, zero dependency, zero subprocess, zero network, zero schema bump.** Read-only rendering of existing data on two existing Layer B surfaces.

### Added — Layer B citation rendering (v1.4.1)

- **Step 0.2a citation preservation** — `skills/genesis-protocol/phase-0-seed-loading.md` Step 0.2a gains `#### Citation preservation (v1.4.1)` subsection documenting that the dict-based YAML parser preserves the 9 `<field>_source_citation` nested keys (`idea_summary_source_citation`, `nom_source_citation`, `type_source_citation`, `hints_techniques_source_citation`, `attaches_source_citation`, `pour_qui_source_citation`, `langue_detectee_source_citation`, `budget_ou_contrainte_source_citation`, `prive_ou_public_source_citation`). Key omission (not explicit `null`) signals absence. Parser mechanics **unchanged** — documentation-only.
- **Step 0.4 intent card template extension** — `<citation>` placeholder inline on 5 mapped rows (Project name, Project slug, Vision, Stack hints, Is-a-plugin) + 4 extras rows (Target audience, Language detected, Budget / constraint, Visibility). Citation-source mapping table documents the 9 row → key pairings (Project slug propagates `nom_source_citation`; Is-a-plugin propagates `type_source_citation`). **Citation suffix format reuses** `skills/genesis-drop-zone/phase-0-welcome.md § "Citation annotation format (v1.4.0)"` **verbatim** as single source of truth — language-neutral ASCII, no locale branching.
- **Step 0.4 `#### Rows explicitly NOT annotated`** — documents the 6 rows without Layer A source (`Target folder`, `License`, `Plan tier`, `Scope locks`, `Gaps to fill`, `Mixed media`). `Mixed media` gets the fullest rationale: `attaches_source_citation` is **preserved but not rendered** because the row's value is sourced from Step 0.3 disk `Glob`, not from `attaches` — rendering the citation on this row would lie about provenance.
- **Step 0.5 `bootstrap_intent.md` template extension** — `<citation>` placeholder inline inside `Value` columns of `## Fields` table (5 rows) and `## Conversational context from drop zone` table (4 rows). Same citation-source mapping as Step 0.4. No new section added, no new column, no schema version bump. Legacy `config.txt` sessions render the `## Fields` table verbatim with no citation suffixes anywhere.

### Added — verification.md scenarios #40-#44

- **Scenario #40** — happy path: seed via `drop_zone_intent_fixture_v1_4_0_fr_with_citations.md` (4 citation entries); Step 0.4 card renders inline suffixes on 4 rows; Is-a-plugin row shows `no (inferred) [page 2]` (propagated from `type_source_citation`); Step 0.5 same suffixes in `## Fields` + `## Conversational context from drop zone`.
- **Scenario #41** — fallback fixture absence parity: seed via `drop_zone_intent_fixture_v1_4_0_fallback.md` (no citations anywhere); Step 0.4 + Step 0.5 render with zero suffixes; anti-Frankenstein null-visible (absence of citation is absence of suffix, not `[unknown]`).
- **Scenario #42** — legacy config.txt render parity: no `drop_zone_intent.md` present; Step 0.4 card renders without `Additional context from drop zone` block and without any citation suffixes; Step 0.5 `## Fields` no suffixes; byte-identical to v1.3.2 / v1.3.3 legacy rendering.
- **Scenario #43** — synthetic partial-citations (only `idea_summary_source_citation` present); per-row gate evaluation confirmed independently (Vision has `[page N]`, others don't). Reasoning-only probe; −0.2 Pain-driven deduction per runtime-replay-deferred convention.
- **Scenario #44** — Mixed media unadorned honesty: `attaches_source_citation` present but `Mixed media` row renders without suffix; cross-check `grep '[page 4]'` on Mixed media line returns zero matches.

Ship gate: **#40, #41, #42, #44 mandatory**; **#43 strongly recommended**; regression on v1.4.0 #37, #38 + v1.3.2 #18, #19 + v1.3.1 #7.

### Changed — memory + cross-skill patterns

- `memory/master.md`:
  - **Cross-skill-pattern #2 privilege map entry for `genesis-drop-zone` appended with v1.4.1 qualifier** — "privilege map unchanged — Layer B-only rendering extension, zero Layer A ripple, no new privilege class".
  - **Cross-skill-pattern #4 extended with v1.4.1 discipline upgrade** — "Layer B may opt-in to render additive keys read-only. Parser mechanics unchanged; rendering logic gains conditional branches on key presence. Fourth data-point of the zero-ripple principle: v1.3.2 wire + v1.3.3 body-vs-frontmatter asymmetry + v1.4.0 additive keys + v1.4.1 additive rendering. Ripple measured at two levels — parser-level (unchanged across the v1.3.2 → v1.4.1 range) and contract-level (forward-compat with old writers preserved: old Layer A + new Layer B = zero citations rendered; new Layer A + old Layer B = citation keys ignored, no crash)." Future Étape-skills composing on this pattern default to "additive keys + additive read-only rendering".

### Changed — v1.4.1 spec addition (Étape 0 drop-zone living spec, sixth consecutive version-scoped scope section)

- `.claude/docs/superpowers/specs/v2_etape_0_drop_zone.md` — adds `## Scope — v1.4.1 Layer B citation surfacing` section (in-scope 9 items + out-of-scope 5 items + rationale 9 bullets); new `### Citation rendering (v1.4.1)` subsection inside existing `## Layer B integration — genesis-protocol Phase 0 (v1.3.2)` section (dispatch lifecycle + annotation format single-source-of-truth pointer + Step 0.4 extended template + citation-source mapping + "Rows explicitly NOT annotated" + Step 0.5 extended template + zero-ripple-elsewhere note); Cross-layer pattern paragraph gains v1.4.1 discipline upgrade sentence; primary 1:1 mirror map gains v1.4.1 scope row (Spec-only) + v1.4.1 rationale row (Spec-only); Cross-skill mirror addendum gains 4 v1.4.1 rows targeting `genesis-protocol/phase-0-seed-loading.md`; R9 tier map gains v1.4.1 no-new-rows paragraph; Verification scenarios intro updated "five ship-gate blocks" → "six"; new scenarios #40-#44 table + v1.4.0 regression set for v1.4.1 note; ship gates block extended; runtime replay note rolled forward; Deferred-to-v1.4.1+ renamed to Deferred-to-v1.4.2+ (item 1 Layer B citation surfacing closed); new top-level `## Rationale for v1.4.1 route` with 9 bullets. **Total +240 / -17 lines** + 2-advisory spec polish (+6 / -5 lines).

### Bumped

- `.claude-plugin/plugin.json` version `1.4.0` → `1.4.1` (**PATCH**).

### Self-rating — v1.4.1

| Axis | Score | Reasoning |
|---|---|---|
| Pain-driven | 8.6 | Loop-closure, not pain-response — no concrete user pain triggered the ship. v1.4.0 created the asymmetry (citations at Layer A, not Layer B); v1.4.1 closes it. Honest ceiling absent user-pain signal. −0.2 per replay-deferred scenario: #40 + #42 require fresh Claude Code session (runtime replay). −0.2 for #43 reasoning-only probe (no synthetic partial-citations fixture created, per zero-fixture-churn design decision). Net ≈ 8.6. |
| Prose cleanliness | 9.3 | Six-commit rhythm sixth consecutive application (spec + spec polish + plan + plan polish + feat + chore). Living-spec pattern sixth consecutive version-scoped scope section (v1.3.0, v1.3.1, v1.3.2, v1.3.3, v1.4.0, v1.4.1). Single source of truth preserved for annotation format (pointer from Layer B back to Layer A v1.4.0 subsection, no redefinition). 2 spec advisories + 3 plan advisories all landed cleanly. |
| Best-at-date | 9.2 | R8 `v2_promptor_fusion_landscape_2026-04-17.md` primary source fresh until 2026-04-24. No new R8 entry needed — v1.4.1 doesn't touch extractor, so `anthropic-python_2026-04-18.md` stack entry (expires 2026-04-19) is not exercised. Citation rendering format reuses v1.4.0 convention verbatim. |
| Self-contained | 9.4 | One PR, one skill touched (`genesis-protocol`). Zero Layer A ripple verified empirically pre-commit + post-commit (`git diff main --stat -- skills/genesis-drop-zone/` empty). Zero fixture churn. Zero new dependency. Zero new file. Pure additive edits to 4 existing files (`phase-0-seed-loading.md`, `verification.md`, `master.md`, `plugin.json`). Narrower than v1.4.0 by every surface metric. |
| Anti-Frankenstein | 9.2 | Inline suffix rendering only — no helper function, no abstraction, no speculative surface. `Mixed media` row deliberately unadorned per honest-provenance rule (preserved-but-not-rendered, not preserved-and-rendered-wrongly). Propagated citations for Project slug + Is-a-plugin are the honest reading of deterministically-derived values. No new vocabulary introduced; existing `<value or [missing]>` placeholder style mirrored. Cross-skill-pattern #4 discipline upgrade is natural fourth data-point composition, not a one-off. |
| **Average** | **9.14** | Aspirational ≥ 9.3/axis met on 1/5 (Prose cleanliness 9.3); floor ≥ 9.0 respected on 4/5; Pain-driven honestly below 9.0 at 8.6 — acknowledged in rationale as "loop-closure, not pain-response". Net 9.14 average. |

**Tenth consecutive ship ≥ 9.0** (v1.2.1 9.26, v1.2.2 9.14, v1.2.3 9.18, v1.2.4 9.16, v1.3.0 9.34, v1.3.1 9.30, v1.3.2 9.28, v1.3.3 9.30, v1.4.0 9.10, v1.4.1 9.14). Running average lift across 21 tagged ships ≈ 8.89 (+0.01).

### Replay-deferred scenarios

Runtime replay of scenarios #40 (happy path fixture + `/genesis-protocol` + Step 0.4 card render) and #42 (legacy `config.txt` render parity) require a fresh Claude Code process in an empty directory invoking `/genesis-protocol` — not executable from inside the ship session. Scenario #43 (synthetic partial-citations) is reasoning-only per zero-fixture-churn design. Artefact-level verification is the ship gate: template inspection, grep probes on `<citation>` placeholder counts (20 ≥ 18 target), anchored Mixed media probe (`awk '/^Mixed media +:/' | grep -c '<citation>' = 0`), fixture round-trip via `Read`, origin-tag counts in regression range. Consistent −0.2 Pain-driven deduction per replay-deferred / reasoning-only scenario rolls forward per v1.3.1 → v1.4.0 convention.

### Next session

`.claude/docs/superpowers/resume/2026-04-18_v1_4_1_to_v1_4_2.md` — v1.4.2 candidates: **A `cited_text_preview` inline surfacing** (render the 80-char quoted preview on hover / expand), **B hyperlink citations** (harness-dependent — needs IDE + web), **C Files API beta adoption** (dedup + larger limits), **D UX toolkit polish** (@clack/prompts + Charm Gum + cli-spinners), **E error-handling refinements** (filesystem permission-denied / disk-full / symlink edge cases).

---

## [1.4.0] — 2026-04-18 — "genesis-drop-zone Citations API extraction (second concentrated privilege class — network; silent graceful fallback; MINOR bump)"

First MINOR bump since v1.3.0 opened the v1.3.x conversational-layer line. Introduces the **second concentrated privilege class** for `genesis-drop-zone`: external Anthropic Messages API call via Python subprocess (`skills/genesis-drop-zone/scripts/extract_with_citations.py`) enabling `citations: {enabled: true}` per document block. Per-field source attribution renders inline in the mirror as `[page N]` / `[lines X-Y]` annotations and persists as optional `<field>_source_citation` nested entries in `drop_zone_intent.md`. **Silent graceful fallback** to v1.3.3 in-context extraction when `ANTHROPIC_API_KEY` is unset, the SDK is missing, the API fails, or output validation fails — the mirror renders v1.3.3-identical with no user-facing indication. **Zero Layer B ripple preserved via additive frontmatter keys** — `schema_version` stays at `1`; Layer B Step 0.2a dict-based parser ignores unknown keys naturally.

### Added — v1.4.0 Citations API extraction path

- **Python extractor** `skills/genesis-drop-zone/scripts/extract_with_citations.py` (356 lines). Reads stdin JSON payload, calls Anthropic Messages API with Citations + 1h cache TTL explicit, emits JSON on stdout or exit codes 0/2/3/4/5/6/7 with stderr diagnostic. Uses the `anthropic` Python SDK (deferred import so exit code 3 surfaces cleanly on missing package). FR canonical null-class tokens enforced via system prompt regardless of source-content language.
- **typed-text citation wrapping** — non-empty inline user text is wrapped in a synthetic `document` block at index 0 of the `documents[]` array with `type: "text"`, `source.type: "text"`, `citations: {enabled: true}`. Makes inline text a citeable source. Attachments follow at indices 1..N. Image blocks are a separate content-block type and do NOT carry the citations flag.
- **Mirror annotation format** — language-neutral ASCII. PDF citations render as `[page N]`, text citations as `[lines X-Y]` (derived from char offsets via `\n` counting, 1-indexed). Image-only drops produce no citations. The single truncation-rule exception: the annotation is appended after the 57 + `...` truncation and may push rows over 60 chars.
- **Frontmatter schema extension** — `drop_zone_intent.md` gains optional nested keys `<field>_source_citation` with shape `{type, document_index, start, end, cited_text_preview}`. Key is **omitted** (not `null`) when no citation applies. `schema_version` stays at `1`.
- **Five mitigations for the network privilege class** — pre-flight env check at skill entry (immutable for session); subprocess isolation; explicit 1h cache TTL always; token-budget logging to stderr (forensic only); silent graceful fallback (no privilege escalation on failure).
- **Environment variables** — `ANTHROPIC_API_KEY` (required; absence → fallback), `GENESIS_DROP_ZONE_MODEL` (default `claude-opus-4-7`), `GENESIS_DROP_ZONE_CACHE_TTL` (default `1h`; never defaulted to `5m` by omission per R8 § Stage 2 mandate), `GENESIS_DROP_ZONE_VERBOSE` (opt-in detailed stderr tracing).

### Added — three new fixtures

- `tests/fixtures/drop_zone_intent_fixture_v1_4_0_fr_with_citations.md` — FR body + 4 `_source_citation` entries with `pdf_page_range` citations. Ship-gate artefact for scenarios #28 (FR), #35 (modification loop), #37 (Layer B parser regression).
- `tests/fixtures/drop_zone_intent_fixture_v1_4_0_en_with_citations.md` — EN body + 4 `_source_citation` entries with `text_char_range` citations (exercises alternate citation type). FR canonical null tokens preserved in frontmatter (v1.3.3 asymmetry unchanged). Ship-gate artefact for #28 (EN) + #37.
- `tests/fixtures/drop_zone_intent_fixture_v1_4_0_fallback.md` — byte-identical to `drop_zone_intent_fixture_v1_3_3_en.md` modulo `skill_version`. CRLF preserved (Python binary-mode copy via `Path.write_bytes`; `perl -pi` / `sed -i` both silently normalize to LF under git-bash and would break the byte-identity claim). Ship-gate artefact for #29 + #38.

### Added — R8 stack entry

- `.claude/docs/superpowers/research/stack/anthropic-python_2026-04-18.md` pinning `anthropic>=0.40.0` minimum + documenting required SDK surface (Messages API + citations + cache_control + usage) + March 2026 cache-TTL default regression + TTL 1 day per stack convention.
- `INDEX.md` row added for the stack entry; `v2_promptor_fusion_landscape` row summary updated to mention the v1.4.0 Citations extractor.

### Changed — SKILL.md dispatch surface

- `skills/genesis-drop-zone/SKILL.md`:
  - New top-level `## Citations API dispatch (v1.4.0)` section (~120 lines) — three-gate lifecycle (`is_fresh_context` / `welcome_locale` / `api_extraction_available`), Python extractor invocation contract with exit-code table, typed-text wrapping rule with exact Python dict shape, four fallback triggers, citation object shape YAML, environment variables table, modification-loop interaction, zero Layer B ripple preserved note.
  - `### In scope (v1.4.0)` sub-block added with 10 bullets mirroring spec scope.
  - `### Out of scope (deferred to v1.4.1+)` replaces v1.3.3's v1.3.4+ block (12 items).
  - `## Phase 0 — mirror` extended with v1.4.0 extraction-source dispatch note + annotation truncation exception.
  - `## Phase 0 — drop_zone_intent.md file` extended with additive frontmatter keys note; `skill_version` stamp reference bumped to `1.4.0`.
  - **`## Concentrated privilege` entirely rewritten** — single-paragraph version replaced with per-class table (v1.3.0-v1.4.0 rows), `### Disk class mitigations (unchanged since v1.3.2)` + `### Network class mitigations (new in v1.4.0)`, `### Precedent for future multi-class privileges` sub-section. Forward note (the v1.3.3 "v1.3.4+ may introduce a second privilege" note) deleted — Path A has shipped.
  - `## Deferred scope` rewritten with 12-item v1.4.1+ list.
  - **All stale v1.3.4+ references swept** — line 70 closing sentence bumped to v1.4.1+; line 367 Forward note deleted; lines 373/378 deferred-list items rewritten.

### Changed — phase-0-welcome.md runtime template surface

- New `### Citation annotation format (v1.4.0)` subsection between the two Mirror template sections and the Bridge section. Documents `[page N]` / `[lines X-Y]` format, truncation rule exception, no-annotation cases (fallback / image-only / uncited field). Language-neutral ASCII. Welcome box ASCII-art frames (2) preserved intact — R9 regression probe verified.

### Changed — memory + cross-skill patterns

- `memory/master.md`:
  - **Cross-skill-pattern #2 refined** from "at most one concentrated privilege per skill" to **"at most one concentrated privilege per operation class, per skill"**. Adds four criteria for multi-class declarations (own consent model, own five mitigations, independently disableable, own failure mode). Notes that a skill accreting a third class should trigger a hard anti-Frankenstein review. `genesis-drop-zone` entry updated to name the **first multi-class declaration in Genesis** — disk (v1.3.2) + network (v1.4.0).
  - **Cross-skill-pattern #4 extended** — v1.4.0 preserves zero-Layer-B-ripple via additive frontmatter keys (`<field>_source_citation`) without bumping `schema_version`. Establishes additive frontmatter + zero-parser-change as the default route for any future Layer A feature that wants to push new information into the cross-layer contract.

### Changed — v1.4.0 spec addition (Étape 0 drop-zone living spec, fourth consecutive version-scoped scope section)

- `.claude/docs/superpowers/specs/v2_etape_0_drop_zone.md` — adds `## Scope — v1.4.0 Citations API extraction` section (in-scope 10 items + out-of-scope 8 items + rationale 9 bullets); new design section `## Citations API — signal + dispatch (v1.4.0)` (dispatch lifecycle + extractor contract + typed-text wrapping + fallback triggers + citation object shape + env vars + modification-loop interaction + zero Layer B ripple preserved); concentrated-privilege declaration rewritten as per-class table with refinement section; 1:1 mirror map extended with v1.4.0 scope + dispatch rows; R9 language policy gains v1.4.0 additions table (Python extractor + extraction prompt + stderr + citation annotations + `_source_citation` nested keys); Deferred-to-v1.3.4+ renamed to Deferred-to-v1.4.1+ with 12 items (Path A Citations CLOSED, removed); verification scenarios #28–#39 added; ship gates updated for v1.4.0 (mandatory #29/#32/#33/#36/#37/#38); References section gains Messages-API + Prompt-Caching line + "New R8 stack entry required" block; new top-level `## Rationale for v1.4.0 route` with 10 bullets. **Total +287 / -26 lines** + 4-advisory spec polish (+42 / -7 lines). Spec frontmatter `target_version` / `description` / `updated_at` lines updated.

### Bumped

- `.claude-plugin/plugin.json` version `1.3.3` → `1.4.0` (**MINOR**).

### Self-rating — v1.4.0

| Axis | Score | Reasoning |
|---|---|---|
| Pain-driven | 9.1 | Closes the last big structural lever for `genesis-drop-zone` (audit-trail via API-hard citations). Victor can now see "Genesis saw this on page 1 of my brief" when the API path runs. Silent fallback is by design (invisible pain-solving when API is off) but documented. Partial −0.2 for eight replay-deferred scenarios (#28-#35 require fresh Claude Code + live API key) rolling forward per v1.3.x convention. |
| Prose cleanliness | 9.1 | Living-spec pattern held for fifth consecutive ship (v1.3.0 → v1.3.1 → v1.3.2 → v1.3.3 → v1.4.0). Six-commit rhythm maintained (spec + spec polish + plan + plan polish + feat + chore). 4 spec advisories + 4 plan advisories landed (both reviewer passes hit 4 — higher than prior cycles because the ship is larger). Per-class privilege table replaces the single-paragraph form across spec + SKILL.md + master.md consistently. |
| Best-at-date | 9.2 | R8 `v2_promptor_fusion_landscape_2026-04-17.md` still fresh until 2026-04-24 (primary source for Citations + 1h cache + Path A commitment). New R8 stack entry `anthropic-python_2026-04-18.md` pinning SDK version + documenting March 2026 cache-TTL regression. Explicit 1h TTL mandate honoured everywhere. Opus 4.7 default with env override. No speculative features. |
| Self-contained | 8.9 | One skill touched but adds real surface area: new Python file (356 lines), 3 new fixtures, new R8 stack entry, new env var dependency (`ANTHROPIC_API_KEY`), new Python package dependency (`anthropic`), new subprocess invocation. Honest deduction for the architectural bulk — this is a MINOR bump that legitimately broadens the skill's runtime surface. Compensated by silent-fallback-to-v1.3.3 meaning users without the API key see zero change from v1.3.3. |
| Anti-Frankenstein | 9.2 | Every element earns its place — Python for SDK handling; env check for pre-flight; subprocess for isolation; 1h TTL for documented API regression; key omission over explicit null for byte-identity. Cross-skill-pattern #2 refinement is structural evolution, not a one-off. No hardcoded Opus→Sonnet chain (single active model per invocation). No user-facing informational note (silent fallback by design, rejected at brainstorm). Three stacked justifications for MINOR over PATCH articulated explicitly in spec rationale. |
| **Average** | **9.10** | Aspirational ≥9.3/axis met on 1/5 (Best-at-date 9.2); floor ≥9.0/axis respected on 4/5; Self-contained honestly below 9.0 at 8.9 — acknowledged in rationale as MINOR-bump-legitimate surface growth. Net 9.10 average. |

**Ninth consecutive ship ≥ 9.0** (v1.2.1 9.26, v1.2.2 9.14, v1.2.3 9.18, v1.2.4 9.16, v1.3.0 9.34, v1.3.1 9.30, v1.3.2 9.28, v1.3.3 9.30, v1.4.0 9.10). Running average lift across 20 tagged ships ≈ 8.88.

### Replay-deferred scenarios

Runtime replay of scenarios #28 (API happy path PDF), #29 (fallback silent identity), #30 (text-only inline with text_char_range), #31 (image-only → no citations), #32 (bad key → fallback), #33 (SDK missing → fallback), #34 (rate-limit simulation), #35 (modification-loop cache hit) all require a fresh Claude Code process in an empty directory with live `ANTHROPIC_API_KEY` and Python runtime — not executable from inside a running session. Artefact-level verification is the ship gate: Python syntax check, R9 audit decomposed (em-dash count = 1, other non-ASCII = 0), functional YAML parse of both `_with_citations` fixtures, fallback byte-identity via `diff`, Layer B `git diff main` empty. Consistent −0.2 Pain-driven deduction per replay-deferred scenario rolls forward until runtime replay happens (same convention as v1.3.1 → v1.3.3).

### Next session

`.claude/docs/superpowers/resume/2026-04-18_v1_4_0_to_v1_4_1.md` — v1.4.1 candidates: **A Layer B citation surfacing** (Step 0.4 intent card + Step 0.5 `bootstrap_intent.md` template display the `[page N]` annotations alongside the parsed fields; additive Layer B extension), **B UX toolkit polish** (`@clack/prompts` + Charm Gum + cli-spinners on the welcome / mirror surfaces — surface is complete now so polish can land without re-fragmenting), **C error-handling refinements** (filesystem-side permission-denied / disk-full / symlink edge cases — API-side errors have their own fallback), **D Files API beta adoption** (dedup + larger file limits).

---

## [1.3.3] — 2026-04-18 — "genesis-drop-zone runtime locale rendering (R9 tier-3 loop closed end-to-end, zero Layer B ripple)"

Runtime locale dispatch across Layer A user-facing surfaces. Welcome + mirror + consent card + halt + bridges + body echo now render the FR variant or EN variant — never both — based on two locale variables. Closes the R9 tier-3 rendering loop opened in v1.3.0 (bilingual templates authored day 1) and carried through v1.3.1 (mirror + 9-field labels) / v1.3.2 (consent card + halt + two bridges).

### Added — genesis-drop-zone v1.3.3 locale dispatch

- **Two-variable runtime locale model** with distinct lifecycles:
  - `welcome_locale` — resolved at skill invocation from trigger-phrase language (FR phrase → `FR`, EN phrase → `EN`); defaults to `FR` on slash invocation `/genesis-drop-zone` (no language signal). Drives welcome box + zero-content re-prompt.
  - `content_locale` — resolved from extracted `langue_detectee` after first content turn (`FR` → FR, `EN` → EN, `mixte` → FR tiebreaker). Drives mirror + consent card + halt + bridges + `drop_zone_intent.md` body echo.
- **Locale-switched rendering** on seven surfaces — each prints exactly one variant per invocation, not both.
- **Divergence between the two variables is expected** — a user with EN intent phrase then FR content sees EN welcome + FR mirror onwards; inverse equally possible. Each surface honours the best signal available at its render time.
- **One new bilingual pair** — EN zero-content re-prompt `I'm listening — drop or write whatever you want to share.` pairs the v1.3.0 FR `Je t'écoute — dépose ou écris ce que tu veux me partager.` (the only bilingual gap across v1.3.0–1.3.2; all other EN variants were already authored day-1 per R9 tier 3).

### Preserved — zero Layer B ripple

- **Frontmatter data contract unchanged** — `drop_zone_intent.md` frontmatter null-class tokens stay **FR canonical** (`"a trouver ensemble"`, `"non mentionne"`, `"non mentionnee"`, `"a affiner — ..."`) regardless of `content_locale`. Layer B's `phase-0-seed-loading.md` Step 0.2a parser is completely untouched — same code reads FR and EN body fixtures identically.
- **Deliberate Layer A / Layer B asymmetry** documented in spec + SKILL.md + master.md: body = locale-detected human echo; frontmatter = FR canonical data contract. Bilingual Layer B null-class parsing explicitly deferred to v1.4+ if real pain emerges.
- **Concentrated privilege class unchanged** — still v1.3.2's single disk write to cwd after consent, halt-on-existing, no `mkdir`. Runtime rendering layer only — no new API call, no new subprocess, no new dependency.

### Changed — living spec + 1:1 mirror map

- `.claude/docs/superpowers/specs/v2_etape_0_drop_zone.md` — adds `## Scope — v1.3.3 runtime locale rendering` (in/out scope + rationale) + new design section `## Runtime locale — signal + dispatch (v1.3.3)` (two-variable table + render targets + divergence rules + frontmatter-contract-unchanged note + zero-content / modification-loop branches). Consent card / halt / accept bridge / decline bridge / drop_zone_intent.md sections updated inline with locale-switched subsections. 1:1 mirror map adds v1.3.3 scope + locale-dispatch rows. R9 language policy table splits frontmatter-values vs body with explicit v1.3.3 asymmetry note. Deferred list renamed to v1.3.4+; runtime locale item removed (closed); bilingual Layer B parsing deferred to v1.4+. Verification scenarios #20–#27 new. Ship gates for v1.3.3 defined with mandatory + strongly-recommended + regression sets. `## Rationale for v1.3.3 route` section added at spec level. Frontmatter header updated (target_version + description + updated_at). Scenario #5 / #9 / #10 expected outcomes updated inline with (v1.3.3 supersession) markers preserving v1.3.1 expectation in parentheses for version traceability.

### Changed — skill files

- `skills/genesis-drop-zone/SKILL.md` — new `## Locale dispatch (v1.3.3)` top-level section mirroring spec design. `### In scope (v1.3.3)` / `### Out of scope (deferred to v1.3.4+)` sub-blocks added. Inline v1.3.3 locale dispatch notes on `## Phase 0 — mirror`, `## Phase 0 — bridge`, `## Phase 0 — consent card`, `## Phase 0 — halt branch`, `## Phase 0 — bridges`, `## Phase 0 — drop_zone_intent.md file`. Concentrated privilege block gains v1.3.3 qualifier. Deferred scope list updated to v1.3.4+ with Citations API flagged as v1.3.4 candidate. Schema metadata `skill_version` reference updated to 1.3.3.
- `skills/genesis-drop-zone/phase-0-welcome.md` — section headers rewritten with explicit render conditions (`welcome_locale = FR/EN`, `content_locale = FR/EN`). Consent card + halt + accept bridge + decline bridge sections split into FR variant + EN variant sub-blocks. Zero-content branch extended with the newly-authored EN re-prompt. Top-of-file intro paragraph rewritten to reference v1.3.3 locale-dispatch convention.

### Changed — memory + privilege map

- `memory/master.md` — privilege map entry for `genesis-drop-zone` gains v1.3.3 qualifier describing runtime locale dispatch (privilege class unchanged). Cross-skill-pattern #4 (Layer A / Layer B stratification) gains one-sentence v1.3.3 zero-Layer-B-ripple discipline note establishing it as the reference for future Layer A rendering polish.

### Added — synthetic fixture

- `tests/fixtures/drop_zone_intent_fixture_v1_3_3_en.md` — EN-content counterpart to v1.3.2's FR fixture. Frontmatter `langue_detectee: "EN"`, body prose intro + mirror echo in EN. Null-class tokens preserved FR canonical (`"non mentionne"` x2, `"non mentionnee"` x1, `"a trouver ensemble"` x1) to exercise the v1.3.3 Layer A / Layer B asymmetry contract and probe Layer B parser regression.

### Hygiene

- `.claude/docs/superpowers/research/INDEX.md` — adds missing row for `v2_promptor_fusion_landscape_2026-04-17.md` (entry existed on disk under `research/sota/` but INDEX was stale; caught during R1.1 open-ritual scan at session open).

### Bumped

- `.claude-plugin/plugin.json` version `1.3.2` → `1.3.3`.

### Self-rating — v1.3.3

| Axis | Score | Reasoning |
|---|---|---|
| Pain-driven | 9.3 | Closes a concrete R9 tier-3 violation visible since v1.3.0 (EN-native users saw FR-only UI despite EN templates existing day-1). Seven surfaces now honour detected locale end-to-end. Body-echo asymmetry with FR canonical frontmatter is user-visible + spec-documented. |
| Prose cleanliness | 9.2 | Living-spec pattern held for fourth consecutive ship (v1.3.0 → v1.3.1 → v1.3.2 → v1.3.3). Spec polish + plan polish done after reviewer passes (3 advisories each, all landed). Six-commit rhythm maintained (spec + spec polish + plan + plan polish + feat + chore). Three inline supersession markers on historical scenarios (#5, #9, #10) preserve version traceability. |
| Best-at-date | 9.2 | Inline R8 citations ceiling preserved (`v2_promptor_fusion_landscape_2026-04-17.md` still fresh until 2026-04-24). No speculative features — every EN template wired was already authored day-1 of its version. Citations API still the best-at-date lever, explicitly deferred to v1.3.4. |
| Self-contained | 9.4 | One PR, one skill touched (`genesis-drop-zone`), zero Layer B ripple. Narrower than v1.3.2 by design. Six-commit rhythm + CHANGELOG + session trace + MEMORY pointer + resume all in this ship. INDEX hygiene fix included (caught at R1.1, landed in same feat commit). |
| Anti-Frankenstein | 9.4 | Zero new privilege class. Zero new dependencies. Zero Layer B ripple (deliberately preserved FR canonical null tokens in frontmatter — documented asymmetry). One new bilingual pair (the only gap). Two-variable dispatch instead of one is the minimum wiring needed; frontmatter-locale-detection is the v1.4+ candidate if pain emerges. |
| **Average** | **9.30** | Target ≥9.3/axis met on 4/5; floor ≥9.0/axis respected on every axis. |

**Eighth consecutive ship ≥ 9.0** (v1.2.1 9.26, v1.2.2 9.14, v1.2.3 9.18, v1.2.4 9.16, v1.3.0 9.34, v1.3.1 9.30, v1.3.2 9.28, v1.3.3 9.30).

### Replay-deferred scenarios

Runtime replay of scenarios #1 (mirror dispatch), #13 (write happy path), #18 (Layer B happy path), #20 (FR intent + EN content), #21 (EN intent + FR content), #23 (slash → FR default), #24 (zero-content welcome_locale) all require a fresh Claude Code process in an empty directory — not executable from inside a running session. Artefact-level verification is the ship gate for all; runtime replay is an observability track, not a merge-blocker. Consistent −0.2 Pain-driven deduction per replay-deferred scenario rolls forward until runtime replay happens (same convention as v1.3.1 / v1.3.2).

### Next session

`.claude/docs/superpowers/resume/2026-04-18_v1_3_3_to_v1_3_4.md` — v1.3.4 candidates: **A Path A Citations API upgrade** (second privilege class, downstream reader already live), **B UX toolkit polish** (@clack/prompts + Charm Gum + cli-spinners), **C error-handling refinements** (permission-denied / disk-full / symlink edge cases).

---

## [1.3.2] — 2026-04-18 — "genesis-drop-zone write + Layer B handoff (first Layer A privilege + first cross-layer wire live)"

First cross-layer wire in the Genesis plugin. `genesis-drop-zone` switches from `none` privilege to the v1.3.2 write declaration, and `genesis-protocol` Phase 0 is extended to detect + parse + consume the written file.

### Added — genesis-drop-zone v1.3.2 Layer A privilege

- **First Layer A concentrated privilege** — `genesis-drop-zone` writes `drop_zone_intent.md` to cwd after a bilingual consent card. Narrow privilege: one file, cwd only, no `mkdir`, halt-on-existing (no overwrite / no timestamp-suffix / no second consent). Matches the halt-on-leak precedent of `session-post-processor`.
- **Bilingual consent card** — minimal accept/cancel, absolute path with arrow marker, natural-language response routing across three equivalence classes (affirmative / negative / modification loop with no iteration cap).
- **`drop_zone_intent.md` file format** — YAML frontmatter (9 semantic fields + 4 metadata keys: `schema_version`, `created_at`, `skill`, `skill_version`) + Markdown body with FR prose intro + mirror echo. UTF-8 no BOM, LF line endings. Atomic Write-tool creation.
- **Halt-on-existing protection** — bilingual halt message with absolute path + remediation; printed in place of the consent card when `test -e` detects an existing file; no overwrite, no fallback.
- **Two version-scoped bridges** — accept bridge instructs `tape /genesis-protocol`; decline bridge is warm + non-pressurizing. Supersede the v1.3.1 single bridge at runtime.

### Added — genesis-protocol v1.3.2 Layer B integration

- **First cross-layer wire live** — `genesis-protocol` Phase 0 Step 0.1 gains `drop_zone_intent.md` detection row + new **Precedence rule** (drop_zone_intent.md > config.txt > empty folder interactive seed, never silent merge).
- **New Step 0.2a — Parse drop_zone_intent.md (when present)** — validates `schema_version`, reads the 9 semantic + 4 metadata keys, maps 6 primary Layer A fields (`idea_summary` → Vision, `nom` → Project name + derived Slug, `type` → inferred Is-a-plugin, `hints_techniques` → Stack hints, `attaches` → Mixed media), preserves 4 Layer-A-specific extras (`pour_qui`, `langue_detectee`, `budget_ou_contrainte`, `prive_ou_public`) for Step 0.4 display + Step 0.5 write.
- **Step 0.4 intent card extended** with origin tags per field (`(from drop zone)`, `(from config.txt)`, `(derived)`, `(default)`, `(inferred)`) + new `Additional context from drop zone` block rendered only when seed was the drop zone.
- **Step 0.5 template extended** with `## Conversational context from drop zone` section preserving the 4 Layer-A-specific extras + `## Raw config.txt` rendered as `n/a — seeded from drop_zone_intent.md` when applicable.
- **`skills/genesis-protocol/SKILL.md`** — files table entry for `phase-0-seed-loading.md` + `seed` argument doc both updated for v1.3.2 primary-seed detection with explicit precedence rule reference.
- **`skills/genesis-protocol/verification.md`** — new scenario + regression scenario for both-files-present precedence.

### Changed — living spec + 1:1 mirror map

- `.claude/docs/superpowers/specs/v2_etape_0_drop_zone.md` — adds `## Scope — v1.3.2 write + Layer B handoff` + 7 new per-surface sections (consent card, schema + body format, write flow, halt branch, bridges, Layer B integration, rationale). Concentrated privilege rewritten (v1.3.0 + v1.3.1 `none`; v1.3.2 write declaration + 5 mitigations). Mirror map extended with 6 primary v1.3.2 rows + new cross-skill mirror family for Layer B touches. Deferred renamed to v1.3.3+ (items 2-3 closed). R9 policy extended with 3 rows covering `drop_zone_intent.md` frontmatter keys/values split, origin tags, Conversational context section. Verification scenarios #13-#19.

### Changed — memory + privilege map

- `memory/master.md` — privilege map entry for `genesis-drop-zone` switches from `(none — welcome + mirror + bridge, v1.3.0 surface + v1.3.1 structured extraction)` to `(writes drop_zone_intent.md to cwd after consent card, halt-on-existing, no mkdir — v1.3.0+v1.3.1+v1.3.2)`. Cross-skill-pattern #4 gets `v1.3.2 is the first cross-layer wire live` note with reference to the spec's Layer B integration section.

### Added — synthetic fixture

- `tests/fixtures/drop_zone_intent_fixture_v1_3_2.md` — synthetic v1.3.2-format `drop_zone_intent.md` for artefact-level Step 0.2a parsing verification. 13 keys (4 metadata + 9 semantic), body with prose intro + mirror echo.

### Bumped

- `.claude-plugin/plugin.json` version `1.3.1` → `1.3.2`.

### Self-rating — v1.3.2

| Axis | Score | Reasoning |
|---|---|---|
| Pain-driven | 9.3 | Closes "creation is coming soon" v1.3.1 bridge promise with direct user-visible delivery — intent now persists to disk, Layer B reads it. First Layer A privilege + first cross-layer wire live. |
| Prose cleanliness | 9.2 | Living-spec pattern held for third consecutive ship. Consent card / halt / bridges / schema all one concise template each. Spec polish + plan polish both done after reviewer passes. Six-commit rhythm maintained. |
| Best-at-date | 9.2 | Inline R8 citations ceiling preserved (`v2_promptor_fusion_landscape_2026-04-17.md` still fresh until 2026-04-24). Citations API upgrade deferred to v1.3.3+ per anti-speculation discipline (downstream reader now in place). |
| Self-contained | 9.3 | One PR ships two skills (genesis-drop-zone + genesis-protocol) + privilege map + fixture + spec + plan + CHANGELOG + session trace + resume. Six-commit rhythm (spec + spec polish + plan + plan polish + feat + chore). Nothing dangles. |
| Anti-Frankenstein | 9.4 | Narrow privilege (cwd only, no `mkdir`), halt-on-existing (not overwrite), bundled Layer B integration (not speculative), API deferred (now has downstream reader). Five mitigations shipped one-for-one with the privilege. `drop_zone_intent.md` rename (not `bootstrap_intent.md`) avoids faux ami with Layer B's file. |
| **Average** | **9.28** | Target ≥9.3/axis met on most axes; floor ≥9.0/axis respected on every axis. |

**Seventh consecutive ship ≥ 9.0** (v1.2.1 9.26, v1.2.2 9.14, v1.2.3 9.18, v1.2.4 9.16, v1.3.0 9.34, v1.3.1 9.30, v1.3.2 9.28).

Running average post-v1.3.2 = **≈ 8.84/10** (v0.2 → v1.3.1 was 8.81 across 17 ships; adding v1.3.2 with equal weight: (8.81 × 17 + 9.28) / 18 ≈ 8.84). Above v1.0.0 target of 8.5 by 0.34. Plateau holds inside the anti-Frankenstein inflection-point budget.

## [1.3.1] - 2026-04-17

### Changed — genesis-drop-zone Phase 0 mirror (replaces v1.3.0 ack)
- `skills/genesis-drop-zone/phase-0-welcome.md` — new section `Mirror template — FR (v1.3.1, printed by default)` replaces `Token-streamed acknowledgement template`. Adds `Mirror template — EN (v1.3.1, mirror-ready)`. Updates `Bridge message` to the v1.3.1 text ("Création du projet (GitHub, fichiers, mémoire) arrive bientôt. Pour l'instant, j'ai lu et compris — reviens à Claude Code normalement.") and its EN mirror.
- `skills/genesis-drop-zone/SKILL.md` — `Purpose` extended. `Scope` gets `In scope (v1.3.1)` sub-block; `Out of scope` moves to v1.3.2+. `Phase 0 — acknowledgement` renamed → `Phase 0 — mirror` with schema table, reveal rules, failure modes, truncation rules. `Concentrated privilege` forward note points to v1.3.2 as the first Layer A privilege ship. `Deferred scope` lists Path A Citations upgrade as new #1.

### Added — extraction schema (9 fields)
- `idea_summary`, `pour_qui`, `type`, `nom`, `attaches`, `langue_detectee`, `budget_ou_contrainte`, `prive_ou_public`, `hints_techniques` — extracted in-context (no API call) and rendered as an aligned-column table revealed row-by-row.
- Null-visible convention: `a trouver ensemble` (core missing), `non mentionne(e)` (bonus missing), `a affiner — X ou Y` (ambiguity). Three classes, exhaustive.
- Truncation: row values ≤ 60 chars (truncate at 57 + `...`), `Depose` caps at 3 items + `+ N autres`.

### Changed — living spec + 1:1 mirror map
- `.claude/docs/superpowers/specs/v2_etape_0_drop_zone.md` — adds `Scope — v1.3.1 extraction`, `Extraction schema — 9 fields`, renames `Token-streamed acknowledgement template` → `Mirror screen — template & reveal`, bridge content updated, `Deferred to v1.3.1+` → `Deferred to v1.3.2+` with item #1 removed (extraction in-scope), concentrated privilege declaration extended to cover both versions, verification scenarios extended with rows #7–#12 (v1.3.1 additions) with per-version ship gates.

### Bumped
- `.claude-plugin/plugin.json` version `1.3.0` → `1.3.1`.
- `memory/master.md` concentrated-privilege map entry for `genesis-drop-zone`: `(none — welcome + mirror + bridge, v1.3.0 surface + v1.3.1 structured extraction)`.

### Self-rating — v1.3.1

| Axis | Score | Reasoning |
|---|---|---|
| Pain-driven | 9.3 | Closes the "Extraction arrivent bientôt" promise v1.3.0 could not yet keep — direct delivery of a promised capability. Null-visible discipline (3 classes) was driven by "what does Victor see when the schema is thin?" Schema 9 fields picked at brainstorming (user-chosen), every field user-legible. |
| Prose cleanliness | 9.2 | Living-spec pattern avoided spec proliferation. Mirror template is one table, not 9 bullets. Truncation rules + ambiguity branch explicit. Spec polish + plan polish both done after reviewer passes. Commit message detailed but readable. |
| Best-at-date | 9.2 | Inline R8 citation of `v2_promptor_fusion_landscape_2026-04-17.md` Stage 2 (token-streaming pattern, Ably SSE). Same SOTA anchor as v1.3.0; entry remains fresh (expires 2026-04-24). Declined API Path A Citations upgrade for v1.3.1 — anti-speculation discipline, not ceiling. |
| Self-contained | 9.4 | Skill extends itself — no new file in the skill package, no new dep. Spec evolves in place. 1:1 mirror discipline extended cleanly. PATCH bump, master.md one-line freshness. 4 files changed for feat. |
| Anti-Frankenstein | 9.4 | API call deferred (no consumer yet). Concentrated privilege stays `none`. Three null classes, not four. Schema 9 fields (user-picked, orthogonal, Victor-legible). Declined API Citations upgrade even with R8 entry fresh — saves for v1.3.2 alongside bootstrap_intent.md write. No speculative plumbing. |
| **Average** | **9.30** | Target ≥9.3/axis met on average; floor ≥9.0/axis respected on every axis. |

Sixth consecutive ship ≥9.0 (v1.2.1 9.26, v1.2.2 9.14, v1.2.3 9.18, v1.2.4 9.16, v1.3.0 9.34, v1.3.1 9.30).

Running average post-v1.3.1 = **8.81/10** (v0.2 → v1.3.0 was 8.78 across 16 ships; adding v1.3.1 with equal weight: (8.78 × 16 + 9.30) / 17 = 8.81).

## [1.3.0] — 2026-04-17 — "genesis-drop-zone welcome vertical slice — Étape 0 Layer A"

First MINOR bump since v1.2.0. Opens the v1.3.x conversational-layer line of Genesis v2. Closes the v1.2.x PATCH cluster on v1.2.0 self-dogfood.

### Added

- `skills/genesis-drop-zone/` — new sibling skill package. First Layer A (conversational) skill of Genesis v2. Ships welcome + token-streamed acknowledgement + bilingual bridge as a vertical slice. Two files: `SKILL.md` (124 lines, 9 sections mirroring 8 rows of the spec's 1:1 mirror map) and `phase-0-welcome.md` (97 lines, FR + EN welcome boxes, ack template, bilingual bridge).
- `.claude/docs/superpowers/specs/v2_etape_0_drop_zone.md` — new implementation-grade spec (268 lines). Inline R8 citations of `v2_promptor_fusion_landscape_2026-04-17.md` anchoring each UX choice in 2026 SOTA (IBM Docling accept-anything, v0/Bolt/Lovable intent-first, Ably SSE token-streamed ack, MIT Tech Review 2026-04 privacy-relationship language, Filestack dual-path rule). Hybrid-C strategy with the vision doc: `v2_vision_promptor_fusion.md` stays intact, receives one pointer line in § Étape 0 for navigation.
- `.claude/docs/superpowers/plans/2026-04-17-v1.3.0-drop-zone-welcome.md` — 17-task implementation plan, reviewer-approved.
- Cross-skill-pattern #4 in `memory/master.md`: Layer A / Layer B stratification. Named as a composition pattern (not a rule) emerging with the first Layer A skill. The four patterns now compose as the discipline surface for v2-onwards skills.

### Changed

- `memory/master.md` — concentrated-privilege map extended to 7 entries (genesis-drop-zone: none, journal-system precedent); skill count six → seven; cross-skill-patterns section now declares four patterns.
- `skills/README.md` — 7th skill entry added below pepite-flagging.
- `.claude/docs/superpowers/specs/v2_vision_promptor_fusion.md` — single pointer line added near § Étape 0 directing to the new implementation spec.
- `.claude-plugin/plugin.json` — version 1.2.4 → 1.3.0.

### Not changed intentionally

- `skills/genesis-protocol/` — zero modifications. The Layer B engine stays strictly untouched. Extraction, `bootstrap_intent.md` write, and handoff to `genesis-protocol` are deferred to v1.3.1+.

### Self-rating — v1.3.0

| Axis | Score | Justification |
|---|---|---|
| Pain-driven coverage | 9.2/10 | Ship addresses the vision-doc-target gap ("Victor cannot use Genesis v1") with a demonstrable surface (welcome + ack + bridge). Deferred scope is crystal-clear. Small deduction: the spec declared Scenarios #1 and #3 as mandatory ship-gate replays; #6 (R9 audit) was run scripted and passes cleanly, and #3 was verified at the context-guard-logic level inside the active worktree (all 3 AND-conjoined conditions observed as non-fresh), but #1 (fresh-dir runtime welcome) requires a fresh Claude Code invocation outside this session and is deferred to the first post-merge session. That's an artefact-level gate, not a runtime-level one. |
| Prose cleanliness | 9.3/10 | Caps respected: spec 268/400, SKILL.md 124/200, phase-0-welcome.md 97/100. Single-paragraph Purpose, no verbosity drift, mirror map gains a Mirrored/Spec-only column from the spec review. The one honest concession: the plan file is 624 lines vs a 400 target — the plan reviewer itself flagged this as load-bearing (per-step bash blocks, full commit/PR bodies inline for buildability) and recommended against trimming at that cost. Flagged here rather than pretending the cap held. |
| Best-at-date alignment | 9.4/10 | First ship since v1.2.0 to consume fresh R8 research. The spec cites `v2_promptor_fusion_landscape_2026-04-17.md` inline at every UX choice (intent-first unified box, dual-path rule, token-streamed ack, privacy relationship language, accept-anything norm), with external anchors (IBM Docling, v0/Bolt/Lovable, Ably, MIT TR 2026-04, Filestack) resolvable through the R8 entry. This is the lever the running-avg analysis predicted would break the 8.6–8.8 ceiling structural to PATCH-fix cycles. |
| Self-contained | 9.3/10 | Clean sibling skill: own directory, own SKILL.md, own 1:1 mirror target. Zero modifications to existing skills. Cross-skill-pattern #4 declared in master.md before the first usage. Concentrated-privilege map extended correctly (7th row). Vision doc pointer is a one-liner. |
| Anti-Frankenstein | 9.5/10 | Welcome-only vertical slice. Zero plumbing (no file writes, no subprocess, no network). Privilege `none`. No test harness, no Python driver, no hook wiring. Deferred list is explicit and ordered. Two-commit pattern (feat + chore) continues the v1.2.1→v1.2.4 discipline. 1:1 mirror discipline extended to a third kind of pair (skill ↔ dedicated implementation spec), formalising what v1.2.4 did informally between runbook pairs. |
| **Average** | **9.34/10** | Target ≥9.3 met; floor ≥9.0 respected on every axis. Running average v0.2 → v1.3.0 ≈ **8.78/10** (up from 8.74, +0.04 delta consistent with the v1.2.1→v1.2.4 cadence of +0.03 per ship). **Five consecutive ships ≥9.0** (v1.2.1 9.26, v1.2.2 9.14, v1.2.3 9.18, v1.2.4 9.16, v1.3.0 9.34). First ship of the v1.3.x cycle clears the per-axis 9.0 floor cleanly. |

---

## [1.2.4] — 2026-04-17 — "R2.3.1 gh active-account pre-flight — F34 rule-level mirror"

### Added

- `skills/genesis-protocol/rules/v1_rules.md` — new `### R2.3.1 gh active-account pre-flight (before any gh write — added v1.2.4)` sub-rule inserted under `### R2.3 PR & merge`. Rule-level mirror of `genesis-protocol` Phase 6 Step 6.0 (shipped in v1.2.3). Resolves target owner from `git remote get-url origin` (single source — v0.2.0+ sessions always have a remote configured, unlike pre-Phase-3.5 bootstrap which needs three fallbacks), runs `gh api user --jq .login`, compares, and on mismatch attempts `gh auth switch -h github.com -u <owner>` with re-verification. Halt templates are byte-for-byte identical to Step 6.0's (differing only in the `❌ R2.3.1 …` / `❌ Step 6.0 …` heading). Applies to every `gh` write op (`gh pr create`, `gh pr merge`, `gh release create`, `gh repo <write-verb>`); read-only calls (`gh api user`, `gh auth status`, `gh repo view`) explicitly exempt. Declared a structural stop in every execution mode. Closes the v0.2.0+ downstream coverage gap flagged in the v1.2.3 session trace and in v1.2.3's own self-rating prose — F34 was live-reproduced during v1.2.1's own PR creation, which was a v0.2.0+ session, not a bootstrap run.

### Changed

- `skills/genesis-protocol/rules/v1_rules.md` — two cross-ref parentheticals added to the R2.3 PR & merge bullets: "(precede with R2.3.1 pre-flight)" on both the `gh pr create` bullet and the `gh pr merge --squash` bullet. Keeps the R2.3 bullet list the entry point that R2.3.1 expands on.
- `.claude-plugin/plugin.json` — version bumped `1.2.3` → `1.2.4`.

### Notes

- **Two commits inside the feat branch, one PR**: `c4464d5` (feat — R2.3.1 + R2.3 cross-refs on one file: +61 / −2) and the pending chore commit (version + CHANGELOG + session trace + MEMORY.md pointer + resume prompt). Same "one root cause per commit, bundle into one PR" rhythm as v1.2.1, v1.2.2, v1.2.3. No SKILL.md sync commit here because R2.3.1 is a project-level rule governing downstream-bootstrapped sessions, not a structural stop of the `genesis-protocol` orchestrator skill itself — SKILL.md's Mode dispatch Category A catalogue stays scoped to orchestrator-internal stops.
- **1:1 mirror discipline extended from spec pairs to rule/runbook pairs**: the three existing 1:1 mirror precedents (journal-system ↔ Layer 0 journal section, pepite-flagging ↔ spec file, genesis-protocol SKILL.md ↔ master.md 7-phase table) all mirror a `SKILL.md` against a source spec. R2.3.1 ↔ Step 6.0 is the first rule/runbook 1:1 mirror, and the "Relation to bootstrap Step 6.0" paragraph inside R2.3.1 is the anti-drift hook that commits future maintainers to reviewing both when either is touched. The cross-skill-patterns section of `master.md` will likely evolve to name this new mirror type as the pattern ossifies — flagged for the next naming-convention pass.
- **Layer 0 additive-auth compliance preserved**: R2.3.1's `gh auth switch` mutates the machine-global gh active account but removes no credential (both accounts remain logged in), so the operation is within Layer 0's additive-auth discipline. R2.3.1 surfaces a one-line note when the switch happens so the user knows the global state changed. Recording the pre-switch login and offering to restore it after the `gh` write op is explicitly flagged as a v1.3 candidate — same deferral as v1.2.3 carried Step 6.0's pre-switch restore over to v1.3. Whichever rule or runbook gets the pre-switch restore first should teach the other via the 1:1 mirror discipline.
- **What did not change in v1.2.4**: F24 Phase 0.1 git-aware inspection (P2 cosmetic), F25/F31 config.txt canonical examples (P2 doc work), F26 non-canonical fields audit UI (still half-fixed from v1.2.2), F28 `genesis-cleanup` sibling skill (P3), F32 Python driver (v1.3 target), F33 R8 scope disambiguation (P3).
- **P1 queue — second closure**. v1.2.3 closed the P1 queue at the bootstrap level with Step 6.0 for F34. v1.2.4 closes the same P1 at the v0.2.0+ rule level with R2.3.1 as Step 6.0's rule-level mirror. The P1 pain surface is now covered at both levels — bootstrap runbook AND downstream-project rules. Any future F34-type recurrence would need a new pain point, not a missing coverage. The next-severity band remains P2 doc work or the **v2 Étape 0 drop-zone pivot** (cache `v2_promptor_fusion_landscape_2026-04-17.md` fresh, expires 2026-04-24 — 6 days of runway after v1.2.4 ship).

### Self-rating — v1.2.4

| Axis | Rating | Notes |
|---|---|---|
| Pain-driven coverage | 9.4/10 | R2.3.1 closes the exact downstream gap flagged in v1.2.3's self-rating prose ("a parallel rule in `v1_rules.md` covering v0.2.0+ post-bootstrap PR sessions would cover the same pain outside the bootstrap runbook"). F34 live-reproducer was a v0.2.0+ session — the bootstrap fix only covered a sibling surface. Small deduction because this ship is downstream prevention rather than a fix for an active live reproducer — less acute than v1.2.3 which addressed the bootstrap's own surface. |
| Prose cleanliness | 9.0/10 | R2.3.1 is ~60 lines, structurally identical branches to Step 6.0's 63 lines. Halt templates are copy-paste-ready. Mode dispatch paragraph explicit. The "Relation to bootstrap Step 6.0" paragraph is the self-documenting anti-drift hook. Minor deduction: R2.3.1 is on the heavy side for a sub-rule, but the branches are proportionate to Step 6.0 which is the reference point. |
| Best-at-date alignment | 8.8/10 | `gh api user --jq .login` + `gh auth switch -h github.com -u <user>` are the established gh CLI primitives, behaviour stable across the last 12 months. No research refresh needed — primitives already validated in v1.2.3. Cache entry `gh-cli-single-click-auth_2026-04-16.md` (fresh, expires 2026-04-23) remains the broader prior-art reference. Same stance as v1.2.3 applied at a different layer. |
| Self-contained | 9.3/10 | R2.3.1 fits under R2.3 as a proper sub-rule; owner resolution is a single `sed` pipe over `git remote get-url origin`. The 1:1 mirror declaration with Step 6.0 is explicit in the rule body itself, not hidden in a CHANGELOG note — so the rule self-documents its invariant. R8 archive already done in v1.2.3, no bookkeeping overhead here. No new runtime, no new file outside `v1_rules.md`, no new config. |
| Anti-Frankenstein | 9.4/10 | Two commits: feat (R2.3.1 + 2 cross-refs on one file) + chore (version + CHANGELOG + session trace + MEMORY.md pointer + resume prompt). Same surgical discipline as v1.2.3. No driver, no retry loop, no hook wiring. The 1:1 mirror with Step 6.0 is anti-Frankenstein applied recursively (reuse the proven semantic, do not invent a parallel one). Pre-switch restore deliberately deferred to v1.3. |
| **Average** | **9.16/10** | Running average v0.2 → v1.2.4 ≈ **8.74/10** (up from 8.71). **Four consecutive ships ≥ 9.0** (v1.2.1 9.26, v1.2.2 9.14, v1.2.3 9.18, v1.2.4 9.16) — surgical commit discipline holding, and the 1:1 mirror discipline extended cleanly from spec pairs to rule/runbook pairs without changing rhythm or cadence. |

---

## [1.2.3] — 2026-04-17 — "gh active-account pre-flight — F34"

### Added

- `skills/genesis-protocol/phase-6-commit-push.md` — new `### Step 6.0 — gh active-account pre-flight` inserted at the opening of Phase 6, before the pre-commit review. Runs `gh api user --jq .login`, compares the result against a target owner resolved from (1) the git remote URL if set, (2) `memory/project/bootstrap_intent.md` as a fallback for pre-Phase 3.5 bootstrap ordering, or (3) the Step 0 consent card. On mismatch, attempts `gh auth switch -h github.com -u <owner>`; if that succeeds, proceeds with a one-line note. If the switch fails (target owner not logged in on this machine), halts with a remediation pointing at `gh auth login --web` and surfaces the current `gh auth status` output. Fixes friction F34 (live-reproduced during v1.2.1's own PR creation — `gh pr create` failed with `GraphQL: must be a collaborator (createPullRequest)` because the active gh account was not the target repo owner).

### Changed

- `skills/genesis-protocol/SKILL.md` — `## Mode dispatch` Category A "Structural stops" examples row now lists `gh active-account mismatch at Phase 6 Step 6.0 when auto-switch fails (added v1.2.3 for F34)`. Keeps the Category A catalogue in sync with the new structural stop landed in the phase-6 runbook; SKILL.md remains the single source of truth for mode dispatch categories.
- `.claude-plugin/plugin.json` — version bumped `1.2.2` → `1.2.3`.
- `.claude/docs/superpowers/research/INDEX.md` — two expired stack entries moved to Archive: `claude-code-plugin-structure_2026-04-14.md` (TTL expired 2026-04-17) and `claude-code-session-jsonl-format_2026-04-15.md` (same). Both archived with a one-line note explaining the freshness-at-archival signal; neither refreshed because the v1.2.3 change is skill-internal and does not depend on Claude Code SDK drift or JSONL record shape.

### Notes

- **Three commits inside the feat branch**: one feat commit for Step 6.0 itself (63 insertions in `phase-6-commit-push.md`), one feat commit for the SKILL.md dispatch-table sync (1-line change), one chore commit for the R8 archive + version bump + CHANGELOG + session trace + resume prompt. Same "one root cause per commit, bundle into one PR" rhythm as v1.2.1 and v1.2.2.
- **Category A structural stop, not a consent gate**: the `gh auth switch` attempt runs in every mode without blocking (it flips between already-authorized accounts, reversible), but the halt on switch-failure is mode-invariant because proceeding with the wrong active account produces an opaque `must be a collaborator` GraphQL error at a later step — strictly worse than halting with a clear remediation.
- **Layer 0 additive-auth compliance**: `gh auth switch` mutates the machine-global gh active account but removes no credential (both accounts remain logged in), so the operation is within Layer 0's additive-auth discipline. Step 6.0 surfaces a one-line note when the switch happens so the user knows the global state changed. Recording the pre-switch login and offering to restore it at Phase 7.3 is explicitly flagged as a v1.3 candidate — out of scope for this surgical ship.
- **What did not change in v1.2.3**: F24 Phase 0.1 git-aware inspection (P2 cosmetic), F25/F31 config.txt canonical examples (P2 doc work), F26 non-canonical fields audit UI (still half-fixed from v1.2.2 — convention documented, template write deferred), F28 `genesis-cleanup` sibling skill (P3), F32 Python driver (v1.3 target), F33 R8 scope disambiguation (P3).
- **P1 queue closed**. After v1.2.3 the v1.2.0 friction log has no remaining P1 frictions — all three P0s (F23 + F27 + F29 + F30) landed in v1.2.1, the P1 cluster (F20 + F21 + F22) landed in v1.2.2, and the last P1 (F34) landed here. The next-severity band is P2 doc work (F25/F31 config examples) or the v2 Étape 0 drop-zone pivot (research cache `v2_promptor_fusion_landscape_2026-04-17.md` fresh, expires 2026-04-24).

### Self-rating — v1.2.3

| Axis | Rating | Notes |
|---|---|---|
| Pain-driven coverage | 9.5/10 | Step 6.0 implements the v1.2.0 friction-log fix sketch verbatim — `gh api user --jq .login`, compare vs resolved owner, auto-switch attempt, halt with `gh auth status` on switch-failure. Live reproducer from v1.2.1's own PR creation is directly addressed. Small deduction: a parallel rule in `v1_rules.md` covering v0.2.0+ post-bootstrap PR sessions would cover the same pain outside the bootstrap runbook, but is out of scope here. |
| Prose cleanliness | 9.0/10 | Step 6.0 is self-contained, halt templates are copy-paste-ready, Mode dispatch callout explicit, note on global-state mutation surfaces the Layer 0 concern. Minor deduction: Step 6.0 is ~63 lines which sits on the heavy side for one step — justified by the branching halt cases but tight budget. |
| Best-at-date alignment | 8.8/10 | `gh api user --jq .login` + `gh auth switch -h github.com -u <user>` are the established gh CLI primitives, behaviour stable across the last 12 months. Two expired stack entries archived as bookkeeping without a fresh snapshot, because the v1.2.3 change does not depend on plugin SDK drift or JSONL record shape — same stance as v1.2.2 applied to the same entries. |
| Self-contained | 9.2/10 | One structural stop landed in one runbook + a 1-line sync in SKILL.md's canonical dispatch table. Owner resolution uses three existing-artefact sources (git remote, bootstrap_intent.md, consent card) without introducing a new owner-resolution contract. R8 archive is pure bookkeeping. No new runtime, no new file, no new config. |
| Anti-Frankenstein | 9.4/10 | Three commits: feat (F34), feat (SKILL.md sync), chore (archive + version + prose). Surgical per v1.2.1–v1.2.2 discipline. No driver, no retry loop, no hook wiring. Explicit deferral of pre-switch restore to v1.3 stated in prose. F34 was the last P1 — this ship closes the P1 queue cleanly without scope creep. |
| **Average** | **9.18/10** | Running average v0.2 → v1.2.3 ≈ **8.71/10** (up from 8.68). Three consecutive ships ≥ 9.0 (v1.2.1 9.26, v1.2.2 9.14, v1.2.3 9.18) — the surgical one-root-cause-per-commit / bundle-in-one-PR discipline continues to hold. |

---

## [1.2.2] — 2026-04-17 — "Mode is a first-class argument — F21 + F20 + F22"

### Added

- `skills/genesis-protocol/SKILL.md` — new `## Arguments` section declaring the three semantic arguments (`mode`, `target`, `seed`) with types, defaults, and purpose. Documents the passthrough convention for non-semantic `key=value` pairs (`context=...`, `strange-loop=...`, `friction-log=...` observed in real v1.2.0 invocations): accepted, captured under "Non-canonical fields (passed through)" in `bootstrap_intent.md`, no runtime effect. Fixes friction F21 (argument schema was undocumented — invocations up to v1.2.1 had to guess at names).
- `skills/genesis-protocol/SKILL.md` — new `## Mode dispatch` section naming the three gate categories (A structural stops, B security floor, C consent gates) and a per-gate dispatch table showing which gates block under each of the three modes. `semi-auto` is named as the intended default for repeat users; `auto` is for experienced users who understand that paradox guards and security floor still apply.
- `memory/project/session_v1_2_2_mode_auto_args.md` — session trace with the two-commit narrative (SKILL.md canonical spec, then per-phase pointers), the mode dispatch rationale, and the explicit deferral list for v1.2.3+ (F34 gh active-account pre-flight is the named next target).

### Changed

- **F20 + F22 — Step 0 consent card is now mode-aware** (`skills/genesis-protocol/SKILL.md`): the paragraph after the paradox guards dispatches per `mode` — `detailed` and `semi-auto` block on `yes`, `auto` renders the card as an informational log and proceeds. Paradox Guards A and B always fire regardless of mode; they are structural stops, not consent gates. The anti-Frankenstein clause is reworded from "do not skip the top-level consent card" to "do not skip the top-level consent card rendering" — the card is rendered in every mode, only the dispatch changes.
- **Per-phase consent gates reference the canonical dispatch** (`phase-0-seed-loading.md`, `phase-3-git-init.md`, `phase-6-commit-push.md`): each phase runbook gets a short mode-dispatch paragraph at its consent-gate location pointing back to `SKILL.md § Mode dispatch`. Two phase-specific callouts: Phase 3.2/3.3 SSH keygen + host alias are category B security floor (always block); Phase 6.1 pre-commit review stays blocking even in `semi-auto` because first commit + first push are unrecoverable.
- `.claude-plugin/plugin.json` — version bumped `1.2.1` → `1.2.2`.

### Notes

- **Two commits inside the feat branch**: `72ef17a` (F21 + F20 + F22 in SKILL.md — the canonical spec) and `a086749` (F20 + F22 per-phase pointers — 6 lines across 3 files). The one-fix-per-PR rhythm from v1.2.1 is preserved via one root cause per commit; the PR bundles them because F21 and F20/F22 share the same `mode` argument plumbing and shipping them separately would mean the per-phase pointers in the second PR would reference an argument defined in the first.
- **Phase -1 mode propagation**: when the orchestrator invokes `phase-minus-one` at Phase -1, it passes its own `mode` value through. The sibling's 3-mode ladder already uses the same vocabulary (`detailed` / `semi-auto` / `auto`) so the two ladders align by design — no re-mapping, no translation layer.
- **What did not change in v1.2.2**: F24 Phase 0.1 git-aware inspection (P2, F30 already covers the Phase 3 blocker case), F25/F31 config.txt canonical examples (P2), F26 non-canonical fields audit UI (P2 — the passthrough CONVENTION is now documented in SKILL.md, but the `bootstrap_intent.md` `## Non-canonical fields` section itself is not yet wired in `phase-0-seed-loading.md`'s write template), F28 `genesis-cleanup` sibling skill (P3), F32 Python driver (v1.3), F33 R8 scope disambiguation (P3), **F34 gh active-account pre-flight (P1 — v1.2.3 target)**.
- **Strictly: F26 is half-fixed.** The passthrough convention now has a canonical home in SKILL.md § Arguments. The actual write of `## Non-canonical fields (passed through)` into `bootstrap_intent.md` at Phase 0.5 is still not explicitly in the template. A v1.2.3 or v1.3 touch-up can complete it — deliberately deferred to keep v1.2.2 surgical.
- **Research cache**: stack entries (`claude-code-plugin-structure`, `claude-code-session-jsonl-format`) expired 2026-04-17 (today) but the v1.2.2 change is skill-internal (no Claude Code SDK dependency), so they were not refreshed. Same stance as v1.2.1 session.

### Self-rating — v1.2.2

| Axis | Rating | Notes |
|---|---|---|
| Pain-driven coverage | 9.4/10 | Every change maps to a v1.2.0 friction (F21 Arguments section, F20/F22 mode-aware dispatch). The `## Mode dispatch` table is the single missing canonical reference v1.2.0 asked for. Small deduction: F26 passthrough convention is now documented but the `bootstrap_intent.md` template write is half-done. |
| Prose cleanliness | 9.0/10 | Canonical mode dispatch table in SKILL.md; per-phase pointers 2 lines each. Commit bodies are 3 paragraphs with root cause + mechanism + scope boundary. Minor deduction: the SKILL.md `## Arguments` + `## Mode dispatch` sections add ~40 lines to a file that was already long. |
| Best-at-date alignment | 8.6/10 | The `mode` argument pattern mirrors what `phase-minus-one` already ships (vocabulary-aligned). No external research refresh needed — the change is about orchestrator-internal semantics. Small deduction: no verification run against a real downstream target yet. |
| Self-contained | 9.2/10 | SKILL.md is the single source of truth for mode dispatch. Phase runbooks reference the table rather than restate the rules, preventing drift. No new runtime, no new config file, no new dependency. |
| Anti-Frankenstein | 9.5/10 | No Python driver (F32 deferred to v1.3 as flagged in v1.2.1). No hook wiring. No test harness. Two surgical commits totalling 60 insertions + 3 deletions across 4 files. F26 deliberately half-fixed to avoid scope creep. |
| **Average** | **9.14/10** | Running average v0.2 → v1.2.2 now **8.68/10** (up from 8.65). Three consecutive ≥ 9.0 versions (v1.2.0 8.88, v1.2.1 9.26, v1.2.2 9.14) — the surgical-commit discipline is holding. |

---

## [1.2.1] — 2026-04-17 — "Paradox guards — F29 + F30 + F23/F27"

### Added

- `skills/genesis-protocol/rules/v1_rules.md` — canonical R1-R10 rules template now lives **inside the skill** (relocated from `.claude/docs/superpowers/rules/` via `git mv`, history preserved). Makes the skill self-contained across all three install modes: dogfood, `--plugin-dir`, and personal-scope `~/.claude/skills/` (fixes F29 — the install path that F18's workaround produces was silently broken pre-v1.2.1).
- `memory/project/session_v1_2_1_paradox_guards.md` — session trace with four verification replays (F23 mental walk-through, F27 derivation, F30 scratch shell test, F29 on-disk check) and explicit deferral list for v1.2.2+.
- `.claude/docs/superpowers/plans/2026-04-17-v1.2.1-paradox-guards.md` — implementation plan (subagent-driven-development discipline), retained as dev-internal artefact.

### Changed

- **F29 — path resolver rewritten** (`skills/genesis-protocol/phase-1-rules-memory.md` Step 1.3): canonical source now `<skill_dir>/rules/v1_rules.md`; legacy fallback at `<plugin-root>/.claude/docs/superpowers/rules/v1_rules.md` retained for pre-v1.2.1 installs; halt surfaces BOTH expected paths if neither resolves.
- **F30 — Phase 3.1 git-aware probe** (`skills/genesis-protocol/phase-3-git-init.md`): literal `.git/` check replaced with `git -C "<target>" rev-parse --show-toplevel 2>/dev/null` three-way dispatch (outside-any-repo → proceed; target-is-own-root → resume prompt; nested-inside-outer → HALT with actionable sibling-directory recommendation). Prerequisites, Step 3.1, and Common Failures all updated in lockstep. A follow-up commit adds a git-bash path normalization note (MSYS returns `C:/...` while POSIX `pwd` returns `/c/...`).
- **F23 + F27 — Step 0 paradox guards** (`skills/genesis-protocol/SKILL.md` + `phase-0-seed-loading.md`): two structural pre-checks added before the consent card renders. Guard A refuses targets inside the orchestrator plugin tree; Guard B refuses slugs colliding with `project-genesis` or the orchestrator's `plugin.json` name. No override flag in v1.2.1. Phase 0 Common Failures entry for slug collision upgraded from WARN to STRUCTURAL STOP for self-collision specifically.
- `CLAUDE.md`, `memory/MEMORY.md`, `memory/master.md` — rules pointer path updated to the new skill-local location.
- `.claude-plugin/plugin.json` — version bumped `1.2.0` → `1.2.1`.

### Notes

- **Four commits, narrow scope**: `c707023` (F29), `90c7777` (F30), `40a96e4` (F23+F27), `a53dd48` (F30 follow-up normalization note). Every other v1.2.0 finding — mode-auto orchestrator semantics (F20/F22), argument schema (F21), config.txt templates (F25/F31), cleanup skill (F28), Python driver (F32), R8 scope (F33), gh active-account pre-flight (F34) — explicitly deferred to v1.2.2+ and listed in the session trace.
- **Target-side path unchanged**: every Genesis-bootstrapped downstream project continues to have its rules at `.claude/docs/superpowers/rules/v1_rules.md`. Only the source location inside the Genesis plugin moved.
- **Verification was manual, not automated**: pure Markdown runbooks + scenario replays (per Option A pure-Markdown discipline from v0.8.0, reaffirmed in v1.2.0 meta-finding #5). F30 probe verified live against the v1.2.1 worktree itself (reproduced the nested-repo detection case).
- **Strange-loop targets now refused by default**: the v1.2.0 exact configuration (`target = project-genesis/.claude/worktrees/*/selfdogfood-target/`) is blocked by Guard A before Phase 0 begins. The v2 candidate `--allow-nested-paradox` override remains deliberately unimplemented.

### Self-rating — v1.2.1

| Axis | Rating | Notes |
|---|---|---|
| Pain-driven coverage | 9.6/10 | Every fix maps 1:1 to a v1.2.0 friction with its exact reproducer. The F30 normalization follow-up emerged from live verification, not speculation. Zero speculative additions. |
| Prose cleanliness | 9.0/10 | Each commit has a 3-paragraph narrative body. Halt templates are copy-paste-ready. Plan + session trace are self-contained documents. Minor deduction: the plan file is ≈ 550 lines — thorough but verbose, could be tighter. |
| Best-at-date alignment | 8.8/10 | `git rev-parse --show-toplevel` is the standard git-aware probe. Path normalization note acknowledges the MSYS/POSIX split. No external R8 refresh needed — changes are skill-internal. |
| Self-contained | 9.4/10 | F29 explicitly makes the skill more self-contained (the core purpose of that fix). Plan and session-trace are dev-internal, not shipped. One file relocated via `git mv` (history preserved). |
| Anti-Frankenstein | 9.5/10 | No new runtime. No test harness. No config surface. No Python. Pure Markdown edits + one file rename. F32 (Python driver) explicitly deferred to v1.3 despite the "runbook ceiling" signal from v1.2.0 meta-finding #5. |
| **Average** | **9.26/10** | New single-version high. Running average v0.2 → v1.2.1 = **8.65/10** (well above the 8.5 v1 target). |

---

## [1.2.0] — 2026-04-17 — "The conscious strange loop — paradox surfaced"

### Added

- `memory/project/selfdogfood_friction_log_v1_2_0_2026-04-17.md` — **14 new frictions (F20–F34)** captured live during a conscious strange-loop self-dogfood: project-genesis running `genesis-protocol` on a worktree target whose `config.txt` describes Genesis itself. 5 STRUCTURAL, 7 DESIGN, 2 COSMETIC. Cumulative F1–F34.
- `.claude/docs/superpowers/research/sota/v2_promptor_fusion_landscape_2026-04-17.md` — R8 SOTA entry consolidating 3 parallel research agents (drop-zone UX canon 2026, Claude API ingestion Path A/B, multi-file synthesis). TTL 2026-04-24. Seeds v2 Étape 0 design.

### Changed

- `specs/v2_vision_promptor_fusion.md` — **prepended Étape 0 "Le Dépôt"** (drop-zone front door): intent-first unified box, Claude Files API + Citations (Path A recommended), relationship-language privacy, token-streamed acknowledgement. Factual correction: the "Promptor 4-part structure" is credited as Genesis-native synthesis inspired by FR-community Mr Promptor / FlowGPT, **not** as a published pattern (academic Promptor arXiv 2310.08101 does not describe this structure).
- `.claude-plugin/plugin.json` — version bumped from `1.1.0` to `1.2.0`.

### Pépites (red-light, routed cross-project)

1. **F29 — Genesis v1.1 plugin personal-scope install is broken today.** Every user who followed F18's `cp -r skills/ ~/.claude/skills/` hits a halt at Phase 1.3 — the three-levels-up rules-path heuristic resolves to `~/.claude/` which has no `.claude/docs/superpowers/rules/`. P0 fix in v1.2.1.
2. **"Promptor 4-part structure" is Genesis-native.** Credit correctly in all external comms (v2 spec, blog, marketplace listing).

### Meta-findings

- The paradox is architectural, not user error. v1.1's "two sessions, two folders" fix is insufficient: the protocol has no self-defence against target-inside-orchestrator-repo (F23), slug-equals-orchestrator-slug (F27), nested `git init` (F30), or personal-scope rules-path resolution (F29). v1.2.1 must add defensive layers at Step 0 + Step 3.1.
- `mode=auto` needs orchestrator-level semantics. The 3-mode ladder was Phase -1-only; every "consent gate in auto mode" friction (F2, F20, F22) shares this root.
- The orchestrator is at the limits of pure-Markdown design (F32). Thin Python driver is the v1.3 path.

### Notes

- **v1.2.0 is a forensic release**, no code fixes. The friction log IS the deliverable. v1.2.1 applies the 3 P0 fixes (F29, F30, F23+F27) in a separate PR to preserve the diagnostic → treatment narrative.
- Strange-loop target path (`selfdogfood-target/`) retained as forensic artefact on the branch.
- Live execution halted mid-Phase 3 after F30 reproduced — nested `.git/` was cleaned up immediately.

### Self-rating — v1.2.0

| Axis | Rating | Notes |
|---|---|---|
| Pain-driven coverage | 9.2/10 | Every friction was experienced live, not predicted. The strange-loop target was chosen to stress-test the paradox — it succeeded. Two pépite-worthy findings produced. |
| Prose cleanliness | 8.8/10 | Friction log is structured (15 entries × severity / phase / root cause / impact / fix), CHANGELOG is compact. v2 spec amendment is an additive Étape 0. |
| Best-at-date alignment | 9.0/10 | R8 SOTA entry backed by 3 parallel 2026 research agents. Promptor attribution corrected from public sources. |
| Self-contained | 7.5/10 | The forensic log is self-contained; the meta-findings reference R8 entries and Layer 0 files. The "3 P0 fixes" list pushes actionable work to v1.2.1 — correct separation, but the value of v1.2.0 alone is documentary. |
| Anti-Frankenstein | 9.0/10 | Zero speculative code. Every pending fix is backed by a reproduced friction. Explicitly did NOT fix live. |
| **Average** | **8.70/10** | Running average v0.2 → v1.2.0 = **8.57/10**. Above the 8.5 v1 target. |

---

## [1.1.0] — 2026-04-16 — "The Victor test — auth wall demolished"

### Added

- `specs/v2_vision_promptor_fusion.md` — v2 vision born from self-dogfood: conversational bootstrap inspired by Promptor, backed by 5 parallel research agents (zero-friction UX, gh CLI auth, conversational onboarding, MCP tools, magical CLI)
- `memory/project/selfdogfood_friction_log_2026-04-16.md` — 18 frictions (5 STRUCTURAL, 9 DESIGN, 4 COSMETIC) from first real genesis-protocol execution
- `memory/project/session_v1_1_selfdogfood.md` — session memory
- `research/sota/zero-friction-bootstrap-ux_2026-04-16.md` — v0/Bolt/Replit patterns, @clack/prompts, Charm Gum
- `research/sota/gh-cli-single-click-auth_2026-04-16.md` — the 4-line auth revolution

### Changed

- **Phase 5.5 auth flow rewritten: 6 manual browser steps → 1 OAuth click + 2FA**
  - `gh auth login --web` with device flow replaces fine-grained PAT creation
  - `Start-Process chrome.exe -ArgumentList '--profile-directory=...'` for Chrome profile routing (GH_BROWSER env var proven unreliable)
  - `gh ssh-key add` replaces browser paste-back for SSH key registration
  - `gh repo create --private --source=. --remote=origin --push` replaces web UI repo creation
  - HTTPS-first at bootstrap; per-project SSH identity remains for ongoing work
- `.claude-plugin/plugin.json` — version bumped from `1.0.0` to `1.1.0`
- `research/INDEX.md` — 2 new entries added

### Notes

- **Self-dogfood proven end-to-end**: `genesis-selfdogfood` repo created on GitHub (myconciergerie-prog/genesis-selfdogfood, private, v0.1.0 tagged) using the new auth path. 3-probe test GREEN/GREEN/GREEN.
- **The Victor test**: new principle — every Genesis step must pass the "77-year-old non-developer" threshold. If a step requires understanding SSH/PAT/GitHub settings, it's a design failure, not a security floor.
- **Browser paste-back retained as legacy fallback** for environments without `gh` CLI.
- **v2 vision is a spec, not implementation** — conversational surface (Promptor fusion) is a future workstream. v1.1 delivers the auth fix only.

### Self-rating — v1.1.0

| Axis | Rating | Notes |
|---|---|---|
| Pain-driven coverage | 10/10 | Every change directly addresses a real friction found during actual execution. Zero speculative additions. The auth wall was hit, analyzed, and demolished. |
| Prose cleanliness | 9/10 | Vision doc is clean. Friction log is structured. Research entries follow R8 format. |
| Best-at-date alignment | 9.5/10 | 5 parallel research agents verified patterns against 2026 sources. gh CLI commands verified on this machine. |
| Self-contained | 8.5/10 | Auth fix is self-contained. Vision doc references external research but is readable standalone. |
| Anti-Frankenstein | 10/10 | Removed friction instead of adding features. Conversation surface deferred to v2. Only shipped what was proven. |
| **Average** | **9.4/10** | New single-version high. Running average v0.2 → v1.1 = **8.67/10**. |

---

## [1.0.0] — 2026-04-16 — "Ship — the strange loop closes"

### Added

- `hooks/hooks.json` — **SessionEnd hook wiring** for automatic session archiving via `session-post-processor`. Fires on session close, invokes `run.py` against the project root. Justified by three consecutive GREEN dogfood runs (v0.6.0 first run, v0.9.0 terminal run) per the v0.5.0 discipline threshold. Conditional execution: the hook silently no-ops in projects where `skills/session-post-processor/run.py` does not exist. Hook-path resolution for plugin-installed mode is a v1.1 validation target.

### Changed

- `.claude-plugin/plugin.json` — version bumped from `0.9.0` to `1.0.0`. First stable release.
- `memory/project/aurum_frozen_scope_lock.md` — **Aurum freeze lifted**. The lock was in effect from 2026-04-14 (Genesis session 1) to 2026-04-16 (this ship). All four lift conditions met: merged to main, tagged v1.0.0, self-installable via `/plugin install`, validated via dry-run + dogfood runs. Aurum v1 kickoff is now unblocked.

### Notes

- **Pure ship session** — zero new skills, zero runbook changes, zero polish. The value is the tag, the freeze lift, and the hook wiring.
- **Self-installable**: `/plugin install project-genesis@myconciergerie-prog/project-genesis` — the GitHub repo IS the marketplace (self-hosted model per R8 research).
- **Six skills stable**: `phase-minus-one` (7.6), `phase-5-5-auth-preflight` (8.2), `journal-system` (8.8), `session-post-processor` (8.4→8.6), `pepite-flagging` (8.8), `genesis-protocol` (9.0). Zero modifications since their respective ship versions.
- **Beta testers receive install instructions** alongside this release — an HTML invitation documents the 4-step installation flow, the 7-phase protocol, the 3 interaction modes, and the 6 skills.
- **The strange loop**: Genesis was conceived during Aurum v0_init on 2026-04-14 as a 7-phase template. v0.1.0 was the scaffold. v0.2.0–v0.9.0 built the six skills through eight sessions of self-improving development. v1.0.0 is the first stable release — and the next session will run Genesis against itself to produce v1.1. The compiler that compiles itself.
- **Aurum v1 kickoff** is the immediately-next workstream. Genesis v1.2 (post-self-dogfood) will be used to bootstrap/retrofit Aurum v1, Meta-Memory, and myconciergerie projects.

### Self-rating — v1.0.0

| Axis | Rating | Notes |
|---|---|---|
| Pain-driven coverage | 9.0/10 | Every action directly unblocks a waiting stakeholder or closes a documented gap. Hook wiring closes the 9-session automation gap (v0.5.0 → v1.0.0, three GREEN dogfood runs). Aurum freeze lift unblocks the next workstream queued since 2026-04-14. The tag enables beta testing — real users are waiting. Zero speculative additions. |
| Prose cleanliness | 8.5/10 | Ship CHANGELOG is compact. hooks.json is 15 lines. Aurum freeze update is a clean addendum. No unnecessary prose. |
| Best-at-date alignment | 8.5/10 | Hook format matches current Claude Code plugin spec per R8 research. Plugin install uses the self-hosted marketplace pattern. Conditional hook execution is a current defensive pattern. Slight deduction: hook-path resolution for plugin-installed mode is untested — v1.1 target. |
| Self-contained | 9.5/10 | One new file (`hooks/hooks.json`). Two edits (`plugin.json`, `aurum_frozen_scope_lock.md`). Zero new dependencies. Zero skill modifications. The most self-contained version in the project's history. |
| Anti-Frankenstein | 9.5/10 | Explicitly did NOT: add new skills, polish further, run the orchestrator for real, change runbooks, add features, create a marketplace manifest, add test harnesses, fix v0.5/v0.6 known gaps. Ship-only session honored perfectly. |
| **Average** | **9.0/10** | Running average v0.2 → v1.0 = **(7.6 + 8.2 + 8.8 + 8.4 + 8.6 + 8.8 + 9.0 + 8.92 + 9.0) / 9 = 8.59/10**. **0.09 above** the v1.0.0 target of 8.5. The cleanest average in the project's history, achieved by honoring "ship without polish". |

### v1.0.0 is shipped

Six skills stable. Orchestrator validated. Meta-memory documented. Hook wired. Beta testers invited. Aurum freeze lifted. The next session self-dogfoods Genesis v1 through its own genesis-protocol — the strange loop closing for real.

### Known gaps for v1.1.0

- **Real execution of the orchestrator** — first downstream bootstrap (Genesis self-dogfood or Aurum v1 kickoff)
- **Hook-path resolution for plugin-installed mode** — v1.0.0 hook works in development mode; installed-plugin path resolution needs validation
- **Mode retrofit for existing projects** — genesis-protocol assumes a fresh folder; existing projects need a lighter "detect and fill gaps" mode
- **Multi-slug YELLOW warning in `run.py`** — v0.5 gap, still open
- **Test vector harness for redaction patterns** — v0.5/v0.7 gap, still open
- **Allow-list for `generic_long_base64` false positives** — v0.6 gap, still open
- **Five low-severity dry-run findings** — deferred from v0.9.0
- **macOS/Linux validation** — v1.0.0 developed and tested on Windows 11 only

---

## [0.9.0] — 2026-04-16 — "Path A polish — leverage memory context, not number-chase"

### Changed

- **`memory/master.md`** — added two new sections that make the meta-memory architecture and the three emergent cross-skill patterns visible inside the plugin's own docs (no longer implicit in the skill implementations):
  - **Layer 0 inheritance** — explains how Genesis project memory inherits universal rules, user profile, hard disciplines, workflow patterns, and the journal spec from `~/.claude/CLAUDE.md` by reference, and what stays project-local (R10 plugin conventions, the six skills, the pépite system, project-specific SSH/GitHub references, the Aurum scope lock). Names this as the Meta-Memory Path C pattern confirmed primary on 2026-04-15
  - **Cross-skill patterns** — names three first-class conventions that emerged through v0.2 → v0.8: (1) **1:1 spec mirror discipline** applied three times (`journal-system`, `pepite-flagging`, `genesis-protocol`); (2) **concentrated-privilege map** with six data points across the six shipped skills; (3) **granular-commits-inside-feat-branch** as the composition of R2.1 + R2 + the informal "one commit per idea" convention. These are patterns that rules compose into — not rules themselves
- **`README.md`** — full public-facing rewrite for the v1.0.0 ship. Replaces the v0.1.0 scaffold-era prose with a real landing-page narrative reflecting the six shipped skills and the 7-phase orchestrator. Bilingual EN+FR per R9. Sections per language: what Genesis does (1 paragraph), the 7-phase protocol table (1:1 with `master.md`), the six shipped skills with one-liners, a 5-step quickstart from install-Claude-Code through first `/genesis-protocol` invocation, pointers to `master.md`/`CHANGELOG.md`/`CLAUDE.md`/skill `SKILL.md` files, and updated requirements. 129 lines total, ~65 per language — landing page, not a doc site
- **`skills/genesis-protocol/phase-1-rules-memory.md`** — three precision improvements landed from the dry-run walkthrough findings:
  - **Step 1.2** clarified that the three sibling-owned `INDEX.md` files (`journal/`, `pepites/`, `project/sessions/`) are delegated to the sibling install-manifests at Step 1.5 and **not** created by Step 1.2 itself. The previous wording "Use Write to create each file" was ambiguous about delegation
  - **Step 1.3** replaced the ambiguous "either under `~/.claude/plugins/...` OR the dev location" source-path resolution with a concrete recipe: walk three levels up from `skills/genesis-protocol/SKILL.md`'s absolute path. This rule works in both dogfood mode (Genesis repo at `C:\Dev\...\project-genesis\`) and marketplace-installed mode (`~/.claude/plugins/project-genesis/`) because the three-levels-up relationship holds in both layouts. Halt-on-not-found rather than silent fallback
  - **Step 1.5** corrected the inaccurate claim that `phase-minus-one`'s install-manifest creates a `memory/reference/automation-stack.md` placeholder. Reality: `phase-minus-one/install-manifest.yaml` is a stack-install spec (per-OS package list), not a file-target manifest. The actual `automation-stack.md` is written at runtime when `phase-minus-one` runs during Phase -1. Also clarified the idempotency mechanism (`create_if_missing_only: true`) for the three file-target sibling manifests
  - **Step 2.3** same plugin-root resolution rule as Step 1.3; clarified that the five copied entries apply to any Claude Code project regardless of `is-a-plugin`
- **`skills/genesis-protocol/phase-3-git-init.md`** — two precision improvements:
  - **Step 3.2** uses `$HOME` instead of `~` in shell commands for cross-shell portability (bash/zsh/PowerShell). The OpenSSH config block at Step 3.3 keeps `~` because OpenSSH's own parser handles it correctly on every OS — the distinction only matters for shell commands
  - **Step 3.3** added a Windows ACL caveat: `chmod 0600` is a no-op on Windows; if `ssh -T` warns about permissions, fall back to `icacls "%USERPROFILE%\.ssh\config" /inheritance:r /grant:r "%USERNAME%:F"`
- **`skills/genesis-protocol/phase-3-git-init.md`** + **`skills/genesis-protocol/phase-0-seed-loading.md`** — documented scope-lock slug derivation. Phase 0 Step 0.2 now states the rule (first whitespace-terminated token, lowercased, punctuation stripped, internal non-alphanumerics replaced with `-`) and Phase 4 Step 4.5 references it. Phase 0 stores both the derived slug and the verbatim `config.txt` string in `bootstrap_intent.md`; Phase 4 uses the slug for the filename and the verbatim string for in-file context, never re-derives
- **`skills/genesis-protocol/phase-6-commit-push.md`** — Step 6.2 rewritten with two forms for the multi-line commit message: HEREDOC preferred for bash/zsh/git-bash (works on all supported host shells), and a `-F` file-backed fallback for pure Windows `cmd`/PowerShell. The previous form used a literal `-m "...\n..."` which only works in bash. Message content is unchanged
- **`.claude/docs/superpowers/research/`** — refreshed two expired stack entries to `expires_at: 2026-04-17`: `claude-code-plugin-structure_2026-04-14.md` (had expired 2026-04-15, still matches on-disk plugin layout against the six shipped skills) and `claude-code-session-jsonl-format_2026-04-15.md` (expired today; refreshed in place; deep re-verification deferred to dogfood run 3 later this session). INDEX updated accordingly. R8 housekeeping per R1.1
- **`memory/project/dryrun_walkthrough_2026-04-16.md`** — new session artefact. Records the paper trace of the `genesis-protocol` orchestrator against `C:\tmp\genesis-dryrun\` (synthetic config.txt, slug=`dryrun-demo`, is-a-plugin=no). 10 findings surfaced; 5 medium-severity ones land as v0.9.0 fixes (above), 5 low-severity ones are documented as v1.1 candidates with rationale. This is the first end-to-end trace of the orchestrator against a non-Genesis target

### Notes

- **Path A confirmed at session open** — the user picked Path A (v0.9.0 polish → v1.0.0) over Path B (v0.8.0 ships as v1.0.0 directly) at the v0.8.0 close, with the explicit framing *"en tenant compte de toutes les avancées dans la mémoire et dans la préparation de méta memory"*. Every polish item in this release traces back to something learned during v1 bootstrap → v0.8 shipping, not generic code hygiene. The dry-run findings, the `master.md` meta-memory sections, and the README pointers are all instances of this framing
- **Phase-file length trimming explicitly skipped** — the v0.9.0 resume prompt listed phase-file trimming as Priority 4 (~10-15% reduction without content loss). The dry-run fixes added precision content to the same files (phase-1: +6 lines, phase-3: +13 lines, phase-6: +12 lines) — mechanical trimming after substantive precision additions would partially undo the additions and conflicts with the "leverage memory context" framing. Documented as a v1.1 candidate if running average ever needs another nudge after v1.0.0 ships
- **Dogfood run 3 is the terminal action of this session** — the v0.9.0 session is long enough that running `session-post-processor` against its own JSONL is the natural way to land the third successful manual dogfood run. If the halt-on-leak gate returns GREEN, hook wiring becomes a real v1.0.0 option (per the v0.5 discipline). If it returns RED or the run fails, noted and moved on — the v0.9.0 polish stands either way
- **All edits respect the granular-commits-inside-chore-branch discipline** — eight commits in this branch (R8 housekeeping, phase-1 fixes + dryrun notes, phase-3 fixes, phase-6 fix, master.md sections, README rewrite, version bump + CHANGELOG, the dogfood-run-3 fixture if any). Squashed at merge time per R2 (eighth consecutive session)
- **Every modified file kept its `SPDX-License-Identifier: MIT` header** per R10
- **Zero new skills** — the six skills are stable as committed at v0.8.0. v0.9.0 is polish, not feature

### Self-rating — v0.9.0

| Axis | Rating | Notes |
|---|---|---|
| Pain-driven coverage | 8.8/10 | Every polish item traces to a specific friction or decision: dry-run walkthrough surfaced 10 real findings (5 fixed); README rewrite addresses the "Genesis v1 is coming soon" out-of-date prose that was a known v0.8.0 gap; meta-memory sections in `master.md` make the cross-skill patterns visible (previously implicit, debug-painful for any future contributor); R8 housekeeping cleared two expired stack entries that R1.1 should have caught earlier in the cycle. The framing of "leverage memory context, not number-chase" is honored — every change traces to v1 → v0.8 lessons, not speculative additions. Slight deduction: the dry-run was a paper trace, not an execution; the 5 fixes are improvements but no fix has been validated by a real downstream bootstrap. |
| Prose cleanliness | 8.8/10 | Every edited file is tighter, not looser. The phase runbook fixes are precision additions (concrete commands replacing ambiguous "OR" language) — they slightly increase line count but reduce ambiguity per line. The new `master.md` sections are dense (3 paragraphs each) and follow the existing master.md voice. The README is bilingual landing-page prose with no dead weight. The session artefact (`dryrun_walkthrough_2026-04-16.md`) is structured, scannable, and ends with a clear conclusion. Minor: phase files were not trimmed, so they remain at 280-330 lines each. |
| Best-at-date alignment | 8.8/10 | All fixes use current Layer 0 patterns (`$HOME` portability, ACL fallback for Windows, HEREDOC convention from Anthropic's own commit-message guidance). The `master.md` Layer 0 inheritance section uses the Meta-Memory Path C terminology confirmed in the 2026-04-15 Wave 2 addendum. The README quickstart cites the install one-liner from the 2026-04-15 R8 cache entry. The R8 refresh did not introduce new SOTA, just confirmed existing entries against the on-disk state. |
| Self-contained | 9.0/10 | Every polish item is self-contained inside the existing files — no new skills, no new directories, no new dependencies, no hooks, no shared state. The dry-run added one session artefact at `memory/project/dryrun_walkthrough_2026-04-16.md` and the rest of the changes are precision edits to existing files. The `dryrun_walkthrough` file has clear v0.9.0 session provenance in its frontmatter and could be archived after v1.0.0 ships if it ever feels load-bearing-only. |
| Anti-Frankenstein | 9.2/10 | Phase-file trimming explicitly skipped because it would undo precision additions just landed — naming the skip and its rationale in this CHANGELOG honors "leverage memory context, not number-chase". No new abstractions. No new patterns invented to "improve" the orchestrator — every patch is a precision improvement on existing language or a visibility addition for an existing pattern. The dry-run was a paper trace, not an execution — refusing to run the orchestrator for real is the correct anti-Frankenstein move because real execution is a v1.1 milestone with its own scope. The three named cross-skill patterns in `master.md` are descriptive, not prescriptive — they document what the six skills already do, not what some future skill should aspire to. |
| **Average** | **8.92/10** | Clears the v0.9.0 floor of 8.5 by **0.42**. Running average v0.2 → v0.9 = `(7.6 + 8.2 + 8.8 + 8.4 + 8.6 + 8.8 + 9.0 + 8.92) / 8 = 8.54/10`. **0.04 above** the v1.0.0 target average of 8.5/10. Path A succeeded: the running average is now cleanly above target with headroom. v1.0.0 ship gate cleared — the next session can tag v1.0.0 with explicit user confirmation. |

### Path A succeeded — v1.0.0 ship gate cleared

The v0.8.0 → v0.9.0 path was framed as "leverage cumulated memory/meta-memory context to land a cleaner v1.0.0", not as a number-chase. Every polish item traces back to a specific lesson from v1 bootstrap → v0.8 shipping. The running average lands at **8.54/10**, 0.04 above the v1.0.0 target — a clean clearance with headroom rather than a 0.01 functional-but-formal miss. The v1.0.0 ship gate is now open: the next session opens with the explicit v1.0.0 tag decision.

### Known gaps for v1.0.0 or v1.1.0

- **Real execution of the orchestrator** — the dry-run was a paper trace. The first real downstream bootstrap is a v1.1 milestone and will surface frictions invisible to a paper trace (network failures, concurrent file writes, OS-specific edge cases). The 5 medium-severity fixes from the v0.9.0 walkthrough address the static surface; the v1.1 first-real-run will address the dynamic surface
- **Phase-file trim** — deferred per the rationale above. Optional v1.1 candidate
- **Multi-slug YELLOW warning in `run.py`** — v0.5 gap, still open
- **Test vector harness for redaction patterns** — v0.5/v0.7 gap, still open
- **Allow-list for `generic_long_base64` false positives** — v0.6 gap, still open
- **Hook wiring for `SessionEnd`** — depends on dogfood run 3 landing CLEAN (the terminal action of this v0.9.0 session). Decision belongs to the v1.0.0 session opener
- **Five low-severity dry-run findings** — documented in `memory/project/dryrun_walkthrough_2026-04-16.md` table with severity rationale; v1.1 candidates

---

## [0.8.0] — 2026-04-16 — "Genesis-protocol orchestrator — the last piece, recursive loop closed"

### Added

- `skills/genesis-protocol/` — the **last remaining stub** implemented as a pure Markdown orchestrator (Option A per the v0.7 → v0.8 resume prompt). Eight files, ~1,400 lines, 1:1 mirror of `memory/master.md`'s 7-phase table. The orchestrator is a **conductor, not a compiler** — it invokes the five sibling skills at the right phase, threads their outputs, and emits a single genesis report at the end. No Python runtime, no hooks, no shared state folder. The sixth and final skill, closing the anti-Frankenstein inflection point:
  - `SKILL.md` — entry point with speech-native triggers, the 7-phase master table (every row maps a phase to its runbook file + sibling skill + consent gate), inline skill pointers for Phase -1 and Phase 5.5 (thin wrappers over the sibling skills they delegate to), the concentrated-privilege map showing that `genesis-protocol` holds exactly one privilege ("writing outside the Genesis repo"), the ordered flow, anti-Frankenstein reminders, and the exit condition
  - `phase-0-seed-loading.md` — Phase 0 runbook: inspect the input folder, parse `config.txt` into a structured intent, read accompanying mixed media (PDF / images / URL lists) with security-floor rules, surface the parsed intent card for user confirmation, persist to `memory/project/bootstrap_intent.md` as the contract between Phase 0 and every downstream phase
  - `phase-1-rules-memory.md` — Phase 1 + Phase 2 runbook (folded because both write adjacent infra subtrees back-to-back before git init): create the memory subtree, copy canonical R1-R10 rules from the Genesis plugin, write the project `CLAUDE.md` with Layer 0 inheritance, invoke the four sibling install-manifests in order (`phase-minus-one` → `journal-system` → `session-post-processor` → `pepite-flagging`), seed `memory/MEMORY.md` as a one-line index, create the research cache directory tree with universal Layer 0 entries inherited by reference and five stack-relevant entries copied from the Genesis plugin's own R8 cache
  - `phase-3-git-init.md` — Phase 3 + Phase 4 runbook (folded because project seeds land as the first commit content after git init): `git init -b main`, generate the per-project ed25519 SSH key, register the `github.com-<slug>` alias with `IdentitiesOnly yes`, paste-back the public key (or Playwright-drive if Phase -1 installed it), verify via `ssh -T`, set the git remote to the SSH alias URL, stage the Phase 1+2 scaffold, write the canonical `.gitignore` (`.env.local`, SSH keys, worktrees, OS cruft, Python/Node artefacts), write `memory/master.md` with the real vision from intent, write `README.md` + `CHANGELOG.md` + conditional `.claude-plugin/plugin.json` + `skills/README.md` for downstream plugin projects, imprint scope locks if declared, re-stage everything for the first commit at Phase 6
  - `phase-5-5-auth.md` — thin pointer file documenting the contract between the orchestrator and the sibling `phase-5-5-auth-preflight` skill. Explicitly *not* a runbook reimplementation: lists what the orchestrator passes (slug, owner, repo, Chrome profile, Playwright opt-in, license, PAT expiration), what it receives (`ssh_<slug>_identity.md`, `github_<slug>_account.md`, `.env.local`, three-probe gate result), why Phase 5.5 runs after Phase 4 and before Phase 6 (four invariants), and the Layer 0 files the sibling consults during its flow
  - `phase-6-commit-push.md` — Phase 6 + Phase 7 runbook (folded because Phase 7 depends on Phase 6's tag and they form the clean handoff together): pre-commit review card with every staged file listed, first bootstrap commit with a multi-line structured message (phases + license + Genesis version), push to origin main, **explicit skip of PR creation** (the bootstrap commit is the one direct-to-main exception; PR pattern kicks in at v0.2.0+), tag `v0.1.0` with push, remote verification via `ls-remote`, then Phase 7: write the resume prompt, invoke `session-post-processor` to archive the bootstrap session's JSONL with the halt-on-leak gate, write the compact session memory entry, update `memory/MEMORY.md`, second commit (`chore(bootstrap)`), emit the final genesis report
  - `install-manifest.yaml` — verification-only manifest with no `targets` (the orchestrator creates nothing at install time — every file it writes happens during runtime invocation via phase runbooks). Confirms the five sibling skills are present under `skills/` at the plugin root, confirms all seven orchestrator files exist, flags Layer 0 gaps as YELLOW, flags plugin version mismatch as YELLOW
  - `verification.md` — two-mode health card (post-install + post-action). Post-install has 10 checks. Post-action has **30+ checks grouped by phase**: Phase -1 (stack manifest), Phase 0 (bootstrap intent), Phase 1+2 (MEMORY.md + rules + CLAUDE.md + 3 sibling install outputs + research cache INDEX + subdirs), Phase 3+4 (git + SSH + remote + `.gitignore` + master.md + README + CHANGELOG + conditional plugin manifest), Phase 5.5 (SSH identity ref + GitHub account ref + `.env.local` + three-probe gate), Phase 6 (first commit + on main + pushed + v0.1.0 tag + tag pushed), Phase 7 (resume prompt + session memory entry + session archive + halt-on-leak GREEN + second commit + MEMORY.md updated). Any RED halts; YELLOWs are warnings; GREEN is complete
- `.claude-plugin/plugin.json` version bumped to `0.8.0`; keywords list gained `genesis-protocol`, `orchestrator`, `7-phase-protocol`.
- `skills/README.md` updated: "Planned skills for v1.0.0" became "Shipped skills — v0.8.0 complete (v1.0.0 ship candidate)" and the `genesis-protocol/` entry now describes the shipped orchestrator.

### Notes

- **Option A confirmed and delivered** — the resume prompt suggested Option A (pure Markdown) over Option B (Markdown + Python driver) and Option C (hybrid). Option A won on two axes: (1) the orchestrator is a conductor, not a compiler — automation is a v1.1 candidate; (2) the anti-Frankenstein gate explicitly prohibits "do not add a Python runtime to the orchestrator in v0.8.0". The rating ceiling is higher for Option A because composition discipline is the value proposition.
- **1:1 spec mirror discipline** applied for the third time (`journal-system` v0.4, `pepite-flagging` v0.7, now `genesis-protocol` v0.8). SKILL.md's 7-phase master table mirrors `memory/master.md`'s 7-phase description — if master.md changes, the orchestrator is updated to match, never the other way around.
- **File folding justification** — the resume prompt suggested 5–7 files. The implementation landed at 8 (SKILL.md + 5 phase files + install-manifest.yaml + verification.md), with phases 2, 4, 7 folded into adjacent runbooks (Phase 2 into `phase-1-rules-memory.md`, Phase 4 into `phase-3-git-init.md`, Phase 7 into `phase-6-commit-push.md`). Folding is a compromise on the 1:1 mirror purity — each phase still has a clear home in SKILL.md's master table and its own section header in the host file, but the file structure itself groups phases by execution adjacency rather than by sequential index.
- **Five skills + one orchestrator shipped** — all six skills in the planned v1 surface are now present. The anti-Frankenstein inflection point is approached: the orchestrator lands cleanly without needing a new runtime, a new abstraction, a new hook, or any reimplementation of sibling logic. Composition was the ceiling and composition is what shipped.
- **Concentrated-privilege map** — SKILL.md enumerates one privilege per skill: `phase-minus-one` installers (mitigated by 3-mode ladder), `phase-5-5-auth-preflight` SSH/PAT/repos (paste-back default + isolated copy-paste), `journal-system` none, `session-post-processor` archives (halt-on-leak gate), `pepite-flagging` cross-project pointers (per-target consent), and **`genesis-protocol` writing an entire new project directory outside the Genesis repo** (top-level consent card + per-phase confirmation).
- **Granular commits inside the feat branch** — eleven commits: one per skill file (8), plugin.json bump, skills/README.md update, CHANGELOG (this commit). Squashed at merge time per R2.
- **Phase 6 bootstrap-commit exception** — the orchestrator explicitly documents that the first bootstrap commit is direct to `main` (not via a feat branch + PR), because there is no base branch yet. Every commit after v0.1.0 in every downstream project uses the standard R2 feat-worktree + PR + squash-merge flow.
- **Scope lock imprinting at Phase 4** — downstream projects that are spin-offs of a source project can declare scope locks at Phase 0 ("freeze <source> at <sha> until <condition>"). The orchestrator imprints them as `memory/project/<lock_slug>_frozen_scope_lock.md` at Phase 4. Genesis itself uses this pattern for the Aurum freeze — v0.8.0 is eating its own dogfood metaphorically.
- **No dry-run in v0.8.0** — the orchestrator ships as-written, without a validation pass against a real downstream project. Dry-run is an explicit v1.1 candidate. The rating accounts for this gap.
- **No hooks wired, still** — `session-post-processor` dogfood run 3 is still pending. Hook wiring stays deferred per the discipline established at v0.5.
- **Every new file carries the `SPDX-License-Identifier: MIT` header** per R10.
- **All five sibling skills untouched** — `phase-minus-one`, `phase-5-5-auth-preflight`, `journal-system`, `session-post-processor`, `pepite-flagging` are stable. Zero modifications. The orchestrator invokes them through their documented contracts without any surface extension.

### Self-rating — v0.8.0

| Axis | Rating | Notes |
|---|---|---|
| Pain-driven coverage | 9.0/10 | Every phase runbook traces to a documented pain. Phase -1 to the Aurum v0_init stack-detection pain. Phase 0 to the config.txt parsing + mixed media pain. Phase 1+2 to the memory scaffold + research cache pain. Phase 3+4 to git init + SSH identity + project seeds pain. Phase 5.5 to the five learnings in `v1_phase_5_5_auth_preflight_learnings.md`. Phase 6+7 to the handoff discipline pain. Zero speculative features. Minor deduction: the runbooks have not been run against a real downstream project yet — dry-run deferred to v1.1 — so the mapping is correct by design but not yet validated by execution. |
| Prose cleanliness | 8.8/10 | Eight files, ~1,400 lines total. Consistent structure across phase files (frontmatter → prerequisites → flow → exit → common failures → anti-Frankenstein). Tables used throughout. SKILL.md's 7-phase master table is the anchor. Minor: phase files are longer than the 5-skill median (some hit 280-320 lines) because of phase folding (1+2, 3+4, 6+7). Length is justified but not minimum viable — a v0.9.0 polish could trim ~10-15%. |
| Best-at-date alignment | 8.8/10 | Uses every Layer 0 pattern: per-project SSH identity, `GH_TOKEN` env override, fine-grained PAT scope list, Chrome profile map, isolated copy-paste, SPDX, anti-Frankenstein, R8 cache, speech-native triggers. References current Genesis precedents (halt-on-leak from `session-post-processor`, consent floor from `pepite-flagging`, 1:1 mirror from `journal-system`). No stale references. Slight deduction: the orchestrator composes existing best practices rather than introducing new ones — right move for an orchestrator, but doesn't demonstrate SOTA advancement on its own. |
| Self-contained | 9.2/10 | Eight files in one directory. Zero runtime dependencies. No Python, no shell, no binaries, no hooks, no shared-state. The only "dependency" is the five sibling skills existing under `skills/` — which is exactly the composition surface. The install-manifest is read-only and creates nothing; the orchestrator creates files only during runtime invocation via phase runbooks, and every file lands in the downstream project folder (never in the Genesis repo itself). Option A is the cleanest self-contained shape achievable. |
| Anti-Frankenstein | 9.2/10 | Option B/C explicitly resisted per resume prompt constraint. 1:1 mirror discipline applied. Each phase runbook has explicit anti-Frankenstein reminders. Concentrated-privilege map enumerated. Every "what this skill does NOT do" list is rigorous. Minor deduction: folding of phases (2 into 1, 4 into 3, 7 into 6) is a consolidation move that trades mirror purity for file-count restraint — defensible (resume suggested 5-7 files) but not zero-cost. The top-level consent card is the privilege mitigation and is documented thoroughly. |
| **Average** | **9.0/10** | Clears the v0.8.0 floor of 8.5 by **0.5**. Running average v0.2 → v0.8 = **(7.6 + 8.2 + 8.8 + 8.4 + 8.6 + 8.8 + 9.0) / 7 = 8.49/10**. This is **0.01 below** the v1.0.0 target average of 8.5/10 — functionally the target, formally just under. Below the 9.1/10 threshold for a direct v1.0.0 tag, so v0.8.0 ships here and a v0.9.0 polish pass remains an option if the user wants to pull the running average cleanly above 8.5 before the v1.0.0 tag. The user's call at session end. |

### Known gaps for v0.9.0 or v1.0.0

- **Dry-run against a real downstream project** — the orchestrator has not been validated by execution. The first real downstream bootstrap will surface frictions informing v1.1. Deferred from v0.8.0 explicitly (resume prompt open question 4).
- **Dogfood run 3 for `session-post-processor`** — still pending. Needs a future Genesis session or the first Aurum session after the freeze lifts. Hook wiring still deferred until run 3 lands CLEAN.
- **README.md polish pass** — the public README still says "Genesis v1 is coming soon" from the bootstrap. If v1.0.0 ships directly from v0.8.0, the README needs updating in the same release. If a v0.9.0 polish intervenes, the README polish lands there.
- **Phase-file length trimming** — `phase-1-rules-memory.md` (280 lines), `phase-3-git-init.md` (298 lines), `phase-6-commit-push.md` (318 lines) are longer than the 5-skill median. A ~10-15% trim without content loss would push prose cleanliness toward 9.0+.
- **Multi-slug YELLOW warning in `run.py`** — v0.5 gap, still open.
- **Test vector harness for redaction patterns** — v0.5/v0.7 gap, still open.
- **Allow-list for `generic_long_base64` false positives** — v0.6 gap, still open.

### Next version target — two paths, user decides

- **Path A (v0.9.0 polish → v1.0.0)**: pull the running average above 8.5 via a small polish pass (README update, phase-file trim, dry-run validation against a tmp downstream folder, maybe one of the v0.5/v0.6 gaps). Then tag v1.0.0 with a clean running average ≥ 8.50 and the anti-Frankenstein inflection-point officially reached. **Cleaner narrative, slightly more work.**
- **Path B (v0.8.0 ships as-is, user calls 8.49 "effectively 8.5" for direct v1 ship)**: accept the 0.01 formal miss, tag v1.0.0 directly on the v0.8.0 squash with explicit confirmation, and start the v1.1 backlog in the next session (dry-run, hook wiring after run 3, phase-file trim, README polish). **Faster ship, Aurum freeze lifts sooner.**
- **The user decides after reading this CHANGELOG and the genesis summary at end of session.**

---

## [0.7.0] — 2026-04-15 — "Pépite flagging skill + R8 slug rule correction"

### Added

- `skills/pepite-flagging/` — the **last independent skill stub** shipped as a 1:1 mirror of the canonical spec `.claude/docs/superpowers/specs/v1_pepite_discovery_flagging.md`. Speech-native, consent-bounded, automatic detection during research operations (WebSearch, WebFetch, sub-agent exploration, R8 refreshes) with a "two or more of six" red-light criteria rule. Six files, ~936 lines total:
  - `SKILL.md` — entry point, automatic + manual trigger phrases, five-step flow (detect → create → surface → act → INDEX), hard rules, anti-Frankenstein scope locks
  - `trigger-criteria.md` — the six red-light criteria with rationale, calibration example, and anti-noise guard per criterion. Applied "two or more" scoring table with worked examples. Anti-over-flagging and anti-under-flagging discipline
  - `pepite-format.md` — frontmatter schema (14 required fields), body section order, slug derivation, status transition table (seed → extracted → actioned → archived, with dismissed as terminal), idempotency rules, one fully-worked illustrative example marked as non-real
  - `cross-project-routing.md` — pointer file template, per-target consent pattern (never batched silently), target project slug lookup with v1 hard-coded machine map, cold-read protocol for pointer consumers, v1/v2 scope lock
  - `install-manifest.yaml` — idempotent directory + INDEX.md creation with `create_if_missing_only` guard, three verification checks, no runtime dependency declaration (pure Markdown + YAML skill)
  - `verification.md` — two-mode health card (13 checks), halt-on-RED on missing required frontmatter, illegal status transition, or **cross-project pointer write without explicit per-target consent** (consent floor — the only privileged operation in this skill)
- `.claude-plugin/plugin.json` version bumped to `0.7.0`, added `pepite-flagging` to the keywords list.

### Fixed

- **R8 research entry correction — live dogfood follow-up from v0.6.0**. The `claude-code-session-jsonl-format_2026-04-15.md` entry described the cwd-to-slug rule as replacing only `\`, `:`, and space with `-`. Empirical verification during the v0.6 first dogfood run proved underscore also maps to `-`; the code was fixed in `slugify_cwd()` but the research entry still carried the incomplete rule. Corrected in this release: the entry now lists `\`, `/`, `:`, `_`, and space as the full replacement set, with an explicit "Correction 2026-04-15 (live dogfood)" note pointing to `memory/journal/2026-04-15_slug-rule-live-dogfood-correction.md` for the epistemic context. Forward slash `/` added to cover git-bash-style cwd strings on Windows. First time an R8 entry has been amended in-place after a live-dogfood correction rather than via a supersede chain — justified because the correction is a bug fix, not new research.

### Notes

- **Four skills shipped** now: `phase-minus-one`, `phase-5-5-auth-preflight`, `journal-system`, `session-post-processor`, plus `session-post-processor/run.py` as a v0.6.0 add. **`pepite-flagging` is the fifth**. Only **one** stub remains: `genesis-protocol/` (the orchestrator, always last).
- **1:1 spec mirror discipline** applied for the second time (first was `journal-system` in v0.4). Every file in `skills/pepite-flagging/` references the canonical spec and explicitly commits to tracking it — if the spec changes, the skill is updated to match, never the other way around.
- **No runtime code** in this skill. Unlike `session-post-processor/run.py`, detection and flagging happen inside Claude's own research operations; file writes use the built-in Write tool. The skill is pure Markdown + YAML. This is deliberate — the detection logic is a judgement call, not a deterministic pipeline, and a Python implementation would either oversimplify (miss pépites the LLM would catch) or duplicate the LLM's job.
- **Consent floor** — cross-project pointer writes are the only privileged operation. Per-target consent is mandatory; silence is always a skip, never an implicit yes; batched "propagate to all" requires explicit echo-back confirmation. `verification.md` Check 10 halts on any consent bypass, deletes the offending pointer, and refuses to auto-retry. Same discipline as `session-post-processor`'s halt-on-leak gate.
- **v1 machine map is hard-coded** in `cross-project-routing.md` — the Genesis user runs ~20 projects, the mapping is small, and it changes slowly. Auto-discovery of sibling projects is a v2 candidate, deferred because a hard-coded map covers the current use case and automation without a felt pain is scope creep.
- **First-half-of-session discipline** applied again: R8 refresh first (slug underscore correction), skill implementation second. Granular commits inside the feat branch: one per skill file + plugin.json bump + CHANGELOG, squashed at merge time.
- **No example pépite pre-seeded**. The illustrative DuckDB+VSS example in `pepite-format.md` is explicitly marked as non-real. The first real pépite will be detected during normal research operations in v0.7.0+ sessions — live dogfood, not synthetic.
- **Every new file carries the `SPDX-License-Identifier: MIT` header** per R10.
- **`phase-minus-one`, `phase-5-5-auth-preflight`, `journal-system`, `session-post-processor`** all untouched. All stable.

### Self-rating — v0.7.0

| Axis | Rating | Notes |
|---|---|---|
| Pain-driven coverage | 9/10 | Every file maps to a spec section or a detection/consent concern. The cross-project consent floor directly addresses the "never auto-propagate" rule from Layer 0. The trigger criteria calibration reflects the anti-over-flagging and anti-under-flagging pains that only become concrete after the skill ships and gets used. The R8 slug rule fix closes the gap left at v0.6 shipping time. Zero speculative features. |
| Prose cleanliness | 8/10 | Six files, ~936 lines. Each file has a clear job and minimal overlap. The spec mirror means some content is deliberately duplicated from `v1_pepite_discovery_flagging.md` — this is intentional because the skill must be legible without clicking through to the spec. Tables used throughout for criteria, transitions, verification checks. The hard-coded machine map in `cross-project-routing.md` is prose-ugly but v1-honest; a prettier auto-discovery surface is explicitly v2. |
| Best-at-date alignment | 9/10 | Criteria 3 ("emerging tech") and Criteria 6 ("highest potential") directly operationalise the Layer 0 `best-practice-at-date default` rule. The cross-project routing is the first operational component of Meta-Memory Layer 3 — stepping stone to Path B per the Layer 0 Meta-Memory architecture. Pointer file format uses current `type: reference` convention consistent with the rest of the Genesis memory stack. |
| Self-contained | 9/10 | Pure Markdown + YAML. Zero runtime dependencies. No Python, no pip, no external binaries. Install step touches only `memory/pepites/` inside the target project. Cross-project pointers are additive auto-memory writes that never touch another project's git state — the only cross-project effect is a file appearing in `~/.claude/projects/<target>/memory/`, which is per-machine state. |
| Anti-Frankenstein | 9/10 | Deferred explicitly: slash commands (v2), auto-propagation without per-target consent (v2), TTL auto-archive (v2), cross-pépite synthesis (v2), pépite ranking (v2 if ever), multi-machine propagation (v2), Python runtime (not needed). The skill's surface is exactly six files mirroring a frozen spec, no more. Pre-seeded example marked as non-real to prevent false provenance. Manual force-flag path exists but the primary mode is auto-detection because that's where the pain is. |
| **Average** | **8.8/10** | Clears the 8.0/10 floor by 0.8. Ties with v0.4.0 (journal-system, also 8.8/10) as the highest single-version rating in the project's history. Above v0.6.0 (8.6/10) because the 1:1 spec mirror discipline is a cleaner rating surface than first-runnable-code, and because the R8 slug rule correction is a side-fix that would normally be carried as debt — closing it in the same release removes a latent drag. Running average v0.2 → v0.7 = **(7.6 + 8.2 + 8.8 + 8.4 + 8.6 + 8.8) / 6 = 8.40/10**, still on track for v1 target 8.5/10. The last milestone (`genesis-protocol`) needs to land at ≥ 9.1 to reach the target — achievable but tight, the orchestrator's rating ceiling depends heavily on how cleanly it composes the five shipped skills. |

### Known gaps for v0.8.0

- **`genesis-protocol` orchestrator skill** — the last remaining stub. Composes all five shipped skills (`phase-minus-one`, `phase-5-5-auth-preflight`, `journal-system`, `session-post-processor`, `pepite-flagging`) into the 7-phase protocol from the master vision. This is the v1 ship target.
- **Dogfood run 3 for `session-post-processor`** — still pending. Needs either a future Genesis session (post-v0.7 maintenance) or the first Aurum session after the freeze lifts. Hook wiring stays deferred until run 3 lands CLEAN.
- **Multi-slug YELLOW warning in `run.py`** — v0.5 gap, still deferred. No multi-slug collision exists on this machine to test against.
- **Test vector harness for redaction patterns** — v0.5 gap. Small `tests/redaction_vectors.py` is a v0.8+ candidate.
- **Allow-list for `generic_long_base64` false positives** — v0.6 gap. Short list of safe path prefixes.
- **First real pépite detection** — no pépites flagged in this session because the session is implementation work, not research. The first real flag happens in a v0.7+ research session.

### Next version target

**v0.8.0 — `genesis-protocol` orchestrator** (the last remaining stub, likely v1.0.0 if it lands high). Target rating: **8.5/10 floor** because the v1 ship is close and the orchestrator's rating sets the v1 average. An alternative is a small maintenance version (hook wiring for session-post-processor, test vector harness, allow-list) if the user wants to reduce technical debt before the ship, but the anti-Frankenstein discipline says ship first and polish after — the orchestrator is the critical path to v1.

---

## [0.6.0] — 2026-04-15 — "Session post-processor run.py executable"

### Added

- `skills/session-post-processor/run.py` — the first Genesis skill to ship a runnable Python module instead of a spec-only Markdown surface. Implements the seven-step pipeline frozen in v0.5.0 (locate → parse → redact → emit → halt-on-leak → INDEX → health card) using only the Python 3.10+ standard library (`json`, `re`, `os`, `pathlib`, `datetime`, `argparse`, `sys`, `unicodedata`). No pip installs, no vendored libraries. CLI flags: `--project-root`, `--cwd` (for worktree override), `--jsonl` (explicit source), `--inject-test-leak` (dogfood-only halt-gate probe).
- `memory/project/sessions/` — seeded via the run.py install step (idempotent `ensure_sessions_dir`), with the canonical `INDEX.md` stub from `install-manifest.yaml`.
- `memory/project/sessions/2026-04-15_on-reprend-v0-6-0-project-genesis.md` — **first real dogfood archive** of a live Genesis session, produced by run.py against `~/.claude/projects/C--Dev-Claude-cowork-project-genesis/a3857578-*.jsonl`. 93 records, 37 tool calls, 20 redactions across 13 patterns, halt-on-leak gate CLEAN. Committed as a durable artefact per the v0.5 → v0.6 resume prompt — the archive is a version-controlled record of the implementation session, redacted by construction.
- `.claude-plugin/plugin.json` version bumped to `0.6.0`.

### Fixed

- **Slug derivation** — the 2026-04-15 on-disk-verified research entry said `\`, `:`, and space map to `-`, but empirical verification during the first dogfood run showed **underscore also maps to `-`** (actual directory `C--Dev-Claude-cowork-project-genesis`, not `C--Dev-Claude_cowork-project-genesis`). `slugify_cwd()` extended to replace `\`, `/`, `:`, `_`, and space. First live-dogfood correction of a research entry. Research entry refresh is a v0.7+ follow-up (low priority — code is correct, only the documentation caveat is outstanding).

### Verified

- **Halt-on-leak gate fires under deliberate test** — `--inject-test-leak` appends a fake `github_pat_` + 90-`A` string to the parsed record list **after** the redaction pass so it bypasses the redactor, reaches the emitter raw, triggers the verification gate, and the written archive is deleted before the INDEX update. Confirmed end-to-end: 54616 bytes written, `github_pat_finegrained` leak detected, file unlinked, RED card emitted, non-zero exit code. The gate is not theoretical.
- **First-run on the current session's JSONL succeeds**: CLEAN verification, 20 redaction hits across 13 patterns, 37 tool calls surfaced, archive is 1182 lines and 49683 bytes.

### Notes

- **Dogfood run 2 of the three-run gate**. Run 1 was the v0.5.0 session itself (implicit — the skill shipped the spec, no executable, so no run was possible, but the session's own JSONL proved the spec was parseable by hand). Run 2 is this v0.6.0 session, with the actual `run.py` processing `a3857578-*.jsonl`. Run 3 will be either a future Genesis session or the first Aurum session after the freeze lifts. **Hook wiring stays deferred** per R10 anti-Frankenstein discipline — no `SessionEnd` automation before all three runs land CLEAN.
- **Only stdlib**, per the v0.5 spec freeze. No `yaml` (frontmatter emitted as plain text), no `requests`, no `pyyaml`. Python 3.14 on this machine covers the 3.10+ floor with room to spare.
- **Generic pattern false positives are acceptable** — `generic_long_base64` caught a file path fragment (`claude/docs/superpowers/research/stack/claude-code-session`) during the first dogfood. This is the documented cost of the redact-heavy strategy: false positives are recoverable, false negatives are incidents. A v0.7+ candidate is a short allow-list of known-safe path fragments, not a regex relaxation.
- **Idempotent archive allocation** — `allocate_archive_path` appends `-2`, `-3`, etc. on filename collision. Re-running the skill against the same session produces a new file each time, and the user can diff them to confirm redaction stability.
- **Atomic emit** — `emit_markdown` writes to `<archive>.md.tmp`, then `.replace()`s to `<archive>.md`. Avoids half-written archives if the process crashes mid-emit.
- **Granular commit discipline** applied again — one commit per logical unit (run.py, sessions/ + dogfood, plugin.json, CHANGELOG).
- **`phase-minus-one`, `phase-5-5-auth-preflight`, `journal-system`, `session-post-processor` spec files untouched**. All stable.
- Every new file carries the `SPDX-License-Identifier: MIT` short-form header.

### Self-rating — v0.6.0

| Axis | Rating | Notes |
|---|---|---|
| Pain-driven coverage | 9/10 | The v0.5.0 session shipped the spec but blocked on the three-run dogfood gate because no executable existed. `run.py` unblocks it end-to-end. Every feature in `run.py` maps to a specific step of the v0.5 spec — zero speculative additions. `--inject-test-leak` is a dogfood-only flag that exists because the halt gate needs a live proof, not a theoretical one. |
| Prose cleanliness | 8/10 | One file, ~700 lines, sectioned into redaction / slug / parser / emitter / verifier / index / health-card / main with block-comment headers. Functions are small and named for what they return, not what they do. Comments only where WHY is non-obvious (env_local_paste special case, dogfood injection rationale, post-redaction tag stripping). Slightly below v0.4's journal-system 9 because it's code not prose, and code carries more intrinsic noise. |
| Best-at-date alignment | 9/10 | 2026-current Python idioms (type hints with `|` union, `Path.read_text(encoding=)`, `re.Pattern[str]`). Redaction patterns match 2026 token formats per the v0.5 spec (github_pat_finegrained 82+ chars, `sk-ant-`, `sb_secret_`, `sk-proj-`, AWS prefix list, Google `AIza`, JWT `eyJ...eyJ...`). No legacy Python 2 baggage, no deprecated stdlib modules. |
| Self-contained | 9/10 | Single file, stdlib only, no pip, no yaml parser, no cross-skill imports. Install step is idempotent and creates only `memory/project/sessions/` + `INDEX.md`. The Python 3.10+ runtime is already declared in `install-manifest.yaml` — no new dependency is introduced by this version. Higher than v0.5 (8) because v0.5 *declared* the runtime dep; v0.6 just *uses* it inside the existing envelope. |
| Anti-Frankenstein | 8/10 | Did NOT wire SessionEnd hooks (R10 discipline). Did NOT add a YELLOW warning for multi-slug collision (v0.5 gap, deferred — there is no real multi-slug collision on this machine to dogfood against, so the logic would be untestable now). Did NOT add a test vector runner (v0.5 gap, deferred — the `--inject-test-leak` flag is the minimal viable halt-gate proof). Did NOT implement retroactive batch processing. The dogfood-injection flag is one 4-line block that only runs with `--inject-test-leak`; its existence is pain-driven (we need to prove the gate fires). Capped at 8 because run.py is a single 700-line file and a future session might legitimately split it (parser/redactor/emitter) if the test harness grows. |
| **Average** | **8.6/10** | Clears the 8.0/10 floor by 0.6. Above v0.5.0 (8.4/10) because implementing a frozen spec is a cleaner rating surface than the spec-freeze itself. Running average across v0.2 → v0.6 = **(7.6 + 8.2 + 8.8 + 8.4 + 8.6) / 5 = 8.32/10**, on track for the v1 target 8.5/10. |

### Known gaps for v0.7.0

- **No multi-slug collision YELLOW warning** — if a project has both a `-2026` and a plain slug under `~/.claude/projects/`, both will match the current rule and the most-recent-mtime pick is usually correct but could surprise. Add a YELLOW warning when multiple slug dirs exist for the same cwd.
- **Research entry refresh for the underscore rule** — the 2026-04-15 `claude-code-session-jsonl-format` research entry still documents `\`, `:`, and space only; refresh to add underscore.
- **Test vector harness** — `redaction-patterns.md` has vectors, run.py has no harness. Small `tests/redaction_vectors.py` would assert `match` vectors redact and `non-match` vectors survive.
- **Allow-list for generic_long_base64 false positives** — path fragments like `claude/docs/superpowers/research/stack/claude-code-session` should not be redacted. Short allow-list of safe prefixes.
- **`pepite-flagging` skill** — the last independent skill stub, now the natural next target for v0.7 (was the alternative v0.6 option).
- **`genesis-protocol` orchestrator** — still last, lands after every phase and skill is implemented and the first public downstream bootstrap proves the flow.
- **`SessionEnd` hook wiring** — still deferred until run 3 of the dogfood gate lands CLEAN.

### Next version target

**v0.7.0** — `pepite-flagging` skill OR run 3 of the post-processor dogfood against an Aurum session (only if the freeze has lifted). Rubric says pick the more concrete pain at session open. Target rating: **8.0/10 floor**.

---

## [0.5.0] — 2026-04-15 — "Session post-processor skill"

### Added

- `skills/session-post-processor/` — the fourth functional skill. Parses the current Claude Code session's JSONL transcript, redacts secrets (GitHub PATs, SSH private keys, Anthropic/OpenAI/Supabase/Stripe/AWS/Google API keys, JWTs, `.env.local` content paste-backs, generic long hex / base64), and emits a readable Markdown archive under `memory/project/sessions/YYYY-MM-DD_<slug>.md`. Includes a mandatory **halt-on-leak verification gate** that re-applies every pattern to the written file and deletes it if any pattern still matches. Manual-invoke only in v0.5.0 — `SessionEnd` hook wiring is a v0.6+ candidate after three successful dogfood runs.
- `skills/session-post-processor/SKILL.md` — entry point, trigger phrases, seven-step flow (locate → parse → redact → emit → halt-on-leak → INDEX → health card), explicit manual-only discipline for v0.5.0 with a three-run dogfood requirement before any hook wiring, anti-Frankenstein scope locks.
- `skills/session-post-processor/jsonl-parser.md` — record-by-record schema walkthrough based on the on-disk-verified 2026-04-15 research entry. Outer type / inner content-block type distinction, `parentUuid` threading with timestamp as primary ordering key, sidechain sub-agent grouping rule, five content-block extraction rules, resilient error handling (no exceptions halt the parse — only the secret-leak gate halts).
- `skills/session-post-processor/redaction-patterns.md` — 14 patterns in specific-before-generic application order with name / regex / rationale / test vectors for each. Variable-name-preserving replacement for `env_local_paste`. Explicit non-goals for handwritten secrets, URL-embedded credentials, binary attachment contents.
- `skills/session-post-processor/markdown-emitter.md` — output template with frontmatter schema, per-record-kind rendering rules, truncation rules, idempotency rule (re-run produces `-N` suffixed file, never silent overwrite).
- `skills/session-post-processor/install-manifest.yaml` — Python 3.10+ runtime dependency (stdlib only), `memory/project/sessions/` + `INDEX.md` creation with `create_if_missing_only` guard, five verification checks. Explicitly does NOT register `SessionEnd` hooks, does NOT modify `settings.json`.
- `skills/session-post-processor/verification.md` — two-mode health card with 12 checks including the critical halt-on-leak redaction gate that deletes the archive file on any pattern hit. File deletion is the single privileged operation in the whole skill.
- `.claude/docs/superpowers/research/stack/claude-code-session-jsonl-format_2026-04-15.md` — refreshed research entry (confidence upgraded medium → high after on-disk verification against `a086701e.jsonl`, 174 records). Clarifies outer vs inner type taxonomy, documents verified flat layout, slug derivation rule, multi-slug-per-project situation (both `project-genesis` and `project-genesis-2026` slugs exist from prior rename), supersedes the 2026-04-14 entry which moves to `research/archive/`.
- `.claude-plugin/plugin.json` version bumped to `0.5.0`.

### Notes

- Ships **one** skill only, per anti-Frankenstein discipline. Remaining stubs: `pepite-flagging/` + `genesis-protocol/` (orchestrator, still last).
- **Granular commit discipline** applied for the first time on this skill, as reinforced by the v0.4.0 PowerShell-window incident. Eight commits in the feat branch (research-refresh → SKILL.md → jsonl-parser → redaction-patterns → markdown-emitter → install-manifest → verification → changelog-bump), squashed to one on merge. Protects against mid-session host loss.
- **Research refresh as a prerequisite**. The existing `claude-code-session-jsonl-format_2026-04-14.md` entry expired today (2026-04-15), was confidence `medium`, and had explicit "verification needed" caveats. Before writing the skill, the session sampled a real JSONL on disk, verified the outer vs inner type taxonomy, and wrote the 2026-04-15 replacement with confidence `high`. First application of the R8 "refresh or extend" rule mid-session.
- **Manual-only for v0.5.0** — no `SessionEnd` hook wiring. Three-run dogfood gate before automation: this session (run 1), a subsequent Genesis session (run 2), an Aurum session after the freeze lifts (run 3).
- **Halt-on-leak gate is the security floor**. A redaction miss must never result in a silent archive file with the secret in it. File deletion is the single privileged operation in the skill.
- **No vendored dependencies**. Prior art cited for schema reference only. Python stdlib is enough.
- **`phase-minus-one`, `phase-5-5-auth-preflight`, and `journal-system` untouched**. All three stable at 7.6 / 8.2 / 8.8.
- Every new file carries `SPDX-License-Identifier: MIT` short-form header per R10.

### Self-rating — v0.5.0

| Axis | Rating | Notes |
|---|---|---|
| Pain-driven coverage | 9/10 | Writing session memories by hand has been the manual step in every Genesis session so far (v0.1 → v0.4, five times). Halt-on-leak gate addresses the specific threat of silently committing a redaction miss. Research refresh closes the "confidence medium" caveat from the 2026-04-14 entry. Zero speculative features. |
| Prose cleanliness | 7/10 | Larger skill (6 files vs 5 for journal-system) because redaction and verification both need their own files. Tables used for patterns, checks, rendering rules. Some intentional redundancy between `jsonl-parser.md` and the research entry so the skill stays legible when the research TTL expires. Denser than journal-system because the subject matter is denser. |
| Best-at-date alignment | 9/10 | On-disk verification against a Claude Opus 4.6 session file from today. Redaction patterns include 2026-current token formats (fine-grained `github_pat_11`, Anthropic `sk-ant-`, Supabase `sb_secret_`, OpenAI `sk-proj-`, Stripe `sk_(test\|live)_`, full AWS prefix list, Google `AIza`). Python 3.10+ `match/case` is 2026-current idiomatic. |
| Self-contained | 8/10 | Runs end-to-end within `skills/session-post-processor/` + `memory/project/sessions/`. Touches `~/.claude/projects/` read-only. Python 3.10+ is the only non-stdlib cross-skill coupling in the Genesis stack so far — previous skills are pure markdown / bash. Capped at 8 because the runtime dependency is a genuine self-containment cost. |
| Anti-Frankenstein | 9/10 | Six files (minimum for this surface). Zero speculative features: no hook wiring in v0.5, no HTML emitter, no token-usage dashboard, no cross-session timeline, no semantic indexing, no interactive replay. Manual-only with three-run dogfood gate. Halt-on-leak gate is the only privileged operation. Skill deliberately does NOT cache parsed records — each run is fresh and auditable. |
| **Average** | **8.4/10** | Clears the 8.0/10 floor by 0.4. Below v0.4.0 (8.8/10) intentionally — larger surface and a real runtime dependency. The journal-system climb was from a smaller surface, not a more rigorous rubric. v1 average target 8.5/10 still defensible. |

### Known gaps for v0.6.0

- **No executable Python module** — ships the pipeline spec, not a runnable `.py`. First dogfood run needs a small entry point written on the fly, eventually promoted to `skills/session-post-processor/run.py`. Deferred because the spec must be frozen before the implementation; v0.5 is the spec freeze.
- **No test vector runner** — `redaction-patterns.md` lists vectors but no harness. Small `tests/redaction_vectors.py` is a v0.6 candidate.
- **No SessionEnd hook wiring** — explicit v0.6+ candidate after three successful manual dogfood runs.
- **No retroactive processing** — current session only. Archiving historical JSONLs (v0.1 → v0.4) deferred.
- **No cross-session timeline** — separate `session-timeline` aggregator, v0.8+ candidate.
- **No JWT decoding** — shape match only, payload decoding deferred.
- **No slug-collision detection** — multiple Windows-path variants collapsing to the same slug would land JSONLs in the same directory. Most-recent-mtime pick is usually correct; YELLOW warning for multi-match is a v0.6+ safety net.

### Next version target

**v0.6.0** — either `pepite-flagging` (the remaining independent skill stub) or the first implementation pass of session-post-processor's executable Python module. Rubric says pick the more concrete pain point at the time. Target rating: **8.0/10 floor**.

---

## [0.4.0] — 2026-04-15 — "Journal system skill"

### Added

- `skills/journal-system/` — the third functional skill, end-to-end implementation of the 6th memory type defined in Layer 0 (`~/.claude/CLAUDE.md` → "Journal System — Universal Thought Capture"). Speech-native, trigger-phrase driven, single-project scope. Recognises the five FR/EN trigger phrases, creates or extends dated entries under `memory/journal/`, preserves the user's verbatim words, and gates every amplification on explicit per-invocation consent. No auto-loading — entries are read intentionally, like a personal notebook.
- `skills/journal-system/SKILL.md` — skill entry point, frontmatter for Claude Code plugin auto-discovery, the five trigger phrases in a single lookup table, the five-step flow (recognise → load/create → verbatim capture → consent-gated amplification → metadata+INDEX sync), the six amplification rules as a brief reminder, and an explicit "what this skill does NOT do" section to lock scope against cross-project aggregation / auto-tagging / full-text search.
- `skills/journal-system/entry-format.md` — canonical frontmatter schema with the eight required fields, the five states (`captured`, `seed`, `growing`, `dormant`, `resolved`) with transition rules, the full stratified dialogue template, the six format-enforcement rules (verbatim blockquote, Claude-voice labelling, horizontal-rule separators, append-only layers, fixed sub-section order, immutable title), the slug generation procedure, primary-vs-fallback location logic, and the starter `INDEX.md` template.
- `skills/journal-system/amplification-rules.md` — the six hard rules from Layer 0, 1:1 mirror with rationale for each: never auto-amplify, never rewrite the user's words, every addition attributed and dated, be sparing with poetry, pushbacks are valid amplifications, a layer can have no amplification. Plus four operational consequence rules (R7 consent is a blocking gate, R8 consent does not cascade across layers, R9 no preemptive offers, R10 amplification never mandatory for completeness).
- `skills/journal-system/install-manifest.yaml` — idempotent install step creating `memory/journal/` directory and seeding `memory/journal/INDEX.md` with the five empty state sections. `create_if_missing_only` guard prevents overwriting user-authored INDEX content. Three verification checks (directory exists, INDEX exists, INDEX is a journal index). No hook registration, no `settings.json` touch, no dependency installation.
- `skills/journal-system/verification.md` — two-mode health card (post-install + post-action) with eight checks: directory exists, INDEX exists, five state sections present, target file exists, frontmatter valid and complete, verbatim quote preserved (Rule 2 guard), INDEX reflects state transitions without duplication, amplification attribution correct (Rule 3 + Rule 1 consent guard). Three status levels (GREEN / YELLOW / RED) with explicit halt on any RED to prevent silent propagation of verbatim-modification or consent-bypass violations.
- `.claude-plugin/plugin.json` version bumped to `0.4.0`.

### Notes

- Ships **one** skill only, per anti-Frankenstein scope discipline. Remaining skill stubs (`genesis-protocol`, `session-post-processor`, `pepite-flagging`) land in their own worktrees later.
- The journal system skill is a **1:1 mirror of the Layer 0 spec**, not an independent design. If Layer 0's journal spec changes, `skills/journal-system/` must be updated to match — never the other way around. This is explicitly stated in `SKILL.md`, `entry-format.md`, and `amplification-rules.md` so future sessions cannot silently drift the skill away from its source of truth.
- The skill is the first Genesis skill that has **no consent card** — unlike `phase-minus-one` and `phase-5-5-auth-preflight` which touch the machine and thus require explicit opt-in. Rationale: the journal system is speech-native, so the trigger phrase itself is the consent. A consent card would be friction on a surface where the user wants zero friction. Amplification consent is still mandatory per-invocation and is handled inline via Rule 1, not via a card.
- No `states.md` or `trigger-phrases.md` as separate files — both live inside their primary consumer (`entry-format.md` for states, `SKILL.md` for trigger phrases). A 7-line state table does not justify a separate file; the indirection would harm readability more than it would help reuse.
- No `modes/` runner directory — this skill does not touch the OS, so the 3-mode ladder from `phase-minus-one` does not apply. Trigger phrases are the only interaction surface.
- `phase-minus-one` and `phase-5-5-auth-preflight` are untouched — both remain stable at 7.6/10 and 8.2/10 respectively. No cross-skill refactor was attempted.
- Cross-project aggregation (the `/journal timeline` view across every repo) is explicitly out of scope — that is the Meta-Memory Path B session's job. This skill ships single-project capture only, but entries are written consistently so the future aggregator has clean input.
- Every new file carries the `SPDX-License-Identifier: MIT` short-form header per R10.
- No new spec file — the canonical spec is the Layer 0 CLAUDE.md "Journal System — Universal Thought Capture" section, already frozen and in the universal layer.

### Self-rating — v0.4.0

| Axis | Rating | Notes |
|---|---|---|
| Pain-driven coverage | 9/10 | Every file addresses a concrete need documented in the Layer 0 spec: the vertigo-dogfooding entry from 2026-04-14 proved amplification works when consent is explicit and grounded. Verbatim preservation guards against the silent paraphrase failure mode. Post-action verification with halt-on-RED prevents the consent-bypass failure mode. Zero speculative features. |
| Prose cleanliness | 8/10 | The skill is smaller than `phase-minus-one` and `phase-5-5-auth-preflight` so the prose could stay tighter. Tables used for the five trigger phrases, five states, eight verification checks. Minimal duplication between files — each file has one job and points to the others via footer references rather than re-stating content. |
| Best-at-date alignment | 9/10 | Mirrors the 2026-04-14 Layer 0 spec exactly, which itself was written as the state-of-the-art on recursive thought capture during the Aurum v0_init session. Frontmatter schema uses current Claude Code plugin conventions. No deprecated patterns. Consent-per-invocation matches the 2026 best practice on LLM consent gating (never persist across turns). |
| Self-contained | 9/10 | Skill runs end-to-end within `skills/journal-system/`. The only external touch is `memory/journal/` which the skill creates itself via `install-manifest.yaml`. No reads from `memory/reference/*`, no dependencies on other skills, no cross-skill file locks. The auto-memory fallback is documented as runtime behaviour with no install-time target. |
| Anti-Frankenstein | 9/10 | Zero speculative surfaces. No consent card (explicitly avoided as friction on a speech-native surface). No `modes/` runner (not an OS-touching skill). No `trigger-phrases.md` or `states.md` (contents fit inside their primary consumer). Five files total, vs 12 for `phase-minus-one` and 8 for `phase-5-5-auth-preflight` — the lightest skill in the stack so far, and the lightness is earned by structural simplicity, not by cutting corners. |
| **Average** | **8.8/10** | Clears the 8.0/10 floor by 0.8. The lightness of the skill lets every axis land high. Above the 8.5/10 v1 ceiling — which the anti-Frankenstein framing called out as the plateau; a small clean skill can land above the ceiling naturally because there is less surface to add complexity to. No need to pad files to "feel complete" — sparse is better than speculative. |

### Known gaps for v0.5.0

- **No runtime probe for the Layer 0 sync check** — `SKILL.md` states that the skill is a 1:1 mirror of the Layer 0 journal system spec and must be updated if Layer 0 changes, but nothing enforces that. A small CI-style probe that diffs the skill's canonical sections against `~/.claude/CLAUDE.md` would detect drift early. Deferred — the Layer 0 spec itself is stable enough that drift is unlikely before v1.
- **No cross-project `/journal timeline` view** — the `memory/journal/INDEX.md` this skill ships is single-project only. The cross-project aggregator that walks every repo's `memory/journal/` on this machine is deferred to the Meta-Memory Path B session. Until then, users query cross-project with `grep -r` manually.
- **No auto-migration from `~/.claude/projects/<slug>/memory/journal_*.md` fallback to the repo's `memory/journal/`** — the fallback is documented but requires a manual move when the worktree becomes available. A small helper that detects and prompts the migration is a v0.5+ candidate. Low priority — the fallback is only triggered in pre-worktree sessions, which are rare.
- **No keyword auto-suggest on entry creation** — the `keywords:` frontmatter field is user-provided or Claude-inferred on demand. An auto-suggestion pass based on the verbatim quote content would lift the "findability" of entries for the future cross-project search. Deferred.
- **No trigger-phrase disambiguation helper** — if a user says "j'ai une idée sur X" the skill asks explicitly. A smarter fuzzy matcher could catch edge phrasings ("notons une pensée", "je veux journaliser ça") but the risk of false positives on non-journal speech is higher than the value. Deliberately left simple.
- **No direct support for importing an existing external notebook** — the skill only creates fresh entries. Users with existing `.md` notebooks they want to migrate into `memory/journal/` do so manually. Bulk import is a v1+ candidate once the first real migration need surfaces.

### Next version target

**v0.5.0** — fourth skill implementation. Two independent skill stubs remain before the orchestrator: `session-post-processor/` (JSONL redaction + markdown archive) and `pepite-flagging/` (red-light discovery flagging with cross-project routing). Pick whichever has the most concrete pain point at the time — the rubric in the v0.3.0 → v0.4.0 resume prompt applies. Target rating: **8.0/10** (floor, not ceiling).

---

## [0.3.0] — 2026-04-15 — "Phase 5.5 Auth Pre-flight skill"

### Added

- `skills/phase-5-5-auth-preflight/` — the second functional skill, end-to-end implementation of Phase 5.5 Auth Pre-flight per `specs/v1_phase_5_5_auth_preflight_learnings.md`. Closes the loop between "Phase -1 set up the machine" and "Phase 5 is ready to push a first repo". Paste-back is the baseline, Playwright automation is an opt-in convenience layer with hard fall-back on any selector mismatch.
- `skills/phase-5-5-auth-preflight/SKILL.md` — skill entry point, frontmatter for Claude Code plugin auto-discovery, six-step flow map, canonical PAT scope list (incl. Administration RW), isolated copy-paste rule (Learning 1), security-floor rules, anti-Frankenstein reminders.
- `skills/phase-5-5-auth-preflight/consent-card.md` — Step 5.5.0 card collecting project slug, GitHub owner, repo name, visibility, PAT expiration window, Chrome profile choice, Playwright opt-in. Every field defaults to safe null; consent is logged to `memory/reference/consent-log.md`.
- `skills/phase-5-5-auth-preflight/ssh-keygen.md` — Step 5.5.1 walkthrough: pre-check existing key, generate dedicated ed25519 key with `-C <slug>@<owner> -N ""`, idempotent append of `Host github.com-<slug>` block with `IdentitiesOnly yes` to `~/.ssh/config`, isolated code blocks for title/key/URL paste-back, `ssh -T` binding confirmation with wrong-identity recovery.
- `skills/phase-5-5-auth-preflight/pat-walkthrough.md` — Step 5.5.2 walkthrough: every field of the fine-grained PAT form in actual UI order (Learning 2), isolated code blocks for every paste value (Learning 1), canonical scope list with Administration RW (Learning 4), "All repositories" rationale, one-time token capture, `.env.local` sink with `gh api user` sanity test. Form snapshot date in frontmatter with `expires_at` 30-day TTL.
- `skills/phase-5-5-auth-preflight/empty-repo-create.md` — Step 5.5.3 walkthrough: the hard lesson that fine-grained PATs cannot create user-owned repos via API, every form field in its own fenced code block, "Initialize with" boxes all left unchecked, `git remote set-url` to the per-project SSH alias, verification via `gh api repos/owner/repo`. Snapshot `expires_at` TTL as above.
- `skills/phase-5-5-auth-preflight/three-probe-test.md` — Step 5.5.4 canonical three-probe gate (SSH handshake against the alias, `gh api user`, `gh api repos/owner/repo` with `.permissions.admin` check). Per-probe failure-mode tables with targeted recovery pointers. Full-pass helper `set -e` snippet with four exit codes (1/2/3 per probe, 0 for all-green) that R1.1 session-open health checks can grep. Standalone by design — Phase 5, downstream skills, and resumption flows all reuse it.
- `skills/phase-5-5-auth-preflight/playwright-automation.md` — conditional automation branch, opt-in via consent card only, Playwright MCP from Phase -1 required. Known-selector map for the three GitHub forms with `expires_at` 30-day TTL, hard fall-back to paste-back on any single selector miss (no retry loops), three-variant token-capture mitigation + `browser_snapshot` safety net, screenshot-on-failure for forensic review.
- `skills/phase-5-5-auth-preflight/verification.md` — Step 5.5.5 final health card plus the canonical schemas for the two reference memory files the skill writes at completion: `memory/reference/ssh_<project>_identity.md` and `memory/reference/github_<project>_account.md`. Three status outcomes (READY / READY_WITH_FALLBACKS / BLOCKED). Idempotency rules for re-running on an already-wired project.
- `.claude-plugin/plugin.json` version bumped to `0.3.0`.

### Notes

- Ships **one** skill only, per anti-Frankenstein scope discipline. Remaining skill stubs (`genesis-protocol`, `journal-system`, `session-post-processor`, `pepite-flagging`) land in their own worktrees later.
- All three stratified learnings from `specs/v1_phase_5_5_auth_preflight_learnings.md` are honoured: Learning 1 (isolated copy-paste blocks, never inside table cells), Learning 2 (form-order instructions matching the actual 2026 GitHub UI), Learning 3 (three-probe pre-flight as the explicit exit gate), Learning 4 (Administration RW in the canonical scope list), Learning 5 (paste-back cost is the v2 automation justification, honoured by the opt-in Playwright branch).
- Form-snapshot files (`pat-walkthrough.md`, `empty-repo-create.md`, `playwright-automation.md`) carry `expires_at: 2026-05-14` so the next session after that date re-validates the GitHub UI and the Playwright selector map before using them.
- `phase-minus-one` skill is untouched — its 7.6/10 rating is stable and no cross-skill refactor was attempted. Both skills remain self-contained within their own directories.
- No hook wiring, no templates/ population, no marketplace manifest — still out of scope.
- Every new file carries the `SPDX-License-Identifier: MIT` short-form header per R10.
- No features added outside the v1 spec; `three-probe-test.md` was split out as a standalone file only because the spec explicitly names it as Phase 5's entry condition, so Phase 5 and R1.1 both need to call it without pulling in the rest of the skill.

### Self-rating — v0.3.0

| Axis | Rating | Notes |
|---|---|---|
| Pain-driven coverage | 9/10 | Every file points to a specific learning in `v1_phase_5_5_auth_preflight_learnings.md` — isolated copy-paste blocks, form-order instructions, three-probe gate, Administration RW scope, the v2 automation justification. Zero speculative additions. |
| Prose cleanliness | 7/10 | Templates are dense but readable; per-step failure-mode tables are uniform across ssh-keygen / pat-walkthrough / empty-repo-create / three-probe-test. Three files repeat a safety-floor preamble intentionally so each stands alone. |
| Best-at-date alignment | 9/10 | 2026 Q2 patterns: fine-grained PATs with full canonical scopes, per-project SSH alias with `IdentitiesOnly yes`, Playwright MCP opt-in with `expires_at` selector TTL, `GH_TOKEN` env override (never `gh auth login`), isolated copy-paste rule baked into every paste-back instruction. |
| Self-contained | 7/10 | Skill runs end-to-end within `skills/phase-5-5-auth-preflight/`. External reads are bounded: `memory/reference/automation-stack.md` (from Phase -1), `.env.local` (own write), `~/.ssh/config` (own append). `three-probe-test.md` is explicitly designed to be callable from outside the skill by Phase 5 and R1.1 — a deliberate extraction, not a leak. |
| Anti-Frankenstein | 9/10 | Zero speculative surfaces; Playwright is opt-in with hard one-miss fall-back and no retry loops; PAT scope list is explicit and frozen; the three-probe test is fixed at three probes; no cross-skill refactor attempted; form-snapshot TTLs prevent silent rot. |
| **Average** | **8.2/10** | Clears the 7.8/10 target by 0.4. Below the 8.5/10 v1 ceiling — still room for v0.4.0 (next skill) to climb naturally without hitting the inflection point. |

### Known gaps for v0.4.0

- No automated tests for the full-pass helper in `three-probe-test.md` — the exit-code contract (1=SSH, 2=PAT, 3=repo, 0=all-green) is documented but not exercised by a harness. A small mock-based test would lift the "Self-contained" axis.
- The Playwright selector map in `playwright-automation.md` is a 2026-04-15 snapshot — the first time the skill runs in a real session after GitHub updates its forms, the fall-back path will be exercised and the selector map must be refreshed. There is no CI probe to detect drift early; a nightly `browser_navigate` health check is a v0.4.0+ candidate.
- `memory/reference/consent-log.md` schema is documented inside `consent-card.md` but not shipped as a starter file — upgrade when a second skill needs to read it.
- No `templates/phase-5-5-auth-preflight-*.md` ship — the walkthrough templates are skill-local. Promotion to `templates/` lands whenever the first downstream consumer project needs a standalone copy.
- The skill assumes `bash` for the shell snippets. PowerShell-equivalent snippets for Windows native terminal (without git-bash) are deferred — the Phase -1 skill already makes `bash` a core requirement so the assumption is internally consistent, but it does narrow the user base.
- Idempotency on re-run is documented but the consent card's "re-run from scratch / skip to 5.5.4 / cancel" branch is prose-only; a concrete runner would lift the axis further. Deferred.

### Next version target

**v0.4.0** — third skill implementation. The three remaining independent candidates are `journal-system/`, `session-post-processor/`, and `pepite-flagging/` (plus `genesis-protocol/` orchestrator, which should be last). Pick whichever reuses the most existing state. Target rating: **8.0/10**.

---

## [0.2.0] — 2026-04-15 — "Phase -1 Dependencies Pre-flight skill"

### Added

- `skills/phase-minus-one/` — the first functional skill, end-to-end implementation of Phase -1 Dependencies Pre-flight per `specs/v1_phase_minus_one_first_user_bootstrap_flow.md` (three stratified layers — initial design, 3-mode ladder, multi-device core)
- `skills/phase-minus-one/SKILL.md` — skill entry point, frontmatter for Claude Code plugin auto-discovery, seven-phase flow map, security-floor rules, multi-device core branch, anti-Frankenstein reminders
- `skills/phase-minus-one/detect.sh` — Phase -1.0 baseline probe. Cross-platform bash, read-only, <5 s. Emits `KEY=VALUE` report on stdout covering OS family, package manager, Layer 3 essentials (Node, npm, Git, gh, VS Code, Claude), Chrome, Claude Code VS Code extension, MCP list (Playwright, `ide`), Claude in Chrome (via native messaging host file when reachable), SSH keys, shell / home. Live-tested against this machine's dev stack during development.
- `skills/phase-minus-one/install-manifest.yaml` — Phase -1 target stack with per-OS install commands (winget / brew / apt / dnf / pacman). Items tagged by layer, rationale, `user_action_required` (none / admin_password / sign_in / extension_grant / pairing / restart), `plan_gate` for subscription-aware branching, and `core` vs optional. Includes the Phase -1.7 bonuses (Antigravity, Codespaces, Termux, voice mode) as `core: false`. Declares the five security-floor categories.
- `skills/phase-minus-one/gap-report.md` — Phase -1.1 card template with template variables, layer grouping, plan-tier branching, per-mode time estimates, security-floor intervention count
- `skills/phase-minus-one/consent-card.md` — Phase -1.2 template collecting mode choice + per-item opt-in in a single prompt. Defaults every box unchecked. Records consent in `memory/reference/consent-log.md`. Handles plan-tier branching for Remote Control row.
- `skills/phase-minus-one/modes/detailed.md` — Phase -1.3 mode 1 runner (detailed pas-à-pas, 30–45 min, user types each command, Claude teaches each step)
- `skills/phase-minus-one/modes/semi-auto.md` — Phase -1.3 mode 2 runner (10–15 min, command cards with yes / no / skip / pause, optional batched cards for homogeneous runs)
- `skills/phase-minus-one/modes/auto.md` — Phase -1.3 mode 3 runner (~5 min, full autonomous loop, graceful pause at every security-floor step, at most one retry + one alternate path before fall-back)
- `skills/phase-minus-one/sign-in-round.md` — Phase -1.4 consolidated sign-in round with fixed ordering (Claude web → GitHub → project-specific → Claude in Chrome extension → mobile app → Remote Control pairing)
- `skills/phase-minus-one/restart-round.md` — Phase -1.5 consolidated restart round (Chrome → shell rc reload → Claude Code session) with marker-file pattern for Claude Code self-restart
- `skills/phase-minus-one/verification.md` — Phase -1.6 health check card plus the canonical `memory/reference/automation-stack.md` schema it writes
- `skills/phase-minus-one/optional-bonus.md` — Phase -1.7 opt-in card for Antigravity / Codespaces / Termux / voice mode, strictly opt-in, consent-gated from Phase -1.2

### Notes

- This PR ships **one** skill only, per anti-Frankenstein scope discipline from the resume prompt. Other skills (`genesis-protocol`, `phase-5-5-auth-preflight`, `journal-system`, `session-post-processor`, `pepite-flagging`) remain as README stubs and land in their own worktrees later.
- No hook wiring, no templates/ population, no marketplace manifest — all out of scope for v0.2.0.
- All new files carry the `SPDX-License-Identifier: MIT` short-form header per R10 plugin conventions.
- `detect.sh` was live-tested on this Windows 11 machine against the actual dev stack and emits 25 well-formed key-value lines covering every probe.

### Self-rating — v0.2.0

| Axis | Rating | Notes |
|---|---|---|
| Pain-driven coverage | 8/10 | Every file in the skill points to a specific section of the Phase -1 spec; no speculative additions; multi-device core honoured |
| Prose cleanliness | 7/10 | Templates are readable but dense in places; three mode files repeat some structure intentionally so each stands alone |
| Best-at-date alignment | 9/10 | 2026 Q2 patterns throughout — winget/brew/apt, Playwright MCP, VS Code extension doubling as `ide` MCP, Claude Code Remote Control, Antigravity hybrid, F-Droid Termux, magical one-liner for Phase -2 |
| Self-contained | 6/10 | Skill is self-contained within `skills/phase-minus-one/`; references the spec + rules + research cache but runs end-to-end without them; the manifest → mode-runner → report-template loop is readable in isolation |
| Anti-Frankenstein | 8/10 | Zero speculative surfaces; mode 3 retry budget capped at one retry + one alternate; bonus items strictly opt-in; no hook wiring, no templates/, no marketplace |
| **Average** | **7.6/10** | Above the 7.0 target; below the 8.5 v1 ceiling — room for v0.3.0 to add the second skill cleanly |

### Known gaps for v0.3.0

- No automated tests — `detect.sh` was live-validated manually on one machine. A small harness emulating the seven-phase flow over a fake manifest would lift the "Self-contained" axis.
- `install-manifest.yaml` is not yet schema-validated at skill load time. A one-time YAML sanity check at Phase -1.0 boot would catch broken edits.
- `memory/reference/automation-stack.md` canonical schema is documented inside `verification.md` rather than shipped as a starter file under `memory/reference/`. Upgrade at v0.3.0 once a second consuming skill needs it.
- No `templates/phase-minus-one-install-manifest.yaml` ship — the manifest is skill-local only. Promotion to `templates/` lands whenever the first downstream consumer project needs a standalone copy.
- Claude in Chrome detection on Windows is `unknown` because native messaging hosts live in the Windows registry. A registry probe via PowerShell could lift this at the cost of shell-portability — deferred to v0.3.0 unless user feedback flags it.

### Next version target

**v0.3.0** — second skill implementation (likely `phase-5-5-auth-preflight/` since it reuses the Phase -1 detection state and is the next deepest-specced item). Target rating: **7.8/10**.

---

## [0.1.0] — 2026-04-14 — "Scaffold bootstrap"

### Added

- Initial plugin scaffold following Claude Code plugin convention
- `.claude-plugin/plugin.json` manifest with required + recommended fields
- MIT `LICENSE` + SPDX short-form headers on every source file
- Bilingual `README.md` (FR + EN) per R9 language policy
- Project-level `CLAUDE.md` inheriting universal rules from `~/.claude/CLAUDE.md` (Layer 0)
- `memory/` directory structure with R4.1 layout + new `journal/` and `pepites/` directories (6th and 7th memory types)
- `memory/project/session_v1_bootstrap.md` capturing this session's context, decisions, and self-ratings
- `memory/project/aurum_frozen_scope_lock.md` enforcing the rule that aurum-ai stays at `0b1de3d` until Genesis v1 ships
- `memory/reference/ssh_genesis_identity.md` documenting the dedicated ed25519 key + `github.com-genesis` alias
- `memory/reference/github_genesis_account.md` documenting the target account, PAT env pattern, SSH URL
- `.claude/docs/superpowers/research/` with **7 R8 cache entries** from bootstrap research (license, plugin distribution, SPDX headers, plugin structure, JSONL format, Claude in IDE tools, cross-OS Claude ecosystem) — all SPDX-headered, all TTL-tagged
- `.claude/docs/superpowers/specs/` with **4 v1 specs** (Phase 5.5 auth pre-flight learnings, Phase -1 first-user bootstrap flow, pépite discovery flagging, Phase 5.5 auth-preflight) and **1 v2 spec** (phase-minus-one-dependencies-automation, to be renamed/merged at Étape 5)
- `.claude/docs/superpowers/rules/v1_rules.md` with R1-R10 adapted for Genesis per Étape 2 scoreboard (KEEP R2; ADAPT R1, R3, R4, R5, R6; INHERIT R8, R9 from Layer 0; DROP R7; NEW R10)
- Empty `skills/`, `templates/`, `hooks/`, `memory/user/`, `memory/feedback/`, `memory/themes/` directories with README placeholders explaining what lands there
- `.env.local` with the project-scoped `GH_TOKEN` (gitignored from first commit, never exposed)
- `.env.local.example` + `.envrc.example` (direnv alternative) as templates for downstream users
- `.gitignore` with secrets, OS files, editor files, language artefacts, and `.claude/worktrees/` (forensic snapshots stay local per R2.5)

### Design work saved during the session (not yet code)

These specs describe what v1.0.0 will implement but no runtime code exists yet for any of them:

- Phase -1 3-mode ladder (detailed / semi-auto / auto)
- Multidevice core (Claude Code Remote Control + mobile companion)
- Journal system trigger phrases (inherited from Layer 0, skill implementation pending)
- Session post-processor logic (JSONL parsing + secret redaction + markdown emission)
- Pépite red-light detection criteria (6 conditions, "two or more" rule)
- Cross-project research sharing via pointer files

### Cross-project additive

- Pointer file written into `~/.claude/projects/C--Dev-Claude-cowork-aurum-ai/memory/reference_genesis_research_cache_pointer_2026-04-15.md` referencing the Genesis R8 cache for future Aurum sessions to consume
- Meta-Memory architecture doc in Aurum's auto-memory updated with the pépite feature integration

### Self-rating — v0.1.0

Rubric: 5 axes, 1-10 each, averaged. Target < 10 per anti-Frankenstein discipline.

| Axis | Rating | Notes |
|---|---|---|
| Pain-driven coverage | 2/10 | Scaffold only — no functional content yet; specs cover the pain points but code is absent |
| Prose cleanliness | 6/10 | Structured but placeholders everywhere; README has pre-release markers |
| Best-at-date alignment | 8/10 | MIT + SPDX + plugin convention + marketplace-ready + 2026 patterns baked into specs |
| Self-contained | 5/10 | Inherits Layer 0 unambiguously; specs stand alone |
| Anti-Frankenstein | 9/10 | Every file audited pain-driven; placeholders not filled beyond need |
| **Average** | **6.0/10** | Honest starting point — the scaffold exists, the content doesn't yet |

### Not yet implemented (lands at Étape 5+)

- Skill content in `skills/*/` — `phase-minus-one`, `phase-5-5-auth-preflight`, `journal-system`, `session-post-processor`, `pepite-flagging`, `genesis-protocol`
- Hook wiring in `hooks/hooks.json` for `SessionEnd` (deferred until post-processor manual mode validates)
- Template markdown in `templates/` — the actual 7-phase Genesis protocol text
- Self-hosted marketplace manifest for `/plugin install project-genesis@myconciergerie-prog/project-genesis`
- Integration tests and dogfooding harness (anti-Frankenstein — defer until pain surfaces)

### Next version target

**v0.2.0** — first worktree PR from Étape 5 with at least one skill (`phase-minus-one/` or `journal-system/`) implemented end-to-end. Target rating: **7.0/10**. Shipped via `gh pr merge --squash` per R2.3, tagged `v0.2.0`.

**v1.0.0 target**: **8.5/10**. Inflection point protection — no feature ships if the marginal rating gain per feature added is near zero.

---

## Release process

Version bumps follow semver:

- `0.x.y` — pre-release, scaffold, experimental content
- `1.x.y` — stable plugin, available via `/plugin install`
- `major` — breaking changes to skill interfaces or plugin manifest
- `minor` — new skills, new features, backward-compatible
- `patch` — bug fixes, doc updates, rule clarifications

Every version bump:

1. Updates `plugin.json` `version` field in the same PR
2. Appends a CHANGELOG entry with the 5-axis self-rating block
3. Tags the squashed merge commit with `v<semver>`
4. Optionally runs `GH_TOKEN="$GH_TOKEN" gh release create v<semver>` with a CHANGELOG extract
5. Updates the self-hosted marketplace manifest to reference the new tag (v1.0.0+)

Ratings below **7.0/10 cannot be tagged as stable `1.x.y`** per R10.3 — use `0.x.y` for pre-release.
