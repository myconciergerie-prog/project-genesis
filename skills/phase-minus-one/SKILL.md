---
name: phase-minus-one
description: Dependencies Pre-flight for first-time Genesis users — detect the current dev stack, show a gap report, let the user pick a mode (detailed / semi-auto / auto), run installs via the OS package manager, batch sign-ins and restarts, verify the stack, and offer optional multi-LLM / multi-device bonuses. Core Phase -1 of the Genesis 7-phase protocol.
---

# Phase -1 — Dependencies Pre-flight

This skill is the first thing Genesis runs on a fresh machine, after the user has manually installed the Claude Code CLI (Phase -2, external to Genesis) and invoked Claude Code in an empty project folder.

The skill walks the user from "Claude Code just started" to "the full Genesis stack is installed and verified, ready for Phase 0 of the Genesis protocol". It minimises manual intervention to the unavoidable security floor (admin passwords, sign-ins, browser extension permission grants, 2FA, device authorization).

Full design rationale: `.claude/docs/superpowers/specs/v1_phase_minus_one_first_user_bootstrap_flow.md` (three stratified layers — initial, 3-mode ladder refinement, multi-device refinement).

## When to invoke

- The user types `/phase-minus-one` (Claude Code auto-surfaces every skill as a slash command).
- The user says any of:
  - "run phase minus one"
  - "lance la pre-flight"
  - "genesis phase -1"
  - "install the genesis stack"
  - "bootstrap my dev machine"
- The Genesis protocol orchestrator invokes this skill as Phase -1 before Phase 0.
- At session open, if `memory/reference/automation-stack.md` does not exist, the skill surfaces itself as a one-line suggestion: *"Run `/phase-minus-one` first to set up the dev stack"*.

**Do not auto-run without user consent.** Phase -1 touches the user's machine — it always asks first.

## The flow — seven numbered phases

Phase -1 is a decision tree with seven numbered phases. The skill runs each phase in order; every phase has an exit condition.

| # | Phase | Purpose | User intervention |
|---|---|---|---|
| -1.0 | Baseline detection | Silent read-only probe of what is already installed | None |
| -1.1 | Gap report card | Present the diff between current state and target stack | Read the card |
| -1.2 | Mode choice + consent | User picks detailed / semi-auto / auto and approves per-item | One prompt |
| -1.3 | Install pass | Run installs per mode, pause only at the security floor | Admin password if triggered |
| -1.4 | Sign-in round | Batched checklist: all required sign-ins in one Chrome sitting | Sign in to each service |
| -1.5 | Restart round | Batched restart prompt: Chrome + Claude Code session together | Restart when ready |
| -1.6 | Verification pass | Silent health check of the installed stack | None |
| -1.7 | Optional bonus offer | Antigravity / Codespaces / Termux / voice mode, opt-in only | Optional sign-up |

Phase -1.8 is implicit: the skill writes `memory/reference/automation-stack.md`, declares any gaps that fell back to paste-back, and hands control back to the Genesis protocol.

## Files in this skill

- `SKILL.md` — this file; entry point and flow overview.
- `detect.sh` — the Phase -1.0 baseline probe. Cross-platform shell, read-only, <5 s.
- `install-manifest.yaml` — the target stack as a per-OS install command map. Consumed by Phase -1.3 to drive installs.
- `gap-report.md` — template rendered at Phase -1.1 to show the current-vs-target diff.
- `consent-card.md` — template rendered at Phase -1.2 to collect the mode choice and per-item opt-ins.
- `modes/detailed.md` — the Phase -1.3 runner for mode 1 (detailed pas-à-pas, ~30–45 min).
- `modes/semi-auto.md` — the Phase -1.3 runner for mode 2 (semi-auto, confirm each command, ~10–15 min).
- `modes/auto.md` — the Phase -1.3 runner for mode 3 (auto, pauses only at the security floor, ~5 min).
- `sign-in-round.md` — the Phase -1.4 batched sign-in checklist template, now including mobile companion pairing for multi-device core.
- `restart-round.md` — the Phase -1.5 batched restart prompt template.
- `verification.md` — the Phase -1.6 final health check card template.
- `optional-bonus.md` — the Phase -1.7 offer for Antigravity / Codespaces / Termux / voice mode.

## How the skill uses these files

1. Read `install-manifest.yaml` to know the target stack.
2. Run `detect.sh` and parse its output into a dict `{item: present|missing|unknown}`.
3. Render `gap-report.md` with the detected state — present it to the user.
4. Render `consent-card.md` — collect mode choice + per-item yes/no.
5. Branch into `modes/<mode>.md` — that file drives Phase -1.3 end-to-end, consuming `install-manifest.yaml` for the commands and falling back on the security-floor rules when it hits a blocking step.
6. Render `sign-in-round.md` once per run, containing every required sign-in surfaced during Phase -1.3. User confirms the whole batch.
7. Render `restart-round.md` once per run with all pending restarts batched.
8. Re-run `detect.sh` for Phase -1.6 verification, render `verification.md` with the result.
9. Offer `optional-bonus.md`. The user can accept any subset or skip entirely.
10. Write `memory/reference/automation-stack.md` and return.

## Mode choice — the 3-mode ladder

The user picks one of three modes after reading the gap report. The trade-off is discovery vs speed vs hands-off.

| Mode | User types | Claude does | Time | For |
|---|---|---|---|---|
| **1 — Detailed pas-à-pas** | Each command themselves | Explains before every step, validates output, teaches | 30–45 min | First-time devs, learning-oriented users |
| **2 — Semi-auto** | `yes` / `no` on each confirmable command card | Proposes each command, runs on confirm, shows output | 10–15 min | Devs who want control but not typing |
| **3 — Auto** | Nothing except sign-ins, admin passwords, extension grants | Runs the full install pass, pauses only at the security floor | ~5 min | Experienced devs, repeat bootstraps |

Mode 3 is **never silent failure** — it always graceful-pauses at the security floor, surfaces a paste-back micro-card, and resumes autonomous mode after the user unblocks.

Any mode can be interrupted with the keyword `pause` per the Layer 0 working-style rule.

## Security floor — what Phase -1 never automates

- Initial sign-in to a service (OAuth / magic link / username+password).
- Admin password prompts (Windows UAC, macOS/Linux sudo for system packages).
- Browser extension permission grants (Chrome / Edge permission dialog).
- 2FA codes (phone-based, authenticator app, hardware key).
- Device authorization flows (e.g. GitHub device code).

When the skill hits one of these, it stops, presents a paste-back micro-card, and waits for the user to confirm before continuing.

## Multi-device core — beta-tester reality

Per refinement layer 2 of the spec, Phase -1 treats multi-device support as **core, not optional bonus**. Phase -1.3 branches on the user's plan tier:

- **Claude Max (or higher)**: install Claude mobile app, walk through Claude Code Remote Control pairing, verify with a ping from phone to desktop, record the mobile device's OS in `memory/reference/mobile-companion.md`.
- **Claude Pro / Team**: install Claude mobile app for read-only access, mention Remote Control requires Max, fall back to GitHub Codespaces as the any-device alternative.
- **Claude Free**: block Phase -1.3 with a clear error — Claude Code requires a paid plan. Direct the user to Pro or Max signup.

The mobile pairing step appears in `sign-in-round.md` as one of the checklist items, so it batches with the other sign-ins.

## Fallback declaration

After Phase -1.6, the skill writes `memory/reference/automation-stack.md` recording what was installed, what was skipped, and what fell back to paste-back. Phase 5.5 reads this file and branches per item: automated path when available, paste-back path otherwise. There is no hard block — users can always proceed with partial automation.

## Anti-Frankenstein reminders

- **Do not add steps outside the spec.** If the spec does not cover it, it does not go in Phase -1.
- **Do not auto-run installs without consent.** Every install is either mode-3 auto-approved, mode-2 confirmed, or mode-1 user-typed. No silent installs.
- **Do not skip the security floor for speed.** Mode 3 pauses at every security-floor item, even if it would be "faster" to bypass.
- **Do not implement bonus items as mandatory.** Antigravity, Codespaces, Termux, voice mode stay opt-in.
- **If the user says `frankenstein`**, stop immediately and back out of the last proposal.

## Exit condition

Phase -1 is complete when:

- `memory/reference/automation-stack.md` exists and lists the installed stack.
- `detect.sh` re-run (Phase -1.6) confirms every approved item is healthy or recorded as fallback.
- The user has not said `pause`.
- Control is handed back to the Genesis protocol for Phase 0.
<!-- SPDX-License-Identifier: MIT -->
