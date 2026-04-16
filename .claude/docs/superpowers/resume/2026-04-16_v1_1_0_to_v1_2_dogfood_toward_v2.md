<!-- SPDX-License-Identifier: MIT -->
---
name: Resume prompt — 2026-04-16 v1.1.0 → v1.2 dogfood toward v2
description: Handoff from the v1.1 self-dogfood session. v1.2 tests Genesis on a REAL downstream project in a SEPARATE folder — Genesis must not know it's being tested. Two sessions needed, two separate Claude Code instances.
type: resume
previous_session: v1.1.0 self-dogfood (PR #20, tag v1.1.0)
next_action: Bootstrap a real downstream project from a fresh folder, then bring findings back
---

# Resume — 2026-04-16 v1.1.0 → v1.2 dogfood toward v2

## What v1.1 did

Auth wall demolished. 6 manual browser steps → 1 OAuth click.
v2 Promptor fusion vision produced. 18 frictions logged. 4 principles gravés.
See `memory/project/session_v1_1_selfdogfood.md` for full details.

## Current state

- Repo: `myconciergerie-prog/project-genesis` on main, tag v1.1.0
- git status: clean, all pushed
- `gh auth`: `myconciergerie-prog` active (OAuth, all scopes)

## CRITICAL — How v1.2 dogfood MUST be structured

### The paradox lesson from v1.1

v1.1 ran Genesis on itself from inside project-genesis/. This caused:
- Standalone repo paradox (had to delete genesis-selfdogfood)
- Genesis "knew" it was self-testing (contaminated the test)
- Deployment confusion (which repo is the real one?)

### The correct structure for v1.2

**TWO separate Claude Code sessions. TWO separate folders. Genesis does not know it's being tested.**

```
SESSION 1 — The user bootstrapping a new project
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WHERE:   Open Claude Code in C:\Dev\Claude_cowork\<new-project>\
         (an EMPTY folder at the ROOT of Claude_cowork, sibling
         to project-genesis, NOT inside it)

WHAT:    Write a config.txt describing a simple real project.
         Then say "bootstrap this project" or "lance genesis".
         Genesis runs as a PLUGIN — the user is a user, not a tester.

AUTH:    The FULL auth flow must execute:
         - gh auth login --web (even if already authenticated —
           the protocol must handle "already logged in" gracefully)
         - SSH keygen for the new project
         - gh ssh-key add
         - gh repo create
         This tests the v1.1 auth fix for real.

END:     The new project is on GitHub, v0.1.0 tagged, 3 probes GREEN.
         The new project has its OWN memory/, rules, research cache.
         Session closes with ITS OWN resume prompt inside the new project.

NOTE:    DO NOT open project-genesis during this session.
         DO NOT reference the friction log.
         DO NOT mention "dogfood" or "testing".
         Be a user. Experience the protocol as Victor would.
         Note frictions as they happen — in your head, not in project-genesis.


SESSION 2 — Bringing findings back to Genesis
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WHERE:   Open Claude Code in C:\Dev\Claude_cowork\project-genesis\

WHAT:    Report what happened in Session 1.
         - New frictions found (or "zero new frictions" if clean)
         - Auth flow outcome (did the v1.1 path work without surprises?)
         - Anything that surprised a "first-time user"
         - Update friction log if needed
         - Tag v1.2.0 if the downstream bootstrap was clean

THEN:    Begin Phase B — the v2 conversational surface.
         Read specs/v2_vision_promptor_fusion.md and start implementing.
```

### Why two sessions matter

| Single session (WRONG) | Two sessions (RIGHT) |
|---|---|
| Genesis sees its own code and memory | Genesis sees only the new project |
| Auth is pre-configured, shortcuts happen | Auth runs fresh, tests the real flow |
| Frictions get "fixed live" instead of logged | Frictions are experienced, then reported |
| The downstream project is entangled with Genesis | The downstream project is independent |
| Deployment confusion (which repo?) | Clean: one repo per project |

## Suggested test project for Session 1

Something simple, real, NOT a developer tool:
- A recipe collection app
- A neighborhood event board
- A personal finance tracker ("Mon Budget" — the Victor example)
- A reading list / book notes app

Ask the user to pick or propose. The project must be real enough that
it would survive beyond the test — not a throwaway.

## Auth pre-check before Session 1

Before opening Claude Code in the new folder, verify:
```bash
gh auth status
# Should show myconciergerie-prog as active
# If not: the auth flow in Session 1 will handle it — that's the test
```

Also verify Genesis plugin is installable:
```bash
# In any Claude Code session:
/plugin install project-genesis@myconciergerie-prog/project-genesis
```

If the plugin install doesn't work, Session 1 falls back to
manual skill invocation (reading the SKILL.md files directly).
Either path is a valid dogfood.

## Files to read at Session 2 open (NOT Session 1)

1. `memory/MEMORY.md`
2. `memory/master.md`
3. `specs/v2_vision_promptor_fusion.md`
4. `memory/project/selfdogfood_friction_log_2026-04-16.md`
5. This resume prompt
6. Whatever the Session 1 user noted as frictions

## Exact phrases

**Session 1** — open Claude Code in `C:\Dev\Claude_cowork\<new-project>\` :

    J'ai une idee de projet. (puis decrire l'idee naturellement)

That's it. No mention of Genesis, no "lance le protocole", no technical
language. If Genesis is installed as a plugin, it should recognize the
trigger and propose to bootstrap. If not, the user says "bootstrap this
project" and Genesis activates.

**Session 2** — open Claude Code in `C:\Dev\Claude_cowork\project-genesis\` :

    Je reviens du dogfood v1.2. J'ai bootstrappé <nom-du-projet> dans
    un dossier séparé. Voilà ce qui s'est passé : <findings>.
    Lis le resume v1.1→v1.2 et on met à jour Genesis avec les résultats.
    Puis on attaque Phase B — la surface conversationnelle v2.
