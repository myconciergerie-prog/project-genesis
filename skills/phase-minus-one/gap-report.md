<!-- SPDX-License-Identifier: MIT -->
---
name: Phase -1.1 gap report card
description: Template rendered by the phase-minus-one skill after detect.sh runs. Shows the user a single card with current state vs target stack, grouped by layer, with per-item time cost and user-action category.
type: template
stage: -1.1
---

# Phase -1.1 — Gap report card

Rendered once, after `detect.sh` runs. One card, read top-to-bottom. The user reads it, then moves to Phase -1.2 for the mode choice.

## Template variables

The skill populates these variables by joining `detect.sh` output with `install-manifest.yaml`:

- `{{OS_FAMILY}}` — windows / macos / linux / unknown
- `{{PKG_MANAGER}}` — winget / brew / apt / dnf / pacman / missing
- `{{PRESENT[]}}` — list of items marked `present` by detect.sh
- `{{MISSING[]}}` — list of items with `core: true` and detect `missing`
- `{{UNKNOWN[]}}` — list of items with `unknown` detection (e.g. Claude in Chrome on Windows)
- `{{OPTIONAL[]}}` — list of items with `core: false` from the manifest
- `{{PLAN_TIER}}` — max / pro / team / free / unknown (detected from Claude account state)

## Card format

```
===== Phase -1.1 — Gap report =====

OS          : {{OS_FAMILY}}
Package mgr : {{PKG_MANAGER}}
Plan tier   : {{PLAN_TIER}}

Layer 3 — Dev essentials (present / missing)
  [{{NODE_MARK}}] Node.js LTS                    ({{NODE_NOTE}})
  [{{GIT_MARK}}]  Git                            ({{GIT_NOTE}})
  [{{CODE_MARK}}] VS Code                        ({{CODE_NOTE}})
  [{{CHROME_MARK}}] Google Chrome                ({{CHROME_NOTE}})
  [{{GH_CLI_MARK}}] GitHub CLI                   ({{GH_CLI_NOTE}})

Layer 4 — Automation surface
  [{{CODE_EXT_MARK}}] Claude Code VS Code extension    (doubles as `ide` MCP server)
  [{{PLAYWRIGHT_MARK}}] Playwright MCP                 (browser automation for Phase 5.5)
  [{{CIC_MARK}}] Claude in Chrome extension            (agentic browser; paste-back only)

Layer 4 — Multi-device (core, per beta-tester framing)
  [{{MOBILE_MARK}}] Claude mobile app                  (companion surface)
  [{{RC_MARK}}] Claude Code Remote Control             ({{RC_GATE}})

Layer 7 — Optional bonuses (offered at Phase -1.7)
  [ ] Google Antigravity                               (multi-LLM agent IDE, opt-in)
  [ ] GitHub Codespaces fallback                        (any-device cloud, opt-in)
  [ ] Android Termux local Claude Code                 (power-user, opt-in)
  [ ] Claude Code voice mode                           (if available, opt-in)

Summary
  Present  : {{COUNT_PRESENT}} items
  Missing  : {{COUNT_MISSING}} items
  Unknown  : {{COUNT_UNKNOWN}} items
  Optional : {{COUNT_OPTIONAL}} items

Estimated time per mode (for missing items only)
  Mode 1 — Detailed pas-à-pas : {{EST_DETAILED}} min
  Mode 2 — Semi-auto          : {{EST_SEMI_AUTO}} min
  Mode 3 — Auto               : {{EST_AUTO}} min

Security-floor interventions expected
  admin passwords    : {{COUNT_ADMIN}}
  sign-ins           : {{COUNT_SIGN_IN}}
  extension grants   : {{COUNT_EXT_GRANT}}
  pairings           : {{COUNT_PAIRING}}
  restarts           : {{COUNT_RESTART}}

===================================
```

## Marks

- `[x]` — present and healthy per detect.sh
- `[ ]` — missing, will be installed if approved
- `[?]` — unknown (detection not reliable on this OS), user will be asked to confirm
- `[·]` — already present but version below target (upgrade offered)

## Grouping rules

- Layers 3 and 4 always render, even if empty.
- Layer 4 multi-device section: if `PLAN_TIER == free`, replace the Remote Control line with a blocking error: **"Phase -1 requires a paid Claude plan — sign up for Pro or Max before continuing."** No other Phase -1 work runs.
- Layer 4 multi-device section: if `PLAN_TIER == pro` or `team`, mark Remote Control as `[~]` (not available on this plan) and add a one-line note pointing to the Codespaces fallback offered in Phase -1.7.
- Layer 7 always renders but only as an invitation — the consent card in Phase -1.2 is where the user opts in.

## Time estimates

Computed by summing per-item cost from the manifest. Default per-item costs for items not explicitly estimated:

- simple winget / brew / apt install: 1 min
- MCP add: 30 s
- extension paste-back: 2 min (sign-in + pin + grant)
- Remote Control pairing: 2 min (user drives pairing ceremony)

`EST_AUTO` assumes the user is present at sign-ins; `EST_DETAILED` adds ~20 min of explanation time; `EST_SEMI_AUTO` sits in the middle.

## Exit condition

Phase -1.1 ends when the user has read the card and typed any acknowledgement. The skill then renders `consent-card.md` (Phase -1.2). No install runs until the user chooses a mode and approves per-item in Phase -1.2.

## Rendering guidance for Claude

- Render the card as a single code block with no surrounding prose — the card is the message.
- Do not inject emoji, colour codes, or ANSI escapes.
- Keep the card <50 lines — truncate optional bonuses to their count line if the card overflows.
- After rendering, the next turn announces: **"Pick a mode: detailed / semi-auto / auto. Or type `skip phase -1` to bypass entirely."**
