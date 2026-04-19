---
name: v2 — Bootstrap via Max subscription, Phase anthropic_auth
description: Architectural shift — drop v1.4.0 subprocess Citations API + anthropic SDK + ANTHROPIC_API_KEY dependency. Bootstrap leverages the Max subscription that Claude Code already holds at session open via the same `claude auth login` flow that authenticates the current Claude Code session itself. New Phase anthropic_auth as a pre-flight check + remediation guide. v1.5.0's halt-with-remediation card becomes obsolete. Backward-compatible at data contract level (existing `drop_zone_intent.md` files remain parseable). Vision sections capture v3 external-installer + BYOAI + Lovable-style hosted SaaS for design orientation.
type: spec
version_target: TBD-by-user (v1.7.0 MINOR or v2.0.0 MAJOR)
created: 2026-04-19
status: design-pending-review
predecessor_specs:
  - v1.4.0 — `genesis-drop-zone` Citations API extractor
  - v1.5.0 — fallback retirement + halt-with-remediation card
research_anchors:
  - .claude/docs/superpowers/research/sota/anthropic-auth-and-oauth-status_2026-04-19.md
brainstorm_session: 2026-04-19 (post-v1.6.3, post-D-pré-flight)
---

# v2 — Bootstrap via Max subscription : Phase anthropic_auth

## TL;DR

Genesis is a Claude Code plugin. Claude Code is already authenticated to Anthropic (Max subscription) at session open via `claude auth login`. **The Citations API subprocess added in v1.4.0 is the only Genesis component that bypassed this auth and required a separate Console `ANTHROPIC_API_KEY`.** v2 drops that subprocess. All extraction reverts to in-context (as in v1.3.x) under the parent Claude Code's Max auth. A new Phase anthropic_auth runs as a pre-flight check : detects auth status via `claude auth status --json`, guides the user through `claude auth login` if not authed, then hands off to Genesis Phase 0.

## Why this design now

### Pain point — the v1.4.0 → v1.5.0 trap

- **v1.4.0** added the Citations API subprocess for provenance metadata (`[page N]` / `[lines X-Y]` markers) — required `ANTHROPIC_API_KEY` from a Console workspace, separate from the user's Max subscription.
- **v1.5.0** retired the silent fallback to in-context extraction (correctly anti-Frankenstein per R8 `anthropic-auth-and-oauth-status_2026-04-19.md` — no first-party OAuth bridge for Messages API, Max ≠ API by Anthropic design, OpenClaw ban April 4 killed gray-zone bridges) and replaced it with a halt-with-remediation card requiring the user to provision a Console API key.
- **Result** : every Victor running `/genesis-drop-zone` for the first time hits a hard stop, must navigate Console + create an API key + set an env var system-wide, then re-launch. Major UX friction for a feature (Citations metadata) that v1.3.x did fine without.

### The frame-release insight

User input 2026-04-19 (during v1.6.4 brainstorming) :

> "il faut revoir la connexion à anthropic via le canal de l'abonnement pas de l'api / de toute façon cette application a pour but d'invoquer claude code donc pas de problème au lancement de claude code / étape anthropic_auth et retour dans genesis"

R8 cache `anthropic-auth-and-oauth-status_2026-04-19.md` was scoped to "subprocess access to Messages API" and concluded "no OAuth bridge ; require API key". The user's input questioned the underlying assumption : *why does the bootstrap need a subprocess at all ?* If extraction stays in-context, no subprocess, no Messages API call, no API key needed — the Max auth that Claude Code already holds is sufficient. This is the entire architectural shift v2 codifies.

The lesson is captured as a feedback memory : `feedback_r8_anchoring_vs_user_intent.md` (auto-memory, project-genesis scope).

### Verified technical baseline (2026-04-19)

```
$ claude auth status
{
  "loggedIn": true,
  "authMethod": "claude.ai",
  "apiProvider": "firstParty",
  "subscriptionType": "max"
}
```

Same auth covers : the Claude Code session itself, all in-context Claude inference (skill rendering, content extraction, conversation), all sub-agents launched via the Task tool, all tool uses. **The only thing this auth does NOT cover** is direct Python subprocess calls to `anthropic.Anthropic().messages.create()`. v2 removes the only Genesis component that needed that.

## In scope (v2 immediate ship)

### 1. Phase anthropic_auth — pre-flight check

A new bootstrap phase **packaged as a separate skill** `phase-auth-preflight` (decision : option D-2 locked, see § "Locked architectural decisions" below). Runs **before** any other Genesis phase invocation (called by both Layer A `genesis-drop-zone` Phase 0 AND Layer B `genesis-protocol` Phase 0 as their first step). Idempotent ; ~10 seconds when authed ; one-turn remediation when not.

#### 1.1 Detect auth status

```bash
claude auth status
```

Returns JSON with at minimum `loggedIn: bool`. Additional fields surfaced for context : `authMethod` (`claude.ai` / `console`), `apiProvider` (`firstParty`), `subscriptionType` (`max` / `pro` / `team` / `enterprise` / `none`), `email`, `orgId`, `orgName`.

#### 1.2 Decision tree

| Condition | Action | User-visible output |
|---|---|---|
| `loggedIn=true` AND `apiProvider=firstParty` | Pass — return control to Genesis next phase | One-line confirmation : `✓ Auth Anthropic OK (<email>, <subscriptionType>)` |
| `loggedIn=false` | Halt with remediation card | Bilingual card : explain `claude auth login` is required, instruct to run it then re-launch the bootstrap |
| `loggedIn=true` AND `apiProvider=Bedrock`/`Vertex`/`Foundry` | Pass with warning note | `✓ Auth via <provider> — Genesis assumes Anthropic-backed inference is available through this provider ; if extraction quality degrades, retry with claude.ai auth` |
| `claude` binary not found | Halt with installer instruction | Bilingual card pointing to `https://claude.ai/install.ps1` (Windows) / `curl -fsSL https://claude.ai/install.sh \| sh` (POSIX) |
| `claude auth status` returns non-JSON or non-zero exit | Halt with diagnostic | Print stderr verbatim, instruct user to file an issue or run `claude auth login` to recover |

#### 1.3 Remediation card — content requirements

For the `loggedIn=false` path (most common Victor case) :

- **Bilingual title** (FR + EN, two columns or stacked per `content_locale`)
- **One-paragraph explanation** : "Genesis runs inside Claude Code which authenticates to Anthropic via your Claude.ai subscription (Pro / Max / Team). Run the command below once, then re-launch this bootstrap."
- **Exact command** : `claude auth login` — single-line, copyable
- **What happens** : "A browser window will open at claude.ai. Sign in (or accept the OAuth prompt if already signed in). Return to this terminal. Re-run this bootstrap."
- **Multi-org note** : "If your account belongs to multiple organizations, choose the one you want this project to be billed against (Max subscription = unlimited inference for the chosen org)."
- **No mention of `--console`** : v2 deliberately does NOT suggest the Console API path because it doesn't help (subprocess Messages API access still requires a separately-generated `sk-ant-api*` key, per R8).

#### 1.4 Handoff

On pass, Phase anthropic_auth writes nothing to disk, sets no env var, prints one confirmation line, returns control to the next phase in the bootstrap chain. No persistent state.

### 2. Drop v1.4.0 subprocess Citations API path

#### 2.1 File deletions and archives — enumerated

**Deleted entirely** :
- `skills/genesis-drop-zone/scripts/extract_with_citations.py` — entire script removed
- `skills/genesis-drop-zone/scripts/` directory removed (empty after the deletion above)

**Moved to R8 archive** :
- `.claude/docs/superpowers/research/stack/anthropic-python_2026-04-18.md` → `.claude/docs/superpowers/research/archive/anthropic-python_2026-04-18.md` with a one-line top note "v2 retired the subprocess that pinned this dependency. Entry preserved for cross-project reference (other projects that use the anthropic SDK directly remain valid consumers)."

**Moved to fixture archive** (`tests/fixtures/.archive/` — created if absent) :
- `tests/fixtures/drop_zone_intent_fixture_v1_4_0_fr_with_citations.md` — citation keys present
- `tests/fixtures/drop_zone_intent_fixture_v1_4_0_en_with_citations.md` — citation keys present
- `tests/fixtures/drop_zone_intent_fixture_v1_5_0_arbitrated.md` — DUAL SEMANTICS (carries both v1.5.0 `snapshot_version` + `arbitrated_fields` AND v1.4.0 `_source_citation` keys ; archived because citation keys make it unrepresentative of v2 schema)

**Kept in active fixtures** (already citation-free, valid as v2 reference) :
- `tests/fixtures/drop_zone_intent_fixture_v1_3_2.md`
- `tests/fixtures/drop_zone_intent_fixture_v1_3_3_en.md`
- `tests/fixtures/drop_zone_intent_fixture_v1_4_0_fallback.md` (per v1.4.0 spec : byte-identical to v1.3.3, no citation keys, valid v2 shape modulo `skill_version`)

**To be created** (replaces archived v1.5.0 arbitrated fixture in v2 schema) :
- `tests/fixtures/drop_zone_intent_fixture_v2_arbitrated.md` — same revision-state semantics (`snapshot_version`, `arbitrated_fields`) but without citation keys, demonstrating the v2 shape

#### 2.2 SKILL.md edits — `genesis-drop-zone`

- **§ "In scope (v1.4.0)"** : annotated as "Retired in v2 — see `.claude/docs/superpowers/specs/2026-04-19-v2-bootstrap-via-max-subscription-design.md`". Section preserved for forensic continuity, marked retired.
- **§ "In scope (v1.5.0)"** : annotated as "Retired in v2 — halt-with-remediation card no longer needed since subprocess no longer exists".
- **§ "In scope (v2)"** : new section, summarizes the architectural shift and points to this spec.
- **Concentrated privilege declaration** : reverts from the v1.5.0 multi-class declaration (disk + network) to **disk-class only** (snapshot writes + history archive — v1.5.0 disk class extension preserved).

#### 2.3 Cross-skill-pattern impact (master.md updates)

- **Pattern #2 — Concentrated privilege map** : `genesis-drop-zone` returns to single-class. Network class retired. The pattern's "first multi-class declaration" precedent is preserved as a historical data-point but the current state of every shipped skill returns to ≤1 class. Document the retirement explicitly.
- **Pattern #4 — Zero-ripple** : NEW ORDINAL data-point (ninth). Locked decision per spec-reviewer judgement : architectural REMOVAL is structurally distinct from v1.5.1's PATCH-prose-cleanup data-point. v1.5.1 was "Layer A polishes wording, contract unchanged". v2 is "Layer A stops writing entire keys, parser-level zero-ripple proven under field omission" — a new failure mode (forward-compat with old writers + backward-compat with old parsers, simultaneously, under a key-omission regime). Master.md pattern #4 narrative gains a ninth ordinal entry tracking this distinction.

### 3. v1.5.0 halt-with-remediation card retirement

The card content moves to `skills/genesis-drop-zone/.archive/v1_5_0_halt_card_content.md` for forensic preservation. The card itself is removed from the skill's runtime path. The R8 `anthropic-auth-and-oauth-status_2026-04-19.md` entry is annotated with a v2 note : "Subprocess access to Messages API is no longer load-bearing for project-genesis post-v2. Entry remains canonical for OTHER projects on this machine that need Messages API." (Per Layer 0 cross-project research sharing convention.)

### 4. Backward compatibility

- **`drop_zone_intent.md` files written by v1.4.0 / v1.4.1 / v1.5.0** with `<field>_source_citation` keys remain parseable by Layer B (Step 0.2a parser ignores unknown keys, per v1.4.0 design).
- **`drop_zone_intent.md` files written by v2** simply omit the citation keys (same as v1.3.x behaviour). Schema_version stays at `1` (no incompatible change).
- **Existing `drop_zone_intent_history/` archives** continue to load.
- **No migration required.**

### 5. Tests + fixtures

Fixture treatment enumerated in § 2.1 above (3 archived, 3 kept, 1 to-create). One additional file in this section :

- `tests/fixtures/.archive/ARCHIVE.md` — short index file listing the 3 archived fixtures with one-line rationale per file ("citation keys present, unrepresentative of v2 schema").

**Phase anthropic_auth test coverage** : 5 cases (authed-firstParty / authed-Bedrock-or-Vertex / loggedIn=false / claude-not-installed / status-command-error). All testable single-shot via `claude -p` since the phase is multi-step but single-turn (no user input mid-flow). Tests live in the `phase-auth-preflight` skill at `skills/phase-auth-preflight/tests/`.

## Out of scope but noted (v3 vision orientation)

These items are NOT shipped in v2 but the v2 implementation must NOT bake assumptions that block them.

### V3.1 External installer surface — Genesis as bootstrap-the-bootstrapper

Today : Victor must already have Claude Code installed AND know to run `/genesis-drop-zone` inside Claude Code. v3 ships a single external entry point (web link / PowerShell one-liner / curl-pipe-bash). This installer :

1. Detects Claude Code installation (Windows : `Get-Command claude` ; POSIX : `command -v claude`)
2. Installs Claude Code with consent if absent (Windows : `irm https://claude.ai/install.ps1 | iex` ; POSIX : `curl -fsSL https://claude.ai/install.sh | sh`)
3. Triggers `claude auth login` (browser opens, user signs in to claude.ai)
4. Creates a fresh project folder under `~/Projects/<slug>/` (or user-chosen path)
5. Invokes `claude` in that folder with `/genesis-drop-zone` already triggered (e.g. via `claude --append-system-prompt-file ...` + auto-launch)

v2's Phase anthropic_auth covers steps 1-3 partially when run from inside Claude Code ; v3 makes the same flow available outside Claude Code as a turnkey installer. **v2 design must keep the Phase anthropic_auth logic factorable into a standalone shell script.**

### V3.2 BYOAI multi-provider

Phase anthropic_auth → Phase **auth** with a provider dispatcher. Detect which provider the user wants (Anthropic / OpenAI / Gemini / Bedrock / Vertex / others) ; route to the provider-specific auth check (`claude auth status` for Anthropic ; `gcloud auth list` for Google ; etc.). The user already has all of these accounts (per Layer 0 user profile "Available AI stack").

**v2 design discipline** :
- Skill / phase / function naming uses `auth` not `claude_auth` whenever the logic is provider-agnostic.
- `Phase anthropic_auth` is the v2 *concrete instance* of a future generic `Phase auth`. The phase's outputs (pass / halt-card / install-card) should not carry Anthropic-specific data structures that would block a Gemini variant.
- The remediation card content is templated with provider-specific variables (provider name, auth command, install command, billing model description) ; in v2 only the Anthropic template ships.

### V3.3 Lovable-style hosted SaaS

Genesis becomes a hosted platform :

- **Auto-hosted Supabase** on VPS OVH infrastructure (per Layer 0 `infra_2026-04-18_supabase_vps_ovh_migration.md`). Each Genesis-bootstrapped project gets a Supabase project provisioned automatically.
- **GitHub repo creation** in bootstrap flow (already partial via Phase 5.5 fine-grained PAT pattern in `phase-5-5-auth-preflight` skill).
- **Deployment to subdomain** : free tier = `<projectslug>.genesis.platform.tld/` ; paid subscription = `<projectslug>.tld` (own subdomain) + extra features.

**v2 design discipline** :
- Bootstrap output artefacts (`drop_zone_intent.md`, `bootstrap_intent.md`, generated project files) must NOT hardcode local paths that would break under hosted deployment. Use relative paths or environment-variable-driven path roots.
- The Genesis CLI plugin remains the *reference implementation* that the v3 hosted platform reuses — not a parallel codebase that diverges.
- Phase 5.5's PAT-creation logic must be factorable into a server-side equivalent that creates GitHub repos via the platform's bot account when running in hosted mode.

## Cross-skill-pattern composition (master.md update required)

- **Pattern #1 (1:1 mirror)** : no impact on `genesis-drop-zone`'s mirror discipline ; the spec itself is canonical for the v2 changes (no separate skill mirrors v2 SKILL.md).
- **Pattern #2 (concentrated privilege)** : `genesis-drop-zone` returns to disk-class only. Document the network-class retirement explicitly. Add Phase anthropic_auth as a new privilege-map entry — class : `subprocess` (calls `claude auth status` and potentially `claude` for install detection), with mitigations : (a) read-only commands only, (b) no auth-state-mutating side effects (never run `claude auth login` automatically — only print the instruction), (c) no env var writes, (d) no file writes, (e) JSON-parse-with-fallback (corrupt output halts gracefully).
- **Pattern #3 (granular commits)** : v2 ship follows the precedent ; spec / spec-polish / plan / plan-polish / feat-core / chore commits in the same feat branch.
- **Pattern #4 (zero-ripple)** : NEW ordinal (ninth data-point) — locked. v2 is structurally distinct from v1.5.1's PATCH-prose-cleanup. See § "In scope item #2 cross-skill-pattern impact" above for the rationale.

## Locked architectural decisions (post-spec-reviewer)

The following decisions are locked in this spec — plan does NOT need to re-litigate :

- **Phase anthropic_auth lives in a separate skill `phase-auth-preflight`** (D-2 locked). **Primary justification : present-day reuse across two entry points** (`genesis-drop-zone` Layer A AND `genesis-protocol` Layer B both need the same auth check ; factoring into one skill is anti-Frankenstein-clean per R10.4 because both call sites exist TODAY). Secondary benefit : naturally hosts v3.2 BYOAI multi-provider dispatcher when that ships, but BYOAI is NOT the load-bearing reason for the factoring decision (per R10.4 anti-speculative-feature gate, future flexibility alone would not justify a 9th skill).
- **Cross-skill-pattern #4** : NEW ordinal (ninth data-point), per spec-reviewer judgement. Architectural REMOVAL semantics is distinct from v1.5.1 PATCH-prose-cleanup semantics.

## Open questions for user (decide before plan writing)

### Q-A : Version label

| Option | Argument |
|---|---|
| **v1.7.0 MINOR** | Additive Phase + remove one feature ; data contract backward-compatible ; tag chain stays in v1.x.y |
| **v2.0.0 MAJOR** | Architectural shift signals "the model changed" ; aligns with master.md "What v2 target is" framing ; clean semver story for the v3 vision items that build on it |

**Reco** : v2.0.0 MAJOR. Subprocess removal + SDK dependency removal + halt-card removal + new Phase = enough collective change to warrant a major bump. Genesis is still pre-product (no external users besides the maintainer), so backward-compat constraints are minimal. v2 framing aligns with the existing master.md vision.

### Q-B : Phase naming — `anthropic_auth` vs `auth`

| Option | Argument |
|---|---|
| **`anthropic_auth`** | Matches user input ; explicit about which provider ; v3.2 BYOAI generalizes by adding a layer above (Phase auth → dispatches to Phase anthropic_auth / openai_auth / gemini_auth) |
| **`auth`** | Provider-agnostic from day 1 ; v3.2 BYOAI adds providers as drop-in implementations ; one less rename later |

**Reco** : Ship v2 with internal naming `anthropic_auth` (matches user input + explicit) but design the implementation as a function `check_provider_auth(provider="anthropic")` so v3.2 generalizes to `check_provider_auth(provider=detected_or_user_choice)` without skill restructure.

### Q-C : Cleanup scope for `<field>_source_citation` schema keys

| Option | Argument |
|---|---|
| **Keep keys in schema docs as deprecated, parser still ignores them** | Maximum backward compatibility ; old Victor projects still validate cleanly |
| **Remove keys from schema entirely** | Cleaner v2 contract ; old files still parse (parser ignores unknown keys) but new docs don't reference them |

**Reco** : Keep as deprecated for one MAJOR version (v2.x), remove in v3.0.0. Same pattern as Anthropic SDK deprecation cadence.

### Q-D : Self-rating projection (post-spec, pre-implementation)

| Axis | Projected | Rationale |
|---|---|---|
| Pain-driven | 9.6 | Closes the v1.5.0 halt-card UX wall ; aligns architecture with user intuition |
| Prose | 9.0 | Spec is dense but clear ; sections scaled to complexity |
| Best-at-date | 9.2 | R8-anchored ; uses canonical `claude auth login` flow ; cites Anthropic docs |
| Self-contained | 9.0 | Touches `genesis-drop-zone` + master.md + R8 archive + 1 new skill (D-2) ; bounded ripple |
| Anti-Frankenstein | 9.4 | REMOVES code (subprocess + SDK + halt-card) ; adds one phase ; reverts to simpler architecture |
| **Mean projected** | **9.24** | Streak ≥ 9.0 restart count would advance to 2 |

## Implementation order (deferred to plan)

The plan document (next deliverable, after spec-reviewer + user review) will sequence :
1. Worktree + spec commit (already shipped if user approves this spec)
2. Plan commit + plan-reviewer
3. Phase anthropic_auth skill creation (D-2 reco — `phase-auth-preflight`)
4. `genesis-drop-zone` SKILL.md edits (deletions + v2 section + privilege map revert)
5. Subprocess + script deletion + tests archive
6. Layer B `genesis-protocol` Phase 0 unchanged (zero-ripple verification)
7. Master.md cross-skill-pattern updates
8. R8 archive note
9. Plugin.json version bump (1.6.3 → 2.0.0 if Q-A reco accepted)
10. Feat commit + PR + squash + tag + chore

Estimated session count : 1-2 (spec ship + implementation ship). Estimated implementation time : 2-3 hours.

<!-- SPDX-License-Identifier: MIT -->
