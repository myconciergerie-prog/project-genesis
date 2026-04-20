<!-- SPDX-License-Identifier: MIT -->
---
title: v2.1.0 Runtime Evidence Log
version: v2.1.0
status: captured
created_at: 2026-04-20
captured_at: 2026-04-20
verdict: 4/4 observables PASS
---

# v2.1.0 Runtime Evidence Log — v2.0.0 architecture live-tested on a fresh project

## Purpose

v2.0.0 shipped on documentary expectation for 4 of 5 `phase-auth-preflight` scenarios (only the authed-firstparty case was auto-testable via real `claude auth status`). Per the v2.0.0→next resume Candidate B, this log captures a real end-to-end runtime test on a fresh project folder, closing the v1.5.0 → v1.6.x runtime-evidence-gap.

The test proves the v2.0.0 architectural shift — `claude auth login` / Max subscription instead of `ANTHROPIC_API_KEY` / subprocess Citations — works end-to-end with real user hands, not just documentary.

## Test fixture

| Key | Value |
|---|---|
| Fixture path | `C:/tmp/genesis-v2-test/` (empty directory, not a git repo, no CLAUDE.md, no memory/) |
| Plugin install | `project-genesis@project-genesis-marketplace` updated from v1.6.3 → v2.0.0 via `claude plugin update` |
| Claude CLI | v2.1.113+ (current installed version on this machine) |
| Auth state at test | `claude auth status` returns `loggedIn=true`, `apiProvider=firstParty`, `email=contact@ar2100.fr`, `subscriptionType=max` |
| Operator | user (myconciergerie-prog) executing in his own terminal |
| Session transport | fresh `claude` invocation in the fixture cwd (standard CLI, no `--dangerously-skip-permissions` to get the honest consent flow) |

## Four observables to capture

| # | What to observe | Expected per v2.0.0 spec | Captured verbatim |
|---|---|---|---|
| A | Phase 0.0 `phase-auth-preflight` runs **before** Phase 0.1 welcome box | A one-line confirmation `✓ Auth Anthropic OK (contact@ar2100.fr, max)` prints before any welcome ASCII art | _(paste first turn output here)_ |
| B | The confirmation line matches the authed-firstparty template | Exact format `✓ Auth Anthropic OK (<email>, <subscriptionType>)` per `phase-auth-preflight/SKILL.md` decision tree row 1 | _(paste the line verbatim here)_ |
| C | Phase 0.1 welcome box prints after Phase 0.0 passes | The unified FR welcome ASCII box per `genesis-drop-zone/phase-0-welcome.md` | _(paste welcome box here)_ |
| D | No `ANTHROPIC_API_KEY` prompt, no halt card, no Console link | The full drop-zone flow (welcome → user intent → 9-field mirror → consent card → optional write) proceeds purely on Max auth. Zero mention of API keys. | _(yes / no ; note any unexpected prompts)_ |

## Execution protocol

1. **Bump local install to v2.0.0** :
   ```powershell
   claude plugin update project-genesis@project-genesis-marketplace
   ```
   Confirm `claude plugin list` shows `project-genesis ... Version: 2.0.0`.

2. **Launch fresh Claude Code session in the fixture** :
   ```powershell
   cd C:/tmp/genesis-v2-test; claude
   ```

3. **Inside the session, invoke the slash command** :
   ```
   /genesis-drop-zone
   ```

4. **Capture observables A, B, C from the first turn output**.

5. **Provide a minimal project idea when the welcome prompts you**, e.g. :
   ```
   Je veux créer un blog perso pour partager mes recettes de cuisine avec mes amis.
   ```

6. **Observe the 9-field mirror, the consent card, the accept/decline bridge**. Capture observable D (no API key prompt anywhere).

7. **Copy the terminal output** (observables A-D sections) and paste back so this spec is updated in place.

## Captured evidence — 2026-04-20 live test

Session : `99de0078-9e3a-4dae-8dd1-c79a9b48974f` (user-invoked, fresh `claude` session in fixture cwd). Plugin version confirmed at v2.0.0 via `claude plugin update project-genesis@project-genesis-marketplace` immediately prior (v1.6.3 → v2.0.0 bump surface output : `✔ Plugin "project-genesis" updated from 1.6.3 to 2.0.0 for scope user. Restart to apply changes.`). Trigger : explicit slash `/project-genesis:genesis-drop-zone` (fully-qualified form with plugin namespace prefix).

### Observable A — Phase 0.0 runs first

```
❯ /project-genesis:genesis-drop-zone

● I'll run the Genesis drop-zone protocol. Phase 0.0 starts with auth pre-flight.

● Skill(project-genesis:phase-auth-preflight)
  ⎿  Successfully loaded skill

● Bash(claude auth status)
  ⎿  {
       "loggedIn": true,
       "authMethod": "claude.ai",
     … +6 lines (ctrl+o to expand)
```

**Verdict** ✓ — `phase-auth-preflight` skill is explicitly invoked as a sub-skill (`Skill(project-genesis:phase-auth-preflight)` tool call visible in the transcript), which in turn shells out to `claude auth status` to obtain the structured JSON. All three actions occur **before** any welcome box render. The sub-skill invocation pattern matches v2.0.0 cross-skill-pattern #4 expectation (skill-invoke-skill via the `Skill(...)` surface rather than a Python import shim).

### Observable B — auth confirmation line verbatim

```
● ✓ Auth Anthropic OK (contact@ar2100.fr, max)

  Now checking is_fresh_context before printing the welcome box.
```

**Verdict** ✓ — exact format match with the `phase-auth-preflight/SKILL.md` decision-tree row 1 template : `✓ Auth Anthropic OK (<email>, <subscriptionType>)`. Populated with real user values (`contact@ar2100.fr` = Layer 0 primary personal email, `max` = `subscriptionType` returned by `claude auth status` JSON). No drift on casing, parenthesization, comma separator, or field order.

### Observable C — welcome box post-preflight

```
● ┌────────────────────────────────────────────────────────────┐
  │                                                            │
  │     Depose ici ton idee.                                   │
  │                                                            │
  │     Un texte, un PDF, une photo, un lien, un audio —       │
  │     tout est bienvenu. Tu peux aussi juste ecrire.         │
  │                                                            │
  │     (Parcourir les fichiers)                               │
  │                                                            │
  │     Tes fichiers restent avec toi pendant cette session.   │
  │                                                            │
  └────────────────────────────────────────────────────────────┘
```

**Verdict** ✓ — FR welcome box per `welcome_locale = FR` (slash invocation default per v1.3.3 locale resolution rule). ASCII rendering clean, pipe alignment preserved, no Unicode mojibake. `is_fresh_context` check (via `ls` + `test -f CLAUDE.md` + `test -d memory/`) ran and confirmed fresh before the box printed, per `genesis-drop-zone/SKILL.md § Context guard`.

### Observable D — no API key friction

**Verdict** ✓ — the complete flow from `/project-genesis:genesis-drop-zone` invocation through 9-field mirror → consent card → decline bridge → `/exit` contains **zero** mentions of `ANTHROPIC_API_KEY`, zero links to Anthropic Console, zero halt-with-remediation cards, zero subprocess spawn attempts. The drop zone operates purely on the Claude Code Max subscription auth that `phase-auth-preflight` validated in Phase 0.0. This is exactly the v2.0.0 architectural win the test was designed to prove.

### Bonus evidence — downstream v1.3.1 / v1.3.2 / v1.3.3 surfaces still intact post-v2 refactor

Not a primary observable, but the captured transcript also exercises and validates :
- v1.3.1 9-field mirror (aligned table, null-visible convention — `Pour qui : a trouver ensemble`, `Type : a affiner — app web, mobile ou desktop`, `Budget : non mentionne`) ✓
- v1.3.2 consent card with absolute path + halt-on-existing pre-write probe (`Bash(test -e ... && echo "EXISTS" || echo "absent")` → `absent` → proceed) ✓
- v1.3.3 decline bridge in FR (`content_locale = FR` resolved from `langue_detectee = FR`) with canonical text `"Relance-moi quand tu veux la poser sur disque."` ✓

All v1.3.x conversational-layer shipped surfaces survived the v2.0.0 refactor without regression. This closes not only the v1.5.0 → v1.6.x runtime-evidence-gap for Phase 0.0 (the v2 new surface) but also incidentally confirms the v1.3.x surfaces still render correctly after the v2.0.0 subprocess removal.

## Scope excluded — follow-up candidate

The captured test used **typed-text input only** (no `(Parcourir les fichiers)` drag-and-drop attachment). Per user input at test time : "pas glissé-déposé un document dans la drop zone". Runtime evidence for the attachment input modality (PDF extraction / image OCR / multi-file drops) is **not** covered by this log. Candidate follow-up : v2.2.0 multi-modal runtime evidence, or fold into a broader v2.2.0 Layer A polish ship. Not blocking for v2.1.0.

## Drift handling — N/A (none observed)

All four observables passed clean on first try. No drift to fix. v2.1.0 ships as a MINOR with cosmetic + runtime evidence axes as planned.
