<!-- SPDX-License-Identifier: MIT -->

# templates/

Reusable templates that Project Genesis ships for downstream projects to adopt. This is the **plugin-root `templates/`** — the content that users consume when they bootstrap a new project via Genesis. Distinct from `.claude/docs/superpowers/templates/` which holds dev-internal templates for Genesis itself.

## Planned templates for v1.0.0

- **`genesis-protocol.md`** — the canonical 7-phase protocol markdown. This is what a user drops into a fresh folder alongside their `config.txt` seed, then runs `claude` + invokes Genesis. Contains the Phase -1 → Phase 7 flow with the 3-mode ladder, the magical one-liner reference, and the multidevice core.
- **`phase-minus-one-install-manifest.yaml`** — target stack with per-OS install commands (Windows winget, macOS brew, Linux apt/dnf/pacman). Consumed by the `phase-minus-one` skill to drive the autonomous install pass.
- **`v1_rules-starter.md`** — the R1-R10 starting rule set, adaptable per project at Phase 3 rules alignment. Includes the adaptation scoreboard format from the Genesis v1 bootstrap session.
- **`memory-architecture.md`** — reference layout for a new project's `memory/` directory with the 7 memory types (user / feedback / project / reference / themes / journal / pepites).
- **`env-local.example.tmpl`** — secrets template with common placeholder slots (GH_TOKEN, Supabase keys, OpenAI / Anthropic / Gemini API keys, etc.). Downstream projects copy this to `.env.local.example` and customize.
- **`gitignore-starter.tmpl`** — canonical `.gitignore` with secrets patterns, OS files, editor files, language artefacts, and `.claude/worktrees/` exclusion per R2.5.
- **`readme-bilingual.tmpl`** — bilingual FR + EN README skeleton per R9 language policy (public docs are bilingual).

Lands at **Étape 5** of the v1 bootstrap session, inside a worktree.

## How downstream projects use these

After Genesis is installed as a plugin (`/plugin install project-genesis@myconciergerie-prog/project-genesis`), a user in a fresh folder with a `config.txt` runs Genesis. The `genesis-protocol` skill reads `config.txt`, runs Phase 0 sanity check, and at Phase 5 bootstrap copies / instantiates the templates above into the new project's directory structure.

Users are free to modify the instantiated templates — Genesis is an opinionated starter, not a lock-in.
