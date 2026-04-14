<!-- SPDX-License-Identifier: MIT -->
---
topic: open-source-license-for-dev-tooling
type: sota
created_at: 2026-04-14
expires_at: 2026-04-21
status: active
sources:
  - https://dev.to/juanisidoro/open-source-licenses-which-one-should-you-pick-mit-gpl-apache-agpl-and-more-2026-guide-p90
  - https://redmonk.com/sogrady/2026/03/25/open-source-licensing-2026/
  - https://www.linuxfoundation.org/licensebestpractices
  - https://fossa.com/learn/developers-guide-open-source-software-licenses/
confidence: high
supersedes: null
---

# Licenses for Dev Tooling Projects — State of the Art 2026

## TL;DR

- **Best-at-date for workflow tooling / dev templates**: **MIT**
- **Most-potential (for corporate adoption)**: **Apache-2.0**
- **Not recommended for workflow templates**: BSL (non-OSI, misleading if marketed as "open source")
- **Always applied regardless of license choice**: SPDX short-form identifier in every source file header

## Why MIT is best-at-date for Genesis

- Simplest permissive license — short text, widely understood, near-zero legal friction for contributors and users
- Used by `obra/superpowers` (the direct comparable Claude Code plugin project) and the majority of plugins in the Anthropic marketplace
- ~60% of all open source projects use one of MIT / GPL / Apache-2; MIT dominates for dev tooling specifically
- Zero ambiguity for solo maintainers and clear terms for downstream users
- Pivot to Apache-2 remains open at any time while the project has a single copyright holder — no lock-in

## Why Apache-2.0 is the pivot option

- Adds an explicit patent grant and anti-litigation protections absent from MIT
- Preferred default of Microsoft / Google / Amazon and other large contributors for SDKs, libraries, and platforms they want corporations to adopt safely
- Relevant if Genesis gains external traction and starts receiving contributions from corporate users who need patent safety
- Pivot path: when the time comes, re-license via a PR on `LICENSE` (requires either single-holder consent or a CLA for prior contributors)

## Why not BSL / SSPL / other source-available

- Non-OSI — "source available" with restrictions, not open source in the standard sense
- Designed to block compete-by-hosting (the AWS problem) — irrelevant for a workflow template that nobody would want to host as a service
- 4-year automatic transition to permissive terms adds complexity with zero payoff for this use case
- Would be actively misleading if marketed as "open source" while being BSL

## Application for Genesis

- `LICENSE` file at repo root with standard MIT text
- SPDX short-form identifier at top of every source file (see `spdx-headers_2026-04-14.md`)
- `README.md` states MIT clearly in both FR and EN sections (R9 bilingual for public docs)
- `plugin.json` has `"license": "MIT"` field
- Document the Apache-2 pivot path in `CHANGELOG.md` so future maintainers know the escape hatch exists
