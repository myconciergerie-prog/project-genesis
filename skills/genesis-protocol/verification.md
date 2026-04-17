<!-- SPDX-License-Identifier: MIT -->
---
name: genesis-protocol verification
description: Two-mode health card for the genesis-protocol orchestrator. Post-install mode confirms the five sibling skills and the seven orchestrator files are present. Post-action mode confirms the target downstream project was bootstrapped successfully — memory subtree, research cache, git repo, SSH identity, GitHub repo, three-probe gate, first commit, v0.1.0 tag, resume prompt, session archive, and halt-on-leak GREEN.
---

# genesis-protocol — verification

The verification card exists in two modes. **Post-install** runs at plugin install time (via `install-manifest.yaml`'s verification block) and confirms the skill is correctly wired into the Genesis plugin. **Post-action** runs at the end of an orchestrator invocation and confirms the target downstream project was bootstrapped successfully.

Both modes render a GREEN / YELLOW / RED card. A YELLOW on any field is a warning the user should read; a RED halts downstream work (post-install) or invalidates the bootstrap (post-action).

## Post-install mode

Runs automatically after `install-manifest.yaml`'s verification checks have passed. The card confirms that every prerequisite the orchestrator needs at runtime is in place.

### Checks

| # | Check | Pass condition | On fail |
|---|---|---|---|
| 1 | Sibling: phase-minus-one present | `skills/phase-minus-one/SKILL.md` exists | RED — orchestrator cannot invoke Phase -1 |
| 2 | Sibling: phase-5-5-auth-preflight present | `skills/phase-5-5-auth-preflight/SKILL.md` exists | RED — orchestrator cannot invoke Phase 5.5 |
| 3 | Sibling: journal-system present | `skills/journal-system/install-manifest.yaml` exists | RED — Phase 1 cannot install journal scaffold |
| 4 | Sibling: session-post-processor present | `skills/session-post-processor/SKILL.md` + `run.py` exist | RED — Phase 7 cannot archive the bootstrap session |
| 5 | Sibling: pepite-flagging present | `skills/pepite-flagging/install-manifest.yaml` exists | RED — Phase 1 cannot install pépite scaffold |
| 6 | Orchestrator entry point | `skills/genesis-protocol/SKILL.md` exists | RED — orchestrator is corrupted |
| 7 | All seven phase runbooks present | `phase-0-seed-loading.md`, `phase-1-rules-memory.md`, `phase-3-git-init.md`, `phase-5-5-auth.md`, `phase-6-commit-push.md` all exist | RED — the 1:1 mirror of master.md's 7-phase table is broken |
| 8 | Install manifest present | `install-manifest.yaml` exists and is readable | RED — cannot invoke install flow |
| 9 | Layer 0 universal files accessible | `~/.claude/CLAUDE.md` exists and mentions "per-project SSH identity" | YELLOW — orchestrator can run but Phase 5.5's sibling will have degraded Layer 0 references |
| 10 | Plugin manifest version consistent | `.claude-plugin/plugin.json` version matches `install-manifest.yaml` version field | YELLOW — manual sync gap; ship-blocking if the plugin is about to publish |

### Card template

```
🟢/🟡/🔴 genesis-protocol — post-install verification

  1. Sibling: phase-minus-one ................. [GREEN|RED]
  2. Sibling: phase-5-5-auth-preflight ......... [GREEN|RED]
  3. Sibling: journal-system ................... [GREEN|RED]
  4. Sibling: session-post-processor ........... [GREEN|RED]
  5. Sibling: pepite-flagging .................. [GREEN|RED]
  6. Orchestrator entry point .................. [GREEN|RED]
  7. Seven phase runbooks present .............. [GREEN|RED]
  8. Install manifest present .................. [GREEN|RED]
  9. Layer 0 accessible ........................ [GREEN|YELLOW]
 10. Plugin version consistent ................. [GREEN|YELLOW]

Overall: [GREEN|YELLOW|RED]
```

Any RED halts the install. YELLOWs are surfaced as warnings but do not halt.

## Post-action mode

Runs after the orchestrator's Phase 7 completes. The card confirms the target downstream project has every artefact the 7-phase protocol promises. This mode is the "did the bootstrap actually work" gate.

### Checks (grouped by phase)

**Phase -1 — Dependencies pre-flight**

| # | Check | Pass condition |
|---|---|---|
| -1.a | Stack manifest exists OR was skipped | `<target>/memory/reference/automation-stack.md` exists OR user explicitly skipped Phase -1 at consent card |
| -1.b | Healthy stack items | Stack manifest lists `git`, `gh`, a browser, and a Claude Code CLI version as healthy |

**Phase 0 — Seed loading**

| # | Check | Pass condition |
|---|---|---|
| 0.a | Bootstrap intent persisted | `<target>/memory/project/bootstrap_intent.md` exists |
| 0.b | Mandatory fields populated | Intent frontmatter / body has name, slug, vision |

**Phase 1 + Phase 2 — Rules, memory, research cache**

| # | Check | Pass condition |
|---|---|---|
| 1.a | MEMORY.md index | `<target>/memory/MEMORY.md` exists and lists all 8 memory subtrees |
| 1.b | Rules file | `<target>/.claude/docs/superpowers/rules/v1_rules.md` exists |
| 1.c | Project CLAUDE.md | `<target>/CLAUDE.md` exists with Layer 0 inheritance |
| 1.d | journal-system installed | `<target>/memory/journal/INDEX.md` exists |
| 1.e | pepite-flagging installed | `<target>/memory/pepites/INDEX.md` exists |
| 1.f | session-post-processor installed | `<target>/memory/project/sessions/INDEX.md` exists |
| 2.a | Research cache INDEX | `<target>/.claude/docs/superpowers/research/INDEX.md` exists |
| 2.b | Research cache subdirs | `sota/`, `stack/`, `archive/` subdirs exist under `research/` |

**Phase 3 + Phase 4 — Git, SSH, project seeds**

| # | Check | Pass condition |
|---|---|---|
| 3.a | Git repo initialized | `<target>/.git/` exists, default branch is `main` |
| 3.b | Per-project SSH key | `~/.ssh/id_ed25519_<slug>` exists, mode 0600 |
| 3.c | SSH config alias | `~/.ssh/config` contains `Host github.com-<slug>` with `IdentitiesOnly yes` |
| 3.d | Git remote configured | `git remote -v` in target shows SSH alias URL |
| 3.e | `.gitignore` present | `<target>/.gitignore` contains `.env.local` and `id_ed25519_*` entries |
| 4.a | Master vision | `<target>/memory/master.md` has real content (not the Phase 1 placeholder) |
| 4.b | README present | `<target>/README.md` exists with project title and license |
| 4.c | CHANGELOG present | `<target>/CHANGELOG.md` has v0.1.0 entry |
| 4.d | Plugin manifest (if applicable) | If `is-a-plugin: yes`, `<target>/.claude-plugin/plugin.json` exists |

**Phase 5.5 — Auth pre-flight**

| # | Check | Pass condition |
|---|---|---|
| 5.5.a | SSH identity reference | `<target>/memory/reference/ssh_<slug>_identity.md` exists |
| 5.5.b | GitHub account reference | `<target>/memory/reference/github_<slug>_account.md` exists |
| 5.5.c | PAT in .env.local | `<target>/.env.local` contains `GH_TOKEN=` line |
| 5.5.d | Three-probe gate | `github_<slug>_account.md` records all three probes as GREEN |

**Phase 6 — First commit + tag**

| # | Check | Pass condition |
|---|---|---|
| 6.a | First commit exists | `git log --oneline` in target shows at least one commit |
| 6.b | Commit on main | `git branch --show-current` is `main` |
| 6.c | Pushed to origin | `git ls-remote origin main` returns non-empty |
| 6.d | Tag v0.1.0 | `git tag -l v0.1.0` returns `v0.1.0` |
| 6.e | Tag pushed | `git ls-remote origin v0.1.0` returns non-empty |

**Phase 7 — Resume prompt + session archive**

| # | Check | Pass condition |
|---|---|---|
| 7.a | Resume prompt | `<target>/.claude/docs/superpowers/resume/<date>_bootstrap_to_v0_2.md` exists |
| 7.b | Session memory entry | `<target>/memory/project/session_bootstrap_<date>.md` exists |
| 7.c | Session archive | `<target>/memory/project/sessions/<date>_bootstrap.md` exists |
| 7.d | Halt-on-leak GREEN | `session-post-processor` health card at the end of Phase 7 was GREEN |
| 7.e | Second commit present | `git log --oneline` shows at least two commits (bootstrap + chore) |
| 7.f | MEMORY.md updated | MEMORY.md references the new session memory and resume prompt |

### Card template

```
🟢/🟡/🔴 genesis-protocol — post-action verification

Target: <absolute path>
Repo  : <owner>/<repo>
Tag   : v0.1.0

Phase -1 — Dependencies pre-flight
  -1.a Stack manifest exists or skipped ..... [GREEN|RED|SKIPPED]
  -1.b Healthy stack items .................. [GREEN|YELLOW|SKIPPED]

Phase 0 — Seed loading
   0.a Bootstrap intent persisted ........... [GREEN|RED]
   0.b Mandatory fields populated ........... [GREEN|RED]

Phase 1 — Rules + memory
   1.a MEMORY.md index ...................... [GREEN|RED]
   1.b Rules file ........................... [GREEN|RED]
   1.c Project CLAUDE.md .................... [GREEN|RED]
   1.d journal-system installed ............. [GREEN|RED]
   1.e pepite-flagging installed ............ [GREEN|RED]
   1.f session-post-processor installed ..... [GREEN|RED]

Phase 2 — Research cache
   2.a Research cache INDEX ................. [GREEN|RED]
   2.b Research cache subdirs ............... [GREEN|RED]

Phase 3 — Git + SSH
   3.a Git repo initialized ................. [GREEN|RED]
   3.b Per-project SSH key .................. [GREEN|RED]
   3.c SSH config alias ..................... [GREEN|RED]
   3.d Git remote configured ................ [GREEN|RED]
   3.e .gitignore present ................... [GREEN|RED]

Phase 4 — Project seeds
   4.a Master vision ........................ [GREEN|RED]
   4.b README present ....................... [GREEN|RED]
   4.c CHANGELOG present .................... [GREEN|RED]
   4.d Plugin manifest ...................... [GREEN|RED|N/A]

Phase 5.5 — Auth pre-flight
   5.5.a SSH identity reference ............. [GREEN|RED]
   5.5.b GitHub account reference ........... [GREEN|RED]
   5.5.c PAT in .env.local .................. [GREEN|RED]
   5.5.d Three-probe gate ................... [GREEN|RED]

Phase 6 — First commit + tag
   6.a First commit exists .................. [GREEN|RED]
   6.b Commit on main ....................... [GREEN|RED]
   6.c Pushed to origin ..................... [GREEN|RED]
   6.d Tag v0.1.0 ........................... [GREEN|RED]
   6.e Tag pushed ........................... [GREEN|RED]

Phase 7 — Resume + archive
   7.a Resume prompt ........................ [GREEN|RED]
   7.b Session memory entry ................. [GREEN|RED]
   7.c Session archive ...................... [GREEN|RED]
   7.d Halt-on-leak GREEN ................... [GREEN|RED]
   7.e Second commit present ................ [GREEN|RED]
   7.f MEMORY.md updated .................... [GREEN|RED]

Overall: [GREEN|YELLOW|RED]
```

### Overall rating rules

- **GREEN** — every check is GREEN or SKIPPED (for Phase -1 if explicitly skipped at consent card). The bootstrap is complete and the user can proceed to the first real session.
- **YELLOW** — one or more YELLOW checks (Layer 0 gaps, plan tier warnings, non-blocking verification misses). The bootstrap is functionally complete but has a documented gap. The user should read the YELLOW items before the first real session.
- **RED** — any RED check. The bootstrap is invalid. The orchestrator halts, the genesis report is still emitted but flagged as incomplete, and the user must fix the failing check before any downstream work.

Halt-on-leak RED at Phase 7.d is a special case: the downstream project exists and is functional (Phase 6 completed), but the session archive was deleted by `session-post-processor`. The user can choose to proceed without a bootstrap archive or to audit + strengthen redaction patterns and re-run Phase 7 only.

## Idempotency

The verification runner is read-only. Running it multiple times has zero side effects. Both modes can be invoked manually at any time — post-install by re-running `install-manifest.yaml`'s verification block, post-action by re-running the orchestrator's verification step even days after the bootstrap to re-check that the files still exist.

## Anti-Frankenstein reminders

- **Do not turn this into a repair tool.** The verification card reports status; it does not fix gaps. Fixing a gap means re-invoking the appropriate phase, not patching files from inside the verification runner
- **Do not add checks beyond those listed here.** Each check is a specific file or git state that one of the seven phases promises to create. Adding a check without a corresponding phase commitment is Frankenstein creep
- **Do not skip RED checks for speed** — the RED is the gate
- **Do not emit per-file diffs in the card.** The card is a health summary; diffs belong to `git diff` or manual inspection. Keeping the card small keeps it readable

---

### Scenario — `drop_zone_intent.md` as Phase 0 seed (v1.3.2+)

**Setup**: fresh empty folder containing a `drop_zone_intent.md` written by a prior `genesis-drop-zone` v1.3.2+ session with the standard 9-field frontmatter + body echo.

**Invoke**: `/genesis-protocol` (or natural-language intent-match trigger) in the folder.

**Expected**:

- Step 0.1 detects `drop_zone_intent.md` and logs `Primary seed: drop_zone_intent.md`.
- Step 0.2a parses the YAML frontmatter (validates `schema_version: 1`, reads the 9 semantic + 4 metadata keys).
- Step 0.2a maps the 6 primary Layer A fields per the § "Field mapping (Layer A → Layer B)" table: `idea_summary` → Vision (verbatim), `nom` → Project name + derived Project slug, `type` → inferred Is-a-plugin, `hints_techniques` → Stack hints, `attaches` → Mixed media descriptor.
- Step 0.2a preserves `pour_qui`, `langue_detectee`, `budget_ou_contrainte`, `prive_ou_public` for Step 0.4 + Step 0.5.
- Step 0.4 card renders with origin tags `(from drop zone)` on Vision / Project name / Stack hints, `(inferred)` on Is-a-plugin, `(derived)` on Slug, `(default)` on License. `Additional context from drop zone` block renders with the 4 Layer-A-specific extras.
- User confirms `yes` → Step 0.5 writes `memory/project/bootstrap_intent.md` containing populated fields + new `## Conversational context from drop zone` section + `## Raw config.txt` rendered as `n/a — seeded from drop_zone_intent.md`.
- Phase 1 proceeds normally, reading the populated `bootstrap_intent.md` as its input.

**Regression scenario — both-files-present precedence**: same setup but with `config.txt` also present in cwd alongside `drop_zone_intent.md`. Expected:

- Step 0.1 logs the precedence note: `config.txt found but drop_zone_intent.md takes precedence — ignoring config.txt`.
- Step 0.2a proceeds (Step 0.2 skipped entirely).
- Step 0.4 / Step 0.5 output identical to the happy-path scenario.
- `## Raw config.txt` section in Step 0.5 output renders as `n/a — seeded from drop_zone_intent.md` (config.txt content never parsed, never archived in Phase 0 output).

**Ship gate**: artefact-level verification (synthetic fixture + Step 0.2a parsing logic traced against the fixture, Step 0.4 / 0.5 template rendering against the fixture's fields). Runtime replay of the full Phase 0 flow deferred to an externally-launched fresh Claude Code session per the same harness constraint that applies to `genesis-drop-zone` scenarios #1 / #13.
