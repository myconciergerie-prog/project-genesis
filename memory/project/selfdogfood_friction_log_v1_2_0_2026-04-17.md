<!-- SPDX-License-Identifier: MIT -->
---
name: Genesis v1.2.0 self-dogfood — live friction log
description: Conscious strange-loop run on 2026-04-17. Genesis bootstraps Genesis-describing-Genesis from a worktree target folder. Each friction captured as it surfaces, no live fixes.
type: project
date: 2026-04-17
session: v1.2.0 self-dogfood
target: .claude/worktrees/feat_2026-04-17_v1.2.0-selfdogfood/selfdogfood-target/
mode: auto
seed: config.txt describing Genesis itself
---

# Genesis v1.2.0 self-dogfood — live friction log

**Strange loop declared**: project-genesis (orchestrator) targeting `selfdogfood-target/` (the loop's fixpoint) with a config.txt whose content IS Genesis.

**v1.1 lesson absorbed**: the target folder is a *subfolder* of the worktree, not the parent repo itself. The paradox is contained, not resolved.

**Method**: invoke `genesis-protocol` skill in mode=auto. Capture friction as it surfaces. Do NOT fix live. Continue as far as the protocol will go.

**Friction numbering**: F20+ (continuing from F19 in the 2026-04-16 log).

---

## Severity scale

- **STRUCTURAL** — protocol design flaw, blocks the Victor test
- **DESIGN** — protocol describes something that doesn't work as written
- **COSMETIC** — awkward but not blocking

---

## Frictions captured live

### F20 — `mode=auto` contradicts skill's "Do not auto-run" primary rule [STRUCTURAL]

**Phase**: 0 (skill entry)
**What**: The user invoked `/genesis-protocol mode=auto`. The SKILL.md's first "When to invoke" block states: *"Do not auto-run. The orchestrator touches git, creates SSH keys, creates PATs, creates a GitHub repo, and writes files into a new project directory. Every single one of those is a concentrated privilege. The first action is always a top-level consent card showing the full plan before any phase starts."*
**Root cause**: Mode=auto is a Phase -1 concept (3-mode ladder: detailed / semi-auto / auto) that was never extended to the orchestrator level. Original F2 from v1.1 log flagged this for Phases 0-7; F20 is F2 confirmed at the orchestrator entry itself — the consent card is hard-wired, not mode-aware.
**Impact**: mode=auto degrades to "render the consent card and assume yes" which is NOT what the user intended. They expect chained phases without checkpoints.
**Fix v1.2**: Add a `mode` argument to the orchestrator. In auto mode, consent cards become *informational summaries* printed to the session (not blocking), except for true security floor (OAuth click, PAT creation).
**Fix v2**: Absorbed into the Promptor fusion — consent happens via the conversational mirror (Étape 2), not hard-wired cards.

### F21 — Argument schema for `/genesis-protocol` is undocumented [DESIGN]

**Phase**: 0 (skill entry)
**What**: The skill's footer prints `ARGUMENTS: mode=auto target=... seed=... context=... strange-loop=... friction-log=...` verbatim, but the SKILL.md does not document what arguments the skill accepts. There is no `## Arguments` or `## Parameters` section. The orchestrator is expected to parse these kvp args from free text.
**Root cause**: Skills in Claude Code have no formal argument schema. The `args` string is passed as raw text. The orchestrator has no declared way to bind `mode=auto` to a runtime behaviour.
**Impact**: Any caller (human or v2 Promptor) guessing at argument names will miss. Consistency between invocations is impossible.
**Fix v1.2**: Add an `## Arguments` section to SKILL.md listing: `mode` (detailed | semi-auto | auto, default detailed), `target` (absolute path, required), `seed` (filename inside target, default config.txt), `consent` (ask | assume | skip, default ask).

### F22 — Consent card mandatory even when mode=auto (F2 re-confirmed at orchestrator) [DESIGN]

**Phase**: 0 (step 0 top-level consent)
**What**: Step 0 says: *"The user must confirm the full card before Phase 0 starts. No silent bootstraps."* No mode-aware override exists. v1.1's F2 flagged this at the protocol level; F22 confirms it at the orchestrator level.
**Root cause**: Same as F2 — the 3-mode ladder was designed for Phase -1 only. The orchestrator inherited consent-gate wording but not mode-awareness.
**Fix**: Rephrase Step 0 as "Consent card rendered; in detailed/semi-auto modes, wait for explicit yes; in auto mode, treat the card as an informational summary and proceed unless the user interjects."

### F23 — Worktree-as-subdir-of-repo defeats the paradox safety net [STRUCTURAL]

**Phase**: 0 (skill entry)
**What**: SKILL.md says: *"Do not let any phase write to the Genesis repo itself. [...] The worktree pattern from R2.1 is the safety net: the orchestrator runs on a folder that is NOT the Genesis repo."* But R2.1 worktrees are physically under `project-genesis/.claude/worktrees/<name>/` — still inside the Genesis repo's tree from a filesystem perspective, even if git treats them as a separate branch.
**In this run**: target = `.claude/worktrees/feat_2026-04-17_v1.2.0-selfdogfood/selfdogfood-target/`. The orchestrator will write to this folder, which is physically under project-genesis, even though git sees the worktree as a different branch. The recursive paradox v1.1 tried to avoid with the "separate repo" rule is NOT avoided by worktrees alone.
**Root cause**: The safety net conflates "separate branch" with "separate filesystem location". A real downstream project is at `C:/Dev/Claude_cowork/<other-project>/`, not at a worktree path.
**Impact**: Phase 3 (`git init` in the target folder) will conflict with the worktree's existing `.git` → the target is already a git repo, inherited from the worktree. Phase 5.5 will try to create a repo named `project-genesis` which already exists. The strange loop is real and blocking.
**Fix v1.2**: Pre-flight check at Step 0: if target path is inside the Genesis repo's worktree tree, surface a blocking warning and propose a sibling folder (e.g. `C:/Dev/Claude_cowork/project-genesis-v1.2-test/`). Or: expand the safety net to "target must not be inside any git repo" (`git rev-parse --show-toplevel` returns a parent not equal to the target).
**This friction is the user's intended strange loop**: the user deliberately chose this target path to stress-test the paradox. The test succeeds — paradox confirmed structural.

### F24 — Phase 0.1 inside-git-repo detection is weak [DESIGN]

**Phase**: 0 (Step 0.1 inspect input folder)
**What**: `phase-0-seed-loading.md` lists "Folder with existing code (`package.json`, `pyproject.toml`, `Cargo.toml`, `.git/`) → Stop" as a trigger. The literal check is "is there a `.git/` in THIS folder?". It does NOT detect "is this folder INSIDE an existing git repo?". In this run, `git rev-parse --show-toplevel` from `selfdogfood-target/` returns the worktree parent — but no `.git/` exists at `selfdogfood-target/` itself, so the literal check would miss.
**Root cause**: The check is a static filename lookup, not a git-aware probe.
**Fix v1.2**: Replace the literal lookup with `git rev-parse --show-toplevel` (success = inside a repo → STOP and warn; failure = outside any repo → proceed).
**Verified live**: ran `git rev-parse --show-toplevel` from target folder at 2026-04-17; returned `.../feat_2026-04-17_v1.2.0-selfdogfood`. F24 reproduced.

### F25 — config.txt format undocumented at USER level (F19 re-confirmed) [DESIGN]

**Phase**: 0 (Step 0.2 parse)
**What**: I wrote the config.txt using a YAML-style `key: value` + `|` block syntax. The phase-0 runbook says "config.txt is free-form but expected to cover" a list of topics. There's no example, no schema, no anchor pointing to one. I had to guess the format. F19 logged this as a downstream friction at the atelier-playmobil bootstrap; F25 confirms it surfaces again even when the same human writes both the seed AND the protocol.
**Impact**: Every user will invent a different format. The orchestrator's "light field-extraction pass" (per anti-Frankenstein reminders) has no canonical reference to compare against. Downstream Phase 0.5 `bootstrap_intent.md` fills fields inconsistently.
**Fix v1.2**: Ship `templates/config.txt.example` with the 7 canonical fields and a one-paragraph docstring explaining each. Reference it in README's Quick Start.

### F26 — Extra config.txt fields silently dropped, no error + no audit [DESIGN]

**Phase**: 0 (Step 0.2 parse)
**What**: My config.txt includes `audience:`, `constraints:`, `known_rough_edges:`, `expected_frictions_to_validate:`, `next_target_after_v1_2:` — none are in the Phase 0 canonical field list (name / slug / vision / stack / license / is-a-plugin / plan-tier / scope-locks). The runbook doesn't say what happens to extras: pass-through to bootstrap_intent.md? dropped silently? surfaced on the card? Unclear.
**Root cause**: Anti-Frankenstein reminder "Do not parse config.txt into a DSL" is correct in spirit but creates ambiguity — freeform means "no schema", but no schema means "no contract on non-canonical fields".
**Fix v1.2**: Phase 0 should record extras verbatim in `bootstrap_intent.md` under a `## Non-canonical fields (passed through)` section and surface them on the parsed-intent card as `Extras: [field names]`. User can opt to promote any of them to a canonical field.

### F27 — Slug collision warning non-blocking even for catastrophic self-collision [DESIGN]

**Phase**: 0 (Step 0.4 / Common Failures)
**What**: Common Failures lists "Slug conflicts with an existing sibling project on this machine — warn, suggest appending `-2` or editing config.txt. Do not auto-rename." In this self-dogfood, the slug is `project-genesis` — the EXACT same slug as the Genesis repo hosting the orchestrator. The orchestrator will warn and continue, which is wrong for a conscious strange-loop that WILL collide at Phase 5.5 GitHub repo creation.
**Root cause**: The collision detector treats all collisions as minor warnings. Self-collision (slug == orchestrator's own slug) is a structural blocker, not a cosmetic warning.
**Fix v1.2**: Add a STRUCTURAL stop for self-collision: if the target slug equals the Genesis repo's own slug, stop with "you are bootstrapping Genesis on Genesis — aborting to prevent recursive collision. Use a differentiated slug (e.g. `project-genesis-selfdogfood`) or target a folder outside the Genesis repo tree."

### F28 — Stale SSH key artefacts from prior dogfood never cleaned [COSMETIC]

**Phase**: 3 (Step 3.2 SSH keygen prerequisite)
**What**: `$HOME/.ssh/` on this machine carries `id_ed25519_genesis-selfdogfood` + `.pub` from the v1.1 dogfood on 2026-04-16 — a session that aborted at the auth wall. Those key pair files are dead weight, still tracked by ssh-agent potentially.
**Root cause**: Genesis has no "abort / rollback / cleanup" pathway. A failed Phase 3.2 leaves keys behind.
**Fix v1.2**: Add a `genesis-cleanup` sibling skill that takes a slug and deletes the SSH key pair + removes the host-alias block from `~/.ssh/config` + offers to delete the local target folder. Alternative: a `--cleanup` flag on the orchestrator invocation.

### F29 — Phase 1 Step 1.3 "three levels up" path resolution breaks in personal-scope install [STRUCTURAL]

**Phase**: 1 (Step 1.3 copy rules)
**What**: SKILL.md and phase-1-rules-memory.md state: *"The plugin root is always three levels above this skill's SKILL.md file (walking up from `skills/genesis-protocol/SKILL.md` gives `skills/genesis-protocol/` → `skills/` → `<plugin-root>/`)."* But skills installed via F18's workaround live at `~/.claude/skills/genesis-protocol/SKILL.md`. Three levels up resolves to `~/.claude/` — which is NOT the plugin root and does NOT contain `.claude/docs/superpowers/rules/v1_rules.md`. The orchestrator would halt with "rules file not found at `C:/Users/conta/.claude/.claude/docs/superpowers/rules/v1_rules.md`" when installed to personal scope.
**Impact**: **Genesis v1.1 plugin installation is currently broken.** Any user who followed F18's `cp -r skills/ ~/.claude/skills/` workaround cannot actually run the protocol end-to-end — it aborts at Phase 1 Step 1.3.
**Root cause**: The resolution heuristic assumes marketplace-installed or `--plugin-dir` layout, where both the skills and the rules live under the same plugin root. Personal-scope install separates them: skills at `~/.claude/skills/` but rules must live with the source repo checkout.
**Fix v1.2**: (a) Ship rules as part of the skill package (`skills/genesis-protocol/rules/v1_rules.md`) so the skill is self-contained. (b) Or resolve the plugin root from `$CLAUDE_PLUGIN_ROOT` env var (set by Claude Code when running a plugin) with a CLI-detectable fallback. (c) Or require the user to also `cp -r .claude/docs/superpowers/rules/ ~/.claude/docs/superpowers/rules/` at install time — and document it.
**Verified at the path-arithmetic level**: SKILL.md loaded from `C:\Users\conta\.claude\skills\genesis-protocol\SKILL.md` in this very session.

### F30 — Phase 3.1 nested-repo silent success [STRUCTURAL]

**Phase**: 3 (Step 3.1 git init)
**What**: `phase-3-git-init.md` says *"The target folder does not yet contain `.git/`. If it does, Phase 3 stops and asks whether the user meant to resume a partial bootstrap."* The check is the literal absence of `.git/` in the target. In this run, `selfdogfood-target/` has no `.git/` — but the parent directory hierarchy already has a `.git` as a worktree of `project-genesis`.
**Live test at 2026-04-17 00:56**: `cd selfdogfood-target && git init -b main` — returned `Initialized empty Git repository` with NO warning. `git rev-parse --show-toplevel` then returned the nested path. Git silently created a repo inside another repo — the infamous nested-repo trap.
**Impact**: Without intervention, the bootstrap produces a nested repository that breaks nearly every downstream assumption (push would push the nested repo, not the outer; PRs wouldn't align; the forensic worktree archive would include an orphan inside an orphan).
**Root cause**: The `.git/`-literal check is not git-aware. `git rev-parse --show-toplevel` is the correct probe.
**Fix v1.2**: Replace the literal check at Step 3.1 with `git rev-parse --show-toplevel 2>/dev/null` — if it returns a path and that path is not the target itself, STOP with: "Target folder is inside an existing git repository at `<outer-path>`. Nested repositories are not supported. Use a sibling directory outside the outer repo, or remove the outer `.git/` if this is the root."
**This confirms F23** — the worktree safety net is inadequate without a git-aware check at Step 3.1.

### F31 — Seed author had to guess where the YAML boundary ends [COSMETIC]

**Phase**: 0 (Step 0.2, authoring)
**What**: When I (Claude) wrote `config.txt`, I hesitated between three plausible formats: (a) frontmatter `---` + YAML, (b) pure YAML keys, (c) free-form paragraphs with Markdown headings. I picked (b) because of similarity to skill metadata elsewhere in the repo. But a human non-technical user (Victor) would pick (c) at best, which the orchestrator parses even less deterministically.
**Root cause**: No canonical example shipped with Genesis.
**Fix v1.2**: Ship two canonical examples: `templates/config-minimal.txt.example` (3-line free-form) and `templates/config-complete.txt.example` (all 8 canonical fields, YAML-ish). Pin in README Quick Start.

### F32 — Orchestrator cannot be invoked programmatically [DESIGN]

**Phase**: 0 (orchestration invocation)
**What**: When I invoked `/genesis-protocol mode=auto target=... seed=... ...`, the skill body was returned to me verbatim as text, and I had to interpret it as a runbook. There is no *executable* orchestrator — the Markdown runbook is a prompt for me. This is Option A pure-Markdown working exactly as designed, but it means:
  - The `mode=auto` argument is only honoured if I remember to honour it (I did; a different session might not).
  - Argument parsing is ad-hoc; there is no contract between `/genesis-protocol mode=auto` and the orchestrator's behaviour.
  - Re-entrancy is fragile: if the session is compacted or resumed, the orchestrator's progress state lives only in files on disk (`bootstrap_intent.md`, `automation-stack.md`), not in an executable resume token.
**Root cause**: Option A was the right v0.8 choice. But at v1.2, the orchestrator is at the limits of what Markdown-as-runbook can deliver.
**Fix v1.3 or v2**: Introduce a lightweight Python driver (`genesis_protocol/driver.py`) that: (a) parses args with `argparse`, (b) loads the Phase X runbooks as templates, (c) tracks progress state in `.genesis/state.json`, (d) re-entrancy from the last completed phase. The Markdown runbooks remain the source of truth for prose; the driver is a thin executor. This is exactly the F5 fix path already flagged in v1.1 log.

### F33 — Research cache entry written in wrong repo scope [DESIGN]

**Phase**: 2 (research cache init) — meta-observation, not a protocol defect
**What**: During this session I wrote `v2_promptor_fusion_landscape_2026-04-17.md` to the worktree's `.claude/docs/superpowers/research/sota/` — which will be committed on the `feat/v1.2.0-selfdogfood` branch. But the research content is about the v2 Promptor roadmap, which is a `project-genesis` concern, not a `selfdogfood-target` concern. It belongs in the Genesis repo's own R8 cache, not in the worktree (which is conceptually "a sibling project being bootstrapped").
**Root cause**: The orchestrator conflates "worktree location" with "project identity". Worktrees of the Genesis repo ARE the Genesis repo from a memory-scope perspective.
**Fix v1.2**: Clarify in R8 cache convention: research for the orchestrator itself lives in project-genesis/main's cache; research *about the target project* lives in target/.claude/.../research/. Add a Step 0.3b that asks the user to disambiguate scope when non-obvious.
**Action for this session**: merge the research entry to main as part of the PR, don't leave it only in the feat branch.

---

## Running notes

- Worktree created at: `.claude/worktrees/feat_2026-04-17_v1.2.0-selfdogfood/`
- Target folder: `selfdogfood-target/` (inside worktree, sibling to `skills/`)
- Branch: `feat/v1.2.0-selfdogfood`
- R8 research cache entry seeded: `v2_promptor_fusion_landscape_2026-04-17.md`

## Stop rationale

Live execution halted mid-Phase 3 after F30 was reproduced with `git init -b main` inside the target. The nested `.git/` was cleaned up immediately.

Further phases would have produced mostly predictable frictions (F27 blocks Phase 5.5 repo create; F29 blocks Phase 1.3 rules copy when Genesis is installed to personal scope; Phase 6 push would have no target repo). Nothing gained by attempting them live — the captured frictions are sufficient signal for v1.2.1.

## Meta-findings

### #1 — The paradox is an architectural issue, not a user error

v1.1 log said *"v1.1 ran Genesis on itself from inside project-genesis/. This caused deployment confusion."* The proposed fix was "use two separate sessions, two separate folders". v1.2 reveals this fix is insufficient. The protocol as written has no self-defence against:
  - Target path inside the orchestrator's own repo tree (F23)
  - Target slug equal to orchestrator's own slug (F27)
  - Nested `git init` inside an existing repo (F30)
  - Rules path resolution assuming plugin-dir layout (F29)

**A user following the README can still cause a nested-repo or collision today.** The v1.2 fix is a defensive layer at Step 0 of the orchestrator + Step 3.1 of the runbook that actively detects and refuses the paradox.

### #2 — The "Promptor 4-part structure" is a Genesis-native synthesis, not a published pattern

Research agent #3 verified: no public source documents the calibrage / prompt / auto-critique / questions structure attributed to "Promptor" in the v2 spec. There is an academic Promptor paper (Zhu et al. 2310.08101) but its abstract does not describe this structure. The closest public ancestor is the "Mr Promptor" / FlowGPT Promptor GPT Store prompt in the French community, which follows a similar calibrage flow without naming the 4-part structure.

**Action**: the v2 spec must be corrected to credit this pattern as Genesis-native, inspired by FR-community work, not cite it as "Promptor's published structure". Left uncorrected, the misattribution would embarrass Genesis at community review.

### #3 — The drag-and-drop box is the missing Étape 0 of v2

The user's next objective ("drag-and-drop box where users drop initial elements → Claude extracts structured data → Promptor formalizes") IS the natural front door of the v2 Promptor fusion. Research agents #1 and #2 together gave us:
  - 2026 drop-zone UX canon: intent-first unified box, token-streamed acknowledgement, accept-anything, relationship-language privacy
  - Claude API ingestion canon: Files API + Citations (Path A) OR Structured Outputs (Path B), 1h cache TTL mandatory
  - Multi-file synthesis: documents before prompt, cross-reference via XML wrappers, contradictions[] array

**Action**: amend `specs/v2_vision_promptor_fusion.md` to prepend a new Étape 0 — "Le Dépôt" — and merge in the architectural choices from research (Path A Citations-audited recommended for v2.0).

### #4 — Mode-auto needs orchestrator-level semantics, not just Phase -1

Every friction labelled "consent gate in mode=auto" (F2, F20, F22) points to the same root cause: the 3-mode ladder was designed for Phase -1 only. For v1.2.1 the mode concept must be a first-class argument of the orchestrator with clear semantics:
  - `detailed`: all consent cards block, all summaries shown, user explicitly confirms every phase
  - `semi-auto`: consent cards block only for concentrated-privilege steps (Phase 3.2 SSH keygen, Phase 5.5 repo create); other phases show a summary and proceed
  - `auto`: no blocking consent cards; only true security floor (OAuth click, PAT creation UI) interrupts; every summary goes to a log the user can review afterwards

### #5 — The orchestrator is at the limits of pure-Markdown design

F32 documents this explicitly. Argument parsing, re-entrancy, mode dispatch, and per-phase state tracking cannot be cleanly expressed in a Markdown runbook interpreted by an LLM session — they need an actual driver. The v1.3 target should be a thin Python driver that treats the Markdown runbooks as templates + state.

### #6 — Pépite-worthy findings

Two findings qualify as cross-project pépites per `specs/v1_pepite_discovery_flagging.md`:

- **F29 (Genesis plugin personal-scope install is broken today)**: a structural bug affecting every user who followed the F18 workaround. Red-light criterion: "a documented install path produces a runtime break." Route to `~/.claude/memory/project_claude_cowork_roadmap.md` as a cross-project alert. Also post-fix, a README warning.
- **"Promptor 4-part structure is Genesis-native"**: factual correction that propagates to v2 spec, any v2 blog post, any marketplace listing. Red-light criterion: "public attribution of a pattern we cannot back up." Route to `specs/v2_vision_promptor_fusion.md` + a CHANGELOG note at v1.2.0.

## Summary by severity

| Severity | Count | IDs |
|---|---|---|
| STRUCTURAL | 5 | F20, F23, F27, F29, F30 |
| DESIGN | 6 | F21, F22, F24, F25, F26, F32, F33 |
| COSMETIC | 2 | F28, F31 |
| **Total (v1.2.0)** | **13 new frictions (F20–F32 + F33)** | **cumulative F1–F33** |

## What v1.2.1 should fix (prioritized)

| Priority | Friction | Fix sketch |
|---|---|---|
| P0 | F29 | Ship rules inside the skill package or require a second `cp -r` step with loud README note |
| P0 | F30 | Replace literal `.git/` check with `git rev-parse --show-toplevel` git-aware probe |
| P0 | F23, F27 | Step 0 structural-stop: refuse target inside orchestrator repo; refuse slug == orchestrator slug |
| P1 | F20, F22 | `mode` argument with detailed/semi-auto/auto semantics + docs |
| P1 | F21, F32 | `## Arguments` section in SKILL.md + thin Python driver roadmap |
| P2 | F25, F31 | Ship `templates/config-*.txt.example` + README Quick Start |
| P2 | F26 | Non-canonical fields passed through to `bootstrap_intent.md` as audit trail |
| P3 | F28 | `genesis-cleanup` sibling skill |
| P3 | F33 | R8 scope disambiguation note
