<!-- SPDX-License-Identifier: MIT -->

> **Forensic preservation** : halt-with-remediation card content from v1.5.0, retired in v2.0.0 because subprocess Citations path no longer exists. Preserved for historical reference and v1.4.x/v1.5.x re-derivation if needed.

> **Extraction scope note** : copied verbatim from `skills/genesis-drop-zone/SKILL.md` lines 401-425 (section `### Halt-with-remediation card` through `Future-proofing note`, inclusive). Stops before `### Consent-card interaction with Phase 0.5` which is a separate dispatch clarification not specific to the halt card itself.

---

### Halt-with-remediation card

When the extractor exits with code 2-7, the dispatch layer renders the bilingual halt card (paired-authored in `phase-0-welcome.md`). The card content names the failure class explicitly so Victor knows what to fix.

**Why an API key (and not a Claude Max subscription)** — Anthropic intentionally separates two billing surfaces and identities:

- **Claude Max ($200/mo subscription)** covers `claude.ai` web app + Claude Desktop + Claude Code CLI inference. Pays for human-driven Claude conversations.
- **API key** (`sk-ant-...` from `console.anthropic.com`) bills per-token to a workspace. Pays for programmatic Messages API / Citations / Files calls — including the Genesis drop-zone Citations extractor subprocess.

The two are intentionally distinct — research-confirmed `.claude/docs/superpowers/research/sota/anthropic-auth-and-oauth-status_2026-04-19.md`. Even on April 19, 2026, no public OAuth path lets a third-party app (including Genesis) use a subscription identity for Messages API. The halt card surfaces this honestly rather than degrading silently.

Per-failure-class card content (v1.5.1 taxonomy — collapsed from 6 distinct cards × 2 langs = 12 variants in v1.5.0 to 2 distinct cards × 2 langs = 4 variants per dogfood Friction #4 + Friction #1 anti-Frankenstein retroactive). Full bilingual templates in `phase-0-welcome.md`:

| Exit code | Card | Remediation summary |
|---|---|---|
| 2 `EXIT_NO_KEY` | **EXIT_NO_KEY card** — distinct | Console deep-link, `setx`/`.zshenv` persistent one-liners, escape hatches, env-scrub warning. Addresses highest-pain user-facing surface (subscription ≠ API confusion). |
| 3-7 (all other exits) | **Generic internal-error card** — merged | Title names the extractor class via stderr, directs to GitHub issue template at `https://github.com/myconciergerie-prog/project-genesis/issues`, one-line stderr-excerpt capture guidance, `GENESIS_DROP_ZONE_VERBOSE=1` diagnostic env var. |

**Why collapsed** — dogfood v1.5.0 on 2026-04-19 surfaced that EXIT_SDK_MISSING vs EXIT_API_ERROR vs EXIT_RATE_LIMIT vs EXIT_BAD_INPUT vs EXIT_OUTPUT_INVALID are all operationally-opaque "something broke internally" from Victor's perspective; Fixture D runtime distinction was unverifiable within 2h timebox. Keeping them as 5 distinct bilingual variants cost 10 bilingual templates for zero user benefit. The stderr still reports the precise extractor class for forensic diagnostic — the script's 6 distinct exit codes are preserved; collapse is at the render layer only. See § "Candidate 2 — Halt-card taxonomy collapse" in `specs/v1_5_1_dogfood_and_prose.md` for the full rationale.

**Footer note** (always rendered, both languages): "the Claude Code (Max) subscription does NOT grant API access. The Anthropic API key is a separate product, billed per-token at the workspace level — see https://console.anthropic.com/settings/keys".

The card prints in `content_locale` order. After printing, the dispatch layer halts (no fallback, no retry, no in-context degradation). Victor fixes the cause and re-runs `/genesis-drop-zone`.

**Future-proofing note**: a future Claude Code release may default `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB=1`, scrubbing `ANTHROPIC_API_KEY` from subprocess env at extractor invocation time. To survive that change, the env var MUST be set at the **OS / shell profile level** (`setx` Windows / `.zshenv` POSIX), NOT just in the current Claude Code session.
