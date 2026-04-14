<!-- SPDX-License-Identifier: MIT -->
---
name: Phase -1.2 consent card
description: Template that collects the user's mode choice (detailed / semi-auto / auto) and a per-item yes/no for every missing item in the gap report. Phase -1 cannot proceed past Phase -1.2 without explicit consent.
type: template
stage: -1.2
---

# Phase -1.2 — Consent card

Rendered right after the gap report. Collects two things in a single prompt:

1. **Mode choice** — the 3-mode ladder from the spec (detailed / semi-auto / auto).
2. **Per-item opt-in** — yes / no on each missing core item, plus explicit opt-in on any optional bonus the user already signalled interest in.

Phase -1.3 does not start until both are answered.

## The 3-mode ladder — recap

| Mode | User does | Claude does | Time | Best for |
|---|---|---|---|---|
| **1 — Detailed pas-à-pas** | Types each command themselves, reads output | Explains the concept before each step, validates output, explains errors | 30–45 min | First-time devs, learning-oriented users |
| **2 — Semi-auto** | Approves each proposed command card | Proposes each command, runs on confirm, shows output summary | 10–15 min | Devs who want control but not typing |
| **3 — Auto (the magical mode)** | Interrupts only at the security floor | Runs the full install pass, pauses only for sign-ins / admin pwds / extension grants | ~5 min | Experienced devs, repeat bootstraps |

All three modes honour the keyword `pause` per Layer 0 — the user can stop any mode mid-step with that one word.

Mode 3 is **never silent failure**. If it hits an admin password, a sign-in, an extension grant, a 2FA code, or a device authorization flow, it graceful-pauses, shows a paste-back micro-card, and resumes autonomous mode after the user unblocks.

## Consent card template

```
===== Phase -1.2 — Consent =====

Step 1 of 2 — Mode choice
  [ ] 1  Detailed pas-à-pas   (~{{EST_DETAILED}} min, you type each command)
  [ ] 2  Semi-auto            (~{{EST_SEMI_AUTO}} min, you confirm each command)
  [ ] 3  Auto                 (~{{EST_AUTO}} min, pauses only at sign-ins)

Step 2 of 2 — Per-item opt-in (missing core items only)

  Layer 3 — Dev essentials
    [ ] Node.js LTS      ({{NODE_CMD}})            cost: 1 min, admin pwd
    [ ] Git              ({{GIT_CMD}})             cost: 1 min, admin pwd
    [ ] VS Code          ({{CODE_CMD}})            cost: 2 min, admin pwd
    [ ] Chrome           ({{CHROME_CMD}})          cost: 1 min, admin pwd
    [ ] GitHub CLI       ({{GH_CLI_CMD}})          cost: 1 min, admin pwd

  Layer 4 — Automation surface
    [ ] Claude Code VS Code extension              cost: 30 s, needs restart
    [ ] Playwright MCP                             cost: 30 s, needs restart
    [ ] Claude in Chrome extension                 cost: 2 min, paste-back + grant

  Layer 4 — Multi-device (core)
    [ ] Claude mobile app (phone install + sign-in)
    [ ] Claude Code Remote Control pairing   ({{RC_GATE_NOTE}})

Reply with one line, e.g.  "mode 3, all yes"
Or pick per item, e.g.     "mode 2, skip chrome and cic, all else yes"
Or abort entirely:         "skip phase -1"

Per Layer 0: any item you skip here falls back to paste-back at Phase 5.5
and the rest of the pre-flight proceeds without blocking.

===================================
```

## Default selections

The card renders with every missing core item **unchecked**. The user opts in explicitly. No checkbox ships ticked by default — anti-Frankenstein discipline applies to dependency installs too.

## Parsing the user's response

Claude parses the user's reply for three facts:

1. **Mode number** — 1, 2, or 3. If absent, default to mode 2 (semi-auto) and confirm once more.
2. **Per-item decisions** — scan for item names in the reply. Unmatched items default to **skip** (fall back to paste-back later). Ambiguous replies trigger a single clarifying question.
3. **Abort signal** — `skip phase -1` / `abort` / `cancel` → skill ends cleanly, writes `memory/reference/automation-stack.md` with all items marked `user_skipped`, and hands control back to Genesis protocol.

## Subscription-aware branching

Before rendering the consent card, the skill checks `PLAN_TIER` from the gap report:

- **`free`**: do not render this card at all. Phase -1 already blocked at Phase -1.1 with the "Claude Code requires a paid plan" error.
- **`pro` / `team`**: Remote Control row renders as `[skipped — requires Max]`; the Codespaces fallback line surfaces in Phase -1.7.
- **`max`** or higher: Remote Control row renders as an opt-in checkbox like any other core item.
- **`unknown`**: render the card with Remote Control marked `[ ? ]` and append a note — *"If your plan is Max, tick this; otherwise skip and I'll offer Codespaces in Phase -1.7."*

## Recording consent

After parsing the reply, write to `memory/reference/consent-log.md`:

```markdown
---
phase: -1.2
recorded_at: YYYY-MM-DD HH:MM
mode: 1 | 2 | 3 | aborted
---

## Per-item decisions
- node.js_lts: yes
- git: yes
- vs_code: yes
- chrome: skip
- ...

## User's verbatim reply
> (quoted)
```

This file is read by Phase 5.5 to branch on fallback paths, and by the session post-processor skill for audit.

## Anti-Frankenstein reminders

- **Do not auto-select items the user did not explicitly approve.** Silence is not consent.
- **Do not prompt more than once.** If the user's reply is ambiguous, ask one clarifying question — not a multi-round interrogation.
- **Do not render this card if Phase -1.1 already blocked** on plan tier or OS.
- **Do not proceed to Phase -1.3 if mode is `aborted`** — exit cleanly via the fallback declaration path.
