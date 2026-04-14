<!-- SPDX-License-Identifier: MIT -->
---
name: Phase -1.7 optional advanced bonus offer
description: Final opt-in prompt after the core stack is verified. Offers the four Phase -1.7 bonuses (Antigravity, Codespaces fallback, Android Termux, voice mode) as individual yes/no items. Strictly opt-in — nothing here is installed without explicit consent.
type: template
stage: -1.7
---

# Phase -1.7 — Optional advanced bonus offer

Rendered only after Phase -1.6 has confirmed a healthy core stack, and only if the consent log flagged any of the four bonuses as "ask me in Phase -1.7". If the consent card skipped them all, Phase -1.7 is skipped entirely.

## The four optional bonuses

### 1. Google Antigravity

**What**: multi-model agent-first IDE from Google (released November 18, 2025), free for individuals. Runs Claude Sonnet 4.6, Claude Opus 4.6, Gemini 3.1 Pro, Gemini 3 Flash, and GPT-OSS 120B natively in one surface. Two interaction modes: Editor View (classic) and Manager Surface (multi-agent orchestration across workspaces).

**Why this user might want it**: the hybrid Antigravity + Claude Code pattern is documented and used by early-adopter devs in Q1 2026. Fits Genesis users who want multi-LLM routing at the IDE layer rather than only at the runtime layer.

**Install**: paste-back — the skill renders the download URL, the user installs the desktop app, signs in with any of their existing Google / Anthropic / OpenAI accounts, and replies `done`. No further configuration needed; the Antigravity install stands alone and does not interfere with Claude Code.

**Recorded in**: `memory/reference/automation-stack.md` under `Optional bonuses accepted in Phase -1.7`.

### 2. GitHub Codespaces fallback

**What**: any-device cloud dev environment via GitHub Codespaces. The skill walks the user through enabling Codespaces on their GitHub account and optionally creating a first Codespace pointing at the Genesis repo.

**Why this user might want it**: if their plan is Claude Pro (not Max), Claude Code Remote Control is not available, and Codespaces is the canonical any-device fallback — open a browser on any machine, spin up a Codespace, run `claude` inside it.

**Install**: paste-back, plus a brief walkthrough:

- Open `https://github.com/codespaces` → enable Codespaces on your account.
- Create a new Codespace pointing at the Genesis repo (or any empty template repo for first-time testing).
- Wait for the Codespace to boot (<2 min).
- Run `claude` inside the Codespace terminal to confirm Claude Code works.
- Optionally add Codespaces to the mobile browser's home screen for phone access.

**Recorded in**: `memory/reference/automation-stack.md`.

### 3. Android Termux local Claude Code

**What**: Termux is a terminal emulator on Android that runs a full Linux userland locally, without root. With Termux + Node.js + Claude Code CLI, the user can run Claude Code **directly on their Android phone**, fully offline-first.

**Why this user might want it**: power-user escape hatch for when they do not want a laptop nearby. The install is Android-specific and surprisingly smooth in Q2 2026 (Termux ships Node via the standard repo; Claude Code's Linux install path works unchanged).

**Install**: paste-back — the skill gives the user the F-Droid URL for Termux (NOT the Play Store version, which is deprecated), the `pkg install nodejs` command, and the Claude Code install one-liner. The user runs them on their phone; nothing on the desktop touches this path.

**Gate**: only offered if the user previously installed the Claude mobile app on Android (iOS users see this bonus as "not applicable on iOS" greyed out).

**Recorded in**: `memory/reference/automation-stack.md`.

### 4. Claude Code voice mode (`/voice`)

**What**: push-to-talk voice interaction with Claude Code. Still a gated rollout in Q1–Q2 2026 — some accounts have it, some don't, and availability depends on the CLI version and the account tier.

**Why this user might want it**: for ambient dev — drive Claude Code hands-free while reading code, walking, or doing something else. Not a primary surface, but a quality-of-life bonus for users who already know they want it.

**Install**: run `claude /voice` in the Claude Code session. If the command succeeds, voice mode is enabled. If it errors ("feature not available on this account"), the skill marks it as `not_available_for_this_account` and moves on without drama.

**Recorded in**: `memory/reference/automation-stack.md`.

## The Phase -1.7 card

```
===== Phase -1.7 — Optional advanced bonuses =====

All four items are strictly opt-in. You can accept any subset or skip
everything and move directly to Phase 0.

  [ ] Google Antigravity
      Multi-LLM agent IDE, free for individuals, hybrids nicely with
      Claude Code. Install via paste-back.

  [ ] GitHub Codespaces fallback
      Any-device cloud dev environment. Recommended if your plan is
      Claude Pro (no Remote Control).

  [ ] Android Termux local Claude Code
      Run Claude Code directly on your phone (Android only).

  [ ] Claude Code voice mode (`/voice`)
      Gated rollout; may not be available on your account.

Reply "skip all" to move to Phase 0.
Reply with a numbered list to accept specific items (e.g. "1 and 2").

=================================================
```

## Parsing the user's reply

- **`skip all`** or **`none`** — no bonuses installed; Phase -1.7 ends immediately.
- **Numbered list** (`1, 3`) or **named list** (`antigravity and termux`) — Claude walks through each accepted item's install flow one at a time, in order, without re-prompting for approval (the Phase -1.7 card already captured consent).
- **Ambiguous / unparsable** — ask one clarifying question with the four items renumbered.

## Special cases

- **If Antigravity was accepted**: after the install, optionally ask if the user wants a short walkthrough of the Manager Surface. This is a nice-to-have, not required — the skill only runs it on explicit yes.
- **If Codespaces was accepted**: the skill suggests pinning the Codespaces URL to the user's browser bookmarks bar.
- **If Termux was accepted**: the skill warns about Play Store Termux being outdated and reinforces the F-Droid URL.
- **If voice mode errors**: the skill records the error and notes in the memory file that voice is not available. It does not retry.

## Recording everything

Every accepted bonus is appended to `memory/reference/automation-stack.md` under the `Optional bonuses accepted in Phase -1.7` section. Every declined bonus is silently omitted — we do not pollute the file with negatives.

## Anti-Frankenstein reminders

- **Nothing here is core.** All four bonuses are strictly opt-in. The consent card in Phase -1.2 must have flagged them individually; Phase -1.7 does not introduce new items the user never asked for.
- **Do not chain bonus installs automatically.** Each accepted item runs its own paste-back flow; do not try to run them in parallel or batch them.
- **Do not prompt for Phase -1.7 if the consent card said "skip all bonuses"** — the offer is extended only if the user expressed interest earlier.
- **Do not mark voice mode as a failure** when `claude /voice` errors with "not available". That is expected for most accounts and is recorded as `not_available_for_this_account`, not as an install error.
