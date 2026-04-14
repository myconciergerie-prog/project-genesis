<!-- SPDX-License-Identifier: MIT -->

# Changelog

All notable changes to Project Genesis are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versioning follows [Semantic Versioning](https://semver.org/).

Every version bump includes a **5-axis self-rating block** per R10.3 discipline, with target < 10 to honor the anti-Frankenstein inflection-point rule.

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
