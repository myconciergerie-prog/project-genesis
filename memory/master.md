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

Full rule set in `skills/genesis-protocol/rules/v1_rules.md` (relocated in v1.2.1 from `.claude/docs/superpowers/rules/` so the `genesis-protocol` skill is self-contained — friction F29). Adapted from Aurum v1 per the Étape 2 scoreboard:

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

## Layer 0 inheritance — how project memory defers to the universal layer

Genesis's project memory (this `memory/` directory plus `CLAUDE.md`) does **not** duplicate universal rules, user profile, hard disciplines, workflow patterns, or machine-specific reference material. Those live in **Layer 0** at `~/.claude/CLAUDE.md` and are auto-loaded into every Claude Code session on this machine — including every Genesis session. Project memory inherits them by reference and only adds Genesis-specific material on top.

Concretely, the following are **owned by Layer 0**, not by this project: the user profile (identity, language, working style, AI stack); hard rules R2.1 worktree discipline, R9 language policy, additive auth, no-new-windows, async-mid-flow; workflow patterns (per-project SSH identity, `GH_TOKEN` env override, fine-grained PAT scope checklist, Chrome profile map); the journal system spec (6th memory type, trigger phrases, stratified format); the R8 research cache convention (TTL, sota/stack/archive split); the best-practice-at-date default and anti-Frankenstein discipline. Genesis's `CLAUDE.md` at the repo root is a short pointer file that names what Layer 0 provides and what lives project-locally — it is explicitly **not** a duplicate of Layer 0.

Project-local additions Genesis **does** own: the v1 rules R1–R10 in `skills/genesis-protocol/rules/v1_rules.md` (which inherit R8 and R9 from Layer 0 by reference and add R10 plugin conventions), the seven shipped skills, the pépite discovery system (7th memory type, `memory/pepites/`), project-specific references (`memory/reference/ssh_genesis_identity.md`, `memory/reference/github_genesis_account.md`), and the scope lock rule for Aurum. Everything else defers up to Layer 0. This inheritance is the Meta-Memory Path C pattern confirmed as the primary path on 2026-04-15 and baked into Genesis v1 as the reference implementation — any project bootstrapped via the `genesis-protocol` skill inherits the same split.

## Cross-skill patterns — the three that emerged through v0.2 → v0.8

Three patterns surfaced during skill implementation and are now named first-class conventions. They are not rules (rules live in `v1_rules.md`); they are **patterns** that rules compose into. When a future skill is added, these are the composition surface to reach for before inventing something new.

**1. 1:1 spec mirror discipline.** When a skill is a faithful implementation of a canonical source document, the skill's `SKILL.md` mirrors the source structurally — same sections, same ordering, same table rows — and drift between the two is a merge-blocker. Applied three times so far: `journal-system` mirrors Layer 0's "Journal System — Universal Thought Capture" section; `pepite-flagging` mirrors `specs/v1_pepite_discovery_flagging.md`; `genesis-protocol`'s `SKILL.md` mirrors this `master.md` 7-phase table. The discipline pays for itself: every file explicitly commits to tracking its source, the rating ceiling is predictable, and code review becomes "diff the two" rather than "read and cross-check".

**2. Concentrated-privilege map.** Every Genesis skill has **at most one** concentrated privilege — one operation that writes outside its own scope or touches something the user cannot easily undo. The rest of each skill is read-only or writes only inside its own project's memory. The seven data points so far: `phase-minus-one` (running installers), `phase-5-5-auth-preflight` (SSH/PAT/repo creation), `journal-system` (none), `session-post-processor` (writing redacted archives, halt-on-leak mitigated), `pepite-flagging` (pointer files into sibling projects, per-target consent mitigated), `genesis-protocol` itself (writing an entire new project directory outside the Genesis repo, top-level consent card mitigated), and `genesis-drop-zone` (writes `drop_zone_intent.md` to cwd after consent card, halt-on-existing, no mkdir — v1.3.0 surface + v1.3.1 structured extraction + v1.3.2 first Layer A privilege write + Layer B Phase 0 handoff wire). Concentrating privilege in one place per skill is the anti-Frankenstein discipline applied to write surfaces. Naming this map makes it a precedent every future skill must answer to: what is your one concentrated privilege, and what is its mitigation?

**3. Granular-commits-inside-feat-branch.** Every feature session since v0.5 has used the same discipline: work happens in a feat (or chore) branch under `.claude/worktrees/`, each meaningful sub-step is a separate commit, the branch is pushed and a PR opened, the PR is squash-merged to main, then tagged. The feat branch is retained after merge per R2.5 as a forensic record. The commits inside the branch preserve the "why" for each step; the squash merge keeps `main` linear; the retained branch lets any future session walk the sub-steps. This is the composition of R2.1 (worktrees) + R2 (PR discipline) + the informal "one commit per idea" convention — naming it here makes it explicit so new sessions do not have to re-derive it.

**4. Layer A / Layer B stratification (v2-onwards, added v1.3.0).** Genesis v2 stratifies the bootstrap into two layered protocols: Layer A (the conversation — Étapes 0, 1, 2, 3) and Layer B (the engine — Phases -1, 0, …, 7). Layer A skills capture intent and translate it for Layer B; Layer B skills do the actual bootstrap work. `genesis-drop-zone` is the first Layer A skill, shipped v1.3.0 as a welcome vertical slice. `genesis-protocol` remains the Layer B orchestrator. The split is a composition pattern, not a rule — new skills declare which layer they live in, and cross-layer dependencies flow Layer A → Layer B, never the reverse. This pattern was not needed while Genesis v1 was an engineer-only tool; it emerged as soon as the v2 conversational surface was introduced. **v1.3.2 is the first cross-layer wire live** — `genesis-drop-zone` writes `drop_zone_intent.md` at cwd (Layer A privilege), `genesis-protocol` Phase 0 detects and consumes it (Layer B read), with precedence over legacy `config.txt`. The pattern is documented in `.claude/docs/superpowers/specs/v2_etape_0_drop_zone.md § "Layer B integration — genesis-protocol Phase 0 (v1.3.2)"` and serves as the reference implementation for future Étape 1 → Phase 1, Étape 2 → Phase 2, Étape 3 → Phase 3 wires.

These four patterns compose. A skill that adds a new privilege must extend the concentrated-privilege map. A skill that implements a canonical spec must declare its 1:1 mirror. A session that touches code must use granular commits inside a worktree branch. A skill that ships under v2-onwards conventions must declare its layer. Any future skill or session that breaks one of these four should call it out explicitly in its self-rating — prose cleanliness and anti-Frankenstein axes both take a hit otherwise.

## Scope lock reminder

**Aurum-ai repo is frozen at `0b1de3d` until Genesis v1 ships.** No aurum-ai commits / PRs / edits allowed in any Genesis session. Only additive auto-memory pointer files are permitted. Full rule in `memory/project/aurum_frozen_scope_lock.md`.
