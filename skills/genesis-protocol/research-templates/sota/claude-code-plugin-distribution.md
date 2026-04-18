<!-- SPDX-License-Identifier: MIT -->
---
topic: claude-code-plugin-distribution
type: sota
created_at: 2026-04-19
expires_at: 2026-04-26
status: active
template_of: genesis-protocol v1.4.2
original_created_at: 2026-04-14
sources:
  - https://code.claude.com/docs/en/discover-plugins
  - https://github.com/anthropics/claude-plugins-official
  - https://www.pasqualepillitteri.it/en/news/215/superpowers-claude-code-complete-guide
  - https://github.com/obra/superpowers
  - https://www.agensi.io/learn/claude-code-plugin-marketplace-guide
confidence: high
supersedes: null
---

# Claude Code Plugin Distribution — State of the Art 2026

## TL;DR

- **Best-at-date**: publish as a Claude Code plugin in a **self-hosted marketplace** — the git repo itself serves as both source and marketplace
- **Most-potential**: submit the polished plugin to `anthropics/claude-plugins-official` for visibility, review, and auto-update through the official Anthropic marketplace
- **Obsolete pattern**: manual "copy template.md into `~/.claude/templates/`" (pre-2026, superseded by plugin install)

## Since January 15, 2026

Claude Code has an **official plugin marketplace** (`claude-plugins-official`, managed by Anthropic). Plugins are installable via:

```
/plugin install <plugin-name>@<marketplace-or-github-ref>
```

The reference comparable project, `obra/superpowers`, was accepted into the official marketplace and is installable via `/plugin install superpowers@claude-plugins-official`. It ships 14 skills that install into `~/.claude/skills/`, and its "using superpowers" master skill dispatches auto-activation at session start.

## Distribution models available

1. **Self-hosted marketplace** (the repo is its own marketplace): users install via `/plugin install <plugin-name>@<github-owner>/<repo>`. No central listing, no review queue, full autonomy over release timing. Downside: discovery is word-of-mouth.
2. **Official Anthropic marketplace** (`claude-plugins-official`): PR against the repo with review. Auto-update for all users. Public visibility. Higher quality bar.
3. **Third-party marketplaces** (e.g. `cased/claude-code-plugins`, `xiaolai/claude-plugin-marketplace`): curated community lists. Similar to option 2 without Anthropic's review.

As of 2026, 2,400+ skills are published across 2,500+ marketplaces; 43 curated marketplaces listed in `Chat2AnyLLM/awesome-claude-plugins`.

## Application for Genesis

- **Phase 1 (this bootstrap session)**: option 1 — self-hosted marketplace. The `myconciergerie-prog/project-genesis` repo IS the marketplace. Install via `/plugin install project-genesis@myconciergerie-prog/project-genesis`.
- **Phase 2 (deferred)**: option 2 — submit to `anthropics/claude-plugins-official` once Genesis has been applied to at least one external project (the aurum-v1 re-bootstrap will be the first real field test).
- **Never fall back** to the pre-2026 pattern of asking the user to copy a markdown file manually — that pattern is obsolete.
