<!-- SPDX-License-Identifier: MIT -->
---
name: Resume prompt — 2026-04-16 v1.1.0 → v1.2 dogfood toward v2
description: Handoff from the v1.1 self-dogfood session to the next session. v1.1 demolished the auth wall and produced the v2 Promptor fusion vision. v1.2 continues the dogfood with the proven auth path, then begins the conversational surface.
type: resume
previous_session: v1.1.0 self-dogfood (PR #20, tag v1.1.0)
next_action: Complete the self-dogfood with v1.1 auth fix, then begin v2 conversational surface
---

# Resume — 2026-04-16 v1.1.0 → v1.2 dogfood toward v2

## What v1.1 did

The self-dogfood session ran the genesis-protocol against itself and hit the
auth wall at Phase 3 Step 3.4. Instead of forcing completion, the session
pivoted to analysis — producing the v2 vision and proving the CLI-first auth
path. Key deliverables:

- **Auth revolution proven**: `gh auth login --web` + `Start-Process` Chrome
  Profile routing + `gh ssh-key add` + `gh repo create --push` = 1 OAuth click
  instead of 6 manual browser steps. Tested end-to-end on this machine.
- **v2 Vision spec**: `specs/v2_vision_promptor_fusion.md` — Promptor-style
  conversational bootstrap, backed by 5 parallel research agents.
- **18 frictions logged**: `memory/project/selfdogfood_friction_log_2026-04-16.md`
- **4 feedback principles** at workspace level: Victor test, security floor
  honesty, execution tunnel vision, automation claim verification.
- **Working auth path** documented at workspace level:
  `~/.claude/projects/C--Dev-Claude-cowork/memory/feedback_gh_auth_working_path.md`

## Current state

- Repo: `myconciergerie-prog/project-genesis` on main @ v1.1.0
- git status: clean
- All pushed, all synced
- `genesis-selfdogfood` standalone repo: DELETED (paradox resolved —
  self-dogfood is a branch of project-genesis, not a separate repo)
- `gh auth`: `myconciergerie-prog` active with OAuth scopes
  `repo,workflow,read:org,admin:public_key`
- SSH: `github.com-genesis-selfdogfood` alias exists in `~/.ssh/config`
  (can be cleaned up or left — not harmful)

## What v1.2 needs to do — TWO PHASES

### Phase A — Complete the dogfood (v1.2.0)

Re-run the genesis-protocol with the v1.1 auth fix on a REAL downstream
project (not Genesis itself — that was the paradox). Pick a simple project
idea and bootstrap it end-to-end:

1. Create an empty folder with a `config.txt`
2. Run the full 7-phase protocol using the v1.1 CLI-first auth
3. Verify: repo on GitHub, v0.1.0 tagged, all probes GREEN
4. Log any NEW frictions (the 18 from v1.1 should be resolved)
5. If clean → v1.2.0 tagged as "first successful downstream bootstrap"

Suggested test project: something simple and real — not another self-reference.
Ask the user what they want to bootstrap.

### Phase B — Begin v2 surface (v1.3+)

With the protocol proven end-to-end, begin implementing the conversational
surface from `specs/v2_vision_promptor_fusion.md`:

1. Replace `config.txt` with a conversation (Etape 1 — L'Etincelle)
   - 2-3 natural language questions
   - Derive slug, license, plugin flag from answers
   - The meta-question: "Tu veux decider ou je decide ?"
2. Replace consent cards with a progress stream (Etape 2 — La Creation)
   - "Je prepare ton espace..." / "Je connecte a GitHub..." / "C'est pret!"
3. Add the mirror step (Etape 3 — Le Miroir)
   - Show what was created, ask if adjustments needed

The UX toolkit research is in:
- `research/sota/zero-friction-bootstrap-ux_2026-04-16.md`
- `research/sota/gh-cli-single-click-auth_2026-04-16.md`

Key tools identified: @clack/prompts for wizard skeleton, Charm Gum for
beautiful prompts, cli-spinners for progress, terminal bell for completion.

## Files to read at session open

1. `memory/MEMORY.md` (index)
2. `memory/master.md` (stable vision)
3. `memory/project/session_v1_1_selfdogfood.md` (what just happened)
4. `specs/v2_vision_promptor_fusion.md` (where we're going)
5. `memory/project/selfdogfood_friction_log_2026-04-16.md` (what to NOT repeat)
6. This resume prompt

## Feedback principles to load from workspace memory

At `~/.claude/projects/C--Dev-Claude-cowork/memory/`:
- `feedback_victor_test.md` — every step must pass the 77-year-old threshold
- `feedback_security_floor_honesty.md` — 5 true categories, rest is artefact
- `feedback_execution_tunnel_vision.md` — friction IS the finding
- `feedback_automation_claim_verification.md` — prove X works before claiming X
- `feedback_gh_auth_working_path.md` — the exact auth sequence that works

## Exact phrase for the next session

Open Claude Code in `C:\Dev\Claude_cowork\project-genesis\` and say:

    On continue le dogfood Genesis. v1.1 a prouve le chemin auth CLI-first.
    Lis le resume v1.1→v1.2 et la vision v2. Phase A : bootstrap un vrai
    projet downstream end-to-end avec le protocole corrige. Phase B : on
    commence la surface conversationnelle Promptor. Propose un projet test
    simple et reel pour Phase A.
