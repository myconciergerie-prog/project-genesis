<!-- SPDX-License-Identifier: MIT -->
---
name: Phase -1.4 sign-in round
description: Batched sign-in checklist rendered once, after Phase -1.3. Accumulates every sign-in deferred during the install pass, plus the multi-device mobile pairing. User does all sign-ins back-to-back in one Chrome + phone sitting; no context-switching back to the terminal between them.
type: template
stage: -1.4
---

# Phase -1.4 — Sign-in round (consolidated)

Rendered once, after the Phase -1.3 install pass finishes, and only if there is at least one deferred sign-in. All the sign-ins that mode 1 / 2 / 3 deferred accumulate into this single card so the user sits down in Chrome (plus phone) once and does them all back-to-back.

## Why batch sign-ins

Context-switching between a terminal and a browser is the slowest part of a first-user bootstrap. Doing five sign-ins in the same browser session, with the user's attention already loaded into "Chrome mode", takes roughly a quarter of the time of doing them one at a time interleaved with install commands.

The spec (layer 1 refinement) makes this explicit: Phase -1.4 is the **consolidated** sign-in round. Installs run first (Phase -1.3), sign-ins batch second (Phase -1.4), restarts batch third (Phase -1.5).

## Template

```
===== Phase -1.4 — Sign-in round =====

You have {{COUNT}} sign-ins to complete. Do them back-to-back in one
Chrome sitting (and one phone sitting for the last two). Come back here
and reply "done" when all {{COUNT}} are ticked.

Chrome sign-ins
  [ ] {{SIGN_IN_1}}       →  {{URL_1}}
  [ ] {{SIGN_IN_2}}       →  {{URL_2}}
  [ ] {{SIGN_IN_3}}       →  {{URL_3}}
  ...

Phone sign-ins (if multi-device core is enabled)
  [ ] Claude mobile app   →  install from your OS app store, sign in with
                             the same Anthropic account as the Chrome step
  [ ] Remote Control      →  open Claude mobile app > Settings > Paired devices
                             > accept pairing prompt from this desktop session
                             (Claude Max plan only — Pro users skip)

Reply "done" when all sign-ins are complete.
Reply "some done" with a list of which ones you finished, if partial.
Reply "skip <item>" to fall back to paste-back at Phase 5.5 for that item.

====================================
```

## Accumulation rules

Phase -1.3 reaches Phase -1.4 carrying a list of deferred sign-ins. Deferral happens when:

- A mode 1 / 2 / 3 step's `user_action_required == sign_in` was encountered and deferred for batching.
- An extension install in any mode requires signing in inside the extension (Claude in Chrome → Anthropic account).
- The user's plan tier could not be detected earlier because no Claude sign-in existed — in that case, the Claude web sign-in is the first item of the batch.
- Project-specific services known ahead of time to be used in Phase 5.5 (e.g. GitHub, Supabase, Vercel) are listed here as well, so sign-ins for Phase 5.5 don't reopen the browser a second time.

If the list is empty (repeat user, everything already signed in), Phase -1.4 is skipped entirely and the flow jumps to Phase -1.5.

## URL sourcing

Each sign-in URL comes from one of three places, in priority:

1. The `install-manifest.yaml` item that deferred the sign-in (if it carries a `PASTE_BACK_URL`).
2. `memory/reference/github_genesis_account.md` (for GitHub) or equivalent reference memory for the service.
3. The service's canonical sign-in URL, hard-coded in a short allowlist in the skill (`https://claude.ai/login`, `https://github.com/login`, etc.).

The skill never generates a sign-in URL from scratch — all URLs are either sourced from memory or from the allowlist.

## Ordering inside the batch

Fixed order, chosen so dependencies resolve as the batch progresses:

1. Claude web sign-in (`https://claude.ai/login`) — first, because plan-tier detection downstream depends on it.
2. GitHub web sign-in (`https://github.com/login`) — used for the SSH key add, the PAT creation, and the empty repo creation in Phase 5.5.
3. Any project-specific service sign-ins, in alphabetical order (deterministic for reproducibility).
4. Claude in Chrome extension → Anthropic sign-in (inside the extension popup).
5. Claude mobile app → Anthropic sign-in (on the user's phone).
6. Claude Code Remote Control → pairing ceremony (on the user's phone, after the mobile sign-in).

## Parsing the user's reply

Claude parses the user's reply for three cases:

- **`done`** — mark every item as complete, move to Phase -1.5.
- **`some done, rest skipped`** — ask for a one-line per-item breakdown, then update each item's status.
- **`skip <item>`** — mark that one as `user_skipped`, leave the rest unaddressed and re-render a smaller card for the remainder.

If the user never replies (`pause`), halt — the sign-in round can resume in the next session by re-rendering this card.

## Recording completions

For each completed sign-in, update `memory/reference/automation-stack.md`:

```markdown
## Sign-ins completed at Phase -1.4
- [x] claude_web            2026-04-15 14:22
- [x] github_web            2026-04-15 14:23
- [x] claude_in_chrome      2026-04-15 14:24
- [x] claude_mobile_app     2026-04-15 14:26
- [x] claude_remote_control 2026-04-15 14:27
- [ ] supabase_web          skipped — fall back to Phase 5.5
```

## Anti-Frankenstein reminders

- **Never render a second card mid-batch.** One card, the user does everything, one reply.
- **Never split the phone-side items into a second separate card.** The user sits down with their phone once; two cards break the flow.
- **Never add sign-ins that were not already deferred or pre-declared.** Phase -1.4 is a consolidator, not a new surface.
- **If the count is zero, do not render the card.** Silent skip to Phase -1.5.
