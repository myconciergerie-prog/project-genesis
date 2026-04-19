<!-- SPDX-License-Identifier: MIT -->

# Runtime evidence runbook — phase-auth-preflight v2.0.0

## Purpose

Capture runtime behaviour of `phase-auth-preflight` across the 5 scenarios from § Test scenarios. Mirrors v1.6.2 `runtime_dogfood_v1_6_2.md` shape.

## Scenario 1 — Authed firstParty (LIVE TEST)

**State** : `claude auth status` returns `loggedIn=true ; apiProvider=firstParty ; subscriptionType=max` (real dev machine state at v2.0.0 ship time).

Command :
```bash
cd C:/tmp
claude -p --plugin-dir <worktree> --output-format json "Run /phase-auth-preflight and report what it does."
```

Expected : output contains `✓ Auth Anthropic OK` line. No halt card. No remediation prompt.

## Scenario 2 — Authed Bedrock (DOC-ONLY)

**State** : `claude auth status` returns `loggedIn=true ; apiProvider=Bedrock`. Cannot reproduce on dev machine without Bedrock credentials.

Expected : output contains `✓ Auth via Bedrock` line + warning note about possible quality degradation.

## Scenario 3 — Logged out (DOC-ONLY, destructive to reproduce)

**State** : `claude auth status` returns `loggedIn=false`. Reproducing requires `claude auth logout` which disrupts dev session — defer to v3.0 test harness.

Expected : full bilingual remediation card per SKILL.md § Remediation card content. No proceed.

## Scenario 4 — Corrupt output (DOC-ONLY)

**State** : `claude auth status` returns malformed JSON. Cannot reproduce naturally — would require shimming the binary.

Expected : halt with diagnostic, stderr printed verbatim, `claude auth login` instruction.

## Scenario 5 — `claude` binary missing (DOC-ONLY, destructive)

**State** : `claude` not in PATH. Reproducing requires PATH manipulation — defer.

Expected : install card with OS-specific one-liner.

## v3.0 deferred

A test harness wrapper that mocks `claude auth status` output (via env var override or shim) is deferred to v3.0 when web-mode integration tests will need similar mocking.
