<!-- SPDX-License-Identifier: MIT -->
---
name: GitHub account target — Project Genesis
description: Target GitHub account and repo for Project Genesis operations, with fine-grained PAT env pattern, SSH alias binding, and known PAT scope gap discovered during v1 bootstrap
type: reference
---

# GitHub account target — Project Genesis

## Target

| Field | Value |
|---|---|
| Account / org | `myconciergerie-prog` |
| Email | `myconciergerie@gmail.com` |
| Repo | `myconciergerie-prog/project-genesis` |
| Visibility | Private (may toggle to public after v1.0.0 polish) |
| Default branch | `main` |
| Profile URL | https://github.com/myconciergerie-prog |
| Repo URL | https://github.com/myconciergerie-prog/project-genesis |
| Repo ID | `1210872943` (returned by `gh api repos/myconciergerie-prog/project-genesis` during pre-flight) |
| Created | 2026-04-14 via web UI (fine-grained PATs cannot create user repos via API — pattern documented in Layer 0) |

## Fine-grained PAT

Stored in `.env.local` (gitignored from first commit) as `GH_TOKEN`. Never committed to git history.

### Scopes at creation (2026-04-14)

- Contents: **Read and write**
- Metadata: **Read** (auto)
- Pull requests: **Read and write**
- Workflows: **Read and write**
- Resource owner: `myconciergerie-prog` (selected via dropdown — NOT personal account default)
- Repository access: **All repositories** (not "Only select", because the repo didn't exist at PAT creation time)
- Expiration: **90 days** (from 2026-04-14 — rotate before expiration)

### Missing scope discovered 2026-04-14

**`Administration: Read and write`** — needed to PATCH repo description / topics / visibility / settings via API. A `gh api --method PATCH repos/myconciergerie-prog/project-genesis -f description=...` call during Étape 4c returned **HTTP 403 "Resource not accessible by personal access token"**.

Consequence: the repo description was initially set with a garbled copy-paste (user copied a table cell including inline notes) and cannot be corrected via API until the PAT is rotated with the Administration scope added. Workaround: edit the description via web UI at the Code tab → About panel → pencil icon.

**This gap is the single biggest addition to the canonical PAT scope checklist for v1 template Phase 5.5**:

```
Canonical v1 PAT scope list (updated 2026-04-14):
  - Contents: Read and write
  - Metadata: Read (auto)
  - Pull requests: Read and write
  - Workflows: Read and write
  - Administration: Read and write   ← added after this session's learning
```

## Usage pattern

**SSH handles git** (clone, push, pull, fetch):

```bash
git clone git@github.com-genesis:myconciergerie-prog/project-genesis.git
git push origin <branch>
```

**`GH_TOKEN` env handles API** (`gh pr create`, `gh pr merge`, `gh api`):

```bash
GH_TOKEN="$GH_TOKEN" gh pr create --title "..." --body "..."
GH_TOKEN="$GH_TOKEN" gh pr merge <pr-number> --squash
GH_TOKEN="$GH_TOKEN" gh api repos/myconciergerie-prog/project-genesis
```

**Never `gh auth login`** — that would switch the global `gh` auth on this machine and affect every other project. Per Layer 0 "GitHub API auth via GH_TOKEN env override" pattern and the additive auth rule, always use env override.

## Commit authoring

Configure git locally in worktrees (NOT globally, to avoid affecting other projects):

```bash
cd .claude/worktrees/<type>_YYYY-MM-DD_<theme>/
git config user.email myconciergerie@gmail.com
git config user.name myconciergerie-prog
```

## Chrome profile for web UI paste-back

**Profile 2** — `myconciergerie@gmail.com`. This is the profile where the user is signed into GitHub as `myconciergerie-prog`. See `~/.claude/CLAUDE.md` "Machine-specific reference — Chrome profiles" for the full mapping.

**Never use `Default` profile** for Genesis work — Default belongs to another project.

Canonical launcher (only if Chrome is not already open on Profile 2 — otherwise use paste-back per the no-new-windows rule):

```powershell
powershell -NoProfile -Command "Start-Process 'C:\Program Files\Google\Chrome\Application\chrome.exe' -ArgumentList '--profile-directory=Profile 2','<URL>'"
```

## Pre-flight tests (Étape 4c, passed 2026-04-14)

Three probes ran successfully:

1. **SSH test**: `ssh -T -o StrictHostKeyChecking=accept-new git@github.com-genesis` → "Hi myconciergerie-prog! You've successfully authenticated..."
2. **PAT user test**: `GH_TOKEN="$GH_TOKEN" gh api user` → returned user data (login: myconciergerie-prog, id: 276056977)
3. **Repo existence test**: `GH_TOKEN="$GH_TOKEN" gh api repos/myconciergerie-prog/project-genesis` → returned repo data (private: true, default_branch: main, permissions.admin: true)

These three probes are now codified as the canonical **Phase 5.5 exit condition** in the v1 template — see `.claude/docs/superpowers/specs/v1_phase_5_5_auth_preflight_learnings.md` Learning 3.

## PAT rotation

Before 90 days elapse from 2026-04-14:

1. Create a new fine-grained PAT at `https://github.com/settings/personal-access-tokens/new` with the **updated scope list** (including `Administration: Read and write`)
2. Copy the new token value
3. Update `GH_TOKEN=<new-token>` in `.env.local`
4. Test with `GH_TOKEN="$GH_TOKEN" gh api user`
5. Delete the old PAT from `https://github.com/settings/personal-access-tokens`
6. Update this memory file's "Scopes at creation" section with the new creation date and the expanded scope list

## Related

- **Aurum GitHub account** (separate, additive, never touched): same `myconciergerie-prog` org but different repo `myconciergerie-prog/aurum-ai`
- **SSH identity pairing**: `memory/reference/ssh_genesis_identity.md` (dedicated `id_ed25519_genesis` key + `github.com-genesis` host alias)
- **Layer 0 pattern**: `~/.claude/CLAUDE.md` "GitHub API auth via GH_TOKEN env override" section + "Fine-grained PAT scope checklist"
