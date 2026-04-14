<!-- SPDX-License-Identifier: MIT -->
---
name: Phase -1.3 mode 2 — semi-auto
description: Runner prompt for the semi-auto mode. Claude proposes each command as a confirmable card, runs it via Bash on user confirm, and shows the output summary. Trades teaching depth for speed, keeps user-in-the-loop on every action.
type: mode_runner
mode: 2
stage: -1.3
---

# Phase -1.3 — Mode 2 (semi-auto)

Runs after the user picked mode 2 in the consent card. Purpose: control without typing. Each command surfaces as a one-card confirmable; the user types `yes` / `no` / `skip` and Claude runs the approved ones.

**Time budget**: 10–15 minutes for a typical missing stack.

**Target audience**: devs who want to see every command before it runs but don't want to type each one themselves.

## Flow

For each approved item in `memory/reference/consent-log.md`, in dependency order:

1. **Render a command card** — format below.
2. **Wait for the user's reply** — one of `yes` / `no` / `skip` / `pause`.
3. **On `yes`**: run the command via Bash, capture stdout + stderr to a memory scratchpad, re-run the item's probe from `detect.sh`.
4. **Show the outcome** — success / failure / partial — in a single line.
5. **Advance** to the next item.

## Command card template

```
----- {{ORDINAL}} / {{TOTAL}} — {{LABEL}} -----

Why      : {{RATIONALE}}
Command  : {{COMMAND}}
Needs    : {{USER_ACTION_REQUIRED}}
Cost     : {{EST_COST_MIN}} min

Reply:  yes / no / skip / pause
---------------------------------------
```

Notes:

- The `Needs` line echoes `user_action_required` from the manifest, so the user knows before approving if this step will trigger a UAC, a sign-in, an extension grant, or a restart.
- The `Command` line is exactly what Claude will run via Bash. No heredocs, no pipelines that the user cannot anticipate.
- If the item is a paste-back (e.g. Chrome extension install), the command field holds the URL prefixed by `PASTE_BACK_URL=` and the card text makes clear the user — not Claude — will drive the install in Chrome.

## Security-floor stops

Mode 2 already pauses on every command, so the security floor adds no extra stops — it simply surfaces the type of action inline. The flow:

- `user_action_required == admin_password`: the card's `Needs` line says so. On `yes`, Claude runs the command via Bash, which triggers UAC / sudo in the user's terminal. The user handles the prompt.
- `user_action_required == sign_in`: Claude defers the sign-in to Phase -1.4 batched round. The card says so explicitly: *"Needs: sign-in, deferred to Phase -1.4"* — the user still approves whether to install the parent item (e.g. the browser before the sign-in step).
- `user_action_required == extension_grant`: the card is a paste-back micro-card, not a runnable command. On `yes`, Claude renders the Chrome Web Store URL and waits for confirmation.
- `user_action_required == pairing`: the card tells the user to open the Claude mobile app and walks them through the ceremony on `yes`.

## Batching optimisation

Where a run of adjacent items all have `user_action_required == none` or `admin_password`, mode 2 may offer a **batched card** covering several items at once, so the user clicks one `yes` for a group. Example:

```
----- 3–6 / 9 — Layer 3 essentials (batched) -----

Why      : Node, Git, VS Code, Chrome are all winget installs with admin pwd.
Commands :
  winget install -e --id OpenJS.NodeJS.LTS
  winget install -e --id Git.Git
  winget install -e --id Microsoft.VisualStudioCode
  winget install -e --id Google.Chrome
Needs    : one UAC prompt (winget elevates once per session)
Cost     : 5 min total

Reply:  yes / no / per-item (expands to individual cards)
---------------------------------------
```

`per-item` unfolds the batch back into individual cards for fine-grained control. Batching is opt-in on the user's side — the card always offers the `per-item` escape.

## On failures

- **`no`** or **`skip`**: mark the item as `user_skipped`, add a fallback note, move on.
- **Command exits non-zero**: show the first 20 lines of stderr, ask the user: *"retry / skip / abort"*. Honour the answer.
- **Probe after install still says `missing`**: the install silently no-op'd (PATH not refreshed, restart needed). Queue a restart item for Phase -1.5 and move on.

## Completion

Once every item is resolved (installed or skipped or deferred), mode 2 ends. Pending sign-ins go to Phase -1.4; pending restarts go to Phase -1.5.

## Pause handling

Same as mode 1 — `pause` halts immediately. The in-flight command (if any) is allowed to finish cleanly but no new card renders until the user resumes.

## Anti-Frankenstein reminders specific to mode 2

- **Do not batch items with mixed `user_action_required` values** — a batched card must be homogeneous.
- **Do not auto-expand a `no` into a retry loop** — one ask per card, the user's decision stands.
- **Do not display the batched form by default if any item in the batch is a paste-back** — paste-backs are always per-item.
