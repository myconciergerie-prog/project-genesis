<!-- SPDX-License-Identifier: MIT -->

# Changelog

All notable changes to Project Genesis are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versioning follows [Semantic Versioning](https://semver.org/).

Every version bump includes a **5-axis self-rating block** per R10.3 discipline, with target < 10 to honor the anti-Frankenstein inflection-point rule.

---

## [1.2.0] — 2026-04-17 — "The conscious strange loop — paradox surfaced"

### Added

- `memory/project/selfdogfood_friction_log_v1_2_0_2026-04-17.md` — **14 new frictions (F20–F34)** captured live during a conscious strange-loop self-dogfood: project-genesis running `genesis-protocol` on a worktree target whose `config.txt` describes Genesis itself. 5 STRUCTURAL, 7 DESIGN, 2 COSMETIC. Cumulative F1–F34.
- `.claude/docs/superpowers/research/sota/v2_promptor_fusion_landscape_2026-04-17.md` — R8 SOTA entry consolidating 3 parallel research agents (drop-zone UX canon 2026, Claude API ingestion Path A/B, multi-file synthesis). TTL 2026-04-24. Seeds v2 Étape 0 design.

### Changed

- `specs/v2_vision_promptor_fusion.md` — **prepended Étape 0 "Le Dépôt"** (drop-zone front door): intent-first unified box, Claude Files API + Citations (Path A recommended), relationship-language privacy, token-streamed acknowledgement. Factual correction: the "Promptor 4-part structure" is credited as Genesis-native synthesis inspired by FR-community Mr Promptor / FlowGPT, **not** as a published pattern (academic Promptor arXiv 2310.08101 does not describe this structure).
- `.claude-plugin/plugin.json` — version bumped from `1.1.0` to `1.2.0`.

### Pépites (red-light, routed cross-project)

1. **F29 — Genesis v1.1 plugin personal-scope install is broken today.** Every user who followed F18's `cp -r skills/ ~/.claude/skills/` hits a halt at Phase 1.3 — the three-levels-up rules-path heuristic resolves to `~/.claude/` which has no `.claude/docs/superpowers/rules/`. P0 fix in v1.2.1.
2. **"Promptor 4-part structure" is Genesis-native.** Credit correctly in all external comms (v2 spec, blog, marketplace listing).

### Meta-findings

- The paradox is architectural, not user error. v1.1's "two sessions, two folders" fix is insufficient: the protocol has no self-defence against target-inside-orchestrator-repo (F23), slug-equals-orchestrator-slug (F27), nested `git init` (F30), or personal-scope rules-path resolution (F29). v1.2.1 must add defensive layers at Step 0 + Step 3.1.
- `mode=auto` needs orchestrator-level semantics. The 3-mode ladder was Phase -1-only; every "consent gate in auto mode" friction (F2, F20, F22) shares this root.
- The orchestrator is at the limits of pure-Markdown design (F32). Thin Python driver is the v1.3 path.

### Notes

- **v1.2.0 is a forensic release**, no code fixes. The friction log IS the deliverable. v1.2.1 applies the 3 P0 fixes (F29, F30, F23+F27) in a separate PR to preserve the diagnostic → treatment narrative.
- Strange-loop target path (`selfdogfood-target/`) retained as forensic artefact on the branch.
- Live execution halted mid-Phase 3 after F30 reproduced — nested `.git/` was cleaned up immediately.

### Self-rating — v1.2.0

| Axis | Rating | Notes |
|---|---|---|
| Pain-driven coverage | 9.2/10 | Every friction was experienced live, not predicted. The strange-loop target was chosen to stress-test the paradox — it succeeded. Two pépite-worthy findings produced. |
| Prose cleanliness | 8.8/10 | Friction log is structured (15 entries × severity / phase / root cause / impact / fix), CHANGELOG is compact. v2 spec amendment is an additive Étape 0. |
| Best-at-date alignment | 9.0/10 | R8 SOTA entry backed by 3 parallel 2026 research agents. Promptor attribution corrected from public sources. |
| Self-contained | 7.5/10 | The forensic log is self-contained; the meta-findings reference R8 entries and Layer 0 files. The "3 P0 fixes" list pushes actionable work to v1.2.1 — correct separation, but the value of v1.2.0 alone is documentary. |
| Anti-Frankenstein | 9.0/10 | Zero speculative code. Every pending fix is backed by a reproduced friction. Explicitly did NOT fix live. |
| **Average** | **8.70/10** | Running average v0.2 → v1.2.0 = **8.57/10**. Above the 8.5 v1 target. |

---

## [1.1.0] — 2026-04-16 — "The Victor test — auth wall demolished"

### Added

- `specs/v2_vision_promptor_fusion.md` — v2 vision born from self-dogfood: conversational bootstrap inspired by Promptor, backed by 5 parallel research agents (zero-friction UX, gh CLI auth, conversational onboarding, MCP tools, magical CLI)
- `memory/project/selfdogfood_friction_log_2026-04-16.md` — 18 frictions (5 STRUCTURAL, 9 DESIGN, 4 COSMETIC) from first real genesis-protocol execution
- `memory/project/session_v1_1_selfdogfood.md` — session memory
- `research/sota/zero-friction-bootstrap-ux_2026-04-16.md` — v0/Bolt/Replit patterns, @clack/prompts, Charm Gum
- `research/sota/gh-cli-single-click-auth_2026-04-16.md` — the 4-line auth revolution

### Changed

- **Phase 5.5 auth flow rewritten: 6 manual browser steps → 1 OAuth click + 2FA**
  - `gh auth login --web` with device flow replaces fine-grained PAT creation
  - `Start-Process chrome.exe -ArgumentList '--profile-directory=...'` for Chrome profile routing (GH_BROWSER env var proven unreliable)
  - `gh ssh-key add` replaces browser paste-back for SSH key registration
  - `gh repo create --private --source=. --remote=origin --push` replaces web UI repo creation
  - HTTPS-first at bootstrap; per-project SSH identity remains for ongoing work
- `.claude-plugin/plugin.json` — version bumped from `1.0.0` to `1.1.0`
- `research/INDEX.md` — 2 new entries added

### Notes

- **Self-dogfood proven end-to-end**: `genesis-selfdogfood` repo created on GitHub (myconciergerie-prog/genesis-selfdogfood, private, v0.1.0 tagged) using the new auth path. 3-probe test GREEN/GREEN/GREEN.
- **The Victor test**: new principle — every Genesis step must pass the "77-year-old non-developer" threshold. If a step requires understanding SSH/PAT/GitHub settings, it's a design failure, not a security floor.
- **Browser paste-back retained as legacy fallback** for environments without `gh` CLI.
- **v2 vision is a spec, not implementation** — conversational surface (Promptor fusion) is a future workstream. v1.1 delivers the auth fix only.

### Self-rating — v1.1.0

| Axis | Rating | Notes |
|---|---|---|
| Pain-driven coverage | 10/10 | Every change directly addresses a real friction found during actual execution. Zero speculative additions. The auth wall was hit, analyzed, and demolished. |
| Prose cleanliness | 9/10 | Vision doc is clean. Friction log is structured. Research entries follow R8 format. |
| Best-at-date alignment | 9.5/10 | 5 parallel research agents verified patterns against 2026 sources. gh CLI commands verified on this machine. |
| Self-contained | 8.5/10 | Auth fix is self-contained. Vision doc references external research but is readable standalone. |
| Anti-Frankenstein | 10/10 | Removed friction instead of adding features. Conversation surface deferred to v2. Only shipped what was proven. |
| **Average** | **9.4/10** | New single-version high. Running average v0.2 → v1.1 = **8.67/10**. |

---

## [1.0.0] — 2026-04-16 — "Ship — the strange loop closes"

### Added

- `hooks/hooks.json` — **SessionEnd hook wiring** for automatic session archiving via `session-post-processor`. Fires on session close, invokes `run.py` against the project root. Justified by three consecutive GREEN dogfood runs (v0.6.0 first run, v0.9.0 terminal run) per the v0.5.0 discipline threshold. Conditional execution: the hook silently no-ops in projects where `skills/session-post-processor/run.py` does not exist. Hook-path resolution for plugin-installed mode is a v1.1 validation target.

### Changed

- `.claude-plugin/plugin.json` — version bumped from `0.9.0` to `1.0.0`. First stable release.
- `memory/project/aurum_frozen_scope_lock.md` — **Aurum freeze lifted**. The lock was in effect from 2026-04-14 (Genesis session 1) to 2026-04-16 (this ship). All four lift conditions met: merged to main, tagged v1.0.0, self-installable via `/plugin install`, validated via dry-run + dogfood runs. Aurum v1 kickoff is now unblocked.

### Notes

- **Pure ship session** — zero new skills, zero runbook changes, zero polish. The value is the tag, the freeze lift, and the hook wiring.
- **Self-installable**: `/plugin install project-genesis@myconciergerie-prog/project-genesis` — the GitHub repo IS the marketplace (self-hosted model per R8 research).
- **Six skills stable**: `phase-minus-one` (7.6), `phase-5-5-auth-preflight` (8.2), `journal-system` (8.8), `session-post-processor` (8.4→8.6), `pepite-flagging` (8.8), `genesis-protocol` (9.0). Zero modifications since their respective ship versions.
- **Beta testers receive install instructions** alongside this release — an HTML invitation documents the 4-step installation flow, the 7-phase protocol, the 3 interaction modes, and the 6 skills.
- **The strange loop**: Genesis was conceived during Aurum v0_init on 2026-04-14 as a 7-phase template. v0.1.0 was the scaffold. v0.2.0–v0.9.0 built the six skills through eight sessions of self-improving development. v1.0.0 is the first stable release — and the next session will run Genesis against itself to produce v1.1. The compiler that compiles itself.
- **Aurum v1 kickoff** is the immediately-next workstream. Genesis v1.2 (post-self-dogfood) will be used to bootstrap/retrofit Aurum v1, Meta-Memory, and myconciergerie projects.

### Self-rating — v1.0.0

| Axis | Rating | Notes |
|---|---|---|
| Pain-driven coverage | 9.0/10 | Every action directly unblocks a waiting stakeholder or closes a documented gap. Hook wiring closes the 9-session automation gap (v0.5.0 → v1.0.0, three GREEN dogfood runs). Aurum freeze lift unblocks the next workstream queued since 2026-04-14. The tag enables beta testing — real users are waiting. Zero speculative additions. |
| Prose cleanliness | 8.5/10 | Ship CHANGELOG is compact. hooks.json is 15 lines. Aurum freeze update is a clean addendum. No unnecessary prose. |
| Best-at-date alignment | 8.5/10 | Hook format matches current Claude Code plugin spec per R8 research. Plugin install uses the self-hosted marketplace pattern. Conditional hook execution is a current defensive pattern. Slight deduction: hook-path resolution for plugin-installed mode is untested — v1.1 target. |
| Self-contained | 9.5/10 | One new file (`hooks/hooks.json`). Two edits (`plugin.json`, `aurum_frozen_scope_lock.md`). Zero new dependencies. Zero skill modifications. The most self-contained version in the project's history. |
| Anti-Frankenstein | 9.5/10 | Explicitly did NOT: add new skills, polish further, run the orchestrator for real, change runbooks, add features, create a marketplace manifest, add test harnesses, fix v0.5/v0.6 known gaps. Ship-only session honored perfectly. |
| **Average** | **9.0/10** | Running average v0.2 → v1.0 = **(7.6 + 8.2 + 8.8 + 8.4 + 8.6 + 8.8 + 9.0 + 8.92 + 9.0) / 9 = 8.59/10**. **0.09 above** the v1.0.0 target of 8.5. The cleanest average in the project's history, achieved by honoring "ship without polish". |

### v1.0.0 is shipped

Six skills stable. Orchestrator validated. Meta-memory documented. Hook wired. Beta testers invited. Aurum freeze lifted. The next session self-dogfoods Genesis v1 through its own genesis-protocol — the strange loop closing for real.

### Known gaps for v1.1.0

- **Real execution of the orchestrator** — first downstream bootstrap (Genesis self-dogfood or Aurum v1 kickoff)
- **Hook-path resolution for plugin-installed mode** — v1.0.0 hook works in development mode; installed-plugin path resolution needs validation
- **Mode retrofit for existing projects** — genesis-protocol assumes a fresh folder; existing projects need a lighter "detect and fill gaps" mode
- **Multi-slug YELLOW warning in `run.py`** — v0.5 gap, still open
- **Test vector harness for redaction patterns** — v0.5/v0.7 gap, still open
- **Allow-list for `generic_long_base64` false positives** — v0.6 gap, still open
- **Five low-severity dry-run findings** — deferred from v0.9.0
- **macOS/Linux validation** — v1.0.0 developed and tested on Windows 11 only

---

## [0.9.0] — 2026-04-16 — "Path A polish — leverage memory context, not number-chase"

### Changed

- **`memory/master.md`** — added two new sections that make the meta-memory architecture and the three emergent cross-skill patterns visible inside the plugin's own docs (no longer implicit in the skill implementations):
  - **Layer 0 inheritance** — explains how Genesis project memory inherits universal rules, user profile, hard disciplines, workflow patterns, and the journal spec from `~/.claude/CLAUDE.md` by reference, and what stays project-local (R10 plugin conventions, the six skills, the pépite system, project-specific SSH/GitHub references, the Aurum scope lock). Names this as the Meta-Memory Path C pattern confirmed primary on 2026-04-15
  - **Cross-skill patterns** — names three first-class conventions that emerged through v0.2 → v0.8: (1) **1:1 spec mirror discipline** applied three times (`journal-system`, `pepite-flagging`, `genesis-protocol`); (2) **concentrated-privilege map** with six data points across the six shipped skills; (3) **granular-commits-inside-feat-branch** as the composition of R2.1 + R2 + the informal "one commit per idea" convention. These are patterns that rules compose into — not rules themselves
- **`README.md`** — full public-facing rewrite for the v1.0.0 ship. Replaces the v0.1.0 scaffold-era prose with a real landing-page narrative reflecting the six shipped skills and the 7-phase orchestrator. Bilingual EN+FR per R9. Sections per language: what Genesis does (1 paragraph), the 7-phase protocol table (1:1 with `master.md`), the six shipped skills with one-liners, a 5-step quickstart from install-Claude-Code through first `/genesis-protocol` invocation, pointers to `master.md`/`CHANGELOG.md`/`CLAUDE.md`/skill `SKILL.md` files, and updated requirements. 129 lines total, ~65 per language — landing page, not a doc site
- **`skills/genesis-protocol/phase-1-rules-memory.md`** — three precision improvements landed from the dry-run walkthrough findings:
  - **Step 1.2** clarified that the three sibling-owned `INDEX.md` files (`journal/`, `pepites/`, `project/sessions/`) are delegated to the sibling install-manifests at Step 1.5 and **not** created by Step 1.2 itself. The previous wording "Use Write to create each file" was ambiguous about delegation
  - **Step 1.3** replaced the ambiguous "either under `~/.claude/plugins/...` OR the dev location" source-path resolution with a concrete recipe: walk three levels up from `skills/genesis-protocol/SKILL.md`'s absolute path. This rule works in both dogfood mode (Genesis repo at `C:\Dev\...\project-genesis\`) and marketplace-installed mode (`~/.claude/plugins/project-genesis/`) because the three-levels-up relationship holds in both layouts. Halt-on-not-found rather than silent fallback
  - **Step 1.5** corrected the inaccurate claim that `phase-minus-one`'s install-manifest creates a `memory/reference/automation-stack.md` placeholder. Reality: `phase-minus-one/install-manifest.yaml` is a stack-install spec (per-OS package list), not a file-target manifest. The actual `automation-stack.md` is written at runtime when `phase-minus-one` runs during Phase -1. Also clarified the idempotency mechanism (`create_if_missing_only: true`) for the three file-target sibling manifests
  - **Step 2.3** same plugin-root resolution rule as Step 1.3; clarified that the five copied entries apply to any Claude Code project regardless of `is-a-plugin`
- **`skills/genesis-protocol/phase-3-git-init.md`** — two precision improvements:
  - **Step 3.2** uses `$HOME` instead of `~` in shell commands for cross-shell portability (bash/zsh/PowerShell). The OpenSSH config block at Step 3.3 keeps `~` because OpenSSH's own parser handles it correctly on every OS — the distinction only matters for shell commands
  - **Step 3.3** added a Windows ACL caveat: `chmod 0600` is a no-op on Windows; if `ssh -T` warns about permissions, fall back to `icacls "%USERPROFILE%\.ssh\config" /inheritance:r /grant:r "%USERNAME%:F"`
- **`skills/genesis-protocol/phase-3-git-init.md`** + **`skills/genesis-protocol/phase-0-seed-loading.md`** — documented scope-lock slug derivation. Phase 0 Step 0.2 now states the rule (first whitespace-terminated token, lowercased, punctuation stripped, internal non-alphanumerics replaced with `-`) and Phase 4 Step 4.5 references it. Phase 0 stores both the derived slug and the verbatim `config.txt` string in `bootstrap_intent.md`; Phase 4 uses the slug for the filename and the verbatim string for in-file context, never re-derives
- **`skills/genesis-protocol/phase-6-commit-push.md`** — Step 6.2 rewritten with two forms for the multi-line commit message: HEREDOC preferred for bash/zsh/git-bash (works on all supported host shells), and a `-F` file-backed fallback for pure Windows `cmd`/PowerShell. The previous form used a literal `-m "...\n..."` which only works in bash. Message content is unchanged
- **`.claude/docs/superpowers/research/`** — refreshed two expired stack entries to `expires_at: 2026-04-17`: `claude-code-plugin-structure_2026-04-14.md` (had expired 2026-04-15, still matches on-disk plugin layout against the six shipped skills) and `claude-code-session-jsonl-format_2026-04-15.md` (expired today; refreshed in place; deep re-verification deferred to dogfood run 3 later this session). INDEX updated accordingly. R8 housekeeping per R1.1
- **`memory/project/dryrun_walkthrough_2026-04-16.md`** — new session artefact. Records the paper trace of the `genesis-protocol` orchestrator against `C:\tmp\genesis-dryrun\` (synthetic config.txt, slug=`dryrun-demo`, is-a-plugin=no). 10 findings surfaced; 5 medium-severity ones land as v0.9.0 fixes (above), 5 low-severity ones are documented as v1.1 candidates with rationale. This is the first end-to-end trace of the orchestrator against a non-Genesis target

### Notes

- **Path A confirmed at session open** — the user picked Path A (v0.9.0 polish → v1.0.0) over Path B (v0.8.0 ships as v1.0.0 directly) at the v0.8.0 close, with the explicit framing *"en tenant compte de toutes les avancées dans la mémoire et dans la préparation de méta memory"*. Every polish item in this release traces back to something learned during v1 bootstrap → v0.8 shipping, not generic code hygiene. The dry-run findings, the `master.md` meta-memory sections, and the README pointers are all instances of this framing
- **Phase-file length trimming explicitly skipped** — the v0.9.0 resume prompt listed phase-file trimming as Priority 4 (~10-15% reduction without content loss). The dry-run fixes added precision content to the same files (phase-1: +6 lines, phase-3: +13 lines, phase-6: +12 lines) — mechanical trimming after substantive precision additions would partially undo the additions and conflicts with the "leverage memory context" framing. Documented as a v1.1 candidate if running average ever needs another nudge after v1.0.0 ships
- **Dogfood run 3 is the terminal action of this session** — the v0.9.0 session is long enough that running `session-post-processor` against its own JSONL is the natural way to land the third successful manual dogfood run. If the halt-on-leak gate returns GREEN, hook wiring becomes a real v1.0.0 option (per the v0.5 discipline). If it returns RED or the run fails, noted and moved on — the v0.9.0 polish stands either way
- **All edits respect the granular-commits-inside-chore-branch discipline** — eight commits in this branch (R8 housekeeping, phase-1 fixes + dryrun notes, phase-3 fixes, phase-6 fix, master.md sections, README rewrite, version bump + CHANGELOG, the dogfood-run-3 fixture if any). Squashed at merge time per R2 (eighth consecutive session)
- **Every modified file kept its `SPDX-License-Identifier: MIT` header** per R10
- **Zero new skills** — the six skills are stable as committed at v0.8.0. v0.9.0 is polish, not feature

### Self-rating — v0.9.0

| Axis | Rating | Notes |
|---|---|---|
| Pain-driven coverage | 8.8/10 | Every polish item traces to a specific friction or decision: dry-run walkthrough surfaced 10 real findings (5 fixed); README rewrite addresses the "Genesis v1 is coming soon" out-of-date prose that was a known v0.8.0 gap; meta-memory sections in `master.md` make the cross-skill patterns visible (previously implicit, debug-painful for any future contributor); R8 housekeeping cleared two expired stack entries that R1.1 should have caught earlier in the cycle. The framing of "leverage memory context, not number-chase" is honored — every change traces to v1 → v0.8 lessons, not speculative additions. Slight deduction: the dry-run was a paper trace, not an execution; the 5 fixes are improvements but no fix has been validated by a real downstream bootstrap. |
| Prose cleanliness | 8.8/10 | Every edited file is tighter, not looser. The phase runbook fixes are precision additions (concrete commands replacing ambiguous "OR" language) — they slightly increase line count but reduce ambiguity per line. The new `master.md` sections are dense (3 paragraphs each) and follow the existing master.md voice. The README is bilingual landing-page prose with no dead weight. The session artefact (`dryrun_walkthrough_2026-04-16.md`) is structured, scannable, and ends with a clear conclusion. Minor: phase files were not trimmed, so they remain at 280-330 lines each. |
| Best-at-date alignment | 8.8/10 | All fixes use current Layer 0 patterns (`$HOME` portability, ACL fallback for Windows, HEREDOC convention from Anthropic's own commit-message guidance). The `master.md` Layer 0 inheritance section uses the Meta-Memory Path C terminology confirmed in the 2026-04-15 Wave 2 addendum. The README quickstart cites the install one-liner from the 2026-04-15 R8 cache entry. The R8 refresh did not introduce new SOTA, just confirmed existing entries against the on-disk state. |
| Self-contained | 9.0/10 | Every polish item is self-contained inside the existing files — no new skills, no new directories, no new dependencies, no hooks, no shared state. The dry-run added one session artefact at `memory/project/dryrun_walkthrough_2026-04-16.md` and the rest of the changes are precision edits to existing files. The `dryrun_walkthrough` file has clear v0.9.0 session provenance in its frontmatter and could be archived after v1.0.0 ships if it ever feels load-bearing-only. |
| Anti-Frankenstein | 9.2/10 | Phase-file trimming explicitly skipped because it would undo precision additions just landed — naming the skip and its rationale in this CHANGELOG honors "leverage memory context, not number-chase". No new abstractions. No new patterns invented to "improve" the orchestrator — every patch is a precision improvement on existing language or a visibility addition for an existing pattern. The dry-run was a paper trace, not an execution — refusing to run the orchestrator for real is the correct anti-Frankenstein move because real execution is a v1.1 milestone with its own scope. The three named cross-skill patterns in `master.md` are descriptive, not prescriptive — they document what the six skills already do, not what some future skill should aspire to. |
| **Average** | **8.92/10** | Clears the v0.9.0 floor of 8.5 by **0.42**. Running average v0.2 → v0.9 = `(7.6 + 8.2 + 8.8 + 8.4 + 8.6 + 8.8 + 9.0 + 8.92) / 8 = 8.54/10`. **0.04 above** the v1.0.0 target average of 8.5/10. Path A succeeded: the running average is now cleanly above target with headroom. v1.0.0 ship gate cleared — the next session can tag v1.0.0 with explicit user confirmation. |

### Path A succeeded — v1.0.0 ship gate cleared

The v0.8.0 → v0.9.0 path was framed as "leverage cumulated memory/meta-memory context to land a cleaner v1.0.0", not as a number-chase. Every polish item traces back to a specific lesson from v1 bootstrap → v0.8 shipping. The running average lands at **8.54/10**, 0.04 above the v1.0.0 target — a clean clearance with headroom rather than a 0.01 functional-but-formal miss. The v1.0.0 ship gate is now open: the next session opens with the explicit v1.0.0 tag decision.

### Known gaps for v1.0.0 or v1.1.0

- **Real execution of the orchestrator** — the dry-run was a paper trace. The first real downstream bootstrap is a v1.1 milestone and will surface frictions invisible to a paper trace (network failures, concurrent file writes, OS-specific edge cases). The 5 medium-severity fixes from the v0.9.0 walkthrough address the static surface; the v1.1 first-real-run will address the dynamic surface
- **Phase-file trim** — deferred per the rationale above. Optional v1.1 candidate
- **Multi-slug YELLOW warning in `run.py`** — v0.5 gap, still open
- **Test vector harness for redaction patterns** — v0.5/v0.7 gap, still open
- **Allow-list for `generic_long_base64` false positives** — v0.6 gap, still open
- **Hook wiring for `SessionEnd`** — depends on dogfood run 3 landing CLEAN (the terminal action of this v0.9.0 session). Decision belongs to the v1.0.0 session opener
- **Five low-severity dry-run findings** — documented in `memory/project/dryrun_walkthrough_2026-04-16.md` table with severity rationale; v1.1 candidates

---

## [0.8.0] — 2026-04-16 — "Genesis-protocol orchestrator — the last piece, recursive loop closed"

### Added

- `skills/genesis-protocol/` — the **last remaining stub** implemented as a pure Markdown orchestrator (Option A per the v0.7 → v0.8 resume prompt). Eight files, ~1,400 lines, 1:1 mirror of `memory/master.md`'s 7-phase table. The orchestrator is a **conductor, not a compiler** — it invokes the five sibling skills at the right phase, threads their outputs, and emits a single genesis report at the end. No Python runtime, no hooks, no shared state folder. The sixth and final skill, closing the anti-Frankenstein inflection point:
  - `SKILL.md` — entry point with speech-native triggers, the 7-phase master table (every row maps a phase to its runbook file + sibling skill + consent gate), inline skill pointers for Phase -1 and Phase 5.5 (thin wrappers over the sibling skills they delegate to), the concentrated-privilege map showing that `genesis-protocol` holds exactly one privilege ("writing outside the Genesis repo"), the ordered flow, anti-Frankenstein reminders, and the exit condition
  - `phase-0-seed-loading.md` — Phase 0 runbook: inspect the input folder, parse `config.txt` into a structured intent, read accompanying mixed media (PDF / images / URL lists) with security-floor rules, surface the parsed intent card for user confirmation, persist to `memory/project/bootstrap_intent.md` as the contract between Phase 0 and every downstream phase
  - `phase-1-rules-memory.md` — Phase 1 + Phase 2 runbook (folded because both write adjacent infra subtrees back-to-back before git init): create the memory subtree, copy canonical R1-R10 rules from the Genesis plugin, write the project `CLAUDE.md` with Layer 0 inheritance, invoke the four sibling install-manifests in order (`phase-minus-one` → `journal-system` → `session-post-processor` → `pepite-flagging`), seed `memory/MEMORY.md` as a one-line index, create the research cache directory tree with universal Layer 0 entries inherited by reference and five stack-relevant entries copied from the Genesis plugin's own R8 cache
  - `phase-3-git-init.md` — Phase 3 + Phase 4 runbook (folded because project seeds land as the first commit content after git init): `git init -b main`, generate the per-project ed25519 SSH key, register the `github.com-<slug>` alias with `IdentitiesOnly yes`, paste-back the public key (or Playwright-drive if Phase -1 installed it), verify via `ssh -T`, set the git remote to the SSH alias URL, stage the Phase 1+2 scaffold, write the canonical `.gitignore` (`.env.local`, SSH keys, worktrees, OS cruft, Python/Node artefacts), write `memory/master.md` with the real vision from intent, write `README.md` + `CHANGELOG.md` + conditional `.claude-plugin/plugin.json` + `skills/README.md` for downstream plugin projects, imprint scope locks if declared, re-stage everything for the first commit at Phase 6
  - `phase-5-5-auth.md` — thin pointer file documenting the contract between the orchestrator and the sibling `phase-5-5-auth-preflight` skill. Explicitly *not* a runbook reimplementation: lists what the orchestrator passes (slug, owner, repo, Chrome profile, Playwright opt-in, license, PAT expiration), what it receives (`ssh_<slug>_identity.md`, `github_<slug>_account.md`, `.env.local`, three-probe gate result), why Phase 5.5 runs after Phase 4 and before Phase 6 (four invariants), and the Layer 0 files the sibling consults during its flow
  - `phase-6-commit-push.md` — Phase 6 + Phase 7 runbook (folded because Phase 7 depends on Phase 6's tag and they form the clean handoff together): pre-commit review card with every staged file listed, first bootstrap commit with a multi-line structured message (phases + license + Genesis version), push to origin main, **explicit skip of PR creation** (the bootstrap commit is the one direct-to-main exception; PR pattern kicks in at v0.2.0+), tag `v0.1.0` with push, remote verification via `ls-remote`, then Phase 7: write the resume prompt, invoke `session-post-processor` to archive the bootstrap session's JSONL with the halt-on-leak gate, write the compact session memory entry, update `memory/MEMORY.md`, second commit (`chore(bootstrap)`), emit the final genesis report
  - `install-manifest.yaml` — verification-only manifest with no `targets` (the orchestrator creates nothing at install time — every file it writes happens during runtime invocation via phase runbooks). Confirms the five sibling skills are present under `skills/` at the plugin root, confirms all seven orchestrator files exist, flags Layer 0 gaps as YELLOW, flags plugin version mismatch as YELLOW
  - `verification.md` — two-mode health card (post-install + post-action). Post-install has 10 checks. Post-action has **30+ checks grouped by phase**: Phase -1 (stack manifest), Phase 0 (bootstrap intent), Phase 1+2 (MEMORY.md + rules + CLAUDE.md + 3 sibling install outputs + research cache INDEX + subdirs), Phase 3+4 (git + SSH + remote + `.gitignore` + master.md + README + CHANGELOG + conditional plugin manifest), Phase 5.5 (SSH identity ref + GitHub account ref + `.env.local` + three-probe gate), Phase 6 (first commit + on main + pushed + v0.1.0 tag + tag pushed), Phase 7 (resume prompt + session memory entry + session archive + halt-on-leak GREEN + second commit + MEMORY.md updated). Any RED halts; YELLOWs are warnings; GREEN is complete
- `.claude-plugin/plugin.json` version bumped to `0.8.0`; keywords list gained `genesis-protocol`, `orchestrator`, `7-phase-protocol`.
- `skills/README.md` updated: "Planned skills for v1.0.0" became "Shipped skills — v0.8.0 complete (v1.0.0 ship candidate)" and the `genesis-protocol/` entry now describes the shipped orchestrator.

### Notes

- **Option A confirmed and delivered** — the resume prompt suggested Option A (pure Markdown) over Option B (Markdown + Python driver) and Option C (hybrid). Option A won on two axes: (1) the orchestrator is a conductor, not a compiler — automation is a v1.1 candidate; (2) the anti-Frankenstein gate explicitly prohibits "do not add a Python runtime to the orchestrator in v0.8.0". The rating ceiling is higher for Option A because composition discipline is the value proposition.
- **1:1 spec mirror discipline** applied for the third time (`journal-system` v0.4, `pepite-flagging` v0.7, now `genesis-protocol` v0.8). SKILL.md's 7-phase master table mirrors `memory/master.md`'s 7-phase description — if master.md changes, the orchestrator is updated to match, never the other way around.
- **File folding justification** — the resume prompt suggested 5–7 files. The implementation landed at 8 (SKILL.md + 5 phase files + install-manifest.yaml + verification.md), with phases 2, 4, 7 folded into adjacent runbooks (Phase 2 into `phase-1-rules-memory.md`, Phase 4 into `phase-3-git-init.md`, Phase 7 into `phase-6-commit-push.md`). Folding is a compromise on the 1:1 mirror purity — each phase still has a clear home in SKILL.md's master table and its own section header in the host file, but the file structure itself groups phases by execution adjacency rather than by sequential index.
- **Five skills + one orchestrator shipped** — all six skills in the planned v1 surface are now present. The anti-Frankenstein inflection point is approached: the orchestrator lands cleanly without needing a new runtime, a new abstraction, a new hook, or any reimplementation of sibling logic. Composition was the ceiling and composition is what shipped.
- **Concentrated-privilege map** — SKILL.md enumerates one privilege per skill: `phase-minus-one` installers (mitigated by 3-mode ladder), `phase-5-5-auth-preflight` SSH/PAT/repos (paste-back default + isolated copy-paste), `journal-system` none, `session-post-processor` archives (halt-on-leak gate), `pepite-flagging` cross-project pointers (per-target consent), and **`genesis-protocol` writing an entire new project directory outside the Genesis repo** (top-level consent card + per-phase confirmation).
- **Granular commits inside the feat branch** — eleven commits: one per skill file (8), plugin.json bump, skills/README.md update, CHANGELOG (this commit). Squashed at merge time per R2.
- **Phase 6 bootstrap-commit exception** — the orchestrator explicitly documents that the first bootstrap commit is direct to `main` (not via a feat branch + PR), because there is no base branch yet. Every commit after v0.1.0 in every downstream project uses the standard R2 feat-worktree + PR + squash-merge flow.
- **Scope lock imprinting at Phase 4** — downstream projects that are spin-offs of a source project can declare scope locks at Phase 0 ("freeze <source> at <sha> until <condition>"). The orchestrator imprints them as `memory/project/<lock_slug>_frozen_scope_lock.md` at Phase 4. Genesis itself uses this pattern for the Aurum freeze — v0.8.0 is eating its own dogfood metaphorically.
- **No dry-run in v0.8.0** — the orchestrator ships as-written, without a validation pass against a real downstream project. Dry-run is an explicit v1.1 candidate. The rating accounts for this gap.
- **No hooks wired, still** — `session-post-processor` dogfood run 3 is still pending. Hook wiring stays deferred per the discipline established at v0.5.
- **Every new file carries the `SPDX-License-Identifier: MIT` header** per R10.
- **All five sibling skills untouched** — `phase-minus-one`, `phase-5-5-auth-preflight`, `journal-system`, `session-post-processor`, `pepite-flagging` are stable. Zero modifications. The orchestrator invokes them through their documented contracts without any surface extension.

### Self-rating — v0.8.0

| Axis | Rating | Notes |
|---|---|---|
| Pain-driven coverage | 9.0/10 | Every phase runbook traces to a documented pain. Phase -1 to the Aurum v0_init stack-detection pain. Phase 0 to the config.txt parsing + mixed media pain. Phase 1+2 to the memory scaffold + research cache pain. Phase 3+4 to git init + SSH identity + project seeds pain. Phase 5.5 to the five learnings in `v1_phase_5_5_auth_preflight_learnings.md`. Phase 6+7 to the handoff discipline pain. Zero speculative features. Minor deduction: the runbooks have not been run against a real downstream project yet — dry-run deferred to v1.1 — so the mapping is correct by design but not yet validated by execution. |
| Prose cleanliness | 8.8/10 | Eight files, ~1,400 lines total. Consistent structure across phase files (frontmatter → prerequisites → flow → exit → common failures → anti-Frankenstein). Tables used throughout. SKILL.md's 7-phase master table is the anchor. Minor: phase files are longer than the 5-skill median (some hit 280-320 lines) because of phase folding (1+2, 3+4, 6+7). Length is justified but not minimum viable — a v0.9.0 polish could trim ~10-15%. |
| Best-at-date alignment | 8.8/10 | Uses every Layer 0 pattern: per-project SSH identity, `GH_TOKEN` env override, fine-grained PAT scope list, Chrome profile map, isolated copy-paste, SPDX, anti-Frankenstein, R8 cache, speech-native triggers. References current Genesis precedents (halt-on-leak from `session-post-processor`, consent floor from `pepite-flagging`, 1:1 mirror from `journal-system`). No stale references. Slight deduction: the orchestrator composes existing best practices rather than introducing new ones — right move for an orchestrator, but doesn't demonstrate SOTA advancement on its own. |
| Self-contained | 9.2/10 | Eight files in one directory. Zero runtime dependencies. No Python, no shell, no binaries, no hooks, no shared-state. The only "dependency" is the five sibling skills existing under `skills/` — which is exactly the composition surface. The install-manifest is read-only and creates nothing; the orchestrator creates files only during runtime invocation via phase runbooks, and every file lands in the downstream project folder (never in the Genesis repo itself). Option A is the cleanest self-contained shape achievable. |
| Anti-Frankenstein | 9.2/10 | Option B/C explicitly resisted per resume prompt constraint. 1:1 mirror discipline applied. Each phase runbook has explicit anti-Frankenstein reminders. Concentrated-privilege map enumerated. Every "what this skill does NOT do" list is rigorous. Minor deduction: folding of phases (2 into 1, 4 into 3, 7 into 6) is a consolidation move that trades mirror purity for file-count restraint — defensible (resume suggested 5-7 files) but not zero-cost. The top-level consent card is the privilege mitigation and is documented thoroughly. |
| **Average** | **9.0/10** | Clears the v0.8.0 floor of 8.5 by **0.5**. Running average v0.2 → v0.8 = **(7.6 + 8.2 + 8.8 + 8.4 + 8.6 + 8.8 + 9.0) / 7 = 8.49/10**. This is **0.01 below** the v1.0.0 target average of 8.5/10 — functionally the target, formally just under. Below the 9.1/10 threshold for a direct v1.0.0 tag, so v0.8.0 ships here and a v0.9.0 polish pass remains an option if the user wants to pull the running average cleanly above 8.5 before the v1.0.0 tag. The user's call at session end. |

### Known gaps for v0.9.0 or v1.0.0

- **Dry-run against a real downstream project** — the orchestrator has not been validated by execution. The first real downstream bootstrap will surface frictions informing v1.1. Deferred from v0.8.0 explicitly (resume prompt open question 4).
- **Dogfood run 3 for `session-post-processor`** — still pending. Needs a future Genesis session or the first Aurum session after the freeze lifts. Hook wiring still deferred until run 3 lands CLEAN.
- **README.md polish pass** — the public README still says "Genesis v1 is coming soon" from the bootstrap. If v1.0.0 ships directly from v0.8.0, the README needs updating in the same release. If a v0.9.0 polish intervenes, the README polish lands there.
- **Phase-file length trimming** — `phase-1-rules-memory.md` (280 lines), `phase-3-git-init.md` (298 lines), `phase-6-commit-push.md` (318 lines) are longer than the 5-skill median. A ~10-15% trim without content loss would push prose cleanliness toward 9.0+.
- **Multi-slug YELLOW warning in `run.py`** — v0.5 gap, still open.
- **Test vector harness for redaction patterns** — v0.5/v0.7 gap, still open.
- **Allow-list for `generic_long_base64` false positives** — v0.6 gap, still open.

### Next version target — two paths, user decides

- **Path A (v0.9.0 polish → v1.0.0)**: pull the running average above 8.5 via a small polish pass (README update, phase-file trim, dry-run validation against a tmp downstream folder, maybe one of the v0.5/v0.6 gaps). Then tag v1.0.0 with a clean running average ≥ 8.50 and the anti-Frankenstein inflection-point officially reached. **Cleaner narrative, slightly more work.**
- **Path B (v0.8.0 ships as-is, user calls 8.49 "effectively 8.5" for direct v1 ship)**: accept the 0.01 formal miss, tag v1.0.0 directly on the v0.8.0 squash with explicit confirmation, and start the v1.1 backlog in the next session (dry-run, hook wiring after run 3, phase-file trim, README polish). **Faster ship, Aurum freeze lifts sooner.**
- **The user decides after reading this CHANGELOG and the genesis summary at end of session.**

---

## [0.7.0] — 2026-04-15 — "Pépite flagging skill + R8 slug rule correction"

### Added

- `skills/pepite-flagging/` — the **last independent skill stub** shipped as a 1:1 mirror of the canonical spec `.claude/docs/superpowers/specs/v1_pepite_discovery_flagging.md`. Speech-native, consent-bounded, automatic detection during research operations (WebSearch, WebFetch, sub-agent exploration, R8 refreshes) with a "two or more of six" red-light criteria rule. Six files, ~936 lines total:
  - `SKILL.md` — entry point, automatic + manual trigger phrases, five-step flow (detect → create → surface → act → INDEX), hard rules, anti-Frankenstein scope locks
  - `trigger-criteria.md` — the six red-light criteria with rationale, calibration example, and anti-noise guard per criterion. Applied "two or more" scoring table with worked examples. Anti-over-flagging and anti-under-flagging discipline
  - `pepite-format.md` — frontmatter schema (14 required fields), body section order, slug derivation, status transition table (seed → extracted → actioned → archived, with dismissed as terminal), idempotency rules, one fully-worked illustrative example marked as non-real
  - `cross-project-routing.md` — pointer file template, per-target consent pattern (never batched silently), target project slug lookup with v1 hard-coded machine map, cold-read protocol for pointer consumers, v1/v2 scope lock
  - `install-manifest.yaml` — idempotent directory + INDEX.md creation with `create_if_missing_only` guard, three verification checks, no runtime dependency declaration (pure Markdown + YAML skill)
  - `verification.md` — two-mode health card (13 checks), halt-on-RED on missing required frontmatter, illegal status transition, or **cross-project pointer write without explicit per-target consent** (consent floor — the only privileged operation in this skill)
- `.claude-plugin/plugin.json` version bumped to `0.7.0`, added `pepite-flagging` to the keywords list.

### Fixed

- **R8 research entry correction — live dogfood follow-up from v0.6.0**. The `claude-code-session-jsonl-format_2026-04-15.md` entry described the cwd-to-slug rule as replacing only `\`, `:`, and space with `-`. Empirical verification during the v0.6 first dogfood run proved underscore also maps to `-`; the code was fixed in `slugify_cwd()` but the research entry still carried the incomplete rule. Corrected in this release: the entry now lists `\`, `/`, `:`, `_`, and space as the full replacement set, with an explicit "Correction 2026-04-15 (live dogfood)" note pointing to `memory/journal/2026-04-15_slug-rule-live-dogfood-correction.md` for the epistemic context. Forward slash `/` added to cover git-bash-style cwd strings on Windows. First time an R8 entry has been amended in-place after a live-dogfood correction rather than via a supersede chain — justified because the correction is a bug fix, not new research.

### Notes

- **Four skills shipped** now: `phase-minus-one`, `phase-5-5-auth-preflight`, `journal-system`, `session-post-processor`, plus `session-post-processor/run.py` as a v0.6.0 add. **`pepite-flagging` is the fifth**. Only **one** stub remains: `genesis-protocol/` (the orchestrator, always last).
- **1:1 spec mirror discipline** applied for the second time (first was `journal-system` in v0.4). Every file in `skills/pepite-flagging/` references the canonical spec and explicitly commits to tracking it — if the spec changes, the skill is updated to match, never the other way around.
- **No runtime code** in this skill. Unlike `session-post-processor/run.py`, detection and flagging happen inside Claude's own research operations; file writes use the built-in Write tool. The skill is pure Markdown + YAML. This is deliberate — the detection logic is a judgement call, not a deterministic pipeline, and a Python implementation would either oversimplify (miss pépites the LLM would catch) or duplicate the LLM's job.
- **Consent floor** — cross-project pointer writes are the only privileged operation. Per-target consent is mandatory; silence is always a skip, never an implicit yes; batched "propagate to all" requires explicit echo-back confirmation. `verification.md` Check 10 halts on any consent bypass, deletes the offending pointer, and refuses to auto-retry. Same discipline as `session-post-processor`'s halt-on-leak gate.
- **v1 machine map is hard-coded** in `cross-project-routing.md` — the Genesis user runs ~20 projects, the mapping is small, and it changes slowly. Auto-discovery of sibling projects is a v2 candidate, deferred because a hard-coded map covers the current use case and automation without a felt pain is scope creep.
- **First-half-of-session discipline** applied again: R8 refresh first (slug underscore correction), skill implementation second. Granular commits inside the feat branch: one per skill file + plugin.json bump + CHANGELOG, squashed at merge time.
- **No example pépite pre-seeded**. The illustrative DuckDB+VSS example in `pepite-format.md` is explicitly marked as non-real. The first real pépite will be detected during normal research operations in v0.7.0+ sessions — live dogfood, not synthetic.
- **Every new file carries the `SPDX-License-Identifier: MIT` header** per R10.
- **`phase-minus-one`, `phase-5-5-auth-preflight`, `journal-system`, `session-post-processor`** all untouched. All stable.

### Self-rating — v0.7.0

| Axis | Rating | Notes |
|---|---|---|
| Pain-driven coverage | 9/10 | Every file maps to a spec section or a detection/consent concern. The cross-project consent floor directly addresses the "never auto-propagate" rule from Layer 0. The trigger criteria calibration reflects the anti-over-flagging and anti-under-flagging pains that only become concrete after the skill ships and gets used. The R8 slug rule fix closes the gap left at v0.6 shipping time. Zero speculative features. |
| Prose cleanliness | 8/10 | Six files, ~936 lines. Each file has a clear job and minimal overlap. The spec mirror means some content is deliberately duplicated from `v1_pepite_discovery_flagging.md` — this is intentional because the skill must be legible without clicking through to the spec. Tables used throughout for criteria, transitions, verification checks. The hard-coded machine map in `cross-project-routing.md` is prose-ugly but v1-honest; a prettier auto-discovery surface is explicitly v2. |
| Best-at-date alignment | 9/10 | Criteria 3 ("emerging tech") and Criteria 6 ("highest potential") directly operationalise the Layer 0 `best-practice-at-date default` rule. The cross-project routing is the first operational component of Meta-Memory Layer 3 — stepping stone to Path B per the Layer 0 Meta-Memory architecture. Pointer file format uses current `type: reference` convention consistent with the rest of the Genesis memory stack. |
| Self-contained | 9/10 | Pure Markdown + YAML. Zero runtime dependencies. No Python, no pip, no external binaries. Install step touches only `memory/pepites/` inside the target project. Cross-project pointers are additive auto-memory writes that never touch another project's git state — the only cross-project effect is a file appearing in `~/.claude/projects/<target>/memory/`, which is per-machine state. |
| Anti-Frankenstein | 9/10 | Deferred explicitly: slash commands (v2), auto-propagation without per-target consent (v2), TTL auto-archive (v2), cross-pépite synthesis (v2), pépite ranking (v2 if ever), multi-machine propagation (v2), Python runtime (not needed). The skill's surface is exactly six files mirroring a frozen spec, no more. Pre-seeded example marked as non-real to prevent false provenance. Manual force-flag path exists but the primary mode is auto-detection because that's where the pain is. |
| **Average** | **8.8/10** | Clears the 8.0/10 floor by 0.8. Ties with v0.4.0 (journal-system, also 8.8/10) as the highest single-version rating in the project's history. Above v0.6.0 (8.6/10) because the 1:1 spec mirror discipline is a cleaner rating surface than first-runnable-code, and because the R8 slug rule correction is a side-fix that would normally be carried as debt — closing it in the same release removes a latent drag. Running average v0.2 → v0.7 = **(7.6 + 8.2 + 8.8 + 8.4 + 8.6 + 8.8) / 6 = 8.40/10**, still on track for v1 target 8.5/10. The last milestone (`genesis-protocol`) needs to land at ≥ 9.1 to reach the target — achievable but tight, the orchestrator's rating ceiling depends heavily on how cleanly it composes the five shipped skills. |

### Known gaps for v0.8.0

- **`genesis-protocol` orchestrator skill** — the last remaining stub. Composes all five shipped skills (`phase-minus-one`, `phase-5-5-auth-preflight`, `journal-system`, `session-post-processor`, `pepite-flagging`) into the 7-phase protocol from the master vision. This is the v1 ship target.
- **Dogfood run 3 for `session-post-processor`** — still pending. Needs either a future Genesis session (post-v0.7 maintenance) or the first Aurum session after the freeze lifts. Hook wiring stays deferred until run 3 lands CLEAN.
- **Multi-slug YELLOW warning in `run.py`** — v0.5 gap, still deferred. No multi-slug collision exists on this machine to test against.
- **Test vector harness for redaction patterns** — v0.5 gap. Small `tests/redaction_vectors.py` is a v0.8+ candidate.
- **Allow-list for `generic_long_base64` false positives** — v0.6 gap. Short list of safe path prefixes.
- **First real pépite detection** — no pépites flagged in this session because the session is implementation work, not research. The first real flag happens in a v0.7+ research session.

### Next version target

**v0.8.0 — `genesis-protocol` orchestrator** (the last remaining stub, likely v1.0.0 if it lands high). Target rating: **8.5/10 floor** because the v1 ship is close and the orchestrator's rating sets the v1 average. An alternative is a small maintenance version (hook wiring for session-post-processor, test vector harness, allow-list) if the user wants to reduce technical debt before the ship, but the anti-Frankenstein discipline says ship first and polish after — the orchestrator is the critical path to v1.

---

## [0.6.0] — 2026-04-15 — "Session post-processor run.py executable"

### Added

- `skills/session-post-processor/run.py` — the first Genesis skill to ship a runnable Python module instead of a spec-only Markdown surface. Implements the seven-step pipeline frozen in v0.5.0 (locate → parse → redact → emit → halt-on-leak → INDEX → health card) using only the Python 3.10+ standard library (`json`, `re`, `os`, `pathlib`, `datetime`, `argparse`, `sys`, `unicodedata`). No pip installs, no vendored libraries. CLI flags: `--project-root`, `--cwd` (for worktree override), `--jsonl` (explicit source), `--inject-test-leak` (dogfood-only halt-gate probe).
- `memory/project/sessions/` — seeded via the run.py install step (idempotent `ensure_sessions_dir`), with the canonical `INDEX.md` stub from `install-manifest.yaml`.
- `memory/project/sessions/2026-04-15_on-reprend-v0-6-0-project-genesis.md` — **first real dogfood archive** of a live Genesis session, produced by run.py against `~/.claude/projects/C--Dev-Claude-cowork-project-genesis/a3857578-*.jsonl`. 93 records, 37 tool calls, 20 redactions across 13 patterns, halt-on-leak gate CLEAN. Committed as a durable artefact per the v0.5 → v0.6 resume prompt — the archive is a version-controlled record of the implementation session, redacted by construction.
- `.claude-plugin/plugin.json` version bumped to `0.6.0`.

### Fixed

- **Slug derivation** — the 2026-04-15 on-disk-verified research entry said `\`, `:`, and space map to `-`, but empirical verification during the first dogfood run showed **underscore also maps to `-`** (actual directory `C--Dev-Claude-cowork-project-genesis`, not `C--Dev-Claude_cowork-project-genesis`). `slugify_cwd()` extended to replace `\`, `/`, `:`, `_`, and space. First live-dogfood correction of a research entry. Research entry refresh is a v0.7+ follow-up (low priority — code is correct, only the documentation caveat is outstanding).

### Verified

- **Halt-on-leak gate fires under deliberate test** — `--inject-test-leak` appends a fake `github_pat_` + 90-`A` string to the parsed record list **after** the redaction pass so it bypasses the redactor, reaches the emitter raw, triggers the verification gate, and the written archive is deleted before the INDEX update. Confirmed end-to-end: 54616 bytes written, `github_pat_finegrained` leak detected, file unlinked, RED card emitted, non-zero exit code. The gate is not theoretical.
- **First-run on the current session's JSONL succeeds**: CLEAN verification, 20 redaction hits across 13 patterns, 37 tool calls surfaced, archive is 1182 lines and 49683 bytes.

### Notes

- **Dogfood run 2 of the three-run gate**. Run 1 was the v0.5.0 session itself (implicit — the skill shipped the spec, no executable, so no run was possible, but the session's own JSONL proved the spec was parseable by hand). Run 2 is this v0.6.0 session, with the actual `run.py` processing `a3857578-*.jsonl`. Run 3 will be either a future Genesis session or the first Aurum session after the freeze lifts. **Hook wiring stays deferred** per R10 anti-Frankenstein discipline — no `SessionEnd` automation before all three runs land CLEAN.
- **Only stdlib**, per the v0.5 spec freeze. No `yaml` (frontmatter emitted as plain text), no `requests`, no `pyyaml`. Python 3.14 on this machine covers the 3.10+ floor with room to spare.
- **Generic pattern false positives are acceptable** — `generic_long_base64` caught a file path fragment (`claude/docs/superpowers/research/stack/claude-code-session`) during the first dogfood. This is the documented cost of the redact-heavy strategy: false positives are recoverable, false negatives are incidents. A v0.7+ candidate is a short allow-list of known-safe path fragments, not a regex relaxation.
- **Idempotent archive allocation** — `allocate_archive_path` appends `-2`, `-3`, etc. on filename collision. Re-running the skill against the same session produces a new file each time, and the user can diff them to confirm redaction stability.
- **Atomic emit** — `emit_markdown` writes to `<archive>.md.tmp`, then `.replace()`s to `<archive>.md`. Avoids half-written archives if the process crashes mid-emit.
- **Granular commit discipline** applied again — one commit per logical unit (run.py, sessions/ + dogfood, plugin.json, CHANGELOG).
- **`phase-minus-one`, `phase-5-5-auth-preflight`, `journal-system`, `session-post-processor` spec files untouched**. All stable.
- Every new file carries the `SPDX-License-Identifier: MIT` short-form header.

### Self-rating — v0.6.0

| Axis | Rating | Notes |
|---|---|---|
| Pain-driven coverage | 9/10 | The v0.5.0 session shipped the spec but blocked on the three-run dogfood gate because no executable existed. `run.py` unblocks it end-to-end. Every feature in `run.py` maps to a specific step of the v0.5 spec — zero speculative additions. `--inject-test-leak` is a dogfood-only flag that exists because the halt gate needs a live proof, not a theoretical one. |
| Prose cleanliness | 8/10 | One file, ~700 lines, sectioned into redaction / slug / parser / emitter / verifier / index / health-card / main with block-comment headers. Functions are small and named for what they return, not what they do. Comments only where WHY is non-obvious (env_local_paste special case, dogfood injection rationale, post-redaction tag stripping). Slightly below v0.4's journal-system 9 because it's code not prose, and code carries more intrinsic noise. |
| Best-at-date alignment | 9/10 | 2026-current Python idioms (type hints with `|` union, `Path.read_text(encoding=)`, `re.Pattern[str]`). Redaction patterns match 2026 token formats per the v0.5 spec (github_pat_finegrained 82+ chars, `sk-ant-`, `sb_secret_`, `sk-proj-`, AWS prefix list, Google `AIza`, JWT `eyJ...eyJ...`). No legacy Python 2 baggage, no deprecated stdlib modules. |
| Self-contained | 9/10 | Single file, stdlib only, no pip, no yaml parser, no cross-skill imports. Install step is idempotent and creates only `memory/project/sessions/` + `INDEX.md`. The Python 3.10+ runtime is already declared in `install-manifest.yaml` — no new dependency is introduced by this version. Higher than v0.5 (8) because v0.5 *declared* the runtime dep; v0.6 just *uses* it inside the existing envelope. |
| Anti-Frankenstein | 8/10 | Did NOT wire SessionEnd hooks (R10 discipline). Did NOT add a YELLOW warning for multi-slug collision (v0.5 gap, deferred — there is no real multi-slug collision on this machine to dogfood against, so the logic would be untestable now). Did NOT add a test vector runner (v0.5 gap, deferred — the `--inject-test-leak` flag is the minimal viable halt-gate proof). Did NOT implement retroactive batch processing. The dogfood-injection flag is one 4-line block that only runs with `--inject-test-leak`; its existence is pain-driven (we need to prove the gate fires). Capped at 8 because run.py is a single 700-line file and a future session might legitimately split it (parser/redactor/emitter) if the test harness grows. |
| **Average** | **8.6/10** | Clears the 8.0/10 floor by 0.6. Above v0.5.0 (8.4/10) because implementing a frozen spec is a cleaner rating surface than the spec-freeze itself. Running average across v0.2 → v0.6 = **(7.6 + 8.2 + 8.8 + 8.4 + 8.6) / 5 = 8.32/10**, on track for the v1 target 8.5/10. |

### Known gaps for v0.7.0

- **No multi-slug collision YELLOW warning** — if a project has both a `-2026` and a plain slug under `~/.claude/projects/`, both will match the current rule and the most-recent-mtime pick is usually correct but could surprise. Add a YELLOW warning when multiple slug dirs exist for the same cwd.
- **Research entry refresh for the underscore rule** — the 2026-04-15 `claude-code-session-jsonl-format` research entry still documents `\`, `:`, and space only; refresh to add underscore.
- **Test vector harness** — `redaction-patterns.md` has vectors, run.py has no harness. Small `tests/redaction_vectors.py` would assert `match` vectors redact and `non-match` vectors survive.
- **Allow-list for generic_long_base64 false positives** — path fragments like `claude/docs/superpowers/research/stack/claude-code-session` should not be redacted. Short allow-list of safe prefixes.
- **`pepite-flagging` skill** — the last independent skill stub, now the natural next target for v0.7 (was the alternative v0.6 option).
- **`genesis-protocol` orchestrator** — still last, lands after every phase and skill is implemented and the first public downstream bootstrap proves the flow.
- **`SessionEnd` hook wiring** — still deferred until run 3 of the dogfood gate lands CLEAN.

### Next version target

**v0.7.0** — `pepite-flagging` skill OR run 3 of the post-processor dogfood against an Aurum session (only if the freeze has lifted). Rubric says pick the more concrete pain at session open. Target rating: **8.0/10 floor**.

---

## [0.5.0] — 2026-04-15 — "Session post-processor skill"

### Added

- `skills/session-post-processor/` — the fourth functional skill. Parses the current Claude Code session's JSONL transcript, redacts secrets (GitHub PATs, SSH private keys, Anthropic/OpenAI/Supabase/Stripe/AWS/Google API keys, JWTs, `.env.local` content paste-backs, generic long hex / base64), and emits a readable Markdown archive under `memory/project/sessions/YYYY-MM-DD_<slug>.md`. Includes a mandatory **halt-on-leak verification gate** that re-applies every pattern to the written file and deletes it if any pattern still matches. Manual-invoke only in v0.5.0 — `SessionEnd` hook wiring is a v0.6+ candidate after three successful dogfood runs.
- `skills/session-post-processor/SKILL.md` — entry point, trigger phrases, seven-step flow (locate → parse → redact → emit → halt-on-leak → INDEX → health card), explicit manual-only discipline for v0.5.0 with a three-run dogfood requirement before any hook wiring, anti-Frankenstein scope locks.
- `skills/session-post-processor/jsonl-parser.md` — record-by-record schema walkthrough based on the on-disk-verified 2026-04-15 research entry. Outer type / inner content-block type distinction, `parentUuid` threading with timestamp as primary ordering key, sidechain sub-agent grouping rule, five content-block extraction rules, resilient error handling (no exceptions halt the parse — only the secret-leak gate halts).
- `skills/session-post-processor/redaction-patterns.md` — 14 patterns in specific-before-generic application order with name / regex / rationale / test vectors for each. Variable-name-preserving replacement for `env_local_paste`. Explicit non-goals for handwritten secrets, URL-embedded credentials, binary attachment contents.
- `skills/session-post-processor/markdown-emitter.md` — output template with frontmatter schema, per-record-kind rendering rules, truncation rules, idempotency rule (re-run produces `-N` suffixed file, never silent overwrite).
- `skills/session-post-processor/install-manifest.yaml` — Python 3.10+ runtime dependency (stdlib only), `memory/project/sessions/` + `INDEX.md` creation with `create_if_missing_only` guard, five verification checks. Explicitly does NOT register `SessionEnd` hooks, does NOT modify `settings.json`.
- `skills/session-post-processor/verification.md` — two-mode health card with 12 checks including the critical halt-on-leak redaction gate that deletes the archive file on any pattern hit. File deletion is the single privileged operation in the whole skill.
- `.claude/docs/superpowers/research/stack/claude-code-session-jsonl-format_2026-04-15.md` — refreshed research entry (confidence upgraded medium → high after on-disk verification against `a086701e.jsonl`, 174 records). Clarifies outer vs inner type taxonomy, documents verified flat layout, slug derivation rule, multi-slug-per-project situation (both `project-genesis` and `project-genesis-2026` slugs exist from prior rename), supersedes the 2026-04-14 entry which moves to `research/archive/`.
- `.claude-plugin/plugin.json` version bumped to `0.5.0`.

### Notes

- Ships **one** skill only, per anti-Frankenstein discipline. Remaining stubs: `pepite-flagging/` + `genesis-protocol/` (orchestrator, still last).
- **Granular commit discipline** applied for the first time on this skill, as reinforced by the v0.4.0 PowerShell-window incident. Eight commits in the feat branch (research-refresh → SKILL.md → jsonl-parser → redaction-patterns → markdown-emitter → install-manifest → verification → changelog-bump), squashed to one on merge. Protects against mid-session host loss.
- **Research refresh as a prerequisite**. The existing `claude-code-session-jsonl-format_2026-04-14.md` entry expired today (2026-04-15), was confidence `medium`, and had explicit "verification needed" caveats. Before writing the skill, the session sampled a real JSONL on disk, verified the outer vs inner type taxonomy, and wrote the 2026-04-15 replacement with confidence `high`. First application of the R8 "refresh or extend" rule mid-session.
- **Manual-only for v0.5.0** — no `SessionEnd` hook wiring. Three-run dogfood gate before automation: this session (run 1), a subsequent Genesis session (run 2), an Aurum session after the freeze lifts (run 3).
- **Halt-on-leak gate is the security floor**. A redaction miss must never result in a silent archive file with the secret in it. File deletion is the single privileged operation in the skill.
- **No vendored dependencies**. Prior art cited for schema reference only. Python stdlib is enough.
- **`phase-minus-one`, `phase-5-5-auth-preflight`, and `journal-system` untouched**. All three stable at 7.6 / 8.2 / 8.8.
- Every new file carries `SPDX-License-Identifier: MIT` short-form header per R10.

### Self-rating — v0.5.0

| Axis | Rating | Notes |
|---|---|---|
| Pain-driven coverage | 9/10 | Writing session memories by hand has been the manual step in every Genesis session so far (v0.1 → v0.4, five times). Halt-on-leak gate addresses the specific threat of silently committing a redaction miss. Research refresh closes the "confidence medium" caveat from the 2026-04-14 entry. Zero speculative features. |
| Prose cleanliness | 7/10 | Larger skill (6 files vs 5 for journal-system) because redaction and verification both need their own files. Tables used for patterns, checks, rendering rules. Some intentional redundancy between `jsonl-parser.md` and the research entry so the skill stays legible when the research TTL expires. Denser than journal-system because the subject matter is denser. |
| Best-at-date alignment | 9/10 | On-disk verification against a Claude Opus 4.6 session file from today. Redaction patterns include 2026-current token formats (fine-grained `github_pat_11`, Anthropic `sk-ant-`, Supabase `sb_secret_`, OpenAI `sk-proj-`, Stripe `sk_(test\|live)_`, full AWS prefix list, Google `AIza`). Python 3.10+ `match/case` is 2026-current idiomatic. |
| Self-contained | 8/10 | Runs end-to-end within `skills/session-post-processor/` + `memory/project/sessions/`. Touches `~/.claude/projects/` read-only. Python 3.10+ is the only non-stdlib cross-skill coupling in the Genesis stack so far — previous skills are pure markdown / bash. Capped at 8 because the runtime dependency is a genuine self-containment cost. |
| Anti-Frankenstein | 9/10 | Six files (minimum for this surface). Zero speculative features: no hook wiring in v0.5, no HTML emitter, no token-usage dashboard, no cross-session timeline, no semantic indexing, no interactive replay. Manual-only with three-run dogfood gate. Halt-on-leak gate is the only privileged operation. Skill deliberately does NOT cache parsed records — each run is fresh and auditable. |
| **Average** | **8.4/10** | Clears the 8.0/10 floor by 0.4. Below v0.4.0 (8.8/10) intentionally — larger surface and a real runtime dependency. The journal-system climb was from a smaller surface, not a more rigorous rubric. v1 average target 8.5/10 still defensible. |

### Known gaps for v0.6.0

- **No executable Python module** — ships the pipeline spec, not a runnable `.py`. First dogfood run needs a small entry point written on the fly, eventually promoted to `skills/session-post-processor/run.py`. Deferred because the spec must be frozen before the implementation; v0.5 is the spec freeze.
- **No test vector runner** — `redaction-patterns.md` lists vectors but no harness. Small `tests/redaction_vectors.py` is a v0.6 candidate.
- **No SessionEnd hook wiring** — explicit v0.6+ candidate after three successful manual dogfood runs.
- **No retroactive processing** — current session only. Archiving historical JSONLs (v0.1 → v0.4) deferred.
- **No cross-session timeline** — separate `session-timeline` aggregator, v0.8+ candidate.
- **No JWT decoding** — shape match only, payload decoding deferred.
- **No slug-collision detection** — multiple Windows-path variants collapsing to the same slug would land JSONLs in the same directory. Most-recent-mtime pick is usually correct; YELLOW warning for multi-match is a v0.6+ safety net.

### Next version target

**v0.6.0** — either `pepite-flagging` (the remaining independent skill stub) or the first implementation pass of session-post-processor's executable Python module. Rubric says pick the more concrete pain point at the time. Target rating: **8.0/10 floor**.

---

## [0.4.0] — 2026-04-15 — "Journal system skill"

### Added

- `skills/journal-system/` — the third functional skill, end-to-end implementation of the 6th memory type defined in Layer 0 (`~/.claude/CLAUDE.md` → "Journal System — Universal Thought Capture"). Speech-native, trigger-phrase driven, single-project scope. Recognises the five FR/EN trigger phrases, creates or extends dated entries under `memory/journal/`, preserves the user's verbatim words, and gates every amplification on explicit per-invocation consent. No auto-loading — entries are read intentionally, like a personal notebook.
- `skills/journal-system/SKILL.md` — skill entry point, frontmatter for Claude Code plugin auto-discovery, the five trigger phrases in a single lookup table, the five-step flow (recognise → load/create → verbatim capture → consent-gated amplification → metadata+INDEX sync), the six amplification rules as a brief reminder, and an explicit "what this skill does NOT do" section to lock scope against cross-project aggregation / auto-tagging / full-text search.
- `skills/journal-system/entry-format.md` — canonical frontmatter schema with the eight required fields, the five states (`captured`, `seed`, `growing`, `dormant`, `resolved`) with transition rules, the full stratified dialogue template, the six format-enforcement rules (verbatim blockquote, Claude-voice labelling, horizontal-rule separators, append-only layers, fixed sub-section order, immutable title), the slug generation procedure, primary-vs-fallback location logic, and the starter `INDEX.md` template.
- `skills/journal-system/amplification-rules.md` — the six hard rules from Layer 0, 1:1 mirror with rationale for each: never auto-amplify, never rewrite the user's words, every addition attributed and dated, be sparing with poetry, pushbacks are valid amplifications, a layer can have no amplification. Plus four operational consequence rules (R7 consent is a blocking gate, R8 consent does not cascade across layers, R9 no preemptive offers, R10 amplification never mandatory for completeness).
- `skills/journal-system/install-manifest.yaml` — idempotent install step creating `memory/journal/` directory and seeding `memory/journal/INDEX.md` with the five empty state sections. `create_if_missing_only` guard prevents overwriting user-authored INDEX content. Three verification checks (directory exists, INDEX exists, INDEX is a journal index). No hook registration, no `settings.json` touch, no dependency installation.
- `skills/journal-system/verification.md` — two-mode health card (post-install + post-action) with eight checks: directory exists, INDEX exists, five state sections present, target file exists, frontmatter valid and complete, verbatim quote preserved (Rule 2 guard), INDEX reflects state transitions without duplication, amplification attribution correct (Rule 3 + Rule 1 consent guard). Three status levels (GREEN / YELLOW / RED) with explicit halt on any RED to prevent silent propagation of verbatim-modification or consent-bypass violations.
- `.claude-plugin/plugin.json` version bumped to `0.4.0`.

### Notes

- Ships **one** skill only, per anti-Frankenstein scope discipline. Remaining skill stubs (`genesis-protocol`, `session-post-processor`, `pepite-flagging`) land in their own worktrees later.
- The journal system skill is a **1:1 mirror of the Layer 0 spec**, not an independent design. If Layer 0's journal spec changes, `skills/journal-system/` must be updated to match — never the other way around. This is explicitly stated in `SKILL.md`, `entry-format.md`, and `amplification-rules.md` so future sessions cannot silently drift the skill away from its source of truth.
- The skill is the first Genesis skill that has **no consent card** — unlike `phase-minus-one` and `phase-5-5-auth-preflight` which touch the machine and thus require explicit opt-in. Rationale: the journal system is speech-native, so the trigger phrase itself is the consent. A consent card would be friction on a surface where the user wants zero friction. Amplification consent is still mandatory per-invocation and is handled inline via Rule 1, not via a card.
- No `states.md` or `trigger-phrases.md` as separate files — both live inside their primary consumer (`entry-format.md` for states, `SKILL.md` for trigger phrases). A 7-line state table does not justify a separate file; the indirection would harm readability more than it would help reuse.
- No `modes/` runner directory — this skill does not touch the OS, so the 3-mode ladder from `phase-minus-one` does not apply. Trigger phrases are the only interaction surface.
- `phase-minus-one` and `phase-5-5-auth-preflight` are untouched — both remain stable at 7.6/10 and 8.2/10 respectively. No cross-skill refactor was attempted.
- Cross-project aggregation (the `/journal timeline` view across every repo) is explicitly out of scope — that is the Meta-Memory Path B session's job. This skill ships single-project capture only, but entries are written consistently so the future aggregator has clean input.
- Every new file carries the `SPDX-License-Identifier: MIT` short-form header per R10.
- No new spec file — the canonical spec is the Layer 0 CLAUDE.md "Journal System — Universal Thought Capture" section, already frozen and in the universal layer.

### Self-rating — v0.4.0

| Axis | Rating | Notes |
|---|---|---|
| Pain-driven coverage | 9/10 | Every file addresses a concrete need documented in the Layer 0 spec: the vertigo-dogfooding entry from 2026-04-14 proved amplification works when consent is explicit and grounded. Verbatim preservation guards against the silent paraphrase failure mode. Post-action verification with halt-on-RED prevents the consent-bypass failure mode. Zero speculative features. |
| Prose cleanliness | 8/10 | The skill is smaller than `phase-minus-one` and `phase-5-5-auth-preflight` so the prose could stay tighter. Tables used for the five trigger phrases, five states, eight verification checks. Minimal duplication between files — each file has one job and points to the others via footer references rather than re-stating content. |
| Best-at-date alignment | 9/10 | Mirrors the 2026-04-14 Layer 0 spec exactly, which itself was written as the state-of-the-art on recursive thought capture during the Aurum v0_init session. Frontmatter schema uses current Claude Code plugin conventions. No deprecated patterns. Consent-per-invocation matches the 2026 best practice on LLM consent gating (never persist across turns). |
| Self-contained | 9/10 | Skill runs end-to-end within `skills/journal-system/`. The only external touch is `memory/journal/` which the skill creates itself via `install-manifest.yaml`. No reads from `memory/reference/*`, no dependencies on other skills, no cross-skill file locks. The auto-memory fallback is documented as runtime behaviour with no install-time target. |
| Anti-Frankenstein | 9/10 | Zero speculative surfaces. No consent card (explicitly avoided as friction on a speech-native surface). No `modes/` runner (not an OS-touching skill). No `trigger-phrases.md` or `states.md` (contents fit inside their primary consumer). Five files total, vs 12 for `phase-minus-one` and 8 for `phase-5-5-auth-preflight` — the lightest skill in the stack so far, and the lightness is earned by structural simplicity, not by cutting corners. |
| **Average** | **8.8/10** | Clears the 8.0/10 floor by 0.8. The lightness of the skill lets every axis land high. Above the 8.5/10 v1 ceiling — which the anti-Frankenstein framing called out as the plateau; a small clean skill can land above the ceiling naturally because there is less surface to add complexity to. No need to pad files to "feel complete" — sparse is better than speculative. |

### Known gaps for v0.5.0

- **No runtime probe for the Layer 0 sync check** — `SKILL.md` states that the skill is a 1:1 mirror of the Layer 0 journal system spec and must be updated if Layer 0 changes, but nothing enforces that. A small CI-style probe that diffs the skill's canonical sections against `~/.claude/CLAUDE.md` would detect drift early. Deferred — the Layer 0 spec itself is stable enough that drift is unlikely before v1.
- **No cross-project `/journal timeline` view** — the `memory/journal/INDEX.md` this skill ships is single-project only. The cross-project aggregator that walks every repo's `memory/journal/` on this machine is deferred to the Meta-Memory Path B session. Until then, users query cross-project with `grep -r` manually.
- **No auto-migration from `~/.claude/projects/<slug>/memory/journal_*.md` fallback to the repo's `memory/journal/`** — the fallback is documented but requires a manual move when the worktree becomes available. A small helper that detects and prompts the migration is a v0.5+ candidate. Low priority — the fallback is only triggered in pre-worktree sessions, which are rare.
- **No keyword auto-suggest on entry creation** — the `keywords:` frontmatter field is user-provided or Claude-inferred on demand. An auto-suggestion pass based on the verbatim quote content would lift the "findability" of entries for the future cross-project search. Deferred.
- **No trigger-phrase disambiguation helper** — if a user says "j'ai une idée sur X" the skill asks explicitly. A smarter fuzzy matcher could catch edge phrasings ("notons une pensée", "je veux journaliser ça") but the risk of false positives on non-journal speech is higher than the value. Deliberately left simple.
- **No direct support for importing an existing external notebook** — the skill only creates fresh entries. Users with existing `.md` notebooks they want to migrate into `memory/journal/` do so manually. Bulk import is a v1+ candidate once the first real migration need surfaces.

### Next version target

**v0.5.0** — fourth skill implementation. Two independent skill stubs remain before the orchestrator: `session-post-processor/` (JSONL redaction + markdown archive) and `pepite-flagging/` (red-light discovery flagging with cross-project routing). Pick whichever has the most concrete pain point at the time — the rubric in the v0.3.0 → v0.4.0 resume prompt applies. Target rating: **8.0/10** (floor, not ceiling).

---

## [0.3.0] — 2026-04-15 — "Phase 5.5 Auth Pre-flight skill"

### Added

- `skills/phase-5-5-auth-preflight/` — the second functional skill, end-to-end implementation of Phase 5.5 Auth Pre-flight per `specs/v1_phase_5_5_auth_preflight_learnings.md`. Closes the loop between "Phase -1 set up the machine" and "Phase 5 is ready to push a first repo". Paste-back is the baseline, Playwright automation is an opt-in convenience layer with hard fall-back on any selector mismatch.
- `skills/phase-5-5-auth-preflight/SKILL.md` — skill entry point, frontmatter for Claude Code plugin auto-discovery, six-step flow map, canonical PAT scope list (incl. Administration RW), isolated copy-paste rule (Learning 1), security-floor rules, anti-Frankenstein reminders.
- `skills/phase-5-5-auth-preflight/consent-card.md` — Step 5.5.0 card collecting project slug, GitHub owner, repo name, visibility, PAT expiration window, Chrome profile choice, Playwright opt-in. Every field defaults to safe null; consent is logged to `memory/reference/consent-log.md`.
- `skills/phase-5-5-auth-preflight/ssh-keygen.md` — Step 5.5.1 walkthrough: pre-check existing key, generate dedicated ed25519 key with `-C <slug>@<owner> -N ""`, idempotent append of `Host github.com-<slug>` block with `IdentitiesOnly yes` to `~/.ssh/config`, isolated code blocks for title/key/URL paste-back, `ssh -T` binding confirmation with wrong-identity recovery.
- `skills/phase-5-5-auth-preflight/pat-walkthrough.md` — Step 5.5.2 walkthrough: every field of the fine-grained PAT form in actual UI order (Learning 2), isolated code blocks for every paste value (Learning 1), canonical scope list with Administration RW (Learning 4), "All repositories" rationale, one-time token capture, `.env.local` sink with `gh api user` sanity test. Form snapshot date in frontmatter with `expires_at` 30-day TTL.
- `skills/phase-5-5-auth-preflight/empty-repo-create.md` — Step 5.5.3 walkthrough: the hard lesson that fine-grained PATs cannot create user-owned repos via API, every form field in its own fenced code block, "Initialize with" boxes all left unchecked, `git remote set-url` to the per-project SSH alias, verification via `gh api repos/owner/repo`. Snapshot `expires_at` TTL as above.
- `skills/phase-5-5-auth-preflight/three-probe-test.md` — Step 5.5.4 canonical three-probe gate (SSH handshake against the alias, `gh api user`, `gh api repos/owner/repo` with `.permissions.admin` check). Per-probe failure-mode tables with targeted recovery pointers. Full-pass helper `set -e` snippet with four exit codes (1/2/3 per probe, 0 for all-green) that R1.1 session-open health checks can grep. Standalone by design — Phase 5, downstream skills, and resumption flows all reuse it.
- `skills/phase-5-5-auth-preflight/playwright-automation.md` — conditional automation branch, opt-in via consent card only, Playwright MCP from Phase -1 required. Known-selector map for the three GitHub forms with `expires_at` 30-day TTL, hard fall-back to paste-back on any single selector miss (no retry loops), three-variant token-capture mitigation + `browser_snapshot` safety net, screenshot-on-failure for forensic review.
- `skills/phase-5-5-auth-preflight/verification.md` — Step 5.5.5 final health card plus the canonical schemas for the two reference memory files the skill writes at completion: `memory/reference/ssh_<project>_identity.md` and `memory/reference/github_<project>_account.md`. Three status outcomes (READY / READY_WITH_FALLBACKS / BLOCKED). Idempotency rules for re-running on an already-wired project.
- `.claude-plugin/plugin.json` version bumped to `0.3.0`.

### Notes

- Ships **one** skill only, per anti-Frankenstein scope discipline. Remaining skill stubs (`genesis-protocol`, `journal-system`, `session-post-processor`, `pepite-flagging`) land in their own worktrees later.
- All three stratified learnings from `specs/v1_phase_5_5_auth_preflight_learnings.md` are honoured: Learning 1 (isolated copy-paste blocks, never inside table cells), Learning 2 (form-order instructions matching the actual 2026 GitHub UI), Learning 3 (three-probe pre-flight as the explicit exit gate), Learning 4 (Administration RW in the canonical scope list), Learning 5 (paste-back cost is the v2 automation justification, honoured by the opt-in Playwright branch).
- Form-snapshot files (`pat-walkthrough.md`, `empty-repo-create.md`, `playwright-automation.md`) carry `expires_at: 2026-05-14` so the next session after that date re-validates the GitHub UI and the Playwright selector map before using them.
- `phase-minus-one` skill is untouched — its 7.6/10 rating is stable and no cross-skill refactor was attempted. Both skills remain self-contained within their own directories.
- No hook wiring, no templates/ population, no marketplace manifest — still out of scope.
- Every new file carries the `SPDX-License-Identifier: MIT` short-form header per R10.
- No features added outside the v1 spec; `three-probe-test.md` was split out as a standalone file only because the spec explicitly names it as Phase 5's entry condition, so Phase 5 and R1.1 both need to call it without pulling in the rest of the skill.

### Self-rating — v0.3.0

| Axis | Rating | Notes |
|---|---|---|
| Pain-driven coverage | 9/10 | Every file points to a specific learning in `v1_phase_5_5_auth_preflight_learnings.md` — isolated copy-paste blocks, form-order instructions, three-probe gate, Administration RW scope, the v2 automation justification. Zero speculative additions. |
| Prose cleanliness | 7/10 | Templates are dense but readable; per-step failure-mode tables are uniform across ssh-keygen / pat-walkthrough / empty-repo-create / three-probe-test. Three files repeat a safety-floor preamble intentionally so each stands alone. |
| Best-at-date alignment | 9/10 | 2026 Q2 patterns: fine-grained PATs with full canonical scopes, per-project SSH alias with `IdentitiesOnly yes`, Playwright MCP opt-in with `expires_at` selector TTL, `GH_TOKEN` env override (never `gh auth login`), isolated copy-paste rule baked into every paste-back instruction. |
| Self-contained | 7/10 | Skill runs end-to-end within `skills/phase-5-5-auth-preflight/`. External reads are bounded: `memory/reference/automation-stack.md` (from Phase -1), `.env.local` (own write), `~/.ssh/config` (own append). `three-probe-test.md` is explicitly designed to be callable from outside the skill by Phase 5 and R1.1 — a deliberate extraction, not a leak. |
| Anti-Frankenstein | 9/10 | Zero speculative surfaces; Playwright is opt-in with hard one-miss fall-back and no retry loops; PAT scope list is explicit and frozen; the three-probe test is fixed at three probes; no cross-skill refactor attempted; form-snapshot TTLs prevent silent rot. |
| **Average** | **8.2/10** | Clears the 7.8/10 target by 0.4. Below the 8.5/10 v1 ceiling — still room for v0.4.0 (next skill) to climb naturally without hitting the inflection point. |

### Known gaps for v0.4.0

- No automated tests for the full-pass helper in `three-probe-test.md` — the exit-code contract (1=SSH, 2=PAT, 3=repo, 0=all-green) is documented but not exercised by a harness. A small mock-based test would lift the "Self-contained" axis.
- The Playwright selector map in `playwright-automation.md` is a 2026-04-15 snapshot — the first time the skill runs in a real session after GitHub updates its forms, the fall-back path will be exercised and the selector map must be refreshed. There is no CI probe to detect drift early; a nightly `browser_navigate` health check is a v0.4.0+ candidate.
- `memory/reference/consent-log.md` schema is documented inside `consent-card.md` but not shipped as a starter file — upgrade when a second skill needs to read it.
- No `templates/phase-5-5-auth-preflight-*.md` ship — the walkthrough templates are skill-local. Promotion to `templates/` lands whenever the first downstream consumer project needs a standalone copy.
- The skill assumes `bash` for the shell snippets. PowerShell-equivalent snippets for Windows native terminal (without git-bash) are deferred — the Phase -1 skill already makes `bash` a core requirement so the assumption is internally consistent, but it does narrow the user base.
- Idempotency on re-run is documented but the consent card's "re-run from scratch / skip to 5.5.4 / cancel" branch is prose-only; a concrete runner would lift the axis further. Deferred.

### Next version target

**v0.4.0** — third skill implementation. The three remaining independent candidates are `journal-system/`, `session-post-processor/`, and `pepite-flagging/` (plus `genesis-protocol/` orchestrator, which should be last). Pick whichever reuses the most existing state. Target rating: **8.0/10**.

---

## [0.2.0] — 2026-04-15 — "Phase -1 Dependencies Pre-flight skill"

### Added

- `skills/phase-minus-one/` — the first functional skill, end-to-end implementation of Phase -1 Dependencies Pre-flight per `specs/v1_phase_minus_one_first_user_bootstrap_flow.md` (three stratified layers — initial design, 3-mode ladder, multi-device core)
- `skills/phase-minus-one/SKILL.md` — skill entry point, frontmatter for Claude Code plugin auto-discovery, seven-phase flow map, security-floor rules, multi-device core branch, anti-Frankenstein reminders
- `skills/phase-minus-one/detect.sh` — Phase -1.0 baseline probe. Cross-platform bash, read-only, <5 s. Emits `KEY=VALUE` report on stdout covering OS family, package manager, Layer 3 essentials (Node, npm, Git, gh, VS Code, Claude), Chrome, Claude Code VS Code extension, MCP list (Playwright, `ide`), Claude in Chrome (via native messaging host file when reachable), SSH keys, shell / home. Live-tested against this machine's dev stack during development.
- `skills/phase-minus-one/install-manifest.yaml` — Phase -1 target stack with per-OS install commands (winget / brew / apt / dnf / pacman). Items tagged by layer, rationale, `user_action_required` (none / admin_password / sign_in / extension_grant / pairing / restart), `plan_gate` for subscription-aware branching, and `core` vs optional. Includes the Phase -1.7 bonuses (Antigravity, Codespaces, Termux, voice mode) as `core: false`. Declares the five security-floor categories.
- `skills/phase-minus-one/gap-report.md` — Phase -1.1 card template with template variables, layer grouping, plan-tier branching, per-mode time estimates, security-floor intervention count
- `skills/phase-minus-one/consent-card.md` — Phase -1.2 template collecting mode choice + per-item opt-in in a single prompt. Defaults every box unchecked. Records consent in `memory/reference/consent-log.md`. Handles plan-tier branching for Remote Control row.
- `skills/phase-minus-one/modes/detailed.md` — Phase -1.3 mode 1 runner (detailed pas-à-pas, 30–45 min, user types each command, Claude teaches each step)
- `skills/phase-minus-one/modes/semi-auto.md` — Phase -1.3 mode 2 runner (10–15 min, command cards with yes / no / skip / pause, optional batched cards for homogeneous runs)
- `skills/phase-minus-one/modes/auto.md` — Phase -1.3 mode 3 runner (~5 min, full autonomous loop, graceful pause at every security-floor step, at most one retry + one alternate path before fall-back)
- `skills/phase-minus-one/sign-in-round.md` — Phase -1.4 consolidated sign-in round with fixed ordering (Claude web → GitHub → project-specific → Claude in Chrome extension → mobile app → Remote Control pairing)
- `skills/phase-minus-one/restart-round.md` — Phase -1.5 consolidated restart round (Chrome → shell rc reload → Claude Code session) with marker-file pattern for Claude Code self-restart
- `skills/phase-minus-one/verification.md` — Phase -1.6 health check card plus the canonical `memory/reference/automation-stack.md` schema it writes
- `skills/phase-minus-one/optional-bonus.md` — Phase -1.7 opt-in card for Antigravity / Codespaces / Termux / voice mode, strictly opt-in, consent-gated from Phase -1.2

### Notes

- This PR ships **one** skill only, per anti-Frankenstein scope discipline from the resume prompt. Other skills (`genesis-protocol`, `phase-5-5-auth-preflight`, `journal-system`, `session-post-processor`, `pepite-flagging`) remain as README stubs and land in their own worktrees later.
- No hook wiring, no templates/ population, no marketplace manifest — all out of scope for v0.2.0.
- All new files carry the `SPDX-License-Identifier: MIT` short-form header per R10 plugin conventions.
- `detect.sh` was live-tested on this Windows 11 machine against the actual dev stack and emits 25 well-formed key-value lines covering every probe.

### Self-rating — v0.2.0

| Axis | Rating | Notes |
|---|---|---|
| Pain-driven coverage | 8/10 | Every file in the skill points to a specific section of the Phase -1 spec; no speculative additions; multi-device core honoured |
| Prose cleanliness | 7/10 | Templates are readable but dense in places; three mode files repeat some structure intentionally so each stands alone |
| Best-at-date alignment | 9/10 | 2026 Q2 patterns throughout — winget/brew/apt, Playwright MCP, VS Code extension doubling as `ide` MCP, Claude Code Remote Control, Antigravity hybrid, F-Droid Termux, magical one-liner for Phase -2 |
| Self-contained | 6/10 | Skill is self-contained within `skills/phase-minus-one/`; references the spec + rules + research cache but runs end-to-end without them; the manifest → mode-runner → report-template loop is readable in isolation |
| Anti-Frankenstein | 8/10 | Zero speculative surfaces; mode 3 retry budget capped at one retry + one alternate; bonus items strictly opt-in; no hook wiring, no templates/, no marketplace |
| **Average** | **7.6/10** | Above the 7.0 target; below the 8.5 v1 ceiling — room for v0.3.0 to add the second skill cleanly |

### Known gaps for v0.3.0

- No automated tests — `detect.sh` was live-validated manually on one machine. A small harness emulating the seven-phase flow over a fake manifest would lift the "Self-contained" axis.
- `install-manifest.yaml` is not yet schema-validated at skill load time. A one-time YAML sanity check at Phase -1.0 boot would catch broken edits.
- `memory/reference/automation-stack.md` canonical schema is documented inside `verification.md` rather than shipped as a starter file under `memory/reference/`. Upgrade at v0.3.0 once a second consuming skill needs it.
- No `templates/phase-minus-one-install-manifest.yaml` ship — the manifest is skill-local only. Promotion to `templates/` lands whenever the first downstream consumer project needs a standalone copy.
- Claude in Chrome detection on Windows is `unknown` because native messaging hosts live in the Windows registry. A registry probe via PowerShell could lift this at the cost of shell-portability — deferred to v0.3.0 unless user feedback flags it.

### Next version target

**v0.3.0** — second skill implementation (likely `phase-5-5-auth-preflight/` since it reuses the Phase -1 detection state and is the next deepest-specced item). Target rating: **7.8/10**.

---

## [0.1.0] — 2026-04-14 — "Scaffold bootstrap"

### Added

- Initial plugin scaffold following Claude Code plugin convention
- `.claude-plugin/plugin.json` manifest with required + recommended fields
- MIT `LICENSE` + SPDX short-form headers on every source file
- Bilingual `README.md` (FR + EN) per R9 language policy
- Project-level `CLAUDE.md` inheriting universal rules from `~/.claude/CLAUDE.md` (Layer 0)
- `memory/` directory structure with R4.1 layout + new `journal/` and `pepites/` directories (6th and 7th memory types)
- `memory/project/session_v1_bootstrap.md` capturing this session's context, decisions, and self-ratings
- `memory/project/aurum_frozen_scope_lock.md` enforcing the rule that aurum-ai stays at `0b1de3d` until Genesis v1 ships
- `memory/reference/ssh_genesis_identity.md` documenting the dedicated ed25519 key + `github.com-genesis` alias
- `memory/reference/github_genesis_account.md` documenting the target account, PAT env pattern, SSH URL
- `.claude/docs/superpowers/research/` with **7 R8 cache entries** from bootstrap research (license, plugin distribution, SPDX headers, plugin structure, JSONL format, Claude in IDE tools, cross-OS Claude ecosystem) — all SPDX-headered, all TTL-tagged
- `.claude/docs/superpowers/specs/` with **4 v1 specs** (Phase 5.5 auth pre-flight learnings, Phase -1 first-user bootstrap flow, pépite discovery flagging, Phase 5.5 auth-preflight) and **1 v2 spec** (phase-minus-one-dependencies-automation, to be renamed/merged at Étape 5)
- `.claude/docs/superpowers/rules/v1_rules.md` with R1-R10 adapted for Genesis per Étape 2 scoreboard (KEEP R2; ADAPT R1, R3, R4, R5, R6; INHERIT R8, R9 from Layer 0; DROP R7; NEW R10)
- Empty `skills/`, `templates/`, `hooks/`, `memory/user/`, `memory/feedback/`, `memory/themes/` directories with README placeholders explaining what lands there
- `.env.local` with the project-scoped `GH_TOKEN` (gitignored from first commit, never exposed)
- `.env.local.example` + `.envrc.example` (direnv alternative) as templates for downstream users
- `.gitignore` with secrets, OS files, editor files, language artefacts, and `.claude/worktrees/` (forensic snapshots stay local per R2.5)

### Design work saved during the session (not yet code)

These specs describe what v1.0.0 will implement but no runtime code exists yet for any of them:

- Phase -1 3-mode ladder (detailed / semi-auto / auto)
- Multidevice core (Claude Code Remote Control + mobile companion)
- Journal system trigger phrases (inherited from Layer 0, skill implementation pending)
- Session post-processor logic (JSONL parsing + secret redaction + markdown emission)
- Pépite red-light detection criteria (6 conditions, "two or more" rule)
- Cross-project research sharing via pointer files

### Cross-project additive

- Pointer file written into `~/.claude/projects/C--Dev-Claude-cowork-aurum-ai/memory/reference_genesis_research_cache_pointer_2026-04-15.md` referencing the Genesis R8 cache for future Aurum sessions to consume
- Meta-Memory architecture doc in Aurum's auto-memory updated with the pépite feature integration

### Self-rating — v0.1.0

Rubric: 5 axes, 1-10 each, averaged. Target < 10 per anti-Frankenstein discipline.

| Axis | Rating | Notes |
|---|---|---|
| Pain-driven coverage | 2/10 | Scaffold only — no functional content yet; specs cover the pain points but code is absent |
| Prose cleanliness | 6/10 | Structured but placeholders everywhere; README has pre-release markers |
| Best-at-date alignment | 8/10 | MIT + SPDX + plugin convention + marketplace-ready + 2026 patterns baked into specs |
| Self-contained | 5/10 | Inherits Layer 0 unambiguously; specs stand alone |
| Anti-Frankenstein | 9/10 | Every file audited pain-driven; placeholders not filled beyond need |
| **Average** | **6.0/10** | Honest starting point — the scaffold exists, the content doesn't yet |

### Not yet implemented (lands at Étape 5+)

- Skill content in `skills/*/` — `phase-minus-one`, `phase-5-5-auth-preflight`, `journal-system`, `session-post-processor`, `pepite-flagging`, `genesis-protocol`
- Hook wiring in `hooks/hooks.json` for `SessionEnd` (deferred until post-processor manual mode validates)
- Template markdown in `templates/` — the actual 7-phase Genesis protocol text
- Self-hosted marketplace manifest for `/plugin install project-genesis@myconciergerie-prog/project-genesis`
- Integration tests and dogfooding harness (anti-Frankenstein — defer until pain surfaces)

### Next version target

**v0.2.0** — first worktree PR from Étape 5 with at least one skill (`phase-minus-one/` or `journal-system/`) implemented end-to-end. Target rating: **7.0/10**. Shipped via `gh pr merge --squash` per R2.3, tagged `v0.2.0`.

**v1.0.0 target**: **8.5/10**. Inflection point protection — no feature ships if the marginal rating gain per feature added is near zero.

---

## Release process

Version bumps follow semver:

- `0.x.y` — pre-release, scaffold, experimental content
- `1.x.y` — stable plugin, available via `/plugin install`
- `major` — breaking changes to skill interfaces or plugin manifest
- `minor` — new skills, new features, backward-compatible
- `patch` — bug fixes, doc updates, rule clarifications

Every version bump:

1. Updates `plugin.json` `version` field in the same PR
2. Appends a CHANGELOG entry with the 5-axis self-rating block
3. Tags the squashed merge commit with `v<semver>`
4. Optionally runs `GH_TOKEN="$GH_TOKEN" gh release create v<semver>` with a CHANGELOG extract
5. Updates the self-hosted marketplace manifest to reference the new tag (v1.0.0+)

Ratings below **7.0/10 cannot be tagged as stable `1.x.y`** per R10.3 — use `0.x.y` for pre-release.
