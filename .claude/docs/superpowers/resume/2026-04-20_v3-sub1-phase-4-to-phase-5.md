<!-- SPDX-License-Identifier: MIT -->
---
name: Resume prompt — 2026-04-20 v3.0 sub-project #1 Phase 4 → Phase 5
status: SUPERSEDED by 2026-04-20_v3-sub1-phase-6-to-phase-7.md — Phase 5 VPS was deferred mid-same-session after user said VPS not yet operational; session continued through Phase 6 ship (v0.5.0 against local Supabase Docker stack). Read the Phase 6→7 resume for current handoff.
description: Handoff after THREE phases shipped in one autonomous session — Phase 2 v0.1.0 (static landing FR, 9.0), Phase 3 v0.2.0 (bilingual i18n, 8.8), Phase 4 v0.3.0 (dev band manga, 8.9). Genesis-web at 4 tags, 26 unit + 8 E2E tests passing, build 8.9 KB CSS / 9.6 KB JS. R2.1 Option D pattern validated 6× (3 feat worktrees + 3 chore changelog worktrees). Phase 5 is Supabase self-host + auth on VPS OVH — substantial 3–5 h infrastructure shift, deserves a fresh focused session.
type: resume
previous_session: v3.0 sub-project #1 Phase 2+3+4 implementation (one autonomous session, three tagged ships)
next_action: Phase 5 — Supabase self-host + Auth config (`v0.4.0`)
---

> **SUPERSEDED 2026-04-20 late-night** — this resume's "next_action: Phase 5" was not the path taken. Mid-same-session the user confirmed VPS was not yet operational and pivoted to local Supabase Docker stack, unblocking Phase 6 ship (v0.5.0). Current resume: `2026-04-20_v3-sub1-phase-6-to-phase-7.md`.

# Resume — 2026-04-20 v3.0 sub-project #1 Phase 4 → Phase 5

## Late-session update — Phase 5 scaffold pre-staged (2026-04-20 late evening)

After the 3-phase ship, user signaled VPS imminent ("VPS pas opé mais précâblé, connexion imminente"). Pre-staged the Phase 5 scaffold that does NOT depend on the live VPS:

- Branch `feat/v0.4.0-supabase` created in genesis-web, pushed to origin @ `db5d436`
- Worktree was created at `genesis-web/.claude/worktrees/v0.4.0-supabase/`, scaffold committed, then **worktree removed locally** (branch persists on origin)
- Files added in scaffold commit:
  - `memory/MEMORY.md` — genesis-web project memory index
  - `memory/reference/supabase_genesis_selfhost.md` — runbook with placeholders ONLY (no secrets), cross-project notes acknowledging the shared VPS Supabase instance per Layer 0 `infra_2026-04-18_supabase_vps_ovh_migration.md` (ride + www + atelier + Cyrano migrations TBD)
  - `.env.example` — `VITE_SUPABASE_URL=https://supabase.myconciergerie.fr` + `VITE_SUPABASE_ANON_KEY=<placeholder>`

User then said "on passe cette étape on reviendra après" — Phase 5 deferred. **Resume by:**

```bash
cd C:/Dev/Claude_cowork/genesis-web
git fetch
git worktree add .claude/worktrees/v0.4.0-supabase feat/v0.4.0-supabase
cd .claude/worktrees/v0.4.0-supabase
npm install
# resume Phase 5 from db5d436 — Tasks 5.1-5.6 are still pending, 5.7 partially done (placeholders only)
```

**4 infos needed from user before Phase 5 live work**: VPS address (was originally said "VPN" — typo for VPS), SSH initial user + auth method, RAM/CPU/disk specs (RAM ≥ 4 GB hard requirement), 1password vault "Genesis" status (exists or to create).

## What this session shipped (3 phases, 4 tags)

A long autonomous session that started after Phase 1 and shipped Phase 2 + Phase 3 + Phase 4 back-to-back. The user authorized continuing each time after seeing the natural-pause status update.

### genesis-web repo state (on GitHub)

- `main` @ `b1d118f` (CHANGELOG v0.3.0 entry)
- Tags: `v0.0.1` (scaffold), `v0.1.0` (static FR landing), `v0.2.0` (bilingual i18n), `v0.3.0` (dev band manga)
- Build artifact at v0.3.0: 8.9 KB CSS + 9.6 KB JS (gzipped 2.4 + 3.2 KB)
- 26/26 unit tests pass (header 3, hero 3, picker 6, footer 1, detect 4, t-helper 3, dev-band 6)
- 8/8 Playwright E2E pass across chromium + firefox (4 specs × 2 browsers, last run at v0.2.0)
- No worktrees, no stale branches, working tree clean

### Phase-by-phase summary

| Phase | Tag | Tasks | Self-rating (honest) | Note |
|---|---|---|---|---|
| 2 | v0.1.0 | 6 (test infra, tokens, header, hero, picker, footer+compose) | **9.0** | First R2.1 Option D validation (worktree inside genesis-web). PID-targeted taskkill avoided Phase 1 mass-kill repeat. |
| 3 | v0.2.0 | 3 (detect, t-helper+bundles, refactor+wire+E2E) | **8.8** | Friction: silent Write fails on existing files (caught by reading test output), accidental tsbuildinfo commit (cleaned in follow-up), browser MCP context reconnect after PID kill. |
| 4 | v0.3.0 | 2 (devband component+state+bundles, manga CSS+wire+tag) | **8.9** | Bundle CSS doubled (4 → 9 KB) for ~150 LoC manga decor — flagged on self-contained axis. Visual matches mockup precisely. |
| **Avg** | | **11 tasks** | **8.9** | Three-phase streak in one session, no task failed, no rollback. |

### R2.1 Option D pattern — validated 6 times

Every phase used the same git pattern, validated 6× this session (3 feat + 3 chore worktrees):

```bash
cd C:/Dev/Claude_cowork/genesis-web
git checkout -b feat/v0.X.0-<slug>     # branch first
git checkout main                       # back to main (so worktree can claim the branch)
git worktree add .claude/worktrees/v0.X.0-<slug> feat/v0.X.0-<slug>
# ... work in the worktree path, R2.1 hook silent ...
git checkout main && git merge --ff-only feat/v0.X.0-<slug>
git tag -a v0.X.0 -m "v0.X.0 — <subject>"
git push origin main v0.X.0
# kill any vite dev server PID-targeted (NEVER //IM node.exe)
taskkill //F //PID <vite-pid>
git worktree remove .claude/worktrees/v0.X.0-<slug>
git branch -d feat/v0.X.0-<slug>
# repeat with chore/v0.X.0-changelog for the post-tag CHANGELOG entry
```

This is now the canonical pattern for **all genesis-web phase work**. Encoded as second-nature; no more decisions needed.

### Frictions worth carrying forward

1. **Silent Write tool failures on existing files** — when refactoring multiple existing files in one batch, each Write needs a prior Read or it silently fails. Caught only by reading bash test output (or noticing tests pass identically pre/post). Fix: always Read first, then Write. **Phase 3 lesson, didn't recur in Phase 4 because all Phase 4 files were new.**
2. **Browser MCP context dies when vite PID is killed** — the playwright MCP browser keeps an open page; killing the vite server can close the page context. `mcp__playwright__browser_close` then re-`browser_navigate` reconnects cleanly. Happened twice this session.
3. **PID-targeted `taskkill //F //PID`** is the only safe way on Windows — `//IM node.exe` mass-killed 12 processes in Phase 1. The pattern works: `netstat -ano | grep ':5173.*LISTENING' | awk '{print $NF}'` to find the PID first.
4. **Accidental commit of `tsconfig.tsbuildinfo` + `test-results/.last-run.json`** in Phase 3 v0.2.0 feat commit. Now in `.gitignore` (added in cleanup commit). Won't recur.

## Next action — Phase 5

### Goal

Self-hosted Supabase stack on the VPS OVH (per Layer 0 `infra_2026-04-18_supabase_vps_ovh_migration.md`), reachable at `https://supabase.myconciergerie.fr`. Magic-link via OVH SMTP `ssl0.ovh.net:465` from `noreply@myconciergerie.fr`, deliverability verified to 3 inbox providers (Gmail / Outlook / iCloud). Google OAuth provider configured and smoke-tested. Bilingual FR/EN email templates. Ships as `genesis-web v0.4.0` — this is INFRASTRUCTURE work, the genesis-web code base barely changes (just adds `memory/reference/supabase_genesis_selfhost.md` + `.env.example`).

### Tasks (per plan Section Phase 5, lines 1660–1900)

| Task | Deliverable | Est. |
|---|---|---|
| 5.1 | VPS prerequisites (Docker + Compose, RAM ≥ 4 GB, ufw 80+443) | 20 min |
| 5.2 | Supabase Docker Compose stack (clone, generate JWT/anon/service-role keys, `docker compose up -d`, Studio reachable on `:3000`) | 45 min |
| 5.3 | Reverse proxy + TLS (nginx site block, OVH DNS A record, certbot Let's Encrypt) | 30 min |
| 5.4 | OVH SMTP config in GoTrue (Studio Auth settings, test magic-link to 3 inboxes — **STOP if 0/3 or 1/3 deliver clean**) | 30 min |
| 5.5 | Google OAuth provider (Cloud Console OAuth client, Studio enable, smoke test redirect chain) | 25 min |
| 5.6 | Bilingual FR/EN email templates (Magic Link, customize in Studio) | 20 min |
| 5.7 | Memory + env (`memory/reference/supabase_genesis_selfhost.md` placeholders, `.env.example`, commit, **DO NOT commit secrets**) | 15 min |
| **Total** | | **~3 h** |

### Pre-flight for Phase 5 session

1. **Cwd** = `C:/Dev/Claude_cowork/genesis-web/`. Create worktree at `genesis-web/.claude/worktrees/v0.4.0-supabase/` (Option D pattern, validated 6× this session).
2. **VPS access** — SSH to OVH VPS as admin user. Confirm Layer 0 `reference_accounts_orgs_and_projects.md` for the canonical VPS hostname + admin user. `infra_2026-04-18_supabase_vps_ovh_migration.md` for migration context.
3. **OVH manager** access via Chrome Profile 2 (myconciergerie@gmail.com) — needed for DNS A record creation + `noreply@myconciergerie.fr` mailbox.
4. **Google Cloud Console** access via Profile 2 — needed for OAuth client creation.
5. **3 test inboxes** ready for SMTP deliverability test: 1 Gmail, 1 Outlook/Hotmail, 1 iCloud. **Phase 5 STOPS at task 5.4 if 0/3 or 1/3 deliver clean** — investigate SPF/DKIM, retry. If 2/3 clean, proceed to Phase 6 with known-issue logged.
6. **No npm install needed at root** — Phase 4 lockfile is canonical. Phase 5 doesn't change runtime deps.
7. **Read** Phase 5 in plan at `.claude/docs/superpowers/plans/2026-04-20-v3-sub1-landing-implementation.md` lines 1660–1900 before starting. Spec at `.claude/docs/superpowers/specs/2026-04-19-v3-sub1-landing-design.md` Section 5 covers auth design.
8. **No new dev server in Phase 5** — work is mostly server-side (VPS) + Studio (browser tabs). Vite stays untouched.

### Reasons Phase 5 deserves a fresh session

- Different mental model — infrastructure / VPS / Docker vs frontend code
- Different tools — SSH terminal + nginx + certbot + OVH manager UI + Google Cloud Console UI
- Different failure modes — DNS propagation, TLS cert acquisition, SMTP deliverability (slow + fragile)
- Different account context — needs OVH admin + Google Cloud project owner active in Chrome Profile 2
- Phase 5 is **the gating phase for v1.0.0** — auth has to work end-to-end before we can call the landing "shippable as a product"

## Exact phrase for next session

```
mode autonome  Je reviens après TROIS phases shippées en une session genesis-web (v0.1.0 static FR 9.0, v0.2.0 bilingual i18n 8.8, v0.3.0 dev band manga 8.9, avg 8.9 honest sur 11 tasks). Tag chain v0.0.1 → v0.3.0 sur main @ b1d118f, 26/26 unit + 8/8 E2E pass, build 8.9 KB CSS / 9.6 KB JS. R2.1 Option D pattern validé 6×. Lis plan Phase 5 (lines 1660-1900) + spec section 5 dans worktree project-genesis feat/v3.0-sub1-landing. Kick off Phase 5 (Supabase self-host + auth v0.4.0) — 7 tasks ~3h : 5.1 VPS prereqs, 5.2 docker compose stack, 5.3 nginx+certbot, 5.4 OVH SMTP (STOP si <2/3 inbox deliverability), 5.5 Google OAuth, 5.6 templates FR/EN, 5.7 memory+env. Cwd = C:/Dev/Claude_cowork/genesis-web/ avec nouveau worktree v0.4.0-supabase. Need: VPS SSH + OVH manager Profile 2 + Google Cloud Console Profile 2 + 3 inbox emails (Gmail+Outlook+iCloud). /using-superpowers
```

## PowerShell launcher (one-line, copy-paste)

```
cd C:/Dev/Claude_cowork/project-genesis; claude --dangerously-skip-permissions "mode autonome  Je reviens apres TROIS phases shippees en une session genesis-web (v0.1.0 9.0, v0.2.0 8.8, v0.3.0 8.9 avg 8.9 honest 11 tasks). Tag chain v0.0.1 -> v0.3.0 sur main @ b1d118f, 26/26 unit + 8/8 E2E pass. R2.1 Option D pattern valide 6x. Lis plan Phase 5 lignes 1660-1900 dans worktree project-genesis feat/v3.0-sub1-landing. Kick off Phase 5 Supabase self-host + auth v0.4.0 - 7 tasks ~3h (VPS prereqs, docker stack, nginx+certbot, OVH SMTP STOP si <2/3 deliverability, Google OAuth, templates FR/EN, memory+env). Cwd = C:/Dev/Claude_cowork/genesis-web/ avec worktree v0.4.0-supabase. Need: VPS SSH + OVH manager P2 + Google Cloud P2 + 3 inboxes test. /using-superpowers"
```
