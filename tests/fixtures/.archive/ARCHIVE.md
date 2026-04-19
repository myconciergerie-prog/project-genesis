<!-- SPDX-License-Identifier: MIT -->

# Archived fixtures

Fixtures retired by v2.0.0 architectural shift (drop subprocess Citations path).

| File | Reason |
|---|---|
| drop_zone_intent_fixture_v1_4_0_fr_with_citations.md | Citation keys (`*_source_citation`) present, unrepresentative of v2 schema. |
| drop_zone_intent_fixture_v1_4_0_en_with_citations.md | Same reason. |
| drop_zone_intent_fixture_v1_5_0_arbitrated.md | DUAL semantics (carries both v1.5.0 `snapshot_version` + `arbitrated_fields` AND v1.4.0 `_source_citation` keys). Replaced by `tests/fixtures/drop_zone_intent_fixture_v2_arbitrated.md` (same revision-state semantics, no citation keys). |

Fixtures retained in active set (citation-free) :
- `drop_zone_intent_fixture_v1_3_2.md`
- `drop_zone_intent_fixture_v1_3_3_en.md`
- `drop_zone_intent_fixture_v1_4_0_fallback.md` (byte-identical to v1.3.3 modulo `skill_version`)
