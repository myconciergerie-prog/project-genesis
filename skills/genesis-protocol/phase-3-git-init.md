<!-- SPDX-License-Identifier: MIT -->
---
name: Phase 3 + Phase 4 — Git init, SSH identity, project-specific seeds
description: Runbook for Phase 3 (git init + per-project SSH identity + git remote + initial staging) and Phase 4 (project-specific seeds — master vision, design specs, skill stubs if the project is a plugin, README). Together these turn the Phase 1/2 scaffold into a local git repo with a meaningful first commit ready to push at Phase 6 after Phase 5.5 authenticates the remote.
---

# Phase 3 + Phase 4 — Git init and project-specific seeds

Phase 3 turns the target folder into a tracked git repo with a dedicated SSH identity and a configured remote. Phase 4 populates the repo with project-specific content (master vision, design specs, initial skill stubs if the project is a plugin, a README). The two phases run back-to-back because:

1. Phase 4 needs git to exist (so the SPDX-headed files land as tracked).
2. Phase 5.5 needs a project slug and a clear "about-to-push" state to run the auth pre-flight against.
3. Splitting them would mean Phase 4 writes files into a git-tracked folder as a separate skill pass — cleaner to land them together.

Phase 3 handles the git plumbing (plumbing = low-level git mechanics); Phase 4 handles the content (content = the files that define what the project is). The runbook keeps each phase in its own section with its own exit condition.

## Prerequisites

- Phase 1 + Phase 2 are complete — `memory/MEMORY.md`, `CLAUDE.md`, rules, research cache INDEX are all present.
- `memory/project/bootstrap_intent.md` exists (Phase 0 output) with the project slug, vision, license, is-a-plugin flag, plan tier, scope locks.
- The target folder does **not yet** contain `.git/`. If it does, Phase 3 stops and asks whether the user meant to resume a partial bootstrap (in which case the orchestrator re-reads the intent and skips to the next incomplete phase).

## Phase 3 — The flow

### Step 3.1 — `git init` in the target folder

Run `git init` inside the target folder. Use `git init -b main` so the default branch is `main` (aligns with R2, the canonical main branch for all Genesis-bootstrapped projects).

After init, confirm:

- `.git/` exists
- `git config --local init.defaultBranch` returns `main` OR `git branch --show-current` returns `main` after the first commit

### Step 3.2 — Generate the per-project SSH identity

Per Layer 0's "per-project SSH identity" workflow pattern, generate a dedicated ed25519 key:

```bash
ssh-keygen -t ed25519 -f "$HOME/.ssh/id_ed25519_<slug>" -C "<slug>-genesis-bootstrap-<YYYY-MM-DD>" -N ""
```

- Use `$HOME` rather than `~` in shell commands — tilde expansion is shell-dependent (bash and zsh expand it, Windows `cmd` does not, and PowerShell only expands it in some contexts). `$HOME` resolves correctly in bash, zsh, and PowerShell (where `$HOME` is an automatic variable). Genesis supports all three as host shells for the bootstrap run.
- `<slug>` is the project slug from `bootstrap_intent.md`.
- The `-N ""` means no passphrase. Per-project keys are stored in `$HOME/.ssh/` with filesystem permissions; they are not extracted to a password manager. If the user opted for a passphrase in the top-level consent card, respect that choice and prompt for the passphrase here.
- The comment encodes slug + provenance + date for future forensics.

**Isolated copy-paste rule (from R9.1 / Layer 0)**: the public key and the host alias go into their own dedicated fenced blocks so the user can paste them unambiguously. The private key is **never** printed, logged, or copied.

### Step 3.3 — Register the SSH host alias

Append to `$HOME/.ssh/config` (create the file if missing):

```
Host github.com-<slug>
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_ed25519_<slug>
  IdentitiesOnly yes
```

The `IdentityFile` line keeps the `~` form — this block is OpenSSH's own config file, and OpenSSH parses `~` correctly on every supported OS regardless of shell. The `$HOME` vs `~` distinction only matters for shell commands (Step 3.2), not for the content of OpenSSH config files.

**Permissions**: `$HOME/.ssh/config` should be `0600` (owner read/write only). On POSIX systems run `chmod 0600 "$HOME/.ssh/config"`. On Windows, OpenSSH for Windows uses ACLs rather than POSIX mode bits; `chmod` inside git-bash is a no-op. OpenSSH usually auto-fixes inherited permissions on first use, but if `ssh -T` at Step 3.4 fails with a permissions warning, fix ACLs explicitly: `icacls "%USERPROFILE%\.ssh\config" /inheritance:r /grant:r "%USERNAME%:F"` in `cmd`, or the PowerShell equivalent.

The `IdentitiesOnly yes` is non-negotiable — without it, SSH tries every loaded key before reaching the project-specific one, and GitHub refuses the second attempt from the same source IP as a protection against enumeration.

### Step 3.4 — Add the public key to GitHub (paste-back or Playwright)

The user pastes the public key into the GitHub web UI at `https://github.com/settings/keys` — or, if Phase -1 installed Playwright MCP and the user opted in at the top-level consent card, the orchestrator drives the form programmatically.

**Phase 3 does not handle the PAT** — that is Phase 5.5's job. Phase 3 only lands the SSH key, because git init + remote URL configuration needs SSH working. PAT is for the API-side work (repo creation, PR creation).

After the key is added, verify with:

```bash
ssh -T git@github.com-<slug>
```

Expected output: `Hi <username>! You've successfully authenticated, but GitHub does not provide shell access.`

If the test fails, stop and hand the recovery to the user. Common causes: typo in `~/.ssh/config`, wrong host alias, key not yet propagated on GitHub (wait 30s and retry once), Chrome signed into the wrong profile.

### Step 3.5 — Set the git remote

```bash
git remote add origin git@github.com-<slug>:<owner>/<repo>.git
```

Where `<owner>` and `<repo>` come from `bootstrap_intent.md` (owner defaults to the GitHub owner confirmed in the top-level consent card; repo defaults to the project slug).

**The remote repo does not exist yet on GitHub at this point.** It will be created at Phase 5.5 via the empty repo web-UI walkthrough. Phase 3 only configures the remote URL locally — the first push at Phase 6 is what actually uses it.

Verify with `git remote -v` — should show two lines (`origin fetch` + `origin push`) with the SSH alias URL.

### Step 3.6 — Stage the Phase 1 + Phase 2 scaffold

Run `git add -A` and `git status` to list everything landed so far:

- `CLAUDE.md`
- `.claude/docs/superpowers/rules/v1_rules.md`
- `.claude/docs/superpowers/research/INDEX.md` + seed entries
- `memory/MEMORY.md`
- `memory/master.md` (placeholder)
- `memory/project/bootstrap_intent.md`
- `memory/project/sessions/INDEX.md`
- `memory/journal/INDEX.md`
- `memory/pepites/INDEX.md`
- `memory/user/README.md`, `memory/feedback/README.md`, `memory/themes/README.md`, `memory/reference/README.md`

**Do not commit yet.** Phase 4 adds more files; the first commit happens at Phase 6 after Phase 4 and Phase 5.5 complete.

### Step 3.7 — Write `.gitignore`

Write `.gitignore` at the target folder root with the canonical Genesis entries:

```
# Environment
.env.local
.env.*.local

# SSH / PAT — never commit
*.pem
*.key
id_ed25519_*

# Claude Code project state (user-local, not repo)
.claude/worktrees/

# OS
.DS_Store
Thumbs.db
desktop.ini

# Editor
.vscode/
.idea/
*.swp
*.swo

# Python (for skills that use run.py)
__pycache__/
*.pyc
.venv/
venv/

# Node (for skills that use JavaScript)
node_modules/
```

The `.env.local` line is critical — Phase 5.5 writes `GH_TOKEN=<pat>` to that file, and it must never land in git. The `id_ed25519_*` line is belt-and-braces (SSH keys live in `~/.ssh/`, not in the repo, but a slip of the cp would leak a private key into git otherwise).

## Phase 4 — The flow

### Step 4.1 — Write `memory/master.md` with the real vision

Replace the Phase 1 placeholder `memory/master.md` with the real stable vision. Pull from `bootstrap_intent.md`:

- Project name + one-paragraph vision
- Stack hints (language, framework, hosting) as a "Stack" section
- License choice
- Rules summary pointing at `.claude/docs/superpowers/rules/v1_rules.md`
- Target for v1.0 (self-rating target = 8.5/10 per R10, same as Genesis)
- Scope locks (if any)

Use the Genesis project's own `memory/master.md` as the structural model — same section headers, adapted content. Keep it in English per R9 (Layer 0 language policy).

### Step 4.2 — Write the initial `README.md`

Write `README.md` at the target folder root with:

- Project title (from intent)
- One-line description
- Status badge: "Bootstrap complete — v0.1.0"
- Stack line
- Quick-start for a contributor
- License line + SPDX comment
- Pointer to `CLAUDE.md` for any Claude Code sessions

Do **not** auto-generate prose from the vision paragraph — copy the vision verbatim into a "## What this project is" section. Let the user edit the README later; the Phase 4 version is scaffolding.

### Step 4.3 — Write `CHANGELOG.md`

Write `CHANGELOG.md` with the v0.1.0 entry:

```markdown
# Changelog

## [0.1.0] — <YYYY-MM-DD>

### Added
- Project bootstrap via Genesis protocol
- Memory architecture (user / feedback / project / reference / themes / journal / pepites)
- Research cache with TTL (sota / stack / archive)
- Rules R1–R10 adapted from Genesis canonical
- Per-project SSH identity `github.com-<slug>`
- First GitHub repo: `<owner>/<repo>`

### Self-rating (5 axes)
*(filled in at the end of the bootstrap session by the user)*

- Pain-driven: ?/10
- Prose cleanliness: ?/10
- Best-at-date: ?/10
- Self-contained: ?/10
- Anti-Frankenstein: ?/10

**Average: ?/10**
```

The self-rating block stays with question marks until the first real session of the downstream project, when the user decides how the bootstrap went. The default bootstrap rating is always deferred — the orchestrator does not pre-fill.

### Step 4.4 — Write initial skill stubs (conditional: is-a-plugin = yes)

If `bootstrap_intent.md` has `is-a-plugin: yes`, Phase 4 lands a `.claude-plugin/plugin.json` manifest and a `skills/README.md` that explains where skills go. No stub skill files are written — the first skill is written in the first real session, not during bootstrap.

Template `.claude-plugin/plugin.json`:

```json
{
  "name": "<slug>",
  "version": "0.1.0",
  "description": "<one-line description from bootstrap_intent>",
  "author": {
    "name": "<github owner>",
    "url": "https://github.com/<owner>"
  },
  "homepage": "https://github.com/<owner>/<repo>",
  "repository": "git@github.com-<slug>:<owner>/<repo>.git",
  "license": "<license>",
  "keywords": []
}
```

Template `skills/README.md`:

```markdown
<!-- SPDX-License-Identifier: <license> -->

# skills/

This directory holds the skills <project> ships. Per Claude Code plugin
convention (Q2 2026), `skills/` is at the plugin root level — NOT inside
`.claude-plugin/`. Only `plugin.json` lives in `.claude-plugin/`.

Each skill is a subdirectory with its own content (SKILL.md at minimum,
plus optional templates / runtime / verification).

*(No skills yet — added in the first real session, not during bootstrap.)*
```

If `is-a-plugin: no`, Phase 4 skips the plugin manifest and `skills/` — the downstream project is a regular software project and does not need the plugin structure.

### Step 4.5 — Run the scope lock imprint (if any)

If `bootstrap_intent.md` lists scope locks (other projects that must be treated as frozen during this bootstrap, like Genesis's Aurum freeze), write `memory/project/<lock_slug>_frozen_scope_lock.md` for each lock with:

- What is frozen (repo name, commit hash if known)
- Until when (trigger to unfreeze — e.g. "Genesis v1.0 shipped")
- Why (context the user provided at Phase 0)
- Hard rule (no commits, no PRs, no edits allowed in any session opened on this project)

The `<lock_slug>` is the machine slug derived at Phase 0 Step 0.2 from the free-form scope lock entry in `config.txt` (first whitespace-terminated token, lowercased, punctuation stripped, internal non-alphanumerics replaced with `-`). The verbatim original string from `config.txt` goes into the file's "Until when" / "Why" body as context — Phase 4 does not re-parse or re-split it. If Phase 0 stored both a derived slug and a verbatim string in `bootstrap_intent.md`, Phase 4 reads both fields; it never re-derives.

Scope locks are **additive** — if the downstream project is bootstrapped as a spin-off of another project, those locks propagate by explicit user declaration, not by inheritance.

### Step 4.6 — Re-stage everything

After Phase 4 writes all of the above, run `git add -A` and `git status` again. The staging should now include everything from Phase 1 + Phase 2 + Phase 3.7 + Phase 4.1-4.5.

Phase 5.5 runs next — it does not touch the staged content, it only creates the GitHub-side identity (PAT + empty repo). The staged content stays put through Phase 5.5 and becomes the first commit at Phase 6.

## Exit condition

Phase 3 + Phase 4 are complete when:

- `.git/` exists at the target folder root
- `git config --local init.defaultBranch` is `main` OR equivalent branch state
- `~/.ssh/id_ed25519_<slug>` (private) + `.pub` (public) exist with correct permissions (0600 / 0644)
- `~/.ssh/config` contains the `github.com-<slug>` Host block with `IdentitiesOnly yes`
- `ssh -T git@github.com-<slug>` returned the green authentication message
- `git remote -v` shows the SSH alias URL for origin
- `.gitignore` exists and covers `.env.local`, SSH keys, `.claude/worktrees/`, OS/editor cruft, Python/Node build artifacts
- `memory/master.md` has the real vision (not the Phase 1 placeholder)
- `README.md` + `CHANGELOG.md` exist at the target folder root
- `.claude-plugin/plugin.json` + `skills/README.md` exist if `is-a-plugin: yes`, otherwise skipped
- `memory/project/<lock_slug>_frozen_scope_lock.md` exists for every scope lock declared
- `git status` shows the full staged tree ready for the first commit at Phase 6
- No content has been committed yet — Phase 6 handles the commit

## Common failures

- **`ssh -T` fails after pushing the key** — 30s propagation delay, retry once, then stop if still failing
- **`~/.ssh/config` has conflicting `Host github.com-*` blocks from earlier projects** — do not auto-merge. Ask the user, append the new block, and verify the new alias works
- **Target folder contains a stale `.git/`** — stop, ask whether the user wanted to resume a partial bootstrap. Never blow away a `.git/` directory silently
- **`is-a-plugin: yes` but `plugin.json` already exists in the target folder** — stop, surface the situation, ask the user whether to keep the existing manifest or overwrite
- **Scope lock target repo does not exist on the machine** — warn but do not block. The lock is a rule, not a verification target

## Anti-Frankenstein reminders

- **Do not auto-push anything in Phase 3 or Phase 4.** Staging only. The first push happens at Phase 6, after Phase 5.5 creates the empty target repo
- **Do not generate prose from the vision.** Copy the user's words verbatim into `memory/master.md` and `README.md`. Paraphrase is Frankenstein territory
- **Do not create more than one SSH key per project.** One ed25519, one alias, one project. Reusing an existing key "because it's easier" is the exact Frankenstein pattern Layer 0 prohibits
- **Do not write stub skill files at Phase 4.** Even if `is-a-plugin: yes`, the first actual skill is written in the first real session, not during the bootstrap run. Phase 4 only lands the directory structure and the manifest
- **Do not copy scope lock files from the source project's memory.** Write them fresh per the user's declaration at Phase 0. Copying would propagate stale status
- **If the user says `frankenstein`**, back out of the last addition and simplify
