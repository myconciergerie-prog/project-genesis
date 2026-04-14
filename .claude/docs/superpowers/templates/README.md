<!-- SPDX-License-Identifier: MIT -->

# .claude/docs/superpowers/templates/

**Dev-internal** templates used by Genesis maintainers during development work. Distinct from the plugin-root `templates/` directory which holds the templates shipped to downstream users.

## What goes here

Templates used during Genesis development itself:

- Memory entry scaffold (when writing a new `project/` or `reference/` entry)
- Spec file skeleton (when starting a new spec in `specs/`)
- Rule change proposal template (when revising `rules/v1_rules.md` → `v2_rules.md`)
- Research cache entry skeleton (R8 frontmatter with all fields)
- Session-opening prompt template (for testing)

## What does NOT go here

- Templates shipped with the plugin → `/templates/` at repo root
- Any content that downstream users would consume

## Currently populated

*(None — internal templates are created as maintenance patterns emerge and are worth formalizing.)*
