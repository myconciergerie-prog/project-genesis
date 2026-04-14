<!-- SPDX-License-Identifier: MIT -->

# hooks/

Claude Code hook files for event-driven automation. Per plugin convention, `hooks/hooks.json` (if present) is auto-loaded.

## Hook events available (Claude Code 2026)

| Event | Trigger |
|---|---|
| `PreToolUse` | Before any tool call |
| `PostToolUse` | After any tool call |
| `Stop` | User interrupts a session mid-flow |
| `SubagentStop` | A sub-agent completes |
| `SessionStart` | New Claude Code session opens |
| `SessionEnd` | Session closes (user types `fin de session` or similar) |
| `UserPromptSubmit` | User submits a prompt |
| `PreCompact` | Before context compaction |
| `Notification` | Generic notification channel |

## Planned hooks for v1.0.0

**None at v1.0.0.** Per anti-Frankenstein discipline, hook wiring is deferred until manual-mode use of the corresponding skills has been proven in practice. Automated hooks are powerful but risk side-effects when they fire in unexpected contexts — the discipline is to confirm that the manual mode works first, then add the hook as a v1.1.0 or later polish item.

## Candidate hooks for v1.1.0+

| Hook | Triggered skill | Purpose |
|---|---|---|
| `SessionEnd` | `session-post-processor` | Auto-convert the JSONL transcript to Markdown + redact + archive on session close |
| `SessionStart` | `phase-minus-one` detection | Verify the automation stack is still healthy + surface gaps |
| `Stop` | `journal-system` prompt | After a long reflective exchange, offer to capture the moment as a journal entry (consent-based) |
| `PostToolUse` on research tools | `pepite-flagging` | Scan research output for pépite red-light criteria automatically |

All of these are opt-in and gated on user consent per R10.4 anti-Frankenstein and Layer 0 consent-based amplification rules. No hook fires without the user having explicitly enabled it.

## Wiring a hook

Once a candidate hook graduates from "candidate" to "shipped", it lives in `hooks/hooks.json` in the Claude Code hook format. Users can disable individual hooks per-session via `/hooks` slash command or permanently via their local `settings.json`.
