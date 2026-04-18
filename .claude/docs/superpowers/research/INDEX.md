<!-- SPDX-License-Identifier: MIT -->

# Research Cache INDEX — project-genesis

Auto-maintained index of R8 research cache entries. Every entry has a TTL and moves to `archive/` when `expires_at < today`. TTLs: `sota/` = 7 days, `stack/` = 1 day.

## Active

| Topic | Type | Created | Expires | Confidence | Summary |
|---|---|---|---|---|---|
| [open-source-license-for-dev-tooling](sota/open-source-license-for-dev-tooling_2026-04-14.md) | sota | 2026-04-14 | 2026-04-21 | high | MIT for Genesis; Apache-2 as pivot path; BSL rejected |
| [claude-code-plugin-distribution](sota/claude-code-plugin-distribution_2026-04-14.md) | sota | 2026-04-14 | 2026-04-21 | high | Self-hosted marketplace now, official Anthropic marketplace later |
| [spdx-headers](sota/spdx-headers_2026-04-14.md) | sota | 2026-04-14 | 2026-04-21 | high | `SPDX-License-Identifier: MIT` short form, every source file |
| [claude-in-ide-tools](sota/claude-in-ide-tools_2026-04-15.md) | sota | 2026-04-15 | 2026-04-22 | high | VS Code extension IS an MCP server (`ide`); Google Antigravity runs Claude Sonnet 4.6/Opus 4.6 natively alongside Gemini 3.1 Pro, free for individuals, agent-first Manager Surface; one-liner Claude Code install `irm https://claude.ai/install.ps1 \| iex` on Windows |
| [claude-ecosystem-cross-os](sota/claude-ecosystem-cross-os_2026-04-15.md) | sota | 2026-04-15 | 2026-04-22 | high | Per-OS capability matrix (Windows/macOS/Linux/iOS/Android); Claude Code Remote Control since Oct 2025; 280 verified MCP connectors; Android Termux local Claude Code; GitHub Codespaces cloud pattern; 7 wow combos identified |

| [zero-friction-bootstrap-ux](sota/zero-friction-bootstrap-ux_2026-04-16.md) | sota | 2026-04-16 | 2026-04-23 | high | v0/Bolt/Replit "one prompt" pattern, @clack/prompts wizard skeleton, Charm Gum, conversational form data (72% higher completion), progressive disclosure, cli-spinners + terminal delight |
| [gh-cli-single-click-auth](sota/gh-cli-single-click-auth_2026-04-16.md) | sota | 2026-04-16 | 2026-04-23 | high | 4-line auth revolution: `GH_BROWSER` for profile routing, `gh auth login --web` for OAuth, `gh auth setup-git` for HTTPS, `gh repo create --source=. --push` — 6 manual steps → 1 click |
| [v2_promptor_fusion_landscape](sota/v2_promptor_fusion_landscape_2026-04-17.md) | sota | 2026-04-17 | 2026-04-24 | high | Three-agent parallel research on drag-drop UX, document extraction, and conversational briefing patterns; primary source driving v1.3.x conversational-layer ships (welcome + mirror + extraction + Layer B handoff + runtime locale) and the v1.4.0 Citations API extractor |
| [anthropic-python](stack/anthropic-python_2026-04-18.md) | stack | 2026-04-18 | 2026-04-19 | medium | Anthropic Python SDK version pin for v1.4.0 Citations extractor — `anthropic>=0.40.0` minimum; documents required surface (Messages API + citations + cache_control + usage) + known March 2026 cache-TTL regression |

## Archive

- [claude-code-session-jsonl-format_2026-04-14.md](archive/claude-code-session-jsonl-format_2026-04-14.md) — superseded by the 2026-04-15 on-disk-verified entry
- [claude-code-plugin-structure_2026-04-14.md](archive/claude-code-plugin-structure_2026-04-14.md) — TTL expired 2026-04-17; structure still matches six shipped skills on disk at the time of archival, but refresh if SDK drift suspected
- [claude-code-session-jsonl-format_2026-04-15.md](archive/claude-code-session-jsonl-format_2026-04-15.md) — TTL expired 2026-04-17; on-disk-verified against v1.2.2 session, content-block type classification still accurate; refresh before any session-post-processor work that depends on record shape
