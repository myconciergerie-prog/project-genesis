<!-- SPDX-License-Identifier: MIT -->
---
name: Phase -1.5 restart round
description: Batched restart prompt rendered once, after Phase -1.4. Lists every restart queued during the install pass (Chrome for native messaging host, Claude Code for new MCPs, rc file reload for new env vars). User restarts everything together and replies "ready".
type: template
stage: -1.5
---

# Phase -1.5 — Restart round (consolidated)

Rendered once, after Phase -1.4, only if at least one restart was queued during Phase -1.3. Restarts that accumulate are:

- **Chrome** — needed after installing the Claude in Chrome extension so the native messaging host is registered.
- **Claude Code session** — needed after `claude mcp add` so the new MCP (Playwright, `ide`, etc.) is loaded.
- **Shell rc file reload** — needed after any step that appended to `~/.bashrc` / `~/.zshrc` / `~/.config/fish/config.fish`, so new env vars (e.g. `GH_TOKEN` pattern, `PATH` changes) take effect.

## Template

```
===== Phase -1.5 — Restart round =====

Please restart the following, in order, then reply "ready":

  [ ] Close all Chrome windows and reopen Chrome
      (required so the Claude in Chrome native messaging host loads)

  [ ] Run:   source ~/.bashrc      (or  source ~/.zshrc  on zsh,
                                    or  exec fish         on fish)
      (required so the new PATH and env vars are visible to this shell)

  [ ] Close this Claude Code session and re-open it via `claude` in
      the same project directory
      (required so Claude Code picks up the new MCPs you just installed)

Reply "ready" when everything above is done.
Reply "skip chrome" / "skip shell" / "skip claude" to defer any of them.

====================================
```

## Ordering

The restarts are listed in **dependency order** so that when the user restarts Claude Code last, everything else is already in place:

1. Chrome first — native messaging host picks up on browser start.
2. Shell rc reload second — env vars propagate to the current shell, which Claude Code will inherit when re-spawned.
3. Claude Code session last — it re-reads `~/.claude.json`, the new MCPs appear, and we are ready for Phase -1.6 verification in the fresh session.

## When all three are unnecessary

If the install pass queued no restart items, Phase -1.5 is skipped. The skill jumps straight to Phase -1.6.

## Handling a Claude Code self-restart

Restarting the Claude Code session is a special case: the very session rendering this card is the one that will be killed and relaunched. The skill handles this by writing a marker file first:

```bash
mkdir -p memory/reference
cat > memory/reference/phase-minus-one-resume.md <<'EOF'
---
stage: -1.5
step: pending_verification
resumed_at: null
---

Phase -1 is paused at the restart round. The user closed and reopened the
Claude Code session. On the next session open, resume at Phase -1.6
(verification pass) with no new prompts.
EOF
```

On the next session open, the skill looks for this marker file at startup, and if present jumps straight to Phase -1.6 without re-running Phase -1.0 → Phase -1.4.

This gives the user a seamless "restart and I'm back where I left off" experience even across the hard boundary of a CLI relaunch.

## Parsing the user's reply

- **`ready`** — mark every restart as completed, move to Phase -1.6.
- **`skip chrome`** / **`skip shell`** / **`skip claude`** — mark the specific restart as skipped, record in the marker file, move on. Verification may surface the consequence (e.g. a new MCP not loaded because Claude Code was not restarted).
- **No reply / `pause`** — write the marker file as above, pause, allow resume on next session open.

## Anti-Frankenstein reminders

- **Never render the restart card if the queued restart set is empty.**
- **Never auto-execute the Claude Code restart** — that is a hard permission boundary; the user triggers it themselves.
- **Never combine the restart with new install steps.** Phase -1.5 is a pure handoff point, not a surface for late additions.
