<!-- SPDX-License-Identifier: MIT -->
---
name: Phase 5.5 Playwright automation branch
description: Optional branch that uses the Playwright MCP (installed at Phase -1 if the user opted in) to drive the GitHub SSH key add, PAT creation, and empty-repo creation forms programmatically, with a known-selector TTL and hard fall-back to paste-back on any mismatch
type: template
stage: 5.5.optional
expires_at: 2026-05-14
---

# Phase 5.5 — Playwright automation branch

Opt-in automation layer over Steps 5.5.1 (public key add), 5.5.2 (PAT creation), and 5.5.3 (empty repo create). Drives GitHub's forms via the Playwright MCP server installed at Phase -1, only if the user explicitly opted in at the consent card. Paste-back is always the safe baseline; Playwright is a convenience layer, not a replacement for understanding what's being done.

**Hard rule**: if any selector mismatches at runtime, the skill **immediately** falls back to paste-back for that step. No retry loops, no "close enough" selectors. The paste-back path is the contract.

**Selector snapshot date**: 2026-04-15 — re-verify when GitHub updates the form layout. See `expires_at` in the frontmatter. After that date, the skill refuses to run the Playwright branch until a human re-validates the selectors.

## Pre-conditions

Before invoking any Playwright action:

1. `memory/reference/automation-stack.md` lists the Playwright MCP as healthy.
2. The consent card recorded `Playwright automation opt-in: yes`.
3. A Chrome profile session is active in the profile chosen at the consent card.
4. The `expires_at` date in this file's frontmatter is in the future.

If any pre-condition fails, log the specific failure and fall back to the paste-back template for that step.

## Step 5.5.1 — Add public SSH key via Playwright

Target URL:

```
https://github.com/settings/ssh/new
```

Navigation sequence:

1. `browser_navigate` to the URL.
2. Wait for the form: `browser_wait_for` selector `input[aria-label="Title"]`.
3. `browser_type` into selector `input[aria-label="Title"]` — value is the SSH title from `ssh-keygen.md` Step 4.
4. `browser_type` into selector `textarea[aria-label="Key"]` — value is the public key content.
5. `browser_click` selector `button:has-text("Add SSH key")`.
6. Wait for redirect to `https://github.com/settings/keys`; selector `a[href="/settings/ssh/new"]` appearing confirms the list page rendered.
7. Confirm the new key's fingerprint is visible on the list page.

**Fall-back trigger**: any `wait_for` that times out after 10 seconds, or any form submission that does not redirect within 10 seconds. Fall back to `ssh-keygen.md` Step 4 paste-back.

## Step 5.5.2 — Create fine-grained PAT via Playwright

Target URL:

```
https://github.com/settings/personal-access-tokens/new
```

Navigation sequence (follows the exact field order documented in `pat-walkthrough.md` Step 2):

1. `browser_navigate` to the URL.
2. `browser_type` into selector `input[aria-label="Token name"]` — the name value.
3. `browser_type` into selector `textarea[aria-label="Description"]` — the description value.
4. `browser_click` selector `button[aria-label="Resource owner"]` — opens the dropdown.
5. `browser_click` selector `li[role="option"]:has-text("{{GITHUB_OWNER}}")` — selects the owner.
6. `browser_click` selector `input[type="radio"][value="custom"]` for expiration — opens the date picker.
7. `browser_type` the `{{EXPIRATION_DAYS}}`-forward-dated value into the date input.
8. `browser_click` selector `input[type="radio"][value="all"]` for Repository access.
9. For each of the five canonical permissions, click the row's dropdown and select the required level:
   - Contents → Read and write
   - Metadata → Read (auto-selected, verify)
   - Pull requests → Read and write
   - Workflows → Read and write
   - Administration → Read and write
10. `browser_click` selector `button:has-text("Generate token")`.
11. Wait for the one-time green banner: selector `div[data-testid="token-value"]` or `span.token`.
12. **Capture the token text** via `browser_evaluate` reading `document.querySelector('[data-testid="token-value"]').textContent`.

**Token capture is the single riskiest Playwright step** — if the selector changes and capture fails, the token is displayed on screen and immediately lost on any navigation. The skill mitigates this by:

- Calling `browser_snapshot` immediately after the "Generate token" click, so the rendered DOM is frozen in the tool result if selector-based capture fails.
- Attempting three selector variants in order: `[data-testid="token-value"]`, `span.token`, then any `<span>` whose text matches `^github_pat_11[A-Za-z0-9_]+$`.
- If all three fail, the skill prints the snapshot HTML to the user with a clear instruction: *"Copy the token value from the screenshot above and paste it here — GitHub will not re-display it."*

The captured token goes into `.env.local` via the same sink as paste-back (`pat-walkthrough.md` Step 4).

**Fall-back trigger**: any selector timeout during Steps 2-10 falls back to `pat-walkthrough.md` paste-back from that step forward. Step 12 has the snapshot safety net described above and does not fall back — once the token is on screen, the only path is to capture it or force the user to re-create.

## Step 5.5.3 — Create empty repo via Playwright

Target URL:

```
https://github.com/new
```

Navigation sequence (follows `empty-repo-create.md` Step 2):

1. `browser_navigate` to the URL.
2. `browser_click` selector `button[aria-label="Owner"]` — opens the Owner dropdown.
3. `browser_click` selector `li[role="option"]:has-text("{{GITHUB_OWNER}}")`.
4. `browser_type` into selector `input[aria-label="Repository name"]` — the repo name.
5. `browser_wait_for` the green availability checkmark: `svg[aria-label="Available"]` appears next to the name field. Time-out 3 seconds.
6. `browser_type` into selector `input[aria-label="Description (optional)"]` — the description value.
7. `browser_click` selector `input[type="radio"][value="{{VISIBILITY}}"]`.
8. **Do not click any "Initialize with" checkbox.** Leave all three unchecked.
9. `browser_click` selector `button:has-text("Create repository")`.
10. Wait for redirect to `https://github.com/{{GITHUB_OWNER}}/{{REPO}}`.

**Fall-back trigger**: name-availability check fails OR redirect does not land on the expected URL within 10 seconds. Fall back to `empty-repo-create.md` paste-back.

## Known-selector health check

Before any step, the skill runs a cheap selector sanity check by navigating to `https://github.com/settings/ssh/new` and confirming `input[aria-label="Title"]` exists. If it does not, GitHub's UI has changed and the entire Playwright branch is disabled for this session. The skill reports the selector drift in `memory/reference/automation-stack.md` under a `selector_drift_detected_at` field so a future session can update this file.

## Screenshot-on-failure

Every fall-back event triggers `browser_take_screenshot` before handing off. The screenshot is saved to `.claude/docs/superpowers/research/archive/playwright_fallback_{{DATE}}_{{STEP}}.png` for forensic review. This is not for auto-repair — it is for the human who will eventually update the selector map to see exactly what GitHub rendered.

## Exit condition

- Either all three steps (5.5.1–5.5.3) executed successfully via Playwright, or
- Any single step fell back to paste-back and the subsequent steps continued from the paste-back path.
- The `memory/reference/automation-stack.md` is updated with the Playwright run outcome.
- Control passes back to the `SKILL.md` main flow, which invokes `three-probe-test.md` regardless of the path taken.

## Anti-Frankenstein

- Do not attempt to auto-repair a broken selector at runtime. One-miss → paste-back, no retry loops.
- Do not store the PAT token in the Playwright snapshot beyond the single turn where it is captured. Scrub the snapshot from Claude's conversation state as soon as the token is in `.env.local`.
- Do not expand the Playwright branch to automate the SSH key generation itself (Step 5.5.1 Step 2) — key material must stay local and non-browser.
- Do not re-use form selectors past the `expires_at` date. Re-validate first.
- Do not add a third fall-back path "just in case" — paste-back is the single fall-back and that simplicity is the whole point.
