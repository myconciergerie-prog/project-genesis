<!-- SPDX-License-Identifier: MIT -->

# .claude/docs/superpowers/plans/

Multi-step implementation plans. This is where design-to-execution plans live between "captured as a spec" and "merged to main".

## What goes here

- Plan files with dated slugs: `YYYY-MM-DD_<slug>.md`
- Bootstrap config artefact: `bootstrap_config_2026-04-14.md` (the original `config.txt` seed from the v1 bootstrap session, archived here for historical reference)
- Multi-session work breakdown documents
- Phase-by-phase rollout plans for features that span multiple PRs

## What does NOT go here

- **Specs** (design reasoning, requirements, options analysis) → `specs/`
- **Research** (external findings, library comparisons, best-at-date surveys) → `research/`
- **Rules** (the R1-R10 ruleset) → `rules/`
- **Resume prompts** (session handoffs) → `resume/`
- **Templates** (dev-internal reusable templates) → `templates/`

## Format

Plans are typically structured as numbered step lists with explicit acceptance criteria per step. They are the link between a spec and a stack of PRs.
