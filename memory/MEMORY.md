<!-- SPDX-License-Identifier: MIT -->

# MEMORY — Project Genesis

Index of project-level memory for Project Genesis. **Always loaded at session open** per R1.1.

## Layer 0 inheritance

This project inherits all universal rules, user profile, hard rules, workflow patterns, and machine-specific reference from `~/.claude/CLAUDE.md` (Layer 0) **by reference**. See the project-level `CLAUDE.md` at the repo root for the pointer rules. This memory index does NOT duplicate Layer 0 content.

## Master

- [Master vision + stack + rules summary](master.md) — the stable project vision; read at every session open

## User

- [user/ README](user/README.md) — user profile is centralized in Layer 0; project-specific user notes would land here if they arise

## Feedback

- [feedback/ README](feedback/README.md) — universal feedback rules inherited from Layer 0; project-specific feedback would land here if it diverges

## Project

- [Session v1 bootstrap — 2026-04-14](project/session_v1_bootstrap.md) — origin session context, decisions frozen, self-ratings, forward map
- [Session v0.2.0 — 2026-04-15](project/session_v0_2_0_skill_phase_minus_one.md) — Phase -1 skill shipped end-to-end, v0.2.0 tagged at 7.6/10, gaps logged for v0.3.0
- [Session v0.3.0 — 2026-04-15](project/session_v0_3_0_skill_phase_5_5_auth_preflight.md) — Phase 5.5 Auth Pre-flight skill shipped end-to-end, v0.3.0 tagged at 8.2/10, gaps logged for v0.4.0
- [Session v0.4.0 — 2026-04-15](project/session_v0_4_0_skill_journal_system.md) — Journal system skill shipped end-to-end after recovery from lost PowerShell-window attempt, v0.4.0 tagged at 8.8/10, gaps logged for v0.5.0
- [Session v0.5.0 — 2026-04-15](project/session_v0_5_0_skill_session_post_processor.md) — Session post-processor skill shipped with halt-on-leak gate, R8 research refresh as prerequisite, first granular-commit discipline application (8 commits in feat branch), v0.5.0 tagged at 8.4/10, gaps logged for v0.6.0
- [Session v0.6.0 — 2026-04-15](project/session_v0_6_0_runpy.md) — Session post-processor run.py executable shipped (first runnable Python in Genesis), dogfood run 2/3 CLEAN, halt-on-leak gate proven live via `--inject-test-leak`, first live-dogfood correction of an R8 entry (slug underscore rule), v0.6.0 tagged at 8.6/10, gaps logged for v0.7.0
- [Session v0.7.0 — 2026-04-15](project/session_v0_7_0_pepite_flagging.md) — Pepite flagging skill shipped (6 files, 1:1 spec mirror, consent floor on cross-project pointer writes), R8 slug rule amended in-place (first live-dogfood amend precedent), v0.7.0 tagged at 8.8/10 (ties highest single-version rating), running average 8.40/10, one stub remaining (genesis-protocol orchestrator = v1.0.0 candidate)
- [Session v0.8.0 — 2026-04-16](project/session_v0_8_0_genesis_protocol.md) — Genesis-protocol orchestrator shipped (8 files, ~1,400 lines, Option A pure Markdown, 1:1 mirror of master.md's 7-phase table, concentrated-privilege map with 6 data points, third 1:1 spec mirror), v0.8.0 tagged at **9.0/10** (new single-version high), **running average 8.49/10 — 0.01 below v1 target** → user picked **Path A (v0.9.0 polish → v1.0.0)** with explicit "leverage memory/meta-memory context" framing. Zero stubs remaining; full v1 skill surface complete
- [Session v0.9.0 — 2026-04-16](project/session_v0_9_0_polish.md) — Path A polish: dry-run walkthrough (10 findings, 5 fixed), meta-memory visibility in `master.md`, README rewrite, dogfood run 3 GREEN. v0.9.0 tagged at **8.92/10**, **running average 8.54/10 — 0.04 above v1 target**. Ship gate cleared. v1.0.0 next
- [Dry-run walkthrough — 2026-04-16](project/dryrun_walkthrough_2026-04-16.md) — paper trace of the genesis-protocol orchestrator against `C:\tmp\genesis-dryrun\` (10 findings, 5 med fixes landed in v0.9.0, 5 low deferred to v1.1)
- [Aurum frozen scope lock](project/aurum_frozen_scope_lock.md) — hard rule that aurum-ai repo stays at `0b1de3d` until Genesis v1 ships; no aurum-ai commits / PRs / edits allowed in any Genesis session
- [Session v1.1 selfdogfood — 2026-04-16](project/session_v1_1_selfdogfood.md) — first real genesis-protocol execution, hit auth wall at Phase 3.4, pivoted to analysis, produced v2 Promptor fusion vision (9.2/10)
- [Self-dogfood friction log — 2026-04-16](project/selfdogfood_friction_log_2026-04-16.md) — 18 frictions (5 STRUCTURAL in auth), Victor test birth, Promptor fusion discovery, v2 vision trigger
- [Session v1.2.0 self-dogfood — 2026-04-17](project/selfdogfood_friction_log_v1_2_0_2026-04-17.md) — conscious strange-loop self-dogfood, 14 new frictions (F20-F34), two pépite-worthy findings (F29 plugin-install broken + Promptor attribution correction), v2 Étape 0 drop-zone surfaced
- [Session v1.2.1 paradox guards — 2026-04-17](project/session_v1_2_1_paradox_guards.md) — three P0 fixes from v1.2.0 landed surgically: F29 skill-self-contained rules, F30 git-aware nested-repo probe, F23+F27 Step 0 paradox guards. One follow-up commit for git-bash path normalization. v1.2.1 tagged
- [Session v1.2.2 mode-auto args — 2026-04-17](project/session_v1_2_2_mode_auto_args.md) — P1 cluster bundled in one PR: F21 `## Arguments` section, F20 mode is first-class argument (detailed/semi-auto/auto), F22 Step 0 consent card dispatches per mode. Three phase runbooks reference the canonical `## Mode dispatch` table. v1.2.2 tagged at **9.14/10**, third consecutive ≥ 9.0 ship. F34 named as v1.2.3 target
- [Session v1.2.3 F34 gh pre-flight — 2026-04-17](project/session_v1_2_3_f34_gh_preflight.md) — last P1 landed. Step 6.0 `gh api user --jq .login` + auto-switch + halt-with-remediation at opening of Phase 6; SKILL.md Mode dispatch Category A catalogue sync; R8 archive of 2 expired stack entries. F34 **live-reproduced on the ship of v1.2.3 itself** — gh active account was `myconciergerieavelizy-cloud` while target owner was `myconciergerie-prog`, `gh auth switch` resolved it exactly as Step 6.0 specifies. v1.2.3 tagged at **9.18/10**, running average **8.71/10**. P1 queue from v1.2.0 now CLOSED
- [Session v1.2.4 R2.3.1 rule-level gh pre-flight — 2026-04-17](project/session_v1_2_4_rule_gh_preflight.md) — F34 rule-level mirror. R2.3.1 added under R2.3 PR & merge in `skills/genesis-protocol/rules/v1_rules.md`, byte-for-byte structurally identical to Step 6.0 branches (halt / auto-switch / re-verification), simpler owner resolution (single source: `git remote get-url origin`, no fallbacks needed in v0.2.0+ sessions). 1:1 mirror discipline extended from spec pairs to rule/runbook pairs. Two-commit bundle in one PR: feat (+61 / −2) + chore. v1.2.4 tagged at **9.16/10**, running average **8.74/10**. **Fourth consecutive ≥ 9.0 ship**. P1 coverage now at both bootstrap AND downstream-rule levels
- [Session v1.3.0 genesis-drop-zone welcome slice — 2026-04-17](project/session_v1_3_0_drop_zone_welcome.md) — first MINOR bump since v1.2.0, opens the v1.3.x conversational-layer line. New sibling skill `genesis-drop-zone` (Layer A) with SKILL.md + phase-0-welcome.md, 1:1 mirror of new implementation spec `v2_etape_0_drop_zone.md`. Welcome + token-streamed acknowledgement + bilingual bridge vertical slice; extraction / bootstrap_intent.md write / handoff deferred to v1.3.1+. Cross-skill-pattern #4 = Layer A / Layer B stratification named in master.md. Concentrated privilege `none` (journal-system precedent). Inline R8 citations broke the 8.6–8.8 Best-at-date PATCH-cycle ceiling. v1.3.0 tagged at **9.34/10**, running average **8.78/10**. **Fifth consecutive ≥ 9.0 ship**
- [Session v1.3.1 genesis-drop-zone extraction mirror — 2026-04-17](project/session_v1_3_1_extraction_mirror.md) — first PATCH on the v1.3.x line. Upgrades v1.3.0's bullet-list acknowledgement into a structured 9-field aligned-column mirror screen driven by in-context extraction (no API call, no disk write). Bridge updated ("Création du projet (GitHub, fichiers, mémoire) arrive bientôt"). Living-spec pattern: `v2_etape_0_drop_zone.md` extended with version-scoped sections. Concentrated privilege stays `none` across both versions; first Layer A privilege ship queued for v1.3.2 (bootstrap_intent.md write). Six-commit rhythm (spec + spec polish + plan + plan polish + feat + chore), two reviewer passes. v1.3.1 tagged at **9.30/10**, running average **8.81/10**. **Sixth consecutive ≥ 9.0 ship**
- [Session v1.3.2 genesis-drop-zone write + Layer B handoff — 2026-04-18](project/session_v1_3_2_write_layer_b_handoff.md) — first Layer A concentrated privilege shipped (writes `drop_zone_intent.md` to cwd after bilingual consent card, halt-on-existing, no mkdir) + first cross-layer wire live (genesis-protocol Phase 0 detects + parses + consumes with precedence over config.txt). Two version-scoped bridges (accept / decline). Layer A file renamed to `drop_zone_intent.md` to avoid collision with Layer B's `memory/project/bootstrap_intent.md`. Cross-skill-pattern #4 reference implementation. One PR touches two skills in one worktree. Six-commit rhythm, two reviewer passes, five mitigations shipped one-for-one with the privilege. v1.3.2 tagged at **9.28/10**, running average **~8.84/10**. **Seventh consecutive ≥ 9.0 ship**
- [Session v1.3.3 genesis-drop-zone runtime locale rendering — 2026-04-18](project/session_v1_3_3_runtime_locale.md) — R9 tier-3 rendering loop closed end-to-end. Runtime locale dispatch via two variables with distinct lifecycles (`welcome_locale` from trigger phrase language; `content_locale` from extracted `langue_detectee` with `mixte` → FR tiebreaker). Seven surfaces switch from hardcoded FR / always-bilingual to locale-detected one-variant-at-a-time. One new bilingual pair (EN zero-content re-prompt). **Zero Layer B ripple** by deliberate design — frontmatter null-class tokens stay FR canonical so `genesis-protocol` Step 0.2a parser is untouched. Intentional Layer A / Layer B asymmetry: body = locale-detected human echo; frontmatter = FR canonical data contract. No new privilege class. One PR, one skill touched. Six-commit rhythm (fourth consecutive), two reviewer passes (3+3 advisories all landed). v1.3.3 tagged at **9.30/10**, running average **~8.87/10**. **Eighth consecutive ship ≥ 9.0**
- [Session v1.4.0 genesis-drop-zone Citations API extraction — 2026-04-18](project/session_v1_4_0_citations_api.md) — **First MINOR bump since v1.3.0** opened the v1.3.x conversational-layer line. **Second concentrated privilege class** for `genesis-drop-zone`: network (Anthropic Messages API via Python subprocess at `skills/genesis-drop-zone/scripts/extract_with_citations.py` with `citations: {enabled: true}` + explicit `cache_control: ttl:1h`). **Cross-skill-pattern #2 refined** from "at most one privilege per skill" to "at most one privilege per operation class, per skill" — first multi-class declaration in Genesis (disk + network, each with its own consent model + five mitigations + independent-disableability). Mirror renders `[page N]` / `[lines X-Y]` annotations when API path runs; `drop_zone_intent.md` frontmatter gains optional `<field>_source_citation` nested keys (omitted when no citation). **Silent graceful fallback** to v1.3.3 in-context extraction on any failure class (unset API key, missing SDK, API error, rate limit, bad input, output invalid) — no user-facing informational note. **Zero Layer B ripple preserved via additive frontmatter keys** — `schema_version` stays at `1`; Layer B Step 0.2a dict-based parser naturally ignores unknown keys. Three fixtures (FR + EN with citations + fallback byte-identical to v1.3.3 EN modulo `skill_version` via Python binary-mode CRLF-preserving copy). New R8 stack entry `anthropic-python_2026-04-18.md` pinning `anthropic>=0.40.0`. Typed-text wrapping rule at `documents[]` index 0 as synthetic citations-enabled document block. Six-commit rhythm (fifth consecutive), two reviewer passes (4+4 advisories all landed). v1.4.0 tagged at **9.10/10** (Self-contained 8.9 honest MINOR-bump surface growth, floor ≥ 9.0 on 4/5 axes), running average **≈8.88/10**. **Ninth consecutive ship ≥ 9.0**

## Reference

- [SSH identity — Project Genesis](reference/ssh_genesis_identity.md) — dedicated `~/.ssh/id_ed25519_genesis` + `github.com-genesis` alias in `~/.ssh/config`, fingerprint and git remote URL
- [GitHub account target — Project Genesis](reference/github_genesis_account.md) — `myconciergerie-prog/project-genesis`, PAT env pattern, SSH URL binding, Chrome Profile 2 for web UI

## Themes

- [themes/ README](themes/README.md) — empty; themes populated as the project grows and multi-entry patterns emerge

## Journal

- [Journal INDEX](journal/INDEX.md) — stratified thought capture (6th memory type per Layer 0 journal system spec). **First entry 2026-04-15** (seed): slug rule live-dogfood correction

## Pépites

- [Pépites INDEX](pepites/INDEX.md) — gold nugget discoveries with cross-project routing metadata (7th memory type per `specs/v1_pepite_discovery_flagging.md`); no entries yet, flagged automatically during research when red-light criteria match

## Pointers to dev-internal docs (not memory, but related)

- `skills/genesis-protocol/rules/v1_rules.md` — R1-R10 for this project (adapted from Aurum v1); relocated from `.claude/docs/superpowers/rules/` in v1.2.1 to make the `genesis-protocol` skill self-contained (friction F29)
- `.claude/docs/superpowers/research/INDEX.md` — R8 research cache with TTL, 7 active entries as of bootstrap
- `.claude/docs/superpowers/specs/` — design specs (4 v1 specs + 1 v2 spec captured during bootstrap)
- `.claude/docs/superpowers/plans/` — implementation plans
- `.claude/docs/superpowers/resume/` — session handoff prompts
