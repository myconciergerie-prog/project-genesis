<!-- SPDX-License-Identifier: MIT -->
---
name: v3.0 sub-project #1 — landing + provider picker UI design
description: Design spec for the first sub-project of Genesis v3 — the landing page at genesis.myconciergerie.fr with BYOAI provider picker, magic-link + Google OAuth sign-in, and /welcome micro-dashboard post-auth. Anthropic-first staged rollout per master.md v3 vision. Free-tier VPS OVH deploy.
type: design-spec
created_at: 2026-04-19
target_version: v3.0-sub1
status: draft
supersedes: null
related:
  - memory/master.md § "What v3 vision is"
  - .claude/docs/superpowers/specs/2026-04-19-v2-bootstrap-via-max-subscription-design.md
  - memory/project/aurum_frozen_scope_lock.md
---

# v3.0 sub-project #1 — Landing + provider picker UI

## 1. Overview

### What this sub-project ships

The public landing page at `genesis.myconciergerie.fr` with:

1. A bilingual (FR+EN auto-detect) marketing hero explaining Genesis.
2. A BYOAI provider picker surfacing three cards (Anthropic active, Gemini and OpenAI placeholdered per staged v3.x/v3.y rollout).
3. A collapsible **DEV STATS** band rendering technical specs in a manga-European aesthetic — targets developer audience without cannibalizing the paid platform positioning (M2 framing — platform benefits for devs, not CLI install command).
4. Real platform sign-in via Supabase Auth — **Google OAuth** + **magic-link email**.
5. A `/welcome` post-auth micro-dashboard with provider config, platform status, future-anchor empty state for sub-project #2 drop-zone, and secondary CTAs (Discord/Changelog/GitHub).

### What this sub-project does NOT ship

Explicitly out of scope (deferred to subsequent v3 sub-projects):

- The drop-zone upload UI (sub-project #2).
- Project extraction / bootstrap pipeline (sub-project #3).
- Deploy pipeline for user projects (sub-project #4).
- User dashboard with real project listings (sub-project #5).
- Stripe / paid-tier subscription flow (sub-project #6+).
- Custom domains / webhooks / team management for paid tier (roadmap — labelled as `ROADMAP` in the DEV STATS card).
- Gemini / OpenAI provider implementations (v3.x / v3.y).

### Why a dedicated sibling repo

Per section 3 decisions below, this code ships in a **new sibling repo `myconciergerie-prog/genesis-web`**, not as a subdirectory of `project-genesis`. Rationale: `project-genesis` is the free MIT-licensed Claude Code plugin (the canonical skill source per master.md design discipline #5); `genesis-web` is the hosted platform entry surface. Decoupling lets the landing ship at a different cadence than the plugin and keeps the marketplace-installable plugin repo clean of web assets.

## 2. Scope boundary — what sub-project #1 truly is

| Dimension | In scope | Out of scope |
|---|---|---|
| Visual | Header, hero, picker, dev band (collapsible), footer, modal, welcome | Drop-zone UI, dashboard, project detail pages |
| Content | Marketing copy for landing + post-auth placeholder copy | Feature-page copy, pricing page, FAQ, docs |
| Auth | Google OAuth + magic-link email (Supabase Auth cloud) | GitHub OAuth, SAML, MFA, team invites |
| Backend | Supabase cloud auth + user metadata only | Drop-zone storage, extraction pipeline, deploy orchestration |
| Providers | Anthropic as active (UI only — no model call) | Actual AI model invocation, provider routing logic |
| Languages | FR + EN auto-detect + toggle | Other languages (pt/es/de deferred) |
| Deploy | VPS OVH via main/production 2-branch, fallback Cloudflare Pages | Auto-scale, multi-region, CDN tuning |
| Analytics | None in v1 | Plausible / umami / GA4 (sub-project #2+) |

**Honesty clause**: the only claims surfaced on the landing are truthful today. The "PLATFORM · PAID" card lists capabilities labelled as `ROADMAP`, not as features. Pricing page is absent because pricing isn't decided.

## 3. Architecture decisions (Q1–Q6)

All decisions locked during the 2026-04-19 brainstorming session. Ordered by the questions that surfaced them.

### Q1 — Stack: **Vite + vanilla TypeScript**

Picked over Next.js and static HTML for three load-bearing reasons:

1. **Grow-path preserved cheaply.** Sub-project #2 will add a drop-zone page reusing `<Header/>`, `<ProviderCard/>`, picker state, and the auth modal. Vite's component model makes that import-by-path trivial; static HTML would require copy-pasting and CSS forking.
2. **No vendor lock-in on deploy.** Vite outputs plain static files — deploys to OVH VPS or Cloudflare Pages without Vercel-tier-commercial restrictions that would affect the paid SaaS tier.
3. **V2 design discipline #5 preserved.** Vanilla TS + web-standard DOM APIs are server-side-vendorable when the v3.x platform backend SSRs components.

Framework flavor: **vanilla TS first**, not React. React can be introduced if picker state plus modal plus localization hooks justify a component framework; v1 scope is tight enough that `DocumentFragment` + custom elements suffice. Revisit at sub-project #2.

### Q2 — Scope: **Minimum Viable Landing (MVL) + real auth**

Rejected "full marketing site" (V2) and "multi-page" (V3) as speculative copy for a product whose backend doesn't exist. MVL is a single scrollable page: hero + picker + dev band + footer. The "waitlist CTA" originally proposed was upgraded to **real platform authentication** per user intent ("je voyais bien magiclink ou gmail pour point d'entrée en connexion").

### Q3 — Repo location: **Sibling repo `myconciergerie-prog/genesis-web`**

Rejected subdirectory in `project-genesis` (`web/`) because:

- **Version semantics** — landing typo fix would force a plugin tag bump, or drift between git tag and `plugin.json` (semver lie).
- **Business model** — plugin is OSS MIT marketplace product; platform is SaaS paid product. Same-repo conflates them.
- **Paid-tier pattern** — user stated (2026-04-19) "paid projects own their git, free projects live in subtree". Three infrastructure tiers (plugin, platform, bootstrapped projects) deserve three repo realms.

Phase 5.5 cost verified as ~2–5 min (not 45 min — `gh auth status` showed existing OAuth token for `myconciergerie-prog` with `admin:public_key` + `repo` + `workflow` + `delete_repo` scopes) because the `gh` CLI already has the right token cached.

### Q4 — Deploy target: **OVH VPS** (fallback: Cloudflare Pages)

Per user intent "commencer sur le VPS en prod". The VPS is provisioned but not yet running at spec time; the deploy pipeline must tolerate this. Plan:

- Landing served by nginx on VPS, same machine that will host Supabase migration later.
- `production` branch pattern (verified on sibling projects `atelier-playmobil-james-west` and `aurum_ai`): `main` = source, `production` = built `dist/` pushed by CI or local deploy script, nginx serves from `production` branch checkout or rsync target.
- DNS: OVH DNS `A genesis` → VPS IP, or `CNAME genesis` → fallback if Cloudflare Pages is used while VPS is being provisioned.
- HTTPS: certbot on VPS (Let's Encrypt), or Cloudflare auto-HTTPS for fallback path.

**Fallback contingency**: if the VPS is not provisioned/configured by the time the landing is ready to ship, the deploy target switches to Cloudflare Pages (zero-setup, free tier, custom domain via `CNAME`). Migration from Cloudflare Pages → VPS later is ~20 min (rsync `dist/`, repoint DNS).

### Q5 — Language: **Bilingual FR + EN auto-detect + toggle**

Per Layer 0 R9 three-tier language policy. Detection via `navigator.language` — `fr-*` renders French, anything else renders English. User override via header toggle (FR | EN), persisted in `localStorage`. String bundles: `src/i18n/fr.json`, `src/i18n/en.json`, helper `t(key)`. ~30–50 strings total for MVL scope.

### Q6 — Auth: **Supabase Auth (new cloud project "Genesis")** + **magic-link** + **Google OAuth**

**Q6a — New Supabase project.** Verified via MCP that no Genesis Supabase project exists yet (three projects listed: Myconciergerie, Cyrano INACTIVE, atelier-playmobil-james-west). Create dedicated "Genesis" project in organization `laaxlkdscxntajtjzcve`, region `eu-west-2` for consistency with siblings. Free tier (50K MAU). Self-hosted migration to VPS Supabase planned for later, but that's a single-project export/import operation, not a refactor.

**Q6b — Both auth methods.** Both Google OAuth + magic-link offered in the modal, user chooses per sign-in. Supabase Auth supports both natively; ~45 min total config (Google Cloud OAuth client + Supabase Email provider template customization).

**Q6c — Post-auth `/welcome` micro-dashboard**. Not a bare placeholder — includes provider badge, platform status card, empty-state project list (future-anchor for sub-project #2), secondary CTAs (Discord / Changelog / GitHub), and sign-out. Shell that sub-project #2 will fill with real drop-zone entry.

## 4. Visual design direction

All ten mockup files persist in `.claude/worktrees/feat_2026-04-20_v3_0_sub1_landing/.superpowers/brainstorm/76763-1776631640/` as ground truth (`visual-direction`, `hybrid-ab`, `refined-b`, `full-landing-fr`, `dev-band-geek`, `dev-band-manga`, `dev-band-manga-light`, `final-landing-assembled`, `auth-modal`, `welcome-dashboard`). Key decisions:

### Palette

| Use | Value |
|---|---|
| Background (hero / picker / footer) | `#faf8f5` cream |
| Background (dev band) | `#f4f1eb` (tonal shift, 3 shades darker than hero) |
| Text primary | `#1a1a1a` |
| Text secondary | `#555` – `#666` |
| Brand accent | `#6b4fff` violet |
| Status active | `#10b981` emerald |
| Status beta / coming | `#f59e0b` amber |
| Ink (dev band manga) | `#0f0f12` black |
| Card disabled bg | `#f4f1eb` + `#e8e4dc` borders |
| Accent triangles (dev band) | `#6b4fff` / `#0891b2` / `#10b981` / `#ec4899` / `#f59e0b` |

### Typography

- **Body sans**: system stack — `-apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif`. No Google Fonts (zero extra network requests, zero CLS from font swap).
- **Monospace**: `ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace`. Used for meta-data (versions, codes, dev band labels).
- **DEV STATS heading**: `font-weight: 900`, `letter-spacing: -0.02em`, `text-shadow: 3px 3px 0 #6b4fff` — Latin equivalent of manga chunky lettering.
- **Hero headline**: 36 px display weight 700 `letter-spacing: -0.025em`.
- **Picker card label**: 14 px weight 700.
- **Status badge**: 10 px weight 600 mono.

### Layout

- **Hero / picker / footer**: centered, max-width 560 px content area.
- **Picker cards**: 108 × 108 px square, `border-radius: 18px`, flex-row centered, gap 14 px. Anthropic card has `border: 2px solid #6b4fff` + violet shadow. Gemini / OpenAI: 1 px gray border, `opacity: 0.55`.
- **Dev band**: collapsible. Default state = teaser bar only (`>> TU CODES ? … DEV STATS ↓`). Click expands bento 3×2 + halftone + speed lines. State persisted in `localStorage`.
- **DEV STATS bento**: 3 columns × 2 rows, `gap: 9px`. Each card: `background: #fff`, `border: 2.5px solid #0f0f12`, clip-path triangle corner color-coded per category. `PLATFORM · PAID` card (6th) has `border: 3.5px solid #6b4fff`, `box-shadow: 4px 4px 0 #0f0f12` (manga chunky offset shadow), radial-dot halftone background, and corner "PAID" badge with its own drop-shadow.
- **Auth modal**: centered over backdrop `rgba(15,15,18,0.45)` + `backdrop-filter: blur(4px)`. Card 320 px max-width, `border-radius: 24px`, shadow `0 20px 60px rgba(0,0,0,0.25)`. Two states: initial (Google + divider + email + submit) / magic-link-sent (📧 icon + 3-step explainer + resend CTA + back link).
- **Welcome page**: 680 px max-width. Header authed (avatar + email + FR/EN + menu). Hero with emerald status line + "Bonjour {name}". 2-column config cards (AI Provider + Platform Status). Empty-state card 🌱 with dashed border. 3 pill CTAs. Footer with sign-out link.

### Visual devices (dev band)

- **Speed lines**: 4 diagonal lines skew-Y -2deg, opacity 0.35, positioned top-left of dev band.
- **Halftone**: `background-image: radial-gradient(#0f0f12 1.5px, transparent 1.5px); background-size: 8px 8px; opacity: 0.15`, positioned top-right.
- **Dashed dividers**: `repeating-linear-gradient(90deg, #0f0f12 0, #0f0f12 12px, transparent 12px, transparent 20px)` (chunky manga-panel feel, not CSS `border: dashed`).
- **Clip-path triangles**: `clip-path: polygon(100% 0, 0 0, 100% 100%)` on card corners, color-coded per category.
- **Latin geometric accents**: `▲ ◆ ★ ✦ ⬡ ◉` — zero Japanese characters (per user clarification — style applied à l'européenne, pas les caractères).

## 5. Repo structure

```
myconciergerie-prog/genesis-web/       # sibling repo, new
├── .github/
│   └── workflows/
│       └── deploy-production.yml      # main → build → push to production → SSH rsync to VPS
├── .gitignore                         # node_modules, dist, .superpowers, .env.local
├── index.html                         # Vite entry
├── package.json                       # version independent of plugin
├── tsconfig.json
├── vite.config.ts
├── public/
│   └── favicon.svg
├── src/
│   ├── main.ts                        # entry — mounts app into #app
│   ├── router.ts                      # minimal routing: /, /auth/callback, /welcome
│   ├── i18n/
│   │   ├── detect.ts                  # navigator.language → fr|en
│   │   ├── t.ts                       # translation helper
│   │   ├── fr.json
│   │   └── en.json
│   ├── auth/
│   │   ├── supabase.ts                # Supabase client singleton
│   │   ├── sign-in.ts                 # Google OAuth + magic-link handlers
│   │   ├── callback.ts                # /auth/callback handler
│   │   └── session.ts                 # session state observer
│   ├── components/
│   │   ├── header.ts                  # logo + FR/EN toggle + avatar-if-authed
│   │   ├── hero.ts                    # landing hero
│   │   ├── picker.ts                  # 3 provider cards + state
│   │   ├── dev-band.ts                # collapsible bento with localStorage state
│   │   ├── auth-modal.ts              # 2-state modal (initial / sent)
│   │   ├── welcome-hero.ts            # authed hero with emerald status line
│   │   ├── config-cards.ts            # provider + platform cards
│   │   ├── empty-state.ts             # projects empty-state
│   │   └── footer.ts                  # footer with sign-out if authed
│   ├── pages/
│   │   ├── landing.ts                 # composes header + hero + picker + dev-band + footer
│   │   ├── welcome.ts                 # composes authed header + welcome-hero + config-cards + empty-state + CTAs + footer
│   │   └── callback.ts                # handles OAuth callback, redirects to /welcome
│   └── styles/
│       ├── tokens.css                 # CSS custom properties (palette, type scale, spacing)
│       ├── reset.css                  # minimal reset
│       ├── components.css             # all component styles keyed by data-component attribute
│       └── dev-band.css               # manga accents (halftone, speed-lines, clip-path triangles)
└── README.md                          # setup, dev, build, deploy
```

### File-size discipline

Per Layer 0 R11 size budget awareness: no single `.ts` file should exceed 200 lines. If a component grows beyond that, split (e.g., `picker.ts` + `picker-card.ts`). Rationale: each file has one purpose, one test target, one diff surface.

## 6. Data flow

### Unauth landing

```
Browser → genesis.myconciergerie.fr
  → GET / (static HTML + JS bundle)
  → main.ts mounts landing.ts
  → header.ts reads navigator.language + localStorage.locale → render FR|EN
  → picker.ts renders 3 cards — Anthropic active, others disabled
  → dev-band.ts reads localStorage.devBandOpen → collapsed|expanded
  → User clicks CTA "Obtenir l'accès anticipé" OR Anthropic card
  → auth-modal.ts mounts with provider=anthropic in context
```

### Auth: magic-link

```
Modal state 1 → user enters email → clicks "Recevoir le lien"
  → sign-in.ts calls supabase.auth.signInWithOtp({
      email,
      options: {
        emailRedirectTo: `${origin}/auth/callback`,
        data: { provider_preference: "anthropic" }
      }
    })
  → Supabase sends email with magic link
  → Modal transitions to state 2 (📧 sent)
User opens email on any device → clicks link
  → Browser lands on /auth/callback?token=...&type=magiclink
  → callback.ts exchanges token → session cookie
  → redirect to /welcome
```

### Auth: Google OAuth

```
Modal state 1 → user clicks "Continuer avec Google"
  → sign-in.ts calls supabase.auth.signInWithOAuth({
      provider: "google",
      options: {
        redirectTo: `${origin}/auth/callback`,
        queryParams: { provider_preference: "anthropic" }
      }
    })
  → Browser redirects to accounts.google.com/o/oauth2/auth?...
  → User consents (one tap for signed-in Google users)
  → Google redirects to Supabase → Supabase redirects to /auth/callback
  → callback.ts exchanges code → session cookie
  → redirect to /welcome
```

### Welcome page

```
Browser → /welcome
  → main.ts detects path → mounts welcome.ts
  → session.ts asks supabase.auth.getSession()
    → No session → redirect to / with ?auth=expired banner
    → Session present → proceed
  → welcome.ts reads auth.user.user_metadata.provider_preference → render provider card
  → config-cards.ts renders AI Provider + Platform Status
  → empty-state.ts renders projects placeholder
  → secondary CTAs and footer with sign-out wire
```

### Locale toggle

```
User clicks FR/EN toggle in header
  → localStorage.locale = "fr"|"en"
  → i18n.t rebinds → DOM text nodes re-render
  → Same-page update, no navigation
```

### Dev band toggle

```
User clicks teaser bar
  → localStorage.devBandOpen = !current
  → dev-band.ts toggles class `expanded` on container
  → CSS max-height transition reveals/collapses bento
```

## 7. Error handling

### Auth errors

| Condition | Handling |
|---|---|
| Email invalid / rate-limited | Modal stays at state 1, inline error under input, Supabase error code mapped to localized message via `ERR_*` pattern (Layer 0 `pattern_api_error_code_stable_i18n.md`) |
| Google OAuth denied by user | Return to landing with subtle toast "Connexion annulée" |
| Google OAuth network failure | Modal stays at state 1, inline error "Réseau indisponible, réessaye" |
| Magic-link expired | `/auth/callback?error=expired` → redirect to `/?auth=expired` with banner explaining + CTA to restart |
| Magic-link reused | Supabase returns error → same handling as expired |
| Supabase down | Modal disabled CTA, inline error "Service temporairement indisponible" |

### Runtime errors

| Condition | Handling |
|---|---|
| `localStorage` unavailable (private browsing) | Fallback to in-memory state; toggle still works in-session, resets on reload |
| `navigator.language` not `fr*`/`en*` | Default to EN |
| JS disabled | Render the hero, picker, footer as static HTML; dev band stays collapsed; auth modal replaced with plain mailto as last-resort CTA |
| Image load failure (none in scope — no images in MVL) | N/A |

### Fallback chain — CTA if auth fails

If Supabase Auth is unreachable at session open, the CTA degrades gracefully:

1. Primary: Google OAuth + magic-link (Supabase Auth) — normal path.
2. Fallback tier 1: Supabase down → CTA becomes `mailto:genesis@myconciergerie.fr?subject=Early%20access` — user can still express intent via email.
3. Fallback tier 2: JS disabled → static HTML `<a href="mailto:...">` present in initial page source.

## 8. Testing strategy

### Automated

| Layer | Tool | Coverage |
|---|---|---|
| Unit | Vitest | `i18n.t` + `detectLocale` + `session` state observer + `picker` state transitions + `devBand` toggle |
| Integration | Vitest + Playwright MCP | Auth modal state transitions; magic-link flow mocked; Google OAuth mocked via Supabase stub |
| E2E | Playwright | Real signup against a throwaway Supabase test project; sign-in with test email; assert redirect to /welcome |
| Visual regression | Playwright screenshot + pixelmatch | Full landing FR, full landing EN, dev band expanded, auth modal state 1, auth modal state 2, welcome page |

### Manual

| Scenario | Who | Frequency |
|---|---|---|
| Dogfood sign-in flow with real Google account | Claude as developer | Once per implementation phase |
| Dogfood magic-link on phone (tap link in email → redirect) | Claude in dev | Once before ship |
| Locale toggle persistence across page reload | Claude | Once before ship |
| Dev band collapse persistence across session | Claude | Once before ship |
| Accessibility smoke (keyboard-only navigation) | Claude | Once before ship |

## 9. Implementation phases

Each phase is landable as its own PR and its own tag. Phases are sequential — each depends on the preceding one.

### Phase 1 — Repo setup (`genesis-web v0.0.1`)

- Run Phase 5.5 auth-preflight for `myconciergerie-prog/genesis-web`:
  - `ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519_genesis-web`
  - Add `Host github.com-genesis-web` alias to `~/.ssh/config`
  - `gh ssh-key add` via cached `myconciergerie-prog` OAuth token
  - `gh repo create myconciergerie-prog/genesis-web --private`
- Run Vite scaffold: `npm create vite@latest . -- --template vanilla-ts`.
- **Prune the scaffold output** to match Section 5 layout: delete default `src/main.ts`, `src/style.css`, `src/counter.ts`, `src/typescript.svg`, and the scaffold's `index.html` boilerplate. Replace with empty placeholders matching the target tree (`src/main.ts` stub, `src/styles/tokens.css` empty, etc.). This prevents two conflicting sources of truth for entry files.
- Initial commit: pruned scaffold + target file tree (empty placeholders) + `.gitignore` (node_modules, dist, .superpowers, .env.local) + SPDX headers + README skeleton.
- Tag `v0.0.1`, push to both `main` and `production` initial branches.

### Phase 2 — Static landing visual (`v0.1.0`)

- Implement `src/styles/tokens.css` + `reset.css` + `components.css`.
- Implement `src/components/header.ts`, `hero.ts`, `picker.ts`, `footer.ts`.
- Implement `src/pages/landing.ts` composing the above.
- No i18n yet — French-only hardcoded to unblock visual review.
- Local dev `npm run dev` + manual dogfood against `final-landing-assembled.html` mockup.
- Tag `v0.1.0`.

### Phase 3 — i18n system (`v0.2.0`)

- Implement `src/i18n/detect.ts` + `t.ts` + `fr.json` + `en.json`.
- Refactor hardcoded strings in Phase 2 components to `t(key)`.
- Header FR/EN toggle with `localStorage` persistence.
- Dogfood: load in FR browser, switch to EN via toggle, reload, verify persistence.
- Tag `v0.2.0`.

### Phase 4 — Dev band collapsible (`v0.3.0`)

- Implement `src/components/dev-band.ts` with bento 3×2, halftone, speed lines, clip-path triangles.
- Collapsible with `localStorage.devBandOpen` persistence.
- Implement `src/styles/dev-band.css` with manga accents.
- Dogfood: click teaser, click again, reload, verify state.
- Tag `v0.3.0`.

### Phase 5 — Supabase project + Auth config (`v0.4.0`)

- Create Supabase project "Genesis" via MCP (`create_project` tool), free tier, region `eu-west-2`, organization `laaxlkdscxntajtjzcve`.
- Enable magic-link provider in Supabase Auth config.
- Configure Google OAuth provider (Google Cloud Console client creation, client ID + secret into Supabase).
- Customize magic-link email template (FR + EN versions via Supabase Auth Email Templates).
- Record Supabase project URL + anon key in `memory/reference/supabase_genesis_project.md` of the `genesis-web` repo (not in env, memory only — anon key is public-safe).
- `.env.local` (gitignored) gets `VITE_SUPABASE_URL` + `VITE_SUPABASE_ANON_KEY`.
- Tag `v0.4.0` (backend config, no code ship beyond `.env.example`).

### Phase 6 — Auth modal + wire CTAs (`v0.5.0`)

- Implement `src/auth/supabase.ts` singleton.
- Implement `src/auth/sign-in.ts` with Google OAuth + magic-link helpers.
- Implement `src/components/auth-modal.ts` with 2 states.
- Wire CTA hero + Anthropic picker card → open modal with `provider=anthropic` context.
- Dogfood: real Google sign-in in a test environment, real magic-link to a test email, verify redirect to `/auth/callback`.
- Tag `v0.5.0`.

### Phase 7 — Auth callback + `/welcome` page (`v0.6.0`)

- Implement `src/auth/callback.ts` to exchange OAuth code / magic-link token → session.
- Implement `src/auth/session.ts` observer.
- Implement `src/router.ts` minimal routing for `/`, `/auth/callback`, `/welcome`.
- Implement `src/components/welcome-hero.ts`, `config-cards.ts`, `empty-state.ts`.
- Implement `src/pages/welcome.ts` composing the authed header + above.
- Wire sign-out button in footer.
- Dogfood: full flow from landing → sign-in → callback → welcome → sign-out → landing.
- Tag `v0.6.0`.

### Phase 8 — Production deploy (`v1.0.0`)

- **VPS-side SSH deploy key setup** (before any push): generate dedicated deploy keypair on VPS (`ssh-keygen -t ed25519 -f ~/.ssh/id_genesis_web_deploy`), add public key as a read-only deploy key in `genesis-web` repo settings (GitHub → Settings → Deploy keys), add matching entry to GitHub Actions `SSH_PRIVATE_KEY` secret for rsync destination, test passwordless SSH from Actions runner to VPS. This is a prerequisite for the deploy workflow below.
- Write `.github/workflows/deploy-production.yml` — on push to `main`: `npm ci && npm run build`, checkout `production` branch, commit `dist/` contents, push; rsync `dist/` to `/var/www/genesis/` on VPS via SSH.
- Alternative pipeline (if VPS not ready): connect Cloudflare Pages to the repo, deploy from `main`.
- Create OVH DNS record: `A genesis → VPS_IP` (or `CNAME` to Cloudflare Pages).
- Provision Let's Encrypt cert on VPS via certbot + nginx server block for `genesis.myconciergerie.fr`.
- End-to-end smoke test: real sign-in on `https://genesis.myconciergerie.fr`.
- **Axe-core accessibility smoke** run in CI against the production build (or deploy preview): fail the pipeline on any critical/serious issues. This satisfies acceptance criterion #11.
- Tag `v1.0.0` — first public shippable version.

## 10. MCP tools needed during implementation

For reference during plan writing and execution (per Layer 0 `feedback_spec_writing_discipline_mcp_first_reviewer_gate.md` — MCP schema awareness).

### Supabase MCP

| Tool | Use |
|---|---|
| `list_organizations` | Confirm target org ID (already run — `laaxlkdscxntajtjzcve`) |
| `list_projects` | Verify no existing Genesis project (already run) |
| `create_project` | Phase 5 — create "Genesis" project |
| `get_project_url` | Phase 5 — retrieve URL to populate `.env.local` |
| `get_publishable_keys` | Phase 5 — retrieve anon key |
| `get_advisors` | Phase 5 post-create — security + performance lint |
| `list_extensions` | Phase 5 — verify `pgcrypto` / auth defaults |
| `get_logs` | Debugging auth failures in Phases 6–8 (Layer 0 `feedback_postgres_logs_first_check.md`) |

### Playwright MCP

| Tool | Use |
|---|---|
| `browser_navigate` + `browser_snapshot` | Dogfood every phase against corresponding mockup |
| `browser_fill_form` + `browser_click` | E2E sign-in test Phase 6–7 |
| `browser_console_messages` + `browser_network_requests` | Debugging auth callback failures |

## 11. Open questions / deferred decisions

These are explicit non-decisions for this spec. Each will be resolved in a later sub-project or dedicated brainstorming session.

| # | Question | When | Notes |
|---|---|---|---|
| 1 | What is the first paid tier price? | Sub-project #6+ | Pricing page absent from MVL by design |
| 2 | Discord / Twitter / Changelog — which actually exists now? | **Phase 2 entry gate** (must be answered before the footer is wired, not a Phase 2 deliverable) | Placeholder CTAs in footer; if none ready, replace with single "Email us" |
| 3 | Is the VPS actually running when Phase 8 kicks off? | Before Phase 8 | If not, Cloudflare Pages fallback is the path; update this spec with outcome |
| 4 | GitHub OAuth as a third sign-in method? | v3.1+ | Not in MVL; consider when developer tier matures |
| 5 | Analytics solution (Plausible / umami / GA4 / none) | Sub-project #2 | Zero analytics in sub-project #1 by design (fewer vendor decisions to unwind) |
| 6 | Typography upgrade to custom font (e.g., Inter / Söhne) | Post-v1.0 | System stack is fine for MVL; visual upgrade is risk-free later |

## 12. Risks and mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| VPS not ready for Phase 8 | Medium | Medium | Cloudflare Pages fallback documented; 20-min migration later |
| Google OAuth client config drift between dev/prod | Medium | Low | Document exact authorized origins in `memory/reference/google_oauth_config.md` of `genesis-web` repo |
| Supabase free tier MAU limit hit | Low | Medium | 50K MAU is ample for MVL + early beta; monitor via Supabase dashboard |
| Magic-link email in spam folder | High | Low | "Check spam" in state 2 copy; template customization with DKIM/SPF via Supabase Auth settings |
| Locale detection misfires (e.g., Canadian French `fr-CA`) | Medium | Low | Match on `fr*` prefix; if user toggles, persist |
| DNS propagation delay at cutover | Low | Low | TTL to 300 s ahead of cutover; monitor |
| User types `genesis.myconciergerie.fr` before DNS is set | Medium | Low | Pre-configure DNS before the domain is announced externally |

## 13. Honesty axis (5-axis self-rating — pre-flight projection)

Projected v1.0.0 self-rating (per Genesis R10 self-rating discipline):

| Axis | Projection | Reasoning |
|---|---|---|
| **Pain-driven** | 8.0 | Genuine user-facing need (entry point for v3 vision), not speculative |
| **Prose cleanliness** | 8.5 | Spec is long but sectioned; no dead prose; mockups are the ground truth |
| **Best-at-date** | 8.5 | Vite + Supabase Auth + VPS OVH are 2026 mature choices; R8 cache backs each |
| **Self-contained** | 8.5 | Sibling repo is self-contained; all external deps pinned; no magic |
| **Anti-Frankenstein** | 9.0 | Explicit scope boundary; roadmap labelled as roadmap; fallback path documented |
| **Average projection** | **8.5** | Target hit |

Self-rating will be re-evaluated honestly at `v1.0.0` commit per Layer 0 `feedback_honest_self_rating_post_feat.md` — willingness to drop ≥ 0.5 if reality differs from projection.

## 14. Related work

- **master.md § "What v3 vision is"** — the strategic context this spec implements.
- **`.claude/docs/superpowers/specs/2026-04-19-v2-bootstrap-via-max-subscription-design.md`** — v2 dropped subprocess Citations API, relevant because the web mode re-introduces a subprocess equivalent server-side; this spec is the first CLI-boundary where the platform needs its own auth strategy distinct from `claude auth status`.
- **Layer 0 `infra_2026-04-18_supabase_vps_ovh_migration.md`** — VPS Supabase migration plan that will eventually host the Genesis Supabase project after cloud → self-host migration.
- **Layer 0 `feedback_ovh_git_ssh_not_https.md`** — OVH Git connector rules (applies if fallback is OVH shared hosting instead of VPS).
- **All 10 mockup files** in `.claude/worktrees/feat_2026-04-20_v3_0_sub1_landing/.superpowers/brainstorm/76763-1776631640/` — visual ground truth.

## 15. Acceptance criteria for v1.0.0

v1.0.0 of `genesis-web` ships when all the following are true:

1. `https://genesis.myconciergerie.fr` resolves and serves the landing over HTTPS.
2. The hero + picker + dev band + footer render correctly in FR and EN at desktop (1280 px) and mobile (375 px) viewport widths.
3. FR/EN toggle persists across page reload via `localStorage`.
4. Dev band collapse state persists across page reload via `localStorage`.
5. Clicking the hero CTA opens the auth modal in < 100 ms.
6. Google OAuth sign-in completes end-to-end to `/welcome`.
7. Magic-link sign-in completes end-to-end: submit email, receive email, click link, land on `/welcome`.
8. `/welcome` shows the user's email, provider badge (Anthropic), platform status, and empty-state.
9. Sign-out returns to landing and clears session.
10. All Playwright E2E tests pass on CI.
11. Axe-core accessibility smoke returns zero critical issues.
12. CHANGELOG entry with 5-axis self-rating ≥ 8.0 per axis honest.
