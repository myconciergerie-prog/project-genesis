<!-- SPDX-License-Identifier: MIT -->
---
name: SSH identity — genesis-web
description: Dedicated ed25519 SSH key and host alias used for git push/pull to github.com/myconciergerie-prog/genesis-web, keeping the project-genesis, Aurum, and all other projects' credentials untouched per Layer 0 per-project SSH identity pattern
type: reference
generated_at: 2026-04-20
---

# genesis-web — SSH identity

Generated 2026-04-20 during Phase 1 Task 1.1 of the v3.0 sub-project #1 landing implementation (Phase 5.5 auth-preflight for the new `genesis-web` sibling repo). Follows the Layer 0 per-project SSH identity pattern — dedicated key, dedicated host alias, `IdentitiesOnly yes` to prevent key ambiguity.

## Key

| Field | Value |
|---|---|
| Type | ed25519 |
| Private key | `~/.ssh/id_ed25519_genesis-web` |
| Public key | `~/.ssh/id_ed25519_genesis-web.pub` |
| Fingerprint | `SHA256:bNnCv24yPjx/0RqQ3j1+IXMsvgDanN91dA4slEOeo/Y` |
| Comment | `genesis-web@myconciergerie-prog` |
| Added to GitHub | 2026-04-20 via gh CLI (`gh ssh-key add --type authentication`) |
| GitHub key title | `genesis-web` |

## SSH config entry

Added to `~/.ssh/config` on 2026-04-20, additive next to the existing `github.com-genesis` and `github.com-aurum` aliases:

```
Host github.com-genesis-web
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_ed25519_genesis-web
  IdentitiesOnly yes
```

**`IdentitiesOnly yes` is critical** — it prevents ssh-agent from offering another key first (e.g. the Genesis or Aurum key, which would authenticate to the wrong repo context). Without this flag, SSH would try all loaded identities in order and potentially succeed with the wrong one.

## Git remote URL

```
git@github.com-genesis-web:myconciergerie-prog/genesis-web.git
```

Note: the host is `github.com-genesis-web` (the alias), **not** `github.com`. The alias resolves via `~/.ssh/config` to real `github.com` with the genesis-web-specific identity. This binding is what gives each project its own identity.

## Pre-flight test (passed on 2026-04-20)

```bash
ssh -T -o StrictHostKeyChecking=accept-new git@github.com-genesis-web
```

Expected output (which was returned successfully):

```
Hi myconciergerie-prog! You've successfully authenticated, but GitHub does not provide shell access.
```

This confirms the key binds to the correct GitHub identity. Exit code 1 is normal — GitHub doesn't provide shell access, so the connection closes after auth success.

## How to apply

- **All genesis-web git operations** (clone, push, pull, fetch) use this SSH alias. Never HTTPS with embedded PAT for this repo.
- **Initial clone** of the empty `myconciergerie-prog/genesis-web` repo created 2026-04-20:

  ```bash
  git clone git@github.com-genesis-web:myconciergerie-prog/genesis-web.git
  ```

- **Worktree creation** (R2.1): after `git clone . .claude/worktrees/<type>_YYYY-MM-DD_<theme>`, the clone inherits the parent's remote URL (which points to local disk). Immediately update:

  ```bash
  git remote set-url origin git@github.com-genesis-web:myconciergerie-prog/genesis-web.git
  ```

- **Moving the repo to a new machine**: copy both `~/.ssh/id_ed25519_genesis-web` and `~/.ssh/id_ed25519_genesis-web.pub` to the new machine's `~/.ssh/` directory, then re-add the `~/.ssh/config` `Host github.com-genesis-web` block. On Windows git-bash, permissions don't need to be tightened to 600 (SSH honors NTFS ACLs); on macOS/Linux, `chmod 600 ~/.ssh/id_ed25519_genesis-web` is required.

## Rotation

If the key is ever compromised or needs rotation:

1. Generate a new ed25519 key with the same comment:

   ```bash
   ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519_genesis-web_new -C "genesis-web@myconciergerie-prog" -N ""
   ```

2. Add the new public key to GitHub via gh CLI (title: `genesis-web — rotated YYYY-MM-DD`):

   ```bash
   gh ssh-key add ~/.ssh/id_ed25519_genesis-web_new.pub --title "genesis-web — rotated YYYY-MM-DD" --type authentication
   ```

3. Test authentication with the new key via `ssh -T -o IdentityFile=~/.ssh/id_ed25519_genesis-web_new git@github.com-genesis-web`
4. Replace old files: `mv ~/.ssh/id_ed25519_genesis-web_new ~/.ssh/id_ed25519_genesis-web && mv ~/.ssh/id_ed25519_genesis-web_new.pub ~/.ssh/id_ed25519_genesis-web.pub`
5. Delete the old public key from GitHub (`gh ssh-key list` → `gh ssh-key delete <id>`)
6. Update this memory file's `Fingerprint` field with the new SHA256

The host alias `github.com-genesis-web` stays the same through rotation — only the underlying `IdentityFile` pointed to by the alias changes.

## Related

- **Project Genesis SSH identity** (separate, additive, never touched): `~/.ssh/id_ed25519_genesis` / host alias `github.com-genesis`. See `memory/reference/ssh_genesis_identity.md`.
- **Aurum SSH identity** (separate, additive, never touched): `~/.ssh/id_ed25519_aurum` / host alias `github.com-aurum`. All three keys coexist in `~/.ssh/` and `~/.ssh/config` without conflict.
- **Layer 0 pattern reference**: `~/.claude/CLAUDE.md` "Per-project SSH identity" section
- **Genesis v3.0 sub-project #1 landing implementation plan**: `.claude/docs/superpowers/plans/2026-04-20-v3-sub1-landing-implementation.md`
