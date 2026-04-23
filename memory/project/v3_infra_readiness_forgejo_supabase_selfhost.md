<!-- SPDX-License-Identifier: MIT -->
---
name: v3 web mode infrastructure readiness — Forgejo + Supabase self-hosted
description: |
  Infrastructure primitives that v3 web mode (genesis.myconciergerie.fr) will
  need to consume. Both are now live on the OVH VPS per the sibling repo
  migration-VPS-OVH v0.5.0 cutover (2026-04-23). This file is the bridge
  between "VPS is ready" and "Genesis code that will use it" — forward-looking
  instructions for when the corresponding Genesis PRs ship, NOT a code-change
  ask on v2.0.0 surface.
type: project
created_at: 2026-04-23
---

# v3 infrastructure readiness — Forgejo + Supabase self-hosted

## What is live on the VPS today (2026-04-23)

The sibling repo `C:/Dev/Claude_cowork/migration-VPS-OVH` shipped v0.5.0 on 2026-04-23 with :

- **Supabase self-hosted 15-service stack** at `https://api.myconciergerie.fr` (Kong gateway + PostgREST + Auth/GoTrue + Realtime + Storage + edge-runtime + Studio) and `https://supabase.myconciergerie.fr` (Studio admin UI).
- **Caddy v2 reverse proxy** with Coraza WAF + OWASP CRS 4.25.0 + Let's Encrypt auto-TLS on every subdomain.
- **Observability + backups** (Beszel + Uptime Kuma + nightly pg_dump + age-encrypted offsite sync to B2 EU).

**Forgejo is NOT yet live** — it is planned as v0.6.0 of `migration-VPS-OVH` per `memory/project/v0_6_0_forgejo_migration_plan.md` + `docs/architecture/ADR-008_forgejo_self_host.md` in that sibling repo. Earliest deploy window is 2026-05-01 (after the v0.5.0 48 h soak + Phase 6 test restore + GitHub Actions billing-block lift).

When Forgejo lands, it will be reachable at `https://git.myconciergerie.fr` following the same Caddy + WAF pattern as the other tenants.

## What this means for Genesis v3 web mode

Per Genesis `master.md § "What v3 vision is"` (2026-04-19), the v3 hosted SaaS at `genesis.myconciergerie.fr` performs four platform-owned side effects on behalf of each Victor (web user) :

1. **Extract + bootstrap** — handled by `genesis-drop-zone` + `genesis-protocol` skills (Layer A + Layer B), provider-agnostic already (rule 1 of design discipline).
2. **Create a git repository for the bootstrapped project** — currently targets GitHub via `phase-5-5-auth-preflight` skill.
3. **Provision a Supabase instance for the project's DB + auth + storage** — currently unscoped in the v1 / v2 implementation (deferred, mentioned as v3 platform behaviour).
4. **Deploy to a subdomain** (`<projectslug>.genesis.myconciergerie.fr/` free tier, `<projectslug>.<apex>` paid tier).

Points 2 + 3 are where the live VPS infrastructure changes the target from the v1/v2 external-provider stance to a platform-owned internal stance. Instructions below describe what the corresponding Genesis PRs (future, NOT this session) must respect.

## Point 2 — git provider abstraction (Forgejo as canonical in v3+)

### Current state (v2.0.0)

`phase-5-5-auth-preflight` skill is GitHub-centric. 128 GitHub references across 8 files in the skill (SKILL.md, pat-walkthrough.md, empty-repo-create.md, consent-card.md, ssh-keygen.md, three-probe-test.md, verification.md, playwright-automation.md). Uses the canonical flow : dedicated ed25519 SSH keypair + `github.com-<project>` alias in `~/.ssh/config` + fine-grained PAT creation via GitHub web UI + empty repo creation + 3-probe test (SSH, PAT user, repo existence).

This flow is NOT wrong — it is the reference implementation for CLI mode, and for any v3 user who opts OUT of the platform's git hosting (e.g. power users who already have a GitHub Team subscription and want to stay there).

### v3 target (post-Forgejo-v0.6.0)

Genesis v3 web mode SHOULD default to **Forgejo hosted on the platform VPS** instead of GitHub, because :

- **Single-source platform control.** The platform already hosts the Supabase instance, the Caddy gateway, the subdomains. Having the git repo live on the same infrastructure means one outage surface, one backup scope, one auth boundary.
- **GitHub Actions overage avoidance.** `migration-VPS-OVH` hit a $14.04 GitHub Actions overage on 2026-04-22 that billing-blocked CI. Forgejo Actions runs on our own CPU, no metered billing.
- **Data sovereignty.** Forgejo-on-VPS-OVH-Gravelines keeps code in France / EU. GitHub's legal jurisdiction is US.
- **Cost consolidation.** Free / paid tier pricing is controlled by the platform, not by GitHub's per-seat model.

Opt-out stays available : paid-tier users who prefer GitHub (existing team workflows, external contributors) can override via the v3 drop-zone intent or the web UI provider picker.

### Concrete changes in future Genesis PRs

The v3 web mode PRs that ship post-Forgejo-v0.6.0 MUST :

1. **Generalize `phase-5-5-auth-preflight` skill to a git-provider-agnostic base + two provider-specific variants** :
   - `phase-5-5-auth-preflight-github` — the current v2 content, renamed, zero logic change.
   - `phase-5-5-auth-preflight-forgejo` — Forgejo-specific (different PAT scope names, different empty-repo API path, different host alias default).
   - `phase-5-5-auth-preflight` becomes a dispatcher that reads the `git_provider` field from `drop_zone_intent.md` (added as additive frontmatter key per cross-skill-pattern #4 zero-ripple discipline ; default `forgejo` in v3 web mode, default `github` in v2 CLI mode).
   This mirrors the promptor-anthropic / promptor-gemini pattern (master.md v3 vision rule 6 : per-provider skill).

2. **Extend `drop_zone_intent.md` schema additively (no schema_version bump)** with an optional `git_provider` key (values : `forgejo` / `github` / `gitlab`-future). Field-level `git_provider_source_citation` follows the same pattern as v1.4.0's citation keys. Default when absent : `forgejo` if the web-mode platform flag is on, `github` otherwise (v2 CLI compat).

3. **Respect design discipline rule 1 (provider-agnostic naming)** : the dispatcher skill's function signatures must accept a `git_provider` parameter, no hardcoded GitHub refs outside the `-github` variant's body.

4. **Respect design discipline rule 5 (CLI plugin as reference implementation)** : the v3 web mode reuses the same skill package server-side. No parallel divergent fork. The dispatcher + variants live in this `skills/` tree ; the web platform vendors them.

5. **Capture the pépite in Layer 0** via `feedback_git_provider_agnostic_in_genesis.md` (cross-project rule) once the v0.6.0 Forgejo deploy + the first Genesis-v3.x PR that consumes it land together.

### What `migration-VPS-OVH` v0.6.0 will expose

For the v3 web mode PR to consume :

- **Forgejo API endpoint** : `https://git.myconciergerie.fr/api/v1/` (same base URL pattern as Gitea).
- **Admin API for repo creation** : `POST /api/v1/admin/users/<user>/repos` with a fine-grained-token-scoped PAT.
- **SSH endpoint** : `git@git.myconciergerie.fr:<user>/<repo>.git` (port 222 per the v0.6.0 plan, separate from admin 2226).
- **Actions runner** : separate Docker container registered to the Forgejo instance, for CI parity with GitHub Actions workflows.

## Point 3 — Supabase provisioning (self-hosted VPS as canonical in v3+)

### Current state (v2.0.0)

Genesis v1 / v2 skill surface does NOT auto-provision Supabase. The bootstrapped project's README typically instructs the operator to create a Supabase Cloud project manually and paste the keys into `.env.local`. v3 web mode is the first version where platform-owned auto-provisioning appears in the design (master.md § "What v3 vision is" bullet 1, Lovable-style hosted SaaS).

### v3 target (consuming the self-hosted Supabase at api.myconciergerie.fr)

The v3 web mode platform service (NOT the Genesis plugin itself — the platform backend that vendors the plugin server-side) performs auto-provisioning. Per-project Supabase provisioning uses the **schema-isolation pattern** already established in `migration-VPS-OVH` ADR-002 :

- **One Supabase instance, per-tenant PostgreSQL schemas.** Each Genesis-bootstrapped project gets its own `<projectslug>_<userhash>` schema inside the shared Supabase DB.
- **Per-tenant PostgREST `PGRST_DB_SCHEMAS` allowlist extension.** The platform's tenant-provision job appends the new schema to the allowlist + reloads PostgREST.
- **Per-tenant JWT secret + anon key + service role key** scoped to the schema (see `migration-VPS-OVH` `scripts/legacy/phase3_plus/21_supabase_tenant_provision.sh` for the reference implementation).
- **Per-tenant Supabase URL** exposed to the project as `SUPABASE_URL=https://api.myconciergerie.fr` (shared Kong, schema routed via `PGRST_DB_SCHEMAS`).

### Concrete changes in future Genesis PRs

1. **Genesis bootstrapped project templates** (the files Genesis writes into a new project's working directory) MUST :
   - Ship `.env.local.example` keys for `SUPABASE_URL` + `SUPABASE_ANON_KEY` + `SUPABASE_SERVICE_KEY` (already standard).
   - Document the default web-mode target `https://api.myconciergerie.fr` in the template README.
   - Keep Supabase Cloud as documented fallback for CLI mode users who do NOT deploy to the platform's VPS.

2. **v3 web mode platform backend** (out of scope for Genesis plugin, but referenced here for cross-project consistency) :
   - Reuses `migration-VPS-OVH` `scripts/legacy/phase3_plus/21_supabase_tenant_provision.sh` pattern to provision each tenant schema at bootstrap time.
   - Injects the generated per-tenant keys into the deployed project's runtime environment.
   - Documented in a future `migration-VPS-OVH` ADR (e.g. ADR-009 tenant provisioning API).

3. **No change to Genesis plugin skill surface** for point 3 — auto-provisioning is platform-backend work, not plugin work. Plugin stays CLI-compatible : `.env.local.example` keys ship empty, operator fills them manually, or the platform backend injects them server-side. Design discipline rule 5 preserved (CLI plugin is the reference ; server vendors the same skill code without divergence).

## Design discipline cross-check (master.md § "Design discipline today" load-bearing on every v2 PR)

The forward-looking instructions above respect all seven disciplines :

1. ✅ **Provider-agnostic naming** — `git_provider` key + dispatcher + variants pattern mirrors the existing multi-provider promptor approach.
2. ✅ **No "current cwd" assumptions** — Forgejo / Supabase URLs are env-var-driven, not cwd-read. Already respected by the `drop_zone_intent.md` file list contract.
3. ✅ **No hardcoded local paths** — platform URLs in config files, not filesystem paths.
4. ✅ **Auth split between modes preserved** — v2 CLI keeps its `claude auth status` + `gh auth status` flow ; v3 web platform-paid Anthropic key + platform-SSO remain separate. Git auth similarly splits : CLI mode uses per-project PAT, web mode uses platform-owned Forgejo admin PAT server-side.
5. ✅ **CLI plugin as reference implementation** — the skill dispatcher + variants live in this repo. Web mode vendors the same code server-side. No parallel codebase.
6. ✅ **BYOAI staging — structure-ready, implementation-deferred** — git provider follows the same staging (`forgejo` shipped v3.0, `github` stays as legacy variant, `gitlab` reserved v3.x).
7. ✅ **Lazy-load discipline (web mode only)** — git provider selection follows same rule : picker is interactive pre-auth, provider-specific skill loaded post-auth-callback.

## Timeline

| Milestone | Owner | ETA |
|---|---|---|
| migration-VPS-OVH v0.5.0 tag | operator | ~2026-04-25 after 48 h soak |
| migration-VPS-OVH v0.6.0 Forgejo deploy start | sibling repo session | earliest 2026-05-01 |
| Forgejo first green on VPS | sibling repo | 2026-05-01 + ~5-7 days |
| Genesis v3.0.0 web mode kickoff | this repo session | after v0.6.0 Forgejo green |
| Genesis `phase-5-5-auth-preflight-forgejo` variant ship | this repo session | v3.0.0 scope |
| Cross-repo Layer 0 entry `feedback_git_provider_agnostic_in_genesis.md` | captured post-first-live-dogfood | v3.0.x |

## Cross-repo pointers

- **Sibling repo** (VPS infra) : `C:/Dev/Claude_cowork/migration-VPS-OVH/`
  - Install guide : `docs/install-guide/` (read `README.md` first)
  - v0.6.0 Forgejo plan : `memory/project/v0_6_0_forgejo_migration_plan.md`
  - ADR-008 Forgejo self-host : `docs/architecture/ADR-008_forgejo_self_host.md`
  - Supabase ADR-002 schema-isolation : `docs/architecture/ADR-002_stack_choice.md` (et seq.)
  - Supabase tenant provisioning reference script : `scripts/legacy/phase3_plus/21_supabase_tenant_provision.sh`

- **This repo** (Genesis) cross-references to update when v3 web mode kicks off :
  - `memory/master.md § "What v3 vision is"` — already captures both points at high level ; the v3 PR that lands this will deep-link to the present file.
  - `skills/phase-5-5-auth-preflight/` — will split into dispatcher + `-github` variant + `-forgejo` variant per design discipline rule 1.
  - `skills/genesis-drop-zone/phase-0-welcome.md` + `phase-0-welcome.md` templates — will extend the `drop_zone_intent.md` schema with the optional `git_provider` key (additive, zero Layer B ripple).
  - `skills/genesis-protocol/` — Phase 0 parser already dict-based, will read the new key naturally (cross-skill-pattern #4 zero-ripple precedent).
