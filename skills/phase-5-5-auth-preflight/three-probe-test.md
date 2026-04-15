<!-- SPDX-License-Identifier: MIT -->
---
name: Phase 5.5.4 three-probe pre-flight test
description: Canonical three-probe Phase 5.5 exit gate — SSH handshake against the per-project alias, GH_TOKEN gh api user, GH_TOKEN gh api repos/owner/repo — standalone so Phase 5, R1.1 session-open health checks, and downstream skills can reuse it
type: template
stage: 5.5.4
---

# Phase 5.5.4 — Three-probe pre-flight test

Three probes, three exit codes, one gate. If any probe fails, the skill does **not** advance to Phase 5; it surfaces a targeted recovery for the failing probe and re-runs `three-probe-test.md` from the top after recovery.

Why a standalone file: Phase 5 reads these probes as its entry condition, R1.1 session-open checks may re-run them on any future session, and other skills (future `phase-0-kickoff`, future `session-post-processor`) may reuse the probe definitions. Keeping them in one file means one source of truth — `v1_phase_5_5_auth_preflight_learnings.md` Learning 3.

## Template variables

- `{{PROJECT_SLUG}}` — from the consent card
- `{{GITHUB_OWNER}}` — from the consent card
- `{{REPO}}` — from the consent card
- `{{HOST_ALIAS}}` — `github.com-{{PROJECT_SLUG}}`

## Probe 1 — SSH handshake

Command:

```bash
ssh -T -o StrictHostKeyChecking=accept-new git@{{HOST_ALIAS}}
```

Expected: stdout / stderr contains the literal substring `Hi {{GITHUB_OWNER}}! You've successfully authenticated`. Exit code is `1` (non-zero) — GitHub never grants shell access, so SSH closes the connection after auth. Exit code 1 with the correct greeting is **success**.

### Failure modes

| Symptom | Diagnosis | Recovery |
|---|---|---|
| `Permission denied (publickey)` | Public key not added to GitHub, or added to the wrong account | Re-open `https://github.com/settings/ssh/new`, paste the key from `ssh-keygen.md` Step 4 |
| `Hi someone-else!` | Key is bound to a different GitHub user | Remove the key from the other account, re-add it to `{{GITHUB_OWNER}}` |
| `Host key verification failed` | `~/.ssh/known_hosts` has a stale entry | `ssh-keygen -R github.com` then re-run the probe |
| `Could not resolve hostname github.com-{{PROJECT_SLUG}}` | `~/.ssh/config` alias not written | Re-run `ssh-keygen.md` Step 3 |
| `IdentityFile ~/.ssh/id_ed25519_{{PROJECT_SLUG}} does not exist` | Key file missing | Re-run `ssh-keygen.md` Step 2 |

After recovery, re-run **only Probe 1**. Do not re-run Probes 2 and 3 until Probe 1 is green.

## Probe 2 — PAT user identity

Command:

```bash
GH_TOKEN="$(grep '^GH_TOKEN=' .env.local | cut -d= -f2-)" gh api user --jq .login
```

Expected: exit code 0, stdout is the single line `{{GITHUB_OWNER}}`.

### Failure modes

| Symptom | Diagnosis | Recovery |
|---|---|---|
| `HTTP 401 Bad credentials` | Token mis-copied, truncated, or expired | Re-create the PAT per `pat-walkthrough.md` (GitHub never re-displays a token) |
| Output is a different login | PAT was created under the wrong Resource owner | Re-create the PAT and pick `{{GITHUB_OWNER}}` in the Resource owner dropdown |
| `gh: command not found` | `gh` CLI not installed | Surface `/phase-minus-one` to install it and exit |
| `HTTP 403 Resource not accessible by integration` | PAT lacks Metadata: Read | Re-create the PAT with the full canonical scope list |
| `.env.local: No such file or directory` | PAT was not persisted | Re-run `pat-walkthrough.md` Step 4 |

After recovery, re-run **only Probe 2**. Do not advance to Probe 3 until Probe 2 is green.

## Probe 3 — Repo existence and permissions

Command:

```bash
GH_TOKEN="$(grep '^GH_TOKEN=' .env.local | cut -d= -f2-)" gh api repos/{{GITHUB_OWNER}}/{{REPO}} --jq '[.full_name, .default_branch, .private, .permissions.admin] | @tsv'
```

Expected: exit code 0, stdout is a single TSV line like:

```
{{GITHUB_OWNER}}/{{REPO}}	main	true	true
```

(The last two fields are `.private` and `.permissions.admin`. Both should be `true` for a freshly-created private repo owned by the PAT's user.)

### Failure modes

| Symptom | Diagnosis | Recovery |
|---|---|---|
| `HTTP 404 Not Found` | Repo does not exist OR PAT lacks repo-level Contents: Read | Verify repo via Step 3 of `empty-repo-create.md`; if repo exists, re-create PAT with canonical scopes |
| `HTTP 403 Resource not accessible by personal access token` | PAT scope gap, usually missing Administration: Read | Re-create PAT with full canonical scope list |
| `.permissions.admin = false` | Repo owned by another user/org and PAT-user only has read | Stop — consent card owner is wrong, start over with the correct owner |
| `.default_branch` is not `main` | Repo was created with a non-main default | Non-blocking if the user accepts; otherwise change via Settings → Branches |

After recovery, re-run **only Probe 3**.

## Full-pass helper (three-in-one)

Once each probe passes individually during development, the skill can run all three in sequence from a single command — useful for R1.1 session-open re-verification on a warm project:

```bash
set -e
ssh -T -o StrictHostKeyChecking=accept-new git@{{HOST_ALIAS}} 2>&1 | grep -q "Hi {{GITHUB_OWNER}}!" && echo "SSH=ok" || { echo "SSH=fail"; exit 1; }
GH_TOKEN_VAL="$(grep '^GH_TOKEN=' .env.local | cut -d= -f2-)"
GH_TOKEN="$GH_TOKEN_VAL" gh api user --jq .login | grep -q "^{{GITHUB_OWNER}}$" && echo "PAT=ok" || { echo "PAT=fail"; exit 2; }
GH_TOKEN="$GH_TOKEN_VAL" gh api "repos/{{GITHUB_OWNER}}/{{REPO}}" --jq .full_name | grep -q "^{{GITHUB_OWNER}}/{{REPO}}$" && echo "REPO=ok" || { echo "REPO=fail"; exit 3; }
echo "ALL=ok"
```

Exit codes: `1` = SSH failure, `2` = PAT failure, `3` = repo failure, `0` = all green. R1.1 can grep `ALL=ok` to decide whether the warm-session auth state is healthy.

## Exit condition

- All three probes return their expected output.
- Full-pass helper prints `ALL=ok` with exit code 0.
- Control passes to `verification.md` for Step 5.5.5.

## Anti-Frankenstein

- Do not treat a partial green as "good enough". All three probes must be green, in order.
- Do not advance to Phase 5 if any probe is red, even if the user asks. The gate exists precisely to catch silent-failure state.
- Do not try to "fix the root cause" by editing `~/.ssh/config` or `.env.local` by hand outside the recovery templates — every recovery points to a specific earlier step of this skill so the state stays auditable.
- Do not skip Probe 3's `.permissions.admin` check. The whole point of the Administration scope is to surface write-capability early, not at the first failing PATCH later.
