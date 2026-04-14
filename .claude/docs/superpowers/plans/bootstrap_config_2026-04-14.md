<!-- SPDX-License-Identifier: MIT -->
---
name: Bootstrap config seed — 2026-04-14
description: Archived original config.txt seed that launched the Project Genesis v1 bootstrap session on 2026-04-14; preserved as historical record of the session's starting point
type: plan
archived_at: 2026-04-15
original_location: <repo-root>/config.txt (before Étape 4d)
status: historical — the session's decisions may have diverged from the seed's assumptions; see memory/project/session_v1_bootstrap.md for the actual path taken
---

# Bootstrap config seed — historical archive

This file is the verbatim content of the original `config.txt` that seeded the Project Genesis v1 bootstrap session on 2026-04-14. It was placed at the repo root at session start and archived here during Étape 4d so the repo root stays clean (plugin convention) while the historical record is preserved in a durable location.

**Important**: the session's actual decisions may have diverged from this seed as research and design work refined the approach. Consult `memory/project/session_v1_bootstrap.md` for the actual path taken, and this file for the original starting intent.

Known divergences between this seed and the session's final decisions:

- **Repo name**: seed mentioned `project-genesis-2026` throughout; session decision was evergreen `project-genesis`
- **License**: seed left it undecided (4 options); session decision was MIT + SPDX short-form headers
- **Install mechanism**: seed listed manual script / README / Node CLI / Python CLI options; session decision was **Claude Code plugin** in a self-hosted marketplace — a pattern the seed didn't know existed at the time of writing
- **Distribution**: seed assumed "copy markdown to ~/.claude/templates/"; session decision was `/plugin install` with auto-update
- **Phase -1 Dependencies Pre-flight**: seed treated it as v2 territory; session promoted it to v1 core after the user said *"il est temps de connecter les MCP"* and *"multidevice dès le début on a des beta testeurs"*
- **Pépite discovery flagging**: not in the seed at all; added during the 2026-04-15 refinement as a new v1 feature
- **Cross-project research sharing**: not in the seed; added to Layer 0 as a universal rule during the same 2026-04-15 turn

---

## Original config.txt content (verbatim, as of 2026-04-14)

```
PROJECT: Project Genesis 2026 — v1 repo bootstrap
ORIGIN: Born from the Aurum.ai v0_init session on 2026-04-14
SESSION START: 2026-04-XX (when the user opens Claude Code here)

========================================================================
  WHAT THIS PROJECT IS
========================================================================

A dedicated, versioned, reusable repo for the Project Genesis 2026
template — the 7-phase protocol that transforms a folder of raw materials
(a config.txt seed + mixed media) into a fully bootstrapped project with
rules, memory, research cache, and resume prompts.

The v0 of this template was born as a side artefact during the Aurum.ai
v0_init session on 2026-04-14. It was committed inside the aurum-ai repo
at commit 0b1de3d for historical reference. But the template's natural
home is its own repo — different nature (workflow tool vs product),
different lifecycle, different audience, potentially different license.

========================================================================
  APPROACH — RECURSIVE DOGFOODING
========================================================================

This session applies the v0 template to bootstrap its own v1 repo. The
v0 is the midwife of its own successor. Every rough edge of v0 will
surface as live friction during self-application, and those friction
points directly inform v1 improvements.

Computing parallel: the first C compiler was written in assembly, then
rewritten in C and compiled by itself. Since 1971 every C compiler has
self-compiled. This is the same move, applied to a project-init protocol.

Philosophical frame: the user named this a "strange loop" (Hofstadter).
The template reflects itself as it processes itself. The loop is finite
(the template eventually converges on a mature v1.x) but the relationship
between user and template co-evolves indefinitely. See the journal entry
for the full reflection:
C:\Users\conta\.claude\projects\C--Dev-Claude-cowork-aurum-ai\memory\journal_2026-04-14_vertigo-genesis-dogfooding.md

========================================================================
  MANDATORY READING AT PHASE 1 (inherited context from Aurum.ai)
========================================================================

Before doing anything else, read in full these files from the Aurum.ai
auto-memory at:

  C:\Users\conta\.claude\projects\C--Dev-Claude-cowork-aurum-ai\memory\

1. MEMORY.md — the full index. Read every linked file in order.

Priority files (the load-bearing context):

  - project_next_session_plan.md
      The explicit plan to execute in this session. Overrides anything
      the aurum v1 resume prompt might say.

  - project_journal_and_session_history_design.md
      Two new systems to build into the v1 template:
      (a) the journal system (states: captured/seed/growing/dormant/
          resolved; trigger phrases; stratified dialogue format;
          amplification-on-consent pattern)
      (b) the session history post-processor (reads Claude Code's
          native JSONL transcripts, redacts secrets, emits markdown)

  - feedback_project_genesis_auth_preflight.md
      The Phase 5.5 Auth Pre-flight spec — the single biggest v1
      improvement. Covers exact PAT scopes, SSH key generation pattern,
      Chrome profile discovery, pre-written .env.local template, repo
      pre-creation manual pattern, pre-flight test call.

  - feedback_no_shortcut_under_close_pressure.md
      The R2.1 lesson from v0_init: never bypass R2.1/R2.3 with local
      git ops in repo root even under fin-de-session pressure. Defer
      instead. This rule must be baked into the template directives.

  - feedback_windows_mcp_tooling.md
      Hard tooling rules: additive auth only, no new terminal/Chrome
      windows, paste-back pattern, never log the user out of any
      account. These become template directives.

  - feedback_async_midflow_questions.md
      Communication preference: user sends short messages mid-flow;
      Claude handles them at the next natural tool-batch boundary.

  - journal_2026-04-14_vertigo-genesis-dogfooding.md
      The birth story of this very project. Read it for tone and
      context. The v0 template was born in this exchange.

  - user_profile.md
      The owner's profile, working style, available AI stack, language
      preferences.

Reference files (external account context — to be PARAMETERIZED in v1
template, not hard-coded):

  - reference_ssh_setup.md
  - reference_github_account.md
  - reference_supabase_aurum.md
  - reference_chrome_profiles.md
  - reference_research_cache.md

========================================================================
  REFERENCE v0 TEMPLATE (the artefact to apply)
========================================================================

Canonical location:
  C:\Dev\Claude_cowork\aurum_ai\.claude\docs\superpowers\templates\project-genesis-2026.md
  (committed at 0b1de3d on main of aurum-ai)

Mirror copy:
  C:\Users\conta\.claude\templates\project-genesis-2026.md

Read it fully at Phase 1 alongside the Aurum memory. It is the procedure
to self-apply.

========================================================================
  CANONICAL v1 RULES (starting point for Genesis rules)
========================================================================

File:
  C:\Dev\Claude_cowork\aurum_ai\.claude\docs\superpowers\rules\v1_rules.md

Copy R1-R9 as the starting rule set. Adapt at Phase 3:
- R7 (multi-backend MCP, BYO-AI) is aurum-specific — likely drop or
  generalize for the Genesis repo itself.
- R3 (deploy pipeline main -> production -> OVH) is aurum-specific —
  Genesis probably has no production deploy; its "deploy" is publishing
  to ~/.claude/templates/ or GitHub Releases.
- R1, R2, R4, R5, R6, R8, R9 carry over essentially unchanged.

========================================================================
  HARD RULES INHERITED AND NON-NEGOTIABLE
========================================================================

- Additive auth only — NEVER log out any account. Every new auth is
  added alongside existing, never replaces.
- No new terminal or Chrome windows spawning. Paste-back pattern.
- R2.1 Worktree discipline — after the first bootstrap commit, ALL
  edits happen inside .claude/worktrees/<type>_YYYY-MM-DD_<theme>/.
  No direct work in the parent root, ever. The v0_init close shortcut
  was documented as a mistake in feedback_no_shortcut_under_close_pressure.md
  and must NOT be repeated here.
- English only for dev artefacts (R9).
- SSH for git push/pull with a DEDICATED identity (new ed25519 key,
  new host alias in ~/.ssh/config — do NOT reuse github.com-aurum).
  The Aurum SSH key belongs to Aurum; Genesis gets its own.
- GH_TOKEN env override for gh API. Never gh auth login. Create a
  NEW GitHub fine-grained PAT for Genesis with correct scopes
  upfront (use the Phase 5.5 pre-flight checklist — this session
  produces that checklist, so v0 will have to ask the user to create
  the PAT manually, and v1 template codifies the exact scopes so
  future projects don't repeat the pain).
- Journal entries are the 6th memory type (type: journal). Dialogue-
  stratified, amplification-on-consent, never auto-loaded at session
  open. See project_journal_and_session_history_design.md for the
  full spec.
- Session histories are NOT manually captured — Claude Code already
  writes JSONL transcripts to the auto-memory directory. This
  session builds a POST-PROCESSOR for those JSONLs (redaction +
  markdown conversion + repo archival), not a recorder.

========================================================================
  WHAT THIS SESSION PRODUCES
========================================================================

Two deliverables in parallel:

1. A new git repo:
   - Local: C:\Dev\Claude_cowork\project-genesis-2026\
   - Remote: myconciergerie-prog/project-genesis-2026 (private initially,
     potentially public later once polished)
   - SSH: dedicated ed25519 key + host alias in ~/.ssh/config
   - Pattern: user manually creates empty repo in web UI, Claude pushes
     via SSH (fine-grained PAT cannot create user repos via API — this
     limitation was discovered during aurum v0_init)

2. Inside that repo, Project Genesis 2026 template v1 containing:
   - Phase 5.5 Auth Pre-flight with exhaustive checklist
   - Built-in journal system (directives + example entry + trigger
     phrases reference)
   - Built-in session history post-processor (script + invocation
     pattern + INDEX.md scaffold)
   - Install script / one-command setup for future projects
   - README.md for human readers + usage examples
   - CHANGELOG.md (v1 is the first real version; v0 was a rough draft
     inside aurum-ai)
   - All hard rules from aurum v0_init baked in as template directives

========================================================================
  WHAT THIS SESSION DOES NOT PRODUCE
========================================================================

- ANY work on aurum-ai itself. Aurum-ai stays frozen at commit 0b1de3d
  until Genesis v1 is complete and installed at ~/.claude/templates/.
- Features without a documented pain point in the Aurum v0_init feedback
  memories. Build only what v0_init pain demanded. Every other feature
  is premature.

========================================================================
  OPEN DESIGN QUESTIONS FOR PHASE 2
========================================================================

- Repo name: keep "project-genesis-2026" (year-versioned) or switch to
  evergreen "project-genesis"? The year would become stale in 2027.
- License: MIT / Apache-2 / BSL / private? Decide before first push if
  the repo might go public later.
- Install mechanism: shell script, Node CLI, Python CLI, or just a
  README that says "copy this markdown to ~/.claude/templates/"?
  Start with the simplest thing that works.
- Test harness: should v1 ship with a test that applies itself to a
  throwaway folder and verifies the output? Dogfooding as a CI step
  is extreme but could be defensible.

========================================================================
  PHRASE TO LAUNCH THIS SESSION
========================================================================

User says to Claude Code opened in C:\Dev\Claude_cowork\project-genesis-2026\ :

  "On démarre le bootstrap de project-genesis-2026 en appliquant
   récursivement la v0 du template qui est dans aurum-ai. Lis ce config.txt,
   puis toute la mémoire auto d'aurum-ai pour le contexte, puis on y va
   phase par phase en étape de validation par défaut."

Claude Code then:
1. Reads this file (config.txt) — Phase 0 of v0 template.
2. Reads C:\Users\conta\.claude\projects\C--Dev-Claude-cowork-aurum-ai\memory\MEMORY.md
   and every linked file (Phase 1 multimodal pre-read, but text-only
   because no multimedia here).
3. Reads C:\Dev\Claude_cowork\aurum_ai\.claude\docs\superpowers\templates\project-genesis-2026.md
   (the v0 template itself).
4. Reads C:\Dev\Claude_cowork\aurum_ai\.claude\docs\superpowers\rules\v1_rules.md
   (starting rule set).
5. Moves into Phase 2 interactive discovery with the 5 open design
   questions above + anything new.
6. Proceeds phase by phase with explicit validation between steps.

========================================================================
```

---

## Why archive this

Three reasons:

1. **Historical traceability** — knowing exactly what was in the seed lets future sessions (or future contributors) understand the starting assumptions and see how the actual session work diverged
2. **Recursive dogfooding evidence** — the v0 template assumed certain things (repo name with year, manual install) that the recursive self-bootstrap surfaced as v1 improvements; this file is the raw artefact that shows the starting delta
3. **Plugin root cleanliness** — the `config.txt` seed was only needed at session start; keeping it at the repo root after Étape 4d would confuse users who install the plugin and see a stray config file; moving to `plans/` is the correct long-term home
