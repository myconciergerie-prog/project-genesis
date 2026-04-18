<!-- SPDX-License-Identifier: MIT -->
---
name: Genesis showcase page — v3 design decisions
description: Brainstorm-resolved design brief for the warm-tech-optimiste rewrite of genesis-showcase.html after v1/v2 user feedback ("pas très sexy, cas d'usage limités"). Captures the 7 decisions locked via /brainstorming skill before implementation.
type: spec
date: 2026-04-18
artefact: genesis-showcase.html (root)
previous_versions: v1 (eae90da) + v2 (9d1b901), both on PR #32
---

# Genesis showcase v3 — design decisions

After v1 (generic SaaS beige) and v2 (dark-terminal dev-landing) both got "bof pas ouf" reactions, user ran `/brainstorming` skill. Seven decisions locked.

## 7 decisions locked

| # | Decision | Choice | Rationale |
|---|---|---|---|
| 1 | Ceremony ladder | Skip full spec-subagent + writing-plans ceremony | Single-file HTML iteration; v1/v2 file-based review loop already served as review gate |
| 2 | Overall vibe | **C · Warm-tech optimiste** (Linear / Vercel warm variant — NOT dark terminal) | Mis-match of v2 dark-dev vs myconciergerie.fr family-concierge distribution venue |
| 3 | Illustration approach | **C · 15 mini-scènes SVG narratives** | "Illustrée" in brief; icons in v1/v2 felt flat |
| 4 | SVG style | **A · Flat plein-couleur moderne** (Duolingo / Stripe-illustrations-like) | 3-4 colors per illu, shapes remplies, micro-shadow, modern-product warm |
| 5 | Palette | **C · Crème + orange vif + cobalt + rose poudré** (+ sage for kids chapter) | Approachable energetic; reads well under both myconciergerie.fr warm aesthetic AND GitHub readers |
| 6 | Layout structure | Flow éditorial alterné (illu gauche / texte droite, alterné), NOT bento-grid | Each narrative scene gets breathing room |
| 7 | Pro use cases | 5/5/5 symmetry; replace Startup MVP + Freelance multi-client with **Chef steward (yacht)** + **Agent immobilier** | User-requested swap; both more specific/visual than the generic startup/freelance framings |

## Palette applied

| Role | Hex | Usage |
|---|---|---|
| Paper | `#faf4e6` | Main background, vignette zones |
| Ink | `#1a1b2e` | Headings, body text |
| Orange vif | `#ff7043` | H1 accents, CTA, numerals, hover glow, chapter I dominant |
| Cobalt | `#3860b6` | Sub-headings, links, chapter II dominant, SVG second-color |
| Rose poudré | `#e5a7a0` | Soft illustration fills, cartouches |
| Vert sauge | `#8fb896` | Chapter III (kids) accent dominant |
| Muted | `#8a8799` | EN italic captions |
| Line | `#ece3cc` | Subtle dividers |

## Typography

System sans-serif stack at various weights (no web-font dependency). Mono only for micro-kickers.

- Display: `ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI", "Inter", system-ui, sans-serif` at `font-weight: 800` with negative letter-spacing
- Body: same stack at 400/500, `line-height: 1.65`
- Mono kickers: `ui-monospace, "SF Mono", Menlo, monospace`

## 15 illustration scenes (flat 3-4 colors each)

### Chapter I — Au travail (orange dominant + rose + cobalt)

1. **Avocat · dossier complexe** — Balance orange + 3 piles dossiers (rose/cobalt/crème) + fil rouge reliant. Hover: fil pulse.
2. **Chef steward yacht** — Galley en coupe + hublot rond cobalt (vague) + étagères stocks (bouteilles rose / boîtes orange / conserves crème) + plan d'armement grille cobalt mur + silhouette chef-toque orange + clipboard passagers rose. Hover: vague bouge dans hublot.
3. **Journaliste enquête** — Carnet ouvert + loupe cobalt + 3 papiers chiffonnés rose + ampoule orange (l'intuition). Hover: ampoule s'allume.
4. **Architecte chantier** — Blueprint cobalt + règle + crayon orange + mini-grue silhouette + coches rose. Hover: grue bouge flèche.
5. **Agent immobilier** — Maison façade crème perspective + toit cobalt + cheminée rose + pancarte "À VENDRE" orange + trousseau clés doré + 2 silhouettes visiteurs (rose + cobalt). Hover: clé tourne ou pancarte flip "VENDU".

### Chapter II — Vie perso (cobalt dominant + rose + orange accent)

6. **Santé aidant** — Cœur cobalt stylisé + clipboard calendrier RDV orange dedans + ligne temporelle rose ondulante. Hover: cœur bat.
7. **Voyage Japon** — Fuji triangulaire cobalt→crème + Shinkansen orange traversant + torii rose horizon. Hover: Shinkansen traverse.
8. **Généalogie** — Arbre tronc cobalt + 3 branches portraits-cadres (rose/orange/crème) + dates + racines orange. Hover: feuille tombe.
9. **Rénovation maison** — Coupe cross-section toit cobalt / étage crème / rez rose + marteau orange + devis qui dépasse. Hover: brique par brique pulse.
10. **Maker/atelier** — Établi + outils muraux (marteau orange / clé cobalt / pinceau rose) + lampe allumée + sciure crème. Hover: étincelles stagger.

### Chapter III — Avec enfants (sage dominant + orange + rose)

11. **Cahier trésors Lilou** — Bocal transparent + plume rose + 2 galets sauge + carte dorée orange + étoile cobalt. Hover: un objet tourne.
12. **Podcast YouTube famille** — Micro studio sauge + pied cobalt + casque rose + écran crème avec wave audio orange. Hover: wave anime.
13. **Minecraft versioning** — 3 blocks cubiques empilés (sauge/rose/orange) + tags v1/v2/v3 crème. Hover: tag flip.
14. **Grand Oral / TPE** — Pupitre silhouette cobalt + microphone orange + pile 3 livres (sauge/rose/orange) + halo rose. Hover: halo intensifie.
15. **Premier site enfant** — Écran crème + `<code>` orange/cobalt + clavier perspective sauge + curseur orange clignotant (permanent).

## Structure / Layout

- Hero (full-width crème) — badge + title XL + subtitle + CTA + typographic drop-zone art (NO dark terminal — hors-vibe warm-tech)
- Pilliers (4 cards) — Mémoire / Discipline / Reprise / Bilingue
- Chapter I — opener (big roman numeral "I" + title + intro paragraph) + 5 vignettes alterné illu↔text + 1 pull-quote testimonial
- Chapter II — same, with subtle cobalt-dominant tonal shift
- Chapter III — same, with sage-dominant tonal shift
- Closing CTA — install snippet cream box + GitHub link
- Footer — colophon warm + small ASCII drop-zone + myconciergerie.fr sponsor integrated naturally

## Micro-animations (zero JS, pure CSS)

- Vignette hover: `translateY(-4px)` + warm shadow, 0.22s `cubic-bezier(0.4, 0, 0.2, 1)`
- One delight-detail per SVG illustration (listed above)
- CTA primary: subtle pulse shadow at rest (2.5s), amplified on hover
- Roman numerals: fade-in + slide-up stagger on viewport entry

## Ship

- Same PR #32, same branch `docs/showcase-2026-04-18`
- Commit `docs polish v3 (rewrite)` replaces v2 content
- Target size ~60-80 KB (still zero external deps — system fonts, inline SVG)
- Bilingual FR primary + EN italic petite per vignette (R9 tier-3 preserved)
- File path unchanged: `genesis-showcase.html` at repo root
