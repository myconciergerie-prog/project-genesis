---
name: GitHub CLI single-click auth — the 4-line revolution
description: Exact commands to reduce Genesis auth from 6 manual browser steps to 1 OAuth click using gh CLI. HTTPS-first, zero SSH at bootstrap, GH_BROWSER for profile routing.
type: sota
expires_at: 2026-04-23
researched_at: 2026-04-16
scope: universal
---

# gh CLI single-click auth — 2026-04-16

## The 4-line solution

```bash
export GH_BROWSER="chrome.exe --profile-directory=\"Profile 2\""
gh auth login --web --git-protocol https --scopes "repo,workflow,read:org"
gh auth setup-git
gh repo create "$OWNER/$REPO" --private --source=. --remote=origin --push
```

ONE user interaction (OAuth "Authorize" click). Zero SSH. Zero PAT. Zero repo UI.

## Key findings

### GH_BROWSER routes to the correct Chrome profile
`GH_BROWSER` env var controls which browser `gh auth login --web` opens.
- Windows: `chrome.exe --profile-directory="Profile 2"`
- macOS: `open -a "Google Chrome" --args --profile-directory="Profile 2"`

### HTTPS-first eliminates SSH at bootstrap
`gh auth setup-git` configures git credential helper. All `git push/pull`
operations work over HTTPS with the OAuth token. No SSH keys needed.
Per-project SSH identity becomes a v0.2.0 optimization.

### OAuth scopes in one flow
`--scopes "repo,workflow,read:org"` gets everything needed:
- `repo` — create repos, push code, manage contents
- `workflow` — push .github/workflows/ files
- `read:org` — required baseline for gh
- `admin:public_key` — only if adding SSH keys (skip for HTTPS path)

### Fine-grained PATs cannot create user repos
Confirmed limitation. OAuth via `gh auth login` bypasses this entirely.
The OAuth token can do everything a fine-grained PAT cannot.

### `gh repo create --source=. --push` does 3 things in 1 command
1. Creates the remote repo
2. Sets the origin remote
3. Pushes the local tree

### For new GitHub users
`gh auth login --web` opens the GitHub login page. "Create account" →
"Continue with Google" is the natural path. Account creation + OAuth
authorization in a single browser session.

## What this replaces in Genesis v1

| v1 step | v2 equivalent |
|---|---|
| SSH keygen | Skip (HTTPS-first) |
| Paste SSH key to GitHub | Skip |
| Create fine-grained PAT | `gh auth login --web` (OAuth) |
| Copy one-time token | Skip (gh stores token) |
| Create empty repo via web UI | `gh repo create` |
| Don't check init checkboxes | Skip (CLI has no checkboxes) |

6 steps → 0 manual steps + 1 OAuth click.
