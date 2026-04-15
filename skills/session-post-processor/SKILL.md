<!-- SPDX-License-Identifier: MIT -->
---
name: session-post-processor
description: Parse the current Claude Code session's JSONL transcript, redact secrets (GitHub PATs, SSH private keys, API tokens, `.env.local` content), and emit a readable Markdown archive under `memory/project/sessions/YYYY-MM-DD_<slug>.md`. Halt-on-leak verification gate. Manual-invoke only — never wire to a `SessionEnd` hook until the manual mode has been dogfooded across at least three real sessions.
---

# Session post-processor

This skill converts a Claude Code session JSONL transcript into a human-readable Markdown archive, with mandatory secret redaction and a halt-on-leak verification gate. It runs **manually** — the user invokes it when a session is complete and they want a durable record in version-controlled memory.

**Canonical JSONL format reference**: `.claude/docs/superpowers/research/stack/claude-code-session-jsonl-format_2026-04-15.md` (on-disk verified against `a086701e.jsonl` on 2026-04-15, supersedes the 2026-04-14 entry).

## Why manual-only for v0.5.0

The Genesis 2026-04-14 Layer 0 rules explicitly defer `SessionEnd` hook wiring until a skill has been **dogfooded in manual mode across at least three real sessions**. A malformed archive or a redaction miss is a data leak if it auto-runs on every session close. Manual invocation means the user is in the loop, inspects the output, and can abort or re-run before any commit.

The first `session-post-processor` hook wiring is a v0.6+ candidate only after:

1. The skill has successfully archived at least three Genesis sessions
2. Every archive has passed the halt-on-leak gate
3. The user has manually reviewed at least one archive end-to-end and confirmed the redaction set catches their actual patterns

## When to invoke

- The user types `/session-post-processor`.
- The user says any of:
  - "archive this session"
  - "process the session"
  - "run the session archiver"
  - "write the session memory from the transcript"
  - "dump the jsonl to markdown"
- The Genesis protocol orchestrator invokes this skill at the end of a session, **only after** v0.6+ wires it via hook (not in v0.5).

**Do not auto-run** in v0.5. The first run on each session is always user-triggered.

## Prerequisites

- The current session's JSONL file exists at `~/.claude/projects/<slugified-cwd>/<session-uuid>.jsonl`. The skill locates it via `mtime` on the most recent `.jsonl` in that directory.
- The target project has a `memory/project/sessions/` directory. The `install-manifest.yaml` step creates it if missing and seeds `INDEX.md`.
- **Python 3.10+** is available on the machine — the skill's pipeline is small but depends on `json`, `re`, `os`, `pathlib`, and `datetime` from the standard library. No pip dependencies.

## The flow — seven steps

### Step 1 — Locate the target JSONL

Compute the current project's slug by applying the verified rule: replace every `\`, `:`, and space in the absolute cwd path with `-`. Drive-letter colon also becomes `-`.

Example:
```
cwd = C:\Dev\Claude_cowork\project-genesis
slug = C--Dev-Claude-cowork-project-genesis
path = ~/.claude/projects/C--Dev-Claude-cowork-project-genesis/
```

Find the `.jsonl` file in that directory with the most recent `mtime`. That is the current session.

If the directory does not exist, stop and surface an error — the session has no transcript to process. If multiple JSONL files exist and the user did not specify which, offer the three most recent by mtime and ask for a pick.

### Step 2 — Parse the JSONL stream

Read the file line by line. Each line is a standalone JSON object. Skip the first line if it contains only session metadata (`{"type":"...", "permissionMode":"...", "sessionId":"<uuid>"}`). Classify every subsequent record by its outer `type`:

- `user` — user prompt or tool_result submission
- `assistant` — assistant response (thinking, text, tool_use)
- `system` — hook feedback, injected reminders
- `file-history-snapshot` — undo/rewind state → **drop entirely**
- `attachment` — inline file / image → compress to `[attachment: <name>]` marker
- anything else → classify as `other`, pass through

Walk `parentUuid` chains to reconstruct turn order. See `jsonl-parser.md` for the full schema walkthrough.

### Step 3 — Run the redaction pass

For every string field in every record, apply the regex patterns from `redaction-patterns.md`. Replace any match with `[REDACTED:<pattern-name>]`. Count hits per pattern and log them (counts only — never the matched values).

**Never log the matched secret**, even in debug output. The redaction pass is append-only — it never writes the raw secret to any output, not even temporarily. If the pattern matcher needs to verify its own match, it verifies the pattern tag, not the payload.

See `redaction-patterns.md` for the full pattern list and rationale.

### Step 4 — Emit the Markdown archive

Render the redacted, parsed records as a Markdown document per the template in `markdown-emitter.md`. Output path:

```
memory/project/sessions/<YYYY-MM-DD>_<session-slug>.md
```

Where `<session-slug>` is derived from:
1. The first user message's first non-empty sentence, slugified (< 50 chars)
2. Or, if the first message is empty / ambiguous, the session UUID's first 8 chars

If the target file already exists (same date + slug), append `-2`, `-3`, etc. Never overwrite silently.

### Step 5 — Run the halt-on-leak verification

After the emit, **re-read the written file** and grep it against the full redaction pattern set. If **any** pattern matches the output, the verification is **RED**:

1. Log the pattern that leaked (name only, not the match)
2. **Delete the written file** immediately
3. Surface the incident to the user with a clear message: *"Archive halted — pattern `<name>` leaked through redaction. File deleted. Do not retry until the redaction set is audited and strengthened."*
4. **Do not retry automatically**. A silent retry would hide the leak. The user must audit the pattern set and re-invoke the skill.

The halt gate is the skill's security floor. It is the difference between "best-effort redaction" and "verified-before-write".

### Step 6 — Update the sessions INDEX

If the archive passed Step 5, append (or update) a one-line entry to `memory/project/sessions/INDEX.md`:

```markdown
- [2026-04-15 — <session title>](2026-04-15_<slug>.md) — <duration> · <tool-call count> · <redaction hit count>
```

The duration, tool-call count, and redaction hit count come from the parse step. If a line for the same file already exists, update it in place — do not duplicate.

### Step 7 — Emit the health card

Run the post-action verification per `verification.md` and emit the GREEN / YELLOW / RED health card. The user reads the card, confirms GREEN, and the skill exits.

## Manual testing for v0.5.0 before any hook wiring

Before the skill is wired to a `SessionEnd` hook (v0.6+ candidate), it must pass these three dogfood runs:

1. **Run 1**: this very v0.5.0 session. The skill archives the session that shipped it (recursive dogfood). Manual review of the output; any redaction miss or formatting issue is fixed before merge.
2. **Run 2**: a second Genesis session (v0.6 or later). Re-run the skill manually; confirm it still passes the gate on a different session shape.
3. **Run 3**: an Aurum session (after the Aurum freeze lifts), to confirm the skill works outside Project Genesis and the slug derivation rule handles a different cwd path.

Only after all three pass cleanly is hook wiring permitted. This is the anti-Frankenstein guard — no auto-run before proof.

## Files in this skill

| File | Purpose |
|---|---|
| `SKILL.md` | This entry point — trigger, seven-step flow, manual-only discipline |
| `jsonl-parser.md` | Record type walkthrough, parentUuid threading, sidechain handling, content-block extraction |
| `redaction-patterns.md` | The full regex pattern set with rationale per pattern and test vectors |
| `markdown-emitter.md` | Output template — frontmatter, turn-by-turn layout, code block handling |
| `install-manifest.yaml` | Creates `memory/project/sessions/` + starter `INDEX.md`, declares Python 3.10+ requirement |
| `verification.md` | Health card — two modes (post-install + post-action), halt-on-RED guard |

## Anti-Frankenstein reminders

- **Do not wire SessionEnd hooks** in v0.5. Hook wiring is a v0.6+ candidate after three successful manual dogfood runs.
- **Do not vendor external JSONL parsers** (`simonw/claude-code-transcripts`, `daaain/claude-code-log`, `withLinda/claude-JSONL-browser`). The skill's pipeline is small enough to build purposely and its redaction patterns are Genesis-specific.
- **Do not retry on a halted archive**. A silent retry hides leaks. The user must audit and re-invoke.
- **Do not include `file-history-snapshot` content** in the archive — it adds noise and leaks internal file paths.
- **Do not include `message.usage`** in user-visible sections. Keep it in frontmatter only, gated by an explicit flag.
- **Do not emit raw `message.content` arrays** — always reconstruct them as human-readable prose and fenced code blocks.
- **If the user says `frankenstein`**, back out of the last proposal.

## What this skill does NOT do

- **Cross-session aggregation** — no timeline across all sessions. This skill archives one session at a time. A future `session-timeline` skill could aggregate archives once there are enough to be worth aggregating.
- **Semantic indexing** — no embedding, no similarity search. The archive is plain Markdown; `grep` and `ripgrep` are the search tools.
- **Interactive replay** — the archive is read-only Markdown. A future `session-replay` skill could re-inject the records into a new Claude Code session, but that is out of scope here.
- **Token usage dashboards** — token counts go in frontmatter behind a flag, not in a user-facing dashboard.
- **Automatic anonymisation of file paths** — paths are not secrets and are left in place (they are already local-only). Only credentials and keys are redacted.
- **Retroactive re-processing** — the skill operates on the current session only. Batch re-processing of old JSONL files is deferred.
