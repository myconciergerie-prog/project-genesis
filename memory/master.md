<!-- SPDX-License-Identifier: MIT -->
---
name: Master vision — Project Genesis
description: Stable vision, stack, and rules summary for the Project Genesis Claude Code plugin — read at every session open per R1.1 as the load-bearing context for all work
type: project
---

# Project Genesis — master vision

## What this project is

A Claude Code plugin that transforms a folder containing a `config.txt` seed (plus optional mixed media) into a fully bootstrapped project — rules, memory architecture, research cache, git repo, and resume prompts — via a 7-phase protocol orchestrated by Claude Code itself. The protocol minimizes user friction to the security floor of unavoidable manual interventions (logins, admin passwords, browser extension permissions, 2FA, device authorization).

The plugin ships:

- **Phase -1 Dependencies Pre-flight** (core) — 3-mode ladder (detailed / semi-auto / auto), multidevice baseline
- **Phase 5.5 Auth Pre-flight** — SSH keygen, fine-grained PAT creation, empty repo creation, 3-probe pre-flight test
- **Journal system** — stratified thought capture, 6th memory type
- **Session post-processor** — JSONL transcript redaction + Markdown archive
- **Pépite discovery flagging** — red-light system with cross-project routing, 7th memory type
- **Canonical R1-R10 rules** — adapted for any new project

## Why it exists

Born during the Aurum.ai v0_init session on 2026-04-14 as a 7-phase template markdown committed at `0b1de3d`. After Aurum v0_init, the user observed that the template's natural home was its own dedicated repo with its own lifecycle, different audience, and potentially different license. The recursive self-bootstrap (applying v0 to itself to produce v1) is dogfooding from day zero — every friction from v0 surfaces in real time during self-application, and each friction informs a v1 improvement.

The user framed it as a "strange loop" (Hofstadter). Compiler bootstrapping philosophy: the first C compiler was written in assembly, rewritten in C, and compiled by itself. Every C compiler since 1971 self-compiles. Genesis follows the same move.

## Stack

| Layer | Tool / pattern | Role | Research reference |
|---|---|---|---|
| Distribution | Claude Code plugin | `.claude-plugin/plugin.json` manifest; `skills/`, `templates/`, `hooks/` at plugin root; self-hosted marketplace initially, Anthropic official marketplace deferred | `research/sota/claude-code-plugin-distribution_2026-04-14.md`, `research/stack/claude-code-plugin-structure_2026-04-14.md` |
| License | MIT + SPDX headers | Permissive; Apache-2 as documented pivot path; SPDX short-form on every source file | `research/sota/open-source-license-for-dev-tooling_2026-04-14.md`, `research/sota/spdx-headers_2026-04-14.md` |
| Language (skills) | Python / Bash / Markdown | Whichever is simplest per skill; anti-Frankenstein gate on language additions | — |
| Version mgmt | Semver | `plugin.json` version + git tag `v<semver>` + CHANGELOG entry with 5-axis self-rating | — |
| Memory | 7 types | user / feedback / project / reference / themes / journal / pepites (6th and 7th types new in Genesis) | `~/.claude/CLAUDE.md` Layer 0 journal spec + `specs/v1_pepite_discovery_flagging.md` |
| Research cache | R8 TTL | sota 7d / stack 1d / archive forensic | Layer 0 R8 section |
| Worktree | R2.1 | Every session works in `.claude/worktrees/<type>_YYYY-MM-DD_<theme>/` after bootstrap; forensic snapshots retained per R2.5 | `rules/v1_rules.md` R2 |
| SSH identity | Per-project ed25519 | `id_ed25519_genesis` + `github.com-genesis` alias in `~/.ssh/config`; SSH for git, `GH_TOKEN` env for API | `memory/reference/ssh_genesis_identity.md` |
| Multidevice | Claude Code Remote Control (Max) / Codespaces (Pro) | Beta-tester-first framing; multidevice core in Phase -1, not optional | `research/sota/claude-ecosystem-cross-os_2026-04-15.md`, `specs/v1_phase_minus_one_first_user_bootstrap_flow.md` |
| IDE | VS Code + Claude Code extension | Extension doubles as local `ide` MCP server — installing it extends the MCP surface for all Claude Code sessions on the machine | `research/sota/claude-in-ide-tools_2026-04-15.md` |
| Optional bonus | Google Antigravity | Multi-model agent IDE (Gemini 3.1 Pro + Claude 4.6 + GPT-OSS), free for individuals, Manager Surface for multi-agent orchestration | `research/sota/claude-in-ide-tools_2026-04-15.md` |

## Rules

Full rule set in `.claude/docs/superpowers/rules/v1_rules.md`. Adapted from Aurum v1 per the Étape 2 scoreboard:

- **KEEP intégral**: R2 (worktree & branch discipline)
- **ADAPT**: R1 (session lifecycle, drop OVH deploy check), R3 (deploy = plugin version bump + marketplace manifest), R4 (memory — add `journal/` + `pepites/` dirs), R5 (dual-layer docs: plugin content at root, dev docs in `.claude/docs/superpowers/`), R6 (sub-agents only, drop R6.3 Managed Agents)
- **INHERIT from Layer 0**: R8 (research cache), R9 (language policy) — cited by reference, not duplicated
- **DROP**: R7 (multi-backend MCP BYO-AI — Aurum-runtime-specific)
- **NEW**: R10 (plugin conventions, SPDX headers, self-rating discipline, anti-Frankenstein gate, pépite discovery discipline)

Layer 0 (`~/.claude/CLAUDE.md`) holds the universal rules applied at every session on this machine: additive auth, no new windows, R2.1 close-pressure discipline, R9 language policy, best-practice-at-date default, anti-Frankenstein, cross-project research sharing, journal system, async mid-flow questions, per-project SSH identity pattern, GH_TOKEN env override, R8 research cache, Chrome profile map.

## Target for v1.0.0

**Self-rating target: 8.5/10** on a 5-axis rubric (pain-driven / prose cleanliness / best-at-date / self-contained / anti-Frankenstein). Intentionally sub-10 per the anti-Frankenstein inflection-point discipline — the plateau of optimality, not perfection.

v0.1.0 scaffold = **6.0/10** (this commit).
v0.2.0 = **7.0/10** (first skill end-to-end).
v1.0.0 = **8.5/10** (all v1 specs implemented).

## What v1 ships

All skills and templates listed in `skills/README.md` and `templates/README.md`, implemented at Étape 5 in worktrees (one PR per skill). Phase -1 Dependencies Pre-flight is **core** (not optional). Multidevice via Claude Code Remote Control (Max plan) or GitHub Codespaces fallback (Pro plan) is **core**. Google Antigravity, Android Termux, voice mode, and connector presets are **opt-in bonuses**.

## What v2 target is

- Browser-automation-driven Phase 5.5 (paste-back becomes optional via Playwright MCP)
- Pépite graph tooling with cross-project propagation automation
- Hook wiring for `SessionEnd` (auto-post-processor)
- Full Meta-Memory Path B: graph walker, backlinks, promote, cross-project-search
- Submission to the official Anthropic marketplace (`anthropics/claude-plugins-official`)

## Scope lock reminder

**Aurum-ai repo is frozen at `0b1de3d` until Genesis v1 ships.** No aurum-ai commits / PRs / edits allowed in any Genesis session. Only additive auto-memory pointer files are permitted. Full rule in `memory/project/aurum_frozen_scope_lock.md`.
