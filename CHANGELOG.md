<!-- SPDX-License-Identifier: MIT -->

# Changelog

All notable changes to Project Genesis are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versioning follows [Semantic Versioning](https://semver.org/).

Every version bump includes a **5-axis self-rating block** per R10.3 discipline, with target < 10 to honor the anti-Frankenstein inflection-point rule.

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
