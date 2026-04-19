<!-- SPDX-License-Identifier: MIT -->
# Genesis v3.0 sub-project #1 — Landing + Provider Picker Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship a bilingual (FR+EN) landing page at `https://genesis.myconciergerie.fr` with a BYOAI provider picker (Anthropic active, Gemini/OpenAI staged), magic-link + Google OAuth sign-in via self-hosted Supabase on VPS OVH, and a `/welcome` post-auth micro-dashboard — as `v1.0.0` of the new `genesis-web` sibling repo.

**Architecture:** Vite + vanilla TypeScript SPA with file-based component composition, static output deployed to OVH VPS via rsync over SSH from GitHub Actions on push to `main`. Auth backend is self-hosted Supabase (Docker Compose stack) on the same VPS, exposed at `https://supabase.myconciergerie.fr` behind nginx reverse proxy. Magic-link email delivery via OVH webmail SMTP (`ssl0.ovh.net:465`) from `noreply@myconciergerie.fr`, inheriting existing SPF/DKIM for deliverability. Landing is collapsible into two visual zones: consumer-warm (hero/picker) and dev-manga (collapsible DEV STATS band).

**Tech Stack:**
- **Frontend:** Vite 6+, TypeScript 5+, system sans + `ui-monospace` fonts (no custom webfonts in v1.0.0)
- **Auth:** `@supabase/supabase-js` v2+ against self-hosted GoTrue
- **i18n:** Custom `t()` helper + 2 JSON bundles (FR/EN), `navigator.language` detection + `localStorage` persistence
- **Test:** Vitest for unit tests, Playwright for E2E + visual regression
- **Infra:** Docker Compose for Supabase, nginx + certbot for TLS, OVH DNS
- **CI/CD:** GitHub Actions on push to `main` → build → push `dist/` to `production` branch → rsync to VPS

**Reference documents (read before starting):**
- Spec: `.claude/docs/superpowers/specs/2026-04-19-v3-sub1-landing-design.md` — single source of truth for all decisions
- Mockups: `.claude/worktrees/feat_2026-04-20_v3_0_sub1_landing/.superpowers/brainstorm/76763-1776631640/` — 10 HTML files, visual ground truth
- master.md § "What v3 vision is" — strategic context
- Layer 0 hard rules (R2.1 worktrees, R8 cache, R9 language policy) — always applicable

**Skill composition this plan uses:**
- @superpowers:test-driven-development — every component has a test written FIRST
- @superpowers:verification-before-completion — every acceptance claim backed by evidence
- @superpowers:systematic-debugging — when auth/deploy issues surface
- @superpowers:using-git-worktrees — all work happens inside the worktree

---

## Scope boundary reminder

This plan delivers v1.0.0 of the `genesis-web` landing-page artifact. **Out of scope:** drop-zone UI (sub-project #2), project extraction pipeline (sub-project #3), deploy pipeline for user projects (#4), user dashboards (#5), paid-tier billing (#6+). If a task tempts scope creep beyond the acceptance criteria in Section 15 of the spec, STOP and raise with the user.

---

## Global file structure

Target repo = `myconciergerie-prog/genesis-web` (created in Phase 1, does NOT exist at plan start).

```
genesis-web/
├── .env.example                    # VITE_SUPABASE_URL + VITE_SUPABASE_ANON_KEY placeholders
├── .gitignore                      # node_modules/ dist/ .env.local .superpowers/
├── .github/
│   └── workflows/
│       └── deploy-production.yml   # Phase 8 — build + rsync deploy
├── LICENSE                         # MIT, added Phase 1
├── README.md                       # setup + dev + build + deploy, iterated each phase
├── CHANGELOG.md                    # per-tag 5-axis self-rating log
├── index.html                      # Vite entry (pruned from scaffold, Phase 1)
├── package.json                    # name "genesis-web", version tracks tags
├── tsconfig.json                   # strict TS, target ES2022
├── vite.config.ts                  # minimal, emits to dist/
├── vitest.config.ts                # happy-dom env for unit tests
├── playwright.config.ts            # chromium+firefox, base URL from env
├── public/
│   └── favicon.svg                 # minimal "◆" glyph, violet #6b4fff
├── memory/
│   ├── MEMORY.md                   # genesis-web project memory index
│   └── reference/
│       └── supabase_genesis_selfhost.md  # VPS endpoint + anon key + runbook
├── src/
│   ├── main.ts                     # entry — router mount
│   ├── router.ts                   # hash or history routing for /, /auth/callback, /welcome
│   ├── i18n/
│   │   ├── detect.ts               # navigator.language + localStorage → "fr"|"en"
│   │   ├── t.ts                    # t(key) helper + reactive rebind
│   │   ├── fr.json                 # French strings
│   │   └── en.json                 # English strings
│   ├── auth/
│   │   ├── supabase.ts             # client singleton from env
│   │   ├── sign-in.ts              # signInWithOAuth + signInWithOtp helpers
│   │   ├── callback.ts             # exchange code/token → session
│   │   └── session.ts              # getSession + observer
│   ├── components/
│   │   ├── header.ts               # logo + FR/EN toggle + avatar-if-authed
│   │   ├── hero.ts                 # centered hero + CTA pill
│   │   ├── picker.ts               # 3 provider cards row
│   │   ├── dev-band.ts             # collapsible bento 3×2 + manga accents
│   │   ├── auth-modal.ts           # 2-state modal (initial / sent)
│   │   ├── welcome-hero.ts         # authed hero with status line
│   │   ├── config-cards.ts         # provider + platform status cards
│   │   ├── empty-state.ts          # projects placeholder 🌱
│   │   └── footer.ts               # footer with sign-out if authed
│   ├── pages/
│   │   ├── landing.ts              # composes unauth landing
│   │   ├── welcome.ts              # composes authed welcome
│   │   └── callback.ts             # handles /auth/callback
│   └── styles/
│       ├── tokens.css              # CSS custom props (palette, type, spacing)
│       ├── reset.css               # minimal reset
│       ├── components.css          # component styles
│       └── dev-band.css            # manga accents (halftone, clip-path, shadow)
└── tests/
    ├── unit/
    │   ├── i18n.detect.test.ts
    │   ├── i18n.t.test.ts
    │   ├── auth.session.test.ts
    │   └── components.picker-state.test.ts
    └── e2e/
        ├── landing-fr.spec.ts
        ├── landing-en.spec.ts
        ├── auth-magic-link.spec.ts
        ├── auth-google-oauth.spec.ts
        ├── welcome.spec.ts
        └── visual-regression.spec.ts
```

---

## Phase 1 — Repo setup (`v0.0.1`)

**Goal:** `myconciergerie-prog/genesis-web` exists on GitHub with an initial Vite-TS scaffold pruned to match the target file tree, plus MIT license and SPDX headers.

**Estimated wall-clock:** 45–60 min.

### Task 1.1: Phase 5.5 auth-preflight for genesis-web

**Files:**
- Create: `~/.ssh/id_ed25519_genesis-web` (outside repo)
- Create: `~/.ssh/id_ed25519_genesis-web.pub` (outside repo)
- Modify: `~/.ssh/config` (append new host alias block)
- Create: `myconciergerie-prog/genesis-web` on GitHub (via `gh repo create`)

- [ ] **Step 1: Verify `gh auth status` includes `myconciergerie-prog` account with `admin:public_key` + `repo` scopes**

Run: `gh auth status`
Expected: output lists `myconciergerie-prog` with scopes including `admin:public_key`, `repo`, `workflow`, `delete_repo`. If missing scopes → STOP and surface; do not try to add scopes silently.

- [ ] **Step 2: Switch active gh account to `myconciergerie-prog`**

Run: `gh auth switch --user myconciergerie-prog`
Expected: `✓ Switched active account for github.com to myconciergerie-prog`

- [ ] **Step 3: Generate dedicated ed25519 SSH key**

Run:
```bash
ssh-keygen -t ed25519 -f "$HOME/.ssh/id_ed25519_genesis-web" -C "genesis-web@myconciergerie-prog" -N ""
```
Expected: two files created, no error. **Private key must never leave local machine.**

- [ ] **Step 4: Add SSH host alias to `~/.ssh/config`**

Append (idempotent — grep first, skip if already present):
```
Host github.com-genesis-web
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_ed25519_genesis-web
  IdentitiesOnly yes
```

Verify:
```bash
grep -c "Host github.com-genesis-web" ~/.ssh/config
```
Expected: `1`.

- [ ] **Step 5: Upload public SSH key to GitHub via CLI**

Run:
```bash
gh ssh-key add "$HOME/.ssh/id_ed25519_genesis-web.pub" --title "genesis-web" --type authentication
```
Expected: `✓ Public key added to your account`.

- [ ] **Step 6: Test SSH binding**

Run:
```bash
ssh -T -o StrictHostKeyChecking=accept-new git@github.com-genesis-web
```
Expected output (exit code 1 is normal — GitHub closes session after auth success):
```
Hi myconciergerie-prog! You've successfully authenticated, but GitHub does not provide shell access.
```
If it says a different username → the key is bound to wrong account; STOP, investigate.

- [ ] **Step 7: Create empty GitHub repo via `gh`**

Run:
```bash
gh repo create myconciergerie-prog/genesis-web --private --description "Genesis web platform — landing + provider picker + auth for genesis.myconciergerie.fr"
```
Expected: `✓ Created repository myconciergerie-prog/genesis-web on GitHub`.

- [ ] **Step 8: Verify repo exists + is empty**

Run:
```bash
gh api repos/myconciergerie-prog/genesis-web --jq '.name, .private, .size'
```
Expected: `genesis-web`, `true`, `0`.

- [ ] **Step 9: Commit memory/reference entry for the SSH identity**

Create `C:/Dev/Claude_cowork/project-genesis/.claude/worktrees/feat_2026-04-20_v3_0_sub1_landing/memory/reference/ssh_genesis_web_identity.md` following the pattern of `memory/reference/ssh_genesis_identity.md`. Include fingerprint (from `ssh-keygen -lf`), alias, remote URL, pre-flight test output.

Then commit in the worktree:
```bash
cd C:/Dev/Claude_cowork/project-genesis/.claude/worktrees/feat_2026-04-20_v3_0_sub1_landing
git add memory/reference/ssh_genesis_web_identity.md
git commit -m "docs(memory): SSH identity for genesis-web sibling repo"
```

### Task 1.2: Local clone + Vite TS scaffold

**Files:**
- Create: new dir `C:/Dev/Claude_cowork/genesis-web/` (outside project-genesis)
- Create: all Vite TS scaffold files in that dir

- [ ] **Step 1: Clone the new empty repo locally**

Run:
```bash
cd C:/Dev/Claude_cowork
git clone git@github.com-genesis-web:myconciergerie-prog/genesis-web.git
cd genesis-web
```
Expected: `warning: You appear to have cloned an empty repository.`

- [ ] **Step 2: Run Vite scaffold inside the clone**

Run:
```bash
npm create vite@latest . -- --template vanilla-ts
```
Respond to prompts: confirm adding to non-empty directory = yes. Template: vanilla-ts (already selected via flag).
Expected: scaffold files appear (`index.html`, `src/main.ts`, `src/counter.ts`, `src/style.css`, `src/typescript.svg`, `package.json`, `tsconfig.json`, `vite.config.ts` absent by default — vanilla template uses `tsconfig.json` only; add `vite.config.ts` in Step 5).

- [ ] **Step 3: Install deps**

Run: `npm install`
Expected: `node_modules/` appears, no `ERROR` in output (warnings are fine).

- [ ] **Step 4: Run dev server to verify scaffold works**

Run: `npm run dev`
Expected: Vite starts at `http://localhost:5173`, page shows "Vite + TypeScript" + counter button. Open browser, click counter, verify increments. Kill dev server (Ctrl+C).

- [ ] **Step 5: Prune scaffold to target tree**

Delete:
```bash
rm src/counter.ts src/typescript.svg src/style.css
```

Replace `src/main.ts` with an empty placeholder:
```ts
// SPDX-License-Identifier: MIT
// Entry point for genesis-web. Router mount happens here (Phase 7).
```

Replace `index.html` content with:
```html
<!doctype html>
<html lang="fr">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Genesis — myconciergerie</title>
    <meta name="description" content="De l'idée au projet déployé, avec Claude. / From idea to deployed project, Claude-native." />
  </head>
  <body>
    <div id="app"></div>
    <script type="module" src="/src/main.ts"></script>
  </body>
</html>
```

Create `vite.config.ts`:
```ts
// SPDX-License-Identifier: MIT
import { defineConfig } from 'vite';

export default defineConfig({
  build: {
    outDir: 'dist',
    sourcemap: true,
  },
  server: {
    port: 5173,
  },
});
```

- [ ] **Step 6: Create target directory skeleton with empty placeholders**

Run:
```bash
mkdir -p src/i18n src/auth src/components src/pages src/styles public memory/reference tests/unit tests/e2e .github/workflows
```

Add an empty `.gitkeep` to each subdirectory that won't get content in Phase 1:
```bash
touch src/i18n/.gitkeep src/auth/.gitkeep src/components/.gitkeep src/pages/.gitkeep src/styles/.gitkeep tests/unit/.gitkeep tests/e2e/.gitkeep .github/workflows/.gitkeep
```

- [ ] **Step 7: Create favicon (minimal violet diamond)**

Create `public/favicon.svg`:
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16"><rect x="4" y="4" width="8" height="8" transform="rotate(45 8 8)" fill="#6b4fff"/></svg>
```

- [ ] **Step 8: Verify dev server still works after pruning**

Run: `npm run dev`
Expected: starts at `http://localhost:5173`, page loads (empty body — no errors in console). Kill dev server.

### Task 1.3: License, gitignore, SPDX, README skeleton

**Files:**
- Create: `LICENSE`, `.gitignore`, `README.md`, `CHANGELOG.md`

- [ ] **Step 1: Add MIT LICENSE**

Create `LICENSE` with standard MIT text, copyright `2026 myconciergerie` (full standard 21-line MIT template).

- [ ] **Step 2: Create `.gitignore`**

Create with:
```
node_modules/
dist/
.env.local
.env.*.local
.superpowers/
.vite/
*.log
.DS_Store
```

- [ ] **Step 3: Create `README.md` skeleton**

```markdown
<!-- SPDX-License-Identifier: MIT -->
# genesis-web

Landing page + provider picker + platform auth for `https://genesis.myconciergerie.fr`. Sibling of the [Project Genesis](https://github.com/myconciergerie-prog/project-genesis) Claude Code plugin.

## Stack

Vite + vanilla TypeScript + self-hosted Supabase on VPS OVH. Bilingual FR+EN. See `.claude/docs/superpowers/specs/2026-04-19-v3-sub1-landing-design.md` in the parent project-genesis repo for full design.

## Dev

```bash
npm install
npm run dev        # http://localhost:5173
npm run build      # outputs dist/
npm test           # vitest unit tests
npm run test:e2e   # playwright E2E tests
```

## Deploy

Push to `main` triggers GitHub Action that builds and pushes to `production` branch, then rsyncs `dist/` to the VPS. See `.github/workflows/deploy-production.yml`.

## License

MIT — see `LICENSE`.
```

- [ ] **Step 4: Create `CHANGELOG.md` skeleton**

```markdown
# Changelog

Version log with 5-axis self-rating (pain-driven / prose cleanliness / best-at-date / self-contained / anti-Frankenstein).

## v0.0.1 — 2026-04-20

Initial scaffold. Vite + vanilla-ts template pruned to target tree. Phase 5.5 auth pre-flight completed. No runtime code yet.

Self-rating axis: N/A (scaffold only).
```

- [ ] **Step 5: Add SPDX header to every `.ts` and `.css` file in the target tree**

Every file Claude creates in this plan starts with:
```
// SPDX-License-Identifier: MIT
```
(or `<!-- SPDX-License-Identifier: MIT -->` for HTML/MD).

- [ ] **Step 6: Commit initial scaffold**

```bash
git add .
git commit -m "feat: initial vite-ts scaffold pruned to target tree

Phase 1 Task 1.2-1.3 — initial genesis-web repo with:
- Vite 6 + TypeScript strict
- Pruned vanilla-ts template (no counter, no svg, no default CSS)
- Target directory skeleton with .gitkeep placeholders
- MIT LICENSE + SPDX headers across all source files
- .gitignore, README, CHANGELOG skeleton
- Minimal favicon.svg

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

- [ ] **Step 7: Push to GitHub and set upstream**

Run:
```bash
git branch -M main
git push -u origin main
```
Expected: branch `main` tracks `origin/main`. Run `gh repo view --web` to open repo in browser; verify files appear.

- [ ] **Step 8: Create `production` branch as orphan pointing at same initial commit**

```bash
git checkout --orphan production
git rm -rf . 2>/dev/null || true
git clean -fdx
echo "# Production build output" > README.md
echo "This branch holds the built \`dist/\` pushed by CI from main. Do not push manually." >> README.md
git add README.md
git commit -m "chore: initialize production branch as orphan

Empty branch that CI will populate with built dist/ on push to main."
git push -u origin production
git checkout main
```
Expected: `production` branch exists on origin with only `README.md`.

- [ ] **Step 9: Tag `v0.0.1`**

```bash
git tag -a v0.0.1 -m "v0.0.1 — initial scaffold"
git push origin v0.0.1
```

---

## Phase 2 — Static landing visual (`v0.1.0`)

**Goal:** Landing page renders statically at desktop + mobile with hero + picker + footer. French-only copy hardcoded. No i18n yet, no auth yet, no dev band yet.

**Estimated wall-clock:** 2–3h.

### Task 2.1: Install test infrastructure

**Files:**
- Modify: `package.json` (add dev deps + scripts)
- Create: `vitest.config.ts`, `playwright.config.ts`

- [ ] **Step 1: Install Vitest + happy-dom + Playwright**

```bash
npm install -D vitest happy-dom @playwright/test
npx playwright install chromium firefox
```

- [ ] **Step 2: Create `vitest.config.ts`**

```ts
// SPDX-License-Identifier: MIT
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    environment: 'happy-dom',
    include: ['tests/unit/**/*.test.ts'],
    globals: true,
  },
});
```

- [ ] **Step 3: Create `playwright.config.ts`**

```ts
// SPDX-License-Identifier: MIT
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  reporter: 'html',
  use: {
    baseURL: process.env.PLAYWRIGHT_BASE_URL || 'http://localhost:5173',
    trace: 'on-first-retry',
  },
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:5173',
    reuseExistingServer: !process.env.CI,
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
  ],
});
```

- [ ] **Step 4: Add npm scripts**

Edit `package.json` scripts section:
```json
"scripts": {
  "dev": "vite",
  "build": "tsc -b && vite build",
  "preview": "vite preview",
  "test": "vitest run",
  "test:watch": "vitest",
  "test:e2e": "playwright test",
  "test:e2e:ui": "playwright test --ui"
}
```

- [ ] **Step 5: Commit test infra**

```bash
git add package.json package-lock.json vitest.config.ts playwright.config.ts
git commit -m "chore: install vitest + playwright test infra

Phase 2 Task 2.1 — test harness ready for TDD development."
```

### Task 2.2: CSS tokens + reset

**Files:**
- Create: `src/styles/tokens.css`, `src/styles/reset.css`

- [ ] **Step 1: Create `src/styles/tokens.css`** (the palette + type + spacing primitives from spec Section 4)

```css
/* SPDX-License-Identifier: MIT */
:root {
  /* Palette */
  --color-bg: #faf8f5;
  --color-bg-band: #f4f1eb;
  --color-text: #1a1a1a;
  --color-text-muted: #555;
  --color-text-subtle: #888;
  --color-border: #e8e4dc;
  --color-border-subtle: rgba(232, 228, 220, 0.6);
  --color-brand: #6b4fff;
  --color-brand-soft: #a5b4fc;
  --color-success: #10b981;
  --color-beta: #f59e0b;
  --color-ink: #0f0f12;
  --color-white: #fff;

  /* Accent triangles */
  --color-accent-runtime: #6b4fff;
  --color-accent-stack: #0891b2;
  --color-accent-license: #10b981;
  --color-accent-plugin: #ec4899;
  --color-accent-providers: #f59e0b;

  /* Type */
  --font-sans: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
  --font-mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;

  /* Type scale */
  --fs-xs: 10px;
  --fs-sm: 11px;
  --fs-base: 12px;
  --fs-body: 13px;
  --fs-body-lg: 15px;
  --fs-hero: 36px;
  --fs-display: 28px;

  /* Spacing */
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 20px;
  --space-6: 24px;
  --space-8: 32px;
  --space-10: 40px;
  --space-12: 48px;

  /* Shadows */
  --shadow-cta: 0 4px 14px rgba(107, 79, 255, 0.22);
  --shadow-picker-active: 0 4px 14px rgba(107, 79, 255, 0.14);
  --shadow-modal: 0 20px 60px rgba(0, 0, 0, 0.25);
  --shadow-manga-offset: 4px 4px 0 var(--color-ink);
}
```

- [ ] **Step 2: Create `src/styles/reset.css`**

```css
/* SPDX-License-Identifier: MIT */
*, *::before, *::after { box-sizing: border-box; }
html, body { margin: 0; padding: 0; }
body {
  font-family: var(--font-sans);
  background: var(--color-bg);
  color: var(--color-text);
  -webkit-font-smoothing: antialiased;
  text-rendering: optimizeLegibility;
}
button { font-family: inherit; cursor: pointer; background: none; border: none; padding: 0; }
a { color: inherit; text-decoration: none; }
img { max-width: 100%; display: block; }
```

- [ ] **Step 3: Create `src/styles/components.css`** with empty placeholder + SPDX header (will fill in Task 2.3-2.5)

```css
/* SPDX-License-Identifier: MIT */
/* Component styles — populated per task in Phase 2. */
```

- [ ] **Step 4: Import styles from `src/main.ts`**

Replace `src/main.ts` with:
```ts
// SPDX-License-Identifier: MIT
import './styles/tokens.css';
import './styles/reset.css';
import './styles/components.css';

// Phase 2 Task 2.3+: render landing page here.
document.getElementById('app')!.textContent = 'Phase 2 WIP';
```

- [ ] **Step 5: Verify dev server renders**

`npm run dev` → open `http://localhost:5173` → see "Phase 2 WIP" on cream background with system font. No console errors. Kill server.

- [ ] **Step 6: Commit tokens + reset**

```bash
git add src/styles/ src/main.ts
git commit -m "feat(styles): tokens + reset CSS

Phase 2 Task 2.2 — CSS custom properties for palette, type, spacing,
shadows per spec Section 4. Reset.css applies system font and cream
background globally."
```

### Task 2.3: Header component

**Files:**
- Create: `src/components/header.ts`, `tests/unit/components.header.test.ts`
- Modify: `src/styles/components.css`, `src/main.ts`

- [ ] **Step 1: Write the failing test**

Create `tests/unit/components.header.test.ts`:
```ts
// SPDX-License-Identifier: MIT
import { describe, it, expect } from 'vitest';
import { renderHeader } from '../../src/components/header';

describe('Header', () => {
  it('renders Genesis logo + FR/EN toggle', () => {
    const el = renderHeader();
    expect(el.querySelector('[data-component="logo"]')?.textContent).toContain('Genesis');
    expect(el.querySelectorAll('[data-component="locale-toggle"] button').length).toBe(2);
  });
  it('marks FR as active when locale="fr"', () => {
    const el = renderHeader({ locale: 'fr' });
    const btnFr = el.querySelector<HTMLButtonElement>('[data-locale="fr"]');
    expect(btnFr?.getAttribute('aria-pressed')).toBe('true');
  });
});
```

- [ ] **Step 2: Run test to verify failure**

Run: `npm test tests/unit/components.header.test.ts`
Expected: FAIL — `renderHeader` not defined.

- [ ] **Step 3: Implement `src/components/header.ts`**

```ts
// SPDX-License-Identifier: MIT
export interface HeaderOptions {
  locale?: 'fr' | 'en';
}

export function renderHeader(opts: HeaderOptions = {}): HTMLElement {
  const locale = opts.locale ?? 'fr';
  const el = document.createElement('header');
  el.className = 'site-header';
  el.innerHTML = `
    <span data-component="logo" class="site-header__logo">◆ Genesis</span>
    <div data-component="locale-toggle" class="locale-toggle">
      <button data-locale="fr" aria-pressed="${locale === 'fr'}">FR</button>
      <button data-locale="en" aria-pressed="${locale === 'en'}">EN</button>
    </div>
  `;
  return el;
}
```

- [ ] **Step 4: Append component styles to `src/styles/components.css`**

```css
.site-header {
  display: flex; justify-content: space-between; align-items: center;
  padding: var(--space-4) var(--space-8);
  border-bottom: 1px solid var(--color-border-subtle);
}
.site-header__logo {
  font-weight: 700; color: var(--color-brand);
  font-size: 16px; letter-spacing: -0.01em;
}
.locale-toggle { display: flex; gap: 2px; font-size: var(--fs-base); }
.locale-toggle button {
  padding: 3px 10px; color: var(--color-text-subtle); border-radius: 12px;
}
.locale-toggle button[aria-pressed="true"] {
  color: var(--color-text); font-weight: 600;
  background: var(--color-white); border: 1px solid var(--color-border);
}
```

- [ ] **Step 5: Run test, verify PASS**

Run: `npm test tests/unit/components.header.test.ts`
Expected: 2 tests passed.

- [ ] **Step 6: Wire header into `main.ts` for visual check**

Replace `main.ts` body (keep imports):
```ts
import { renderHeader } from './components/header';
const app = document.getElementById('app')!;
app.appendChild(renderHeader({ locale: 'fr' }));
```

- [ ] **Step 7: Visual dogfood vs mockup**

`npm run dev`. Open `http://localhost:5173`. Compare header to the `final-landing-assembled.html` mockup header. Must match: logo left, FR/EN toggle right, cream bg, violet logo. Kill server.

- [ ] **Step 8: Commit**

```bash
git add src/components/header.ts tests/unit/components.header.test.ts src/styles/components.css src/main.ts
git commit -m "feat(components): Header with logo + FR/EN locale toggle

Phase 2 Task 2.3 — bilingual-aware header per spec Section 4. Test
covers render + aria-pressed state."
```

### Task 2.4: Hero component

**Files:**
- Create: `src/components/hero.ts`, `tests/unit/components.hero.test.ts`
- Modify: `src/styles/components.css`, `src/main.ts`

- [ ] **Step 1: Write the failing test**

Create `tests/unit/components.hero.test.ts`:
```ts
// SPDX-License-Identifier: MIT
import { describe, it, expect } from 'vitest';
import { renderHero } from '../../src/components/hero';

describe('Hero', () => {
  it('renders headline, subhead, CTA', () => {
    const el = renderHero({
      headline: 'De l\'idée au projet\ndéployé, avec Claude.',
      subhead: 'Décrivez votre projet.',
      ctaLabel: 'Obtenir l\'accès anticipé →',
    });
    expect(el.querySelector('h1')?.textContent).toContain('idée');
    expect(el.querySelector('[data-component="subhead"]')?.textContent).toContain('Décrivez');
    expect(el.querySelector<HTMLButtonElement>('[data-component="cta"]')?.textContent).toContain('anticipé');
  });
  it('CTA click fires onCtaClick handler', () => {
    let clicked = false;
    const el = renderHero({
      headline: 'x', subhead: 'y', ctaLabel: 'z',
      onCtaClick: () => { clicked = true; },
    });
    el.querySelector<HTMLButtonElement>('[data-component="cta"]')!.click();
    expect(clicked).toBe(true);
  });
});
```

- [ ] **Step 2: Run test to verify failure**

Run: `npm test tests/unit/components.hero.test.ts`
Expected: FAIL.

- [ ] **Step 3: Implement `src/components/hero.ts`**

```ts
// SPDX-License-Identifier: MIT
export interface HeroOptions {
  headline: string;
  subhead: string;
  ctaLabel: string;
  onCtaClick?: () => void;
}

export function renderHero(opts: HeroOptions): HTMLElement {
  const el = document.createElement('section');
  el.className = 'hero';
  const headlineHtml = opts.headline.split('\n').join('<br>');
  el.innerHTML = `
    <h1 class="hero__headline">${headlineHtml}</h1>
    <p data-component="subhead" class="hero__subhead">${opts.subhead}</p>
    <button data-component="cta" class="hero__cta">${opts.ctaLabel}</button>
  `;
  if (opts.onCtaClick) {
    el.querySelector('[data-component="cta"]')!.addEventListener('click', opts.onCtaClick);
  }
  return el;
}
```

- [ ] **Step 4: Append hero styles to `src/styles/components.css`**

```css
.hero {
  text-align: center;
  padding: 60px var(--space-8) 44px;
}
.hero__headline {
  font-size: var(--fs-hero);
  font-weight: 700;
  line-height: 1.08;
  letter-spacing: -0.025em;
  margin: 0 0 var(--space-4);
  color: var(--color-text);
}
.hero__subhead {
  font-size: var(--fs-body-lg);
  color: var(--color-text-muted);
  margin: 0 auto var(--space-8);
  max-width: 480px;
  line-height: 1.5;
}
.hero__cta {
  display: inline-block;
  background: var(--color-brand);
  color: var(--color-white);
  padding: 13px 24px;
  font-size: 15px;
  font-weight: 600;
  border-radius: 32px;
  box-shadow: var(--shadow-cta);
  transition: transform 0.1s ease;
}
.hero__cta:hover { transform: translateY(-1px); }
.hero__cta:active { transform: translateY(0); }
```

- [ ] **Step 5: Run test, verify PASS**

Run: `npm test tests/unit/components.hero.test.ts`
Expected: 2 tests passed.

- [ ] **Step 6: Wire hero into `main.ts`, visual dogfood, kill server, commit**

Update `main.ts` to append `renderHero` after header with FR copy from spec Section 4. Verify visually vs mockup. Commit:
```bash
git add src/components/hero.ts tests/unit/components.hero.test.ts src/styles/components.css src/main.ts
git commit -m "feat(components): Hero with headline, subhead, CTA

Phase 2 Task 2.4 — centered hero per final-landing-assembled mockup."
```

### Task 2.5: Picker component

**Files:**
- Create: `src/components/picker.ts`, `tests/unit/components.picker.test.ts`, `tests/unit/components.picker-state.test.ts`
- Modify: `src/styles/components.css`, `src/main.ts`

- [ ] **Step 1: Write the failing tests**

Create `tests/unit/components.picker.test.ts`:
```ts
// SPDX-License-Identifier: MIT
import { describe, it, expect } from 'vitest';
import { renderPicker } from '../../src/components/picker';

describe('Picker', () => {
  it('renders 3 provider cards', () => {
    const el = renderPicker({ activeProvider: 'anthropic', statusLabels: { active: 'Disponible', comingSoon: 'Bientôt' } });
    expect(el.querySelectorAll('[data-component="provider-card"]').length).toBe(3);
  });
  it('Anthropic card is marked active, others disabled', () => {
    const el = renderPicker({ activeProvider: 'anthropic', statusLabels: { active: 'Disponible', comingSoon: 'Bientôt' } });
    const anthropic = el.querySelector<HTMLElement>('[data-provider="anthropic"]');
    const gemini = el.querySelector<HTMLElement>('[data-provider="gemini"]');
    expect(anthropic?.classList.contains('provider-card--active')).toBe(true);
    expect(gemini?.classList.contains('provider-card--disabled')).toBe(true);
  });
  it('Anthropic click fires onProviderClick with "anthropic"', () => {
    let clicked = '';
    const el = renderPicker({
      activeProvider: 'anthropic',
      statusLabels: { active: 'Disponible', comingSoon: 'Bientôt' },
      onProviderClick: (p) => { clicked = p; },
    });
    el.querySelector<HTMLElement>('[data-provider="anthropic"]')!.click();
    expect(clicked).toBe('anthropic');
  });
  it('disabled card click is ignored', () => {
    let clicked = '';
    const el = renderPicker({
      activeProvider: 'anthropic',
      statusLabels: { active: 'Disponible', comingSoon: 'Bientôt' },
      onProviderClick: (p) => { clicked = p; },
    });
    el.querySelector<HTMLElement>('[data-provider="gemini"]')!.click();
    expect(clicked).toBe('');
  });
});
```

- [ ] **Step 2: Run test to verify failure**

Run: `npm test tests/unit/components.picker.test.ts`
Expected: FAIL.

- [ ] **Step 3: Implement `src/components/picker.ts`**

```ts
// SPDX-License-Identifier: MIT
export type Provider = 'anthropic' | 'gemini' | 'openai';

export interface PickerOptions {
  activeProvider: Provider;
  statusLabels: { active: string; comingSoon: string };
  headingLabel?: string;
  onProviderClick?: (provider: Provider) => void;
}

const PROVIDER_ORDER: Provider[] = ['anthropic', 'gemini', 'openai'];
const PROVIDER_NAMES: Record<Provider, string> = {
  anthropic: 'Anthropic', gemini: 'Gemini', openai: 'OpenAI',
};

export function renderPicker(opts: PickerOptions): HTMLElement {
  const el = document.createElement('section');
  el.className = 'picker';
  const heading = opts.headingLabel ?? 'Choisis ton AI';
  const cards = PROVIDER_ORDER.map((p) => {
    const isActive = p === opts.activeProvider;
    const label = isActive ? opts.statusLabels.active : opts.statusLabels.comingSoon;
    const classes = ['provider-card', isActive ? 'provider-card--active' : 'provider-card--disabled'];
    return `
      <button
        data-component="provider-card"
        data-provider="${p}"
        class="${classes.join(' ')}"
        ${isActive ? '' : 'disabled'}
      >
        <div class="provider-card__name">${PROVIDER_NAMES[p]}</div>
        <div class="provider-card__status">${isActive ? '● ' : ''}${label}</div>
      </button>
    `;
  }).join('');
  el.innerHTML = `
    <div class="picker__heading">${heading}</div>
    <div class="picker__cards">${cards}</div>
  `;
  if (opts.onProviderClick) {
    el.querySelectorAll<HTMLElement>('[data-component="provider-card"]:not([disabled])').forEach((card) => {
      card.addEventListener('click', () => {
        const provider = card.getAttribute('data-provider') as Provider;
        opts.onProviderClick!(provider);
      });
    });
  }
  return el;
}
```

- [ ] **Step 4: Append picker styles**

```css
.picker { padding: var(--space-5) var(--space-8) 60px; }
.picker__heading {
  font-size: var(--fs-sm);
  color: var(--color-text-subtle);
  text-align: center;
  margin-bottom: 18px;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  font-weight: 600;
}
.picker__cards {
  display: flex;
  justify-content: center;
  gap: 14px;
}
.provider-card {
  width: 108px; height: 108px;
  border-radius: 18px;
  display: flex; flex-direction: column; justify-content: center;
  padding: 18px 10px; text-align: center;
  background: var(--color-white);
  border: 2px solid transparent;
  transition: transform 0.1s ease;
}
.provider-card:hover:not([disabled]) { transform: translateY(-2px); }
.provider-card--active {
  border-color: var(--color-brand);
  box-shadow: var(--shadow-picker-active);
}
.provider-card--disabled {
  background: var(--color-bg-band);
  border: 1px solid var(--color-border);
  opacity: 0.55;
  cursor: not-allowed;
}
.provider-card__name {
  font-size: 14px; font-weight: 700; color: var(--color-text);
}
.provider-card--disabled .provider-card__name { color: var(--color-text-subtle); font-weight: 600; }
.provider-card__status {
  font-size: var(--fs-xs); color: var(--color-success);
  margin-top: 6px; font-weight: 600;
}
.provider-card--disabled .provider-card__status { color: var(--color-text-subtle); }
```

- [ ] **Step 5: Run tests, verify PASS**

Run: `npm test tests/unit/components.picker.test.ts`
Expected: 4 tests passed.

- [ ] **Step 6: Wire into `main.ts`, visual dogfood vs mockup, commit**

```bash
git add src/components/picker.ts tests/unit/components.picker.test.ts src/styles/components.css src/main.ts
git commit -m "feat(components): Picker with 3 provider cards

Phase 2 Task 2.5 — Anthropic active, Gemini/OpenAI disabled per
BYOAI staging. Callback fires only for active provider."
```

### Task 2.6: Footer component

**Files:**
- Create: `src/components/footer.ts`, `tests/unit/components.footer.test.ts`
- Modify: `src/styles/components.css`, `src/main.ts`

- [ ] **Step 1: Write the failing test**

Create `tests/unit/components.footer.test.ts`:
```ts
// SPDX-License-Identifier: MIT
import { describe, it, expect } from 'vitest';
import { renderFooter } from '../../src/components/footer';

describe('Footer', () => {
  it('renders copyright + 3 link placeholders', () => {
    const el = renderFooter();
    expect(el.textContent).toContain('© 2026 Genesis');
    expect(el.querySelectorAll('[data-component="footer-link"]').length).toBe(3);
  });
});
```

- [ ] **Step 2: Run test, verify failure.** (`npm test tests/unit/components.footer.test.ts` → FAIL)

- [ ] **Step 3: Implement `src/components/footer.ts`**

```ts
// SPDX-License-Identifier: MIT
export function renderFooter(): HTMLElement {
  const el = document.createElement('footer');
  el.className = 'site-footer';
  el.innerHTML = `
    <span>© 2026 Genesis · by myconciergerie</span>
    <div class="site-footer__links">
      <a data-component="footer-link" href="#contact">Contact</a>
      <a data-component="footer-link" href="https://github.com/myconciergerie-prog/project-genesis">GitHub</a>
      <a data-component="footer-link" href="#privacy">Privacy</a>
    </div>
  `;
  return el;
}
```

- [ ] **Step 4: Append footer styles**

```css
.site-footer {
  padding: var(--space-6) var(--space-8);
  display: flex; justify-content: space-between; align-items: center;
  font-size: var(--fs-sm); color: var(--color-text-subtle);
  border-top: 1px solid var(--color-border-subtle);
}
.site-footer__links { display: flex; gap: 18px; }
.site-footer__links a { cursor: pointer; }
```

- [ ] **Step 5: Run test, verify PASS.**

- [ ] **Step 6: Wire footer + compose landing page** into `main.ts`:

```ts
// SPDX-License-Identifier: MIT
import './styles/tokens.css';
import './styles/reset.css';
import './styles/components.css';
import { renderHeader } from './components/header';
import { renderHero } from './components/hero';
import { renderPicker } from './components/picker';
import { renderFooter } from './components/footer';

const app = document.getElementById('app')!;
app.appendChild(renderHeader({ locale: 'fr' }));
app.appendChild(renderHero({
  headline: "De l'idée au projet\ndéployé, avec Claude.",
  subhead: "Décrivez votre projet. Genesis extrait, code, teste et déploie — sans quitter votre browser.",
  ctaLabel: "Obtenir l'accès anticipé →",
  onCtaClick: () => console.log('CTA clicked — modal not yet implemented'),
}));
app.appendChild(renderPicker({
  activeProvider: 'anthropic',
  statusLabels: { active: 'Disponible', comingSoon: 'Bientôt' },
  onProviderClick: (p) => console.log(`Provider picked: ${p}`),
}));
app.appendChild(renderFooter());
```

- [ ] **Step 7: Visual dogfood vs `final-landing-assembled.html` mockup** — dev server, side-by-side browser compare. Adjust CSS if spacing differs visibly (but do not restyle — match mockup).

- [ ] **Step 8: Commit + tag `v0.1.0`**

```bash
git add .
git commit -m "feat: full static landing FR — header + hero + picker + footer

Phase 2 complete — v0.1.0. French-only hardcoded copy per scope.
No i18n yet (Phase 3), no dev band (Phase 4), no auth (Phase 5-7).
Visual matches final-landing-assembled mockup within ~5 px tolerance."

git tag -a v0.1.0 -m "v0.1.0 — static landing FR"
git push origin main v0.1.0
```

---

## Phase 3 — i18n system (`v0.2.0`)

**Goal:** `navigator.language` detection + `localStorage` persistence + FR/EN toggle actually switches strings. `fr.json` and `en.json` contain all landing strings.

**Estimated wall-clock:** 1.5–2h.

### Task 3.1: Locale detection + persistence

**Files:**
- Create: `src/i18n/detect.ts`, `tests/unit/i18n.detect.test.ts`

- [ ] **Step 1: Write the failing test**

```ts
// SPDX-License-Identifier: MIT
import { describe, it, expect, beforeEach } from 'vitest';
import { detectLocale, setLocale, getStoredLocale } from '../../src/i18n/detect';

describe('detectLocale', () => {
  beforeEach(() => { localStorage.clear(); });

  it('returns stored value when present', () => {
    localStorage.setItem('locale', 'en');
    expect(detectLocale('fr-FR')).toBe('en');
  });
  it('returns "fr" when navigator.language starts with fr', () => {
    expect(detectLocale('fr-FR')).toBe('fr');
    expect(detectLocale('fr-CA')).toBe('fr');
    expect(detectLocale('fr')).toBe('fr');
  });
  it('returns "en" for anything else', () => {
    expect(detectLocale('en-US')).toBe('en');
    expect(detectLocale('de-DE')).toBe('en');
    expect(detectLocale('ja')).toBe('en');
  });
  it('setLocale + getStoredLocale round-trip', () => {
    setLocale('en');
    expect(getStoredLocale()).toBe('en');
    setLocale('fr');
    expect(getStoredLocale()).toBe('fr');
  });
});
```

- [ ] **Step 2: Run test, verify FAIL.** Run: `npm test tests/unit/i18n.detect.test.ts`.

- [ ] **Step 3: Implement `src/i18n/detect.ts`**

```ts
// SPDX-License-Identifier: MIT
export type Locale = 'fr' | 'en';
const STORAGE_KEY = 'locale';

export function detectLocale(navLang: string = navigator.language): Locale {
  const stored = getStoredLocale();
  if (stored) return stored;
  return navLang.toLowerCase().startsWith('fr') ? 'fr' : 'en';
}

export function setLocale(locale: Locale): void {
  try {
    localStorage.setItem(STORAGE_KEY, locale);
  } catch { /* private browsing — fallback to in-memory only */ }
}

export function getStoredLocale(): Locale | null {
  try {
    const v = localStorage.getItem(STORAGE_KEY);
    return v === 'fr' || v === 'en' ? v : null;
  } catch { return null; }
}
```

- [ ] **Step 4: Run tests, PASS. Commit.**
```bash
git add src/i18n/detect.ts tests/unit/i18n.detect.test.ts
git commit -m "feat(i18n): locale detection + localStorage persistence

Phase 3 Task 3.1 — navigator.language fr* → fr, else en. Override
via setLocale persists to localStorage; graceful fallback on private
browsing where storage throws."
```

### Task 3.2: `t()` helper + FR/EN bundles

**Files:**
- Create: `src/i18n/fr.json`, `src/i18n/en.json`, `src/i18n/t.ts`, `tests/unit/i18n.t.test.ts`

- [ ] **Step 1: Define the string keys all components need**

Create `src/i18n/fr.json`:
```json
{
  "site": {
    "title": "Genesis"
  },
  "hero": {
    "headline": "De l'idée au projet\ndéployé, avec Claude.",
    "subhead": "Décrivez votre projet. Genesis extrait, code, teste et déploie — sans quitter votre browser.",
    "cta": "Obtenir l'accès anticipé →"
  },
  "picker": {
    "heading": "Choisis ton AI",
    "statusActive": "Disponible",
    "statusComingSoon": "Bientôt"
  },
  "footer": {
    "copyright": "© 2026 Genesis · by myconciergerie",
    "contact": "Contact",
    "github": "GitHub",
    "privacy": "Privacy"
  }
}
```

Create `src/i18n/en.json`:
```json
{
  "site": {
    "title": "Genesis"
  },
  "hero": {
    "headline": "From idea to deployed\nproject, Claude-native.",
    "subhead": "Describe your project. Genesis extracts, codes, tests, deploys — all in your browser.",
    "cta": "Get early access →"
  },
  "picker": {
    "heading": "Pick your AI",
    "statusActive": "Active",
    "statusComingSoon": "Coming soon"
  },
  "footer": {
    "copyright": "© 2026 Genesis · by myconciergerie",
    "contact": "Contact",
    "github": "GitHub",
    "privacy": "Privacy"
  }
}
```

- [ ] **Step 2: Write the failing test for `t()`**

```ts
// SPDX-License-Identifier: MIT
import { describe, it, expect } from 'vitest';
import { t, setBundleLocale } from '../../src/i18n/t';

describe('t', () => {
  it('returns FR string when locale is fr', () => {
    setBundleLocale('fr');
    expect(t('hero.cta')).toContain('Obtenir');
  });
  it('returns EN string when locale is en', () => {
    setBundleLocale('en');
    expect(t('hero.cta')).toContain('Get early access');
  });
  it('returns the key itself for unknown keys', () => {
    setBundleLocale('fr');
    expect(t('does.not.exist')).toBe('does.not.exist');
  });
});
```

- [ ] **Step 3: Run test, FAIL.**

- [ ] **Step 4: Implement `src/i18n/t.ts`**

```ts
// SPDX-License-Identifier: MIT
import fr from './fr.json';
import en from './en.json';
import type { Locale } from './detect';

type Bundle = typeof fr;
const BUNDLES: Record<Locale, Bundle> = { fr, en };
let currentLocale: Locale = 'fr';

export function setBundleLocale(locale: Locale): void {
  currentLocale = locale;
}

export function t(key: string): string {
  const parts = key.split('.');
  let node: unknown = BUNDLES[currentLocale];
  for (const part of parts) {
    if (node && typeof node === 'object' && part in (node as Record<string, unknown>)) {
      node = (node as Record<string, unknown>)[part];
    } else { return key; }
  }
  return typeof node === 'string' ? node : key;
}
```

- [ ] **Step 5: Add `"resolveJsonModule": true` to `tsconfig.json` compilerOptions** if not already present.

- [ ] **Step 6: Run test, PASS. Commit.**
```bash
git add src/i18n/fr.json src/i18n/en.json src/i18n/t.ts tests/unit/i18n.t.test.ts tsconfig.json
git commit -m "feat(i18n): t() helper + FR/EN string bundles

Phase 3 Task 3.2 — JSON-based bundles, dot-path key lookup, graceful
fallback returns key on miss."
```

### Task 3.3: Refactor components to use `t()` + wire toggle

**Files:**
- Modify: `src/components/header.ts`, `hero.ts`, `picker.ts`, `footer.ts`
- Modify: `src/main.ts`
- Create: `tests/e2e/landing-fr.spec.ts`, `tests/e2e/landing-en.spec.ts`

- [ ] **Step 1: Update each component to call `t()` for string content, accepting no hardcoded labels**

Example for `hero.ts`:
```ts
import { t } from '../i18n/t';
export function renderHero(opts: { onCtaClick?: () => void } = {}): HTMLElement {
  // ... read t('hero.headline'), t('hero.subhead'), t('hero.cta')
}
```
Repeat for `header`, `picker`, `footer`. Pass no copy through props (bundle is canonical).

- [ ] **Step 2: Update all affected component tests** to not pass copy props (they now read from bundles).

- [ ] **Step 3: In `main.ts`, wire locale detection + toggle**

```ts
// SPDX-License-Identifier: MIT
import './styles/tokens.css';
import './styles/reset.css';
import './styles/components.css';
import { detectLocale, setLocale } from './i18n/detect';
import { setBundleLocale } from './i18n/t';
import { renderHeader } from './components/header';
import { renderHero } from './components/hero';
import { renderPicker } from './components/picker';
import { renderFooter } from './components/footer';

function renderApp() {
  const locale = detectLocale();
  setBundleLocale(locale);
  document.documentElement.lang = locale;

  const app = document.getElementById('app')!;
  app.innerHTML = '';
  const header = renderHeader({ locale });
  header.querySelectorAll<HTMLElement>('[data-locale]').forEach((btn) => {
    btn.addEventListener('click', () => {
      const next = btn.getAttribute('data-locale') as 'fr' | 'en';
      setLocale(next);
      renderApp(); // re-render
    });
  });
  app.appendChild(header);
  app.appendChild(renderHero({ onCtaClick: () => console.log('CTA') }));
  app.appendChild(renderPicker({
    activeProvider: 'anthropic',
    onProviderClick: (p) => console.log(p),
  }));
  app.appendChild(renderFooter());
}
renderApp();
```
Note: `renderHero` + `renderPicker` signatures change to no longer take copy in opts — they read from `t()`.

- [ ] **Step 4: Playwright E2E test `tests/e2e/landing-fr.spec.ts`**

```ts
// SPDX-License-Identifier: MIT
import { test, expect } from '@playwright/test';

test('landing renders in FR by default on fr-FR browser', async ({ browser }) => {
  const context = await browser.newContext({ locale: 'fr-FR' });
  const page = await context.newPage();
  await page.goto('/');
  await expect(page.locator('h1')).toContainText('idée');
  await expect(page.locator('.hero__cta')).toContainText('anticipé');
  await expect(page.locator('[data-provider="anthropic"] .provider-card__status')).toContainText('Disponible');
});

test('toggle to EN switches all strings', async ({ browser }) => {
  const context = await browser.newContext({ locale: 'fr-FR' });
  const page = await context.newPage();
  await page.goto('/');
  await page.locator('[data-locale="en"]').click();
  await expect(page.locator('h1')).toContainText('idea');
  await expect(page.locator('.hero__cta')).toContainText('Get early access');
  await expect(page.locator('[data-provider="anthropic"] .provider-card__status')).toContainText('Active');
});

test('locale persists across reload', async ({ browser }) => {
  const context = await browser.newContext({ locale: 'fr-FR' });
  const page = await context.newPage();
  await page.goto('/');
  await page.locator('[data-locale="en"]').click();
  await page.reload();
  await expect(page.locator('h1')).toContainText('idea');
});
```

- [ ] **Step 5: Playwright test `landing-en.spec.ts`** for `en-US` default:
```ts
// SPDX-License-Identifier: MIT
import { test, expect } from '@playwright/test';
test('landing renders EN by default on en-US', async ({ browser }) => {
  const context = await browser.newContext({ locale: 'en-US' });
  const page = await context.newPage();
  await page.goto('/');
  await expect(page.locator('h1')).toContainText('idea');
});
```

- [ ] **Step 6: Run full test suite**

Run: `npm test && npm run test:e2e`
Expected: unit tests PASS, E2E tests PASS.

- [ ] **Step 7: Commit + tag `v0.2.0`**

```bash
git add .
git commit -m "feat(i18n): wire FR/EN detection, toggle, persistence across landing

Phase 3 complete — v0.2.0. navigator.language → FR if fr*, else EN.
Header toggle persists via localStorage. Playwright E2E validates all
three flows."
git tag -a v0.2.0 -m "v0.2.0 — bilingual landing"
git push origin main v0.2.0
```

---

## Phase 4 — Dev band collapsible (`v0.3.0`)

**Goal:** Collapsible DEV STATS band rendered under picker, persisted open/closed state via localStorage, manga accents (halftone, speed lines, clip-path triangles, offset shadow on PAID card).

**Estimated wall-clock:** 2–3h.

### Task 4.1: Dev band state + bundle strings

**Files:**
- Modify: `src/i18n/fr.json`, `src/i18n/en.json` (add `devBand` namespace)
- Create: `src/components/dev-band.ts`, `tests/unit/components.dev-band.test.ts`

- [ ] **Step 1: Extend FR/EN bundles**

Add to `fr.json`:
```json
"devBand": {
  "teaserPrompt": ">> TU CODES ?",
  "teaserCta": "DEV STATS ↓",
  "teaserCtaOpen": "DEV STATS ↑",
  "heading": "DEV STATS",
  "tagline": "// Pour qui code et veut que ça convertisse sans friction",
  "buildLabel": "build",
  "liveLabel": "LIVE",
  "cards": {
    "runtime": { "label": "▲ RUNTIME", "title": "Claude 4.7", "meta": "Opus · 1M ctx" },
    "stack": { "label": "◆ STACK", "title": "Vite · TS", "meta": "Supabase · VPS" },
    "license": { "label": "★ LICENSE", "title": "MIT · Open", "meta": "→ GitHub repo" },
    "plugin": { "label": "✦ PLUGIN CLI", "title": "v2.0.0", "meta": "9 skills · β" },
    "providers": { "label": "⬡ PROVIDERS", "title": "Anthropic", "meta": "Gemini ⏸ / OpenAI ⏸" },
    "platform": { "label": "◉ PLATFORM", "title": "API · Webhooks", "meta": "Domain · Teams · ROADMAP", "badge": "PAID" }
  },
  "links": { "github": "→ GitHub", "marketplace": "→ Marketplace Anthropic", "docs": "→ Docs" }
}
```

And equivalent EN version in `en.json` (translate "TU CODES ?" → "DEV SHOP", "Pour qui code..." → "For devs who want conversion without friction", etc.).

- [ ] **Step 2: Write the failing test**

```ts
// SPDX-License-Identifier: MIT
import { describe, it, expect, beforeEach } from 'vitest';
import { renderDevBand } from '../../src/components/dev-band';

describe('DevBand', () => {
  beforeEach(() => { localStorage.clear(); });

  it('renders collapsed by default', () => {
    const el = renderDevBand();
    expect(el.classList.contains('dev-band--expanded')).toBe(false);
    expect(el.querySelector<HTMLElement>('.dev-band__bento')?.hidden).toBe(true);
  });
  it('expands on teaser click', () => {
    const el = renderDevBand();
    el.querySelector<HTMLElement>('.dev-band__teaser')!.click();
    expect(el.classList.contains('dev-band--expanded')).toBe(true);
    expect(localStorage.getItem('devBandOpen')).toBe('true');
  });
  it('renders 6 bento cards', () => {
    const el = renderDevBand();
    el.querySelector<HTMLElement>('.dev-band__teaser')!.click();
    expect(el.querySelectorAll('[data-component="bento-card"]').length).toBe(6);
  });
});
```

- [ ] **Step 3: Run test, FAIL.**

- [ ] **Step 4: Implement `src/components/dev-band.ts`**

```ts
// SPDX-License-Identifier: MIT
import { t } from '../i18n/t';

const STORAGE_KEY = 'devBandOpen';

function getStored(): boolean {
  try { return localStorage.getItem(STORAGE_KEY) === 'true'; }
  catch { return false; }
}

function setStored(open: boolean): void {
  try { localStorage.setItem(STORAGE_KEY, String(open)); } catch { /* noop */ }
}

const CARD_KEYS = ['runtime', 'stack', 'license', 'plugin', 'providers', 'platform'] as const;

export function renderDevBand(): HTMLElement {
  let isOpen = getStored();
  const el = document.createElement('section');
  el.className = `dev-band${isOpen ? ' dev-band--expanded' : ''}`;
  el.innerHTML = buildMarkup(isOpen);
  el.querySelector<HTMLElement>('.dev-band__teaser')!.addEventListener('click', () => {
    isOpen = !isOpen;
    setStored(isOpen);
    el.classList.toggle('dev-band--expanded', isOpen);
    el.querySelector<HTMLElement>('.dev-band__bento')!.hidden = !isOpen;
    el.querySelector<HTMLElement>('.dev-band__teaser-cta')!.textContent =
      isOpen ? t('devBand.teaserCtaOpen') : t('devBand.teaserCta');
  });
  return el;
}

function buildMarkup(isOpen: boolean): string {
  const cards = CARD_KEYS.map((key) => {
    const isPaid = key === 'platform';
    const badge = isPaid ? `<span class="bento-card__badge">${t(`devBand.cards.platform.badge`)}</span>` : '';
    return `
      <article data-component="bento-card" class="bento-card${isPaid ? ' bento-card--paid' : ''}" data-accent="${key}">
        ${badge}
        <div class="bento-card__label">${t(`devBand.cards.${key}.label`)}</div>
        <div class="bento-card__title">${t(`devBand.cards.${key}.title`)}</div>
        <div class="bento-card__meta">${t(`devBand.cards.${key}.meta`)}</div>
      </article>
    `;
  }).join('');
  return `
    <button class="dev-band__teaser">
      <span>${t('devBand.teaserPrompt')}</span>
      <div class="dev-band__teaser-divider"></div>
      <span class="dev-band__teaser-cta">${isOpen ? t('devBand.teaserCtaOpen') : t('devBand.teaserCta')}</span>
    </button>
    <div class="dev-band__bento" ${isOpen ? '' : 'hidden'}>
      <div class="dev-band__halftone"></div>
      <div class="dev-band__speed-lines"></div>
      <header class="dev-band__header">
        <div>
          <h2 class="dev-band__heading">${t('devBand.heading')}</h2>
          <div class="dev-band__tagline">${t('devBand.tagline')}</div>
        </div>
        <div class="dev-band__status">
          <span class="dev-band__live">● ${t('devBand.liveLabel')}</span>
          <span class="dev-band__build">${t('devBand.buildLabel')} <strong>v2.0.0</strong></span>
        </div>
      </header>
      <div class="dev-band__cards">${cards}</div>
    </div>
  `;
}
```

- [ ] **Step 5: Run test, PASS.**

### Task 4.2: Dev band styles — manga accents

**Files:**
- Create: `src/styles/dev-band.css` (imported by `main.ts`)

- [ ] **Step 1: Create `src/styles/dev-band.css`** (based on `dev-band-manga-light.html` mockup)

Full CSS: teaser bar with dashed divider, halftone `radial-gradient` overlay, speed-lines absolute positioning, bento grid 3×2, clip-path triangle per `data-accent`, bento-card--paid with `box-shadow: var(--shadow-manga-offset)` + badge. (~150 lines CSS — see mockup file for exact values.)

- [ ] **Step 2: Import in `main.ts`** and wire `renderDevBand()` after picker, before footer.

- [ ] **Step 3: Visual dogfood vs mockup.**

- [ ] **Step 4: Commit + tag `v0.3.0`**

```bash
git add .
git commit -m "feat(dev-band): collapsible DEV STATS band with manga accents

Phase 4 complete — v0.3.0. localStorage-persistent collapse state,
halftone + speed lines + clip-path triangles, PAID card with offset
shadow. Visual matches dev-band-manga-light mockup."
git tag -a v0.3.0 -m "v0.3.0 — dev band"
git push origin main v0.3.0
```

---

## Phase 5 — Supabase self-host + Auth config (`v0.4.0`)

**Goal:** Self-hosted Supabase stack running on VPS at `https://supabase.myconciergerie.fr`, magic-link via OVH SMTP verified delivered to real inboxes, Google OAuth configured and tested.

**Estimated wall-clock:** 3–5h.

### Task 5.1: VPS prerequisites

- [ ] **Step 1: SSH to VPS as admin user**

Confirm user + sudo: `ssh vps && whoami && sudo -v`.

- [ ] **Step 2: Install Docker + Docker Compose (Ubuntu)**

```bash
sudo apt update
sudo apt install -y docker.io docker-compose-plugin
sudo usermod -aG docker $USER
```
Log out and back in, verify: `docker --version && docker compose version`.

- [ ] **Step 3: Verify RAM ≥ 4 GB** — `free -h`. If < 4 GB, STOP and surface for VPS upgrade.

- [ ] **Step 4: Open firewall ports 80 + 443 only**

```bash
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### Task 5.2: Supabase Docker Compose stack

- [ ] **Step 1: Clone official Supabase repo on VPS**

```bash
cd /opt
sudo mkdir -p supabase && sudo chown $USER: supabase
cd supabase
git clone --depth 1 https://github.com/supabase/supabase .
cd docker
```

- [ ] **Step 2: Copy + edit `.env`**

```bash
cp .env.example .env
```

Generate secrets:
```bash
POSTGRES_PASSWORD=$(openssl rand -hex 32)
JWT_SECRET=$(openssl rand -hex 32)
DASHBOARD_PASSWORD=$(openssl rand -hex 16)
```

Edit `.env` to set:
- `POSTGRES_PASSWORD=<generated>`
- `JWT_SECRET=<generated>`
- `ANON_KEY=<derived from JWT_SECRET per https://supabase.com/docs/guides/self-hosting/docker#generate-api-keys>`
- `SERVICE_ROLE_KEY=<derived similarly>`
- `SITE_URL=https://genesis.myconciergerie.fr`
- `API_EXTERNAL_URL=https://supabase.myconciergerie.fr`
- `DASHBOARD_USERNAME=admin`
- `DASHBOARD_PASSWORD=<generated>`

Store the generated secrets in a password manager AND in `memory/reference/supabase_genesis_selfhost.md` (NEVER commit the secrets — commit only the memory file structure with placeholders).

- [ ] **Step 3: Start the stack**

```bash
docker compose up -d
docker compose ps
```
Expected: all services show `running` or `healthy`. Wait 60s after first start, re-check.

- [ ] **Step 4: Verify Studio accessible locally**

```bash
curl -u admin:$DASHBOARD_PASSWORD http://localhost:3000/
```
Expected: HTML response (Studio UI).

### Task 5.3: Reverse proxy + TLS

- [ ] **Step 1: Install nginx + certbot**

```bash
sudo apt install -y nginx certbot python3-certbot-nginx
```

- [ ] **Step 2: Write nginx server block**

Create `/etc/nginx/sites-available/supabase.myconciergerie.fr`:
```nginx
server {
  listen 80;
  server_name supabase.myconciergerie.fr;
  location / {
    proxy_pass http://localhost:8000;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
  }
}
```

Enable: `sudo ln -s /etc/nginx/sites-available/supabase.myconciergerie.fr /etc/nginx/sites-enabled/`. Test: `sudo nginx -t`. Reload: `sudo systemctl reload nginx`.

- [ ] **Step 3: Add OVH DNS record**

In OVH manager: `A supabase.myconciergerie.fr → <VPS_IP>`, TTL 300. Verify propagation: `dig supabase.myconciergerie.fr @1.1.1.1`.

- [ ] **Step 4: Get Let's Encrypt cert**

```bash
sudo certbot --nginx -d supabase.myconciergerie.fr --non-interactive --agree-tos --email contact@ar2100.fr
```
Expected: `Successfully deployed certificate`. Nginx auto-updates config for HTTPS.

- [ ] **Step 5: Verify health endpoint**

```bash
curl https://supabase.myconciergerie.fr/auth/v1/health
```
Expected: JSON `{"name":"GoTrue","version":"...","description":"GoTrue is a..."}`.

### Task 5.4: OVH SMTP config in GoTrue

- [ ] **Step 1: Create `noreply@myconciergerie.fr` mailbox in OVH manager** if not existing (Email → Domain → New mailbox, 5 GB default). Note password.

- [ ] **Step 2: Open Supabase Studio at `https://supabase.myconciergerie.fr/project/default/settings/auth`**

Log in with `admin` + dashboard password.

- [ ] **Step 3: Configure custom SMTP**

Auth settings → SMTP Settings → Enable custom SMTP:
- Host: `ssl0.ovh.net`
- Port: `465`
- User: `noreply@myconciergerie.fr`
- Pass: mailbox password
- Sender name: `Genesis`
- Sender email: `noreply@myconciergerie.fr`

Save. Studio tests connection automatically — expect green checkmark.

- [ ] **Step 4: Trigger test magic-link and verify deliverability to 3 inboxes**

Use Studio's Auth → Users → Send magic link to 3 real emails you control:
1. A Gmail address
2. An Outlook.com / Hotmail address
3. An iCloud address

For each: open the inbox within 2 minutes, verify email arrived in primary inbox (NOT spam), click link, verify redirect to `https://genesis.myconciergerie.fr` (will 404 for now — that's fine, we're testing the email flow).

**If any of the 3 lands in spam → STOP.** Investigate SPF/DKIM on `myconciergerie.fr` via `dig TXT myconciergerie.fr @1.1.1.1`, confirm OVH SMTP is authorized sender, adjust DNS if needed, retry. Do not proceed with Phase 6 until all 3 deliver clean.

### Task 5.5: Google OAuth provider

- [ ] **Step 1: Google Cloud Console — create OAuth 2.0 Client ID**

1. Open Google Cloud Console → APIs & Services → Credentials (in correct Chrome profile per Layer 0 `reference_chrome_profiles_machine.md` — Profile 2 = myconciergerie@gmail.com)
2. Select or create project "Genesis Platform"
3. + Create Credentials → OAuth client ID → type: Web application
4. Name: "Genesis Platform — genesis.myconciergerie.fr"
5. Authorized JS origins: `https://genesis.myconciergerie.fr` (also add `http://localhost:5173` for dev)
6. Authorized redirect URIs: `https://supabase.myconciergerie.fr/auth/v1/callback`
7. Save → copy Client ID + Client Secret

- [ ] **Step 2: Enable Google provider in Supabase Auth**

Studio → Auth → Providers → Google → enable → paste Client ID + Client Secret → Save.

- [ ] **Step 3: Smoke test Google OAuth**

Open `https://supabase.myconciergerie.fr/auth/v1/authorize?provider=google&redirect_to=https://genesis.myconciergerie.fr` in a browser signed into Google (Profile 2). Consent screen appears. Approve. Verify redirect lands on `https://genesis.myconciergerie.fr?code=...` (404 fine — the code exchange will work once app is wired in Phase 6).

### Task 5.6: Email templates FR / EN

- [ ] **Step 1: Customize Magic Link template in Studio**

Auth → Templates → Magic Link. Replace default with bilingual template (French first, English below):

```html
<!-- SPDX-License-Identifier: MIT -->
<h2>Connexion à Genesis</h2>
<p>Clique le lien ci-dessous pour te connecter :</p>
<p><a href="{{ .ConfirmationURL }}">Continuer sur Genesis</a></p>
<p>Ce lien expire dans 1 heure.</p>
<hr>
<h2>Sign in to Genesis</h2>
<p>Click the link below to sign in:</p>
<p><a href="{{ .ConfirmationURL }}">Continue to Genesis</a></p>
<p>This link expires in 1 hour.</p>
<hr>
<p style="font-size:11px;color:#666">© 2026 Genesis · by myconciergerie</p>
```

Save. Send a test to yourself via Users panel. Verify formatting in Gmail.

### Task 5.7: Memory + env

**Files (in `genesis-web` repo):**
- Create: `memory/MEMORY.md`, `memory/reference/supabase_genesis_selfhost.md`, `.env.example`

- [ ] **Step 1: Create `memory/reference/supabase_genesis_selfhost.md`** with structure (NEVER put secrets here — commit only placeholders and operational notes):

```markdown
<!-- SPDX-License-Identifier: MIT -->
---
name: Supabase self-host — genesis-web
type: reference
---

# Supabase self-host runbook

VPS: `<VPS_HOSTNAME>` (IP in OVH manager). Stack path: `/opt/supabase/docker/`.

## Endpoints

- Studio: `https://supabase.myconciergerie.fr` (basic auth: admin / <password-in-1password>)
- API: `https://supabase.myconciergerie.fr/auth/v1/*`, `/rest/v1/*`
- Public anon key: see `.env.local` (gitignored)

## Stack management

- Up: `cd /opt/supabase/docker && docker compose up -d`
- Down: `docker compose down`
- Logs: `docker compose logs <service>` (services: auth, rest, realtime, storage, kong, db, studio)
- Update: `git pull && docker compose pull && docker compose up -d`
- Backup (Postgres): `docker compose exec db pg_dump -U postgres postgres > backup-$(date +%F).sql`

## Auth providers enabled

- Email (magic-link only — password disabled)
- Google OAuth — Client ID in Studio Auth → Providers

## SMTP

- OVH webmail `ssl0.ovh.net:465` TLS
- Sender `noreply@myconciergerie.fr`
- Inherits SPF/DKIM from myconciergerie.fr OVH DNS

## Secrets (NOT in git)

- `POSTGRES_PASSWORD`, `JWT_SECRET`, `DASHBOARD_PASSWORD`, `SMTP_PASSWORD` — all in 1password vault "Genesis"
- `/opt/supabase/docker/.env` on VPS is the live source of truth
```

- [ ] **Step 2: Create `.env.example` in `genesis-web` repo**

```
VITE_SUPABASE_URL=https://supabase.myconciergerie.fr
VITE_SUPABASE_ANON_KEY=<paste anon key from Studio Settings API>
```

- [ ] **Step 3: Create `.env.local` (gitignored) with actual values**

Do NOT commit this file. `.gitignore` already excludes it.

- [ ] **Step 4: Create `memory/MEMORY.md` index for genesis-web**

```markdown
<!-- SPDX-License-Identifier: MIT -->
# MEMORY — genesis-web

## Reference

- [Supabase self-host runbook](reference/supabase_genesis_selfhost.md) — VPS endpoints, stack commands, SMTP config, secret locations
```

- [ ] **Step 5: Commit + tag `v0.4.0`**

```bash
git add memory/ .env.example
git commit -m "feat(infra): Supabase self-host on VPS + OVH SMTP + Google OAuth

Phase 5 complete — v0.4.0. Self-hosted Supabase Docker Compose
stack at https://supabase.myconciergerie.fr. Magic-link delivered
via OVH SMTP verified against 3 real inboxes. Google OAuth
configured. Secrets in 1password, memory/reference/ runbook
commits structure only."
git tag -a v0.4.0 -m "v0.4.0 — supabase self-host + auth config"
git push origin main v0.4.0
```

---

## Phase 6 — Auth modal + wire CTAs (`v0.5.0`)

**Goal:** Clicking hero CTA or Anthropic picker opens the auth modal; Google OAuth + magic-link both trigger real Supabase requests and redirect to `/auth/callback`.

**Estimated wall-clock:** 2–3h.

### Task 6.1: Supabase client singleton + sign-in helpers

**Files:**
- Install: `@supabase/supabase-js`
- Create: `src/auth/supabase.ts`, `src/auth/sign-in.ts`, unit tests

- [ ] **Step 1: Install**

```bash
npm install @supabase/supabase-js
```

- [ ] **Step 2: Create `src/auth/supabase.ts`**

```ts
// SPDX-License-Identifier: MIT
import { createClient } from '@supabase/supabase-js';

const url = import.meta.env.VITE_SUPABASE_URL;
const key = import.meta.env.VITE_SUPABASE_ANON_KEY;
if (!url || !key) throw new Error('VITE_SUPABASE_URL and VITE_SUPABASE_ANON_KEY must be set');

export const supabase = createClient(url, key, {
  auth: { autoRefreshToken: true, persistSession: true, detectSessionInUrl: true },
});
```

- [ ] **Step 3: Create `src/auth/sign-in.ts`**

```ts
// SPDX-License-Identifier: MIT
import { supabase } from './supabase';
import type { Provider } from '../components/picker';

const callbackUrl = `${window.location.origin}/auth/callback`;

export async function signInWithGoogle(providerPref: Provider): Promise<void> {
  const { error } = await supabase.auth.signInWithOAuth({
    provider: 'google',
    options: {
      redirectTo: callbackUrl,
      queryParams: { provider_preference: providerPref },
    },
  });
  if (error) throw error;
}

export async function signInWithMagicLink(email: string, providerPref: Provider): Promise<void> {
  const { error } = await supabase.auth.signInWithOtp({
    email,
    options: {
      emailRedirectTo: callbackUrl,
      data: { provider_preference: providerPref },
    },
  });
  if (error) throw error;
}
```

- [ ] **Step 4: Write sign-in unit tests with Supabase mocked.** (Mock `@supabase/supabase-js` module; assert `signInWithOAuth` called with right args, same for Otp.)

### Task 6.2: Auth modal component

**Files:**
- Create: `src/components/auth-modal.ts`, `tests/unit/components.auth-modal.test.ts`

- [ ] **Step 1: Write failing tests** — covers state 1 render, state 2 render, Google click calls handler, email submit calls handler, close button removes modal.

- [ ] **Step 2: Implement `src/components/auth-modal.ts`** following `auth-modal.html` mockup two states.

- [ ] **Step 3: Run tests, PASS.**

- [ ] **Step 4: Wire trigger in `main.ts`**

Update `onCtaClick` in `renderHero` + `onProviderClick` in `renderPicker` to open modal with `provider='anthropic'`.

- [ ] **Step 5: Manual dogfood — click CTA, modal opens, enter test email, submit, verify network request to `/auth/v1/otp`, verify modal transitions to state 2.**

- [ ] **Step 6: Commit.**

### Task 6.3: E2E auth flow tests

**Files:**
- Create: `tests/e2e/auth-magic-link.spec.ts`, `tests/e2e/auth-google-oauth.spec.ts`

- [ ] **Step 1: Playwright test for magic-link request**

```ts
import { test, expect } from '@playwright/test';
test('magic-link request succeeds', async ({ page }) => {
  await page.goto('/');
  await page.locator('.hero__cta').click();
  await expect(page.locator('.auth-modal')).toBeVisible();
  await page.fill('input[type="email"]', 'test+e2e@example.com');
  await page.locator('[data-component="magic-link-submit"]').click();
  await expect(page.locator('.auth-modal--sent')).toBeVisible();
});
```

- [ ] **Step 2: Google OAuth test — stub the redirect** (Playwright can't complete external redirects easily; assert redirect fires correctly via `page.waitForURL('**/auth/v1/authorize**')`).

- [ ] **Step 3: Run full suite, commit + tag `v0.5.0`**

---

## Phase 7 — Auth callback + `/welcome` page (`v0.6.0`)

**Goal:** `/auth/callback` exchanges code/token to session; `/welcome` renders authed micro-dashboard; sign-out works.

**Estimated wall-clock:** 2–3h.

### Task 7.1: Router

**Files:**
- Create: `src/router.ts`, `tests/unit/router.test.ts`

- [ ] **Step 1: Minimal hash-free history router for 3 paths (`/`, `/auth/callback`, `/welcome`)**

### Task 7.2: Session observer

**Files:**
- Create: `src/auth/session.ts`, `src/auth/callback.ts`, tests

- [ ] **Step 1: `getSession()`, `onAuthStateChange` observer, `signOut()` helpers.**
- [ ] **Step 2: `callback.ts` reads URL hash/query, calls `supabase.auth.exchangeCodeForSession()`, redirects.**

### Task 7.3: Welcome page composition

**Files:**
- Create: `src/components/welcome-hero.ts`, `config-cards.ts`, `empty-state.ts`, `src/pages/welcome.ts`

- [ ] **Step 1-4: Implement per `welcome-dashboard.html` mockup.** Tests for each.

### Task 7.4: Sign-out in footer when authed

- [ ] **Step 1: Footer shows "Déconnexion" link when session present; clicking calls `signOut()` + redirects to `/`.**

### Task 7.5: E2E full flow

**File:** `tests/e2e/welcome.spec.ts` — (requires Playwright to intercept Supabase HTTP response to simulate auth; alternative: use Supabase test user via service role key in test env).

- [ ] **Step 1-3: Build test that: stubs auth session, navigates to `/welcome`, asserts hero + config cards + empty state + sign-out wire.**

- [ ] **Commit + tag `v0.6.0`**

---

## Phase 8 — Production deploy (`v1.0.0`)

**Goal:** `https://genesis.myconciergerie.fr` serves the landing with working auth end-to-end. Acceptance criteria #1–#12 from spec Section 15 all green.

**Estimated wall-clock:** 2–3h.

### Task 8.1: VPS-side deploy key + nginx for landing

- [ ] **Step 1: Generate VPS deploy keypair** — `ssh-keygen -t ed25519 -f ~/.ssh/id_genesis_web_deploy -N ""` on VPS.
- [ ] **Step 2: Register public key as deploy key in `genesis-web` repo** (GitHub → Settings → Deploy keys → Add key, paste `id_genesis_web_deploy.pub`).
- [ ] **Step 3: Add GitHub Actions secret `VPS_SSH_PRIVATE_KEY`** with the private key contents.
- [ ] **Step 4: Add GitHub Actions secrets `VPS_HOST`, `VPS_USER`, `VPS_PATH=/var/www/genesis/`.**
- [ ] **Step 5: Create `/var/www/genesis/` on VPS with right ownership** — `sudo mkdir -p /var/www/genesis && sudo chown deploy:www-data /var/www/genesis`.
- [ ] **Step 6: Nginx server block for `genesis.myconciergerie.fr`** → root `/var/www/genesis`, index `index.html`. Certbot cert.
- [ ] **Step 7: OVH DNS `A genesis → VPS_IP`, TTL 300.**

### Task 8.2: GitHub Actions deploy workflow

**File:** `.github/workflows/deploy-production.yml`

- [ ] **Step 1: Write workflow**

```yaml
name: Deploy to production
on:
  push:
    branches: [main]
jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20' }
      - run: npm ci
      - run: npm test
      - run: npm run build
        env:
          VITE_SUPABASE_URL: ${{ secrets.VITE_SUPABASE_URL }}
          VITE_SUPABASE_ANON_KEY: ${{ secrets.VITE_SUPABASE_ANON_KEY }}
      - run: |
          npx playwright install --with-deps chromium
          npm run test:e2e
      - name: Axe-core smoke
        run: npx playwright test tests/e2e/axe.spec.ts
      - name: Push dist to production branch
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git fetch origin production
          git worktree add ../prod production
          cp -r dist/* ../prod/
          cd ../prod
          git add .
          git commit -m "deploy: ${{ github.sha }}" || echo "no changes"
          git push origin production
      - name: Rsync to VPS
        uses: burnett01/rsync-deployments@5.2
        with:
          switches: -avzr --delete
          path: dist/
          remote_path: /var/www/genesis/
          remote_host: ${{ secrets.VPS_HOST }}
          remote_user: ${{ secrets.VPS_USER }}
          remote_key: ${{ secrets.VPS_SSH_PRIVATE_KEY }}
```

- [ ] **Step 2: Add `VITE_SUPABASE_URL` + `VITE_SUPABASE_ANON_KEY` to GitHub Actions secrets.**

- [ ] **Step 3: Axe-core install**

```bash
npm install -D @axe-core/playwright
```

Create `tests/e2e/axe.spec.ts`:
```ts
// SPDX-License-Identifier: MIT
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test('landing is accessible (no critical/serious issues)', async ({ page }) => {
  await page.goto('/');
  const results = await new AxeBuilder({ page }).analyze();
  const critical = results.violations.filter(v => v.impact === 'critical' || v.impact === 'serious');
  expect(critical).toEqual([]);
});
```

- [ ] **Step 4: Push to main, watch Actions**

```bash
git push origin main
gh run watch
```

Expected: all steps green. Check dist appears in `production` branch. Check `/var/www/genesis/` has index.html on VPS.

### Task 8.3: End-to-end smoke test

- [ ] **Step 1: Open `https://genesis.myconciergerie.fr` in incognito**, verify HTTPS green padlock, landing renders.
- [ ] **Step 2: Click CTA, choose Google OAuth** with a real test Gmail account. Verify redirect through Google → Supabase → `/auth/callback` → `/welcome`.
- [ ] **Step 3: Sign out from welcome, verify back to landing unauth'd.**
- [ ] **Step 4: Click CTA again, enter email** (different test email), wait for magic-link, click in Gmail, verify landing on `/welcome`.
- [ ] **Step 5: Check VPS `/var/log/nginx/access.log` + `docker compose logs auth` for no errors.**

### Task 8.4: CHANGELOG + self-rating + tag `v1.0.0`

- [ ] **Step 1: Update `CHANGELOG.md`** with v1.0.0 entry:
  - Features shipped (landing, i18n, dev band, auth, welcome, deploy)
  - Honest 5-axis self-rating (0–10 per axis + avg)
  - Known issues if any
- [ ] **Step 2: Re-evaluate rating honestly** — per Layer 0 `feedback_honest_self_rating_post_feat.md`, willingness to drop ≥ 0.5 if reality differs from projection.

- [ ] **Step 3: Tag + push**

```bash
git tag -a v1.0.0 -m "v1.0.0 — landing live at genesis.myconciergerie.fr"
git push origin v1.0.0
```

- [ ] **Step 4: Create session archive** via Genesis session-post-processor skill in the project-genesis repo, record the implementation journey.

- [ ] **Step 5: Write resume prompt for next session** (sub-project #2 drop-zone kickoff).

---

## Post-ship checklist (before calling v1.0.0 done)

- [ ] All 12 acceptance criteria from spec Section 15 verified manually.
- [ ] Playwright E2E passes on chromium + firefox in CI.
- [ ] Axe-core smoke passes (no critical/serious).
- [ ] `https://genesis.myconciergerie.fr` loads in < 1 s (run PageSpeed Insights).
- [ ] Mobile viewport (375 px) renders without horizontal scroll.
- [ ] Magic-link delivered to fresh Gmail, Outlook, iCloud — all primary inbox.
- [ ] Google OAuth flow completes end-to-end.
- [ ] Supabase users table shows 2 test users with correct `provider_preference` metadata.
- [ ] Nginx + Supabase Docker compose both survive a VPS reboot.
- [ ] `memory/reference/supabase_genesis_selfhost.md` is accurate and secret-free.
- [ ] CHANGELOG v1.0.0 entry present with honest 5-axis rating ≥ 8.0 each axis.
