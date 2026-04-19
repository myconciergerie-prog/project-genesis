<!-- SPDX-License-Identifier: MIT -->
---
name: v1.6.2 Runtime dogfood — implementation plan
description: Phase A (autonomous pre-runtime) + Phase B (autonomous post-runtime) + Phase C (ship) + Phase D (conditional Layer 0) + Phase E (chore). Bite-sized tasks with exact paths, commands, expected output. Spec at `.claude/docs/superpowers/specs/v1_6_2_runtime_dogfood.md`. Phase A is fully autonomous — halts at runtime gate where user spawns 5 fresh Claude Code sessions per runbook. Phase B resumes autonomously once evidence pasted.
type: plan
spec: .claude/docs/superpowers/specs/v1_6_2_runtime_dogfood.md
version: v1.6.2
---

# v1.6.2 Runtime Dogfood — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to execute this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Close the v1.5.0 paper-trace dogfood debt via runtime evidence captured from 5 fresh Claude Code sessions (4 v1.5.0 fixtures dispatch-only + 1 new `alexandre_windows` full happy-path).

**Architecture:** Layer A-only session. Fixture prep + runbook + evidence log under `skills/genesis-drop-zone/tests/`. New Alexandre fixture at `C:/tmp/genesis-v1.6.2-alexandre/`. Zero Layer B ripple enforced by AC10 diff check. Real Anthropic Messages API subprocess calls on 4 fixtures ; EXIT_NO_KEY halt card runtime on Fixture A. Hybrid blocker gate (class A in-feat / B+C defer).

**Tech Stack:** Claude Code plugin (8 skills), Python 3.10+ for fixture Pillow image gen, bash (Windows git-bash) for AC checks, `gh` CLI for PR.

---

## File structure (Phase A edits)

```
.claude/worktrees/feat_2026-04-19_v1_6_2_runtime_dogfood/
├── .claude-plugin/plugin.json                             ← version bump
├── .claude/docs/superpowers/
│   ├── specs/v1_6_2_runtime_dogfood.md                    ← already landed (spec + spec-polish commits)
│   └── plans/v1_6_2_runtime_dogfood.md                    ← THIS FILE
├── memory/master.md                                       ← pattern #4 depth-update
└── skills/genesis-drop-zone/
    └── tests/
        ├── runtime_dogfood_v1_6_2.md                      ← runbook (new, reusable)
        └── runtime_dogfood_evidence_v1_6_2.md             ← evidence log (stubs filled Phase A, data filled Phase B)
```

And external to worktree :
```
C:/tmp/genesis-v1.6.2-alexandre/
├── config.txt
├── catalogue_fenetres_fr.md
├── specs_usine_pl.md
├── voice_memo_alexandre.txt
└── photo_facade_client.jpg
```

---

## Phase A — Autonomous pre-runtime (spec/plan already landed)

### Task A0: Plan-polish gate

- [ ] **Step 1: Dispatch plan-reviewer agent**

Agent tool, subagent_type=code-reviewer. Prompt references this plan file + spec file. Report P0/P1/P2/P3 + approval.

- [ ] **Step 2: Apply P1 + P2 fixes in polish commit**

One `plan-polish(v1.6.2)` commit per v1.6.1 precedent. P3s optional bundle.

- [ ] **Step 3: Idempotency — grep for polish marker before committing**

```bash
cd "C:/Dev/Claude_cowork/project-genesis/.claude/worktrees/feat_2026-04-19_v1_6_2_runtime_dogfood"
git log --oneline feat/v1.6.2-runtime-dogfood | grep -c "plan-polish(v1.6.2)"
```
Expected pre-commit: `0`. Post-commit: `1`.

### Task A1: Create Alexandre fixture directory + 5 artefacts

**Files:**
- Create: `C:/tmp/genesis-v1.6.2-alexandre/config.txt`
- Create: `C:/tmp/genesis-v1.6.2-alexandre/catalogue_fenetres_fr.md`
- Create: `C:/tmp/genesis-v1.6.2-alexandre/specs_usine_pl.md`
- Create: `C:/tmp/genesis-v1.6.2-alexandre/voice_memo_alexandre.txt`
- Create: `C:/tmp/genesis-v1.6.2-alexandre/photo_facade_client.jpg`

- [ ] **Step 1: Verify `C:/tmp/` exists + create subdir**

```bash
test -d /c/tmp && mkdir -p /c/tmp/genesis-v1.6.2-alexandre
ls -la /c/tmp/genesis-v1.6.2-alexandre
```
Expected : directory exists, empty.

- [ ] **Step 2: Write `config.txt` (FR, 3-4 lines)**

Write via Write tool. Content :
```
Projet : SaaS devis-fenêtre instant pour commercial terrain.
Client : Alexandre, Paris. Usine partenaire : Pologne.
Objectif : devis immédiat dès 1ère visite client (vs 1 semaine actuel).
Bonus : montrer rendu produit depuis photo façade client.
```

- [ ] **Step 3: Write `catalogue_fenetres_fr.md` (FR, ~30 lines)**

Fake catalogue structure : sections matériaux (PVC / Alu / Bois), dimensions standard (cm), options (double/triple vitrage, argon, bas-émissif), finitions (RAL standard, bois chêne/sapin). Prix indicatifs HT €.

- [ ] **Step 4: Write `specs_usine_pl.md` (PL + EN technique, ~15 lines)**

Fake Polish factory specs : `## Produkcja`, `## Standardy`, `## Uwaga techniczna` headers ; body mixes Polish narrative + English technical tokens (U-value, Uw coefficient, CE marking).

- [ ] **Step 5: Write `voice_memo_alexandre.txt` (FR informel, ~10 lines)**

Transcript-style voice memo : Alexandre parle à Claude en FR informel ("bon donc tu vois j'ai 3 clients cette semaine qui veulent du alu en noir RAL 9005 et le problème c'est que chaque fois je dois repasser par la Pologne et ça prend 1 semaine").

- [ ] **Step 6: Generate valid JPG with Pillow (≥ 5 KB, JFIF-headered)**

```bash
python -c "from PIL import Image, ImageDraw; im=Image.new('RGB',(400,300),(200,220,240)); d=ImageDraw.Draw(im); d.rectangle([50,50,350,250],outline=(50,50,50),width=3); d.rectangle([80,80,190,220],fill=(180,200,220)); d.rectangle([210,80,320,220],fill=(180,200,220)); im.save('/c/tmp/genesis-v1.6.2-alexandre/photo_facade_client.jpg','JPEG',quality=85)"
ls -l /c/tmp/genesis-v1.6.2-alexandre/photo_facade_client.jpg
```
Expected : file exists, size ≥ 5000 bytes.

- [ ] **Step 7: Verify all 5 files exist, sizes > 0 (AC4)**

```bash
ls -l /c/tmp/genesis-v1.6.2-alexandre/
```
Expected : 5 files, all sizes > 0.

### Task A2: Write runbook stub (reusable)

**Files:**
- Create: `skills/genesis-drop-zone/tests/runtime_dogfood_v1_6_2.md`

- [ ] **Step 1: Check tests/ directory exists in skill**

```bash
cd "C:/Dev/Claude_cowork/project-genesis/.claude/worktrees/feat_2026-04-19_v1_6_2_runtime_dogfood"
test -d skills/genesis-drop-zone/tests && echo EXISTS || (mkdir skills/genesis-drop-zone/tests && echo CREATED)
```

- [ ] **Step 2: Write runbook with 4 sections (AC2)**

Sections minimum :
1. Pre-flight (API key check, Claude Code version check, git status clean in fixture cwd)
2. Per-fixture spawn + trigger + observe procedure (5 steps per fixture : cd / ensure env / spawn `claude` / type trigger phrase / capture)
3. Redaction rules (7 regexes from spec § 4.2 #6, mirrored verbatim)
4. Re-run guidance (how to re-run after class-A fix)

- [ ] **Step 3: Verify runbook has ≥ 4 top-level `##` sections (AC2)**

```bash
grep -c "^##[^#]" skills/genesis-drop-zone/tests/runtime_dogfood_v1_6_2.md
```
Expected : ≥ 4.

### Task A3: Write evidence log stub (session-specific)

**Files:**
- Create: `skills/genesis-drop-zone/tests/runtime_dogfood_evidence_v1_6_2.md`

- [ ] **Step 1: Write evidence log with 5 fixture sections**

Each `### Fixture <name>` section contains empty placeholders :
```markdown
### Fixture alexandre_windows
- **Trigger phrase used :** TBD at runtime
- **Invocation form observed :** TBD
- **Cards rendered :** TBD
- **Artefacts written :** TBD
- **Frictions found :** TBD
```

Plus global tables :
- H1 table : 5 rows (one per fixture) with format `| fixture_<name> | dispatch (confirmed|failed|deferred) | <verbatim-invocation-form> |`
- H2/H3/H4/H5 rows with TBD values
- Friction triage table (empty, headers : class A / B / C / description / disposition)
- Deferred-friction queue (empty)

- [ ] **Step 2: Verify `^### Fixture` count = 5 (AC3)**

```bash
grep -c "^### Fixture" skills/genesis-drop-zone/tests/runtime_dogfood_evidence_v1_6_2.md
```
Expected : `5`.

### Task A4: Bump plugin.json

**Files:**
- Modify: `.claude-plugin/plugin.json`

- [ ] **Step 1: Read current version**

```bash
jq -r .version .claude-plugin/plugin.json
```
Expected : `1.6.1`.

- [ ] **Step 2: Edit `"version": "1.6.1"` → `"version": "1.6.2"`**

Use Edit tool, `old_string="\"version\": \"1.6.1\""`, `new_string="\"version\": \"1.6.2\""`.

- [ ] **Step 3: Verify (AC5)**

```bash
jq -r .version .claude-plugin/plugin.json
```
Expected : `1.6.2`.

### Task A5: Master.md pattern #4 depth-update on sixth data-point

**Files:**
- Modify: `memory/master.md` (single paragraph in § "Cross-skill patterns ... 4. Layer A / Layer B stratification")

- [ ] **Step 1: Locate the eighth-data-point paragraph**

```bash
grep -n "Eighth data-point" memory/master.md
```
Expected : 1 line match ~ line 95.

- [ ] **Step 2: Append sentence after the eighth data-point note, marking v1.6.2 as a depth update on the sixth data-point**

Use Edit tool. `old_string` = last sentence of the eighth-data-point block (specifically the sentence ending with "SOTA-driven template rework."). `new_string` = same sentence + appended sentence :

```
**v1.6.2 depth update on the sixth data-point** (no new ordinal) — Layer A-only runtime-evidence capture session ships with zero Layer B ripple per AC10 machine check. Structurally the same ripple class as v1.5.1 Layer A-only corrections (sixth data-point) : the work differs (runtime evidence vs paper-trace / prose correction) but the ripple is identical (zero Layer B diff line). Per v1.6.1 precedent (pattern #1 depth update on fourth, no new ordinal), same-ripple-class extension is a depth update, not a new ordinal. A ninth data-point remains reserved for a genuinely new ripple mode.
```

- [ ] **Step 3: Verify (AC12)**

```bash
grep -c "depth update on the sixth data-point" memory/master.md
```
Expected : ≥ 1.

### Task A6: Pre-commit zero Layer B ripple check (AC10)

- [ ] **Step 1: Run the AC10 grep pipeline**

```bash
cd "C:/Dev/Claude_cowork/project-genesis/.claude/worktrees/feat_2026-04-19_v1_6_2_runtime_dogfood"
git diff --name-only main...HEAD \
  | grep -v '^skills/genesis-drop-zone/' \
  | grep -v '^\.claude-plugin/plugin\.json$' \
  | grep -vE '^\.claude/docs/superpowers/(specs/v1_6_2_runtime_dogfood\.md|resume/2026-04-19_v1_6_2.*|plans/v1_6_2_runtime_dogfood\.md|research/INDEX\.md)$' \
  | grep -vE '^memory/(project/session_v1_6_2.*|MEMORY\.md|master\.md)$' \
  | grep -v '^CHANGELOG\.md$' \
  | wc -l
```
Expected : `0`.

If non-zero, list offending paths and abort Phase A commit. Investigate whether the edit was legitimate (Layer A paths missed in whitelist) or accidental (Layer B ripple).

### Task A7: feat-core commit

- [ ] **Step 1: Stage all Phase A files**

```bash
git add .claude-plugin/plugin.json
git add .claude/docs/superpowers/plans/v1_6_2_runtime_dogfood.md
git add memory/master.md
git add skills/genesis-drop-zone/tests/runtime_dogfood_v1_6_2.md
git add skills/genesis-drop-zone/tests/runtime_dogfood_evidence_v1_6_2.md
```

- [ ] **Step 2: Commit with feat-core message**

```bash
git commit -m "$(cat <<'EOF'
feat-core(v1.6.2): runtime dogfood prep — runbook + evidence stub + fixture + master.md depth

Phase A pre-runtime commit. Creates :
- skills/genesis-drop-zone/tests/runtime_dogfood_v1_6_2.md (reusable runbook)
- skills/genesis-drop-zone/tests/runtime_dogfood_evidence_v1_6_2.md (evidence stub, 5 fixtures)
- .claude-plugin/plugin.json bump 1.6.1 → 1.6.2
- memory/master.md pattern #4 depth-update on sixth data-point

Alexandre fixture at C:/tmp/genesis-v1.6.2-alexandre/ (5 artefacts, external to repo per R2.5).

Zero Layer B ripple verified by AC10 grep pipeline (pre-commit).
H1-H5 evidence rows remain TBD ; Phase B fills post-runtime.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

- [ ] **Step 3: Verify commit landed**

```bash
git log --oneline feat/v1.6.2-runtime-dogfood | head -4
```
Expected : 3 commits (spec, spec-polish, feat-core).

---

## Phase A exit — HALT at runtime gate

After Task A7 commits, print the exit card :

```
────────────────────────────────────────────────────────────
PHASE A COMPLETE — RUNTIME GATE

Next step is manual (user action required).

Please spawn 5 fresh Claude Code sessions, one per fixture cwd :

  1. cd C:/tmp/genesis-v1.5.0-dryrun/fixture_A && claude
     (this fixture : ANTHROPIC_API_KEY MUST be unset — see runbook Pre-flight)
  2. cd C:/tmp/genesis-v1.5.0-dryrun/fixture_B && claude
  3. cd C:/tmp/genesis-v1.5.0-dryrun/fixture_C && claude
  4. cd C:/tmp/genesis-v1.5.0-dryrun/fixture_D && claude
  5. cd C:/tmp/genesis-v1.6.2-alexandre/ && claude

Runbook at :
  skills/genesis-drop-zone/tests/runtime_dogfood_v1_6_2.md

Per fixture : follow "Per-fixture spawn + trigger + observe" section.
Redact per "Redaction rules" section before pasting back.

Paste back to THIS session the redacted per-fixture evidence
(trigger phrase used, invocation form observed, cards rendered,
artefacts written, frictions found). I will then resume Phase B
autonomously : fill evidence log, hybrid gate triage, commit
feat-runtime, PR, tag, chore.
────────────────────────────────────────────────────────────
```

---

## Phase B — Autonomous post-runtime (resumes once evidence pasted)

### Task B1: Parse user-pasted evidence + idempotency check

- [ ] **Step 1: Verify evidence log not already filled**

```bash
cd "C:/Dev/Claude_cowork/project-genesis/.claude/worktrees/feat_2026-04-19_v1_6_2_runtime_dogfood"
grep -c "TBD at runtime" skills/genesis-drop-zone/tests/runtime_dogfood_evidence_v1_6_2.md
```
Expected pre-Phase-B : ≥ 5 (stubs unfilled). Expected post-Phase-B : `0`.

- [ ] **Step 2: If count < 5 pre-Phase-B, abort — evidence log already partially/fully filled, investigate**

### Task B2: Fill evidence log per fixture

**Files:**
- Modify: `skills/genesis-drop-zone/tests/runtime_dogfood_evidence_v1_6_2.md`

- [ ] **Step 1: For each of 5 fixtures, replace TBD stubs with redacted user-pasted content**

Use Edit tool per fixture. Keep user-pasted content verbatim (already redacted per runbook). If any TBD remains unaddressed for a fixture, mark it `DEFERRED - <reason>` rather than leaving `TBD`.

- [ ] **Step 2: Fill H1-H5 global table rows**

Per spec § AC6-AC10 formats. H1 rows shape `| fixture_<name> | dispatch (confirmed|failed|deferred) | <verbatim-invocation-form> |`. H5 row = AC10 grep result.

- [ ] **Step 3: Populate friction triage table**

Classify each observed friction into class A/B/C per § 4.3. Class A → record with proposed fix path. Class B+C → record with proposed deferred ship (v1.6.3+).

- [ ] **Step 4: Verify evidence integrity gate (§ 4.5.1)**

Every H1-H5 row has at least one observation (confirmed / failed / deferred-with-reason). No empty cells.

```bash
grep -cE "^\| H[1-5] \| .+ \|" skills/genesis-drop-zone/tests/runtime_dogfood_evidence_v1_6_2.md
```
Expected : ≥ 5.

### Task B3: Hybrid gate triage

- [ ] **Step 1: Count class-A findings**

If 0 class-A → skip Task B4.
If 1-2 class-A → proceed Task B4.
If 3+ class-A with common root cause → ABORT v1.6.2 per § 5 common-root-cause abort. Write partial-evidence CHANGELOG + resume as v1.6.3 unified fix.
If 3+ class-A with distinct root causes → fix first 2 in Task B4, log 3rd+ as "immediate v1.6.3 PATCH chain" in evidence log.

### Task B4: Class-A fixes (if any)

**Files:**
- Modify: `skills/genesis-drop-zone/SKILL.md` and/or `skills/genesis-drop-zone/phase-0-welcome.md` (per observation)
- FORBIDDEN : `skills/genesis-drop-zone/scripts/extract_with_citations.py` per NG3

- [ ] **Step 1: Per class-A finding, apply prose/halt-card/consent-gate fix**

Each class-A fix = separate commit `fix-class-a(v1.6.2) #<n>`. Commit message references evidence log line and friction class rationale.

- [ ] **Step 2: Re-run AC10 grep**

```bash
git diff --name-only main...HEAD \
  | grep -v '^skills/genesis-drop-zone/' \
  | grep -v '^\.claude-plugin/plugin\.json$' \
  | grep -vE '^\.claude/docs/superpowers/(specs/v1_6_2_runtime_dogfood\.md|resume/2026-04-19_v1_6_2.*|plans/v1_6_2_runtime_dogfood\.md|research/INDEX\.md)$' \
  | grep -vE '^memory/(project/session_v1_6_2.*|MEMORY\.md|master\.md)$' \
  | grep -v '^CHANGELOG\.md$' \
  | wc -l
```
Expected : `0` still.

### Task B5: feat-runtime commit

- [ ] **Step 1: Stage evidence log**

```bash
git add skills/genesis-drop-zone/tests/runtime_dogfood_evidence_v1_6_2.md
```

- [ ] **Step 2: Commit**

```bash
git commit -m "$(cat <<'EOF'
feat-runtime(v1.6.2): evidence filled — H1-H5 per-fixture observations

Runtime evidence captured from 5 fresh Claude Code sessions per runbook.

Summary :
- H1 dispatch : <X confirmed / Y failed / Z deferred per fixture>
- H2 arbitration (alexandre_windows) : <arbitrated_fields present/absent>
- H3 Phase 0.5 Path 2a consent : <N fixtures confirmed>
- H4 EXIT_NO_KEY halt (Fixture A) : <rendered / not rendered>
- H5 zero Layer B ripple : AC10 grep = 0

Friction triage : <N class A / M class B / P class C>.
Class-A fixes committed separately (see log between feat-core and feat-runtime).

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Phase C — PR, squash merge, tag

### Task C1: Push feat branch + open PR

- [ ] **Step 1: Verify active gh account**

```bash
gh api user --jq .login
```
Expected : `myconciergerie-prog`. If `avelizy-cloud`, run `gh auth switch -u myconciergerie-prog` + use `GH_TOKEN` env override per R2.3.1.

- [ ] **Step 2: Push feat branch**

```bash
TOKEN=$(gh auth token -u myconciergerie-prog)
GH_TOKEN="$TOKEN" git push -u origin feat/v1.6.2-runtime-dogfood
```

- [ ] **Step 3: Open PR**

```bash
GH_TOKEN="$TOKEN" gh pr create \
  --title "v1.6.2 — runtime dogfood (PATCH)" \
  --body "$(cat <<'EOF'
## Summary

- Closes v1.5.0 paper-trace dogfood debt (2-cycle deferred) via runtime evidence from 5 fresh Claude Code sessions
- 4 v1.5.0 fixtures dispatch-only + 1 new alexandre_windows full happy-path (real Anthropic Messages API calls, Citations-enabled)
- Fixture A runs with ANTHROPIC_API_KEY unset → EXIT_NO_KEY halt card runtime-validated
- Hybrid blocker gate : class A → in-feat fix, B+C → defer v1.6.3
- Pattern #4 depth update on sixth data-point (Layer A-only ripple class, no new ordinal per v1.6.1 depth-update precedent)

## Test plan

- [ ] Phase A runbook + evidence stub + fixture + master.md depth-update all land in feat-core
- [ ] AC10 grep pipeline returns 0 (zero Layer B ripple)
- [ ] 5 fresh Claude Code sessions spawned per runbook, evidence redacted + pasted back
- [ ] H1-H5 all populated in evidence log
- [ ] Class-A findings (if any) fixed in separate commits before feat-runtime
- [ ] Self-rating honest post-feat : projected 9.14, streak ≥ 9.0 advances to 4 or honest deduction breaks streak with note

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

### Task C2: Squash merge PR

- [ ] **Step 1: Squash merge**

```bash
GH_TOKEN="$TOKEN" gh pr merge --squash --subject "v1.6.2 — runtime dogfood (PATCH)"
```
(No `--delete-branch` per R2.5 — branch retained forensic.)

- [ ] **Step 2: Pull + verify main head**

```bash
cd C:/Dev/Claude_cowork/project-genesis
git checkout main
git pull origin main
git log --oneline | head -2
```

### Task C3: Tag v1.6.2

- [ ] **Step 1: Create annotated tag on main**

```bash
git tag -a v1.6.2 -m "v1.6.2 — runtime dogfood (PATCH)"
```

- [ ] **Step 2: Push tag**

```bash
GH_TOKEN="$TOKEN" git push origin v1.6.2
```

- [ ] **Step 3: Verify**

```bash
git tag | tail -5
```
Expected chain : `... v1.5.0 v1.5.1 v1.6.0 v1.6.1 v1.6.2`.

---

## Phase D — Layer 0 sync (CONDITIONAL — AC13)

Only triggers if Phase B surfaced a third data-point confirming GH_TOKEN env-override pattern is needed for `gh pr create` mid-session (beyond `gh auth switch`).

### Task D1: Conditional Layer 0 amplification

- [ ] **Step 1: Check Phase B evidence log for GH_TOKEN-env-override observation**

```bash
grep -c "GH_TOKEN" skills/genesis-drop-zone/tests/runtime_dogfood_evidence_v1_6_2.md
```
If `0` → skip Phase D entirely.
If `≥ 1` → proceed D2.

- [ ] **Step 2: Amplify Layer 0 `workflow_github_and_tooling.md`**

Edit `~/.claude/memory/layer0/workflow_github_and_tooling.md` to encode `GH_TOKEN=$(gh auth token -u <user>)` prefix as **mandatory pre-flight** for write gh calls (not optional fallback).

- [ ] **Step 3: Write sentinel**

```bash
touch ~/.claude/memory/layer0/_v1_6_2_layer0_sync_DONE_2026-04-19.md
```

---

## Phase E — Chore (session documentation)

### Task E1: Create chore worktree

- [ ] **Step 1: Create chore worktree**

```bash
cd C:/Dev/Claude_cowork/project-genesis
git worktree add .claude/worktrees/chore_2026-04-19_v1_6_2_session -b chore/v1.6.2-session main
```

### Task E2: CHANGELOG entry (v1.6.2 honest 5-axis)

**Files:**
- Modify: `.claude/worktrees/chore_2026-04-19_v1_6_2_session/CHANGELOG.md`

- [ ] **Step 1: Add v1.6.2 entry above v1.5.1**

Include 5-axis honest rating, running-average delta, streak-status update. Match v1.5.1 / v1.6.1 entry structure.

### Task E3: Session trace

**Files:**
- Create: `memory/project/session_v1_6_2_runtime_dogfood.md`

- [ ] **Step 1: Write session trace mirroring v1.5.1 / v1.6.1 structure**

Sections : What shipped / Why / Architecture decisions / Reviewer P1+P2 summary / Self-rating honest / Cross-skill pattern data-points added / Hypothesis outcomes / Out-of-scope follow-ups / PR+tag state.

### Task E4: MEMORY.md pointer

**Files:**
- Modify: `memory/MEMORY.md`

- [ ] **Step 1: Add single-line entry under appropriate section**

Max 150 chars. Points to `session_v1_6_2_runtime_dogfood.md`.

### Task E5: Resume prompt

**Files:**
- Create: `.claude/docs/superpowers/resume/2026-04-19_v1_6_2_to_next.md`

- [ ] **Step 1: Write resume prompt mirroring v1.6.1 structure**

Include : what v1.6.2 shipped, Phase D confirmation checklist, current state, next session candidates (v1.6.3 retirement semantics / v1.6.2 Skill-tool runtime / v1.7.0 new skill), reco + auto-critique, exact phrase for next session, PowerShell launcher one-liner.

### Task E6: Chore commit

- [ ] **Step 1: Stage + commit**

```bash
cd C:/Dev/Claude_cowork/project-genesis/.claude/worktrees/chore_2026-04-19_v1_6_2_session
git add CHANGELOG.md memory/project/session_v1_6_2_runtime_dogfood.md memory/MEMORY.md .claude/docs/superpowers/resume/2026-04-19_v1_6_2_to_next.md
git commit -m "$(cat <<'EOF'
chore(memory): v1.6.2 — CHANGELOG honest + session trace + MEMORY + resume

Post-ship memory chore for v1.6.2 runtime dogfood.

- CHANGELOG v1.6.2 honest 5-axis rating
- Session trace with hypothesis outcomes + friction triage
- MEMORY.md pointer
- Resume prompt for next session (v1.6.3 / v1.6.2 / v1.7.0 candidates)

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

### Task E7: PR + merge chore

- [ ] **Step 1: Push + open + squash merge + verify**

Same GH_TOKEN prefix pattern as Phase C.

---

## Ship-gate checklist (before claiming v1.6.2 done)

- [ ] All Phase A edit tasks complete (A1-A5)
- [ ] AC10 grep = 0 pre-feat-core commit (A6)
- [ ] feat-core commit landed (A7)
- [ ] User spawned 5 fresh sessions + pasted evidence back
- [ ] Phase B evidence log integrity gate passed (§ 4.5.1)
- [ ] Class-A findings (if any) fixed in separate commits before feat-runtime
- [ ] feat-runtime commit landed (B5)
- [ ] PR opened, squash-merged, tagged v1.6.2
- [ ] Phase D conditional executed iff triggered
- [ ] Chore phase E complete
- [ ] Self-rating honest computed + CHANGELOG entry reflects honest delta

## Running-average post-ship calculation

Pre-v1.6.2 running avg : 8.90 (18 ratings).
Post-v1.6.2 running avg = (8.90 × 18 + <honest_v1.6.2>) / 19.

If honest = 9.14 → (160.20 + 9.14) / 19 = 169.34 / 19 ≈ **8.91 (+0.01)**.
If honest drops to 8.5 → (160.20 + 8.50) / 19 = 168.70 / 19 ≈ **8.88 (-0.02)**.

Streak ≥ 9.0 : advances to 4 iff honest ≥ 9.0 ; breaks otherwise.
