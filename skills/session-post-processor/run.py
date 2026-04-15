# SPDX-License-Identifier: MIT
"""session-post-processor / run.py

Executable entry point for the `session-post-processor` Genesis skill. Parses
a Claude Code session JSONL transcript, redacts secrets via the frozen regex
set, emits a Markdown archive under `memory/project/sessions/`, and runs a
halt-on-leak verification gate that deletes the archive if any pattern
re-matches the written file.

Only the Python 3.10+ standard library is used — `json`, `re`, `os`,
`pathlib`, `datetime`, `argparse`, `sys`, `unicodedata`. No pip installs.

Canonical spec:
  skills/session-post-processor/SKILL.md
  skills/session-post-processor/jsonl-parser.md
  skills/session-post-processor/redaction-patterns.md
  skills/session-post-processor/markdown-emitter.md
  skills/session-post-processor/verification.md

Manual-invoke only. DO NOT wire to a `SessionEnd` hook until three real
manual dogfood runs have passed the halt-on-leak gate.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path


# ---------------------------------------------------------------------------
# Redaction patterns — frozen order, specific before generic
# ---------------------------------------------------------------------------

REDACTION_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    (
        "ssh_private_key_block",
        re.compile(
            r"-----BEGIN (OPENSSH|RSA|DSA|EC|ED25519) PRIVATE KEY-----"
            r".*?-----END \1 PRIVATE KEY-----",
            re.DOTALL,
        ),
    ),
    ("github_pat_finegrained", re.compile(r"\bgithub_pat_[A-Za-z0-9_]{82,}\b")),
    ("github_classic_token", re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{36,}\b")),
    ("anthropic_api_key", re.compile(r"\bsk-ant-[a-zA-Z0-9\-_]{32,}\b")),
    ("openai_api_key", re.compile(r"\bsk-(?:proj-)?[a-zA-Z0-9\-_]{32,}\b")),
    ("supabase_pat", re.compile(r"\bsbp_[a-f0-9]{40,}\b")),
    ("supabase_secret_key", re.compile(r"\bsb_secret_[A-Za-z0-9_\-]{32,}\b")),
    ("stripe_secret_key", re.compile(r"\bsk_(?:test|live)_[A-Za-z0-9]{24,}\b")),
    (
        "aws_access_key",
        re.compile(
            r"\b(?:AKIA|ASIA|AIDA|ABIA|ACCA|AIPA|ANPA|ANVA|AROA|APKA|ASCA)"
            r"[A-Z0-9]{16}\b"
        ),
    ),
    ("google_api_key", re.compile(r"\bAIza[0-9A-Za-z\-_]{35}\b")),
    (
        "jwt_token",
        re.compile(r"\beyJ[A-Za-z0-9_\-]{10,}\.eyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}\b"),
    ),
    (
        "env_local_paste",
        re.compile(
            r"(?m)^\s*(GH_TOKEN|GITHUB_TOKEN|API_KEY|SECRET|PRIVATE_KEY|PASSWORD"
            r"|DB_PASS|DB_PASSWORD|DATABASE_URL|ANTHROPIC_API_KEY|OPENAI_API_KEY"
            r"|SUPABASE_SERVICE_KEY|STRIPE_SECRET)\s*=\s*.+$"
        ),
    ),
    ("generic_long_hex", re.compile(r"\b[a-f0-9]{64,}\b")),
    ("generic_long_base64", re.compile(r"\b[A-Za-z0-9+/]{40,}={0,2}\b")),
]

PATTERN_NAMES = [name for name, _ in REDACTION_PATTERNS]


def redact(text: str, counter: dict[str, int]) -> str:
    """Apply the frozen pattern set to `text`, counting hits per pattern.

    `env_local_paste` gets special handling: keep the variable name, replace
    only the value. Every other pattern is a plain `[REDACTED:<name>]` swap.
    """
    if not text:
        return text
    for name, pattern in REDACTION_PATTERNS:
        if name == "env_local_paste":
            def replace_env(match: re.Match[str], _name: str = name) -> str:
                counter[_name] = counter.get(_name, 0) + 1
                return f"{match.group(1)}=[REDACTED:{_name}]"
            text = pattern.sub(replace_env, text)
        else:
            def replace_generic(match: re.Match[str], _name: str = name) -> str:
                counter[_name] = counter.get(_name, 0) + 1
                return f"[REDACTED:{_name}]"
            text = pattern.sub(replace_generic, text)
    return text


# ---------------------------------------------------------------------------
# Slug derivation
# ---------------------------------------------------------------------------

def slugify_cwd(cwd: str) -> str:
    """Replace `\\`, `/`, `:`, `_`, and space with `-` (on-disk verified rule)."""
    out = []
    for ch in cwd:
        if ch in ("\\", "/", ":", "_", " "):
            out.append("-")
        else:
            out.append(ch)
    return "".join(out)


def slugify_title(title: str, max_len: int = 50) -> str:
    """Title → lowercase, ASCII, non-alphanumeric → hyphen, trimmed."""
    if not title:
        return ""
    nfkd = unicodedata.normalize("NFKD", title)
    ascii_only = nfkd.encode("ascii", "ignore").decode("ascii")
    lowered = ascii_only.lower()
    hyphenated = re.sub(r"[^a-z0-9]+", "-", lowered).strip("-")
    if len(hyphenated) > max_len:
        hyphenated = hyphenated[:max_len].rstrip("-")
    return hyphenated


# ---------------------------------------------------------------------------
# Parser — JSONL → typed record list
# ---------------------------------------------------------------------------

def locate_source_jsonl(cwd: str, explicit: Path | None = None) -> Path:
    """Find the most recent JSONL for the given cwd slug, or use an override."""
    if explicit is not None:
        if not explicit.exists():
            raise FileNotFoundError(f"Explicit JSONL not found: {explicit}")
        return explicit
    slug = slugify_cwd(cwd)
    projects_root = Path.home() / ".claude" / "projects" / slug
    if not projects_root.exists():
        raise FileNotFoundError(
            f"No session directory for slug `{slug}` under {projects_root.parent}. "
            f"Either the session has no JSONL yet or the slug derivation is wrong."
        )
    jsonls = sorted(
        projects_root.glob("*.jsonl"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    if not jsonls:
        raise FileNotFoundError(f"No .jsonl files under {projects_root}.")
    return jsonls[0]


def parse_timestamp(ts: str | None, fallback: datetime | None) -> datetime:
    """ISO-8601 UTC → aware datetime. Fallback + 1 ms on failure."""
    if ts is None:
        return (fallback or datetime.now(timezone.utc))
    try:
        parsed = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed
    except (ValueError, TypeError):
        return (fallback or datetime.now(timezone.utc))


def extract_content_blocks(msg: dict, counter: dict[str, int]) -> list[dict]:
    """Flatten message.content into typed block dicts with redaction applied."""
    if not isinstance(msg, dict):
        return []
    content = msg.get("content")
    if content is None:
        return []
    if isinstance(content, str):
        return [{"kind": "text", "text": redact(content, counter)}]
    if not isinstance(content, list):
        return [{"kind": "unknown_inner", "text": f"[unknown inner shape: {type(content).__name__}]"}]

    blocks: list[dict] = []
    for block in content:
        if not isinstance(block, dict):
            continue
        btype = block.get("type", "unknown")
        if btype == "text":
            blocks.append({"kind": "text", "text": redact(block.get("text", ""), counter)})
        elif btype == "thinking":
            thinking_text = block.get("thinking") or ""
            if thinking_text.strip():
                blocks.append({"kind": "thinking", "text": redact(thinking_text, counter)})
        elif btype == "tool_use":
            name = block.get("name", "unknown")
            tool_input = block.get("input", {}) or {}
            blocks.append({
                "kind": "tool_call",
                "id": block.get("id", ""),
                "name": name,
                "input": redact_dict(tool_input, counter),
            })
        elif btype == "tool_result":
            raw = block.get("content", "")
            if isinstance(raw, list):
                parts: list[str] = []
                for item in raw:
                    if isinstance(item, dict) and item.get("type") == "text":
                        parts.append(item.get("text", ""))
                    elif isinstance(item, str):
                        parts.append(item)
                raw_text = "\n".join(parts)
            elif isinstance(raw, str):
                raw_text = raw
            else:
                raw_text = json.dumps(raw, ensure_ascii=False)
            blocks.append({
                "kind": "tool_result",
                "tool_use_id": block.get("tool_use_id", ""),
                "text": redact(raw_text, counter),
                "is_error": bool(block.get("is_error", False)),
            })
        else:
            blocks.append({"kind": "unknown_inner", "text": f"[unknown inner type: {btype}]"})
    return blocks


def redact_dict(obj, counter: dict[str, int]):
    """Recursively redact string leaves inside a JSON-shaped object."""
    if isinstance(obj, str):
        return redact(obj, counter)
    if isinstance(obj, dict):
        return {k: redact_dict(v, counter) for k, v in obj.items()}
    if isinstance(obj, list):
        return [redact_dict(v, counter) for v in obj]
    return obj


def parse_jsonl(path: Path, counter: dict[str, int]) -> tuple[dict, list[dict]]:
    """Read the JSONL and emit (session_metadata, typed_records).

    Every string in the output has already been through `redact()`.
    """
    session_meta: dict = {
        "session_id": None,
        "permission_mode": None,
        "cwd": None,
        "start_time": None,
        "end_time": None,
        "malformed_lines": 0,
    }
    records: list[dict] = []
    prev_ts: datetime | None = None

    with path.open("r", encoding="utf-8", errors="replace") as f:
        for line_no, line in enumerate(f):
            line = line.rstrip("\n")
            if not line.strip():
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                session_meta["malformed_lines"] += 1
                continue

            rtype = obj.get("type", "unknown")

            # Metadata extraction — happens on every record that carries it
            if session_meta["session_id"] is None and obj.get("sessionId"):
                session_meta["session_id"] = obj.get("sessionId")
            if session_meta["permission_mode"] is None and obj.get("permissionMode"):
                session_meta["permission_mode"] = obj.get("permissionMode")
            if session_meta["cwd"] is None and obj.get("cwd"):
                session_meta["cwd"] = obj.get("cwd")

            # First-line metadata record — purely informational
            if rtype == "permission-mode":
                session_meta["permission_mode"] = obj.get("permissionMode")
                session_meta["session_id"] = obj.get("sessionId") or session_meta["session_id"]
                continue

            # Dropped entirely — internal state only
            if rtype == "file-history-snapshot":
                continue

            ts = parse_timestamp(obj.get("timestamp"), prev_ts)
            if session_meta["start_time"] is None:
                session_meta["start_time"] = ts
            session_meta["end_time"] = ts
            prev_ts = ts

            if rtype == "user":
                msg = obj.get("message") or {}
                blocks = extract_content_blocks(msg, counter)
                records.append({
                    "kind": "user",
                    "timestamp": ts,
                    "blocks": blocks,
                    "is_sidechain": bool(obj.get("isSidechain")),
                    "uuid": obj.get("uuid") or obj.get("promptId") or "",
                })
            elif rtype == "assistant":
                msg = obj.get("message") or {}
                blocks = extract_content_blocks(msg, counter)
                records.append({
                    "kind": "assistant",
                    "timestamp": ts,
                    "blocks": blocks,
                    "is_sidechain": bool(obj.get("isSidechain")),
                    "uuid": obj.get("uuid") or "",
                })
            elif rtype == "system":
                content = obj.get("content") or obj.get("message", {}).get("content") or ""
                if isinstance(content, list):
                    content = "\n".join(
                        c.get("text", "") for c in content if isinstance(c, dict)
                    )
                records.append({
                    "kind": "system_note",
                    "timestamp": ts,
                    "text": redact(str(content), counter),
                })
            elif rtype == "attachment":
                att = obj.get("attachment") or {}
                name = att.get("name") or att.get("fileName") or att.get("filename") or "unnamed"
                records.append({
                    "kind": "attachment_marker",
                    "timestamp": ts,
                    "name": redact(str(name), counter),
                })
            else:
                records.append({
                    "kind": "unknown_outer",
                    "timestamp": ts,
                    "type": rtype,
                })

    records.sort(key=lambda r: r["timestamp"])
    return session_meta, records


# ---------------------------------------------------------------------------
# Emitter — typed records → Markdown archive
# ---------------------------------------------------------------------------

def humanise_duration(start: datetime, end: datetime) -> str:
    if start is None or end is None:
        return "unknown"
    delta = end - start
    total_seconds = int(delta.total_seconds())
    if total_seconds < 0:
        return "unknown"
    hours, remainder = divmod(total_seconds, 3600)
    minutes, _seconds = divmod(remainder, 60)
    if hours:
        return f"{hours}h {minutes:02d}m"
    return f"{minutes}m"


def derive_session_slug(records: list[dict], session_uuid: str) -> str:
    """First user message's first sentence → slug, or first 8 of UUID."""
    for rec in records:
        if rec["kind"] != "user":
            continue
        for block in rec.get("blocks", []):
            if block.get("kind") == "text" and block.get("text"):
                text = block["text"].strip()
                first_sentence = re.split(r"(?<=[.!?])\s", text, maxsplit=1)[0]
                slug = slugify_title(first_sentence, max_len=50)
                if slug:
                    return slug
    return (session_uuid or "session")[:8]


def compute_frontmatter_fields(records: list[dict], counter: dict[str, int]) -> dict:
    tool_calls_total = 0
    tool_calls_by_name: dict[str, int] = {}
    files_written: set[str] = set()
    files_edited: set[str] = set()
    sub_agents = 0
    for rec in records:
        if rec["kind"] != "assistant":
            continue
        for block in rec.get("blocks", []):
            if block.get("kind") != "tool_call":
                continue
            tool_calls_total += 1
            name = block.get("name", "unknown")
            tool_calls_by_name[name] = tool_calls_by_name.get(name, 0) + 1
            inp = block.get("input") or {}
            if name == "Write":
                fp = inp.get("file_path")
                if fp:
                    files_written.add(fp)
            elif name == "Edit":
                fp = inp.get("file_path")
                if fp:
                    files_edited.add(fp)
            elif name == "Agent":
                sub_agents += 1
    return {
        "tool_calls_total": tool_calls_total,
        "tool_calls_by_name": tool_calls_by_name,
        "files_written": sorted(files_written),
        "files_edited": sorted(files_edited),
        "sub_agents_spawned": sub_agents,
        "redaction_hits_total": sum(counter.values()),
        "redaction_hits_by_pattern": dict(counter),
    }


def format_tool_call_body(name: str, inp: dict) -> str:
    """Brief summary of a tool call — key fields only, never the full dict."""
    if name == "Bash":
        cmd = str(inp.get("command", ""))
        desc = str(inp.get("description", ""))
        line1 = f"$ {cmd[:200]}{'…' if len(cmd) > 200 else ''}"
        return f"{line1}\n# {desc}" if desc else line1
    if name == "Write":
        fp = inp.get("file_path", "")
        content = inp.get("content", "")
        size = len(content) if isinstance(content, str) else 0
        return f"file_path: {fp}\nsize: {size} bytes"
    if name == "Edit":
        fp = inp.get("file_path", "")
        old = str(inp.get("old_string", ""))[:80]
        new = str(inp.get("new_string", ""))[:80]
        return f"file_path: {fp}\n- {old}\n+ {new}"
    if name == "Read":
        return f"file_path: {inp.get('file_path', '')}"
    if name in ("Grep", "Glob"):
        return f"pattern: {inp.get('pattern', '')}\npath: {inp.get('path', '')}"
    if name == "Agent":
        return f"subagent_type: {inp.get('subagent_type', '')}\ndescription: {inp.get('description', '')}"
    if name == "WebFetch":
        return f"url: {inp.get('url', '')}"
    if name == "WebSearch":
        return f"query: {inp.get('query', '')}"
    if name in ("TaskCreate", "TaskUpdate"):
        return json.dumps(inp, ensure_ascii=False)[:300]
    return json.dumps(inp, ensure_ascii=False)[:300]


def tool_language_hint(name: str) -> str:
    if name == "Bash":
        return "bash"
    if name in ("Write", "Edit"):
        return "diff"
    return "text"


def truncate_lines(text: str, max_lines: int = 40) -> str:
    lines = text.splitlines()
    if len(lines) <= max_lines:
        return text
    head = "\n".join(lines[:max_lines])
    return f"{head}\n… ({len(lines) - max_lines} more lines)"


def truncate_chars(text: str, max_chars: int = 500) -> str:
    if len(text) <= max_chars:
        return text
    return f"{text[:max_chars]}… ({len(text) - max_chars} more chars)"


def render_yaml_dict(d: dict, indent: int = 2) -> str:
    """Minimal YAML dict rendering for frontmatter histograms."""
    if not d:
        return "  {}"
    pad = " " * indent
    lines = []
    for k, v in d.items():
        key = str(k).replace(":", "_")
        lines.append(f"{pad}{key}: {v}")
    return "\n".join(lines)


def emit_markdown(
    records: list[dict],
    session_meta: dict,
    summary: dict,
    source_jsonl: Path,
    out_path: Path,
) -> None:
    """Write the full Markdown archive atomically (write to .tmp, rename)."""
    start = session_meta["start_time"]
    end = session_meta["end_time"]
    local_start = start.astimezone() if start else None
    local_end = end.astimezone() if end else None
    duration = humanise_duration(start, end) if start and end else "unknown"
    session_slug = derive_session_slug(records, session_meta.get("session_id", "") or "")
    session_uuid = session_meta.get("session_id") or ""
    cwd = session_meta.get("cwd") or ""
    project_slug = slugify_cwd(cwd) if cwd else ""
    permission_mode = session_meta.get("permission_mode") or "unknown"

    description = ""
    for rec in records:
        if rec["kind"] == "user":
            for block in rec.get("blocks", []):
                if block.get("kind") == "text" and block.get("text"):
                    description = truncate_chars(block["text"].strip().replace("\n", " "), 120)
                    break
            if description:
                break

    # Frontmatter
    lines: list[str] = []
    lines.append("<!-- SPDX-License-Identifier: MIT -->")
    lines.append("---")
    lines.append(f"name: {session_slug}")
    lines.append(f"description: {json.dumps(description, ensure_ascii=False)}")
    lines.append("type: session-archive")
    lines.append(f"session_uuid: {session_uuid}")
    lines.append(f"project_slug: {project_slug}")
    lines.append(f"project_cwd: {cwd}")
    lines.append(f"start_time: {local_start.isoformat() if local_start else 'unknown'}")
    lines.append(f"end_time: {local_end.isoformat() if local_end else 'unknown'}")
    lines.append(f"duration: {duration}")
    lines.append(f"tool_calls_total: {summary['tool_calls_total']}")
    lines.append("tool_calls_by_name:")
    lines.append(render_yaml_dict(summary["tool_calls_by_name"]))
    lines.append(f"files_written: {len(summary['files_written'])}")
    lines.append(f"files_edited: {len(summary['files_edited'])}")
    lines.append(f"sub_agents_spawned: {summary['sub_agents_spawned']}")
    lines.append(f"redaction_hits_total: {summary['redaction_hits_total']}")
    lines.append("redaction_hits_by_pattern:")
    lines.append(render_yaml_dict(summary["redaction_hits_by_pattern"]))
    lines.append("include_usage_stats: false")
    lines.append("---")
    lines.append("")
    lines.append(f"# Session archive — {session_slug}")
    lines.append("")
    lines.append("## Session metadata")
    lines.append("")
    lines.append(f"- **Session UUID**: `{session_uuid}`")
    lines.append(f"- **Project**: `{project_slug}` (`{cwd}`)")
    lines.append(f"- **Started**: {local_start.strftime('%Y-%m-%d %H:%M:%S %Z') if local_start else 'unknown'}")
    lines.append(f"- **Ended**: {local_end.strftime('%Y-%m-%d %H:%M:%S %Z') if local_end else 'unknown'}")
    lines.append(f"- **Duration**: {duration}")
    lines.append(f"- **Permission mode**: {permission_mode}")
    lines.append(f"- **Source JSONL**: `{source_jsonl}`")
    lines.append(f"- **Malformed lines skipped**: {session_meta.get('malformed_lines', 0)}")
    lines.append("")

    # Activity summary
    lines.append("## Activity summary")
    lines.append("")
    lines.append("### Tool calls")
    lines.append("")
    if summary["tool_calls_by_name"]:
        lines.append("| Tool | Count |")
        lines.append("|---|---|")
        for name, count in sorted(summary["tool_calls_by_name"].items(), key=lambda kv: -kv[1]):
            lines.append(f"| {name} | {count} |")
    else:
        lines.append("*(no tool calls)*")
    lines.append("")
    lines.append("### Files written")
    lines.append("")
    if summary["files_written"]:
        for fp in summary["files_written"]:
            lines.append(f"- `{fp}`")
    else:
        lines.append("*(none)*")
    lines.append("")
    lines.append("### Files edited")
    lines.append("")
    if summary["files_edited"]:
        for fp in summary["files_edited"]:
            lines.append(f"- `{fp}`")
    else:
        lines.append("*(none)*")
    lines.append("")
    lines.append("### Redaction report")
    lines.append("")
    if summary["redaction_hits_by_pattern"]:
        lines.append("| Pattern | Hit count |")
        lines.append("|---|---|")
        for name, count in sorted(summary["redaction_hits_by_pattern"].items(), key=lambda kv: -kv[1]):
            lines.append(f"| {name} | {count} |")
        lines.append("")
        lines.append(f"Total: **{summary['redaction_hits_total']}** redactions across the session.")
    else:
        lines.append("*(no redactions — unusual, confirm the pattern set is loaded)*")
    lines.append("")

    # Turn-by-turn
    lines.append("## Turn-by-turn transcript")
    lines.append("")
    turn_no = 0
    for rec in records:
        kind = rec["kind"]
        ts = rec.get("timestamp")
        local_ts = ts.astimezone() if ts else None
        ts_str = local_ts.strftime("%H:%M:%S") if local_ts else "--:--:--"

        if kind == "user":
            turn_no += 1
            lines.append(f"### Turn {turn_no} — user · {ts_str}")
            lines.append("")
            for block in rec.get("blocks", []):
                bkind = block.get("kind")
                if bkind == "text":
                    text = truncate_chars(block.get("text", ""), 500)
                    for bl in text.splitlines() or [""]:
                        lines.append(f"> {bl}")
                    lines.append("")
                elif bkind == "tool_result":
                    header = f"→ result for {block.get('tool_use_id', '')}"
                    header += " (error)" if block.get("is_error") else " (ok)"
                    if block.get("is_error"):
                        header = f"[ERROR] {header}"
                    lines.append("```text")
                    lines.append(header)
                    lines.append(truncate_lines(block.get("text", ""), 40))
                    lines.append("```")
                    lines.append("")
                elif bkind == "unknown_inner":
                    lines.append(block.get("text", ""))
                    lines.append("")
        elif kind == "assistant":
            turn_no += 1
            lines.append(f"### Turn {turn_no} — assistant · {ts_str}")
            lines.append("")
            for block in rec.get("blocks", []):
                bkind = block.get("kind")
                if bkind == "text":
                    lines.append(block.get("text", ""))
                    lines.append("")
                elif bkind == "thinking":
                    lines.append("<details>")
                    lines.append("<summary>Thinking (click to expand)</summary>")
                    lines.append("")
                    lines.append(truncate_lines(block.get("text", ""), 80))
                    lines.append("")
                    lines.append("</details>")
                    lines.append("")
                elif bkind == "tool_call":
                    name = block.get("name", "unknown")
                    lang = tool_language_hint(name)
                    lines.append(f"```{lang}")
                    lines.append(f"$ {name}")
                    lines.append(truncate_lines(format_tool_call_body(name, block.get("input") or {}), 20))
                    lines.append("```")
                    lines.append("")
                elif bkind == "unknown_inner":
                    lines.append(block.get("text", ""))
                    lines.append("")
        elif kind == "system_note":
            text = rec.get("text", "").strip()
            if text:
                one_line = text.replace("\n", " ")
                lines.append(f"_system: {truncate_chars(one_line, 300)}_")
                lines.append("")
        elif kind == "attachment_marker":
            lines.append(f"[attachment: {rec.get('name', 'unnamed')}]")
            lines.append("")
        elif kind == "unknown_outer":
            lines.append(f"_[unknown type: {rec.get('type', '?')}]_")
            lines.append("")

    lines.append("## End of archive")
    lines.append("")
    lines.append(f"Session ended at {local_end.strftime('%H:%M:%S %Z') if local_end else 'unknown'}.")
    lines.append("")

    body = "\n".join(lines)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = out_path.with_suffix(out_path.suffix + ".tmp")
    tmp_path.write_text(body, encoding="utf-8")
    tmp_path.replace(out_path)


def allocate_archive_path(sessions_dir: Path, date: datetime, slug: str) -> Path:
    """<sessions_dir>/<YYYY-MM-DD>_<slug>.md, with -2/-3 suffix on collision."""
    date_str = date.astimezone().strftime("%Y-%m-%d")
    base = f"{date_str}_{slug}"
    candidate = sessions_dir / f"{base}.md"
    i = 2
    while candidate.exists():
        candidate = sessions_dir / f"{base}-{i}.md"
        i += 1
    return candidate


# ---------------------------------------------------------------------------
# Halt-on-leak verification gate
# ---------------------------------------------------------------------------

def verify_no_leak(archive_path: Path) -> tuple[bool, dict[str, int]]:
    """Re-apply the pattern set to the written file. Any hit = LEAK."""
    content = archive_path.read_text(encoding="utf-8")
    leaks: dict[str, int] = {}
    for name, pattern in REDACTION_PATTERNS:
        # Any match on a post-redaction file that contains the literal
        # `[REDACTED:<name>]` marker is NOT a leak — it's the redaction tag
        # itself. Strip those markers before re-matching.
        stripped = re.sub(r"\[REDACTED:[a-z_]+\]", "", content)
        hits = pattern.findall(stripped)
        if hits:
            leaks[name] = len(hits)
    return (len(leaks) == 0, leaks)


# ---------------------------------------------------------------------------
# INDEX maintenance
# ---------------------------------------------------------------------------

INDEX_TEMPLATE = """<!-- SPDX-License-Identifier: MIT -->

# Session Archives INDEX

Machine-readable session archives produced by the `session-post-processor`
skill. Each archive is a Markdown summary of a Claude Code session with
secrets redacted and a halt-on-leak verification gate.

See `skills/session-post-processor/SKILL.md` for the trigger phrases and flow.

## Archives
*(none — run the skill to produce the first archive)*
"""


def ensure_sessions_dir(project_root: Path) -> Path:
    sessions_dir = project_root / "memory" / "project" / "sessions"
    sessions_dir.mkdir(parents=True, exist_ok=True)
    index = sessions_dir / "INDEX.md"
    if not index.exists():
        index.write_text(INDEX_TEMPLATE, encoding="utf-8")
    return sessions_dir


def update_index(sessions_dir: Path, archive_path: Path, session_meta: dict, summary: dict) -> None:
    index = sessions_dir / "INDEX.md"
    if not index.exists():
        index.write_text(INDEX_TEMPLATE, encoding="utf-8")

    start = session_meta.get("start_time")
    local_start = start.astimezone() if start else None
    date_str = local_start.strftime("%Y-%m-%d") if local_start else "unknown"
    duration = humanise_duration(session_meta.get("start_time"), session_meta.get("end_time"))
    title = archive_path.stem
    rel = archive_path.name
    entry = (
        f"- [{date_str} — {title}]({rel}) — "
        f"{duration} · {summary['tool_calls_total']} tool calls · "
        f"{summary['redaction_hits_total']} redactions"
    )

    content = index.read_text(encoding="utf-8")
    lines = content.splitlines()

    # Drop the placeholder line if present
    lines = [l for l in lines if "*(none — run the skill" not in l]

    # Update-in-place if the archive filename is already present, else append
    replaced = False
    for i, line in enumerate(lines):
        if f"]({rel})" in line:
            lines[i] = entry
            replaced = True
            break

    if not replaced:
        # Find the "## Archives" section and append right after it
        archives_idx = -1
        for i, line in enumerate(lines):
            if line.strip() == "## Archives":
                archives_idx = i
                break
        if archives_idx == -1:
            lines.append("")
            lines.append("## Archives")
            archives_idx = len(lines) - 1
        # Insert after the header (and any immediate blank lines)
        insert_at = archives_idx + 1
        while insert_at < len(lines) and lines[insert_at].strip() == "":
            insert_at += 1
        lines.insert(insert_at, entry)

    index.write_text("\n".join(lines) + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# Health card
# ---------------------------------------------------------------------------

def emit_health_card(
    mode: str,
    source: Path | None,
    archive: Path | None,
    checks: dict,
    redaction_counter: dict,
    leak_info: dict,
    status: str,
) -> str:
    now = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M")
    lines: list[str] = []
    lines.append(f"## Session post-processor health — {now}")
    lines.append("")
    lines.append(f"**Mode**: {mode}")
    if source is not None:
        lines.append(f"**Source**: `{source}`")
    if archive is not None:
        lines.append(f"**Archive**: `{archive}`")
    lines.append("")
    lines.append("### Checks")
    lines.append("")
    lines.append("| Check | Result |")
    lines.append("|---|---|")
    for key, val in checks.items():
        lines.append(f"| {key} | {val} |")
    lines.append("")
    if redaction_counter:
        lines.append("### Redaction hits")
        lines.append("")
        lines.append("| Pattern | Hits |")
        lines.append("|---|---|")
        for name, count in sorted(redaction_counter.items(), key=lambda kv: -kv[1]):
            lines.append(f"| {name} | {count} |")
        lines.append("")
    if leak_info:
        lines.append("### LEAKS DETECTED")
        lines.append("")
        for name, count in leak_info.items():
            lines.append(f"- **{name}**: {count} hits")
        lines.append("")
    lines.append(f"**Status**: {status}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Session post-processor — archive a Claude Code JSONL transcript with halt-on-leak redaction.",
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        default=None,
        help="Target project repo root (where memory/project/sessions/ lives). Defaults to the resolved cwd.",
    )
    parser.add_argument(
        "--cwd",
        type=str,
        default=None,
        help="Override the cwd used for slug derivation (e.g. when running from a worktree).",
    )
    parser.add_argument(
        "--jsonl",
        type=Path,
        default=None,
        help="Explicit JSONL source file (bypass slug-based lookup).",
    )
    parser.add_argument(
        "--inject-test-leak",
        action="store_true",
        help="Dogfood only: inject a fake github_pat into the output after redaction to prove the halt gate fires.",
    )
    args = parser.parse_args(argv)

    project_root = (args.project_root or Path.cwd()).resolve()
    cwd_for_slug = args.cwd or os.environ.get("CLAUDE_PROJECT_DIR") or str(project_root)

    checks: dict[str, str] = {}
    counter: dict[str, int] = {}

    # Install step — idempotent
    sessions_dir = ensure_sessions_dir(project_root)
    checks["sessions/ dir"] = "OK"
    checks["INDEX.md"] = "OK"

    # Step 1 — Locate
    try:
        source = locate_source_jsonl(cwd_for_slug, args.jsonl)
    except FileNotFoundError as exc:
        checks["source JSONL"] = f"NONE — {exc}"
        card = emit_health_card("post-action", None, None, checks, counter, {}, "RED")
        print(card)
        return 2
    checks["source JSONL"] = f"OK — {source.name}"

    # Step 2 + 3 — Parse (redaction happens inline on every string)
    try:
        session_meta, records = parse_jsonl(source, counter)
    except Exception as exc:  # only unexpected; parser swallows malformed lines
        checks["parser"] = f"FAILED — {type(exc).__name__}: {exc}"
        card = emit_health_card("post-action", source, None, checks, counter, {}, "RED")
        print(card)
        return 3
    malformed = session_meta.get("malformed_lines", 0)
    checks["parser"] = f"OK ({len(records)} records, {malformed} malformed)"
    checks["redaction pass"] = f"OK ({sum(counter.values())} hits)"

    # Dogfood-only leak injection — matches the finegrained GitHub PAT pattern.
    # Intentionally bypasses the redaction pass by appending a new record AFTER
    # parsing so the emitter writes it raw, then the halt gate catches it.
    if args.inject_test_leak:
        fake_pat = "github_pat_" + "A" * 90
        records.append({
            "kind": "system_note",
            "timestamp": session_meta.get("end_time") or datetime.now(timezone.utc),
            "text": f"dogfood-only leak probe: {fake_pat}",
        })

    # Step 4 — Emit
    summary = compute_frontmatter_fields(records, counter)
    session_slug = derive_session_slug(records, session_meta.get("session_id", "") or "")
    start = session_meta.get("start_time") or datetime.now(timezone.utc)
    archive_path = allocate_archive_path(sessions_dir, start, session_slug)
    try:
        emit_markdown(records, session_meta, summary, source, archive_path)
    except Exception as exc:
        checks["archive written"] = f"FAILED — {type(exc).__name__}: {exc}"
        card = emit_health_card("post-action", source, None, checks, counter, {}, "RED")
        print(card)
        return 4
    size = archive_path.stat().st_size
    if size == 0:
        archive_path.unlink(missing_ok=True)
        checks["archive written"] = "EMPTY — deleted"
        card = emit_health_card("post-action", source, None, checks, counter, {}, "RED")
        print(card)
        return 5
    checks["archive written"] = f"OK ({size} bytes)"

    # Step 5 — Halt-on-leak gate
    clean, leak_info = verify_no_leak(archive_path)
    if not clean:
        archive_path.unlink(missing_ok=True)
        checks["halt-on-leak gate"] = f"LEAK — deleted ({', '.join(leak_info.keys())})"
        card = emit_health_card("post-action", source, None, checks, counter, leak_info, "RED")
        print(card)
        print(
            "\nArchive halted — patterns leaked through redaction. "
            "File deleted. Audit redaction-patterns.md before retrying.",
            file=sys.stderr,
        )
        return 10
    checks["halt-on-leak gate"] = f"CLEAN ({len(REDACTION_PATTERNS)}/{len(REDACTION_PATTERNS)} patterns)"

    # Step 6 — INDEX
    try:
        update_index(sessions_dir, archive_path, session_meta, summary)
        checks["INDEX updated"] = "OK"
    except Exception as exc:
        checks["INDEX updated"] = f"FAILED — {type(exc).__name__}: {exc}"

    # Step 7 — Cleanup sanity
    tmp_path = archive_path.with_suffix(archive_path.suffix + ".tmp")
    if tmp_path.exists():
        tmp_path.unlink()
        checks["tmp cleanup"] = "DIRTY — cleaned"
    else:
        checks["tmp cleanup"] = "OK"

    card = emit_health_card("post-action", source, archive_path, checks, counter, {}, "GREEN")
    print(card)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
