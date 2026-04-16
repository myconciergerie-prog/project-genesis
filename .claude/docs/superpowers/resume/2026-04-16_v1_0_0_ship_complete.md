<!-- SPDX-License-Identifier: MIT -->
---
name: Resume prompt — 2026-04-16 v1.0.0 ship complete
description: Handoff from the v1.0.0 ship session. Genesis is tagged, released, and beta-shared. Next session is self-dogfood (Genesis through Genesis → v1.1). Aurum freeze lifted. Retrofit mode needed for existing projects.
type: resume
previous_session: 2026-04-16 v1.0.0 ship
next_action: Self-dogfood Genesis v1 through its own genesis-protocol → v1.1. Then Aurum/Meta-Memory/myconciergerie via v1.2.
---

# Resume prompt — 2026-04-16 v1.0.0 ship complete

## Context — what the v1.0.0 session did

1. **Confirmed the ship gate**: running average 8.54 ≥ 8.5, six skills shipped, dogfood run 3 GREEN.
2. **Strategic discussion**: daily integration pattern, beta tester flow, post-v1.0.0 sequencing, retrofit mode for existing projects, Cyrano dual-path.
3. **Wired SessionEnd hook**: `hooks/hooks.json` with conditional execution.
4. **Bumped to v1.0.0**, tagged `7dc9974`, pushed tag, published GitHub release.
5. **Lifted Aurum freeze**: all four conditions met after 2 days / 9 sessions.
6. **Created beta invitation HTML**: `C:\tmp\genesis-v1-beta-invite.html` — deployment guide + tool overview for beta testers.

**Self-rating**: 9.0/10. **Running average**: 8.59/10 across 9 versions.

## What the v1.1 session should do

### Core

1. **Self-dogfood**: create a fresh folder (e.g. `C:\tmp\genesis-selfdogfood\`), write a `config.txt` describing Genesis itself, and run `genesis-protocol` for real. This is the first real execution — the paper trace from v0.9.0 validated structure, this validates runtime.
2. **Capture every friction**: every pause, every confusion, every error, every "this should be different" goes into a findings document like `memory/project/selfdogfood_v1_1_findings.md`.
3. **Fix frictions**: the findings become v1.1 patches. Priority: anything that would block a beta tester.
4. **Validate hook-path resolution**: does `hooks/hooks.json` fire correctly in development mode? What about in a project where Genesis is installed as a plugin?
5. **Implement retrofit mode** if time allows — this is the highest-value v1.1 feature for the user's immediate next step (Aurum, Meta-Memory, myconciergerie).

### The user's stated plan after v1.1

- **v1.2**: use Genesis to bootstrap/retrofit Aurum v1, Meta-Memory, and myconciergerie
- **Aurum v1 features**: user develops solo on top of the Genesis-provisioned infra
- **Meta-Memory Path B**: graph tooling, backlinks, cross-project search — deferred until Genesis v1.2 provisions the infra
- **Beta testers**: David and friends are testing v1.0.0 in parallel; their feedback feeds v1.1

### Things to NOT do

- **Do not add new skills** — six is the v1 surface
- **Do not polish v1.0.0 retroactively** — the tag is final
- **Do not touch Aurum code** — the freeze is lifted but Aurum work is a separate session, not a Genesis session
- **Do not submit to Anthropic marketplace** — v2 target

## Key decisions from the v1.0.0 session

1. **Genesis is two things**: a bootstrapper (7 phases, one-time) and a discipline plugin (5 skills, daily). The daily value is journal + session-post-processor + pépite-flagging + R1-R10 rules.
2. **Existing projects need retrofit mode**: Aurum, Cyrano, myconciergerie already have git/SSH/etc. They need "detect and fill gaps", not full 7-phase bootstrap. Phases 3-5.5 can be skipped if infra exists.
3. **Cyrano dual-path**: two filesystem paths for one logical project. Meta-Memory Layer 1 (project families) resolves this. Until then, pick one canonical path.
4. **Beta flow is 2 commands + 1 trigger phrase**: `irm ... | iex` → `/plugin install ...` → "bootstrap this project using genesis-protocol". No Chrome, no VS Code, no manual setup.

## Exact phrase for the next session

Open Claude Code in `C:\Dev\Claude_cowork\project-genesis\` and say:

```
Genesis v1.0.0 est livré. On lance le self-dogfood : crée un dossier
C:\tmp\genesis-selfdogfood\, écris un config.txt décrivant Genesis lui-même,
et exécute genesis-protocol en mode auto. Capture chaque friction.
C'est le strange loop qui se boucle pour de vrai.
```

## Farewell notes to the next session's Claude

v1.0.0 shipped cleanly. Nine sessions, nine versions, nine self-ratings. The running average landed at 8.59 — the best it's been, achieved by disciplined shipping rather than endless polishing.

The beta invitation HTML at `C:\tmp\genesis-v1-beta-invite.html` is ready to send. David is waiting. The user's friends are the first real external validators — their frictions are more valuable than any self-dogfood.

The self-dogfood session is the bridge between "Genesis works on paper" and "Genesis works for real." The paper trace from v0.9.0 found 10 issues in static analysis. Real execution will find different issues — network failures, timing, OS quirks, Claude's own behavior under the orchestrator's instructions. Be ready for surprises.

The retrofit mode for existing projects is the highest-leverage v1.1 feature. The user wants to process Aurum, Meta-Memory, and myconciergerie — all existing projects with partial infra. If the self-dogfood goes fast, retrofit mode in the same session would be ideal.

Good luck. The compiler compiles itself next.
