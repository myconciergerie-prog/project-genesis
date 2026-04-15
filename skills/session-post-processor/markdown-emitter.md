<!-- SPDX-License-Identifier: MIT -->
---
name: session-post-processor / markdown-emitter
description: Template and rendering rules for the Markdown archive emitted by the skill. Consumes the typed record list from jsonl-parser.md, emits a single Markdown file under memory/project/sessions/YYYY-MM-DD_<slug>.md.
---

# Markdown emitter

The emitter takes the typed, redacted record list from the parser and writes a single Markdown file. This file describes the output layout and the rendering rules for each record kind.

## Output file path

```
memory/project/sessions/<YYYY-MM-DD>_<session-slug>.md
```

Where:

- `<YYYY-MM-DD>` is the session's **start** date in the user's local timezone
- `<session-slug>` is derived from the first user message's first non-empty sentence, slugified to < 50 chars (lowercase, accents stripped, non-alphanumerics → hyphens, leading/trailing hyphens stripped); or `<uuid>[:8]` if the first message is empty or generic

If the target path already exists, append `-2`, `-3`, etc. **Never overwrite silently**. A re-run on an already-archived session should produce a new file, and the user can diff the two to confirm the redaction set is still effective.

## Archive file structure

```markdown
<!-- SPDX-License-Identifier: MIT -->
---
name: <session-slug>
description: <one-line summary — first user message's first sentence, truncated to 120 chars>
type: session-archive
session_uuid: <full-session-uuid>
project_slug: <slugified-cwd>
project_cwd: <original-absolute-path>
start_time: <ISO-8601 local>
end_time: <ISO-8601 local>
duration: <humanised — "1h 27m" or "43m">
tool_calls_total: <N>
tool_calls_by_name:
  Bash: N
  Write: N
  Edit: N
  Read: N
  Grep: N
  ...
files_written: <N>
files_edited: <N>
sub_agents_spawned: <N>
redaction_hits_total: <N>
redaction_hits_by_pattern:
  github_pat_finegrained: N
  env_local_paste: N
  ...
include_usage_stats: false    # set to true to include token counts below
# --- optional, only if include_usage_stats: true ---
# input_tokens: N
# output_tokens: N
# cache_read_tokens: N
# cache_creation_tokens: N
---

# Session archive — <session-slug>

## Session metadata

- **Session UUID**: `<uuid>`
- **Project**: `<project-slug>` (`<absolute-path>`)
- **Started**: <YYYY-MM-DD HH:MM local>
- **Ended**: <YYYY-MM-DD HH:MM local>
- **Duration**: <humanised>
- **Permission mode**: <from first-line metadata>

## Activity summary

### Tool calls

| Tool | Count |
|---|---|
| Bash | N |
| Write | N |
| Edit | N |
| Read | N |
| ... | ... |

### Files written

- `<path>` — N calls
- `<path>` — N calls

### Files edited

- `<path>` — N calls

### Sub-agents spawned

- `Explore` — "<description>" (N turns inside sidechain)
- `Plan` — "<description>"

### Commands run (redacted)

- `git status -s` — "Check working tree state"
- `git commit -m "..."` — "First granular commit"
- `GH_TOKEN=[REDACTED:env_local_paste] gh pr create ...` — "Open PR via token env override"

### Redaction report

| Pattern | Hit count |
|---|---|
| github_pat_finegrained | N |
| env_local_paste | N |
| jwt_token | N |

Total: **N** redactions across the session.

## Turn-by-turn transcript

### Turn 1 — user · <HH:MM:SS>

> <the user's first message, in a blockquote>

### Turn 2 — assistant · <HH:MM:SS>

<assistant's text response as plain markdown prose>

<details>
<summary>Thinking (click to expand)</summary>

<thinking block content, if present and non-empty>
</details>

```bash
$ Bash — "<description>"
<redacted command>
```

### Turn 3 — user (tool result) · <HH:MM:SS>

```
→ result for toolu_01abc... (success)
<tool output, truncated to 40 lines with "... (N more lines)" marker if longer>
```

### Turn 4 — assistant · <HH:MM:SS>

<more prose>

```python
$ Write — "<description>"
file_path: <path>
size: <N> bytes
```

### Sub-agent: Explore — "Find the journal-system trigger phrases"

<indented sub-section; each sidechain turn rendered same as main turns but offset by two spaces and prefixed with `sub:`>

> sub: <sub-agent turn>

<sub: assistant reply>

(... end of sub-agent section ...)

## End of archive

Session ended at <HH:MM local>.
```

## Rendering rules per record kind

### `user_prompt`

Render as a Markdown blockquote:

```
### Turn N — user · HH:MM:SS

> <text>
```

If the text is long (> 500 chars), keep the first 500 chars and append `… <N more chars>`. Truncation never affects redaction — the full message was already redacted before this step.

### `assistant_text`

Render as plain prose, no blockquote:

```
### Turn N — assistant · HH:MM:SS

<text>
```

### `assistant_thinking`

Render inside a collapsed `<details>` block:

```
<details>
<summary>Thinking (click to expand)</summary>

<thinking text>
</details>
```

If thinking text is empty, skip the block entirely. **Never emit the `signature` field** — it is internal.

### `tool_call`

Render as a fenced code block with a pseudo-shell-prompt header:

```
$ <name> — "<description or short input summary>"
<key fields from input, one per line, truncated>
```

Fences use the language matching the tool where it makes sense:
- `Bash` → `bash`
- `Read` / `Write` / `Edit` → `diff`
- `Grep` / `Glob` → `plaintext`
- default → `plaintext`

The tool_call summary is brief — it does **not** embed the full `input_full` dict. The full input is retrievable from the source JSONL if needed; the archive is a summary.

### `tool_result`

Render as a fenced code block with a result header:

```
→ result for <tool_use_id> (<success|error>)
<text, truncated to 40 lines>
```

If more than 40 lines, append `… (N more lines)`. If `is_error: true`, prefix the header with `[ERROR]` and highlight it.

### `system_note`

Render as a small italicised note:

```
_system: <text>_
```

Collapse consecutive system notes into a single block if they are adjacent — multiple hook-feedback events back-to-back are noise otherwise.

### `attachment_marker`

Render as a one-line marker:

```
[attachment: <name>]
```

Never try to embed the content.

### `sidechain_group`

Render as an indented sub-section under the parent `tool_call` turn:

```
### Turn N — assistant · HH:MM:SS

[prose + Agent tool call as usual]

#### Sub-agent: <agent type> — "<description>"

> sub: <first turn>

<sub: reply>

(... sub-agent turns, rendered with "sub: " prefix ...)

#### End of sub-agent group
```

A missing sidechain group (no sub-agent spawned) is a no-op — the parent turn renders normally.

## Truncation rules

### Per-message

- User prompts longer than **500 chars** are truncated with a marker
- Tool results longer than **40 lines** are truncated with a marker
- Assistant text blocks are not truncated (they are the substance of the archive)

### Per-file

- The final archive has no hard size limit — a long session produces a long archive
- Consecutive identical system notes are collapsed (see rendering rule)
- File-history-snapshot records are dropped entirely by the parser; they never reach the emitter

## Frontmatter computation

The emitter computes the frontmatter fields from the parsed record list:

- `tool_calls_total` = count of `tool_call` records
- `tool_calls_by_name` = histogram of `name` field across `tool_call` records
- `files_written` = count of distinct `file_path` values on `Write` tool_calls
- `files_edited` = count of distinct `file_path` values on `Edit` tool_calls
- `sub_agents_spawned` = count of `tool_call` records with `name == "Agent"`
- `redaction_hits_total` = sum of hit counts across all patterns
- `redaction_hits_by_pattern` = full hit-count histogram
- `duration` = end_time - start_time, humanised

`include_usage_stats: false` is the default — keep it false unless the user explicitly asks for token stats. This avoids surfacing cache-hit patterns that reveal prompt structure.

## Idempotency rules

A re-run on the same session produces a new file with a `-N` suffix. The skill does **not** update the existing file. This way:

- The user can diff the two runs to confirm redaction stability
- A new redaction pattern added between runs will produce different output, and the diff makes it visible
- The halt-on-leak gate runs on every invocation, so a re-run of a previously-passing session re-verifies with the current pattern set

## What the emitter does NOT do

- **Interactive HTML output** — this is plain Markdown for version control; a separate `session-replay-viewer` skill could render to HTML later
- **Inlined images from attachments** — attachments are markers only
- **Embedded full JSONL as a backup** — the archive is a summary; the source JSONL lives in `~/.claude/projects/` for retrieval
- **Cross-linking between archives** — no hyperlinks to other session files; a `session-timeline` aggregator is deferred
- **User-message editing** — the user's words are preserved exactly as they were (same rule as the journal system)
- **Machine-readable session stats export** — the frontmatter is the full machine-readable view; no separate JSON export
