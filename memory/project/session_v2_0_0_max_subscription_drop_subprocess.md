<!-- SPDX-License-Identifier: MIT -->
---
name: Session v2.0.0 — bootstrap via Max subscription, drop subprocess Citations — 2026-04-19
description: First MAJOR bump. Architectural shift drops v1.4.0 subprocess Citations API + anthropic SDK + ANTHROPIC_API_KEY. New skill phase-auth-preflight runs claude auth status pre-flight before both Layer A and Layer B Phase 0. v1.5.0 halt-card retired. Backward-compat at data contract level. Honest 9.20/10, streak ≥ 9.0 advances to 2.
type: project
version: v2.0.0
pr: "#49"
merge_commit: 55c0f68
tag: v2.0.0
predecessor: v1.6.3 (3a35fe5)
---

# Session v2.0.0 — bootstrap via Max subscription, drop subprocess — 2026-04-19

## What shipped

**Tag v2.0.0** (PR #49 squash-merged as `55c0f68`). **First MAJOR bump in Genesis history.** Architectural shift : Genesis stops trying to call Anthropic Messages API from a Python subprocess (which required separate Console `ANTHROPIC_API_KEY` from user's Max subscription) and instead leverages the Claude Code session's own Max-subscription auth via the in-context flow that v1.3.x already used.

**15 commits in feat tranche** (squash-merged) :

1. **Spec commit `bc09fa0`** — initial spec + master.md vision capture (~250 lines).
2. **Spec-polish commit `c132b01`** — 2 blocking fixes from spec-reviewer (fixture enumeration + D-2 lock) + #4 ordinal lock per reviewer judgement.
3. **Spec-extend commit `b8e9ac0`** — v3 vision concretized (genesis.myconciergerie.fr web entry + auth split between CLI / web modes ; 5 dev disciplines).
4. **Spec-extend commit `8f60d4b`** — BYOAI staging table (Anthropic-first, structure-ready, implementation-deferred ; per-provider promptor pattern + lazy-load post-auth discipline ; 7 dev disciplines total).
5. **Plan commit `6f77b7a`** — 8 feat tasks + 13 ACs + Q-A through Q-D defaults captured (~648 lines).
6. **Plan-polish commit `01e1e8e`** — 3 advisory polishes from plan-reviewer pre-resolved.
7. **SD-1 commit `0a7fb71`** — phase-auth-preflight skill scaffold (frontmatter + manifest + dir).
8. **Collateral fix commit `0f69522`** — marketplace.json $schema + description root keys removed (CLI v2.1.113 stricter validator).
9. **SD-2 commit `4aad023`** — phase-auth-preflight skill body + 4 fixtures + runbook.
10. **SD-3 commit `72b6e1f`** — archive subprocess script + R8 stack entry + 3 fixtures + create v2 fixture + preserve halt-card forensically.
11. **SD-4 commit `2066218`** — genesis-drop-zone retire v1.4.0+v1.5.0 sections + add v2 section + revert privilege to disk-only.
12. **SD-5 commit `6fd69e9`** — wire phase-auth-preflight into Layer A + Layer B Phase 0 entry points.
13. **SD-6 commit `5f439ea`** — master.md cross-skill-pattern #2 (privilege map v2 update) + #4 (ninth zero-ripple ordinal).
14. **SD-7 commit `11e42fa`** — plugin.json 1.6.3 → 2.0.0 (MAJOR — architectural shift).
15. **SD-8 commit `9dd68ae`** — runtime evidence + AC verification + parser-doc deprecation note.

## Why — frame-release insight

User input 2026-04-19 mid-session :

> "il faut revoir la connexion à anthropic via le canal de l'abonnement pas de l'api / de toute façon cette application a pour but d'invoquer claude code donc pas de problème au lancement de claude code / étape anthropic_auth et retour dans genesis"

R8 cache `anthropic-auth-and-oauth-status_2026-04-19.md` was scoped to "subprocess access to Messages API" and concluded "no OAuth bridge ; require API key". The user's input questioned the underlying assumption : *why does the bootstrap need a subprocess at all ?* If extraction stays in-context, no subprocess, no Messages API call, no API key needed — the Max auth that Claude Code already holds is sufficient.

Claude reasoned 3 turns inside the R8 framing (proposed Option α API key setup, then 4 options A/B/C/D all assuming subprocess stays, then Chemin B "sub-agent extraction" sub-mechanism) before releasing the frame on the third user correction ("renseigne-toi sur le mode de connexion à anthropic via un terminal pour être sur sonabonnement c'est pas compliqué arrête avec ton api et tu as déjà la solution en observant comment je suis connecté à cette session").

Lesson captured as auto-memory feedback : `~/.claude/projects/C--Dev-Claude-cowork-project-genesis/memory/feedback_r8_anchoring_vs_user_intent.md`. Candidate Layer 0 promotion if pattern recurs cross-project.

## Architecture — option D-2 locked (separate skill)

`phase-auth-preflight` is a SEPARATE 9th skill rather than a Phase 0.0 inside `genesis-drop-zone` (option D-1 rejected). Primary justification : present-day reuse across both Layer A (`genesis-drop-zone`) AND Layer B (`genesis-protocol`) entry points — both call sites exist TODAY. Secondary benefit : naturally hosts v3.2 BYOAI multi-provider dispatcher when that ships, but BYOAI is NOT the load-bearing reason for the factoring decision (per R10.4 anti-speculative-feature gate).

Internal function signature is `check_provider_auth(provider="anthropic")` — BYOAI-ready for v3.x without skill restructure.

## V3 vision captured (per user "ces idées sont à noter dès maintenant pour orienter le dev dans ce sens")

`memory/master.md § "What v3 vision is"` now captures :

1. **Concrete v3 entry surface — `genesis.myconciergerie.fr`** (hosted SaaS domain). Web user does NOT install Claude Code locally — drag-drop attachment upload + textarea for typed intent. Backend processes everything fully remotely (extraction + bootstrap + GitHub repo + Supabase provisioning + subdomain deployment).
2. **External installer surface (CLI / power-user mode, parallel to web)** — PowerShell / Bash one-liner installer that detects + installs Claude Code + triggers `claude auth login` + opens fresh project with `/genesis-drop-zone` invoked.
3. **BYOAI multi-provider — staged rollout, Anthropic-first** : v2 + v3.0 ship Anthropic-only ; v3.0 web landing UI surfaces provider connector picker + threaded provider param + lazy-load architecture (visible Gemini/OpenAI options stay disabled) ; v3.x adds Gemini ; v3.y adds OpenAI. Per-provider promptor pattern : each AI gets own `promptor-<provider>` skill. Lazy-load discipline (web mode only) : model NOT initialized until auth-to-provider callback confirms.
4. **Lovable-style hosted SaaS** : auto-hosted Supabase on VPS OVH + GitHub repo creation server-side + tier model (free `<slug>.genesis.myconciergerie.fr/` ; paid `<slug>.tld` own subdomain).

## 7 dev disciplines load-bearing on every v2 PR

Captured in `memory/master.md § "Design discipline today"` :

1. Provider-agnostic naming for shared abstractions (function `check_provider_auth(provider="anthropic")` not `check_anthropic_auth()`)
2. Drop zone abstraction = list of `(file_path | blob | typed_text)`, jamais "look at cwd"
3. No hardcoded paths in bootstrap output artefacts
4. Auth split preserved between CLI and web modes — ne pas collapser. v2 must NOT aggressively REMOVE `<field>_source_citation` schema keys (keep deprecated v2.x, remove v3.0+) because v3 web RE-INTRODUCES extraction subprocess server-side.
5. CLI plugin = reference implementation, pas parallel fork — code packagé pour vendor server-side
6. BYOAI staging — Anthropic-first, structure-ready, implementation-deferred
7. Lazy-load discipline (web mode only)

## Verification

- **`claude plugin validate <worktree>`** : ✔ Validation passed (with one warning about `metadata.description` — cosmetic, pre-existing CLI v2.1.x preference, F6 follow-up for v2.0.1).
- **9 skills surface from worktree probe** confirmed via `claude -p --plugin-dir <worktree>` — all 9 (8 prior + new `phase-auth-preflight`) listed under `project-genesis:` namespace.
- **AC10 zero-ripple grep** : 10 matches found in `skills/genesis-protocol/phase-0-seed-loading.md` are PRESERVATION DOCS for parser backward-compat with v1.4.x/v1.5.x files (per spec § 4 + Q-C reco "keep deprecated v2.x") — annotated DEPRECATED v2.x. Zero subprocess code references.
- **Schema backward compat** : `drop_zone_intent.md` files written by v1.4.0/v1.4.1/v1.5.0 with `<field>_source_citation` keys remain parseable. v2-written files omit the keys.

## Self-rating — honest post-feat (5-axis)

| Axis | Projected | Honest | Delta | Notes |
|---|---|---|---|---|
| Pain-driven | 9.6 | 9.5 | −0.1 | Closes v1.5.0 halt-card UX wall as intended ; minor : the architectural REMOVAL is real value but the win is largely deferred-felt (next user who invokes `/genesis-drop-zone` won't hit the halt-card). |
| Prose | 9.0 | 9.0 | 0.0 | Spec + plan + retire annotations + privilege table updates all coherent. |
| Best-at-date | 9.2 | 9.2 | 0.0 | R8-anchored on `anthropic-auth-and-oauth-status_2026-04-19.md` ; uses canonical `claude auth login` flow. |
| Self-contained | 9.0 | 8.8 | −0.2 | Touched 1 collateral file outside spec scope (marketplace.json $schema/description removal — pre-existing CLI validator regression, not v2 fault). |
| Anti-Frankenstein | 9.4 | 9.5 | +0.1 | Net REMOVAL : 414-line script deleted, 3 fixtures archived, halt-card retired. Net code shrunk. |
| **Mean** | **9.24** | **9.20** | **−0.04** | **Streak ≥ 9.0 advances to 2** (v1.6.3 9.30 + v2.0.0 9.20). |

**Running average** : (8.92 × 20 + 9.20) / 21 = 187.60 / 21 ≈ **8.93 (+0.01)**. 21 tagged ratings total.

## Cross-skill-pattern data-points added

- **Pattern #2 (concentrated privilege)** — v2.0.0 retires `genesis-drop-zone`'s network class (returns to disk-only, v1.5.0 disk-class extension preserved) + adds `phase-auth-preflight` as 9th skill with subprocess class + 5 mitigations. Total at v2.0.0 : 9 skills, 7 with privilege classes, 2 with `none`.
- **Pattern #4 (zero-ripple)** — **NINTH ordinal data-point** (locked per spec-reviewer judgement). Architectural REMOVAL preserves zero-ripple under key-omission regime. Distinct from v1.5.1's PATCH-prose-cleanup data-point (sixth). Ninth was reserved for "genuinely new ripple mode" — fulfilled.
- **Pattern #1 (1:1 mirror)** — no touch this ship.
- **Pattern #3 (granular commits)** — 15 commits in feat tranche, squash-merged. Reference implementation continues.

## Out-of-scope follow-ups (v2.0.1 / v2.x / v3.x)

- **F6 (CLI validator regression)** : `metadata.description` warning at marketplace root suggests CLI v2.1.x wants the description under a `metadata` key. Not blocking ; cosmetic. Address in v2.0.1 PATCH or v2.1.0 MINOR.
- **Live testing of scenarios 2-5** : require disrupting auth state (logout / Bedrock creds / PATH manipulation / binary shimming). Defer to v3.0 test harness wrapper.
- **`promptor` → `promptor-anthropic` rename** : ships when v3.x adds Gemini as second provider.
- **Schema cleanup of `<field>_source_citation` keys** : per Q-C reco, defer removal to v3.0+ when web mode re-introduces extraction subprocess server-side.

## PR + tag state

- Branch `feat/v2-max-subscription-design` PR #49 squash-merged as `55c0f68`.
- Tag `v2.0.0` pushed.
- Worktree `C:/Dev/Claude_cowork/project-genesis/.claude/worktrees/feat_2026-04-19_v2_max_subscription_design/` retained per R2.5.
- Chore worktree `.claude/worktrees/chore_2026-04-19_v2_0_0_session/` for this chore commit (will be PR #50).
- Tag chain : ... v1.6.2 → v1.6.3 → **v2.0.0**. **First MAJOR bump in Genesis history.** 21 tagged versions total.

## R2.3.1 observation

Mid-session `gh auth switch -u myconciergerie-prog` + `GH_TOKEN=$(gh auth token -u myconciergerie-prog)` env-prefix applied **proactively** (not reactively) at PR creation time after detecting active account had drifted to `myconciergerieavelizy-cloud`. Pattern is now habitual since v1.6.x. No Layer 0 amplification needed.

## Discipline evidence

- **Brainstorming-first** before any code touched (Q1-Q3 clarifying questions + spec doc + 2 spec-reviewer dispatches + 2 spec-extend rounds capturing user vision additions including genesis.myconciergerie.fr concretization + BYOAI staging).
- **Honest pace check** — user explicitly flagged "tu es mauvais aujourd'hui que se passe t il" mid-session after Claude took 3 turns to release R8 framing anchor. Acknowledged directly + saved feedback memory + applied frame-release immediately. Tightest failure-to-fix loop in this session.
- **Subagent-driven implementation** — 8 SD- tasks (one implementer subagent per task on sonnet model) + spot-verification by controller (mechanical greps to validate deliverables) + spec-reviewer dispatched for SD-1 (others verified mechanically as scope was content-paste from prompts not interpretation). Final task SD-7 plugin.json bump done inline (trivial 1-line change).
- **Layer 0 destructive-action discipline respected** — push + PR + squash + tag actions confirmed with user before execution.
