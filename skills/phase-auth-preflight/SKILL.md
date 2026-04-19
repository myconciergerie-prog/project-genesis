---
name: phase-auth-preflight
description: 'Pre-flight check for Anthropic auth via Claude Code Max subscription. Runs `claude auth status` JSON probe ; passes silently if loggedIn ; otherwise prints bilingual remediation card instructing `claude auth login` and halts. Invoked as Phase 0.0 by `/genesis-drop-zone` (Layer A) and as first step of Phase 0 by `/genesis-protocol` (Layer B). v2.0.0 introduces this skill ; replaces v1.5.0 halt-with-remediation card after v1.4.0 subprocess Citations path is dropped. Internal function signature `check_provider_auth(provider="anthropic")` is BYOAI-ready for v3.x without skill restructure.'
---

# Phase Auth Pre-flight

## Purpose

Genesis bootstrapping requires Anthropic-backed inference (Claude). v2 leverages the Max subscription that Claude Code already holds at session open via `claude auth login` — no separate `ANTHROPIC_API_KEY` / Console workspace / subprocess Messages API call. This skill verifies that auth is actually present BEFORE any phase that depends on it (Layer A `genesis-drop-zone` Phase 0 ; Layer B `genesis-protocol` Phase 0). Idempotent ; ~10s when authed ; one-turn remediation when not.

Internal function signature is `check_provider_auth(provider="anthropic")` — BYOAI-ready for v3.x without restructure (see `memory/master.md § "What v3 vision is"` for the staging plan).

## Decision tree

Run `claude auth status` (no flags — output is JSON by default in v2.1.x). Parse the JSON output and route per the table below :

| Condition | Action | User-visible output |
|---|---|---|
| `loggedIn=true` AND `apiProvider=firstParty` | Pass — return control to caller | One-line confirmation : `✓ Auth Anthropic OK (<email>, <subscriptionType>)` |
| `loggedIn=true` AND `apiProvider` in `Bedrock`/`Vertex`/`Foundry` | Pass with warning note | `✓ Auth via <provider> — Genesis assumes Anthropic-backed inference is available through this provider ; if extraction quality degrades, retry with claude.ai auth` |
| `loggedIn=false` | Halt with remediation card (see § "Remediation card content" below) | Bilingual remediation card |
| `claude` binary not found in PATH | Halt with installer instruction | Bilingual install card pointing to `https://claude.ai/install.ps1` (Windows) / `curl -fsSL https://claude.ai/install.sh \| sh` (POSIX) |
| `claude auth status` returns non-JSON or non-zero exit | Halt with diagnostic | Print stderr verbatim, instruct user to run `claude auth login` to recover |

## Remediation card content

For the `loggedIn=false` path (most common Victor case) :

````
╭─────────────────────────────────────────────────────────────╮
│  Genesis a besoin de l'auth Claude Code  ·  Genesis needs   │
│  Claude Code auth                                           │
╰─────────────────────────────────────────────────────────────╯

Genesis tourne dans Claude Code, qui s'authentifie à Anthropic
via ton abonnement Claude.ai (Pro / Max / Team). Une seule
commande, puis relance ce bootstrap.

Genesis runs inside Claude Code which authenticates to Anthropic
via your Claude.ai subscription (Pro / Max / Team). Run the
command below once, then re-launch this bootstrap.

   claude auth login

Une fenêtre browser s'ouvrira sur claude.ai. Connecte-toi (ou
accepte l'OAuth si déjà connecté). Reviens ici, relance.

A browser window will open at claude.ai. Sign in (or accept the
OAuth prompt if already signed in). Return to this terminal.
Re-run this bootstrap.

Note multi-org : si ton compte appartient à plusieurs
organisations, choisis celle que tu veux pour ce projet.

Multi-org note : if your account belongs to multiple organizations,
choose the one you want this project billed against.
````

No `--console` mention. v2 deliberately does NOT suggest the Console API path because subprocess Messages API access still requires a separately-generated `sk-ant-api*` key (per R8 `anthropic-auth-and-oauth-status_2026-04-19.md`) — the bootstrap doesn't need that anymore.

## Test scenarios

Five fixtures cover the full decision-tree :

| Fixture | Scenario | Expected behaviour |
|---|---|---|
| `tests/fixtures/auth_status_authed_firstparty.json` | Real authed Max subscription | Pass + print `✓ Auth Anthropic OK` line |
| `tests/fixtures/auth_status_authed_bedrock.json` | Authed via Bedrock | Pass with warning note |
| `tests/fixtures/auth_status_loggedin_false.json` | Logged out | Halt with remediation card (`claude auth login` instruction) |
| `tests/fixtures/auth_status_corrupt.json` | Malformed JSON output | Halt with diagnostic, print stderr verbatim |
| (no fixture — manual) | `claude` binary missing from PATH | Halt with install card |

Only the authed-firstparty case is auto-testable on dev machine via `claude -p` (real `claude auth status` returns this state). Other scenarios require disrupting auth state to test live ; documented in `tests/runtime_evidence_v2_0_0.md` as manual-verification-required.

<!-- SPDX-License-Identifier: MIT -->
