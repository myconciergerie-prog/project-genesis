<!-- SPDX-License-Identifier: MIT -->

# skills/

This directory holds the skills that Project Genesis ships. Per Claude Code plugin convention (2026), `skills/` is at the plugin root level — **NOT** inside `.claude-plugin/`. Only `plugin.json` lives in `.claude-plugin/`.

## Shipped skills — v1.6.0 (8 skills)

Each skill's entry below links it to the pain point / spec that motivated it and the version it shipped in. The original v1 set (six skills) landed v0.1–v0.8 and was complete at v0.8.0 with the `genesis-protocol` orchestrator (pure-Markdown Option A). `genesis-drop-zone` shipped v1.3.0 as the first Layer A vertical slice. `promptor` shipped v1.6.0 as the first orthogonal meta-skill (neither Layer A nor Layer B).

- **`genesis-protocol/`** — **shipped v0.8.0**. The 7-phase protocol orchestrator, pure Markdown (Option A) conductor composing the five sibling skills into a single `/genesis-protocol` invocation. Eight files: `SKILL.md` with the 7-phase master table (1:1 mirror of `memory/master.md`), four phase runbooks (`phase-0-seed-loading.md`, `phase-1-rules-memory.md` covering phases 1+2, `phase-3-git-init.md` covering phases 3+4, `phase-6-commit-push.md` covering phases 6+7), one thin skill-pointer file (`phase-5-5-auth.md`), a verification-only `install-manifest.yaml` that checks sibling skills are present, and a two-mode `verification.md` with per-phase post-action checks. The orchestrator reimplements nothing — it invokes existing skills at the right phase, threads their outputs, and emits a single genesis report. One concentrated privilege (writing outside the Genesis repo), mitigated by the top-level consent card.
- **`phase-minus-one/`** — Dependencies Pre-flight. Detects OS, package manager, existing stack, gaps. Presents gap report card. Offers 3-mode ladder (detailed pas-à-pas / semi-auto / auto). Runs installs via `winget` / `brew` / `apt`. Handles the batched sign-in round and batched restart round. Multidevice core per `specs/v1_phase_minus_one_first_user_bootstrap_flow.md`.
- **`phase-5-5-auth-preflight/`** — Auth Pre-flight checklist implementation. SSH keygen + `~/.ssh/config` alias. Fine-grained PAT creation walkthrough with the full scope list (Contents RW, Metadata R, PR RW, Workflows RW, Administration RW). Empty repo creation pattern via web UI paste-back. Three-probe pre-flight test (SSH + `gh api user` + `gh api repos/.../.../`). Branches on Playwright MCP availability for automation vs paste-back.
- **`journal-system/`** — Stratified thought capture. Trigger phrases recognizer (`ouvre / reprends / enregistre / enrichis / clôture la pensée sur X`). Entry creator with YAML frontmatter and stratified dialogue format. Amplification-on-consent handler. State transition manager (`seed` → `growing` → `dormant` → `resolved` | `captured`). See Layer 0 for the full journal spec.
- **`session-post-processor/`** — Reads Claude Code's native JSONL transcripts from `~/.claude/projects/<slug>/<uuid>.jsonl`. Parses typed message records chained by `parentUuid`. Runs secret redaction pass (regex patterns for `github_pat_`, `ghp_`, `sbp_`, `sb_secret_`, `sk_`, JWT, AWS keys). Emits Markdown transcript with frontmatter to `.claude/docs/superpowers/sessions/YYYY-MM-DD_<slug>.md`. Updates `sessions/INDEX.md` with a one-line entry. Optional `SessionEnd` hook wiring deferred to v1.1.0.
- **`pepite-flagging/`** — Red-light detection during research. The 6 criteria with "two or more" rule. Pépite entry creator with routing metadata (`origin_project` / `transverse` / `specific_projects`). Cross-project pointer writer. Surfacing card generator for user prompts. Status transition handler (`seed` → `extracted` / `actioned` / `archived` / `dismissed`). Full spec in `.claude/docs/superpowers/specs/v1_pepite_discovery_flagging.md`.
- **`genesis-drop-zone/`** — **shipped v1.3.0 (welcome vertical slice)**. First Layer A (conversational) skill of Genesis v2. Prints the unified drop-zone welcome box (FR by default, EN mirror-ready), streams a reformulated acknowledgement of what the user gave, closes with an honest bilingual bridge message. Concentrated privilege: `none`. Extraction, `bootstrap_intent.md` write, and handoff to `genesis-protocol` deferred to v1.3.1+. 1:1 mirror of `.claude/docs/superpowers/specs/v2_etape_0_drop_zone.md`.
- **`promptor/`** — **shipped v1.6.0**. Production-grade Anthropic system-prompt template (Claude Opus 4.7 1M + MCP, two-phase, KV-cache optimized). Privilege class: `none`. Orthogonal to Layer A / Layer B (meta-tool, invocable cross-session and cross-project outside the bootstrap protocol). Two files: `SKILL.md` invocation gate + `references/template.md` canonical XML + 6 architectural principles + adaptation points + when-not-to-use + cross-project utility. 1:1 mirror of Layer 0 pépite `~/.claude/memory/layer0/pepite_promptor_template_anthropic_prompt_engineering.md` (skill is canonical source of truth ; pépite is synced cache for sessions outside Genesis-bootstrapped projects).

## Claude Code skills convention (Q2 2026 reminder)

- Every skill gets a `/<skill-name>` slash-command interface automatically
- Skills are recommended over `.claude/commands/` for new plugins (commands still work for backward compatibility)
- Auto-discovery: Claude Code loads everything under `skills/` without manifest-level paths in `plugin.json` — keep standard directory names
- Each skill is a subdirectory with its own content (markdown prompts, Python / shell scripts, optional assets)

Refer to `.claude/docs/superpowers/research/stack/claude-code-plugin-structure_2026-04-14.md` for the full plugin layout spec.

## Anti-Frankenstein reminder

No skill ships without a documented pain point it addresses. Every skill above points to a specific `specs/` file or a specific feedback memory from the Aurum v0_init session. Speculative skills are rejected by default per R10.4.
