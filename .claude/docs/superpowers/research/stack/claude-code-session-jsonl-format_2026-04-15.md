<!-- SPDX-License-Identifier: MIT -->
---
topic: claude-code-session-jsonl-format
type: stack
created_at: 2026-04-15
expires_at: 2026-04-16
status: active
sources:
  - https://databunny.medium.com/inside-claude-code-the-session-file-format-and-how-to-inspect-it-b9998e66d56b
  - https://github.com/simonw/claude-code-transcripts
  - https://github.com/daaain/claude-code-log
  - https://github.com/withLinda/claude-JSONL-browser
  - local-verified-2026-04-15 — C:/Users/conta/.claude/projects/C--Dev-Claude-cowork-project-genesis/a086701e-2ef2-4194-98af-74549dc763e4.jsonl
confidence: high
supersedes: .claude/docs/superpowers/research/stack/claude-code-session-jsonl-format_2026-04-14.md
---

# Claude Code Session JSONL Transcript Format — 2026-04-15 Verified Snapshot

This entry **supersedes** `claude-code-session-jsonl-format_2026-04-14.md` with on-disk verification against a real Claude Opus 4.6 session file from 2026-04-15. Confidence upgraded from `medium` to `high`.

## Storage location — verified

```
~/.claude/projects/<url-encoded-absolute-path>/<session-uuid>.jsonl
```

- **Flat layout confirmed**. No `sessions/` subdirectory on this machine. The `session-post-processor` skill can target the flat path directly, but should still probe for a nested path as a safety net because older or alternate Claude Code builds may differ.
- **URL-encoding rule**: replace every `\`, `:`, and space in the absolute path with `-`. Drive-letter colon also becomes `-`. Example: `C:\Dev\Claude_cowork\project-genesis` → `C--Dev-Claude-cowork-project-genesis` (double dash after `C` reflects `C:` → `C-` and then `\` → `-`, which collapse to `--`).
- **One project can have multiple slugs** — verified on this machine. `project-genesis` had both `C--Dev-Claude-cowork-project-genesis/` (current) and `C--Dev-Claude-cowork-project-genesis-2026/` (prior path before rename). The skill must pick the slug matching the current `cwd`, and should surface any sibling slugs as a YELLOW health warning so the user can decide whether to archive or merge them.
- **Files are named `<session-uuid>.jsonl`** — UUID v4, one file per Claude Code session.

## Verified file-level shape

Every line of the JSONL is a single valid JSON object. Lines are independently parseable — a mid-write crash loses only the last partial line.

**First line** of any session carries session metadata only:

```json
{"type":"...", "permissionMode":"...", "sessionId":"<uuid>"}
```

Subsequent lines are **message records** with the following top-level shape:

```json
{
  "parentUuid": "<uuid-of-previous-message-or-null>",
  "isSidechain": false,
  "type": "user" | "assistant" | "system" | "file-history-snapshot" | "attachment" | ...,
  "message": { ...Anthropic API Message... },
  "promptId": "<uuid>",           // on user messages only
  "timestamp": "ISO-8601-UTC"
}
```

The nested `message` field is shaped exactly like an Anthropic API `Message` object (role + content blocks).

## Outer record types — verified

From the sample session (`a086701e-2ef2-4194-98af-74549dc763e4.jsonl`, 174 records):

| Outer `type` | Count | Meaning |
|---|---|---|
| `user` | 66 | User messages or tool-result submissions back to the assistant |
| `assistant` | 82 | Assistant responses (text, thinking, tool calls) |
| `system` | 2 | Hook feedback, injected reminders, permission prompts |
| `file-history-snapshot` | 14 | Periodic working-tree backup state for undo / rewind |
| `attachment` | 7 | Inline images, files, or other binary attachments |

**Not observed in this session** but documented in prior art: `summary` (periodic long-session compaction marker), `git_snapshot` (working tree snapshots). The skill must handle unknown outer types gracefully — classify as `other` and pass through.

## Nested content block types — inside `message.content[]`

The `message.content` array on `assistant` records contains typed blocks:

| Inner `type` | Count | Meaning |
|---|---|---|
| `text` | 22 | Plain assistant prose visible to the user |
| `thinking` | 6 | Extended thinking blocks (present only when thinking mode is enabled on the turn) |
| `tool_use` | 65 | Tool invocation — has `name`, `input`, `id` |

On `user` records, content blocks include:

| Inner `type` | Meaning |
|---|---|
| `tool_result` | Output of a tool call, linked by `tool_use_id` back to the assistant's `tool_use` block |
| plain string | Regular user prompt (the `content` field is a string, not an array, in this case) |

User messages can have `content` as a **bare string** or as an **array of content blocks** — the parser must handle both.

## Tool call fields

Every `assistant` `tool_use` content block has:

```json
{
  "type": "tool_use",
  "id": "toolu_<id>",
  "name": "Bash" | "Read" | "Edit" | "Write" | "Grep" | "Glob" | "Agent" | ...,
  "input": { ...tool-specific params... }
}
```

For the `session-post-processor`, the tool names and inputs are the hot surface — they determine the event narrative in the emitted Markdown archive. Specifically:

- `Write` / `Edit` / `NotebookEdit` — extract `file_path` to build the "files touched" list
- `Bash` — extract `command` + `description` to build the "commands run" list (with redaction — a `git commit`, `gh pr create`, or `env` command can leak tokens)
- `Read` / `Grep` / `Glob` — extract path / pattern for "files inspected"
- `Agent` — extract `subagent_type` + `description` for "sub-agents spawned"
- `TodoWrite` / `TaskCreate` / `TaskUpdate` — extract task content for the chronological task timeline

## Timestamps

Every record except the session-metadata first line carries `timestamp` as an ISO-8601 UTC string (`"2026-04-15T00:13:24.891Z"`). The skill converts to local time for display in the Markdown archive, using the user's system timezone.

**Session start** = first record's timestamp (after the metadata line).
**Session end** = last record's timestamp.
**Duration** = difference; surface in the archive's frontmatter.

## Token usage

`assistant` records carry `message.usage`:

```json
{
  "input_tokens": N,
  "output_tokens": N,
  "cache_creation_input_tokens": N,
  "cache_read_input_tokens": N
}
```

Summing across all assistant records gives per-session token spend — useful to surface in the archive frontmatter as a cost proxy, but **not** surfaced to downstream users because it can reveal prompt-cache patterns. Keep it in the frontmatter only, gated by a `include_usage_stats: true` flag in the skill's config.

## Sidechain records

`isSidechain: true` marks records belonging to a spawned sub-agent (Task/Agent tool invocation). These carry their own threaded dialogue. The skill should group sidechain records by their parent `Agent` tool_use_id and emit them as indented sub-sections in the Markdown archive.

On the sample session, `isSidechain` was `false` on every record — no sub-agents were spawned. The skill must still handle sidechains correctly for sessions that do spawn agents (the v1 bootstrap session did, per its file-history record count).

## `file-history-snapshot` records

```json
{
  "type": "file-history-snapshot",
  "messageId": "<uuid>",
  "snapshot": {
    "messageId": "<uuid>",
    "trackedFileBackups": { ...path → backup mapping... },
    "timestamp": "ISO-8601-UTC"
  },
  "isSnapshotUpdate": false
}
```

These are the undo-rewind state, not user-visible content. The skill can **skip them entirely** in the Markdown archive — their only value is machine-level rollback and they leak internal state (tracked file paths) that adds noise.

## `attachment` records

Attachments (images, files) pointed to external content. The skill should:

- Emit a one-line `[attachment: <name> · <type>]` marker in the Markdown archive
- **Not** inline the binary content (waste of space, and may contain secrets)
- **Not** copy the attachment to the archive directory — reference-only

## Application for Genesis `session-post-processor`

The skill's pipeline:

1. **Locate** — find the latest `<uuid>.jsonl` under `~/.claude/projects/<slugified-cwd>/`, using `os.path.getmtime` for recency
2. **Parse** — stream the file line by line, `json.loads` each line, classify by outer `type`
3. **Group** — walk `parentUuid` chain to reconstruct turn-by-turn ordering
4. **Filter** — drop `file-history-snapshot` records entirely; compress `attachment` records to markers
5. **Redact** — regex pass over every string field against the secret pattern set (see `redaction-patterns.md` in the skill)
6. **Emit** — write `memory/project/sessions/YYYY-MM-DD_<session-slug>.md` with frontmatter (session UUID, start/end timestamps, total turns, tool call counts, redaction hit counts) + chronological turn-by-turn Markdown
7. **Index** — append / update a line in `memory/project/sessions/INDEX.md`
8. **Verify** — run the secret-leak check (grep the output against the pattern set); if any hit passes through, the write is RED and the file is deleted before the skill returns

## Anti-Frankenstein note

Do **not** vendor `simonw/claude-code-transcripts` or `daaain/claude-code-log` as dependencies. The Genesis skill's specific responsibilities — secret redaction with Genesis-specific patterns, Markdown output tuned for `memory/project/sessions/`, and the halt-on-leak verification gate — are small enough to build purposely. Prior art is cited for schema reference and schema-validation diff only.

## What the v0.4.0 JSONL evidence confirms vs the 2026-04-14 entry

| Claim in v0.4.14 entry | Verified on 2026-04-15? | Notes |
|---|---|---|
| Flat `~/.claude/projects/<slug>/<uuid>.jsonl` | ✅ | No `sessions/` subdir on this machine |
| One file per session | ✅ | Matches |
| One JSON object per line | ✅ | Matches |
| Message types: user, assistant, tool_result, system, summary, git_snapshot | ⚠️ Partial | `user`, `assistant`, `system` verified. `tool_result` is an **inner** content block type, not an outer record type. `summary` and `git_snapshot` not observed but documented in prior art. **New outer types** observed: `file-history-snapshot`, `attachment`. |
| `parentUuid` chain for threading | ✅ | Every record has a `parentUuid` field |
| Sub-agent events | ⚠️ Revised | Sub-agent dialogue is marked via `isSidechain: true`, not a separate outer type |
| Token usage per turn | ✅ | In `message.usage` on assistant records |
| Model selection per turn | ✅ | In `message.model` on assistant records |
| Working directory / git state snapshots | ⚠️ Revised | Not in the JSONL itself; the `file-history-snapshot` records capture tracked-file backups, not cwd or git HEAD |

**Biggest revision**: the inner vs outer type distinction. The v0.4.14 entry conflated them. The skill's parser must handle both levels: classify records by outer `type`, then walk `message.content[]` blocks by inner `type`.

## TTL and next refresh

This entry's TTL is 1 day (`stack/` category). It expires 2026-04-16. The next refresh should:

1. Verify the slug derivation rule is still `\|:|space → -` (Claude Code may change the encoding)
2. Confirm flat vs nested layout (Claude Code may introduce a `sessions/` subdir)
3. Check whether any new outer record types have been introduced (they would appear in the `type:` count of a fresh session)

The `session-post-processor` skill itself is a natural refresh tool once shipped — running it against the latest session regenerates this entry's verification data for free.
