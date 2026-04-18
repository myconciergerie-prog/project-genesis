<!-- SPDX-License-Identifier: MIT -->
---
topic: spdx-headers
type: sota
created_at: 2026-04-19
expires_at: 2026-04-26
status: active
template_of: genesis-protocol v1.4.2
original_created_at: 2026-04-14
sources:
  - https://spdx.dev/learn/handling-license-info/
  - https://spdx.github.io/spdx-spec/v2.3/using-SPDX-short-identifiers-in-source-files/
  - https://www.linuxfoundation.org/licensebestpractices
  - https://reuse.software/faq/
confidence: high
supersedes: null
---

# SPDX License Identifier Headers — Best Practice 2026

## TL;DR

- Every source file gets a case-sensitive **`SPDX-License-Identifier: MIT`** line in a comment near the top
- Use the short-form identifier (single license ID), not a full expression, when the project uses a single license
- Strongly recommended by the Linux Foundation — enables software composition analysis tools to attribute licenses accurately at scale

## Canonical formats per file type

| File type | Header line |
|---|---|
| Python (`.py`) | `# SPDX-License-Identifier: MIT` |
| Shell (`.sh`, `.bash`) | `# SPDX-License-Identifier: MIT` |
| PowerShell (`.ps1`) | `# SPDX-License-Identifier: MIT` |
| Markdown (`.md`) | `<!-- SPDX-License-Identifier: MIT -->` |
| YAML (`.yaml`, `.yml`) | `# SPDX-License-Identifier: MIT` |
| JavaScript / TypeScript | `// SPDX-License-Identifier: MIT` |
| JSON | N/A — JSON has no comments; coverage via `license` field in the relevant manifest (`plugin.json`, `package.json`) |

## Placement rules

- At or near the top of the file, on its own line in a comment appropriate for the language
- Can appear directly under a copyright notice, or replace it entirely — SPDX short-form is sufficient by itself per Linux Foundation guidance
- Case-sensitive: must be exactly `SPDX-License-Identifier: <id>`
- The identifier must come from the SPDX License List (`https://spdx.org/licenses/`)

## Single license vs expressions

For Genesis the single short-form `MIT` is sufficient. Expressions (with parentheses, `AND` / `OR`, `WITH`) are only needed when a file is covered by multiple licenses simultaneously — not our case.

## Application for Genesis

- Every `.py`, `.md`, `.sh`, `.ps1`, `.yaml`, `.yml`, `.js`, `.ts` file in the repo carries the SPDX header on line 1 (or line 2 if there's a shebang)
- `LICENSE` file at repo root holds the full MIT text
- `plugin.json` has `"license": "MIT"` field (JSON can't host the SPDX comment, so manifest-level license field covers it)
- No SPDX header needed on non-source assets (images, binaries)
- CI lint (deferred): a simple script that fails on any source file missing its SPDX header — add later if the pain is felt, not pre-emptively (anti-Frankenstein)
