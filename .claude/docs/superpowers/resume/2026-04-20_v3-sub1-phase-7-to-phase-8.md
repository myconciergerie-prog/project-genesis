<!-- SPDX-License-Identifier: MIT -->
---
name: Resume prompt — 2026-04-20 v3.0 sub-project #1 Phase 7 → Phase 8
description: Handoff after Phase 7 ship (v0.6.0 — router + /welcome + session observer + sign-out). Genesis-web at 6 tags (v0.0.1 → v0.6.0, v0.4.0 still reserved for VPS). 71/71 unit + 24/24 E2E pass. Honest self-rating 8.7 (streak 8.9 broken by Supabase realtime rollback on Windows + config.toml cwd-sensitivity + dev-server port mismatch with auth allowlist). Next is Phase 8 — VPS production deploy — which requires VPS provisioning by user (OVH) before Claude work resumes. Full end-to-end session lifecycle works locally; Phase 7 code will run unchanged on prod with two .env.local lines swapped.
type: resume
previous_session: v3.0 sub-project #1 Phase 7 implementation (v0.6.0)
next_action: Phase 8 — VPS production deploy (v1.0.0) — **BLOCKED on OVH VPS provisioning by user**
---

# Resume — 2026-04-20 v3.0 sub-project #1 Phase 7 → Phase 8

## What Phase 7 shipped (`v0.6.0`)

Delivered in one autonomous session after the 4-phase record (Phase 2+3+4+6). All 5 Phase 7 tasks done in ~1.5h.

### genesis-web repo state (on GitHub)

- `main` @ `7dfcdb8` (chore v0.6.0 CHANGELOG merged)
- Tags: `v0.0.1` `v0.1.0` `v0.2.0` `v0.3.0` `v0.5.0` **`v0.6.0`** — **v0.4.0 still intentionally skipped** for the future VPS deploy
- Build at v0.6.0: **16.83 KB CSS + 213.29 KB JS** (gzipped 3.8 + 56.3 KB). +3.4 KB CSS / +8.6 KB JS vs v0.5.0 (router + session + callback + welcome page composition)
- **71/71 unit tests pass** (added 34: router 6, session 7, callback 6, welcome-hero 4, config-cards 3, empty-state 3, page composition 5)
- **24/24 Playwright E2E pass** (chromium + firefox): 3 landing + 5 auth-magic-link + 1 auth-google-oauth + **3 Phase 7 welcome** (full flow + expired banner + unknown path fallback)
- No worktrees, no stale branches, working tree clean
- Two PRs merged: #1 feat/v0.6.0-welcome → main, #2 chore/v0.6.0-changelog → main

### What ships end-to-end on localhost

The full session lifecycle works against the local Supabase Docker stack:

1. Landing `/` → "Obtenir l'accès anticipé →" CTA → Auth modal (Phase 6)
2. Email submitted → GoTrue sends magic-link email → Mailpit catches it at `:54324`
3. User clicks link → `http://127.0.0.1:54321/auth/v1/verify?...&redirect_to=http://localhost:5173/auth/callback`
4. GoTrue 302 → `/auth/callback#access_token=...&type=magiclink`
5. `src/auth/callback.ts` detects hash, `supabase.auth.getSession()` returns the session (SDK auto-processed the hash via `detectSessionInUrl: true`)
6. Router navigates `/welcome` with replaceState
7. `/welcome` renders the authed dashboard: user chip in header, "Bonjour {name} 👋" hero, AI Provider + Platform cards, 🌱 empty state, secondary CTAs, Déconnexion link in footer
8. Click Déconnexion → `signOut()` + `router.navigate('/')` → landing visible again
9. Unauth-only access attempts to `/welcome` → `/?auth=expired` with amber banner

### Honest self-rating (5-axis)

**8.7** — drop from 8.9 streak because of three real frictions:

- **Pain-driven 9.0** — first complete session lifecycle; unblocks Phase 8 entirely (Phase 7 code runs unchanged on VPS — only `.env.local` changes)
- **Prose cleanliness 8.5** — one atomic feat commit, but `supabase stop`+`start` from the wrong dir and starting dev server on 5177 first cost ~5 min
- **Best-at-date 8.5** — vanilla-TS router (no lib), @supabase/supabase-js 2.x session helpers, `exchangeCodeForSession` for PKCE
- **Self-contained 8.5** — 53+26+37+49 LOC core + 118 CSS, no premature abstraction (no params/nested routes/guards in router — YAGNI for 3 paths)
- **Anti-Frankenstein 9.0** — header + footer extended via optional props, no Phase 2-6 rewrites

### Frictions worth carrying forward (new this session)

1. **Supabase `stop`+`start` rollback on Windows — recurrence of Phase 6 pattern, now hitting `realtime` instead of `storage`**. Same mechanism: one container goes unhealthy during startup health-wait → `supabase start` aborts and removes the whole stack. Fix: `[realtime] enabled = false` in `supabase/config.toml`, analogous to the `[storage] enabled = false` from Phase 6. **If a third container hits this on Windows (likely candidate: vector, pooler, or edge_runtime), consider promoting the full "Windows minimal local Supabase config" to Layer 0** as a canonical pattern (currently only partial in `reference/supabase_genesis_selfhost.md`).
2. **`supabase` CLI reads `supabase/config.toml` from cwd, not from sibling repo root**. Running `npx supabase start` from the main repo dir ignored the worktree's config.toml edits. Fix: run CLI from the worktree when editing config. Containers still share by `project_id`, so this is usually invisible.
3. **GoTrue `GOTRUE_URI_ALLOW_LIST` is exact-match, not prefix**. Port 5177 (my first dev-server attempt) wasn't in the allowlist → email silently fell back to `site_url` (`http://127.0.0.1:3000`, dead). Fix: switch to 5173 which was in the list, or add ports explicitly. The allowlist supports multiple entries (see config.toml `additional_redirect_urls` array).
4. **Mailpit API blocked by CORS in browser context** — `fetch('http://127.0.0.1:54324/...')` from `page.evaluate()` fails, but server-side `page.request` or `curl` work. Use server-side fetches when parsing emails in E2E.
5. **Task description ambiguity — "session retro" file didn't exist**. The user's resume phrase referenced `2026-04-20_genesis-web-phase-2-3-4-6.md` but that retro was never written as a separate file — the previous resume prompt carried all retro content inline. Proceeded with the resume prompt alone. Worth noting: the session-post-processor skill exists but is manual-invoke only, and was not fired at Phase 6 close.

### Cumulative frictions (carried from prior phases, still relevant)

1. Silent Write tool failures on existing files (Phase 3, 6) — Read before Write is the only reflex that prevents it.
2. `git add -A` after first build of new test infra (Phase 3) — reflex worked Phases 4/6/7.
3. Supabase storage + realtime healthcheck timeouts on Windows (Phase 6 + Phase 7) — config toggles are the fix.
4. Test assertion pattern (Phase 6) — `classList.contains` not `querySelector('.cls-modifier')` for root-element checks.
5. Browser MCP context closes on vite PID kill — `browser_close` then re-navigate.
6. PID-targeted taskkill — validated 4× more, zero mass-kill incidents.

### Local Supabase stack state at session end

Still running. 10+ containers healthy. Realtime now disabled per config:

```
supabase_studio   healthy   :54323
supabase_pg_meta  healthy
supabase_auth     healthy   :54321  ← GoTrue with URI_ALLOW_LIST extended to include localhost:5173
supabase_kong     healthy   :54321  (API gateway)
supabase_rest     running
supabase_inbucket healthy   :54324  ← Mailpit magic-link catcher
supabase_analytics healthy
supabase_db       healthy
# realtime disabled (Windows rollback workaround)
# storage disabled (Phase 6 workaround, still)
```

Stop via `docker stop $(docker ps -q --filter name=supabase_)` OR `cd <worktree-or-genesis-web-root> && npx supabase stop`. Next session can reuse as-is.

## Next action — Phase 8

### Goal

`https://genesis.myconciergerie.fr` serves the landing with working auth end-to-end. Acceptance criteria #1–#12 from spec Section 15 all green. Tag `v1.0.0` — first public shippable version.

### **BLOCKER** — VPS provisioning

Phase 8 is 90% user infrastructure work, 10% Claude code. The VPS has not yet been provisioned. Before Claude work resumes, user needs:

1. **OVH VPS live** — Linux, Docker-capable, SSH reachable, IPv4 (IPv6 optional)
2. **Domain DNS ready** — `A genesis.myconciergerie.fr → VPS_IP`, TTL 300, propagated
3. **VPS base stack installed** — Docker + nginx + certbot, user `deploy` with ssh keys ready
4. **Supabase self-hosted stack running on VPS** — this is Phase 5's deferred work (plan lines 1100+), will reuse the official Supabase Docker Compose from the repo. Realtime + storage can be re-enabled (Linux, no Windows healthcheck issue).
5. **OVH SMTP credentials in 1Password vault "Genesis"** — for GoTrue outbound email (no more Mailpit)
6. **Google OAuth credentials for production** — new OAuth client in GCP with `https://genesis.myconciergerie.fr/auth/callback` as authorized redirect, client_id + secret in 1Password
7. **GitHub Actions secrets set** — `VPS_SSH_PRIVATE_KEY`, `VPS_HOST`, `VPS_USER`, `VPS_PATH=/var/www/genesis/`, `VITE_SUPABASE_URL`, `VITE_SUPABASE_ANON_KEY`

See plan lines 2117–2250 for full Phase 8 breakdown. Tasks 8.1–8.6 cover deploy key setup, nginx + certbot, DNS, GH Actions workflow, end-to-end smoke test, and `v1.0.0` tag.

### Tasks to do in the Phase 8 session (once VPS is live)

| Task | Deliverable | Est. |
|---|---|---|
| 8.1 | VPS deploy key + nginx + certbot + DNS + `/var/www/genesis/` dir | 30 min (user-led) |
| 8.2 | `.github/workflows/deploy-production.yml` (unit + E2E + build + rsync + axe-core) | 45 min |
| 8.3 | End-to-end smoke on `https://genesis.myconciergerie.fr` | 20 min |
| 8.4 | Tag `v1.0.0` | 5 min |
| **Total** | | **~1.5–2h** |

### Alternative if VPS is delayed

User could ask to ship **Phase 5 (VPS Supabase self-host, `v0.4.0`)** first as a pre-req, rolled into a combined v0.4.0 + v1.0.0 ship. Or pivot to Cloudflare Pages for the frontend (Phase 8 has it as a fallback pipeline path) to unblock frontend while Supabase VPS is provisioned separately.

## Pre-flight for Phase 8 session

1. **Cwd** = `C:/Dev/Claude_cowork/genesis-web/`. Create worktree at `genesis-web/.claude/worktrees/v1.0.0-deploy/` on fresh `feat/v1.0.0-deploy` branch.
2. **Verify VPS prerequisites** (checklist above items 1–7). Do not start code before items 1–6 are green.
3. **Local Supabase stack** — can stop it now to free ~500 MB RAM; Phase 8 uses the VPS-hosted stack, not local.
4. **Read plan Phase 8** at `.claude/docs/superpowers/plans/2026-04-20-v3-sub1-landing-implementation.md` lines 2117–2250.
5. **Spec section 11-15** at `.claude/docs/superpowers/specs/2026-04-19-v3-sub1-landing-design.md` for acceptance criteria and deploy architecture.

## Exact phrase for next session

```
mode autonome  Je reviens après Phase 7 shipped genesis-web v0.6.0 (8.7 honest streak 8.9 broken par Supabase realtime rollback Windows + config.toml cwd + port/allowlist). Tag chain v0.0.1 → v0.6.0 sur main @ 7dfcdb8, v0.4.0 skipped réservé VPS. 71/71 unit + 24/24 E2E pass. Full session lifecycle (landing → magic-link → welcome → sign-out) working end-to-end sur local Supabase. Phase 8 = VPS production deploy + v1.0.0 — BLOCKED on OVH VPS provisioning. Vérifie si VPS live (ssh + docker + nginx + certbot + supabase stack + OVH SMTP + Google OAuth prod creds). Si oui: lis resume Phase 7→8 + plan lignes 2117-2250 + spec sections 11-15, kick off Phase 8 (4 tasks ~1.5-2h). Cwd = C:/Dev/Claude_cowork/genesis-web/ avec worktree v1.0.0-deploy. Si VPS pas prêt: propose alternative (Cloudflare Pages pivot ou Phase 5 combined avec Phase 8). /using-superpowers
```

## PowerShell launcher (one-line, copy-paste)

```
cd C:/Dev/Claude_cowork/project-genesis; claude --dangerously-skip-permissions "mode autonome  Je reviens apres Phase 7 shipped genesis-web v0.6.0 (8.7 honest streak 8.9 broken par Supabase realtime rollback Windows + config.toml cwd + port/allowlist). Tag chain v0.0.1 -> v0.6.0 main @ 7dfcdb8, v0.4.0 skipped reserve VPS. 71/71 unit + 24/24 E2E pass. Full session lifecycle (landing -> magic-link -> welcome -> sign-out) working e2e local Supabase. Phase 8 = VPS production deploy + v1.0.0 - BLOCKED on OVH VPS provisioning. Verifie si VPS live (ssh + docker + nginx + certbot + supabase stack + OVH SMTP + Google OAuth prod). Si oui lis resume Phase 7->8 + plan lignes 2117-2250 + spec 11-15 et kick off Phase 8 (4 tasks ~1.5-2h). Cwd = C:/Dev/Claude_cowork/genesis-web/ avec worktree v1.0.0-deploy. Si VPS pas pret propose alternative (Cloudflare Pages pivot ou Phase 5 combined). /using-superpowers"
```
