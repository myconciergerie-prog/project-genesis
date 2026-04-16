# Genesis v1.0.0 Self-Dogfood — Friction Log

**Date**: 2026-04-16
**Target**: genesis-selfdogfood/ (Genesis bootstrapping itself)
**Mode**: auto
**Reached**: Phase 3 Step 3.4 (SSH key registration to GitHub)
**Stopped by**: auth wall — 0 of 6 manual browser steps could be automated
**Primary deliverable**: this log + VISION_v2.md (Promptor fusion)

---

## Severity scale

- **STRUCTURAL** — protocol design flaw, blocks the Victor test
- **DESIGN** — protocol describes something that doesn't work as written
- **COSMETIC** — awkward but not blocking

---

## The frictions

### F1 — Phase -1 skip check is chronologically impossible [DESIGN]

**Phase**: -1 (skip check)
**What**: Protocol says "check if `memory/reference/automation-stack.md` exists in the target project." But the target folder doesn't exist yet at Phase -1 — it's created at Phase 0.
**Root cause**: Protocol assumes the target folder pre-exists. In practice, the orchestrator creates it.
**Fix**: Phase -1 skip check should probe the HOST machine's stack (which it does), not look for a file in a folder that doesn't exist yet. Decouple the skip-check from the target folder.

### F2 — No auto-mode for consent gates beyond Phase -1 [DESIGN]

**Phase**: 0 (intent card)
**What**: Phase -1 has 3 modes (detailed/semi-auto/auto). Phases 0-7 have no mode concept — every consent gate interrupts even when the user said "mode auto."
**Root cause**: The 3-mode ladder was designed for Phase -1 only. The orchestrator inherited the consent gates from its skills but not the mode system.
**Fix**: Extend the mode ladder to the full protocol. In auto mode, consent gates become confirmation logs (shown but not blocking) unless they're TRUE security floor items.

### F3 — Phase 0 creates memory/project/ before Phase 1 scaffolds memory/ [COSMETIC]

**Phase**: 0 → 1
**What**: Phase 0 writes `memory/project/bootstrap_intent.md` but the full `memory/` scaffold is Phase 1's job. Implicit coupling.
**Root cause**: `bootstrap_intent.md` needs to be persisted before Phase 1, but Phase 1 owns the directory structure.
**Fix**: Document this as intentional. Phase 1 Step 1.2 idempotency handles it correctly. Not a real problem, just surprising.

### F4 — CLAUDE.md template encoding not specified [COSMETIC]

**Phase**: 1 (Step 1.4)
**What**: Template uses Unicode arrows (←). Works in UTF-8 but encoding is never specified.
**Fix**: Add "all files UTF-8" to the protocol conventions. Trivial.

### F5 — Install-manifests are YAML templates interpreted by a Markdown orchestrator [DESIGN]

**Phase**: 1 (Step 1.5)
**What**: Sibling skills define their install targets in YAML `install-manifest.yaml` with `template: |` blocks. The orchestrator (Option A pure Markdown) has no YAML parser — it "interprets" the YAML by reading it and manually writing the files. If the template in YAML drifts from what the orchestrator writes, the 1:1 mirror is silently broken.
**Root cause**: Option A (pure Markdown) was chosen over Option B (Python driver). The YAML manifests were designed for a machine parser that doesn't exist yet.
**Fix**: Either (a) add a simple YAML parser at v1.1 (Python one-liner), or (b) convert install-manifests to Markdown templates that the orchestrator can copy verbatim. Option (b) is more anti-Frankenstein.

### F6 — R8 copy list in Phase 2 is static, cache state is dynamic [DESIGN]

**Phase**: 2 (Step 2.3)
**What**: Runbook lists 5 specific entries to copy by name. In reality, the cache has evolved — entries moved to archive, were refreshed, have different filenames. The static list doesn't match the dynamic state.
**Root cause**: The runbook was written at v0.8.0 against the cache state of that moment. The cache evolved through v0.9.0 and v1.0.0.
**Fix**: Replace the static 5-entry list with a dynamic query: "copy all non-expired entries from sota/ and stack/ that match the Claude Code / plugin / SPDX / ecosystem topics." The orchestrator already reads the cache — let it filter.

### F7 — Copied R8 entries are expired on arrival [DESIGN]

**Phase**: 2 (Step 2.3)
**What**: 2 of 5 entries have TTL 1 day (stack/) and were 1-2 days old at copy time. Protocol says "do not copy stale entries" but also says "copy these 5 entries." Contradiction.
**Root cause**: TTL policy (stack/ = 1 day) is too aggressive for entries that are structural references, not volatile snapshots.
**Fix**: Either (a) reclassify structural stack entries as sota/ (TTL 7 days), or (b) add a "reference" TTL category (no expiry, manual refresh). Plugin structure and JSONL format don't change daily.

### F8 — git init CWD assumption [DESIGN]

**Phase**: 3 (Step 3.1)
**What**: Protocol says "run `git init` inside the target folder" and assumes the Claude Code session CWD IS the target folder. In self-dogfood, the session was opened in the parent directory.
**Root cause**: Protocol assumes Claude Code is opened IN the target folder. The orchestrator runs FROM the Genesis repo, targeting a different folder.
**Fix**: Every git command must use `git -C <target_folder>`. This was in the Phase 6 runbook but not in Phase 3.

### F9 — `gh ssh-key add` not in the protocol; PAT missing SSH scope [STRUCTURAL]

**Phase**: 3 (Step 3.4)
**What**: `gh ssh-key add` would eliminate the browser step entirely, but (a) the command is never mentioned in the protocol, and (b) the PAT scope checklist omits "Git SSH keys (write)."
**Root cause**: Protocol was designed around browser paste-back as the primary path. CLI alternatives were not researched.
**Fix**: Add "Git SSH keys (write)" to the PAT scope checklist. Add `gh ssh-key add` as the PRIMARY path, browser as fallback.

### F10 — PAT fine-grained lacks SSH key management scope [STRUCTURAL]

**Phase**: 3/5.5
**What**: The canonical PAT scope checklist (Contents, Metadata, PRs, Workflows, Administration) does not include SSH key management. `gh ssh-key add` returns HTTP 403.
**Root cause**: The scope checklist was derived from Aurum v0_init learnings which focused on repo operations, not key management.
**Fix**: Add "Git SSH keys: Read and write" to the canonical scope list. This is one checkbox in the PAT creation form — trivial for the user, eliminates an entire browser step.

### F11 — Playwright MCP cannot access existing browser sessions [STRUCTURAL]

**Phase**: 3 (Step 3.4)
**What**: Playwright MCP opens its own Chromium instance with no cookies, no sessions, no access to the user's logged-in GitHub. The `playwright-automation.md` file assumes Playwright can drive GitHub forms — it can't without a login flow first.
**Root cause**: Playwright MCP is designed for testing/scraping, not for reusing existing user sessions. It would need `--user-data-dir` or `connect-over-cdp` to access an existing Chrome profile.
**Fix v1.1**: Document this limitation honestly. Playwright automation of authenticated GitHub forms requires a full login flow inside Playwright first (security floor: password + 2FA).
**Fix v2**: Eliminate the need for browser automation entirely by using CLI (`gh`) for all GitHub operations.

### F12 — Best automation path (Chrome profile + clipboard) undocumented [DESIGN]

**Phase**: 3 (Step 3.4)
**What**: The path that actually works best on this machine — `Start-Process chrome.exe --profile-directory="Profile 2"` + `clip.exe` — is not documented in the protocol. It comes from Layer 0 knowledge (Chrome profile map) but the protocol doesn't reference it.
**Root cause**: Protocol documents three paths (paste-back, Playwright, skip-to-5.5) but not the fourth that actually works.
**Fix**: Add "Chrome profile launcher + clipboard" as the documented fallback between "CLI automation" and "generic paste-back."

### F13 — Playwright browser dies between calls [COSMETIC]

**Phase**: 3
**What**: Playwright Chromium closed non-deterministically between tool calls. No reconnection mechanism.
**Root cause**: MCP session lifecycle issue — browser process may be garbage-collected between invocations.
**Fix**: Playwright MCP should keep the browser alive for the duration of the MCP session, or reconnect transparently.

### F14 — Playwright cannot connect to existing Chrome (fundamental) [STRUCTURAL]

**Phase**: 3
**What**: Even if Playwright stays alive, it cannot connect to the user's Chrome instance. CDP requires Chrome to be launched with `--remote-debugging-port`, which can't be added to an already-running Chrome.
**Root cause**: Architecture mismatch — Playwright is a testing tool, not a user-session-reuse tool.
**Fix**: Don't rely on Playwright for authenticated operations. Use CLI tools (`gh`) that carry their own auth. Playwright is for unauthenticated flows only (public pages, scraping, testing).

### F15 — Chrome ignores --remote-debugging-port on running instance [COSMETIC]

**Phase**: 3
**What**: `chrome.exe --remote-debugging-port=9222 --profile-directory="Profile 2"` delegates to the existing Chrome process which doesn't have debugging enabled.
**Root cause**: Chrome single-instance architecture.
**Fix**: Not fixable from Genesis's side. Reinforces F14: don't rely on browser automation for auth.

### F16 — `gh auth login --web` opens OS default browser, not target profile [DESIGN]

**Phase**: 3
**What**: `gh auth login --web` opens whatever the OS default browser is, not necessarily the Chrome profile where the user is logged into the right GitHub account.
**Root cause**: `gh` uses `os.Open()` which delegates to the OS browser handler. No `--browser` flag exists.
**Fix**: Use `BROWSER` environment variable to route to the correct Chrome profile: `BROWSER="chrome.exe --profile-directory='Profile 2'"`. Research needed on whether `gh` respects this.

### F17 — SSH key registration is NOT a security floor but is treated as one [STRUCTURAL]

**Phase**: 3/5.5 (synthesis)
**What**: The protocol treats SSH key registration, PAT creation, and repo creation as "paste-back or Playwright" steps — implying they're automatable with graceful fallback. In reality, NONE of the automation paths work. These are architecture artefacts, not security floors.
**Root cause**: The dry-run walkthrough at v0.9.0 explicitly skipped all auth steps ("pure paper trace"). The automation claims were never verified.
**Fix**: Reclassify. Only password entry and 2FA are true security floors. Everything else (SSH key add, repo create, push) must be automated via CLI before the protocol can claim "auto mode."

---

## Summary by severity

| Severity | Count | Examples |
|---|---|---|
| STRUCTURAL | 5 | F9, F10, F11, F14, F17 — the auth wall |
| DESIGN | 8 | F1, F2, F5, F6, F7, F8, F12, F16 — protocol says X, reality is Y |
| COSMETIC | 4 | F3, F4, F13, F15 — awkward but not blocking |

## The meta-finding

All 5 STRUCTURAL frictions are in the same area: **GitHub authentication and key management**. The entire auth flow (Phase 3 Step 3.4 through Phase 5.5) was designed around browser interaction as the primary path, with CLI as an afterthought. The fix is to invert this: **CLI first, browser never** (for the bootstrap). The single remaining browser interaction is the OAuth authorization page — and that IS a true security floor (initial sign-in).

This is the genesis of VISION_v2.md: the Promptor fusion where Victor clicks "Authorize" once and everything else is invisible.
