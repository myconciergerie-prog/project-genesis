<!-- SPDX-License-Identifier: MIT -->
---
name: Phase -1.3 mode 3 — auto
description: Runner prompt for the auto mode. Claude runs the full install pass end-to-end, pausing only at the five security-floor categories (admin password, sign-in, extension grant, 2FA, device authorization). Never silent failure — always graceful paste-back pause.
type: mode_runner
mode: 3
stage: -1.3
---

# Phase -1.3 — Mode 3 (auto)

Runs after the user picked mode 3 in the consent card. Purpose: magical speed. Claude runs every approved install in sequence. The user's attention is needed only at the security floor.

**Time budget**: ~5 minutes, dominated by download times and login events.

**Target audience**: experienced devs, repeat bootstraps on known machines, users who want speed.

**Non-negotiable guarantee**: mode 3 is **never a silent failure**. It pauses gracefully at every unavoidable manual step, surfaces a paste-back micro-card, and resumes autonomous mode after the user unblocks.

## Flow

Execution is a plain loop over the approved items in dependency order:

1. Pull the next item from `memory/reference/consent-log.md`.
2. If its `user_action_required` is one of `admin_password | sign_in | extension_grant | pairing | 2fa | device_auth`, enter the pause sub-flow (below).
3. Otherwise, run the command from `install-manifest.yaml` via Bash.
4. Capture the output. On non-zero exit, enter the failure sub-flow (below).
5. Re-run the item's probe from `detect.sh`. If still missing, queue a restart item for Phase -1.5 and move on.
6. Advance.

No cards, no per-item confirmations. Claude talks to the user only to report progress (one short line per item: *"{{LABEL}} installed"*) or to enter a pause.

## Pause sub-flow (security-floor step)

When a step hits a security-floor category, mode 3 pauses like this:

```
----- PAUSE — security-floor step -----

Step         : {{ORDINAL}} / {{TOTAL}} — {{LABEL}}
Category     : {{CATEGORY}}
What you do  : {{USER_INSTRUCTION}}
URL (if any) : {{PASTE_BACK_URL}}

Reply with  "done"  when you've completed the step.
Reply with  "skip"  to fall back to paste-back at Phase 5.5 for this item.
----------------------------------------
```

The `USER_INSTRUCTION` line is one sentence, specific to the category:

- **admin_password** → *"Type your admin password when the UAC / sudo prompt appears in the terminal."*
- **sign_in** → *"Open the URL above, sign in with your Anthropic / GitHub / Google account, then reply `done`."*
- **extension_grant** → *"Open the URL, install the extension, accept the permission prompt, pin it, then reply `done`."*
- **2fa** → *"Enter the 2FA code from your authenticator on the page you just opened, then reply `done`."*
- **device_auth** → *"Paste the device code shown above into the page you just opened, then reply `done`."*
- **pairing** → *"Open the Claude mobile app, accept the pairing prompt, then reply `done`."*

On `done`: re-run the probe, mark the item installed if healthy, resume autonomous mode.

On `skip`: mark the item as `user_skipped`, record the fallback in `memory/reference/automation-stack.md`, resume with the next item.

## Failure sub-flow

When a command exits non-zero or the post-install probe still says missing, mode 3 does three things in sequence before giving up:

1. **Retry once** — transient network glitches are common, one silent retry catches most of them.
2. **Alternate install path** — if the manifest has an alternate (e.g. `brew` → `brew --cask`, or `apt` → direct `.deb`), try it.
3. **Fall back to paste-back** — surface a micro-card: *"I could not install {{LABEL}} automatically. Here is the manual link: {{URL}}. Reply `done` after you install, or `skip`."*

No silent failures, no infinite retries. At most one automatic retry and one alternate attempt before the user is pulled in.

## Plan-tier branch

Before entering the loop, mode 3 checks `PLAN_TIER` from the gap report:

- **max** or higher: include Remote Control pairing in the install list.
- **pro** / **team**: skip Remote Control, queue the Codespaces fallback for Phase -1.7 as an advisory (not mandatory).
- **free**: Phase -1 never reaches mode 3 — blocked at Phase -1.1.

## Progress reporting

Mode 3 emits one short status line per item, prefixed by an ordinal:

```
[1/9] Node.js LTS          installed (v20.12.1)
[2/9] Git                  installed (2.44.0)
[3/9] VS Code              installed (1.115.0)
[4/9] Google Chrome        installed (124.0.6367.201)
[5/9] GitHub CLI           installed (2.48.0)
[6/9] VS Code extension    installed, restart queued
[7/9] Playwright MCP       installed, restart queued
[8/9] Claude in Chrome     PAUSE — extension grant required
```

Every fourth item or so, Claude may emit a single-sentence elapsed-time update: *"5 min elapsed, 3 items remaining"*.

## Completion

Once every item is resolved, mode 3 hands control to Phase -1.4 if there are deferred sign-ins, else directly to Phase -1.5 if there are queued restarts, else directly to Phase -1.6 for verification.

## Pause handling

`pause` halts mode 3 immediately. Any in-flight Bash command is allowed to finish, but no new item is started. The user can resume with `go` or `resume auto`, or switch to mode 2 with `switch to semi-auto`.

## Anti-Frankenstein reminders specific to mode 3

- **Never swallow failures** — mode 3's speed comes from autonomy, not from hiding problems.
- **Never exceed one automatic retry and one alternate path** — further attempts must go to the user.
- **Never install items not in the approved consent log**, even if detect.sh reveals new opportunities mid-flow.
- **Never merge pauses into bigger batches** — each security-floor step gets its own pause card, so the user always knows exactly what they're being asked to do.
- **Never call mode 3 "auto" without the security-floor pauses** in the same breath — the magical feel depends on users trusting the pause discipline.
