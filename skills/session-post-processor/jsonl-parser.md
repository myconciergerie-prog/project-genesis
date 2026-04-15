<!-- SPDX-License-Identifier: MIT -->
---
name: session-post-processor / jsonl-parser
description: Record-by-record walkthrough of the Claude Code session JSONL format — outer vs inner types, parentUuid threading, sidechain sub-agent handling, content-block extraction rules. Mirrors the on-disk-verified 2026-04-15 research entry; refresh in lockstep.
---

# JSONL parser

This file describes how to parse a Claude Code session JSONL transcript into an ordered, typed, turn-by-turn representation suitable for Markdown emission. The canonical schema reference is `.claude/docs/superpowers/research/stack/claude-code-session-jsonl-format_2026-04-15.md`.

## Input contract

- **File**: a single `.jsonl` file under `~/.claude/projects/<slug>/<uuid>.jsonl`
- **Shape**: one JSON object per line, each line independently valid
- **Encoding**: UTF-8
- **Crash recovery**: if the last line is partial, drop it and continue — the rest of the file is still parseable

## Top-level record shape

### First line — session metadata

```json
{"type":"<first-record-type>", "permissionMode":"<mode>", "sessionId":"<uuid>"}
```

The first line may not follow the general record shape. Parse it for `sessionId` and `permissionMode` and move on. Do not include it in the turn stream.

### Subsequent lines — message records

```json
{
  "parentUuid": "<uuid-of-previous-record-or-null>",
  "isSidechain": false,
  "type": "user" | "assistant" | "system" | "file-history-snapshot" | "attachment" | "<other>",
  "message": { ... },
  "promptId": "<uuid>",
  "timestamp": "2026-04-15T00:13:24.891Z"
}
```

**Required fields** (present on every non-metadata record):

- `type` — outer record type (see below)
- `timestamp` — ISO-8601 UTC string

**Common fields**:

- `parentUuid` — points to the previous record in the conversation thread; `null` on the first user message of the session
- `isSidechain` — `true` if this record belongs to a spawned sub-agent dialogue; `false` for the main conversation
- `message` — nested Anthropic API Message object (shape varies by outer type)
- `promptId` — UUID identifying a user prompt (on `user` records only)

## Outer type classifier

| Outer `type` | Keep in archive? | How to render |
|---|---|---|
| `user` | Yes | Turn entry — user prompt or tool_result |
| `assistant` | Yes | Turn entry — text, thinking, tool_use blocks |
| `system` | Yes | Collapsible note — hook feedback or injected reminder |
| `file-history-snapshot` | **No** | Drop entirely; internal undo state |
| `attachment` | Compress | Emit `[attachment: <name>]` marker, do not inline content |
| `summary` | Yes | Compaction marker — render as a horizontal rule + one-line summary |
| anything else | Yes (tagged) | Render as `[unknown type: <type>]` — pass-through so unseen types still show up |

The skill must not silently drop unknown outer types. Surfacing them is the only way to catch schema drift early.

## Inner content block types

On `assistant` records, `message.content` is always an **array** of content blocks:

| Inner `type` | Fields | How to render |
|---|---|---|
| `text` | `text` (string) | Plain Markdown prose |
| `thinking` | `thinking` (string), `signature` (string) | Fenced `thinking` block, collapsed by default; `signature` is internal, never render |
| `tool_use` | `id`, `name`, `input` (object) | Code block with `$ <tool> <summary>` header + JSON-formatted input |

On `user` records, `message.content` can be **either**:

- A bare string (regular user prompt) → render as a quoted Markdown blockquote
- An array of content blocks → iterate:

| Inner `type` | Fields | How to render |
|---|---|---|
| `text` | `text` (string) | Blockquote |
| `tool_result` | `tool_use_id`, `content` (string or array), `is_error` (bool) | Code block with `→ result for <tool_use_id>`; `is_error: true` gets a RED marker |

## parentUuid threading

Each record's `parentUuid` points to the record immediately before it in the logical thread. To reconstruct turn order:

1. Build a `records_by_uuid` dict: for each record, compute its UUID (from `message.id` on assistant records or `promptId` on user records) and store by that key.
2. For the ordered stream, sort all records by `timestamp` ascending. In a well-formed session this matches the `parentUuid` chain — but `timestamp` is the robust ordering key because a clock is monotonic across the session.
3. Use `parentUuid` as a sanity check: if a record claims a parent that does not exist in the `records_by_uuid` dict, log a warning but continue (a mid-write crash on the parent could have orphaned the child).

**Do not rely on `parentUuid` alone** for ordering — timestamp is the primary key.

## Sidechain sub-agent handling

When an `assistant` record has a `tool_use` block with `name: "Agent"`, the spawned sub-agent's records appear later in the same JSONL file, but with `isSidechain: true`. Their `parentUuid` chains inside the sidechain are independent of the main thread.

To group them:

1. Identify every `Agent` tool_use by its `id` (e.g. `toolu_01abc...`).
2. When a sidechain record's `parentUuid` chain eventually reaches one of those `Agent` tool_use ids (or when the first sidechain record after an `Agent` call has `parentUuid` pointing into that call's scope), associate the sidechain group with that parent Agent call.
3. In the Markdown archive, emit the sub-agent's group as an indented sub-section under the parent Agent call:

```markdown
### Agent — Explore — "Find the journal-system trigger phrases"
  - [sub-agent turn 1] ...
  - [sub-agent turn 2] ...
  - [sub-agent result] ...
```

On sessions with no sub-agent spawns, no sidechain records exist and this grouping is a no-op. The parser must still handle them correctly for sessions that do spawn.

## Tool call extraction — the hot surface

Every assistant `tool_use` block carries `name` + `input`. The parser extracts specific fields by tool name for the archive's "activity summary":

| Tool | Extract | For section |
|---|---|---|
| `Write` | `file_path`, `content` length | "Files written" |
| `Edit` | `file_path`, diff fragment | "Files edited" |
| `NotebookEdit` | `notebook_path`, cell id | "Notebooks edited" |
| `Read` | `file_path`, `offset`, `limit` | "Files inspected" |
| `Grep` / `Glob` | pattern, path | "Searches" |
| `Bash` | `command`, `description` | "Commands run" — **apply redaction before storing** |
| `Agent` | `subagent_type`, `description` | "Sub-agents spawned" |
| `TodoWrite` / `TaskCreate` / `TaskUpdate` | task content | "Task timeline" |
| `WebFetch` / `WebSearch` | URL, query | "Web accesses" |
| anything else | `name` only | "Other tool calls" |

**Never extract full tool inputs into the summary**. The full input lives in the turn-by-turn section; the summary is a rolled-up list. Avoiding duplication keeps the archive compact.

## Content-block extraction rules

### Rule 1 — Never emit signatures

`thinking` blocks have a `signature` field used by the Anthropic API for content authentication. It is internal machinery. **Never** include it in the archive. Render only the `thinking` text, nothing else from the block.

### Rule 2 — Treat empty thinking blocks as absent

Some `thinking` blocks have `thinking: ""` — the signature is present but the content is empty (cache hit, or disabled-this-turn). Skip those blocks entirely.

### Rule 3 — Bash command redaction happens before storage

Never store a raw `Bash` command in the parsed stream. Apply the redaction patterns from `redaction-patterns.md` as the command is extracted, before it enters the data structure. This ensures the "Commands run" summary and the turn-by-turn section share the same redacted text, and a bug in one emitter cannot accidentally leak from the other.

### Rule 4 — Attachment content never enters the stream

Attachments are compressed to `[attachment: <name>]` at the classifier step, before any content inspection. The parser must not read attachment bodies — they may be binary, may contain secrets, and have no place in the Markdown archive.

### Rule 5 — Unknown inner types pass through with a tag

If an assistant or user content block has an inner `type` not listed above, render it as `[unknown inner type: <type>]` — do not drop it. Schema drift is visible this way.

## Output of the parser

The parser emits a list of typed records ready for the Markdown emitter:

```python
[
  {"kind": "user_prompt", "timestamp": "...", "text": "..."},
  {"kind": "assistant_text", "timestamp": "...", "text": "..."},
  {"kind": "assistant_thinking", "timestamp": "...", "text": "..."},
  {"kind": "tool_call", "timestamp": "...", "name": "Bash", "input_summary": "...", "input_full": {...}},
  {"kind": "tool_result", "timestamp": "...", "tool_use_id": "...", "text": "...", "is_error": false},
  {"kind": "system_note", "timestamp": "...", "text": "..."},
  {"kind": "attachment_marker", "timestamp": "...", "name": "..."},
  {"kind": "sidechain_group", "timestamp": "...", "parent_tool_use_id": "...", "records": [...]},
]
```

Every string field in this output has already been through the redaction pass. The Markdown emitter consumes this list and never sees raw JSONL content.

## Error handling

- **Malformed line**: log, skip, continue. Do not abort — the rest of the transcript is still parseable.
- **Unknown outer type**: pass through with `[unknown type: <type>]` tag.
- **Unknown inner type**: pass through with `[unknown inner type: <type>]` tag.
- **Missing required field**: log a warning, best-effort render, continue.
- **Timestamp parse error**: use the previous record's timestamp + 1 ms, log a warning.

**Never raise an exception that halts the parse**. A session with one bad line is still worth archiving in the remaining 99% of its lines. The only halt condition is the Step 5 secret-leak gate — not parse errors.
