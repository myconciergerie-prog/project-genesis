<!-- SPDX-License-Identifier: MIT -->
---
name: Resume prompt — 2026-04-15 v1 bootstrap followup → Étape 5 first skill
description: Session handoff from the v1 bootstrap session (2026-04-14 → 2026-04-15) that shipped the v0.1.0 scaffold. The next session picks up at Étape 5 — first skill implementation in a dedicated worktree PR, targeting v0.2.0
type: resume
previous_session: 2026-04-14 v1_bootstrap (extended to 2026-04-15)
next_action: Étape 5 — implement the `phase-minus-one` skill end-to-end in a dedicated worktree, target v0.2.0 at 7.0/10
---

# Resume prompt — 2026-04-15 v1 bootstrap followup

## Context — what the previous session did

The previous session (2026-04-14 opened, extended through 2026-04-15) was the Project Genesis v1 bootstrap. It accomplished:

1. **Path A of the Meta-Memory architecture** — finalized `~/.claude/CLAUDE.md` (Layer 0 universal) with user profile, hard rules (additive auth, no new windows, R2.1 close-pressure discipline, R9 language policy, async mid-flow questions), workflow patterns (per-project SSH identity, GH_TOKEN env override, fine-grained PAT scope checklist, R8 research cache, best-practice-at-date default, anti-Frankenstein, cross-project research sharing), journal system (6th memory type), and machine-specific Chrome profiles map.

2. **Applied the v0 template recursively** — the v0 template committed in aurum-ai at `0b1de3d` was used to bootstrap this repo. Compiler-bootstrapping philosophy. Every friction from v0 surfaced in real time during self-application and informed v1 specs.

3. **Rules alignment** — froze R1-R10 for Genesis per the Étape 2 scoreboard (KEEP R2; ADAPT R1, R3, R4, R5, R6; INHERIT R8, R9 from Layer 0; DROP R7; NEW R10). Full rules in `.claude/docs/superpowers/rules/v1_rules.md`.

4. **Research burst** — 7 R8 cache entries written:
   - `sota/open-source-license-for-dev-tooling_2026-04-14.md`
   - `sota/claude-code-plugin-distribution_2026-04-14.md`
   - `sota/spdx-headers_2026-04-14.md`
   - `sota/claude-in-ide-tools_2026-04-15.md`
   - `sota/claude-ecosystem-cross-os_2026-04-15.md`
   - `stack/claude-code-plugin-structure_2026-04-14.md`
   - `stack/claude-code-session-jsonl-format_2026-04-14.md`

5. **Design specs captured** — 4 v1 specs + 1 v2 spec (to be renamed/merged in Étape 5):
   - `specs/v1_phase_5_5_auth_preflight_learnings.md` — live-dogfooding learnings for Phase 5.5
   - `specs/v1_phase_minus_one_first_user_bootstrap_flow.md` — stratified spec with 2 refinement layers; multidevice core; 3-mode ladder
   - `specs/v1_pepite_discovery_flagging.md` — red-light pépite system, 7th memory type, cross-project routing
   - `specs/v2_phase_minus_one_dependencies_automation.md` — original v2 spec, to merge with the v1 flow spec at Étape 5

6. **Auth pre-flight (Étape 4a-c)** — generated `id_ed25519_genesis` + added `Host github.com-genesis` to `~/.ssh/config`; user created fine-grained PAT + empty repo via paste-back; three-probe pre-flight tests (SSH + `gh api user` + `gh api repos/.../.../`) all passed.

7. **Stack installations** — Playwright MCP added via `claude mcp add --scope user playwright npx @playwright/mcp@latest`; Claude in Chrome extension installed by user in Profile 2; Claude Code VS Code extension confirmed already present and linked.

8. **Scaffold shipped** — Étape 4d wrote 39 files. Étape 4e ran the one-time R2.1 exception: `git init -b main`, secrets sneak check clean, first commit `ac9801a50313cfde45fa3524414e6c907e47eefc` (`bootstrap: project-genesis v0.1.0 scaffold`), remote `git@github.com-genesis:myconciergerie-prog/project-genesis.git`, push to origin main. Repo is live.

9. **Cross-project additive writes to Aurum auto-memory** — `reference_genesis_research_cache_pointer_2026-04-15.md` pointer file + `project_meta_memory_architecture.md` append with the pépite integration. Zero violation of the Aurum scope lock (auto-memory is hors-repo).

10. **This resume prompt** — written in the first real Genesis worktree `chore/2026-04-15_resume-prompt` per R2.1, merged via `gh pr merge --squash`, demonstrating the R2.1 flow on the first post-bootstrap PR.

## Current state at session handoff

- **Repo**: `C:\Dev\Claude_cowork\project-genesis\`
- **GitHub**: `myconciergerie-prog/project-genesis` (private)
- **main branch**: squash-merged `chore/2026-04-15_resume-prompt` on top of `ac9801a` — origin is one commit ahead of the bootstrap scaffold. Local root may be behind until the next session runs `git fetch && git pull --ff-only` on main.
- **Self-rating**: v0.1.0 = 6.0/10 (from CHANGELOG.md). Target for v0.2.0 = 7.0/10 after first skill ships. Target for v1.0.0 = 8.5/10.
- **Working tree**: clean (R1.1 step 3 passes; there may be a local-behind-origin delta to fast-forward sync).

## Known issue carried over — GitHub repo description garbled

The repo description on GitHub still contains a copy-paste artefact from Étape 4b (user copied a table cell with inline notes into the description field). The fine-grained PAT used during Étape 4c was missing `Administration: Read and write` scope, so `gh api --method PATCH repos/... -f description=...` returned HTTP 403. Two fix options, both non-blocking:

1. **Manual via web UI** (fastest, 30 seconds): open `https://github.com/myconciergerie-prog/project-genesis` → the About panel on the right side of the Code tab → click the pencil icon → replace the description with:
   ```
   Project Genesis — recursive project bootstrap template, shipped as a Claude Code plugin
   ```
2. **PAT rotation**: rotate the PAT at `https://github.com/settings/personal-access-tokens` with `Administration: Read and write` added to the scope list, update `GH_TOKEN` in `.env.local`, then Claude can PATCH the description via API.

Either way, cosmetic and non-blocking for Étape 5.

## Known operational hangover — old empty folder

The local folder `C:\Dev\Claude_cowork\project-genesis-2026\` still exists (empty, held by Claude Code's cwd during the bootstrap session). After the session closes and Claude Code releases its cwd, the user can delete it manually:

```powershell
Remove-Item -Recurse -Force "C:\Dev\Claude_cowork\project-genesis-2026"
```

Non-blocking. The real working directory is `C:\Dev\Claude_cowork\project-genesis\`.

## The next concrete action — Étape 5: implement the `phase-minus-one` skill

**Why start with `phase-minus-one`**: it is the most pain-driven skill, has the deepest specification (stratified with 2 refinement layers in `specs/v1_phase_minus_one_first_user_bootstrap_flow.md`), and represents the biggest v1 improvement over v0 (the entire Dependencies Pre-flight concept did not exist in v0). Shipping it first takes the repo from scaffold state to functional-first-skill state, which is the v0.2.0 milestone at 7.0/10.

### Subtasks for Étape 5 (first feat worktree PR)

1. **Sync main to origin** (if behind):
   ```bash
   cd C:\Dev\Claude_cowork\project-genesis
   git fetch origin
   git pull --ff-only origin main
   ```
   This is allowed in root — it is a pure fast-forward, not a hand-edit. R2.1 forbids edits, not mechanical syncs.

2. **Create the feat worktree** per R2.1:
   ```bash
   cd C:\Dev\Claude_cowork\project-genesis
   git clone . .claude/worktrees/feat_2026-04-XX_phase-minus-one-skill
   cd .claude/worktrees/feat_2026-04-XX_phase-minus-one-skill
   git config user.email myconciergerie@gmail.com
   git config user.name myconciergerie-prog
   git checkout -b feat/2026-04-XX_phase-minus-one-skill
   git remote set-url origin git@github.com-genesis:myconciergerie-prog/project-genesis.git
   ```

3. **Read the spec** — `specs/v1_phase_minus_one_first_user_bootstrap_flow.md` in full, including both refinement layers. This spec contains the canonical design — implementation is a faithful translation of the spec, not a reinterpretation.

4. **Implement `skills/phase-minus-one/`** with:
   - `SKILL.md` describing the skill, its trigger, its mode choice, its flow
   - `detect.py` or `detect.sh` for baseline detection (OS, package manager, Node, Git, VS Code, Chrome, existing MCPs, Claude in Chrome extension presence via native messaging host config file)
   - `install-manifest.yaml` with per-OS install commands (Windows `winget`, macOS `brew`, Linux `apt` / `dnf` / `pacman`)
   - `gap-report.md` template for the gap report card
   - `consent-card.md` template (3-mode ladder + per-item opt-in)
   - `modes/detailed.md` + `modes/semi-auto.md` + `modes/auto.md` — mode-specific prompts
   - `sign-in-round.md` template for the batched sign-in checklist
   - `restart-round.md` template for the batched restart prompt
   - `verification.md` template for the final health check card
   - `optional-bonus.md` for Phase -1.7 (Antigravity, Codespaces, Termux, voice mode)
   - Mobile companion branching logic (Claude Code Remote Control for Claude Max users, Codespaces fallback for Pro users)

5. **Update `CHANGELOG.md`** with the v0.2.0 entry + fresh 5-axis self-rating block. Target average 7.0/10.

6. **Bump `plugin.json` version** to `0.2.0` in the same PR (not a separate commit).

7. **Commit** with message `feat(phase-minus-one): implement Dependencies Pre-flight skill end-to-end` + Co-Authored-By line.

8. **Push** the branch: `git push -u origin feat/2026-04-XX_phase-minus-one-skill`

9. **Open PR**: `GH_TOKEN="$GH_TOKEN" gh pr create --title "feat(phase-minus-one): Dependencies Pre-flight skill v0.2.0" --body "..."`

10. **Squash merge**: `GH_TOKEN="$GH_TOKEN" gh pr merge <pr-number> --squash` (NO `--delete-branch` per R2.3).

11. **Tag** `v0.2.0` on the squashed merge commit after origin confirms the merge:
    ```bash
    git fetch origin
    git tag v0.2.0 origin/main
    git push origin v0.2.0
    ```

12. **Memory entry**: write `memory/project/session_v0_2_0_skill_phase_minus_one.md` documenting the session — what was built, self-rating, known gaps for v0.3.0.

13. **Resume prompt + goodbye card** for the next-next session.

### Acceptance criteria for v0.2.0

- `skills/phase-minus-one/` contains all components listed above
- Every file has an SPDX header
- `CHANGELOG.md` updated with v0.2.0 entry and self-rating ≥ 7.0/10
- `plugin.json` version = `0.2.0`
- PR cleanly squash-merged to origin main
- Git tag `v0.2.0` on origin
- Worktree retained per R2.5 (never `rm -rf`)

### Things to NOT do in Étape 5 (anti-Frankenstein reminders)

- **Do not implement more than one skill** — `phase-minus-one` only. Other skills (journal-system, session-post-processor, pepite-flagging, auth-preflight, genesis-protocol) land in their own worktrees in later sessions.
- **Do not wire `SessionEnd` hooks** automatically — deferred until manual mode validates per anti-Frankenstein.
- **Do not add features outside the spec** — if the spec does not cover it, it does not go in v0.2.0.
- **Do not skip the self-rating block** — R10.3 gate.
- **If the user says `frankenstein`** during this session — back out of the last proposal immediately.

## Exact phrase for the next session

Open Claude Code in `C:\Dev\Claude_cowork\project-genesis\` and say:

```
On reprend Étape 5 Project Genesis. Lis le resume prompt le plus récent
dans .claude/docs/superpowers/resume/, puis implémente le skill
phase-minus-one end-to-end dans un worktree feat/. Target v0.2.0 à 7.0/10.
```

Claude Code then runs R1.1 open ritual (date, MEMORY.md, master.md, `git status -s`, latest resume prompt = this file, R8 TTL scan on `research/INDEX.md` — two `stack/` entries expire 2026-04-15 so they may need archival depending on the open date, `sota/` entries expire 2026-04-21/22), creates the worktree per R2.1, reads this file in full, reads `specs/v1_phase_minus_one_first_user_bootstrap_flow.md`, and implements.

## References that Étape 5 will consume

- `specs/v1_phase_minus_one_first_user_bootstrap_flow.md` — the canonical spec (two stratified layers)
- `specs/v2_phase_minus_one_dependencies_automation.md` — the original v2 spec, merge into the above at Étape 5
- `research/sota/claude-ecosystem-cross-os_2026-04-15.md` — per-OS matrix + Claude Code Remote Control + 280 connectors
- `research/sota/claude-in-ide-tools_2026-04-15.md` — VS Code extension = `ide` MCP server + Antigravity
- `research/sota/claude-code-plugin-distribution_2026-04-14.md` — plugin install mechanics
- `rules/v1_rules.md` — R1-R10 full rules
- `~/.claude/CLAUDE.md` — Layer 0 (auto-loaded)
- `memory/master.md` + `memory/project/session_v1_bootstrap.md` — prior context

## Farewell notes to the next session's Claude

The v0 template was a midwife for v1 via recursive self-application. Étape 5 is where v1 stops being specifications and becomes functioning code. Keep the 8.5/10 target honest — do not inflate the rating. Do not add speculative features. If something in the spec feels wrong during implementation, update the spec and note why, don't silently diverge. The spec files are living documents layered over time (mirror of the journal system's stratification), so appending a "Refinement 2026-04-XX" section is the correct pattern, not rewriting earlier sections.

Good luck. The recursive loop continues.
