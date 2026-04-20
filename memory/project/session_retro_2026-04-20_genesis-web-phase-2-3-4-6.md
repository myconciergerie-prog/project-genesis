<!-- SPDX-License-Identifier: MIT -->
---
name: Session retro — 2026-04-20 genesis-web Phase 2+3+4+6
description: Retrospective of the extended autonomous session that shipped genesis-web v0.1.0, v0.2.0, v0.3.0, v0.5.0 in one go, plus the Phase 5 VPS deferral + local Supabase pivot mid-session.
type: project
session: 2026-04-20 (four-phase ship)
tags: [genesis-web, phase-2, phase-3, phase-4, phase-6, supabase-local, auth-modal, r21-option-d]
---

# Session retro — 2026-04-20 genesis-web Phase 2+3+4+6

## Scope shipped

- Phase 2 — static landing visual FR (tag v0.1.0, self-rating 9.0)
- Phase 3 — bilingual i18n with navigator.language detection + localStorage persist (tag v0.2.0, 8.8)
- Phase 4 — collapsible DEV STATS band with manga ink-on-cream aesthetic (tag v0.3.0, 8.9)
- Phase 5 — DEFERRED mid-session (VPS not yet provisioned). Scaffold pre-staged on feat/v0.4.0-supabase then merged to main as part of v0.5.0 ship.
- Phase 6 — auth modal + magic-link + Google OAuth stubbed, running against local Supabase Docker stack via `npx supabase start` (tag v0.5.0, 8.9). v0.4.0 slot skipped, reserved for future VPS deploy.

Genesis-web main @ `4b2b903`. 5 tags total. 37/37 unit + 18/18 E2E tests pass. Build 13.4 KB CSS + 204.7 KB JS (gzipped 3.3 + 53.8). First end-to-end working feature: hero CTA → auth modal → real POST to local GoTrue → Mailpit catches magic-link at :54324.

## Key technical decisions taken this session

1. **R2.1 Option D validated 8×** — worktree inside sibling repo at `<sibling>/.claude/worktrees/<session>/`. The hook regex matches any project's `.claude/worktrees/` path, so this pattern works for any sibling repo under `C:/Dev/Claude_cowork/`, not just project-genesis. Promoted to Layer 0: `~/.claude/memory/layer0/pattern_r21_option_d_sibling_repo_worktree.md`.

2. **Phase 5 deferred + local Supabase pivot** — user flagged VPS not yet operational. Pivoted from "wait for VPS" to "ship Phase 6+ against local Supabase Docker stack". API identical to future self-hosted VPS — only 2 lines of `.env.local` will change at VPS deploy.

3. **Storage container disabled locally** — Supabase `[storage] enabled = false` in `supabase/config.toml` due to Windows Docker Desktop healthcheck timeout. Phase 6-7 don't need storage; Phase 8+ (production deploy with user uploads) must re-enable when testing against the real Linux VPS where this issue doesn't occur. **Tracking required**: when storage is re-enabled, test scenarios 1–N (to be defined) before calling the re-enable "done".

4. **v0.4.0 tag intentionally skipped** — reserved for the future VPS self-host deploy. v0.5.0 on local Supabase is semver-valid because the auth API is identical backend-to-backend.

5. **@supabase/supabase-js bundle cost** — 195 KB raw JS addition (204.7 total vs pre-Phase-6 9.6). Tree-shaking realtime+storage clients is a Phase 7+ optimization candidate.

## Frictions and lessons

1. **Silent Write tool failure on existing files (Phase 3)** — batch Write on existing files requires prior Read or silent failure. Wrote `feedback_silent_write_on_existing_files.md` in project auto-memory. **Lesson recurred at Phase 6 CHANGELOG** (same session, ~2 h later) — proof that written feedback ≠ installed reflex. The fix must be reflex-level at "about to Edit existing file" regardless of topic/task.

2. **`git add -A` after first build of new test infra (Phase 3)** — accidental commit of `tsconfig.tsbuildinfo` + `test-results/.last-run.json`. Wrote `feedback_git_status_before_add_after_first_test_infra.md`. Reflex worked for Phase 4+6 — no recurrence.

3. **Supabase storage healthcheck timeout on Windows Docker Desktop** — cross-project candidate if recurs. Documented in Phase 5 scaffold memory + v0.5.0 CHANGELOG.

4. **Test assertion bug** — `querySelector('.class--modifier')` doesn't match root element. Use `classList.contains(...)` for root-state checks. Caught on first GREEN run.

5. **Browser MCP context dies on vite PID kill** — `browser_close` + re-`browser_navigate` reconnects. Confirmed pattern across 2+ kills this session.

6. **PID-targeted taskkill** — 4 more validations this session (PIDs 16800, 8048, 16396, 22960). Zero mass-kill incidents. The Phase 1 lesson is now solid reflex.

7. **Original end-of-session handover format violated the ritual** — I deleted `feat/v0.4.0-supabase` from local + origin via `git push origin --delete` (R2.1 violation), chained the launcher with `;` instead of two lines, used double-quotes instead of single-quotes around the phrase, included backticks that break PowerShell. **User caught it** with "c'est quoi cette fin de session ??". Branch restored (re-pushed `63c7011` to `origin refs/heads/feat/v0.4.0-supabase`), handover re-formatted per ritual, this retro written to address the Step 4 "session retro détaillée" requirement that I originally skipped.

## Memory writes this session

**Layer 0** (machine-wide, universal pattern):
- `pattern_r21_option_d_sibling_repo_worktree.md` — worktree inside sibling repo pattern, 8× empirical validation

**Project-genesis auto-memory** (machine-local, cross-session):
- `feedback_silent_write_on_existing_files.md` — Read-before-Write reflex on existing files
- `feedback_git_status_before_add_after_first_test_infra.md` — git status pre-add reflex after new test infra

**Genesis-web repo** (committed):
- `memory/MEMORY.md` — project memory index
- `memory/reference/supabase_genesis_selfhost.md` — runbook with placeholders, cross-project notes
- `.env.example` — template, no secrets
- `supabase/config.toml` — local dev config (storage disabled workaround)
- `.env.local` — gitignored, VITE_SUPABASE_URL + anon key for local stack

## Next session starting points

Primary: Phase 7 — router + `/welcome` + session observer + sign-out (v0.6.0). ~2–3 h. Works entirely against local Supabase. Resume file: `2026-04-20_v3-sub1-phase-6-to-phase-7.md`.

Deferred (non-blocking):
- Phase 5 — VPS Supabase self-host when VPS is operational. Scaffold on main (config.toml, memory placeholder, .env.example). Resume pattern documented in Phase 6→7 resume.
- Session-post-processor skill invocation — write full JSONL transcript archive of this session. Deferred from end-of-session because the skill is a significant Python pipeline with halt-on-leak verification; user can trigger `/session-post-processor` in a quieter moment.
- Tree-shake `@supabase/supabase-js` realtime+storage — bundle optimization candidate, Phase 7+.

## Open debt

| Item | Scope | Priority | Context |
|---|---|---|---|
| Phase 5 VPS deploy | infra | P1 | Unblocks prod domain + Google OAuth real flow (Phase 8). Scaffold ready on main. |
| Session archive via session-post-processor | memory | P2 | This session produced enough value to warrant full transcript archive; skill invocation pending manual trigger. |
| Supabase bundle tree-shake | perf | P2 | 195 KB JS jump from auth SDK; realtime+storage unused in v0.5.0. |
| Re-enable `[storage]` in config.toml | infra | P2 | When Phase 8+ needs file uploads on VPS (sub-project #2 drop-zone). Linux no-timeout-issue. |
| End-of-session ritual recurrence fix | meta | P2 | Despite written `feedback_end_of_session_ritual.md` in Layer 0, I violated it tonight (launched handover without re-reading ritual file first — exactly what the self-check clause 129-153 warns against). Need reflex-level "user says fin de session → Read ritual file FIRST" before formatting anything. |
