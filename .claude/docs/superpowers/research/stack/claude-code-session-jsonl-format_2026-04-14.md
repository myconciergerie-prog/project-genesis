<!-- SPDX-License-Identifier: MIT -->
---
topic: claude-code-session-jsonl-format
type: stack
created_at: 2026-04-14
expires_at: 2026-04-15
status: active
sources:
  - https://databunny.medium.com/inside-claude-code-the-session-file-format-and-how-to-inspect-it-b9998e66d56b
  - https://github.com/simonw/claude-code-transcripts
  - https://github.com/daaain/claude-code-log
  - https://github.com/withLinda/claude-JSONL-browser
  - https://claude-world.com/tutorials/s16-session-storage/
  - https://code.claude.com/docs/en/hooks
confidence: medium
supersedes: null
---

# Claude Code Session JSONL Transcript Format — 2026 Snapshot

## Storage location

```
~/.claude/projects/<url-encoded-project-path>/
  └── <session-uuid>.jsonl
```

Where `<url-encoded-project-path>` is the project's absolute path with `\` / `:` / spaces converted to `-` or similar (e.g. `C--Dev-Claude-cowork-aurum-ai`). One `.jsonl` file per session, named by session UUID.

**Verification needed at Phase 5**: the exact on-disk layout varies between Claude Code versions. Aurum's session on 2026-04-14 appeared as `~/.claude/projects/C--Dev-Claude-cowork-aurum-ai/<uuid>.jsonl` with no `sessions/` subdir. Some 2026 sources mention a `sessions/<uuid>.jsonl` nested path. The Genesis session-post-processor skill must probe both locations and use whichever exists — do not hard-code.

## File format

- **JSONL** — one JSON object per line, each line independently valid
- Each object is a typed message record; records chain via `parentUuid` pointing to the previous message's UUID
- Crash-recovery is built in: a mid-write crash only loses the last partial line, never the whole transcript

## Message types observed

- `user` — user prompts
- `assistant` — assistant responses with content blocks (text, tool calls, thinking)
- `tool_result` — tool call outputs
- `system` — system prompts, injected reminders, hook feedback
- `summary` — periodic summary records for long sessions
- `git_snapshot` — working tree state snapshots

## Data captured per session

- Full message-by-message dialogue
- Tool calls with exact inputs and outputs
- Extended thinking blocks (when thinking mode active)
- Sub-agent spawning events
- Token usage per turn
- Model selection per turn
- Working directory and git state snapshots

## Existing post-processors (prior art for reference)

- **`simonw/claude-code-transcripts`** — Simon Willison's tooling; MIT-licensed, reference-quality, probably the cleanest schema reference available
- **`daaain/claude-code-log`** — Python CLI that converts transcripts to HTML
- **`withLinda/claude-JSONL-browser`** — web-based file explorer + Markdown conversion

**Anti-Frankenstein note**: Genesis will **not** vendor any of these as a dependency. The Genesis post-processor skill is small enough (~150-300 LoC Python) to build purposely, and its specific responsibilities (secret redaction + R8-compatible Markdown output + sessions INDEX.md update) are Genesis-specific. Prior art is cited for schema reference and comparison only.

## Application for Genesis

The `skills/session-post-processor/` skill will:

1. Locate the latest `.jsonl` file for the current project under `~/.claude/projects/<url-encoded-cwd>/`
2. Parse the JSONL stream one line at a time, classifying each record by type
3. Build an ordered turn-by-turn representation (user prompt → tool calls → tool results → assistant response)
4. Run **secret redaction** — regex pass over every string field matching known token prefixes:
   - `github_pat_` (fine-grained GitHub PAT)
   - `ghp_`, `gho_`, `ghu_`, `ghs_`, `ghr_` (classic GitHub tokens)
   - `sbp_` (Supabase PAT)
   - `sb_secret_`, `sb_publishable_` (Supabase keys)
   - `sk_`, `pk_` (Stripe-style keys)
   - JWT-shaped strings (`eyJ...`)
   - `AKIA`, `ASIA` (AWS access key prefixes)
   - Replace matches with `[REDACTED:<pattern-name>]`
5. Emit a Markdown transcript to `.claude/docs/superpowers/sessions/YYYY-MM-DD_<session-name>.md` with frontmatter (session name, UUID, start/end timestamps, participants, commits touched, journal entries created)
6. Append a one-line entry to `.claude/docs/superpowers/sessions/INDEX.md`
7. Optional: wire to a `SessionEnd` hook in `hooks/hooks.json` for auto-run — **only after manual use has validated the approach** (anti-Frankenstein: don't auto-wire before the manual mode is proven)
