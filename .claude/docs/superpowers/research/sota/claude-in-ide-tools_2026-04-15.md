<!-- SPDX-License-Identifier: MIT -->
---
topic: claude-in-ide-tools
type: sota
created_at: 2026-04-15
expires_at: 2026-04-22
status: active
sources:
  - https://code.claude.com/docs/en/vs-code
  - https://marketplace.visualstudio.com/items?itemName=anthropic.claude-code
  - https://developers.googleblog.com/build-with-google-antigravity-our-new-agentic-development-platform/
  - https://medevel.com/google-antigravity-meets-claude-code/
  - https://www.datacamp.com/blog/claude-code-vs-antigravity
  - https://en.wikipedia.org/wiki/Google_Antigravity
  - https://dev.to/norinori1/the-complete-guide-to-using-claude-copilot-antigravity-jules-gemini-cli-effectively2026-41ja
  - https://medium.com/@joe.njenga/i-tried-claude-code-in-google-antigravity-and-discovered-a-new-insane-workflow-e5402d043aa4
  - https://www.morphllm.com/install-claude-code
confidence: high
supersedes: null
---

# Claude in IDEs — Q2 2026 State of the Art

## TL;DR

Four viable IDE entry points for Claude-based development in Q2 2026, ranked by fit for a solo-owner workflow tooling project like Genesis:

1. **Claude Code CLI + VS Code extension** — best-at-date mainstream. Gives inline diffs, autonomous exploration, `ide` MCP server, subagents, plan mode, extended thinking toggle.
2. **Claude Code CLI alone** — minimum viable, maximum autonomy, terminal-native. Best for headless sessions and advanced users.
3. **Google Antigravity + Claude** — agent-first IDE that runs Claude Sonnet 4.6 and Claude Opus 4.6 natively alongside Gemini 3.1 Pro / 3 Flash / GPT-OSS 120B. Free for individuals. Manager Surface orchestrates parallel agents across workspaces.
4. **Cursor** — still popular but lags Claude Code + Antigravity on agent-first workflows.

For Project Genesis v1 Phase -1, recommend stack (1) as default and offer stack (3) as optional bonus for users who want multi-model workflows from day one.

## Claude Code VS Code extension — unique value Q2 2026

Official Anthropic extension (`anthropic.claude-code`). GA early 2026.

### Unique vs CLI

- **Sidebar panel with real-time inline diffs** — accept/reject per file, per change, side-by-side like a Git client
- **Autonomous exploration** — Claude reads, writes, navigates the codebase independently while the user watches in the IDE
- **Subagents panel** — multiple parallel AI tasks visible as separate tabs in the editor
- **Extended thinking toggle** — UI switch for reasoning visibility on/off (CLI has it, extension exposes a clickable toggle)
- **Plan mode** — review and edit Claude's plans before accepting; plans are interactively editable in the extension UI
- **`@`-mentions with file + line ranges** — reference a specific slice of a file in a prompt without copy-pasting
- **`@terminal:name`** — reference a terminal's live output in a prompt, so Claude reads command output / errors / logs without copy-paste
- **Context awareness** — extension knows the currently open file and active selection

### Architectural point — the extension IS an MCP server

When the VS Code extension activates, it runs a **local MCP server named `ide`** that the Claude Code CLI connects to **automatically**. This lets:

- The CLI agent open diffs in VS Code's native diff viewer
- The CLI agent read the user's current VS Code selection
- The CLI agent execute Jupyter notebook cells with a confirmation step
- Any Claude Code session on the machine access VS Code's native capabilities without extra MCP setup

**Implication for Genesis**: installing the VS Code extension is **doubly valuable** — it adds IDE UX AND extends the MCP surface available to all Claude Code sessions on the machine. This was the missing piece in the earlier assessment.

### CLI retains advantages

- Fully autonomous long-running tasks
- Checkpoint management for complex workflows
- Rapid terminal interactions with full command access
- Deeper control over process lifecycle
- Headless operation on remote machines / CI

### Recommended pattern for Genesis

- **Phase 0 → 5** of the Genesis protocol: use the **CLI** (fast, autonomous, checkpoint-friendly)
- **Diff review** in Phase 5: switch to **VS Code extension** sidebar for accept/reject per file
- **Post-bootstrap content iteration**: VS Code extension for the ergonomics; fall back to CLI when a session needs to be headless

## Google Antigravity — Q2 2026 SOTA agent IDE

Announced **November 18, 2025** by Google alongside Gemini 3. **Public preview, free for individuals.** MacOS / Windows / Linux.

### Multi-model support — the strategic value

Antigravity is **model-agnostic**. Available models as of early 2026:

- Gemini 3.1 Pro (High and Low reasoning modes)
- Gemini 3 Flash (fast, cheap)
- **Claude Sonnet 4.6** — native support
- **Claude Opus 4.6** — native support
- GPT-OSS 120B

The user can assign **different models to different agents** — e.g., Opus for architecture planning, Flash for quick implementations, Sonnet for medium tasks — all orchestrated from one IDE surface.

This is the multi-LLM routing the Aurum R7 rule talks about, but done at the IDE layer instead of the app-runtime layer. Huge alignment with the user's multi-LLM subscriber profile in Layer 0.

### Two distinct interaction modes

- **Editor View** — classic AI-powered IDE with tab completions and inline commands. Analogous to Cursor or VS Code + Claude Code extension.
- **Manager Surface** — dedicated surface to **spawn, orchestrate, and observe multiple agents working asynchronously across different workspaces**. This is the agent-first paradigm: instead of one AI helping in one editor, a fleet of agents working in parallel on parts of the project.

### Other features

- Native **1M token context window** via Gemini 3.1 Pro
- Persistent knowledge in `.gemini/antigravity/knowledge/` directory
- **Skills system** for reusable instructions at project level and cross-project — parallels Claude Code's skills concept, worth studying for cross-pollination
- Tab completions powered by the agent model in the Editor View
- Inline command palette for agent invocation

### Hybrid Antigravity + Claude Code — documented pattern

Several sources (Medium, medevel, DataCamp, DEV community) describe a hybrid workflow now used by early-adopter devs in Q1 2026:

- **Claude Code CLI** handles fast local iterations in the terminal
- **Antigravity Manager Surface** handles long-running parallel tasks (e.g., "refactor N modules at once, one agent per module, observe all simultaneously")
- Both access the same filesystem and git repo
- **Opus 4.6** used as the "planner" agent, **Flash** used as the "worker" for repetitive tasks, **Sonnet** for medium-complexity individual tasks
- The user manages the agents instead of coding directly — a manager-level abstraction

### Fit for Genesis v1 Phase -1

**Optional-recommended**, not required. Reasoning:

- Adds install complexity and another account (Google account OAuth for Gemini)
- Delivers clear value for multi-agent workflows but most Genesis bootstraps don't need that on day one
- Frankenstein risk if mandated — many users won't use agent orchestration for a single template project

**Recommendation**: Phase -1 presents Antigravity as **optional advanced bonus** with a clear value proposition — "install if you plan to run multi-agent parallel workflows mixing Gemini + Claude + GPT; skip if you work mostly with Claude Code CLI alone". Opt-in, not opt-out, not blocking.

## One-command Claude Code install — the magical starting point

**Windows PowerShell** (native installer, no Node.js dependency, sets PATH, auto-updates in background):

```powershell
irm https://claude.ai/install.ps1 | iex
```

**Windows CMD** (equivalent):

```cmd
curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
```

**macOS / Linux**:

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

These are the **Phase -2 prerequisite** — the single manual action the user performs before Genesis can take over. After this command runs, `claude` is available globally, auto-updating, and Phase -1 can take full control from inside any Claude Code session.

**Plan requirement**: Pro or higher. Free plan does NOT include Claude Code.

## Application for Genesis v1 Phase -1

- **Mandatory stack**: Claude Code CLI (Phase -2 prerequisite) + VS Code extension + Playwright MCP
- **Strongly recommended**: Claude in Chrome (authenticated browser workflows)
- **Optional advanced bonus**: Google Antigravity (multi-model agent orchestration)
- **The magical one-liner**: `irm https://claude.ai/install.ps1 | iex` is documented in Genesis `README.md` as the Phase -2 command — the single manual action required before Genesis can run
- **3-mode ladder** in Phase -1 (user picks at consent time): detailed pas-à-pas / semi-auto / auto — see `v1_phase_minus_one_first_user_bootstrap_flow.md`
