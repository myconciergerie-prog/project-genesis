<!-- SPDX-License-Identifier: MIT -->
---
name: SSH identity — Project Genesis
description: Dedicated ed25519 SSH key and host alias used for git push/pull to github.com/myconciergerie-prog/project-genesis, keeping the Aurum key and all other projects' credentials untouched per Layer 0 per-project SSH identity pattern
type: reference
generated_at: 2026-04-14
---

# Project Genesis — SSH identity

Generated 2026-04-14 during the v1 bootstrap session Étape 4a. Follows the Layer 0 per-project SSH identity pattern — dedicated key, dedicated host alias, `IdentitiesOnly yes` to prevent key ambiguity.

## Key

| Field | Value |
|---|---|
| Type | ed25519 |
| Private key | `~/.ssh/id_ed25519_genesis` |
| Public key | `~/.ssh/id_ed25519_genesis.pub` |
| Fingerprint | `SHA256:nVsRWWGwAPVM2brGFqcNgrPmao70wG37LlarShPh3cI` |
| Comment | `project-genesis@myconciergerie-prog` |
| Added to GitHub | 2026-04-14 via web UI paste-back — Settings → SSH and GPG keys |
| GitHub key title | `project-genesis (myconciergerie-prog dev)` |

## SSH config entry

Added to `~/.ssh/config` on 2026-04-14, additive next to the existing `github.com-aurum` alias:

```
Host github.com-genesis
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_ed25519_genesis
  IdentitiesOnly yes
```

**`IdentitiesOnly yes` is critical** — it prevents ssh-agent from offering another key first (e.g. the Aurum key, which would authenticate to the wrong repo context). Without this flag, SSH would try all loaded identities in order and potentially succeed with the wrong one.

## Git remote URL

```
git@github.com-genesis:myconciergerie-prog/project-genesis.git
```

Note: the host is `github.com-genesis` (the alias), **not** `github.com`. The alias resolves via `~/.ssh/config` to real `github.com` with the Genesis-specific identity. This binding is what gives each project its own identity.

## Pre-flight test (passed on 2026-04-14)

```bash
ssh -T -o StrictHostKeyChecking=accept-new git@github.com-genesis
```

Expected output (which was returned successfully):

```
Hi myconciergerie-prog! You've successfully authenticated, but GitHub does not provide shell access.
```

This confirms the key binds to the correct GitHub identity. Exit code 1 is normal — GitHub doesn't provide shell access, so the connection closes after auth success.

## How to apply

- **All Genesis git operations** (clone, push, pull, fetch) use this SSH alias. Never HTTPS with embedded PAT for this repo.
- **Worktree creation** (R2.1): after `git clone . .claude/worktrees/<type>_YYYY-MM-DD_<theme>`, the clone inherits the parent's remote URL (which points to local disk). Immediately update:

  ```bash
  git remote set-url origin git@github.com-genesis:myconciergerie-prog/project-genesis.git
  ```

- **Moving the repo to a new machine**: copy both `~/.ssh/id_ed25519_genesis` and `~/.ssh/id_ed25519_genesis.pub` to the new machine's `~/.ssh/` directory, then re-add the `~/.ssh/config` `Host github.com-genesis` block. On Windows git-bash, permissions don't need to be tightened to 600 (SSH honors NTFS ACLs); on macOS/Linux, `chmod 600 ~/.ssh/id_ed25519_genesis` is required.

## Rotation

If the key is ever compromised or needs rotation:

1. Generate a new ed25519 key with the same comment:

   ```bash
   ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519_genesis_new -C "project-genesis@myconciergerie-prog" -N ""
   ```

2. Add the new public key to GitHub via web UI paste-back (title: `project-genesis (myconciergerie-prog dev) — rotated YYYY-MM-DD`)
3. Test authentication with the new key via `ssh -T -o IdentityFile=~/.ssh/id_ed25519_genesis_new git@github.com-genesis`
4. Replace old files: `mv ~/.ssh/id_ed25519_genesis_new ~/.ssh/id_ed25519_genesis && mv ~/.ssh/id_ed25519_genesis_new.pub ~/.ssh/id_ed25519_genesis.pub`
5. Delete the old public key from GitHub web UI
6. Update this memory file's `Fingerprint` field with the new SHA256

The host alias `github.com-genesis` stays the same through rotation — only the underlying `IdentityFile` pointed to by the alias changes.

## Related

- **Aurum SSH identity** (separate, additive, never touched): `~/.ssh/id_ed25519_aurum` / host alias `github.com-aurum`. Both keys coexist in `~/.ssh/` and `~/.ssh/config` without conflict.
- **Layer 0 pattern reference**: `~/.claude/CLAUDE.md` "Per-project SSH identity" section
