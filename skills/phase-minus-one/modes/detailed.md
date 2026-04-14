<!-- SPDX-License-Identifier: MIT -->
---
name: Phase -1.3 mode 1 — detailed pas-à-pas
description: Runner prompt for the detailed mode. User types each command themselves while Claude explains the concept before every step, validates output, and teaches.
type: mode_runner
mode: 1
stage: -1.3
---

# Phase -1.3 — Mode 1 (detailed pas-à-pas)

Runs after the user picked mode 1 in the consent card. Purpose: learning. The user types every command; Claude explains and teaches.

**Time budget**: 30–45 minutes for a typical missing stack.

**Target audience**: first-time devs, learning-oriented users, and anyone who wants to actually understand the stack rather than have it installed silently.

## Flow

For each approved item in `memory/reference/consent-log.md`, in the strict dependency order from `install-manifest.yaml` (Layer 2 → 3 → 4):

1. **Announce the step** — one sentence: *"Next: {{LABEL}}. This is {{LAYER_ROLE}}."*
2. **Explain the concept** — 2–4 sentences about why the item is in Phase -1 and what it unlocks. Pull the rationale straight from the manifest's `rationale` field; expand it slightly.
3. **Show the command** — copy-pasteable, one line, no heredocs, inside a code block. Reference the exact command from the manifest for this OS.
4. **Wait for the user** to type / paste the command into a terminal they control.
5. **Ask them to share the output** — short prompt: *"Paste the output here so I can check it."*
6. **Validate** — parse the output, match it against the item's `probe_key` expected value (present / version match). On success: *"Good. {{KEY}} is ready."* On failure: explain the error in plain language, propose one fix, loop.
7. **Move to the next item.**

The user never feels rushed. Claude answers questions in-line. If the user asks *"why not use X instead?"*, Claude answers with the trade-off and, if warranted, offers to switch — but stays within the documented manifest.

## Security-floor stops

When the next item has `user_action_required == admin_password`:

- Before showing the command, warn: *"This step will trigger a UAC / sudo prompt. Type your admin password when asked."*
- After the command runs, ask the user to confirm: *"Did the elevation prompt appear and did you type the password?"*
- If yes, proceed. If no, propose running the same command again from an elevated terminal.

When the next item has `user_action_required == sign_in`:

- Do NOT try to sign in inside mode 1. Mark the item as "sign-in deferred" and continue with the next item.
- Every sign-in deferred in mode 1 accumulates into the Phase -1.4 batched sign-in round — the user does them all at once in Chrome at the end, not one at a time.

When the next item has `user_action_required == extension_grant`:

- Render a paste-back micro-card with the Chrome Web Store URL from the manifest.
- Wait for the user to confirm the extension is installed and pinned.
- Ask the user to sign in inside the extension only if mode 1 is also running extension-specific sign-in.
- Record the item as installed on confirmation. If confirmation never comes, mark it as "fell back to paste-back" and continue.

When the next item has `user_action_required == pairing`:

- Walk through the pairing ceremony from the Remote Control docs (phone app → paired-device screen → scan or accept).
- Verify with a simple ping: *"Send any keyboard tap from your phone and I'll confirm I see it."*
- Record the mobile device's OS in `memory/reference/mobile-companion.md`.

## Teaching mode — content guidance

The explanation for each step aims for three beats:

- **What** — plain-language description of the tool.
- **Why now** — how this item is a dependency for the next.
- **What comes next** — one-sentence teaser of the next step, so the user can see the staircase.

Keep beats to 1–2 sentences each. The goal is a user who could re-install this stack on a different machine tomorrow, not a reader of a documentation site.

## On failures

- **Command not found** — the package manager is missing or not on PATH. Refer the user to Phase -1.0 baseline for `PKG_MANAGER` and propose the one-line install of the package manager itself.
- **Network / firewall errors** — mark the item as "install-deferred", continue with the next item, and add a note to `memory/reference/automation-stack.md` explaining the block.
- **Permission denied** — re-run with sudo / elevated terminal; if still blocked, fall back to paste-back.
- **Everything else** — show the error verbatim, ask the user what they want to try, honour their decision.

## Completion

Once every item in the consent log is either `installed` or `deferred`, mode 1 ends. Control passes to Phase -1.4 (sign-in round) with the accumulated list of deferred sign-ins.

## Pause handling

If the user types `pause` at any point, stop immediately. Write a partial state to `memory/reference/automation-stack.md` so the next session can resume where we stopped. Phase -1 can be re-entered safely on the next session.

## Anti-Frankenstein reminders specific to mode 1

- **Do not auto-run the command for the user**, even if they ask *"can you just do it?"* — that defeats the mode's purpose. If the user wants auto, offer to switch to mode 3 mid-flow.
- **Do not teach topics outside Phase -1.** If the user asks a deep question about npm registries or SSH internals, answer briefly and offer a follow-up session. Phase -1 is not the tutorial.
