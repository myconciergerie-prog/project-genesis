<!-- SPDX-License-Identifier: MIT -->
---
name: Bootstrap intent — colocs-tracker
description: Structured project intent parsed from brief.md + annexe.md at Genesis Phase 0 (stress-test variant). Consumed by all downstream phases as the source of truth for project name, slug, vision, license, plugin flag, plan tier, and scope locks.
type: project
phase: 0
stress_test: true
---

# Bootstrap intent — colocs-tracker

## Parsed at

2026-04-18 — Genesis v1.4.1 stress-test run

## Fields

| Field | Value | Source |
|---|---|---|
| Project name | Colocs Tracker | brief.md (derived from "tracker les dépenses partagées entre colocs") |
| Slug | colocs-tracker | user-confirmed at Step 0 consent card |
| Vision | Petit outil web pour tracker les dépenses partagées entre colocs étudiants Île-de-France et familles recomposées partageant un logement. MVP responsive, pas d'app native V1. Onboarding multi-utilisateur. | brief.md + annexe.md (union) |
| License | MIT (default) | not specified in seeds — Genesis default applied |
| Is-a-plugin | no | inferred (web app, not Claude Code skill) |
| Plan tier | unspecified — assume Free | inferred from budget 800€ ceiling |
| Stack hints | Next.js + Supabase (web responsive) | brief.md |
| Scope locks | none | no lock declared |
| Mixed media | brief.md, annexe.md | folder scan |

## Reconciliation — brief.md → annexe.md (chronological override)

| Field | brief.md (initial) | annexe.md (post-réunion 15 avril) | Retained |
|---|---|---|---|
| Budget | 500 € | 800 € | **800 €** |
| Cible | colocs étudiants IDF | + familles recomposées | **union** |
| Onboarding | (silent) | multi-user explicit | **multi-user** |
| Stack | Next.js + Supabase | (silent) | **Next.js + Supabase** |
| Livrable | web responsive | (silent) | **web responsive** |

## Gaps acknowledged at Phase 0 (deferred to Phase 4 or beyond)

- Auth provider Supabase (magic link vs OAuth Google) — deferred to Phase 4 design spec
- Splitting model (égal / pondéré / catégories) — deferred to Phase 4 design spec
- i18n FR+EN dès J1 per Layer 0 R9 — assume yes, confirm Phase 4
- Plan tier explicit — deferred (will surface at Phase 5.5 if real bootstrap)
- License explicit — MIT default applied
- Hosting (Vercel / OVH / autre) — deferred to Phase 4

## Raw brief.md (verbatim)

```
# Brief — Colocs Tracker

## Vision

Un petit outil pour tracker les dépenses partagées entre colocs.

## Budget

Budget max **500 €** pour le MVP.

## Stack

Stack envisagée : Next.js + Supabase.

## Cible

Principalement des **colocs étudiants en Île-de-France**.

## Livrable

Web app responsive, pas besoin d'app mobile native pour V1.
```

## Raw annexe.md (verbatim)

```
# Annexe technique — révision post-réunion du 15 avril

## Budget révisé

Après revue, le budget est porté à **800 €** pour couvrir les features V2.

## Cible élargie

La cible s'élargit aux **familles recomposées** qui partagent un logement — use case similaire.

## Notes complémentaires

Cahier des charges fonctionnel à affiner. Prévoir un onboarding multi-utilisateur.
```

## Stress-test frictions captured at Phase 0

1. **No `config.txt` slot for BRIEF + ANNEXE chronological override** — Phase 0 Step 0.1 table classes "no config.txt but BRIEF.md exists" as "Unusual — ask user", but doesn't anticipate a 2-file evolving spec (initial + revision). Suggested v1.5 enhancement: add a "BRIEF.md + chronological annexes" canonical input shape with explicit chronological-override semantics.
2. **No multi-file seed parser** — Phase 0 implicitly assumes 1 canonical seed file. Multi-file seeds require manual reconciliation by the orchestrator-driver, not codified in the runbook.
3. **No conflict-reconciliation helper** — when fields conflict between seeds (e.g. budget 500→800), reconciliation policy (chronological override vs user prompt vs union) is not specified. Default applied here: chronological override (later wins) for scalars, union for sets.
