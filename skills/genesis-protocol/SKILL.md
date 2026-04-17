<!-- SPDX-License-Identifier: MIT -->
---
name: genesis-protocol
description: Orchestrate the 7-phase Project Genesis protocol end-to-end on a fresh project folder — dependencies pre-flight, seed loading from config.txt + mixed media, rules and memory architecture setup, research cache initialization, git repo + SSH identity, project-specific seeds, auth pre-flight, first commit + PR + merge + tag, and resume prompt for the next session. Composes the five shipped Genesis skills (phase-minus-one, phase-5-5-auth-preflight, journal-system, session-post-processor, pepite-flagging) into a single conductor; never reimplements any of them.
---

# Genesis protocol — the orchestrator

This skill is the **conductor** of the Project Genesis 7-phase protocol. It takes a fresh project folder — typically containing a `config.txt` seed plus optional mixed media — and walks it through the full bootstrap sequence until the project has a real git repo on GitHub, a first commit merged, a resume prompt for the next session, and every memory subsystem wired.

The orchestrator does **not** reimplement any of the five shipped Genesis skills. It invokes them at the right phase, threads their outputs together, and emits a single "genesis report" at the end. One privileged operation is concentrated in the orchestrator: **writing into a new project directory outside the Genesis repo itself**. Every phase that writes outside the Genesis repo must have an explicit consent gate — same discipline as `session-post-processor`'s halt-on-leak gate and `pepite-flagging`'s cross-project pointer consent.

**Canonical spec**: `memory/master.md` → "What this project is" + the implicit 7-phase table whose formal version lives in this SKILL.md. The orchestrator is a 1:1 mirror of that description, same discipline as `journal-system` (mirror of Layer 0) and `pepite-flagging` (mirror of `v1_pepite_discovery_flagging.md`).

## When to invoke

- The user types `/genesis-protocol`.
- The user says any of:
  - "bootstrap this project"
  - "lance genesis"
  - "run the genesis protocol"
  - "apply genesis to this folder"
  - "start a new project with genesis"
  - "genesis bootstrap"
- The user is sitting inside an **empty or near-empty project folder** that contains a `config.txt` seed (or is about to create one).

**Do not auto-run without explicit consent.** The orchestrator touches git, creates SSH keys, creates PATs, creates a GitHub repo, and writes files into a new project directory. Every single one of those is a concentrated privilege. The first action is always a top-level consent card showing the full plan before any phase starts. **Two paradox guards run before the card** (target-inside-orchestrator-tree and self-collision-slug) — structural stops added in v1.2.1 after the v1.2.0 strange-loop self-dogfood proved a user could create a nested repo or a colliding GitHub name by accident.

The shape of the consent interaction is driven by the `mode` argument (see `## Arguments` below): in `detailed` mode the card blocks until the user confirms; in `semi-auto` the card blocks only for concentrated-privilege operations; in `auto` the card is informational and the orchestrator proceeds unless the user interjects. Paradox guards fire in every mode — they are structural stops, not consent gates.

## Arguments

The orchestrator accepts three semantic arguments as `key=value` pairs on the skill invocation (e.g. `/genesis-protocol mode=auto target=/abs/path seed=config.txt`). Any extra `key=value` pair is accepted as **passthrough** — recorded in `memory/project/bootstrap_intent.md` under `## Non-canonical fields (passed through)` but with no runtime effect. Added in v1.2.2 after friction F21 (argument schema was undocumented and invocations guessed at names).

| Argument | Values | Default | Purpose |
|---|---|---|---|
| `mode` | `detailed` \| `semi-auto` \| `auto` | `detailed` | Consent dispatch across Step 0, Phase 0.4, Phase 3 SSH paste-back, Phase 6 pre-commit review, Phase 7 halt-on-leak. Propagates into `phase-minus-one` as its own 3-mode ladder input. See `## Mode dispatch` below. |
| `target` | Absolute path to a folder | Current working directory of the session | Destination folder for the bootstrap. Paradox Guard A checks this path against the orchestrator plugin root. |
| `seed` | Filename inside the target folder | `config.txt` | File read at Phase 0.2 for the free-form project intent. If missing, Phase 0.1 offers the interactive seed card. |

Passthrough examples observed in real invocations: `context=...`, `strange-loop=...`, `friction-log=...`. They are accepted, captured in the Phase 0 parsed-intent card as `Extras: [field names]`, and written verbatim to `bootstrap_intent.md`. The orchestrator does not interpret them.

**Mode is sticky through the run.** If the user picks `semi-auto` at invocation, every phase receives `semi-auto` dispatch. Mode cannot be changed mid-run except by aborting and re-invoking — there is no mid-flight escalation path in v1.2.2 (a v2 candidate).

**Mode never overrides structural stops.** Paradox Guards A and B, nested-repo halts (Phase 3.1), halt-on-leak gates (Phase 7.2), any failed probe at Phase 5.5.4, and any `frankenstein` / `pause` / `abort` keyword from the user stop the orchestrator regardless of mode. The security floor defined in `## Mode dispatch` is also mode-invariant.

## Mode dispatch — which gates block under which mode

Every consent-adjacent interaction in the protocol falls into one of three categories. Mode only changes the behaviour of category C gates.

| Category | Behaviour | Examples |
|---|---|---|
| **A — Structural stops** | Always halt, never dispatch by mode | Paradox Guards A/B at Step 0; nested `git init` at Phase 3.1; halt-on-leak RED at Phase 7.2; any failed probe at Phase 5.5.4; `gh` active-account mismatch at Phase 6 Step 6.0 when auto-switch fails (added v1.2.3 for F34) |
| **B — Security floor** | Always pause for unavoidable manual OS/browser action, never automated | OAuth browser click at Phase 3.4 / 5.5; fine-grained PAT creation UI at Phase 5.5.1; admin password prompts during Phase -1 installs; 2FA challenges; GitHub device code flows |
| **C — Consent gates** | Dispatch per `mode` | Top-level consent card at Step 0; parsed-intent confirmation at Phase 0.4; pre-commit review card at Phase 6.1; pre-push / pre-merge confirmations |

Category C dispatch table:

| Gate | `detailed` | `semi-auto` | `auto` |
|---|---|---|---|
| Step 0 top-level card | block on `yes` | block on `yes` | render as informational log, proceed |
| Phase 0.4 parsed-intent card | block on `yes`/`edit`/`abort` | block on `yes`/`edit`/`abort` | render, proceed (user may still interject `pause` / `abort`) |
| Phase 3 SSH keygen paste-back | block on paste confirmation | block (concentrated privilege) | block (security floor — GitHub web UI) |
| Phase 3.5 remote add confirmation | block on `yes` | summary, proceed | summary, proceed |
| Phase 6.1 pre-commit review | block on `yes`/`inspect`/`abort` | block (concentrated privilege: first push) | summary, proceed |
| Phase 6.5 tag confirmation | block on `yes` | summary, proceed | summary, proceed |
| Phase 7 session-archive preview | block on `yes` | summary, proceed | summary, proceed |

**`semi-auto` is the intended default for repeat users**: it keeps blocking gates at the concentrated-privilege steps (SSH, PAT, first push, repo create) where silent failures are unrecoverable, while letting the rest of the protocol flow without typing. `detailed` is for first-time users who want to read and confirm every step. `auto` is for experienced users who understand the paradox guards and security floor still apply.

**Interjection is always accepted.** In any mode, the user can type `pause`, `abort`, or `frankenstein` and the orchestrator responds per Layer 0's working-style rule. Auto mode does not mean the user has surrendered control — it means the orchestrator does not ask before each non-privileged step.

**Phase -1 mode propagation.** When `phase-minus-one` is invoked at Phase -1, the orchestrator passes the same `mode` value through. The sibling skill's own 3-mode ladder (detailed / semi-auto / auto) accepts the same vocabulary by design — the two ladders stay aligned. If the user picks `auto` at the orchestrator and Phase -1 hits a security floor it cannot automate, the sibling pauses and resumes the same way the orchestrator does.

## Prerequisites

- **Layer 0** is loaded in the current Claude Code session. This is automatic on any machine that has `~/.claude/CLAUDE.md` installed. The orchestrator reads Layer 0 patterns (per-project SSH identity, `GH_TOKEN` env override, Chrome profile map) by reference, not by copy.
- **Claude Code CLI** is already running in the target project folder. Genesis does not bootstrap the CLI itself — that is Phase -2 (user-manual, external to the plugin).
- **The five sibling skills** are present under `skills/` at the plugin root: `phase-minus-one`, `phase-5-5-auth-preflight`, `journal-system`, `session-post-processor`, `pepite-flagging`. The `install-manifest.yaml` verification step confirms this.
- **Phase -1 may not yet have run** — the orchestrator invokes it as the first phase of the sequence. If `memory/reference/automation-stack.md` already exists, the orchestrator asks whether to skip Phase -1 or re-run it.

## The 7-phase master table — 1:1 mirror of `memory/master.md`

| # | Phase | Purpose | Skill(s) invoked | Runbook file | Consent gate |
|---|---|---|---|---|---|
| **-1** | Dependencies pre-flight | Detect dev stack, install gaps, batch sign-ins, batch restart, verify, offer bonuses | `phase-minus-one` | Inline below (pure skill pointer) | Inside `phase-minus-one` |
| **0** | Seed loading | Read `config.txt` + any mixed media in the input folder, parse the project intent | Built-in file reads, no skill | `phase-0-seed-loading.md` | Confirm input folder contents |
| **1** | Rules + memory architecture | Copy R1-R10 rules, create `memory/` subtree, seed `MEMORY.md`, invoke install-manifests of `phase-minus-one` + `journal-system` + `session-post-processor` + `pepite-flagging` | Built-in Write + 4 skill install-manifests | `phase-1-rules-memory.md` | Confirm project slug + rules variant |
| **2** | Research cache init | Create `.claude/docs/superpowers/research/INDEX.md`, seed entries from Layer 0 R8 universal sota cache | Built-in Write, no skill | `phase-1-rules-memory.md` § Phase 2 (folded) | Confirm seed entry subset |
| **3** | Git repo init + SSH identity | `git init`, generate per-project SSH key, register `github.com-<project>` alias, set git remote, first local commit staging | Manual paste-back + Layer 0 per-project SSH pattern | `phase-3-git-init.md` | Key creation consent + remote URL |
| **4** | Project-specific seeds | Write `memory/master.md`, design specs, initial skill stubs (if the project is a plugin), `README.md`, `CLAUDE.md` | Built-in Write, no skill | `phase-3-git-init.md` § Phase 4 (folded) | Confirm project vision summary |
| **5.5** | Auth pre-flight | SSH keygen cross-check, fine-grained PAT creation, empty repo creation on GitHub, 3-probe test | `phase-5-5-auth-preflight` | `phase-5-5-auth.md` (pointer) | Inside `phase-5-5-auth-preflight` |
| **6** | First bootstrap commit + push + PR + merge + tag | Stage, commit with SPDX, push via SSH, open PR with `GH_TOKEN`, squash merge, tag `v0.1.0` | Built-in Bash + `GH_TOKEN` env | `phase-6-commit-push.md` | Pre-merge confirmation |
| **7** | Resume prompt + session archive | Write `.claude/docs/superpowers/resume/<date>_bootstrap_to_v0_2.md`, invoke `session-post-processor` to archive the bootstrap session | Built-in Write + `session-post-processor` | `phase-6-commit-push.md` § Phase 7 (folded) | Post-processor halt-on-leak gate |

**Every phase is addressed in this table.** Phases -1 and 5.5 are thin skill-pointer phases — their detailed flow lives inside their respective skills and is not duplicated here. Phases 2, 4, 7 are folded into adjacent runbook files to keep the file count manageable (8 files instead of 12), but each has a dedicated section header inside its host file so the 1:1 mirror is preserved in content even when file boundaries differ.

## Phase -1 — inline skill pointer

Phase -1 is handled entirely by the `phase-minus-one` skill. The orchestrator's job is:

1. **Check** whether `memory/reference/automation-stack.md` already exists in the target project.
2. **If yes**: ask the user whether to skip Phase -1 (stack already verified) or re-run it (the user suspects drift). Default: skip.
3. **If no**: invoke the `phase-minus-one` skill with the full 7-sub-phase flow (`-1.0` baseline detection through `-1.7` optional bonus offer). Wait for the skill to write `memory/reference/automation-stack.md` and return.
4. **Exit condition**: `memory/reference/automation-stack.md` exists and lists at least `git`, `gh`, a browser, and a Claude Code CLI version as healthy.

The orchestrator never reimplements detection logic, mode ladders, or install flows. If `phase-minus-one` needs a fix, fix it there and the orchestrator automatically benefits.

## Phase 5.5 — inline skill pointer

Phase 5.5 is handled entirely by the `phase-5-5-auth-preflight` skill. The orchestrator's job is:

1. **Check** that Phase -1 has completed (`memory/reference/automation-stack.md` exists) and that Phase 4 has written a project slug that the auth skill can key off.
2. **Invoke** the `phase-5-5-auth-preflight` skill with the project slug from Phase 4 and the target GitHub owner from the user's consent card.
3. **Wait** for the skill to complete its six numbered steps (5.5.0 consent card through 5.5.5 verification card) and return. The three-probe test at 5.5.4 is the hard gate — if any probe is red, the skill surfaces a targeted recovery and the orchestrator stays paused until it re-runs 5.5.4 green.
4. **Exit condition**: `memory/reference/ssh_<project>_identity.md` and `memory/reference/github_<project>_account.md` exist in the target project, and the three probes are green.

See `phase-5-5-auth.md` for the thin pointer contract (slug passing, Chrome profile selection, which Layer 0 reference docs apply).

## The concentrated privilege — writing outside the Genesis repo

Every skill in Project Genesis has at most one concentrated privilege:

| Skill | Concentrated privilege |
|---|---|
| `phase-minus-one` | Running installers on the user's machine (mitigated by 3-mode ladder + consent per item) |
| `phase-5-5-auth-preflight` | Creating SSH keys + PATs + GitHub repos (mitigated by paste-back default + isolated copy-paste rule) |
| `journal-system` | None (speech-native capture, no external side effects) |
| `session-post-processor` | Writing redacted archives (mitigated by halt-on-leak gate) |
| `pepite-flagging` | Writing pointer files into sibling project directories (mitigated by per-target consent) |
| **`genesis-protocol`** | **Writing an entire new project directory outside the Genesis repo** (mitigated by top-level consent card + per-phase confirmation) |

The top-level consent card shown at Step 0 of the orchestrator contains:

- Target project folder absolute path
- Project slug (derived from folder name or user input)
- GitHub owner and repo name that will be created
- Chrome profile to use for GitHub web UI steps
- PAT scopes that will be requested
- License choice (default MIT)
- Plan tier (affects multidevice branch)
- Whether Phase -1 will run or be skipped
- Whether `pepite-flagging` will be installed into the downstream project (default yes, opt-out available)

The user must confirm the full card before Phase 0 starts. No silent bootstraps.

## Files in this skill

| File | Purpose |
|---|---|
| `SKILL.md` | This entry point — trigger phrases, 7-phase master table, skill pointers for -1 and 5.5, concentrated-privilege map |
| `phase-0-seed-loading.md` | Phase 0 runbook — `config.txt` parsing, mixed media handling, input folder convention |
| `phase-1-rules-memory.md` | Phase 1 + Phase 2 runbook — rules copy, `memory/` scaffold, 4 sibling-skill install-manifests, research cache INDEX + seed entries |
| `phase-3-git-init.md` | Phase 3 + Phase 4 runbook — `git init`, per-project SSH identity, project-specific seeds (master vision, specs, stubs) |
| `phase-5-5-auth.md` | Thin pointer to the `phase-5-5-auth-preflight` skill — slug passing contract, Chrome profile, Layer 0 refs |
| `phase-6-commit-push.md` | Phase 6 + Phase 7 runbook — first commit + push + PR + merge + tag, resume prompt, session archive invocation |
| `install-manifest.yaml` | Verification-only manifest (no dirs or files to create; confirms the five sibling skills exist) |
| `verification.md` | Two-mode health card — post-install (sibling skills present) + post-action (7 phases green, downstream project bootstrapped) |
| `rules/v1_rules.md` | Canonical R1-R10 rules template copied verbatim to the target's `.claude/docs/superpowers/rules/v1_rules.md` at Phase 1 Step 1.3. Relocated into the skill in v1.2.1 so the orchestrator works in personal-scope install (friction F29). |

## How the orchestrator runs — the ordered flow

The orchestrator is a strict sequence. It never runs phases in parallel. It never skips ahead on optimism.

1. **Step 0 — Paradox guards + top-level consent card**. Before rendering the consent card, run two structural pre-checks (a v1.2.1 defensive layer against conscious-strange-loop targets that surfaced as frictions F23 + F27 in the 2026-04-17 self-dogfood).

   - **Guard A — target-inside-orchestrator-tree (F23)**: compute the orchestrator plugin root as three levels above this `SKILL.md` file's absolute path (same walk used by `phase-1-rules-memory.md` Step 1.3 fallback). If the target absolute path starts with the orchestrator plugin-root absolute path, **STOP** with:

     ```
     ❌ Step 0 Guard A — target is inside the Genesis plugin tree

     Target:         <target>
     Plugin root:    <orchestrator-plugin-root>

     The orchestrator refuses to bootstrap a project inside its own
     plugin tree — every phase would corrupt the plugin's state (Phase 3
     git init nested, Phase 5.5 repo name collision, Phase 6 push to
     wrong origin).

     Recommended target: a sibling directory outside the plugin repo.
     Example: C:/Dev/Claude_cowork/<your-project>/

     Override (not recommended): there is no --allow-nested flag in
     v1.2.1. If you truly need this, create a directory outside the
     plugin and start over.
     ```

   - **Guard B — self-collision slug (F27)**: after the planned slug is resolved (either from `config.txt` at Phase 0.2 or derived from target folder name at the consent card), compare against the structural-stop list:

     - `project-genesis` (literal orchestrator slug)
     - the value of `"name"` in `<plugin-root>/.claude-plugin/plugin.json`, when that file resolves

     If the target slug matches any entry, **STOP** with:

     ```
     ❌ Step 0 Guard B — slug collision with orchestrator itself

     Proposed slug:  <slug>
     Collides with:  <reserved>

     Bootstrapping with the orchestrator's own slug would collide at
     Phase 5.5 when Genesis tries to 'gh repo create <owner>/<slug>' —
     the repo already exists. The strange-loop target is refused for
     safety.

     Pick a differentiated slug: append '-selfdogfood', '-test', a date
     stamp, or rename the project. Edit config.txt and re-invoke.
     ```

   If both guards pass, render the top-level consent card (the full plan, every field listed in the "concentrated privilege" section). Dispatch per `mode` — see `## Mode dispatch` for the full table:

   - `mode=detailed` (default) or `mode=semi-auto` → block until the user answers `yes`; on `no` or silence-then-`abort`, exit cleanly.
   - `mode=auto` → render the card as an informational log and proceed to Phase -1. The user can still interject with `pause`, `abort`, or `frankenstein` at any time and the orchestrator responds per Layer 0's working-style rule.

   Guards A and B always fire regardless of mode — mode only changes the consent card dispatch.
2. **Phase -1** — invoke `phase-minus-one` unless skipped.
3. **Phase 0** — run `phase-0-seed-loading.md`.
4. **Phase 1** + **Phase 2** — run `phase-1-rules-memory.md`. Phase 1 lands the memory scaffold; Phase 2 lands the research cache INDEX and seed entries.
5. **Phase 3** + **Phase 4** — run `phase-3-git-init.md`. Phase 3 lands git + SSH; Phase 4 lands project-specific content (master vision, specs, stubs).
6. **Phase 5.5** — invoke `phase-5-5-auth-preflight`. Three probes must be green before proceeding.
7. **Phase 6** + **Phase 7** — run `phase-6-commit-push.md`. Phase 6 lands the first PR and tag; Phase 7 lands the resume prompt and invokes `session-post-processor` to archive the bootstrap session.
8. **Verification** — run `verification.md` post-action mode. Health card must be GREEN across all phases before the orchestrator declares success.
9. **Genesis report** — emit a single summary block listing every phase outcome, every file created, every skill invoked, the resulting git tag, and the path to the resume prompt for the next session.

Any step that fails stops the orchestrator immediately. The orchestrator does not auto-retry failed phases. The user reads the error, fixes the issue (or aborts), and re-invokes the orchestrator — which reads `memory/reference/automation-stack.md`, `memory/reference/ssh_*_identity.md`, and the git state to resume from the right phase automatically.

## Anti-Frankenstein reminders

- **Do not reimplement any skill.** The orchestrator invokes, never duplicates. If a phase needs logic that lives in a sibling skill, invoke the sibling. If the sibling lacks the logic, fix the sibling and reinvoke — never copy the logic into the orchestrator.
- **Do not add automation beyond Option A pure Markdown in v0.8.0.** A Python driver is a v1.1 candidate at earliest, and only after the Markdown orchestrator has been dogfooded against at least one real downstream project.
- **Do not wire any hooks.** `SessionEnd` / `SessionStart` hooks stay deferred until after the manual-mode dogfood milestones from `session-post-processor`.
- **Do not create a "genesis-protocol runtime" folder outside the skill.** Everything the orchestrator needs lives in this one directory under `skills/`. No shared-state folder, no temp scratch, no `.genesis/` sidecar.
- **Do not skip the top-level consent card rendering.** The card is *rendered* in every mode — in `detailed` and `semi-auto` it blocks for confirmation, in `auto` it is printed as an informational log the user can interrupt. Silent bootstraps (no card at all, in any mode) are a Frankenstein trap. On a re-run from a partial bootstrap, the card is re-rendered with the fields already filled in and the mode-appropriate dispatch re-applied.
- **Do not call `phase-minus-one` from inside any other phase.** Phase -1 is the first phase, once per run. If a later phase discovers a missing dependency, it surfaces the gap and asks the user to re-run `phase-minus-one` — never re-invokes silently.
- **Do not let any phase write to the Genesis repo itself.** The orchestrator targets the downstream project folder. Writes to the Genesis repo would mean the orchestrator is accidentally dogfooding on itself inside a bootstrap run — a recursive loop with no base case. The worktree pattern from R2.1 is the safety net: the orchestrator runs on a folder that is NOT the Genesis repo.
- **If the user says `frankenstein`**, back out of the last proposal.

## What this skill does NOT do

- **Dry-run / preview mode.** v0.8.0 ships a conductor that actually runs. Dry-run is a v1.1 candidate once the first real downstream bootstrap has validated the flow.
- **Phase rollback / undo.** Failed phases stop the orchestrator; the user fixes and re-invokes. Rollback is a v2 candidate because rolling back Phase 5.5 (SSH + PAT + repo) is a separate tool.
- **Multi-project batch bootstrap.** One folder per invocation. Multi-project is a composition primitive the user builds on top of the orchestrator, not inside it.
- **Non-GitHub git hosts.** GitHub-only in v1.0. GitLab / Bitbucket / Codeberg / Gitea are v2 candidates with the same concentrated-privilege pattern.
- **Automatic language choice for the downstream project.** The user picks at Phase 0 via the consent card. Genesis does not infer a language from the input folder.
- **Non-Claude-Code plugin bootstraps.** v1.0 assumes the downstream project is either a Claude Code plugin or a regular software project — either way it gets the memory/research/journal/pepite scaffolding. Non-CLI artefacts (standalone docs sites, design systems, marketing pages) are out of scope until explicit pain is documented.

## Exit condition

The orchestrator is complete when:

- The top-level consent card was confirmed.
- All seven phases ran in order and returned GREEN.
- The downstream project has: `memory/MEMORY.md`, `memory/master.md`, `memory/journal/INDEX.md`, `memory/pepites/INDEX.md`, `memory/project/sessions/INDEX.md`, `.claude/docs/superpowers/research/INDEX.md`, `.claude/docs/superpowers/rules/v1_rules.md`, `.claude/docs/superpowers/resume/<date>_bootstrap_to_v0_2.md`.
- The downstream project has a git repo pointing at `git@github.com-<project>:<owner>/<repo>.git`, a first commit, a merged PR, and a tag `v0.1.0`.
- The downstream project has `.env.local` with `GH_TOKEN=<pat>` (gitignored).
- The bootstrap session's JSONL has been archived to `memory/project/sessions/<date>_bootstrap.md` via `session-post-processor`, and the halt-on-leak gate returned GREEN.
- The verification health card is GREEN across all 7 phases.
- The user has read the genesis report.

At that point the downstream project is ready for its first real session. The resume prompt at `.claude/docs/superpowers/resume/<date>_bootstrap_to_v0_2.md` is the hand-off — opening Claude Code in the downstream project folder and following R1.1 will load it automatically.

## Why this is the last skill before v1.0.0

The five sibling skills cover the individual phases. `genesis-protocol` is the piece that turns them into a protocol — the compositional glue that makes Genesis a product rather than a collection of utilities. Shipping the orchestrator closes the recursive loop: Genesis can now bootstrap a new project using the same skills it used to bootstrap itself. Every friction that surfaces during the first downstream bootstrap will inform v1.1, exactly the same dogfood pattern that took Genesis from v0.1 scaffold to v0.7 five-skill shipment.

The anti-Frankenstein inflection point is reached when the orchestrator lands cleanly without needing a single new skill, a single runtime, or a single hook. Composition is the ceiling.
