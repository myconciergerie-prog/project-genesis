<!-- SPDX-License-Identifier: MIT -->
---
topic: claude-code-plugin-structure
type: stack
created_at: 2026-04-14
expires_at: 2026-04-17
status: active
refreshed_at: 2026-04-16
sources:
  - https://code.claude.com/docs/en/plugins
  - https://github.com/affaan-m/everything-claude-code/blob/main/.claude-plugin/PLUGIN_SCHEMA_NOTES.md
  - https://claude-plugins.dev/skills/@anthropics/claude-plugins-official/plugin-structure
  - https://dev.classmethod.jp/en/articles/claude-code-skills-subagent-plugin-guide/
  - https://mcpmarket.com/tools/skills/claude-code-plugin-schema-reference
confidence: high
supersedes: null
---

# Claude Code Plugin Structure — Spec Snapshot 2026

## Canonical directory layout

```
<plugin-name>/
├── .claude-plugin/
│   └── plugin.json       ← manifest ONLY lives here, nothing else
├── commands/             ← slash commands (backward-compatible)
├── agents/               ← custom sub-agents
├── skills/               ← skills (RECOMMENDED over commands/ in 2026)
├── hooks/
│   └── hooks.json        ← auto-loaded
├── templates/            ← reusable templates (Genesis-specific convention)
├── scripts/              ← helper scripts
├── .mcp.json             ← MCP server declarations (optional)
├── README.md
├── LICENSE
└── CHANGELOG.md
```

**Critical gotcha**: `commands/`, `agents/`, `skills/`, `hooks/` **MUST** be at the plugin root — NOT inside `.claude-plugin/`. The `.claude-plugin/` directory holds **only** `plugin.json`. Getting this wrong breaks auto-discovery.

## plugin.json fields

### Required

- `name` — machine-readable slug
- `version` — semver (`1.0.0`)
- `description` — one-line human summary

### Recommended

- `author` — object with `name`, `email`, `url`
- `homepage` — project website or README URL
- `repository` — git URL
- `license` — SPDX short identifier (e.g. `"MIT"`)
- `keywords` — array of tags for discovery

### Optional custom-path overrides

- `commands`, `agents`, `skills`, `hooks`, `mcpServers`, `outputStyles`, `lspServers`

Only needed when a directory lives outside the standard path. For Genesis we use standard paths → no overrides required.

## Auto-discovery behaviour

Claude Code auto-loads components from the standard directories above without requiring explicit paths in `plugin.json`. The `hooks/hooks.json` file is auto-loaded. Manifest-level `hooks` is only used to reference **additional** hook files beyond the default.

## Available hook events

`PreToolUse`, `PostToolUse`, `Stop`, `SubagentStop`, `SessionStart`, `SessionEnd`, `UserPromptSubmit`, `PreCompact`, `Notification`

## Skills vs commands — 2026 unification

Slash commands and skills are **unified** in 2026. Files in `.claude/commands/` still work for backward compatibility, but the recommended approach is `.claude/skills/`. Every skill automatically gets a `/<skill-name>` slash-command interface. A plugin that ships only `skills/` gets both slash commands and auto-activation for free.

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
