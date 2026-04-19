<!-- SPDX-License-Identifier: MIT -->
---
name: Runtime dogfood evidence log — v1.6.2
description: Per-fixture runtime observations from 5 automated `claude -p` subprocess runs (4 v1.5.0 dryrun fixtures + 1 alexandre_windows) + 1 explicit-invocation control + 1 post-`plugin disable` control. Runtime dogfood method was automated via `claude -p --plugin-dir <worktree>` subprocess calls from driver session to avoid manual 5-session spawns. Methodology gap surfaced : `--plugin-dir` does NOT shadow a stale user-scope cached install of the same-named plugin — even `claude plugin disable` leaves the cache loading its skill list at `--plugin-dir` invocation time. H1-H4 hypotheses thus UNABLE-TO-TEST in this harness configuration ; H5 zero-Layer-B-ripple CONFIRMED. Self-rating drops vs projection to reflect that the pain-driven target (runtime skill validation) was NOT attained, though a different pain (methodology gap) was surfaced. Streak ≥ 9.0 breaks with this ship per Layer 0 honesty discipline.
---

# Runtime dogfood evidence log — v1.6.2

**Driver session** : v1.6.2 feat branch `feat/v1.6.2-runtime-dogfood`.
**Phase A commit** : `db0749f` (initial stub with 5 placeholder fixture sections + runbook + master.md depth).
**Phase B filling** : this commit, `feat-runtime(v1.6.2)`.
**Method** : 5 + 2 subprocess runs via `claude -p --plugin-dir <worktree> --output-format=json --dangerously-skip-permissions "<trigger phrase>"`. Verbatim JSON outputs archived at `C:/tmp/v1.6.2-runs/` (not committed to repo — `.gitignore`-equivalent by location).

---

## Per-fixture observations

### Fixture scenario_halt_no_key (EXIT_NO_KEY test — `C:/tmp/genesis-v1.5.0-dryrun/scenario_halt_no_key/`)

- **Trigger phrase used :** `"aide-moi à bootstrap ce projet depuis ce dossier"` (natural French, `-p` mode, subprocess env stripped of `ANTHROPIC_API_KEY` via `env -u`).
- **Invocation form observed :** NONE — no `/genesis-drop-zone` skill dispatch. Spawned Claude freelanced its own domain-consultant response.
- **Cards rendered :** None from the skill. Instead a freelance Q&A asking "dogfood mode / real bootstrap / debug mode" as clarification.
- **Artefacts written :** None in the fixture cwd (`ls -la` post-run : unchanged).
- **Frictions found :** Skill `genesis-drop-zone` did NOT auto-surface on natural phrase. Separately, spawned Claude clearly recognized the dryrun-scenario context (named scenario_halt_no_key explicitly in response) from Layer 0 memory, but chose freelance Q&A over skill dispatch. **H4 NOT tested** since skill wasn't invoked.

Runtime JSON : `/c/tmp/v1.6.2-runs/run_halt_no_key.json` — duration 56.7 s, 6 turns, $0.33.

### Fixture scenario_first_write (multi-file happy-start dispatch — `C:/tmp/genesis-v1.5.0-dryrun/scenario_first_write/`)

- **Trigger phrase used :** `"aide-moi à bootstrap ce projet depuis ce dossier"`.
- **Invocation form observed :** NONE — no `/genesis-drop-zone` dispatch. Spawned Claude generated a freelance "consent card" (format similar to Layer B `genesis-protocol` consent card, but invented, not dispatched).
- **Cards rendered :** Custom "Genesis orchestrator — consent card" with freelance field set (Target folder / Project slug / Repo visibility / etc.). NOT the Phase 0.1 welcome card from `genesis-drop-zone/phase-0-welcome.md`.
- **Artefacts written :** None (session exited via `-p` single-shot).
- **Frictions found :** Same as halt_no_key — skill not dispatched on natural phrase. **H1 NOT validly refuted** since we cannot distinguish skill-loading failure from auto-surface failure without isolating the plugin.

Runtime JSON : `/c/tmp/v1.6.2-runs/run_first_write.json` — duration 77.4 s, 9 turns, $0.39.

### Fixture scenario_retirement (re-run / supersession scenario — `C:/tmp/genesis-v1.5.0-dryrun/scenario_retirement/`)

- **Trigger phrase used :** `"aide-moi à bootstrap ce projet depuis ce dossier"`.
- **Invocation form observed :** NONE.
- **Cards rendered :** Freelance arbitrage table ("Phase 0 pré-consent — arbitrage avant le consent card") contrasting 3 input artefacts (config.txt / existing drop_zone_intent.md / brief.md). Rich analysis of budget-visibility-users contradictions. **NOT rendered from the skill** — freelance synthesis.
- **Artefacts written :** None.
- **Frictions found :** Worth noting that the freelance response DID surface the retirement-scenario pattern (existing snapshot vs new drop) — indicating Claude is cognitively capable of Phase 0.4-like arbitration even without skill dispatch. This is ambivalent for H2 : either (a) arbitration is "easy" for Claude and skill adds minimal value, OR (b) skill provides discipline/format that freelance lacks.

Runtime JSON : `/c/tmp/v1.6.2-runs/run_retirement.json` — duration 61.0 s, 7 turns, $0.35.

### Fixture scenario_halt_no_sdk (SDK-absent edge — now generic internal-error per v1.5.1 — `C:/tmp/genesis-v1.5.0-dryrun/scenario_halt_no_sdk/`)

- **Trigger phrase used :** `"aide-moi à bootstrap ce projet depuis ce dossier"`.
- **Invocation form observed :** NONE.
- **Cards rendered :** Freelance "Halt recommandé — ce projet n'a pas besoin de Genesis" table arguing disproportion between fixture scope (solo CSV→PNG script) and Genesis deliverables.
- **Artefacts written :** None.
- **Frictions found :** Same pattern — freelance Halt recommendation, not skill dispatch. The "halt" is Claude's own judgment, not EXIT_* exit-code dispatch.

Runtime JSON : `/c/tmp/v1.6.2-runs/run_halt_no_sdk.json` — duration 53.9 s, 7 turns, $0.33.

### Fixture alexandre_windows (full happy-path target — `C:/tmp/genesis-v1.6.2-alexandre/`)

- **Trigger phrase used :** `"aide-moi à bootstrap ce projet depuis ce dossier"`.
- **Invocation form observed :** NONE — no `/genesis-drop-zone` dispatch.
- **Cards rendered :** Rich freelance "Step 0 — Top-level consent card" with extracted multi-source Alexandre data :
  - Produit identified ("SaaS devis-fenêtre instantané")
  - Pain-point identified ("cycle devis 1 semaine FR↔PL")
  - Business tier extracted (ALU premium 520-1280 €/m², PVC 180-420, bois 680-1450)
  - Factory constraint extracted (MOQ 8 pièces RAL 9005 mat, triple vitrage +2 semaines, EN 14351-1, ISO 9001 PL-QC-9042)
  - Synthesized a consent card with DEFAULT proposals (project slug, GitHub owner, Chrome profile, PAT scopes)
- **Artefacts written :** None (single-shot `-p`).
- **Frictions found :** Claude demonstrated STRONG multi-source arbitration capability via freelance reasoning, drawing coherently from all 4 text artefacts (skipping the JPG per our expectation). The content is PROPER arbitration-quality, but format is Claude's freelance invention, not the skill's Phase 0.4 card schema.

Runtime JSON : `/c/tmp/v1.6.2-runs/run_alexandre.json` — duration 146.1 s, 12 turns, $1.03.

---

## Control runs (diagnostic, not counted in AC6 H1 table)

### Control #1 — explicit `/genesis-drop-zone` invocation (cwd `C:/tmp/genesis-v1.6.2-alexandre/`)

- **Trigger phrase used :** `"invoque /genesis-drop-zone sur le dossier courant"`.
- **Observation :** Spawned Claude response : **"Le skill `genesis-drop-zone` n'existe pas dans ton harness. Les skills genesis disponibles sont : genesis-protocol / phase-5-5-auth-preflight / phase-minus-one."**
- **Diagnostic :** These 3 skills match the v1.1.0 user-scope plugin install at `C:/Users/conta/.claude/plugins/cache/project-genesis-marketplace/project-genesis/1.1.0/skills/`. Confirmed : `--plugin-dir` is NOT loading the 8-skill worktree — the stale v1.1.0 cached install's skill list is surfacing instead.

Runtime JSON : `/c/tmp/v1.6.2-runs/run_control_explicit.json` — duration 23.4 s, 9 turns, $0.23.

### Control #2 — same invocation after `claude plugin disable project-genesis`

- **Trigger phrase used :** `"liste les skills genesis disponibles dans ton harness"`.
- **Observation :** Spawned Claude listed 6 skills : genesis-protocol / journal-system / pepite-flagging / phase-5-5-auth-preflight / phase-minus-one / session-post-processor. **Still NOT `genesis-drop-zone` nor `promptor`.**
- **Diagnostic :** Disabling the plugin does NOT unload its skill list from the cache at `--plugin-dir` invocation time. The 6 surfaced skills match those physically present at `cache/.../1.1.0/skills/` — confirming Claude Code's plugin-skill-indexer preserves a stale view even across `--plugin-dir` override + `plugin disable`.

Runtime JSON : `/c/tmp/v1.6.2-runs/run_post_disable_list.json` — duration 5.8 s, 1 turn, $0.12.

---

## H1 — dispatch evidence table

| Fixture | Dispatch | Invocation form (verbatim) |
|---|---|---|
| scenario_halt_no_key | **unable-to-test** | none observed — skill not surfaced due to F1 methodology blocker |
| scenario_first_write | **unable-to-test** | none observed — F1 blocker |
| scenario_retirement | **unable-to-test** | none observed — F1 blocker |
| scenario_halt_no_sdk | **unable-to-test** | none observed — F1 blocker |
| alexandre_windows | **unable-to-test** | none observed — F1 blocker |

## H2-H5 global hypothesis rows

| H | Hypothesis | Observation |
|---|---|---|
| H1 | Claude Code skill engine dispatches `/genesis-drop-zone` on verbatim trigger phrase in each of the 5 fixture cwds | **UNABLE-TO-TEST** — F1 methodology blocker (see Frictions). 5 natural-phrase runs all freelanced. Explicit-invocation control confirmed skill not loaded from worktree. Deferred to v1.6.3 with proper harness. |
| H2 | Phase 0.4 arbitration on alexandre_windows renders `arbitrated_fields` list non-empty | **UNABLE-TO-TEST** formally — but freelance evidence shows Claude CAN synthesize multi-source Alexandre arbitration coherently (RAL 9005 + MOQ 8 + EN 14351-1 + Uw range + 3 pricing tiers extracted). Ambivalent signal : either skill adds minimal incremental value over freelance OR skill's format discipline is the real deliverable. Resolve at v1.6.3. |
| H3 | Phase 0.5 Path 2a (first-write empty-divergences) renders v1.3.2 consent card on at least 1 fixture | **UNABLE-TO-TEST** — no skill dispatch, no Phase 0.5 Path rendered. Deferred. |
| H4 | Fixture scenario_halt_no_key with ANTHROPIC_API_KEY unset renders EXIT_NO_KEY halt card | **UNABLE-TO-TEST** formally — skill didn't dispatch so halt path not exercised. Freelance response correctly detected the halt-no-key scenario intent but didn't render the skill's halt card (with the v1.5.1 updated remediation content). Deferred. |
| H5 | `git diff --name-only main...feat/v1.6.2-runtime-dogfood` shows zero Layer B files modified | **CONFIRMED** — AC10 grep pipeline returns 0 (verified at Phase A pre-commit + verified again before this feat-runtime commit). Pattern #4 depth-update on sixth data-point still valid (Layer A-only ship). |

## Friction triage (§ 4.3 hybrid gate)

| Friction # | Class | Description | Disposition |
|---|---|---|---|
| F1 | B (prose / methodology ambigu) | `claude --plugin-dir <path>` does NOT override a same-named stale cached plugin install. Even `claude plugin disable <name>` does not prevent the cache's skill list from surfacing. Runbook needs a pre-flight step : either (a) `claude plugin uninstall <name>` first, OR (b) use `--bare` with `ANTHROPIC_API_KEY` env-var set, OR (c) publish new version and `claude plugin update` first. This is ARGUABLY a Claude Code CLI bug, not a Genesis bug — but the runbook must document the workaround regardless. | **DEFERRED v1.6.3** — runbook methodology fix. Ship path : update runbook Pre-flight section + add `claude plugin uninstall` instruction + re-run evidence capture against true-isolated harness. |
| F2 | B (observation) | `-p` single-shot mode cannot exercise multi-turn skill flows (Phase 0.1 → 0.2 → 0.3 → 0.4 → 0.5). Even with F1 fixed, single-shot reveals only first-card render. Phase 0.4 arbitration + Phase 0.5 consent need interactive or `--input-format stream-json` multi-turn. | **DEFERRED v1.6.3+** — either (a) manual interactive sessions (the originally-planned method user-work), (b) scripted stream-json multi-turn via subprocess-managed pipes. |
| F3 | C (observation / insight) | Freelance Claude on natural phrase produces rich arbitration-quality content without skill dispatch — especially on the alexandre_windows multi-source drop (extracted 4 fixture artefacts into a coherent consent card). Implication : the skill's value-add over freelance should be explicitly characterized. Not a bug, but a product-clarity question. | **DEFERRED** — candidate for v2 design conversation ("when does invoking the skill improve over freelance Claude?"). |

## Deferred-friction queue (B + C → v1.6.3+)

| Friction # | Proposed ship | Reason for defer |
|---|---|---|
| F1 | v1.6.3 — runbook methodology fix | Ship v1.6.3 as "runtime dogfood harness fix + re-run H1-H4 evidence capture against isolated plugin load" |
| F2 | v1.6.3 or later | Ties into F1 resolution ; multi-turn evidence capture can be scripted only after single-turn works |
| F3 | v2 design conversation | Product-positioning question, not a bug |

---

## Cost + time summary

- 5 fixture runs : $2.43, ~394 s total (6.6 min)
- 2 control runs : $0.35, ~30 s total
- **Grand total : $2.78, ~424 s (7.1 min)**

Evidence gathering cost well within reasonable budget for a runtime dogfood ship. Future v1.6.3 with F1 fix should run at similar cost (plus one uninstall + reinstall step, negligible).
