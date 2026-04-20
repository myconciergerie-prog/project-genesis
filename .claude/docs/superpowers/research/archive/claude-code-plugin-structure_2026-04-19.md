<!-- SPDX-License-Identifier: MIT -->
---
topic: claude-code-plugin-structure
type: stack
created_at: 2026-04-19
expires_at: 2026-04-20
status: active
template_of: genesis-protocol v1.4.2
sources:
  - https://code.claude.com/docs/en/plugins-reference
  - https://github.com/anthropics/claude-code/blob/main/plugins/README.md
  - https://github.com/anthropics/claude-plugins-official
  - https://www.datacamp.com/tutorial/how-to-build-claude-code-plugins
  - https://dev.classmethod.jp/en/articles/claude-code-skills-subagent-plugin-guide/
confidence: high
supersedes: archive/claude-code-plugin-structure_2026-04-14.md
---

# Claude Code Plugin Structure — Spec Snapshot 2026

## Canonical directory layout

```
<plugin-name>/
├── .claude-plugin/
│   └── plugin.json       ← manifest ONLY lives here, nothing else
├── commands/             ← slash commands (backward-compatible flat .md files)
├── agents/               ← custom sub-agents
├── skills/               ← skills (RECOMMENDED over commands/ in 2026)
├── output-styles/        ← output style definitions
├── monitors/
│   └── monitors.json     ← background monitor configurations
├── hooks/
│   └── hooks.json        ← auto-loaded
├── bin/                  ← executables added to Bash tool PATH
├── templates/            ← reusable templates (Genesis-specific convention)
├── scripts/              ← helper scripts
├── settings.json         ← default settings applied when plugin is enabled
├── .mcp.json             ← MCP server declarations (optional)
├── .lsp.json             ← LSP server configurations (optional)
├── README.md
├── LICENSE
└── CHANGELOG.md
```

**Critical gotcha**: `commands/`, `agents/`, `skills/`, `hooks/`, `output-styles/`, `monitors/`, and `bin/` **MUST** be at the plugin root — NOT inside `.claude-plugin/`. The `.claude-plugin/` directory holds **only** `plugin.json`. Getting this wrong breaks auto-discovery.

## plugin.json fields

### Required

If you include a manifest, `name` is the **only** required field. The manifest itself is optional — Claude Code auto-discovers components from standard directories and derives plugin name from the directory name when no manifest is present.

- `name` — machine-readable slug (kebab-case, no spaces); used for component namespacing in the UI (e.g. agent `agent-creator` for plugin `plugin-dev` appears as `plugin-dev:agent-creator`)

### Metadata fields (recommended)

- `version` — semver (`1.0.0`); if also set in marketplace entry, `plugin.json` takes priority
- `description` — one-line human summary
- `author` — object with `name`, `email`, `url`
- `homepage` — project website or README URL
- `repository` — git URL
- `license` — SPDX short identifier (e.g. `"MIT"`)
- `keywords` — array of tags for discovery

### Component path fields (optional overrides)

- `skills`, `commands`, `agents`, `outputStyles`, `monitors` — custom path(s) replacing the default directory; accepts string or array
- `hooks`, `mcpServers`, `lspServers` — config paths or inline config; multiple sources merge rather than replace
- `dependencies` — array of plugin names (or `{ "name": "...", "version": "~2.1.0" }` objects) this plugin requires
- `userConfig` — object of user-configurable values prompted at enable time; keys available as `${user_config.KEY}` in commands and as `CLAUDE_PLUGIN_OPTION_<KEY>` env vars
- `channels` — array of message-channel declarations (Telegram, Slack, Discord style) bound to an MCP server

**Path rules**: all custom paths must be relative to plugin root and start with `./`. For `skills`, `commands`, `agents`, `outputStyles`, and `monitors`, a custom path *replaces* the default — to keep the default AND add more paths, include the default in an array: `"skills": ["./skills/", "./extras/"]`.

Only needed when a directory lives outside the standard path. For Genesis we use standard paths → no overrides required.

## Auto-discovery behaviour

Claude Code auto-loads components from the standard directories above without requiring explicit paths in `plugin.json`. The `hooks/hooks.json` file is auto-loaded. Manifest-level `hooks` is only used to reference **additional** hook files beyond the default.

## Available hook events

As of 2026, the full set of supported hook events (case-sensitive):

| Event | When it fires |
|---|---|
| `SessionStart` | When a session begins or resumes |
| `UserPromptSubmit` | When you submit a prompt, before Claude processes it |
| `PreToolUse` | Before a tool call executes. Can block it |
| `PermissionRequest` | When a permission dialog appears |
| `PermissionDenied` | When a tool call is denied by auto mode classifier; return `{retry: true}` to allow model retry |
| `PostToolUse` | After a tool call succeeds |
| `PostToolUseFailure` | After a tool call fails |
| `Notification` | When Claude Code sends a notification |
| `SubagentStart` | When a subagent is spawned |
| `SubagentStop` | When a subagent finishes |
| `TaskCreated` | When a task is being created via `TaskCreate` |
| `TaskCompleted` | When a task is being marked as completed |
| `Stop` | When Claude finishes responding |
| `StopFailure` | When the turn ends due to an API error |
| `TeammateIdle` | When an agent team teammate is about to go idle |
| `InstructionsLoaded` | When a CLAUDE.md or `.claude/rules/*.md` file is loaded into context |
| `ConfigChange` | When a configuration file changes during a session |
| `CwdChanged` | When the working directory changes (e.g. Claude executes `cd`) |
| `FileChanged` | When a watched file changes on disk; `matcher` field specifies which filenames to watch |
| `WorktreeCreate` | When a worktree is being created via `--worktree` or `isolation: "worktree"` |
| `WorktreeRemove` | When a worktree is being removed |
| `PreCompact` | Before context compaction |
| `PostCompact` | After context compaction completes |
| `Elicitation` | When an MCP server requests user input during a tool call |
| `ElicitationResult` | After a user responds to an MCP elicitation |
| `SessionEnd` | When a session terminates |

## Hook types

- `command` — execute shell commands or scripts
- `http` — send the event JSON as a POST request to a URL
- `prompt` — evaluate a prompt with an LLM (uses `$ARGUMENTS` placeholder for context)
- `agent` — run an agentic verifier with tools for complex verification tasks

## Skills vs commands — 2026 unification

Slash commands and skills are **unified** in 2026. Files in `.claude/commands/` still work for backward compatibility, but the recommended approach is `.claude/skills/`. Every skill automatically gets a `/<skill-name>` slash-command interface. A plugin that ships only `skills/` gets both slash commands and auto-activation for free.

Skills are directories with `SKILL.md`; commands are simple flat markdown files. The `skills/` directory is the recommended path for new plugins.

## Plugin installation scopes

| Scope | Settings file | Use case |
|---|---|---|
| `user` | `~/.claude/settings.json` | Personal plugins across all projects (default) |
| `project` | `.claude/settings.json` | Team plugins shared via version control |
| `local` | `.claude/settings.local.json` | Project-specific plugins, gitignored |
| `managed` | Managed settings | Read-only, update only |

## Plugin caching

Marketplace-installed plugins are copied to `~/.claude/plugins/cache/` rather than used in-place. Each installed version is a separate directory. Previous versions are marked orphaned and removed 7 days after update/uninstall (grace period for concurrent sessions).

The `${CLAUDE_PLUGIN_DATA}` variable resolves to `~/.claude/plugins/data/{id}/` — a persistent directory that survives plugin updates. Use this for `node_modules`, Python virtualenvs, generated code, and caches. Deleted automatically when plugin is uninstalled from all scopes (unless `--keep-data` is passed).

## Application for Genesis

- `.claude-plugin/plugin.json` with:
  - `"name": "project-genesis"`
  - `"version": "1.0.0"` (at first release)
  - `"description": "..."`
  - `"license": "MIT"`
  - `"author"`, `"repository"`, `"homepage"`, `"keywords"` populated
- `skills/` directory containing Genesis-specific skills: `genesis-protocol/`, `journal-system/`, `session-post-processor/`, `auth-preflight/`, `meta-memory/` (exact list finalized at Étape 4)
- `templates/` directory for the Project Genesis protocol markdown and any reusable scaffolds
- `hooks/hooks.json` **only if** we have a `SessionEnd` hook to trigger the session post-processor — defer until the post-processor skill is ready and the user validates it should auto-run
- No `commands/` directory unless a skill has a reason to also expose an explicit `commands/` form — avoid duplication
