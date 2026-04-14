<!-- SPDX-License-Identifier: MIT -->
---
name: Phase -1 — First-user bootstrap flow
description: Design thinking for the v1 template's Phase -1 Dependencies Pre-flight, answering the question "how does a user with nothing installed reach a fully automated Phase 5.5 with minimal manual intervention — ideally just logins?"
type: spec
target_version: v1
created_at: 2026-04-14
originSessionId: project-genesis v1 bootstrap
status: active
---

# Phase -1 — First-user bootstrap flow

## Problem statement

A user runs Genesis for the very first time on a fresh machine with no developer stack installed. They want the template to do as much of the setup as possible autonomously, intervening only where intervention is unavoidable by design (logins, admin passwords, app restarts).

The question is: **what is the minimum manual surface, and in what order?**

This is the design counterpart to the earlier Phase -1 Dependencies Pre-flight proposal (`v1_phase_minus_one_dependencies_automation.md`). That file describes *what* to install. This file describes *the order and the handoff* — how control moves from the user to Claude and what the user must still do after the handoff.

## Dependency chain — foundation first

There is a strict dependency ordering. Earlier items are prerequisites for later ones. Genesis cannot skip a layer.

```
  Layer 0 — Operating system
    │
    ▼
  Layer 1 — Package manager
    │  (winget on Windows, brew on macOS, apt/dnf/pacman on Linux)
    ▼
  Layer 2 — Claude Code CLI (the bootstrap pivot)
    │  (installed either via the OS package manager, npm, or Anthropic's standalone installer)
    ▼
  Layer 3 — Local dev essentials (Node, Git, VS Code, Chrome)
    │  (now installable autonomously because Claude Code has Bash)
    ▼
  Layer 4 — Automation surface (MCPs + IDE extensions + browser extensions)
    │  (Playwright MCP, Claude Code VS Code extension, Claude in Chrome)
    ▼
  Layer 5 — Project-specific services (GitHub, Supabase, Vercel, etc.)
    │  (logins — the only unavoidable manual surface after Layer 2)
    ▼
  Phase 0 of the Genesis protocol proper
```

**The pivot point is Layer 2**. Everything before Claude Code is running is manual. Everything after is Claude-driven with user interventions only at sign-in points.

## The handoff moment

Before Layer 2:
- User installs Claude Code CLI manually
- This is **Phase -2** (pre-Claude-Code, external to Genesis)
- Genesis cannot orchestrate this because Genesis doesn't exist yet in the user's world
- Anthropic's install docs cover this; Genesis links to them

At Layer 2:
- The user opens a terminal, runs `claude` in a fresh project folder, and invokes Genesis
- This is the first moment Genesis has control
- Claude Code now has Bash, WebSearch, WebFetch, and file tools
- **Everything else can be bootstrapped from here**

## What cannot be automated after Layer 2 — the security floor

Even once Claude Code is running, some interventions are unavoidable by design:

1. **Initial sign-in to a service** — OAuth, username + password, magic links. By security design, Claude cannot do this without the user being physically present at the browser for at least the first login.
2. **Admin passwords** — Windows UAC prompts, macOS sudo, Linux sudo for system-level package installs. User must type this.
3. **Browser extension permission grants** — when installing a Chrome extension, Chrome prompts the user to accept permissions. This is a browser-level security check that no tool can bypass.
4. **2FA codes** — phone-based, authenticator-app-based, hardware-key-based. User intervention by design.
5. **Device authorization flows** — e.g. GitHub device code flow, where the user pastes a code into a web page while already signed in.

Everything else **can** be automated. Phase -1 should aggressively minimize user interaction to these 5 categories only.

## What CAN be automated after Layer 2

With Bash + a package manager + Playwright MCP installed, Claude Code can autonomously:

- Install any CLI tool (`git`, `node`, `gh`, `direnv`, etc.) via the OS package manager
- Install Node.js runtime at the required version
- Install VS Code
- Install Chrome or Edge (the browser binary — extensions still need user)
- Install VS Code extensions via `code --install-extension <id>`
- Add MCP servers to `~/.claude.json` via `claude mcp add`
- Generate SSH keys, add entries to `~/.ssh/config`
- Create project folder structures, write files, run `git init`
- Install npm / pip / brew packages
- Start/stop/restart local services
- Run health checks against any local or remote endpoint
- Probe filesystems, registries, config files
- Drive browser forms via Playwright MCP (once that's installed) — GitHub PAT creation, SSH key add, repo creation, Supabase project create, etc.

The list is long. The constraint is almost entirely on **sign-ins**, not on capabilities.

## Phase -1 — refined decision tree

```
Phase -1.0  Baseline detection (silent, read-only, <5 s)
            Probe:
              - OS family + version
              - Package manager presence (winget/brew/apt/dnf/pacman)
              - Node.js version (>= 18 for Playwright MCP)
              - Git version
              - VS Code install + version
              - Chrome or Edge install
              - Claude in Chrome extension (via native messaging host config file)
              - Claude Code VS Code extension (via code --list-extensions)
              - Existing MCPs (claude mcp list)
              - Existing SSH keys (~/.ssh/)
              - Shell rc files and env var state
            Report: current state as a diff against the v1 target stack.

Phase -1.1  Gap report card
            Show the user a single card listing:
              - What is already present (✓)
              - What is missing (✗)
              - What is optional-but-recommended (◇)
              - For each missing item: what it enables, how it installs, time cost,
                what user action is required (none / admin pwd / sign-in / restart)

Phase -1.2  Consent — opt-in per layer, not bulk
            The user approves or skips each missing item individually. For any item
            flagged "needs admin password" or "needs sign-in", the user can choose
            to skip and fall back to paste-back at Phase 5.5 later.

Phase -1.3  Autonomous install pass
            For each approved item, Claude:
              - Runs the install command via Bash (package manager or direct)
              - Captures output to memory/reference/install-log.md
              - On failure: marks the item as "failed, will fall back at Phase 5.5",
                continues with the next approved item
              - Only pauses to prompt the user for:
                * Admin password
                * Sign-in
                * Restart an application (Chrome, Claude Code session)

Phase -1.4  Sign-in round — consolidated
            Present ALL required sign-ins together as a single ordered checklist,
            so the user does them back-to-back in one Chrome session instead of
            context-switching between Claude and browser multiple times:
              - Claude in Chrome → Anthropic account sign-in
              - GitHub web UI → account sign-in (if not already)
              - Any project-specific services that will be used in Phase 5.5
            Each line has the paste-back URL and a check-box for confirmation.

Phase -1.5  Restart round — consolidated
            Some installs need restarts (Chrome for native messaging host,
            Claude Code for new MCPs, rc file reload for new env vars).
            Present all restarts in one batch with a single "continue when ready"
            prompt, so the user reloads everything together.

Phase -1.6  Verification pass
            Silent:
              - claude mcp list → all approved MCPs healthy
              - code --list-extensions → Claude Code VS Code extension present
              - ssh -T github.com (generic check, no specific alias yet)
              - git --version, node --version, all other health checks
              - Chrome in Chrome extension check (if installed): tiny /chrome test ping
            Report the verified stack as a summary card. Ready for Phase 0.

Phase -1.7  Fallback declaration
            Any item that was skipped or failed is recorded in
            memory/reference/automation-stack.md with the reason. Phase 5.5 branches
            per item: automated path if available, paste-back path otherwise.
            No hard block: users can always proceed with partial automation.
```

## Package manager primacy — the multiplier

The single biggest autonomy-multiplier for Phase -1 is a working OS package manager. Once Claude has access to `winget`, `brew`, or `apt`, installing the bulk of the dev stack becomes a handful of Bash commands.

### Windows — winget (pre-installed in Windows 10/11 since 2020+)

```bash
winget install OpenJS.NodeJS.LTS
winget install Microsoft.VisualStudioCode
winget install Google.Chrome
winget install Git.Git
winget install GitHub.cli
```

Most of these work at user scope without admin. Some trigger UAC — Phase -1.3 detects that and routes the user to Phase -1.4 for the password prompt.

### macOS — brew (one-line install; common on dev machines)

```bash
brew install node visual-studio-code google-chrome git gh
```

### Linux — distro-specific, usually pre-installed

```bash
# Debian/Ubuntu
sudo apt install nodejs npm code google-chrome-stable git gh

# Fedora/RHEL
sudo dnf install nodejs npm code google-chrome-stable git gh
```

### What if no package manager is available

- **Windows 10/11**: winget is pre-installed, this is a non-case.
- **Older Windows (<10)**: not a supported target.
- **Linux without a package manager**: statistically negligible, fall back to manual.
- **macOS without brew**: Claude can install brew via one shell command (`/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`) — it's the canonical bootstrap of brew itself and is documented as safe.

In every OS case, a package manager exists or can be installed with one Claude-runnable command. Phase -1.0's baseline check confirms this.

## The user's actual manual surface — ideal target

After Phase -1, the user should have been asked for only:

1. **One-time Claude Code CLI install** (Phase -2, before Genesis even runs — unavoidable)
2. **One or two admin passwords** if system-level packages need them
3. **A consolidated sign-in session** in Phase -1.4 — all logins back-to-back in one Chrome sitting, no jumps back to the terminal
4. **A single restart** of Chrome and/or Claude Code session in Phase -1.5
5. **Sign-ins for project-specific services** at Phase 5.5 (but these are minimized by Phase -1.4 doing them ahead when possible)

That's it. **Four or five human interactions total** for a fresh-machine bootstrap. Everything else is Claude autonomous.

## Current session (2026-04-14) as a data point

This very session was run by a user who already had:
- Windows 11 Pro
- Node.js 24
- Git
- VS Code 1.115.0 + Claude Code extension already installed and linked
- Chrome with Profile 2 signed into myconciergerie@gmail.com
- SSH client (git-bash)
- Claude Max 20x subscription active
- 9 MCPs already configured in `~/.claude.json`

Missing items discovered during the session:
- Playwright MCP → installed during session via `claude mcp add`
- Claude in Chrome extension → installed by user via paste-back during session
- Dedicated Genesis SSH key → generated during session
- GitHub PAT for project-genesis → created by user via paste-back during session
- Empty `myconciergerie-prog/project-genesis` repo → created by user via paste-back during session

Total user paste-back actions: **~8** (extension install + pin + sign-in + PAT creation + PAT paste + SSH key URL + repo create + description fix pending).

Under the v1 Phase -1 design proposed above, for a **second-time** user who has run Phase -1 once on this machine, the paste-back count drops to **~2** (one-time GitHub form fills for the new repo's PAT and the new repo creation — because fine-grained PATs are per-project by nature).

Under an **ideal fully-automated Phase -1** (Playwright MCP + Claude in Chrome both active from first run), the paste-back count drops to **0** for repeat users: Claude in Chrome navigates to GitHub's already-authenticated session and creates the PAT and repo via form automation, then pastes the PAT into `.env.local` itself.

This is the target. This is what Genesis v1 Phase -1 makes possible.

## Chicken-and-egg considerations

There is a subtle chicken-and-egg problem: Phase -1 needs to install Playwright MCP to automate things, but installing Playwright MCP requires Node.js, which Phase -1 might also need to install. Order matters.

Phase -1 resolves this by running installs in the strict dependency order (Layer 3 before Layer 4 in the hierarchy above). Node.js installs first, then Playwright MCP, then Claude Code VS Code extension, then Claude in Chrome. Each layer's health check gates the next.

## What Genesis v1 ships

- A `skills/phase-minus-one/` skill containing the decision-tree logic, detection probes, consent card generation, install runners, and the gap report card
- A `templates/phase-minus-one-install-manifest.yaml` file listing the target stack with install commands per OS
- A `hooks/` entry for detecting first-run vs repeat-run state (has the user been through Phase -1 on this machine before)
- Documentation in `README.md` (bilingual FR + EN) explaining the first-user flow, the handoff moment, and the minimum manual surface
- Memory template `memory/reference/automation-stack.md` that records what's installed on the machine for future sessions to read

## What Genesis v1 does NOT ship

- Auto-install of the Claude Code CLI itself (Layer 2) — Genesis runs after Claude Code is already running, so it can't install itself
- Auto-install of browser extensions (permission flow is unavoidable)
- Auto-sign-in to any service (security floor)
- A wizard UI (per anti-Frankenstein — use Claude Code's native prompt flow, not a custom UI layer)

## Self-rating of this spec (initial, 2026-04-14)

- Pain-driven coverage: 9/10 (addresses the exact question the user asked)
- Prose cleanliness: 7/10 (comprehensive but could be tighter)
- Best-at-date alignment: 9/10 (uses winget/brew/apt, Playwright MCP, Claude in Chrome, all 2026 canonical)
- Self-contained: 8/10 (references the related spec, otherwise stands alone)
- Anti-Frankenstein: 9/10 (zero speculative additions; every item pain-driven)
- Average: **8.4/10** — at the target inflection point for a v1 spec

---

## Refinement 2026-04-15 — the magical starting point + 3-mode ladder + Antigravity

After the initial spec above, the user refined the design on 2026-04-15 with three critical additions:

1. The **first-user mental model** must feel magical — one install, then Claude takes over
2. Phase -1 must offer a **3-mode ladder** (detailed / semi-auto / auto) so the user picks their level of involvement
3. The research must evaluate **Antigravity** and any other top-tier tool identified during research, not just VS Code

Fresh research on 2026-04-15 captured in `research/sota/claude-in-ide-tools_2026-04-15.md` surfaced two decisive findings that reshape this spec.

### The magical Phase -2 prerequisite — one PowerShell line

The user's only unavoidable manual action before Genesis can exist in their world is the Claude Code CLI install. On Windows, this collapses to a single line:

```powershell
irm https://claude.ai/install.ps1 | iex
```

No Node.js dependency, no PATH editing, auto-update in background, takes ~60 seconds. macOS and Linux have equivalent one-liners. This is the **magical starting point** — the user's mental model is "I paste one line into PowerShell, then Claude does everything else". Genesis `README.md` documents this line verbatim as Phase -2.

### The Claude Code VS Code extension doubles as an MCP server

Discovery during 2026-04-15 research: when the Claude Code VS Code extension activates, it runs a local MCP server named `ide` that the CLI auto-connects to. This gives:
- The CLI access to VS Code's native diff viewer (richer diff rendering than terminal)
- The CLI access to the user's current VS Code selection
- The CLI the ability to execute Jupyter cells with confirmation

**Consequence**: installing the VS Code extension is doubly valuable — IDE UX plus automatic MCP surface expansion. It promotes from "recommended" to "strongly recommended baseline" in Phase -1.

### Google Antigravity — optional advanced bonus

Released November 18, 2025 by Google. **Free for individuals.** Multi-model agent-first IDE that runs Claude Sonnet 4.6, Claude Opus 4.6, Gemini 3.1 Pro, Gemini 3 Flash, and GPT-OSS 120B natively in one surface. Two interaction modes: Editor View (classic) and Manager Surface (multi-agent orchestration across workspaces).

The hybrid Antigravity + Claude Code pattern is documented and used by early-adopter devs in Q1 2026. Fits Genesis users who want multi-LLM routing at the IDE layer rather than only at the runtime layer.

**Status in Phase -1**: optional advanced bonus, opt-in, not blocking. Installed only if the user explicitly says yes during the consent card.

### The 3-mode ladder

Phase -1.2 (consent) now offers the user a choice of **involvement level**, not just per-item opt-in. The three modes trade off discovery / speed / hands-off respectively:

| Mode | What the user does | What Claude does | Time cost | Best for |
|---|---|---|---|---|
| **1 — Detailed pas-à-pas** | Types each command themselves, reads the output, asks questions | Explains the concept before each step, validates output, explains errors | ~30–45 min | First-time devs, learning-oriented users, people who want to understand the stack |
| **2 — Semi-auto** | Clicks "go" on each proposed command card | Proposes each command in a confirmable card, runs on go, shows output summary | ~10–15 min | Developers who want control but not typing; review-first personalities |
| **3 — Auto (the magical mode)** | Interrupts only for sign-ins, admin passwords, and browser extension grants; otherwise just watches | Runs a master install orchestration, handles failures via retries or graceful fallback to paste-back, pauses only for the 5 categories of unavoidable manual interactions | ~5 min (dominated by downloads + login events) | Experienced devs, repeat bootstraps on known machines, users who want speed |

**Mode choice is a single prompt** presented after Phase -1.1's gap report card. The user picks once and Phase -1.3+ runs in the chosen mode. Any mode can be interrupted with the `pause` keyword (per Layer 0 working style).

**Fallback behavior**: Mode 3 detects conditions where autonomy is not possible (admin password needed, sign-in needed, extension permission needed) and **pauses gracefully**, presents a paste-back micro-card for the blocking step, then resumes autonomous mode after the user unblocks. Mode 3 is **never a silent failure** — it is always "auto with pauses at the security floor".

### Updated Phase -1 decision tree

```
Phase -1.0  Baseline detection (silent, read-only)
Phase -1.1  Gap report card
Phase -1.2  Mode choice (detailed / semi-auto / auto) + per-item consent
Phase -1.3  Autonomous or semi-auto install pass (per mode)
Phase -1.4  Sign-in round (consolidated, user-driven by security floor)
Phase -1.5  Restart round (consolidated)
Phase -1.6  Verification pass
Phase -1.7  Optional advanced bonus offer (Antigravity) — opt-in only
Phase -1.8  Fallback declaration + ready for Phase 0
```

### Updated target stack for Phase -1

| Layer | Tool | Status | Install method |
|---|---|---|---|
| 2 (pivot) | Claude Code CLI | **Phase -2 prerequisite** — user runs the one-liner | `irm https://claude.ai/install.ps1 \| iex` |
| 3 | Node.js LTS | Auto-install if missing | `winget install OpenJS.NodeJS.LTS` |
| 3 | Git | Auto-install if missing | `winget install Git.Git` |
| 3 | VS Code | Auto-install if missing (strongly recommended) | `winget install Microsoft.VisualStudioCode` |
| 3 | Chrome | Auto-install if missing (for Claude in Chrome) | `winget install Google.Chrome` |
| 4 | Claude Code VS Code extension | Auto-install via `code --install-extension anthropic.claude-code` — doubles as `ide` MCP server | CLI command |
| 4 | Playwright MCP | Auto-install via `claude mcp add --scope user playwright npx @playwright/mcp@latest` | CLI command |
| 4 | Claude in Chrome extension | Paste-back install (browser permission floor) | Chrome Web Store URL |
| 4 (optional) | Google Antigravity | Opt-in bonus, paste-back install | Antigravity installer URL, Phase -1.7 |
| 5 | Project-specific services (GitHub, etc.) | Sign-ins in Phase -1.4 or Phase 5.5 | Per-service |

### Impact on Genesis v1 deliverables

The v1 template must ship with:
- `skills/phase-minus-one/` containing the decision tree + the three mode runners + the gap probes + the consent card generator + the optional-bonus offer
- `templates/phase-minus-one-install-manifest.yaml` listing the target stack per OS with commands
- `README.md` documenting the magical one-liner at the top, in both FR and EN (R9 bilingual for public docs)
- `memory/reference/automation-stack.md` template for recording installed state for future sessions

### Self-rating after refinement

- Pain-driven coverage: 10/10 (fully covers the user's refined question)
- Prose cleanliness: 7/10 (the spec now has two strata — preserved as layering intentionally)
- Best-at-date alignment: 10/10 (magical one-liner + VS Code MCP discovery + Antigravity Q2 2026)
- Self-contained: 9/10 (references two research entries but stands alone for Phase -1 design)
- Anti-Frankenstein: 9/10 (Antigravity kept optional, not mandated)
- Average: **9.0/10** — slightly above the 8.5 target because this spec is load-bearing for v1 design

**Note on the layered format**: this spec intentionally preserves the 2026-04-14 initial section and adds the 2026-04-15 refinement on top, instead of rewriting. This mirrors the journal system's stratified dialogue pattern. Future refinements can add further dated sections without erasing history.

---

## Refinement layer 2 — 2026-04-15 — multidevice in v1 core (beta-tester reality)

User framing on 2026-04-15: *"multidevice dès le début on a des beta testeurs"*. This reclassifies multidevice support from optional Phase -1.7 bonus to **core Phase -1** baseline.

### Rationale

Beta testers will observe and critique multidevice behaviour from day one. Shipping Genesis v1 without multidevice in the default flow would signal that the feature is afterthought-grade. The user's profile (Claude Max 20x subscriber running projects across desktop + mobile) is representative of the beta audience, and the Claude Code Remote Control + mobile companion combo is already mature as of Q2 2026.

### What moves to core Phase -1

The following items are **promoted from -1.7 optional to -1.3 core**:

| Item | Rationale | Subscription gate |
|---|---|---|
| Claude mobile app install (iOS or Android) | Mobile companion surface, works for all plan tiers | None (free app, paid plan for full features) |
| **Claude Code Remote Control** setup | Drives desktop session from phone, native streaming, auto-reconnect | **Claude Max** ($100–200/mo) |

### Subscription-aware branching

Phase -1.3 detects the user's plan tier (via the signed-in Claude account state) and branches:

```
IF plan is Claude Max (or higher):
  - Install Claude mobile app
  - Walk through Claude Code Remote Control pairing
  - Verify pairing works with a simple ping from phone to desktop
  - Record the mobile device's OS in memory/reference/mobile-companion.md
  - Fully multidevice-enabled bootstrap → ready for Phase 0

ELIF plan is Pro or Team:
  - Install Claude mobile app for read-only access
  - Mention that Remote Control requires upgrading to Max
  - Fall back to GitHub Codespaces pattern as the any-device alternative
  - Fully usable but without the native Remote Control streaming

ELIF plan is Free (Claude Code not available at all):
  - Block Phase -1.3 with a clear error
  - Direct user to Pro or Max signup
  - This is not a valid Genesis target state — Claude Code requires paid plan
```

### What stays optional in Phase -1.7

- **Google Antigravity** — optional advanced bonus for multi-model / multi-agent workflows
- **GitHub Codespaces** — optional cloud fallback for users who want any-browser access (but Pro users may be funneled here as their Remote Control alternative)
- **Voice mode** — `/voice` toggle, still gated rollout
- **Android Termux** — power-user escape hatch, opt-in only
- **Connector presets** — per-project, deferred to Phase 5.5

### Updated stack table

| Layer | Tool | Status | Notes |
|---|---|---|---|
| 2 | Claude Code CLI | **Phase -2 prerequisite** — one-line installer | User action |
| 3 | Node.js LTS | Auto-install if missing | winget / brew / apt |
| 3 | Git | Auto-install if missing | winget / brew / apt |
| 3 | VS Code | Auto-install if missing | winget / brew / apt |
| 3 | Chrome | Auto-install if missing | winget / brew / apt |
| 4 | Claude Code VS Code extension | Auto-install — doubles as `ide` MCP server | CLI command |
| 4 | Playwright MCP | Auto-install | `claude mcp add` |
| 4 | Claude in Chrome | Paste-back (permission floor) | One extension install |
| 4 | **Claude mobile app (iOS or Android)** | **Core — promoted from bonus** | User installs on their phone; Claude walks through |
| 4 | **Claude Code Remote Control** | **Core if plan is Max** — else falls back to Codespaces | Pairing flow guided by Claude |
| 7 (optional) | Google Antigravity | Opt-in bonus, paste-back install | Multi-model agent orchestration |
| 7 (optional) | GitHub Codespaces fallback | Opt-in for Pro users needing any-device access | — |
| 7 (optional) | Android Termux local | Opt-in power-user path | Android only |
| 7 (optional) | Voice mode `/voice` | Opt-in if available | Gated rollout Q1-Q2 2026 |

### Phase -1.4 (sign-in round) — now includes mobile pairing

The consolidated sign-in round gains a "pair your phone" step after the GitHub sign-in:

```
Consolidated Phase -1.4 sign-in checklist:
  ☐ Claude in Chrome extension → Anthropic account sign-in
  ☐ GitHub web UI → account sign-in (if not already)
  ☐ Claude mobile app on phone → Anthropic account sign-in (same account)
  ☐ Claude Code Remote Control pairing → accept pairing prompt on phone
  ☐ Any project-specific services for Phase 5.5
```

Five checkboxes in a single Chrome sitting + phone sitting, done in ~3–5 minutes. No context-switching back to the terminal between them.

### Self-rating after layer 2 refinement

- Pain-driven coverage: 10/10
- Prose cleanliness: 7/10 (now three strata — preserved intentionally)
- Best-at-date alignment: 10/10
- Self-contained: 9/10
- Anti-Frankenstein: 9/10 (multidevice is justified by beta-tester framing; optional bonuses are still clearly optional)
- Average: **9.0/10** — same as layer 1, holds the target
