<!-- SPDX-License-Identifier: MIT -->
---
name: Session v2.1.0 — marketplace validate warning fix + v2.0.0 runtime evidence — 2026-04-20
description: Small-scope MINOR bundling v2.0.0 loose ends. Piste A adds metadata.description to marketplace.json (closes last validate warning from v2.0.0 collateral fix). Piste B captures verbatim 4/4 runtime evidence observables for phase-auth-preflight Phase 0.0 on fresh project /genesis-drop-zone invocation (closes v1.5.0 → v1.6.x runtime-evidence-gap). Honest 8.92/10, streak ≥ 9.0 BROKEN at 2.
type: project
version: v2.1.0
pr: "#51"
merge_commit: 3911a22
tag: v2.1.0
predecessor: v2.0.0 (55c0f68)
---

# Session v2.1.0 — marketplace validate warning fix + v2.0.0 runtime evidence — 2026-04-20

## What shipped

**Tag v2.1.0** (PR #51 squash-merged as `3911a22`). Small-scope MINOR closing two v2.0.0 loose ends flagged in the v2.0.0→next resume. No architectural shift, no new privilege class, no new skill — just axis closure and hygiene.

**3 commits in feat tranche** (squash-merged) :

1. **`ec01fed` fix(marketplace)** — adds `metadata.description` to `.claude-plugin/marketplace.json` with the project one-liner. Claude CLI v2.1.113+ validator wants description under the `metadata` key (v2.0.0 collateral fix `0f69522` removed it from root because the stricter validator rejected its placement). Verified clean post-fix : `✔ Validation passed` (zero warnings).
2. **`439f185` test(runtime)** — new spec `v2_1_0_runtime_evidence_log.md` capturing verbatim 4/4 observables from a real end-to-end `/project-genesis:genesis-drop-zone` invocation.
3. **`ca04ca2` chore(hygiene)** — 2 R8 stack entries archived post 1-day TTL + `.gitignore` extended for local-only Claude Code state.

## Why — closing v2.0.0 deferred items honestly

v2.0.0 shipped as a MAJOR with 15 commits of architectural shift. Three items were explicitly deferred into a follow-up note (the v2.0.0→next resume) :

- **F6 cosmetic** : `claude plugin validate` showed one remaining warning about missing `metadata.description`. Trivial fix but not bundled into v2.0.0 because the collateral fix commit `0f69522` had already removed the root `description` key and adding the metadata.description was a scope-adjacent change the ship had no plan capacity to re-scope for.
- **Runtime evidence gap** : v2.0.0 shipped on documentary expectation for 4/5 `phase-auth-preflight` scenarios (only authed-firstparty is auto-testable via real `claude auth status`). The v2 architecture benefit (bootstrap works on Max auth, no API key) was not yet validated live on a real fresh project — only inferred from the skill body correctness.
- **R1.1 hygiene** : 2 stack R8 entries created 2026-04-19 for the v1.4.2 marketplace unblock ship had a 1-day TTL that was about to elapse.

This ship closes all three in one tranche, bundled as v2.1.0 MINOR (upgrading from a potential v2.0.1 PATCH because of the runtime evidence spec addition which is a new artefact, not purely a fix).

## Runtime evidence — the load-bearing axis

The runtime test was user-driven : Claude prepared the fixture (`C:/tmp/genesis-v2-test/` empty dir) and the spec stub, user bumped their local install (`claude plugin update` v1.6.3 → v2.0.0), user launched `claude` in the fixture, user invoked `/project-genesis:genesis-drop-zone`, captured the full scrollback, pasted back. Claude parsed the transcript and filled the 4 observables verbatim.

**4/4 PASS on first try** :

| # | Observable | Evidence |
|---|---|---|
| A | Phase 0.0 runs before welcome | `Skill(project-genesis:phase-auth-preflight)` sub-skill invocation visible in tool-call trace ; shells to `Bash(claude auth status)` returning the JSON ; three actions precede any welcome box render |
| B | `✓ Auth Anthropic OK (<email>, <subscription>)` format | `✓ Auth Anthropic OK (contact@ar2100.fr, max)` — exact match with `phase-auth-preflight/SKILL.md` decision-tree row 1 |
| C | FR welcome box post-preflight | `┌─...─┐ │ Depose ici ton idee. │ ... └─...─┘` — ASCII alignment preserved, `welcome_locale = FR` default on slash |
| D | Zero API key friction | Full flow from trigger → 9-field mirror → consent card → decline bridge → `/exit` contains zero `ANTHROPIC_API_KEY` prompts, zero Console links, zero halt cards |

**Bonus observable** : v1.3.1 9-field mirror + v1.3.2 consent card with pre-write `test -e` probe + v1.3.3 decline bridge in FR all render intact post-v2 refactor, confirming the v2.0.0 subprocess removal did not regress the conversational layer. The consent-card pre-write probe is visible as `Bash(test -e "C:/tmp/genesis-v2-test/drop_zone_intent.md" && echo "EXISTS" || echo "absent")` returning `absent` before proceeding.

**Scope excluded** : attachment drag-and-drop input modality (test used typed-text only per user input "pas glissé-déposé un document dans la drop zone"). Named in the spec as candidate v2.2.0 multi-modal runtime evidence follow-up.

## Process lessons — 3 minor hiccups, all recovered

1. **`git mv` auto-stage during R1.1 ritual** — when I moved the 2 expired stack entries to archive during R1.1, `git mv` implicitly staged the renames in the index. When I later ran `git add .claude-plugin/marketplace.json && git commit` for Piste A, git bundled the renames into commit 1. Squash-merged this is invisible, but branch-level commit granularity drifted from intent (I had planned 3 cleanly-separated commits : fix / test / chore-hygiene ; actually got fix-plus-renames / test / chore-gitignore+INDEX). Minor nit.
2. **First user paste was incomplete** — when I asked the user to copy terminal scrollback for the runtime evidence, the first paste started only at the 9-field mirror generation phase, missing observables A / B / C above it. Required a second turn with explicit "scroll all the way up, paste from `claude` launch to `/exit`" instruction. Cost : one clarification turn. Process learning : future user-hands-in-loop test instructions should be explicit about scrollback boundaries from the start.
3. **gh CLI auth switch needed** — the gh CLI active account had drifted to `myconciergerieavelizy-cloud` between sessions (normal behavior, it switches on use). `gh pr create` failed with "must be a collaborator" until `gh auth switch -u myconciergerie-prog`. Same pattern as v1.6.x and v2.0.0 ships. Not worth a Layer 0 feedback — already stable recovery pattern.
4. **plugin.json bump omission from feat tranche** — the v1.6.3 and v2.0.0 patterns bump `plugin.json` version as part of the feat commit tranche. I skipped it in v2.1.0 feat, caught it in chore tranche review, bundled the bump into the chore commit with explicit discipline evidence. Minor process nit, called out in the self-rating.

## Forward map

**Candidates for next ship** (from the v2.1.0→next resume that follows this session) :

- **v2.2.0 multi-modal runtime evidence** — extend the runtime evidence coverage to the attachment drag-and-drop input modality (PDF, image, mixed-media drops). The v1.4.0 Citations API surface was retired in v2.0.0 but the mirror still shows attachments correctly from in-context extraction. Would close the full drop-zone-input-modality axis.
- **v3.0 web mode kickoff** — `genesis-web` sibling repo is at v0.6.0 (auth modal + welcome router shipped). Next step for v3 is the consumption mechanism decision between `project-genesis` (skill source) and `genesis-web` (platform) : npm publish vs git submodule vs direct vendoring. Also : formalize the split in master.md (currently captured as v3 vision but the physical sibling repo existence is not yet reflected).
- **Aurum frozen scope lock review** — the lock formally lifted at v1.0.0 (documented in `memory/project/aurum_frozen_scope_lock.md`). v2.0.0 and v2.1.0 were both beyond the original lock scope. A future session could formally unlock and open Aurum v1 kickoff.

## Tag chain snapshot

22 versions tagged total. Recent tail : … v1.6.2 (025ad1b) → v1.6.3 (3a35fe5) → **v2.0.0** (55c0f68) → **v2.1.0** (3911a22).

Running average : 8.93 (flat from v2.0.0's 8.93, 22 ratings now).

Streak ≥ 9.0 : **BROKEN at 2** (v1.6.3 9.30 + v2.0.0 9.20 → v2.1.0 8.92 ends the run). New streak starts at 0 post-v2.1.0.

Streak history : longest streak this project has seen was 11 consecutive (v1.2.1 → v1.4.2, broken by v1.5.0 8.62). Current streak-length ranking : 11 → 3 → 2 → 2 (recent) → 1s. The 8.9 honest reflects real narrow-coverage on Pain-driven axis (1-of-5 phase-auth-preflight scenarios live, 4 still documentary), not invented humility.
