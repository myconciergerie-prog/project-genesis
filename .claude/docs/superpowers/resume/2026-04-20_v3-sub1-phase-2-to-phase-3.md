<!-- SPDX-License-Identifier: MIT -->
---
name: Resume prompt — 2026-04-20 v3.0 sub-project #1 Phase 2 → Phase 3
description: Handoff after Phase 2 (static landing visual FR — header + hero + picker + footer, v0.1.0 tagged) to Phase 3 (i18n system v0.2.0). Self-rating Phase 2 = 9.0 honest (avg over 5 axes). R2.1 hook resolved cleanly via Option D (worktree inside genesis-web). 9/9 unit tests pass, build clean, live verified via Playwright. Phase 3 estimate 1.5–2 h.
type: resume
previous_session: v3.0 sub-project #1 Phase 2 implementation
next_action: Phase 3 — i18n system (`v0.2.0`)
---

# Resume — 2026-04-20 v3.0 sub-project #1 Phase 2 → Phase 3

## What Phase 2 shipped

`genesis-web v0.1.0` — static landing page visual, French-only hardcoded copy, 4 components composed in `main.ts`. All 6 plan tasks delivered, then a follow-up CHANGELOG chore for the 5-axis self-rating entry.

### genesis-web repo state (on GitHub)

- `main` @ `4eb9f1d` (CHANGELOG entry) — 8 commits ahead of v0.0.1 baseline
- Tag `v0.1.0` @ `90a0d24` (squash of 6 feat commits + 1 chore + final compose)
- Build artifact: `dist/index.html` 0.62 KB + `dist/assets/index-*.css` 4.0 KB + `dist/assets/index-*.js` 3.5 KB (gzipped 1.4 KB + 1.5 KB combined)
- 9/9 unit tests pass (vitest + happy-dom). E2E config ready, no E2E specs yet (deferred to Phase 7+).

### Commit chain (Phase 2)

| SHA | Message |
|---|---|
| `4eb9f1d` | docs(changelog): v0.1.0 — Phase 2 landing FR |
| `90a0d24` | feat: full static landing FR — header + hero + picker + footer |
| `96b2f20` | feat(components): Picker with 3 provider cards |
| `4c4a52f` | feat(components): Hero with headline, subhead, CTA |
| `0f56c2c` | feat(components): Header with logo + FR/EN locale toggle |
| `f5dc5c8` | feat(styles): tokens + reset CSS |
| `5e00523` | chore: install vitest + playwright test infra |

### R2.1 hook strategy — decision and outcome

**Picked Option D** (over A/B/C from Phase 1 friction log): create a worktree inside `genesis-web` itself at `C:/Dev/Claude_cowork/genesis-web/.claude/worktrees/v0.1.0-landing/`, branch `feat/v0.1.0-landing`. The hook (at `~/.claude/hooks/enforce-worktree.ps1`) exempts any path matching `<project>\.claude\worktrees\<session>\` regardless of which project, so this is fully R2.1-compliant — no bypass, no Bash heredoc, no hook modification needed.

After Phase 2 ship: ff-merge to main → tag v0.1.0 → push → `git worktree remove` + `git branch -d`. The CHANGELOG chore re-validated the pattern by spinning up a second worktree (`v0.1.0-changelog`) for the 16-line edit, then cleaning up identically.

**Recommendation for Phase 3+**: keep using Option D. Each phase = one fresh worktree at `genesis-web/.claude/worktrees/v0.X.Y-<slug>/`, ff-merge to main when done.

### Phase 2 self-rating — honest 9.0

| Axis | Score | Reasoning |
|---|---|---|
| Pain-driven | 9.0 | Foundational visual layer for all subsequent phases (i18n, dev band, auth). Zero regressions. PID-targeted taskkill avoided Phase 1 mass-kill repeat. |
| Prose cleanliness | 9.5 | 6 atomic feat commits + 1 chore commit, all SPDX-tagged, descriptive messages, build clean (no TS errors, no warnings). |
| Best-at-date | 8.5 | Vite 8.0.8, TS 6.0.2, Vitest 4.1.4, Playwright 1.59.1, happy-dom 20.9.0 — all current as of 2026-04-20. |
| Self-contained | 9.0 | No external runtime deps, system fonts only, hardcoded FR copy, sub-10 KB build (gzipped 2.9 KB total). |
| Anti-Frankenstein | 9.0 | Each component isolated and composed in main.ts. No premature router/i18n/auth abstractions. Scope discipline held — Phase 2 boundaries respected. |
| **Avg** | **9.0** | Strong jump from Phase 1 (7.9). Validates Option D hook strategy. |

### Friction log for Phase 2

Two minor frictions, both expected and absorbed cleanly:

1. **Playwright MCP navigation interrupt** — back-to-back `browser_navigate` calls during HMR refresh produced "navigation interrupted by another navigation" error once. Re-issued the call, succeeded immediately. Not worth a Layer 0 entry — too transient.
2. **Worktree `rm` blocked by running vite dev server** — when removing the v0.1.0-landing worktree, the physical directory could not be deleted because PID 16800 (vite) had `node_modules/` files open. Resolution: PID-targeted `taskkill //F //PID 16800` (NOT `//IM node.exe`, per Phase 1 lesson), then `rm -rf` succeeded. Worth flagging to confirm pattern: **always kill background dev servers by PID before `git worktree remove`**.

## Next action — Phase 3

### Goal

`navigator.language` detection + `localStorage` persistence + FR/EN toggle that actually swaps strings. `fr.json` and `en.json` contain all landing strings extracted from current `main.ts` hardcodes. Ships as `genesis-web v0.2.0`.

### Tasks (per plan Section Phase 3, lines 1150+)

| Task | Deliverable | Est. |
|---|---|---|
| 3.1 | `src/i18n/detect.ts` + tests (4 tests for nav.language + localStorage round-trip) | 25 min |
| 3.2 | `src/i18n/t.ts` t(key) helper + reactive rebind + tests | 25 min |
| 3.3 | `fr.json` + `en.json` bundles — extract every string from main.ts hardcodes | 20 min |
| 3.4 | Wire toggle: clicking EN re-renders all components with English copy | 30 min |
| 3.5 | Persistence: localStorage round-trip survives page reload | 10 min |
| 3.6 | Visual dogfood both locales + tag `v0.2.0` | 15 min |
| **Total** | | **~1.5–2 h** |

### Pre-flight for Phase 3 session

1. **Cwd for Phase 3+ work** = `C:/Dev/Claude_cowork/genesis-web/` then create worktree at `genesis-web/.claude/worktrees/v0.2.0-i18n/` (Option D pattern).
2. **No npm install needed at root** — Phase 2 lockfile is canonical. Only re-install inside fresh worktree.
3. **Read plan Section Phase 3** at `.claude/docs/superpowers/plans/2026-04-20-v3-sub1-landing-implementation.md` lines ~1150 onward.
4. **Spec section 3** at `.claude/docs/superpowers/specs/2026-04-19-v3-sub1-landing-design.md` covers the i18n design — read before starting.
5. **R8 cache check** — `claude-code-plugin-structure_2026-04-19.md` and `claude-code-session-jsonl-format_2026-04-19.md` may be expired (expires 2026-04-20). Refresh if Phase 3 needs them (it shouldn't — i18n is pure runtime).
6. **Playwright dev server**: when killing it at session end, always use PID-targeted taskkill, never `//IM node.exe`.

## Exact phrase for next session

```
mode autonome  Je reviens après Phase 2 complète genesis-web v0.1.0 (header + hero + picker + footer FR, 9/9 unit tests pass, tag v0.1.0 @ 90a0d24, CHANGELOG @ 4eb9f1d). Self-rating Phase 2 = 9.0 honest (5-axis avg, strong jump from Phase 1 7.9). R2.1 strategy = Option D (worktree inside genesis-web/.claude/worktrees/) validated cleanly twice (feat + chore). Lis plan Phase 3 et spec section 3 dans worktree project-genesis feat/v3.0-sub1-landing. Kick off Phase 3 (i18n system v0.2.0) — 6 tasks : 3.1 detect, 3.2 t() helper, 3.3 fr/en bundles, 3.4 toggle wire, 3.5 persistence, 3.6 visual dogfood + tag. Cwd Phase 3+ = C:/Dev/Claude_cowork/genesis-web/ avec nouveau worktree v0.2.0-i18n. /using-superpowers
```

## PowerShell launcher (one-line, copy-paste)

```
cd C:/Dev/Claude_cowork/project-genesis; claude --dangerously-skip-permissions "mode autonome  Je reviens apres Phase 2 complete genesis-web v0.1.0 (header hero picker footer FR, 9/9 tests, tag v0.1.0 @ 90a0d24). Self-rating 9.0 honest. R2.1 Option D validated 2x. Lis plan Phase 3 et spec section 3 dans worktree project-genesis feat/v3.0-sub1-landing. Kick off Phase 3 (i18n system v0.2.0) - 6 tasks (detect t-helper bundles toggle persistence dogfood). Cwd Phase 3+ = C:/Dev/Claude_cowork/genesis-web/ avec nouveau worktree v0.2.0-i18n. /using-superpowers"
```
