<!-- SPDX-License-Identifier: MIT -->

# Research Cache INDEX — project-genesis

Auto-maintained index of R8 research cache entries. Every entry has a TTL and moves to `archive/` when `expires_at < today`. TTLs: `sota/` = 7 days, `stack/` = 1 day.

## Active

| Topic | Type | Created | Expires | Confidence | Summary |
|---|---|---|---|---|---|
| [open-source-license-for-dev-tooling](sota/open-source-license-for-dev-tooling_2026-04-14.md) | sota | 2026-04-14 | 2026-04-21 | high | MIT for Genesis; Apache-2 as pivot path; BSL rejected |
| [claude-code-plugin-distribution](sota/claude-code-plugin-distribution_2026-04-14.md) | sota | 2026-04-14 | 2026-04-21 | high | Self-hosted marketplace now, official Anthropic marketplace later |
| [spdx-headers](sota/spdx-headers_2026-04-14.md) | sota | 2026-04-14 | 2026-04-21 | high | `SPDX-License-Identifier: MIT` short form, every source file |
| [claude-code-plugin-structure](stack/claude-code-plugin-structure_2026-04-14.md) | stack | 2026-04-14 | 2026-04-17 | high | `.claude-plugin/plugin.json` + root-level `commands/`, `skills/`, `hooks/`; skills unified with slash commands in 2026; refreshed 2026-04-16 (v0.9.0 — structure still matches six shipped skills on disk, no observed SDK changes) |
| [claude-code-session-jsonl-format](stack/claude-code-session-jsonl-format_2026-04-15.md) | stack | 2026-04-15 | 2026-04-17 | high | JSONL transcripts at `~/.claude/projects/<slug>/<uuid>.jsonl` flat layout **on-disk verified**; outer types (user/assistant/system/file-history-snapshot/attachment) vs inner content-block types (text/thinking/tool_use/tool_result) clarified; supersedes 2026-04-14 entry; refreshed 2026-04-16 (v0.9.0 session) |
| [claude-in-ide-tools](sota/claude-in-ide-tools_2026-04-15.md) | sota | 2026-04-15 | 2026-04-22 | high | VS Code extension IS an MCP server (`ide`); Google Antigravity runs Claude Sonnet 4.6/Opus 4.6 natively alongside Gemini 3.1 Pro, free for individuals, agent-first Manager Surface; one-liner Claude Code install `irm https://claude.ai/install.ps1 \| iex` on Windows |
| [claude-ecosystem-cross-os](sota/claude-ecosystem-cross-os_2026-04-15.md) | sota | 2026-04-15 | 2026-04-22 | high | Per-OS capability matrix (Windows/macOS/Linux/iOS/Android); Claude Code Remote Control since Oct 2025; 280 verified MCP connectors; Android Termux local Claude Code; GitHub Codespaces cloud pattern; 7 wow combos identified |

## Archive

- [claude-code-session-jsonl-format_2026-04-14.md](archive/claude-code-session-jsonl-format_2026-04-14.md) — superseded by the 2026-04-15 on-disk-verified entry
