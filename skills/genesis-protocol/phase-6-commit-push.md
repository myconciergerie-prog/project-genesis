<!-- SPDX-License-Identifier: MIT -->
---
name: Phase 6 + Phase 7 — First commit, push, PR, merge, tag, resume prompt, session archive
description: Runbook for Phase 6 (staging review → first commit → push → PR → squash merge → tag v0.1.0) and Phase 7 (write resume prompt + invoke session-post-processor to archive the bootstrap session). These two phases run back-to-back because Phase 7 depends on Phase 6's tag existing, and both together form the clean handoff from bootstrap to first real session.
---

# Phase 6 + Phase 7 — First commit, PR, tag, resume prompt, session archive

Phase 6 turns the staged bootstrap tree into a real commit, pushes it, opens a PR, squash-merges it to `main`, and tags `v0.1.0`. Phase 7 writes the resume prompt for the next session and invokes `session-post-processor` to archive the bootstrap session's JSONL transcript to a redacted Markdown archive. Both phases run back-to-back because:

1. Phase 7's session archive references the tag created at Phase 6.
2. Phase 7's resume prompt summarizes the Phase 6 commit + PR + merge outcome.
3. The session-post-processor invocation at Phase 7 is the orchestrator's last tool call before the genesis report — splitting it off into a standalone runbook would leave a two-step tail phase dangling.

Phase 6 is the last concentrated-privilege phase (writes to the GitHub remote). Phase 7 is the cleanup + handoff.

## Prerequisites

- Phase 5.5 is complete — SSH identity, PAT, empty repo, three probes all GREEN.
- The working tree in the target folder has all Phase 1–4 files staged (`git status` shows a full tree under "Changes to be committed").
- `.env.local` contains `GH_TOKEN=<pat>` and is gitignored.
- `CLAUDE.md`, `memory/MEMORY.md`, rules, research cache, memory scaffolding, master vision, README, CHANGELOG are all present and unstaged-free.
- The top-level consent card from `SKILL.md` Step 0 is still in effect (no user-driven scope change since Phase 5.5).

## Phase 6 — The flow

### Step 6.1 — Pre-commit review

Run `git status` and list every staged file. Render a short summary card:

```
📦 Ready to commit (first bootstrap commit)

Target repo : <owner>/<repo>
Tag         : v0.1.0 (will be created after squash merge)

Files staged (<count>):
  CLAUDE.md
  .gitignore
  README.md
  CHANGELOG.md
  memory/MEMORY.md
  memory/master.md
  memory/project/bootstrap_intent.md
  memory/project/sessions/INDEX.md
  memory/journal/INDEX.md
  memory/pepites/INDEX.md
  memory/reference/{ssh_<slug>_identity,github_<slug>_account}.md
  memory/{user,feedback,themes}/README.md
  .claude/docs/superpowers/rules/v1_rules.md
  .claude/docs/superpowers/research/INDEX.md + <N> seed entries
  .claude-plugin/plugin.json           (if is-a-plugin: yes)
  skills/README.md                     (if is-a-plugin: yes)
  memory/project/<lock>_frozen_scope_lock.md  (if scope locks)

Proceed with first commit?  (yes / inspect / abort)
```

- **yes** → proceed to Step 6.2
- **inspect** → render a `git diff --cached --stat` output and ask again
- **abort** → exit cleanly, leave the staged state in place for the user to resolve manually

### Step 6.2 — First commit

Run:

```bash
git -C <target_folder> commit -m "feat(bootstrap): initial Genesis bootstrap of <project name> [v0.1.0]

Seeded via Project Genesis 7-phase protocol:
- Phase -1 dependencies pre-flight
- Phase 0 seed loading from config.txt
- Phase 1+2 rules, memory architecture, research cache
- Phase 3+4 git init, per-project SSH identity, project-specific seeds
- Phase 5.5 auth pre-flight (SSH + PAT + empty repo + 3-probe gate)
- Phase 6 this commit
- Phase 7 resume prompt + session archive (next)

License: <license>
Genesis version: <genesis_plugin_version>
"
```

The commit message is multi-line and structured so `git log` on the downstream project shows an auditable trail of the bootstrap phases. No trailing `Co-Authored-By` line — the downstream project is user-owned, not co-authored by Claude.

### Step 6.3 — Push to remote

```bash
git -C <target_folder> push -u origin main
```

Expected result: the empty remote repo created at Phase 5.5 now has the first commit on `main`. If the push fails:

- **`error: src refspec main does not match any`** → the local branch is not yet `main`. Run `git branch -m master main` and retry
- **`Permission denied (publickey)`** → SSH alias misconfigured. Phase 5.5 should have caught this; surface the failure and halt
- **`remote contains work you do not have`** → the remote was not empty (someone created a README or LICENSE during the empty-repo-create step). Pull with `--rebase`, resolve if needed, re-push

### Step 6.4 — Open the PR

The bootstrap commit is directly on `main`, which is unusual for Genesis (R2 worktree discipline says all work happens in a feat branch merged via PR). The bootstrap is the one exception: the first commit **is** `main`, because there is no base branch yet. The PR pattern kicks in at v0.2.0 onwards.

Therefore: **Phase 6 does NOT open a PR for the bootstrap commit.** The commit is already on `main`; there is no feat branch to merge. The PR / squash-merge flow is exclusive to v0.2.0+.

Skip Step 6.4 for the bootstrap run. The remaining steps (6.5 tag, 6.6 verify) still apply.

### Step 6.5 — Tag `v0.1.0`

```bash
git -C <target_folder> tag -a v0.1.0 -m "v0.1.0 — initial Genesis bootstrap"
git -C <target_folder> push origin v0.1.0
```

The tag is the proof-of-bootstrap. Phase 7's resume prompt references it.

### Step 6.6 — Verify the remote state

```bash
git -C <target_folder> ls-remote origin main
git -C <target_folder> ls-remote origin v0.1.0
```

Both should return non-empty results with matching SHAs. If either is empty, the push failed silently and the orchestrator halts.

Optional verification: `gh api repos/<owner>/<repo>` via `GH_TOKEN` from `.env.local` — should return 200 with the repo metadata.

## Phase 7 — The flow

### Step 7.1 — Write the resume prompt

Write `.claude/docs/superpowers/resume/<YYYY-MM-DD>_bootstrap_to_v0_2.md` in the target folder with:

```markdown
<!-- SPDX-License-Identifier: <license> -->
---
name: Resume prompt — <YYYY-MM-DD> bootstrap → v0.2.0 first real session
description: Handoff from the Genesis bootstrap session to the first real session of <project>. The bootstrap committed v0.1.0; v0.2.0 is the first application-specific work.
type: resume
previous_session: Genesis bootstrap
next_action: First real session — pick the first skill / feature to implement per <project>'s master vision.
---

# Resume prompt — <YYYY-MM-DD> bootstrap → v0.2.0

## Context — what the bootstrap session did

The bootstrap session ran the Genesis 7-phase protocol against this folder:

1. Phase -1 dependencies pre-flight verified the dev stack
2. Phase 0 parsed config.txt into memory/project/bootstrap_intent.md
3. Phases 1+2 landed rules, memory, and research cache
4. Phases 3+4 initialized git, SSH identity, and project-specific seeds
5. Phase 5.5 created the GitHub identity (SSH + PAT + repo + 3-probe gate)
6. Phase 6 committed v0.1.0 and pushed to main
7. Phase 7 (this prompt) closes out the bootstrap

**Current state**:
- Repo: <owner>/<repo>
- Main branch: at v0.1.0 on origin
- SSH alias: github.com-<slug>
- PAT: stored in .env.local (gitignored)

## What v0.2.0 needs to do

v0.2.0 is the first real session. Pick the first deliverable per
memory/master.md's vision. For software projects: implement the first
feature end-to-end in a feat branch, tag v0.2.0. For plugin projects:
implement the first skill in skills/<skill_name>/ with its SKILL.md,
install-manifest.yaml, verification.md, tag v0.2.0. Follow R2 worktree
discipline — the bootstrap commit was the last time main received a
direct commit.

## Things to NOT do in v0.2.0

- Do not skip R1.1 session open ritual
- Do not commit directly to main (use a feat worktree per R2)
- Do not reimplement Genesis's orchestrator logic — if Genesis is wrong,
  fix it in the Genesis repo, not here
- Do not wire hooks until at least three successful manual dogfood runs
  have validated the underlying skill (same discipline as Genesis's
  session-post-processor)

## Exact phrase for the next session

Open Claude Code in the target folder and say:

    On démarre v0.2.0 — première session réelle après le bootstrap
    Genesis. Lis memory/master.md + memory/project/bootstrap_intent.md
    pour la vision, puis propose le premier livrable en feat worktree.
```

### Step 7.2 — Invoke `session-post-processor`

Invoke the sibling `session-post-processor` skill with the target folder as the `cwd` and the current JSONL transcript as the input. The sibling's seven-step flow runs:

1. Locate the target JSONL (the bootstrap session's transcript, the most recent file under `~/.claude/projects/<cwd-slug>/`)
2. Parse the JSONL stream (drop `file-history-snapshot`, classify records)
3. Run the redaction pass (GitHub PATs, SSH private keys, API tokens, `.env.local` values)
4. Emit the Markdown archive to `memory/project/sessions/<YYYY-MM-DD>_bootstrap.md`
5. Run the halt-on-leak verification — if RED, delete the archive and halt the orchestrator
6. Update `memory/project/sessions/INDEX.md` with a one-line entry
7. Emit the health card — must be GREEN

Because this is a **bootstrap session**, the JSONL contains:

- The PAT as a paste-back value shown to the user at Phase 5.5 Step 5.5.2 — **MUST be redacted**
- The SSH public key — not secret, leave in place
- The SSH private key — never printed, should not appear in the transcript, but the redaction pattern catches it if it does
- Potentially the user's Google account email or GitHub username — not redacted (those are identifiers, not secrets)

The halt-on-leak gate at Step 5 is the final safety net. If it RED-flags, the bootstrap run still succeeded (the downstream project exists), but the session archive was not written and the user must inspect the pattern miss before any future sessions of the downstream project get their transcripts archived.

### Step 7.3 — Write the session memory entry

After the session archive is written successfully (halt-on-leak GREEN), also write a compact memory entry at `memory/project/session_bootstrap_<YYYY-MM-DD>.md` with:

- Session goal: "Bootstrap <project> via Genesis protocol"
- Phases executed (1-7) and their outcomes
- Files created (count by category)
- Git tag created: `v0.1.0`
- Time elapsed (if easily derived)
- Self-rating placeholder: the user fills this in at the first real session, not during the bootstrap

The archive from `session-post-processor` is the full transcript; the memory entry is the 1-page summary. Both exist because one is a record and the other is a pointer.

### Step 7.4 — Update `memory/MEMORY.md` with the new entries

Append to `memory/MEMORY.md` under the Project section:

```markdown
- [Session bootstrap — <YYYY-MM-DD>](project/session_bootstrap_<YYYY-MM-DD>.md) — Genesis protocol 7-phase run, v0.1.0 tagged
```

And the resume prompt reference:

```markdown
## Resume prompts

- [<YYYY-MM-DD> bootstrap → v0.2.0](.claude/docs/superpowers/resume/<YYYY-MM-DD>_bootstrap_to_v0_2.md)
```

These additions are committed in a small follow-up commit at Step 7.5.

### Step 7.5 — Second commit with the session memory additions

Phase 7 adds files that did not exist at Phase 6's commit: the resume prompt, the session archive, the session memory entry, and the updated `memory/MEMORY.md`. These land in a second commit on `main`:

```bash
git -C <target_folder> commit -m "chore(bootstrap): session memory + resume prompt"
git -C <target_folder> push origin main
```

No new tag — the v0.1.0 tag is on the Phase 6 commit. The Phase 7 commit is a chore on top of the tag.

### Step 7.6 — Emit the genesis report

Render a single summary block that the user reads as the final output of the orchestrator run:

```
✅ Genesis bootstrap complete

Project     : <name>
Folder      : <absolute path>
Repo        : <owner>/<repo>
Branch      : main @ <sha> (HEAD after chore commit)
Tag         : v0.1.0
License     : <license>

Phases executed:
  -1  Dependencies pre-flight .................. <skipped | green>
   0  Seed loading ............................. green
   1  Rules + memory ........................... green
   2  Research cache ........................... green
   3  Git init + SSH ........................... green
   4  Project seeds ............................ green
   5.5 Auth pre-flight ......................... green (3/3 probes)
   6  First commit + push + tag ................ green
   7  Resume prompt + session archive .......... green (halt-on-leak GREEN)

Files created   : <count>
Skills invoked  : phase-minus-one, phase-5-5-auth-preflight,
                  journal-system, session-post-processor,
                  pepite-flagging
Session archive : memory/project/sessions/<date>_bootstrap.md
Resume prompt   : .claude/docs/superpowers/resume/<date>_bootstrap_to_v0_2.md

Next action: open Claude Code in the target folder and start v0.2.0.
```

The genesis report is the last thing the user sees before the orchestrator exits. It is the "you are done" signal.

## Exit condition

Phase 6 + Phase 7 are complete when:

- `git log --oneline` in the target folder shows at least two commits (Phase 6 bootstrap, Phase 7 chore)
- `git tag -l v0.1.0` returns `v0.1.0`
- Remote `origin` has `main` and `v0.1.0` pushed
- `memory/project/session_bootstrap_<date>.md` + `memory/project/sessions/<date>_bootstrap.md` + `.claude/docs/superpowers/resume/<date>_bootstrap_to_v0_2.md` all exist and are committed
- `memory/MEMORY.md` has been updated with pointers to the new session memory and resume prompt
- `session-post-processor` halt-on-leak verification returned GREEN
- The genesis report has been emitted

## Common failures

- **Push to empty remote fails with `remote contains work you do not have`** — the repo was not truly empty at Phase 5.5. Pull with rebase, resolve, re-push. Record the incident in `memory/project/session_bootstrap_<date>.md`
- **Halt-on-leak RED at Phase 7.2** — the session JSONL contains a redaction-miss. The session archive is deleted. The user must audit the redaction pattern set in the Genesis plugin (`skills/session-post-processor/redaction-patterns.md`) and strengthen it before the downstream project's first real session generates another archive
- **Tag push fails with `tag already exists`** — some prior aborted bootstrap left a v0.1.0 tag behind. Stop, surface, ask whether to force-move or pick v0.1.1
- **Second commit at Phase 7.5 fails with `nothing to commit`** — means Phase 7 did not add any new files. Surface as a warning; the bootstrap is still valid, but the missing resume prompt is a gap the user should investigate
- **`gh api repos/...` verification fails with 404** — the PAT may have the wrong resource owner. Stop, surface, direct to Phase 5.5 for rerun

## Anti-Frankenstein reminders

- **Do not open a PR for the bootstrap commit.** The bootstrap is the one direct-to-main exception. All subsequent commits go via feat branch + PR
- **Do not squash the two commits into one.** Phase 6 and Phase 7 have distinct purposes; keeping them as separate commits preserves the auditability (bootstrap commit = what Genesis wrote; chore commit = session memory + resume = what happened during the run)
- **Do not auto-retry on halt-on-leak RED.** The gate is the gate. The user must audit before any retry
- **Do not skip the session archive invocation "to save time"**. The archive is the provenance record for every bootstrap. Skipping it means a v0.2.0 session cannot read what happened during the bootstrap except by re-reading `git log`, which is thinner
- **Do not customize the genesis report template.** Keep it uniform across every downstream project so `grep` across `memory/project/sessions/` works naturally
- **If the user says `frankenstein`**, halt immediately — the orchestrator is near the end of the run, but the last-step discipline is the same as the first-step discipline
