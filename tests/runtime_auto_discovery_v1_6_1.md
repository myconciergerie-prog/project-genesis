<!-- SPDX-License-Identifier: MIT -->
---
name: Runtime auto-discovery validation — v1.6.1
description: Reproducible runbook + evidence log for validating that the promptor skill surfaces in a fresh Claude Code session in a sibling project, on trigger-phrase input. Executed once in Phase B of v1.6.1 ship; future v1.6.x+ sessions can re-run the procedure to re-validate after any skill-description or binding-rule change.
type: test
created: 2026-04-19
---

# Runtime auto-discovery — v1.6.1

## Procedure

1. **Spawn context**
   - Open a fresh Claude Code session in a sibling project cwd (any Genesis-bootstrapped repo on this machine **except** `project-genesis` itself to avoid in-repo discovery bias).
   - Candidates on this machine : Aurum (frozen read-only OK per `memory/project/aurum_frozen_scope_lock.md` additive-only clause), Cyrano, Myconciergerie.
   - Ensure the Project Genesis plugin is installed at user scope or via `--plugin-dir` pointing at this repo. The `promptor` skill must be reachable by the fresh session.
   - **No Edit / Write / commit** during the validation session (read-only mode, additive-only clause respected for Aurum).

2. **Trigger**
   - Type ONE of the verbatim trigger phrases from the v1.6.0 binding rule, then wait for Claude's first response turn (do not interact after) :
     - `aide-moi à drafter un prompt pour claude opus 4.7 pour un agent extracteur`
     - `architecture un prompt production-grade pour [use case concret]`
     - `optimise ce prompt pour KV cache`
     - `reverse-engineere un prompt optimal pour [tâche stricte]`

3. **Observe**
   - Did Claude auto-invoke the `promptor` skill via the Skill tool ? (observable as a visible tool-use block in the transcript)
   - If invoked : at what form — bare `promptor`, namespaced `project-genesis:promptor`, or other ?
   - If not invoked : was it offered as candidate ? Did Claude explicitly reference the skill ?
   - Did Claude produce the Phase 1 standby card verbatim (2 questions, STOP, awaiting engineer specs) ? Or did it jump to Phase 2 creation without acquiring specs ?

4. **Capture evidence**
   - Copy the relevant transcript excerpt (user prompt + Claude's first ~2 turns, including any tool-use blocks).
   - Redact project-specific identifiers (absolute paths, API keys, user emails, project-internal naming, third-party service tokens).
   - Preserve trigger phrase verbatim + skill reference verbatim.
   - Paste into § Evidence below.

5. **Decision routing (spec AC#7)**
   - **Option A — Bare `promptor` surfaces reliably** → keep binding rule non-pinned (v1.6.0 status). Add a "runtime validated 2026-04-19" note to Layer 0 `feedback_invoke_promptor_for_production_anthropic_prompts.md` § "The rule" body.
   - **Option B — Namespaced form required** → pin `project-genesis:promptor` in § "The rule" + sync note in `skills/promptor/SKILL.md` frontmatter description.
   - **Option C — Mixed / context-dependent** → document both-surface precedence in § "The rule" (bare preferred ; namespaced fallback on misses).

## Evidence

> **Spawn cwd** : (fill at Phase B execution — e.g. `C:/Dev/Claude_cowork/myconciergerie/`)
>
> **Trigger phrase typed** : (fill verbatim)
>
> **Skill surfacing** : (fill : bare / namespaced / both / absent)
>
> **Phase 1 standby card rendered** : (fill : yes / no / partial)
>
> **Transcript excerpt (redacted)** :
>
> ```
> (fill with ≤ 30-line excerpt, identifiers redacted)
> ```

## Pinning decision

> (fill at Phase B execution — Option A / B / C, with one-sentence rationale citing the evidence above)

## Re-run guidance

A future v1.6.x+ session can re-run this runbook to re-validate auto-discovery after any of these changes :

- Skill `description` frontmatter edit in `skills/promptor/SKILL.md`
- Trigger-phrase list edit in Layer 0 `feedback_invoke_promptor_for_production_anthropic_prompts.md`
- Claude Code harness or skill-discovery engine upgrade (per `research/stack/claude-code-plugin-structure_<date>.md` refresh)
- New sibling project bootstrapped via Genesis (validates discovery in the bootstrapped context)

Append a new § Evidence block dated accordingly ; do not overwrite the v1.6.1 validation.
