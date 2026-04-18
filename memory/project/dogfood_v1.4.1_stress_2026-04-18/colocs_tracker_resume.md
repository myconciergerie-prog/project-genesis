<!-- SPDX-License-Identifier: MIT -->
---
name: Resume prompt — colocs-tracker bootstrap → v0.2
description: Hand-off prompt for the next Claude Code session opened in this folder. Reads at session-open per R1.1 alongside MEMORY.md.
type: resume
phase: 7
date: 2026-04-18
---

# Resume prompt — Colocs Tracker (post-Genesis-stress-test bootstrap)

## What just happened (2026-04-18)

This project was bootstrapped via Genesis Protocol v1.4.1 in **stress-test mode**. The bootstrap intentionally stopped before Phase 5.5 (auth) and Phase 6 (push/PR/merge to GitHub) — see `memory/project/stress_test_report.md` for the full friction log.

Concretely, you have:

- `memory/` complete subtree with all 8 sections + INDEX files from 4 sibling skills
- `CLAUDE.md` project entry point
- `.claude/docs/superpowers/rules/v1_rules.md` (R1-R10)
- `.claude/docs/superpowers/research/` with 3/5 R8 stack-relevant entries (TTL expired — refresh before relying on)
- `.claude/docs/superpowers/specs/2026-04-18-colocs-tracker-mvp-design.md` — V1 design draft
- Local git repo (init only, no remote) with 0 commits

You **don't** have:
- SSH key for this project
- GitHub repo + remote
- PAT / `.env.local` with `GH_TOKEN`
- Initial commit (everything is unstaged untracked)
- App code (no `package.json`, no `src/`)

## R1.1 open ritual reminder

Before any Edit/Write : read `memory/MEMORY.md`, then `memory/master.md`, then `memory/project/bootstrap_intent.md`, then this resume prompt, then `memory/project/stress_test_report.md`. Skip files that obviously won't apply to today's request.

## Decision tree for the next session

### Branch A — Promote stress-test → real bootstrap

If the user wants to make this project real :

1. **Confirm scope** : owner = `myconciergerieavelizy@gmail.com` (Scope 2 per Layer 0 `reference_accounts_orgs_and_projects.md`), GitHub org = `myconciergerieavelizy-cloud`, Chrome profile = `Default`.
2. **Run Phase 5.5** (`phase-5-5-auth-preflight` skill) with slug `colocs-tracker`. This creates SSH key + PAT + empty GitHub repo + 3-probe verification.
3. **Run Phase 6** : first commit + push + PR + merge + tag `v0.1.0`.
4. **Refresh expired R8 entries** at `.claude/docs/superpowers/research/sota/` (all 3 are past 7-day TTL as of 2026-04-18).
5. **Run Phase 7** session-post-processor on the bootstrap session JSONL.
6. Then start Branch B for app code.

### Branch B — Start V1 dev (assume bootstrap is real)

If the user wants to start coding V1 :

1. **Open the design draft** : `.claude/docs/superpowers/specs/2026-04-18-colocs-tracker-mvp-design.md`. Walk through the **7 open questions** with the user. Don't write code before answers.
2. **Decide hosting timing** : Layer 0 `infra_2026-04-18_supabase_vps_ovh_migration.md` flags Supabase Cloud → VPS OVH migration deadline **2026-05-10**. Either (a) wait for migration, or (b) bootstrap on Cloud and migrate post-MVP. Recommendation = (b).
3. **Scaffold Next.js 15+ App Router** in a worktree per R2.1 : `.claude/worktrees/scaffold/`. Never edit at the repo root.
4. **First feature** = household creation + magic link auth. Sequence : Supabase project → schema migration → RLS policies (per Layer 0 `feedback_supabase_rls_to_authenticated_force.md`) → Next.js auth wiring → 1 RLS smoke test (per Layer 0 `feedback_supabase_rls_smoke_impersonation.md`).

### Branch C — Read the stress test report and improve Genesis

If the user wants to fix Genesis itself based on this stress test :

1. Open `memory/project/stress_test_report.md`.
2. The 5 captured frictions (input shape, multi-file seed, conflict reconciliation, plugin root resolution, missing R8 entries) are the v1.5 candidate enhancements.
3. Switch to the Genesis project at `C:\Dev\Claude_cowork\project-genesis\` to act on them. **Do not edit Genesis from this folder** — R2.1 worktree discipline + cross-repo confusion.

## Simple resume phrase (for the human)

> "On reprend colocs-tracker. Branche A (vraie bootstrap), B (commencer le code V1), ou C (corriger Genesis depuis la stress test) ?"

## Three suggestions with auto-critique

1. **Branche A puis B** dans la même session. ❌ Trop large — Phase 5.5 + 6 + setup Next.js + premier feature = ~3h, dilution. Mieux séparer.
2. **Branche A seule, ~30 min** : promote en vraie bootstrap, taggue v0.1.0, stop. ✅ Net, livrable. Idéal si user veut "valider l'état" avant d'investir dans le code.
3. **Branche C en priorité**, ~45 min : corrige Genesis pour que le prochain stress test ne ré-itère pas les mêmes 5 frictions. ⚠️ Bénéfice indirect — l'user pourrait préférer avancer sur son projet plutôt que sur l'outil.

**Recommandation par défaut** : ouvrir avec la phrase de reprise, laisser l'user trancher.
