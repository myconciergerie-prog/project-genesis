<!-- SPDX-License-Identifier: MIT -->
---
name: Bootstrap intent — project-genesis (v1.2.0 self-dogfood)
description: Structured project intent parsed from config.txt at Genesis Phase 0 during the 2026-04-17 v1.2.0 conscious strange-loop self-dogfood. Consumed by all downstream phases — with explicit acknowledgement that Phase 3 and 5.5 will fail structurally per F23 / F27.
type: project
phase: 0
---

# Bootstrap intent — project-genesis (self-dogfood v1.2.0)

## Parsed at

2026-04-17T00:55 local (Windows, Claude Code session UUID this session)

## Fields

| Field | Value | Source |
|---|---|---|
| Project name | project-genesis | config.txt |
| Slug | project-genesis | config.txt (**COLLIDES WITH ORCHESTRATOR — F27**) |
| Vision | Claude Code plugin transforming config.txt + mixed media into a fully bootstrapped project via a 7-phase protocol. v1 shipped; v1.2 hardens through self-dogfood; v2 targets Promptor fusion with drag-drop box + one-click auth, boomer-friendly. | config.txt |
| License | MIT | config.txt |
| Is-a-plugin | yes | config.txt |
| Plan tier | Max | config.txt |
| Stack hints | distribution=Claude Code plugin; language=Python/Bash/Markdown; version_mgmt=semver + CHANGELOG; memory=7 types; research_cache=R8 TTL; worktree=R2.1; ssh_identity=per-project; multidevice=Remote Control / Codespaces; ide=VS Code + Claude Code extension | config.txt |
| Scope locks | aurum-ai (frozen at 0b1de3d until Genesis v1 ships) | config.txt known_rough_edges |
| Mixed media | none | folder scan |

## Non-canonical fields passed through (F26)

- `audience`: Engineers who want a reproducible project bootstrap with discipline. v2 audience expands to anyone who can describe an idea.
- `constraints`: must_not_break_aurum_frozen_scope_lock / additive_auth_only / no_new_windows / r9_language_policy / anti_frankenstein_target sub-10 / target_self_rating_v1_2_0 8.6
- `known_rough_edges`: F1..F19 already logged; plugin_install_does_not_exist; config_txt_undocumented_to_users; auth_wall_absorbed_in_v1_1; strange_loop_paradox
- `expected_frictions_to_validate`: Phase -1 skip-check alignment; Phase 0 YAML-ish parsing; Phase 3 auth without paste-back; orchestrator target-is-itself paradox detection; mode=auto propagation; skills invocable from worktree
- `next_target_after_v1_2`: v2 Promptor fusion with drop zone (see specs + R8 cache entry)

## Raw config.txt

(4.2 KB — see `selfdogfood-target/config.txt` at HEAD of this worktree)

## Gaps noted at Phase 0

- **None functional** — all mandatory fields (name, slug, vision) populated.
- **F23 blocker** — target path is inside the Genesis repo's worktree tree. Phase 3 `git init` will conflict with worktree `.git` ; Phase 5.5 repo creation will collide with the existing `myconciergerie-prog/project-genesis`. **Orchestrator will hit a structural wall at Phase 3 or 5.5.** User intent: capture this friction; do not bypass.
- **F27 blocker** — self-collision on slug. Phase 5.5 would attempt to create `myconciergerie-prog/project-genesis` which already exists with v1.1.0 shipped.

## Proceed decision

User said `mode=auto` + "capture chaque friction". Proceeding to Phase 1 with explicit acknowledgement that downstream phases will fail. The failures ARE the deliverable.
