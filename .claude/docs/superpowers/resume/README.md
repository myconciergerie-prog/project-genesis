<!-- SPDX-License-Identifier: MIT -->

# .claude/docs/superpowers/resume/

Session resume prompts. Each session closes (per R1.3 close ritual) with a resume prompt written here for the next session to pick up.

## Format

Files are named `YYYY-MM-DD_<slug>.md` and contain:

1. **Context** — what the previous session accomplished, what's in flight, what's blocked
2. **Current state** — git branch state, PR state, worktree state, memory state
3. **The exact next action** — with commands, file paths, and acceptance criteria
4. **The exact phrase** the user should say to Claude Code at session open to resume

## How to use at session open

Per R1.1 step 4, every session reads **the most recent** file in this directory during the open ritual. If the most recent file is stale (older than a week without context), read multiple files back to re-establish context.

## Currently populated

*(None — the first resume prompt will be written at Étape 6 of the v1 bootstrap session, pointing at the next session's work.)*
