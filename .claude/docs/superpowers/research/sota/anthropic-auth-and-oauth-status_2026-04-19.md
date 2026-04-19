<!-- SPDX-License-Identifier: MIT -->
---
type: sota
topic: Anthropic OAuth / browser-redirect auth status for Messages API & SDK
created: 2026-04-19
expires_at: 2026-04-26
confidence: high
scope: universal-candidate (currently project-genesis only)
---

# Anthropic OAuth / browser-redirect auth status — April 2026

## TL;DR

**No first-party OAuth path for Messages API as of April 19, 2026.** Claude Code itself uses OAuth 2.0 against `claude.ai` (`sk-ant-oat01-*` long-lived tokens), but those tokens are **explicitly rejected** by the Messages API ("OAuth authentication is currently not supported"). **Claude Max ($200/mo) does NOT grant API quota** — Pro/Max covers `claude.ai` + Claude Desktop + Claude Code CLI inference only; Messages API / Files / Citations require a separate workspace `ANTHROPIC_API_KEY` from the Console. The April 4, 2026 **"OpenClaw ban"** killed every gray-zone bridge (Cline / Cursor / Windsurf / OpenClaw routed Messages API through subscription OAuth → blocked via client fingerprinting). For Claude Code plugins requiring SDK access, the only ToS-clean path is requiring users to provision an API key.

## Confirmed findings

### 1. OAuth endpoints exist for Claude Code, NOT for Messages API

- Claude Code first-launch is browser OAuth against `claude.ai` (Authorization Code with PKCE).
- `claude setup-token` mints a `CLAUDE_CODE_OAUTH_TOKEN` (~1 year TTL).
- These tokens are scoped **for Claude Code inference only**.
- **No public `authorize` / `token` / `refresh` endpoints exposed for third-party app registration.**
- **No documented scopes** (`messages:write`, etc.).
- Issue [anthropics/claude-code#37205](https://github.com/anthropics/claude-code/issues/37205) ("Allow OAuth tokens for Messages API") is currently labeled `invalid` + `stale`.

### 2. Claude Max → API bridge is dead

- Confirmed by Anthropic ToS, Help Center, and post-OpenClaw enforcement (April 4, 2026).
- **Subscription ≠ API access by Anthropic's intentional architecture.** Two separate billing surfaces, two separate identities (subscription account vs Console workspace).
- Bridges that worked pre-April-4 (Cline, Cursor, Windsurf, OpenClaw, original Meridian) routed Messages API calls through subscription OAuth — now blocked by Anthropic's **client fingerprinting** on OAuth token usage.
- Meridian v1.37.5 (April 18, 2026) survived only by routing through the **Claude Agent SDK** (which inherits parent Claude Code subscription auth for inference), NOT for arbitrary Messages API access from external code.

### 3. Subprocess inheritance is a dead end

- Default behaviour: child processes spawned by Claude Code inherit parent env (including `ANTHROPIC_API_KEY` if set).
- **Hardening default trend**: `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB=1` strips Anthropic + cloud-provider credentials from subprocess env. Recommended-on increasingly.
- Even without scrubbing: the OAuth token in `~/.claude/.credentials.json` is **rejected by Messages API by design** (per finding #1) — inheriting it gives nothing.
- Claude Code 2.1.83 plugin credential keychain stores plugin-specific user-supplied secrets; **does not expose Anthropic creds to plugins**.

### 4. SDK helpers absent

- `anthropic` Python SDK ≥ 0.40 + `@anthropic-ai/sdk` npm: **no `login()` / `device_flow()` / `link_account()` helper**. Auth is `apiKey: process.env.ANTHROPIC_API_KEY` only (plus Bedrock / Vertex / Azure auth wrappers).
- No first-party community package wraps a sanctioned browser flow.
- Unsanctioned wrappers (`grll/claude-code-login`, `griffinmartin/opencode-claude-auth`, `ex-machina-co/opencode-anthropic-auth`) all rely on subscription OAuth → **post-April-4 broken or ToS-risky**.

### 5. Comparable implementations all require API key

- **Vercel AI SDK / Mastra / LangChain / LlamaIndex**: pass-through `ANTHROPIC_API_KEY`. None offer Anthropic browser auth.
- **Cursor / Continue / Aider / Cline**: post-April-4 require Console API keys for Anthropic models.
- **Google Antigravity**: Google's IDE, authenticates via Google OAuth, provides Claude through Google's billing — not via Anthropic auth at all.

### 6. Plugin feasibility — even hypothetically

Even if Anthropic shipped third-party OAuth tomorrow, Layer 0 "no new windows" hard rule on this machine means a Claude Code plugin would need either:
- **Paste-back URL** (print authorize URL → user opens in already-running Chrome → pastes code back), or
- **Device flow** (display short code → user enters at `anthropic.com/device`).

Neither pattern exists today. Inheriting Claude Code's session is off-table per finding #3.

## Implementation impact — project-genesis v1.5.0

| Option | Feasibility April 2026 | Verdict |
|---|---|---|
| (a) Status quo + halt-with-remediation card | **Fully feasible.** Matches every other tool in the ecosystem post-OpenClaw. | **Ship this.** |
| (b) Browser-redirect via Anthropic OAuth | **Not feasible.** No public OAuth endpoints for Messages API. Building on subscription OAuth = ToS violation + user account ban risk. | **Reject.** |
| (c) Inherit Claude Code's session | **Not feasible.** Token type rejected by Messages API by design; subprocess scrub trend; no plugin API surface. | **Reject.** |

## Halt-with-remediation card content — five upgrade priorities (vs initial v1.5.0 spec)

The v1.5.0 spec § In scope item 7 names 4 elements: bilingual title, remediation text (set env var + relaunch), Console link, Max ≠ API note. Research adds 5 substantive content upgrades:

1. **Explain *why* (subscription ≠ API)** — one short paragraph, not just "note clarifying". Subscription pays for `claude.ai` + Claude Desktop + Claude Code CLI inference; API key is a separate Console product, billed per-token to a workspace. The two are intentionally distinct identities and billing paths.
2. **Console deep-link with role pre-selected** — link to `https://console.anthropic.com/settings/keys` with `Claude Code` (or "Developer") role pre-selected if URL params support it. Failing that, instruct: "Click 'Create Key' → name it 'genesis-drop-zone' → role 'Claude Code' → copy the `sk-ant-...` value".
3. **Exact OS-specific one-liners** — Windows `setx ANTHROPIC_API_KEY "<key>"` (system-wide, persists across shells); POSIX `export ANTHROPIC_API_KEY="<key>"` (current shell, plus add to `.zshenv` / `.bashrc` for persistence). Show both.
4. **Escape hatches mention** — `ANTHROPIC_AUTH_TOKEN` for LLM gateway / proxy stacks; `apiKeyHelper` config setting for rotating-secret deployments. One-liner mention; defer details to Anthropic docs.
5. **`CLAUDE_CODE_SUBPROCESS_ENV_SCRUB` warning** — the env var must be set **system-wide** (`setx` on Windows; `.zshenv` on POSIX), not just inside the Claude Code session. Otherwise a future Claude Code release that defaults `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB=1` would scrub the var when spawning the extractor subprocess. Future-proofing today.

## Risk flags (re-verify before tagging v1.5.0)

1. **Cache TTL ≈ days, not weeks** — OpenClaw ban was April 4; another enforcement wave plausible. Re-verify [`code.claude.com/docs/en/authentication`](https://code.claude.com/docs/en/authentication) precedence list before tag.
2. **Console role naming**: "Claude Code role" vs "Developer role" recently distinguished — confirm Console UI labels haven't shifted.
3. **`CLAUDE_CODE_SUBPROCESS_ENV_SCRUB`** may flip to default-on in a future release — document the requirement to set var **system-wide**, not just session.
4. **`--bare` mode** does not read `CLAUDE_CODE_OAUTH_TOKEN` — relevant if plugin ever shells out with `--bare`. Use `ANTHROPIC_API_KEY` or `apiKeyHelper`.

## Sources cited

- [Claude Code Authentication docs (official)](https://code.claude.com/docs/en/authentication)
- [Issue #37205 — Allow OAuth tokens for Messages API](https://github.com/anthropics/claude-code/issues/37205)
- [Agent SDK overview (official)](https://platform.claude.com/docs/en/agent-sdk/overview)
- [Plugins in the SDK (official)](https://platform.claude.com/docs/en/agent-sdk/plugins)
- [The Missing Piece in Anthropic's Ecosystem: Third-Party OAuth — Medium, March 2026](https://medium.com/@em.mcconnell/the-missing-piece-in-anthropics-ecosystem-third-party-oauth-ccb5addb8810)
- [What Is the OpenClaw Ban — MindStudio, April 2026](https://www.mindstudio.ai/blog/anthropic-openclaw-ban-oauth-authentication)
- [Meridian (rynfar) — Claude Max bridge via Agent SDK, MIT](https://github.com/rynfar/meridian)
- [Claude Code plugin credentials keychain analysis — dev.to](https://dev.to/rsdouglas/claude-code-plugin-credentials-what-the-new-keychain-storage-does-and-doesnt-do-cnf)
- [Using Claude Code with your Pro or Max plan — Anthropic Help Center](https://support.claude.com/en/articles/11145838-using-claude-code-with-your-pro-or-max-plan)
- [OpenClaw + Claude Code Costs 2026 — shareuhack](https://www.shareuhack.com/en/posts/openclaw-claude-code-oauth-cost)
- [Claude API Authentication in 2026 — Lalatendu Swain, March 2026](https://lalatenduswain.medium.com/claude-api-authentication-in-2026-oauth-tokens-vs-api-keys-explained-12e8298bed3d)

## Cross-project candidacy

This research has **universal scope** — every project on this machine that uses Anthropic Messages API (Aurum.ai, Cyrano, Myconciergerie ride/www, Genesis, future projects) is affected by the same architectural reality. After v1.5.0 ships, candidate for promotion to `~/.claude/docs/superpowers/research/sota/` (Layer 0 universal R8 cache) per cross-project sharing convention. Project-genesis remains the canonical caller in the v1.5.x cycle but the finding is not project-specific.
