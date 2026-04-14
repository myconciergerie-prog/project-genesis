<!-- SPDX-License-Identifier: MIT -->
---
name: Phase -1 Dependencies Pre-flight — Genesis v2 roadmap
description: Before Phase 0 sanity check, Genesis v2 should request explicit user consent to install Windows/browser/desktop automation MCPs so that Phase 5.5 Auth Pre-flight can be fully automated instead of relying on the paste-back pattern
type: spec
target_version: v2
created_at: 2026-04-14
originSessionId: project-genesis v1 bootstrap
status: proposed
---

# Phase -1 — Dependencies Pre-flight (Genesis v2)

## Problem observed during v1 self-bootstrap

During the Project Genesis v1 bootstrap session on 2026-04-14, Phase 5.5 Auth Pre-flight required the user to:
- Paste the public SSH key into the GitHub web UI manually
- Create a fine-grained PAT by clicking through the GitHub settings form
- Create an empty repo via the GitHub web UI because fine-grained PATs cannot create user repos via API
- Paste the PAT back into Claude

This paste-back pattern is functional but adds ~5 minutes of user friction per bootstrap and breaks the "act directly via CLI / MCP" ideal from `~/.claude/CLAUDE.md`. The user correctly identified during the session that a **browser automation MCP** would allow Claude to handle all of these steps directly — eliminating the paste-back pattern entirely.

## Root cause — missing MCP dependencies

Claude Code can automate browser and desktop actions **if the right MCPs are installed**. The ecosystem has matured:

- **Playwright MCP** — full browser control via Microsoft's Playwright driver (headless or headed, Chromium / Firefox / WebKit)
- **Stagehand MCP** — higher-level natural-language browser automation built on top of Playwright by Browserbase
- **Windows UI automation MCPs** — control native Windows apps via UI Automation / pywinauto
- **Chrome DevTools Protocol MCP** — direct CDP access for fine-grained Chrome control

None of these are installed by default. Requesting the user to install them **mid-session** is disruptive. Requesting them **up-front, before Phase 0**, with a clear explanation of what each enables, aligns with the user's expectations and the "no new windows" rule (automation runs via CDP against the already-open Chrome profile, no new window spawned).

## Proposed Phase -1 — run before Phase 0

```
☐ Phase -1.1  Scan installed MCPs via claude mcp list
☐ Phase -1.2  Identify missing automation MCPs for this machine's OS
              - Windows: Playwright MCP + Windows UI automation MCP
              - macOS:   Playwright MCP + AppleScript MCP
              - Linux:   Playwright MCP + xdotool MCP
☐ Phase -1.3  Present a consent card listing each missing MCP with:
              - What it enables (concrete actions, e.g. "auto-add SSH key to GitHub")
              - How it installs (exact claude mcp add command)
              - Security implications (read-only vs read-write, what scopes)
              - Opt-in per MCP, not bulk
☐ Phase -1.4  For each MCP the user approves:
              - Run claude mcp add <server-spec>
              - Verify installation via claude mcp list | grep <name>
              - If installation requires session restart, document and prompt
☐ Phase -1.5  Record approvals in memory/reference/mcp-automation-stack.md
              so future sessions know which automation surface is available
☐ Phase -1.6  Phase 0 sanity check proceeds with awareness of which automation
              MCPs are available — Phase 5.5 branches on this
```

## Branch logic in Phase 5.5

```
IF Playwright/Stagehand MCP available:
  Phase 5.5 fully automated — Claude drives Chrome Profile 2 in headed mode,
  navigates to github.com/settings/ssh/new, pastes the pub key, submits form,
  waits for 200 OK, moves to PAT creation, submits, captures token from DOM,
  stores in .env.local, creates empty repo via the same automation path.
  Zero user interaction beyond final consent.

ELSE:
  Phase 5.5 falls back to paste-back pattern (current Genesis v1 behavior):
  Claude gives URLs + form contents to the user, user acts in their already-
  open Chrome window, pastes results back to Claude.
```

## Consent card design principles

- **Per-MCP opt-in** — no bulk accept. Each MCP's scope is different.
- **Explain the automation surface**, not the technology. "This lets me fill GitHub forms for you" not "Playwright is a Microsoft testing framework".
- **Show the equivalent paste-back cost** so the user can judge whether the automation is worth the install. "Without this MCP: 5 paste-back exchanges. With this MCP: 1 consent click."
- **Hard reject signal**: if the user says no to a specific automation MCP, **never ask again** for the same MCP in any future session on this machine. Record in Layer 0 as an opt-out.
- **Never install without explicit yes** — inherits the additive-auth spirit: automation surface is additive, opt-in, reversible.

## Failure modes to handle

- **MCP install fails** → log, fall back to paste-back, offer to retry post-session
- **MCP installed but session needs restart** → explain, ask user to `/reload`, resume from Phase 0 with automation available
- **Automation works for SSH key add but fails for PAT creation** (e.g. GitHub changes their form) → graceful degradation, paste-back for the failing step only
- **Chrome profile not open** → per the no-new-windows rule, automation MCPs should drive via CDP on the existing Chrome instance only; if it's not running, ask the user to open Chrome Profile 2 first (paste-back retry)

## Trade-offs

- **Pro**: near-zero friction bootstrap, matches the "act directly" ideal
- **Pro**: consistent automation surface across all future projects bootstrapped via Genesis
- **Pro**: machine-level one-time install pays off across dozens of project bootstraps
- **Con**: new attack surface — browser automation MCPs can read/write any web page, not just GitHub. Mitigated by per-MCP consent + per-action review mode during sensitive ops.
- **Con**: install friction at first run pushes the first bootstrap to ~10 min pre-flight instead of 2 min paste-back — inverted learning curve. Mitigated by making the consent card pre-approve future installs.

## Why this is not a v1 feature

Anti-Frankenstein gate:
- Adding Phase -1 to v1 would require implementing MCP install automation, consent UX, and the branch logic in Phase 5.5 — a 2-3 session effort at minimum
- v1 self-bootstrap is a single-user test, and the paste-back cost is ~5 min one-time — acceptable
- v1 must ship first with a working plugin form factor, then v2 iterates on ergonomics
- Starting v1 with Phase -1 would delay Genesis availability and risk scope creep

**Decision**: v1 ships with manual paste-back Phase 5.5. v2 introduces Phase -1 Dependencies Pre-flight and fully-automated Phase 5.5. Target timing: after Genesis v1 has been used to bootstrap **at least one** external project (aurum-v1 re-bootstrap) so we have a second data point on the paste-back cost before investing in automation.

## Input signal from user 2026-04-14

> "Il faudrait prioritiser l'acceptation du user d'installer toutes les dépendances qui te permettraient et qui permettraient à genesis d'accéder à chrome et au powershell. à penser maintenant pour la v2 de genesis"

Captured verbatim here so v2 can cite the origin of the requirement.
