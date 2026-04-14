<!-- SPDX-License-Identifier: MIT -->
---
name: Phase -1.6 verification pass
description: Final silent health check of the installed stack after Phase -1.5 restart round. Re-runs detect.sh, probes a few extra live surfaces (MCP list, code --list-extensions, ssh -T github.com generic), renders a single summary card, and writes memory/reference/automation-stack.md. Ready for Phase 0 when green.
type: template
stage: -1.6
---

# Phase -1.6 — Verification pass

Runs after Phase -1.5 restart round. Silent probes, one card output, one memory file. No user interaction unless a probe reveals a regression.

## Probes

Runs in this order:

1. `detect.sh` — same probe as Phase -1.0, now re-run against the post-install state.
2. `claude mcp list` — confirms every approved MCP is present and reports its health status.
3. `code --list-extensions | grep -i anthropic.claude-code` — confirms the VS Code extension is installed (it should also appear in `claude mcp list` as `ide`).
4. `ssh -T git@github.com` — generic GitHub SSH handshake, no specific alias. Expected output contains the phrase "successfully authenticated" even though it exits non-zero.
5. `git --version`, `node --version`, `gh --version` — cheap sanity checks that the installs put the binaries on PATH.
6. `claude --version` — cheap but important — confirms Claude Code survived the restart in a healthy state.
7. Optional Claude in Chrome ping — if the install-log says the extension was installed, run a minimal `/chrome ping` probe and capture the reply (non-blocking — the extension may not be pinned yet).

Every probe that fails is recorded with its error output in the health card; nothing fails the skill outright.

## Verification card template

```
===== Phase -1.6 — Verification =====

Installed and healthy
  [x] {{ITEM_1}}              (v{{VERSION_1}})
  [x] {{ITEM_2}}              (v{{VERSION_2}})
  ...

MCPs loaded
  [x] ide                      (Claude Code VS Code extension)
  [x] playwright               (@playwright/mcp@latest)
  ...

Live surface probes
  [x] ssh -T git@github.com    (authenticated)
  [x] claude --version         ({{CLAUDE_VERSION}})
  [x] claude mcp list          ({{MCP_COUNT}} MCPs)
  [ ] /chrome ping             (extension not yet pinned — non-blocking)

Fallbacks declared
  [~] {{ITEM_X}}                (fell back to paste-back at Phase 5.5)
  [~] {{ITEM_Y}}                (skipped by user)

Status: READY FOR PHASE 0
       (or)
Status: READY FOR PHASE 0 WITH FALLBACKS
       (or)
Status: BLOCKED — see {{BLOCKER_REASON}}

====================================
```

The three possible statuses:

- **READY FOR PHASE 0** — everything green, no fallbacks.
- **READY FOR PHASE 0 WITH FALLBACKS** — core green, optional / non-core items skipped or fell back to paste-back. Phase 5.5 will branch on these.
- **BLOCKED** — a core item failed and cannot fall back. Surface the specific blocker, propose a one-line fix, and do NOT hand control to Phase 0. User must resolve before continuing.

## Writing memory/reference/automation-stack.md

Phase -1.6 writes a single reference-memory file summarising the final state:

```markdown
---
name: Automation stack (machine state)
description: What dev stack is installed on this machine for Genesis runs, recorded by the phase-minus-one skill after the Phase -1.6 verification pass
type: reference
machine_id: {{HOSTNAME}}
os_family: {{OS_FAMILY}}
phase_minus_one_last_run: {{DATE}}
phase_minus_one_mode: 1 | 2 | 3
---

## Installed (Phase -1 complete)
- Node.js LTS           v{{VERSION}}    installed_at: {{DATE}}
- Git                   v{{VERSION}}    installed_at: {{DATE}}
- VS Code               v{{VERSION}}    installed_at: {{DATE}}
- Google Chrome         v{{VERSION}}    installed_at: {{DATE}}
- GitHub CLI            v{{VERSION}}    installed_at: {{DATE}}
- Claude Code VS Code extension         installed_at: {{DATE}}
- Playwright MCP        latest          installed_at: {{DATE}}
- Claude in Chrome      (paste-back)    installed_at: {{DATE}}

## Multi-device
- Claude mobile app     platform={{IOS|ANDROID}}   signed_in: yes
- Remote Control        paired: yes | no | n/a (Pro plan)

## Fell back to paste-back at Phase 5.5
- (none)  or  (list per item with reason)

## Optional bonuses accepted in Phase -1.7
- (none)  or  (list per item)

## Notes
- Run again with `/phase-minus-one` if you change hardware or add a new account.
- This file is rewritten on every run, so old state is not preserved. Use git log to read history.
```

The file lives in `memory/reference/` so that future sessions reading `memory/MEMORY.md` index can see it and skip re-running Phase -1 when unchanged.

## Idempotency

Re-running the skill on a machine that already has this file is safe: Phase -1.0 reads the current state, Phase -1.1 renders a near-empty gap report, Phase -1.2 offers a short consent card (usually just optional bonuses), and Phase -1.3 runs only the newly-requested items.

## Parsing the verification outcome

Claude reads the card's final status line and branches:

- **READY FOR PHASE 0**: emit a one-sentence confirmation, optionally prompt for Phase -1.7 bonuses if the consent log had any, then hand control back to the Genesis protocol.
- **READY FOR PHASE 0 WITH FALLBACKS**: same as above, but the confirmation mentions the fallbacks briefly.
- **BLOCKED**: render the blocker with the proposed fix, wait for the user to unblock, re-run Phase -1.6 only (not the whole skill) once they reply.

## Anti-Frankenstein reminders

- **Never treat a failed probe as "good enough"** — mark it either fixed or fall-back, never ignore.
- **Never re-run earlier phases from the verification step** — the restart round already happened; Phase -1.6 is the terminal check, not a loop back.
- **Never hold state in RAM beyond this card render** — everything the skill knows at the end of Phase -1.6 must be written into `memory/reference/automation-stack.md` so the next session sees it.
