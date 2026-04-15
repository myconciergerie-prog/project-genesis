<!-- SPDX-License-Identifier: MIT -->
---
name: Phase 5.5.1 SSH keygen walkthrough
description: Generate a dedicated ed25519 SSH key for the project, add an IdentitiesOnly host alias to ~/.ssh/config, register the public key with GitHub via paste-back, and confirm the binding with ssh -T — per Layer 0 per-project SSH identity pattern
type: template
stage: 5.5.1
---

# Phase 5.5.1 — SSH keygen

One dedicated ed25519 key per project. One host alias per project. `IdentitiesOnly yes` on every alias. Never reuse an existing key for a new project — it leaks credentials across blast radii and violates additive auth.

## Template variables

- `{{PROJECT_SLUG}}` — from the consent card
- `{{GITHUB_OWNER}}` — from the consent card
- `{{KEY_PATH}}` — `~/.ssh/id_ed25519_{{PROJECT_SLUG}}`
- `{{HOST_ALIAS}}` — `github.com-{{PROJECT_SLUG}}`

## Step 1 — Pre-check the key does not already exist

Never silently overwrite an existing key. Run:

```bash
test -f ~/.ssh/id_ed25519_{{PROJECT_SLUG}} && echo "EXISTS" || echo "OK"
```

If the output is `EXISTS`, **stop**. Surface a two-option recovery card:

- Use the existing key as-is (skip to Step 3 with the current public key).
- Pick a different key name and re-run the consent card with the new slug.

Never overwrite without explicit confirmation.

## Step 2 — Generate the key

```bash
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519_{{PROJECT_SLUG}} -C "{{PROJECT_SLUG}}@{{GITHUB_OWNER}}" -N ""
```

Notes on the flags:

- `-t ed25519` — modern curve, small key, fast.
- `-f` — explicit path; never rely on the interactive prompt.
- `-C` — comment is `<slug>@<owner>`, shown in GitHub's key list later. Never store the user's real email here.
- `-N ""` — empty passphrase. Project keys are machine-local and covered by OS disk encryption; requiring a passphrase every push would break the non-interactive flows the skill depends on. If the user asks for a passphrase, they must also configure an ssh-agent on their own — document it but don't force it.

After this command runs, the user should see two files:

- `~/.ssh/id_ed25519_{{PROJECT_SLUG}}` — private key (NEVER print this)
- `~/.ssh/id_ed25519_{{PROJECT_SLUG}}.pub` — public key (safe to print)

Print the fingerprint so the user can cross-reference it later:

```bash
ssh-keygen -lf ~/.ssh/id_ed25519_{{PROJECT_SLUG}}.pub
```

Record the SHA256 fingerprint in the draft `memory/reference/ssh_{{PROJECT_SLUG}}_identity.md`.

## Step 3 — Append the host alias to `~/.ssh/config`

Idempotent append. First check the alias does not already exist:

```bash
grep -q "^Host {{HOST_ALIAS}}$" ~/.ssh/config 2>/dev/null && echo "EXISTS" || echo "OK"
```

If `OK`, append the block below. If `EXISTS`, leave the file alone and verify it points to the right `IdentityFile` — offer a one-line recovery if it doesn't.

Block to append (note the leading blank line — it separates this block from anything already in the file):

```
Host {{HOST_ALIAS}}
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_ed25519_{{PROJECT_SLUG}}
  IdentitiesOnly yes
```

**`IdentitiesOnly yes` is non-negotiable.** Without it, ssh-agent will offer every loaded identity in order and potentially authenticate as the wrong account. The whole point of per-project keys is lost if this flag is missing.

Safe append command:

```bash
mkdir -p ~/.ssh && chmod 700 ~/.ssh
cat >> ~/.ssh/config <<'EOF'

Host {{HOST_ALIAS}}
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_ed25519_{{PROJECT_SLUG}}
  IdentitiesOnly yes
EOF
chmod 600 ~/.ssh/config
```

On Windows git-bash, `chmod 600` is a no-op but harmless — NTFS ACLs already protect `~/.ssh/`.

## Step 4 — Print the public key for paste-back

The user needs to paste this into GitHub's web UI (`Settings → SSH and GPG keys → New SSH key`). Print it in an **isolated fenced code block** per the v1 copy-paste rule:

```bash
cat ~/.ssh/id_ed25519_{{PROJECT_SLUG}}.pub
```

Present the output exactly like this (the backticks are literal — the user copies everything between them):

**Public key to paste** *(paste exactly the content of the code block below, nothing else):*

````
ssh-ed25519 AAAA... {{PROJECT_SLUG}}@{{GITHUB_OWNER}}
````

**Title to paste into GitHub's "Title" field** *(paste exactly the content of the code block below, nothing else):*

```
{{PROJECT_SLUG}} ({{GITHUB_OWNER}} dev)
```

**URL to open** *(paste exactly the content of the code block below, nothing else):*

```
https://github.com/settings/ssh/new
```

The user opens the URL in their chosen Chrome profile (from consent card), pastes the title and the key, clicks `Add SSH key`, and reports back `done` or `added`.

## Step 5 — Confirm the binding

After the user reports the key is added:

```bash
ssh -T -o StrictHostKeyChecking=accept-new git@{{HOST_ALIAS}}
```

Expected output (exit code 1 is normal — GitHub doesn't provide shell access, so the connection closes after auth success):

```
Hi {{GITHUB_OWNER}}! You've successfully authenticated, but GitHub does not provide shell access.
```

If the name after `Hi` is anything other than `{{GITHUB_OWNER}}`, **stop**. The key authenticated as the wrong account — usually because the user is signed into a different GitHub identity in Chrome or the key was added to the wrong account. Surface a recovery card:

- Remove the key from whichever account it was added to.
- Verify Chrome profile matches the target owner.
- Re-run Step 4.

If the output contains `Permission denied`, the key was not added or not found. Recovery: re-open the URL and re-paste.

Only on a clean `Hi {{GITHUB_OWNER}}!` output does Step 5.5.1 count as complete.

## Exit condition

- Dedicated key exists at `~/.ssh/id_ed25519_{{PROJECT_SLUG}}` with non-null fingerprint.
- Host alias `{{HOST_ALIAS}}` appears in `~/.ssh/config` with `IdentitiesOnly yes`.
- Public key is registered to the expected GitHub account.
- `ssh -T git@{{HOST_ALIAS}}` reports the expected `{{GITHUB_OWNER}}` identity.
- Control passes to `pat-walkthrough.md` for Step 5.5.2.

## Anti-Frankenstein

- Do not reuse an existing key for a new project, even if it's "close enough".
- Do not skip `IdentitiesOnly yes`.
- Do not print the private key — ever — under any mode.
- Do not try to add the public key via API — the scope required (`Administration user:write`) is rarely present on fine-grained PATs and silently mis-binds to the wrong account if the token is from a different user.
