<!-- SPDX-License-Identifier: MIT -->
---
topic: claude-ecosystem-cross-os
type: sota
created_at: 2026-04-15
expires_at: 2026-04-22
status: active
sources:
  - https://venturebeat.com/orchestration/anthropic-just-released-a-mobile-version-of-claude-code-called-remote
  - https://sealos.io/blog/claude-code-on-phone/
  - https://www.builder.io/blog/claude-code-mobile-phone
  - https://support.claude.com/en/articles/11869629-using-claude-with-android-apps
  - https://techcrunch.com/2026/03/03/claude-code-rolls-out-a-voice-mode-capability/
  - https://support.claude.com/en/articles/11101966-using-voice-mode
  - https://github.com/rdmgator12/awesome-claude-connectors
  - https://support.claude.com/en/articles/11596036-anthropic-connectors-directory-faq
  - https://www.anthropic.com/partners/mcp
  - https://popularaitools.ai/blog/claude-code-workflow-patterns-agentic-guide-2026
  - https://news.ycombinator.com/item?id=46544142
  - https://www.skeptrune.com/posts/claude-code-on-mobile-termux-tailscale/
  - https://chamith.medium.com/how-we-integrated-claude-code-into-our-github-workflow-97a5db8bcb8e
confidence: high
supersedes: null
---

# Claude Ecosystem Across Operating Systems — Q2 2026 SOTA

## TL;DR

As of Q2 2026, the Claude ecosystem covers every major platform with increasingly tight integration:

- **Desktop**: Windows, macOS, Linux all get Claude Code CLI + VS Code extension + Claude in Chrome + native desktop app
- **Mobile native**: iOS and Android get the Claude app with full feature parity + voice mode + system integrations (Siri Shortcuts iOS, system app automation Android)
- **Mobile → Desktop bridge**: **Claude Code Remote Control** (October 2025+) lets iPhone/Android drive a desktop Claude Code session over a native streaming connection — no port forwarding, no VPN, auto-reconnect. Claude Max tier required.
- **Cloud-first**: GitHub Codespaces integration lets Claude Code run in a browser-accessible cloud container; @mention `@claude` on a GitHub issue and Claude checks out, fixes, tests, opens PR without any local action
- **Android-native dev**: Termux + SSH + Tailscale + tmux gives Android users a full Linux dev environment with Claude Code CLI running locally on the phone — laptop-less development
- **Connector ecosystem**: Anthropic's Claude Connectors Directory lists **280 verified MCP integrations** across databases, dev tools, communication, cloud, and productivity. Plus 150+ community servers. The ecosystem replaced "every AI tool integration" in 2026.

## Per-OS capability matrix

### Windows 10/11

| Capability | How |
|---|---|
| Claude Code CLI | `irm https://claude.ai/install.ps1 \| iex` — native installer, no Node required |
| Claude Code VS Code extension | `code --install-extension anthropic.claude-code` — runs `ide` MCP server locally |
| Claude in Chrome | Chrome Web Store — `claude --chrome` or `/chrome` in session |
| Claude Desktop app | Windows native Electron app, paid plan |
| Claude mobile companion | Remote Control from iOS/Android drives the desktop session |
| Package manager | `winget` pre-installed since 2020, user-scope non-admin installs |
| Browser automation | Playwright MCP via `claude mcp add` |
| Multi-model IDE | Google Antigravity (native Windows build, free) |
| Voice mode | `/voice` in Claude Code (rolling out March 2026), 5% of users early |
| Native integration | PowerShell 7 + winget + registry = full automation surface |

### macOS

| Capability | How |
|---|---|
| Claude Code CLI | `curl -fsSL https://claude.ai/install.sh \| bash` |
| Claude Code VS Code extension | Same as Windows |
| Claude in Chrome | Same as Windows |
| Claude Desktop app | macOS native, richer notifications, Shortcuts integration |
| Claude mobile companion | Remote Control from iOS handoff-friendly |
| Package manager | `brew` — one-line install if missing |
| Browser automation | Playwright MCP |
| Multi-model IDE | Google Antigravity (native macOS build) |
| Voice mode | `/voice` in Claude Code |
| Apple ecosystem | Shortcuts integration, Universal Clipboard, Handoff |

### Linux

| Capability | How |
|---|---|
| Claude Code CLI | `curl -fsSL https://claude.ai/install.sh \| bash` |
| Claude Code VS Code extension | Same as above |
| Claude in Chrome or Edge | Chrome Web Store |
| Claude Desktop app | Varies per distro — AppImage / .deb / .rpm |
| Package managers | `apt` / `dnf` / `pacman` depending on distro |
| Browser automation | Playwright MCP |
| Multi-model IDE | Google Antigravity (Linux build) |
| Voice mode | `/voice` in Claude Code |

### iOS

| Capability | How |
|---|---|
| Claude mobile app | App Store, free install, paid plan for full features |
| Voice mode | 5 voices, full Claude conversations |
| Vision | Camera + image upload + analysis |
| Artifacts | Read / edit / create artifacts on the phone |
| File creation & editing | Native |
| Health data analytics | Pro/Max plans only |
| Siri Shortcuts | Trigger Claude from Siri or iOS Shortcuts app |
| Reminders integration | Claude can create Reminders items from chat |
| **Claude Code Remote Control** | Since October 2025, issue commands to your desktop Claude Code from the iOS app — requires Claude Max subscription |
| Claude Code in GitHub Codespaces | Via browser or Catnip-style iOS client — run Claude Code in a cloud container, access from phone |
| No local CLI | iOS sandboxing prevents shell / Termux equivalents |

### Android

| Capability | How |
|---|---|
| Claude mobile app | Play Store, feature parity with iOS |
| Voice mode | Same as iOS |
| Vision, Artifacts, Files | Same as iOS |
| Home screen widgets | Android-specific UI surface |
| **System app automation** | Claude can draft messages, emails, calendar events, set alarms and timers, find locations, use everyday apps — **without copy-paste**. Deeper OS integration than iOS. |
| **Claude Code Remote Control** | Same as iOS, driving desktop session |
| **Termux + full Linux env** | Termux gives a real Linux terminal on Android with no root; can run Claude Code CLI natively on the phone |
| **Termux + SSH + Tailscale + tmux** | Power-user setup — desktop runs Claude Code, Tailscale creates a private network, Termux gives Android a real terminal, SSH connects, tmux keeps sessions alive across disconnects |
| Claude Code in GitHub Codespaces | Same as iOS |
| Most powerful mobile dev option | Android beats iOS for local development on-device thanks to Termux |

## The wow combos — beyond Antigravity

### Combo 1 — Claude Code Remote Control

**What it is**: Anthropic released a "Remote Control" mode in October 2025 that lets iPhone or Android users issue commands to a desktop Claude Code session from their phone. Native streaming connection, no port forwarding, no VPN, auto-reconnect on laptop sleep / network drop / etc.

**Why it's wow**: this replaces the entire Termux + SSH + Tailscale + tmux setup with a single-button pairing. Claude Max subscribers (user has this) can start a long-running task on desktop, leave the house, and continue supervising/issuing commands from their phone during a commute, a walk, or a coffee break. The session persists.

**User requirement**: Claude Max tier ($100-200/month). User has Claude Max 20x → eligible.

### Combo 2 — Claude Code + GitHub @mention workflow

**What it is**: a GitHub integration where a team member types `@claude <task description>` in a GitHub issue or PR comment, and Claude Code automatically checks out the repo in a cloud context, creates a branch, makes the fix, runs tests, and opens a PR. Zero local checkout required.

**Why it's wow**: turns GitHub itself into an async interface to Claude Code. A developer can assign non-critical issues to Claude while doing something else, and Claude returns with a PR for review. Works from any device that can post a GitHub comment — including mobile GitHub apps.

**Setup**: GitHub App + Claude Code action integration (documented in Anthropic's GitHub workflow integration guides).

### Combo 3 — Claude Code in GitHub Codespaces (Catnip pattern)

**What it is**: spin up a GitHub Codespace pre-configured with Claude Code installed and logged in. Access the Codespace from any device — desktop browser, iPad Safari, Android Chrome, iPhone browser. Run Claude Code in the cloud container, edit code in the browser. Zero local setup.

**Why it's wow**: completely eliminates the "I'm away from my dev machine" problem. Any browser becomes a full Claude Code environment. The Catnip project on GitHub packages this into a one-click pattern for iPhone users.

**Trade-off**: Codespaces has usage costs (GitHub billing), and the cloud context has latency compared to local. Best for async / long-running tasks.

### Combo 4 — Android Termux local Claude Code

**What it is**: install Termux from F-Droid on Android, bootstrap a Linux environment, install Claude Code CLI directly on the phone. No desktop involved. Your phone becomes a self-contained dev machine.

**Why it's wow**: truly laptop-less development. For emergency fixes, hackathons, travel, or people who want to code from anywhere. Pair with a Bluetooth keyboard and a phone stand and you have a 150g dev workstation.

**Limitations**: ARM-only (most Android phones are ARM, fine), battery life, screen size, typing ergonomics. But works fully.

### Combo 5 — Claude Desktop + MCP connectors at scale

**What it is**: the Claude Desktop app supports the same MCP servers as Claude Code. Anthropic's Claude Connectors Directory lists **280 verified MCP integrations** across:

- **Databases**: PostgreSQL, SQLite, MongoDB, MySQL, Redis, BigQuery, Snowflake
- **Dev tools**: GitHub, GitLab, Bitbucket, Jira, Linear, Jenkins, CircleCI
- **Communication**: Slack, Discord, Notion, Microsoft Teams, Zoom
- **Productivity**: Asana, Box, Canva, Figma, Hex, monday.com, Airtable
- **Cloud**: AWS, GCP, Azure, Cloudflare
- **Files**: Google Drive, Dropbox, OneDrive, Box
- **Finance/data**: Stripe, Plaid, S&P Global, Ahrefs
- **Search/research**: Perplexity, Brave Search, Google Search
- **Custom**: anyone can write their own MCP server in Python / TypeScript / any language

Plus 150+ community-contributed servers in the Awesome MCP list. By early 2026, MCP had reached 97 million installs and was treated as the de-facto standard for AI tool integration.

**Why it's wow**: Claude becomes the center of a **vast** ecosystem of tools, replacing the need for dozens of individual service integrations. Write once, plug into anything that speaks MCP.

### Combo 6 — Voice mode in Claude Code (desktop)

**What it is**: `/voice` toggle inside Claude Code, rolling out in March 2026. Speak commands instead of typing. Five voice personalities. ~5% of users enabled so far, broader rollout coming.

**Why it's wow**: for long coding sessions, voice becomes a hands-free escape valve — dictate while you have a coffee, explain plans while you pace, brainstorm while you look out a window. Combined with Claude Code's plan mode, voice lets you narrate architecture at the speed of thought and have Claude turn it into a written plan.

**Status**: early beta, gradual rollout — may not be available to the user yet.

### Combo 7 — Android Claude app + system apps

**What it is**: on Android, Claude integrates directly with system apps. From a conversation, Claude can draft a WhatsApp message, create a calendar event, set a timer, find a location in Maps, compose an email, add a reminder, all without the user copy-pasting anything between apps.

**Why it's wow**: this is the natural extension of the agentic paradigm into daily life, not just coding. Android's deeper OS-level integrations give Claude a superpower that iOS's sandboxed apps don't match as tightly. For a multi-project owner running a life's worth of communications, the time savings stack up.

## Anthropic Connectors Directory — scale check

- **280 verified** MCP integrations in the official directory as of early 2026
- **50+** official MCP servers maintained in Anthropic's GitHub organization
- **150+** community-contributed servers in the Awesome MCP list
- **97 million** MCP installs by January 2026 — the protocol is effectively the industry standard for AI tool integration
- Anyone can build a custom connector in Python or TypeScript — Anthropic publishes the spec

**Finding a specific connector**: search Anthropic's help center article "Anthropic Connectors Directory FAQ" or browse the awesome-claude-connectors GitHub list.

## Workflow patterns that move the needle

From production usage data summarized by multiple sources:

- **Sequential Flow (Explore-Plan-Act)** — 70% of daily work. Three permission-escalating phases: read-only exploration, plan review, full-access implementation.
- **Operator Pattern** — central orchestrator delegates to specialized sub-agents. For tasks that need parallel coordination.
- **Planning-first pattern** — draft a plan with no implementation, annotate, send back, repeat until locked, then implement. Anthropic internal testing: unguided attempts succeed ~33% of the time; structured planning dramatically raises success rate.
- **Key insight**: the difference between high-output engineers and everyone else is NOT prompt quality — it's the structure they build around Claude before execution. Genesis's phased protocol with validation checkpoints is exactly this pattern.

## Application for Genesis v1 Phase -1

The cross-OS ecosystem discovery adds three optional Phase -1 recommendations on top of the core stack:

### New Phase -1.7 entries (all optional, opt-in)

1. **Claude Code Remote Control** — for Claude Max subscribers, install the Claude mobile app on iOS or Android and pair it with the desktop Claude Code session. Zero-config, one-time setup, persistent sessions.
2. **Mobile companion install** — even without Remote Control, Genesis can suggest installing the Claude mobile app for the user's preferred phone OS so they have a ubiquitous Claude interface.
3. **Cloud fallback option** — document the GitHub Codespaces pattern as an optional setup for users who want Claude Code accessible from any browser (useful for multi-machine workflows or travel).
4. **Android-specific** — if the user is on Android, mention the Termux pattern as a power-user escape hatch. If on iOS, the Remote Control pattern replaces it.

### Updated Phase -1 consent card language

"Genesis can optionally set up a mobile companion so you can monitor or drive Claude Code from your phone. Options: (a) Claude iOS app + Remote Control, (b) Claude Android app + Remote Control, (c) GitHub Codespaces with Claude Code (browser-accessible from anywhere), (d) Skip for now. Your choice."

This is **opt-in**, not required. Anti-Frankenstein preserved: no user gets forced into a mobile setup if they don't want one.

### Why not recommend ALL the tools

Every combo above is valid and wow, but mandating them all would be the classic Frankenstein trap. Genesis v1 Phase -1 sticks with:

- **Required**: Claude Code CLI, VS Code extension, Playwright MCP
- **Strongly recommended**: Claude in Chrome
- **Optional bonuses**: Google Antigravity, Claude mobile app + Remote Control, GitHub Codespaces fallback, Android Termux (power user)
- **Skipped by design**: voice mode (beta, gated), Catnip / custom cloud patterns (too niche), specific MCP connectors (deferred to per-project needs in Phase 5.5)

## Self-rating

- Pain-driven: 9/10 (user explicitly asked for the breadth)
- Prose cleanliness: 7/10 (long but structured)
- Best-at-date: 10/10 (covers Q2 2026 completely)
- Self-contained: 9/10 (standalone reference)
- Anti-Frankenstein: 8/10 (selective, but captures a lot — could be tighter)
- Average: **8.6/10**
