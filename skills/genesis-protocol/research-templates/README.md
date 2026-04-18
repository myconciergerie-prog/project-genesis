<!-- SPDX-License-Identifier: MIT -->
# Research templates — genesis-protocol in-skill R8 bundle

## Purpose

R8 cache templates bundled with the `genesis-protocol` skill for downstream
project seeding at Phase 2 Step 2.3. Decouples downstream R8 cache seed from
plugin-envelope filesystem topology — works identically across dogfood,
`--plugin-dir`, and personal-scope (`~/.claude/skills/`) install modes.

## Structure

```
research-templates/
├── README.md       ← this file
├── sota/           ← state-of-the-art entries (TTL 7d in downstream cache)
│   ├── claude-code-plugin-distribution.md
│   ├── claude-ecosystem-cross-os.md
│   └── spdx-headers.md
└── stack/          ← stack / version-pin entries (TTL 1d in downstream cache)
    ├── claude-code-plugin-structure.md
    └── claude-code-session-jsonl-format.md
```

## Filename convention

Skill-local templates **drop the `_YYYY-MM-DD` date suffix** common in project
R8 caches. Date traceability lives in the frontmatter (`created_at` +
`expires_at`). The skill version pin (see `.claude-plugin/plugin.json`) is the
freshness anchor for templates.

## Copy discipline (Phase 2 Step 2.3)

When `genesis-protocol` Phase 2 Step 2.3 seeds the downstream project's R8
cache, it performs a **copy-and-rename** : each template file is copied to the
downstream `.claude/docs/superpowers/research/{sota,stack}/` with the seed
date appended to the filename (per downstream R8 convention :
`<topic>_<ISO-seed-date>.md`). The destination frontmatter `created_at` is
updated to the seed date; `expires_at` follows the normal R8 TTL from the
seed date. The template's original timestamps are preserved in the source
for audit.

## Refresh policy

Templates are maintained in lockstep with plugin releases. When a template's
content deviates from current-best-practice (e.g. Anthropic API surface
change, new Claude Code plugin convention), refresh before the next plugin
release. Downstream projects can independently refresh their copies post-seed
using the normal R8 cache workflow (Layer 0 research discipline).

**Escape clause (v1.4.2)**: if a refresh would introduce a structural /
breaking change (not just content currency), route the change through a
MINOR release, not a PATCH. Templates that evolve structurally are
plugin-release-gated.

## Cross-references

- Spec: `.claude/docs/superpowers/specs/v1_4_2_marketplace_unblock.md`
- Phase 2 Step 2.3 runbook: `skills/genesis-protocol/phase-1-rules-memory.md`
- R8 cache convention: Layer 0 `~/.claude/memory/layer0/workflow_research_and_memory.md`
