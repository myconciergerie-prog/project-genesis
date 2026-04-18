<!-- SPDX-License-Identifier: MIT -->
---
name: Anthropic Python SDK — version pin for v1.4.0 Citations extractor
description: R8 stack entry documenting the minimum-supported `anthropic` Python SDK version for `genesis-drop-zone` v1.4.0 extractor. TTL 1 day per stack convention — refresh at every session open.
type: research-stack
scope: project-specific
created_at: 2026-04-18
expires_at: 2026-04-19
confidence: medium
---

# Anthropic Python SDK — stack pin

## Purpose

The v1.4.0 `genesis-drop-zone` ship introduces the first external runtime dependency in Genesis — the Python `anthropic` SDK — invoked by `skills/genesis-drop-zone/scripts/extract_with_citations.py`. This stack entry pins the supported version range at ship time and records known-breaking-change dates so a future session can spot stale behaviour quickly.

Per R8 convention for `stack/` entries: TTL 1 day. Refresh at every session open that touches the extractor.

## Minimum supported version

**`anthropic >= 0.40.0`**.

Required surface:

- `anthropic.Anthropic()` client constructor reading `ANTHROPIC_API_KEY` from env.
- `client.messages.create(...)` Messages API.
- `messages` parameter accepts `content` blocks of type `document` with nested `citations: {enabled: True}` and `cache_control: {type: "ephemeral", ttl: "1h"}`.
- `response.content[*].citations[*]` exposes `cited_text`, `document_index`, `start_page_number` / `end_page_number` (for PDF sources), `start_char_index` / `end_char_index` (for text sources).
- Exception classes `anthropic.RateLimitError`, `anthropic.APIStatusError`, `anthropic.APIError`.
- `response.usage` exposes `input_tokens`, `cache_read_input_tokens`, `cache_creation_input_tokens`, `output_tokens`.

## Known breaking-change dates

- **March 2026** — Anthropic silently tightened prompt-cache default TTL from 1h to 5m. The v1.4.0 extractor hardcodes `ttl: "1h"` on every document block's `cache_control` and never relies on the default. Env override `GENESIS_DROP_ZONE_CACHE_TTL` accepts `5m` or `1h`. Ref: R8 entry `sota/v2_promptor_fusion_landscape_2026-04-17.md § Stage 2` citing Anthropic GitHub issue #46829.
- **SDK API evolution** — verify at each refresh that `content` block types (`document`, `image`, `text`) and citation fields (`cited_text`, `document_index`, page/char indices) are still the accepted surface. The SDK moved from major.minor versioning to semver around v0.35 in late 2025 — non-breaking additions are frequent; breaking removals are rare but do happen on major bumps.

## Installation reminder (user-side)

```bash
pip install 'anthropic>=0.40.0'
```

The extractor fails with exit code 3 (`EXIT_SDK_MISSING`) and a diagnostic message if `anthropic` is not importable. The SKILL.md dispatch routes to the v1.3.3 in-context fallback path in that case — no user-visible failure.

## Changelog reference

- PyPI: `https://pypi.org/project/anthropic/`
- GitHub: `https://github.com/anthropics/anthropic-sdk-python`

Refresh this entry by running `pip index versions anthropic` or checking the PyPI page for the latest stable + any breaking-change notes in the SDK changelog since 2026-04-18.

## TTL discipline

**Expires 2026-04-19.** When this entry's `expires_at` date passes, a refreshing session should:

1. Check `pip index versions anthropic` (or the PyPI page) for the current stable.
2. Verify the required SDK surface (enumerated above) is still stable — scan the CHANGELOG since the last refresh for `BREAKING` markers or deprecations on Messages API / Citations / cache_control / response.usage.
3. Update `created_at` / `expires_at` + bump the minimum-supported-version if the SDK has moved breaking-change-wise.
4. Update `INDEX.md` row with the new date.
5. If the refresh finds no drift, a simple re-date + `confidence: high` is sufficient.

If the refresh finds drift that would break the v1.4.0 extractor, file a `v1.4.x` or `v1.5.0` plan entry to adapt.
