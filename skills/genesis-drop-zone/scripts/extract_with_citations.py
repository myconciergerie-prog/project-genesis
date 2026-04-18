# SPDX-License-Identifier: MIT
"""genesis-drop-zone / scripts / extract_with_citations.py

Second-privilege-class (network) extractor for `genesis-drop-zone` v1.4.0.
Calls the Anthropic Messages API with `citations: {enabled: true}` per
document block to extract the 9-field drop-zone intent schema with
per-field source attribution.

The SKILL.md dispatch layer launches this as a Python subprocess after
the drop-zone welcome + content turn, reads the JSON on stdout, and
either annotates the mirror with citations or routes to v1.3.3
in-context fallback on any non-zero exit code.

Input (stdin, JSON): cwd, attachments[], typed_text, content_locale_hint, model.
Output (stdout on exit 0): JSON with schema_version=1, 9 semantic fields,
optional <field>_source_citation entries (key omitted when no citation),
and usage.

Exit codes:
  0 OK / 2 no key / 3 SDK missing / 4 API error / 5 rate limit /
  6 bad input / 7 output invalid.

Env vars: ANTHROPIC_API_KEY, GENESIS_DROP_ZONE_MODEL,
GENESIS_DROP_ZONE_CACHE_TTL, GENESIS_DROP_ZONE_VERBOSE.

Canonical spec: `.claude/docs/superpowers/specs/v2_etape_0_drop_zone.md`
sections "Scope - v1.4.0 Citations API extraction" and "Citations API
- signal + dispatch (v1.4.0)".
"""

from __future__ import annotations

import base64
import json
import mimetypes
import os
import sys
from pathlib import Path


# Constants

DEFAULT_MODEL = "claude-opus-4-7"
DEFAULT_CACHE_TTL = "1h"
SCHEMA_VERSION = 1
MAX_TOKENS = 2048

FR_CANONICAL_NULL_CORE = "a trouver ensemble"
FR_CANONICAL_NULL_BONUS_MASC = "non mentionne"
FR_CANONICAL_NULL_BONUS_FEM = "non mentionnee"
# Ambiguity literal contains U+2014 em-dash per spec canonical contract.
FR_CANONICAL_AMBIGUITY_TEMPLATE = "a affiner — X ou Y"

SEMANTIC_FIELDS = (
    "idea_summary",
    "pour_qui",
    "type",
    "nom",
    "attaches",
    "langue_detectee",
    "budget_ou_contrainte",
    "prive_ou_public",
    "hints_techniques",
)

EXIT_OK = 0
EXIT_NO_KEY = 2
EXIT_SDK_MISSING = 3
EXIT_API_ERROR = 4
EXIT_RATE_LIMIT = 5
EXIT_BAD_INPUT = 6
EXIT_OUTPUT_INVALID = 7


# Input validation


def read_stdin_payload() -> dict:
    """Parse and validate the JSON payload on stdin."""
    try:
        payload = json.loads(sys.stdin.read())
    except json.JSONDecodeError as exc:
        print(f"[extractor] stdin JSON parse failed: {exc}", file=sys.stderr)
        sys.exit(EXIT_BAD_INPUT)

    required = ("cwd", "attachments", "typed_text", "content_locale_hint", "model")
    missing = [k for k in required if k not in payload]
    if missing:
        print(f"[extractor] stdin payload missing keys: {missing}", file=sys.stderr)
        sys.exit(EXIT_BAD_INPUT)
    if not isinstance(payload["attachments"], list):
        print("[extractor] attachments must be a list", file=sys.stderr)
        sys.exit(EXIT_BAD_INPUT)
    return payload


# Document block assembly


def build_documents(attachments: list, typed_text: str, cache_ttl: str) -> tuple[list, list]:
    """Assemble document blocks (citations on) and image blocks (no citations)."""
    documents: list = []
    images: list = []

    if typed_text:
        documents.append(
            {
                "type": "document",
                "source": {"type": "text", "media_type": "text/plain", "data": typed_text},
                "title": "User typed text",
                "context": "Inline conversational input from the drop-zone turn.",
                "citations": {"enabled": True},
                "cache_control": {"type": "ephemeral", "ttl": cache_ttl},
            }
        )

    for path_str in attachments:
        path = Path(path_str)
        if not path.is_absolute():
            path = Path.cwd() / path
        if not path.exists():
            print(f"[extractor] attachment not found, skipping: {path}", file=sys.stderr)
            continue

        mime, _ = mimetypes.guess_type(str(path))
        suffix = path.suffix.lower()

        if mime == "application/pdf" or suffix == ".pdf":
            encoded = base64.standard_b64encode(path.read_bytes()).decode("ascii")
            documents.append(
                {
                    "type": "document",
                    "source": {"type": "base64", "media_type": "application/pdf", "data": encoded},
                    "title": path.name,
                    "context": "Attached file from drop zone.",
                    "citations": {"enabled": True},
                    "cache_control": {"type": "ephemeral", "ttl": cache_ttl},
                }
            )
        elif (mime and mime.startswith("text/")) or suffix in {".md", ".txt", ".rst"}:
            text_content = path.read_text(encoding="utf-8", errors="replace")
            documents.append(
                {
                    "type": "document",
                    "source": {"type": "text", "media_type": "text/plain", "data": text_content},
                    "title": path.name,
                    "context": "Attached text from drop zone.",
                    "citations": {"enabled": True},
                    "cache_control": {"type": "ephemeral", "ttl": cache_ttl},
                }
            )
        elif mime and mime.startswith("image/"):
            encoded = base64.standard_b64encode(path.read_bytes()).decode("ascii")
            images.append(
                {
                    "type": "image",
                    "source": {"type": "base64", "media_type": mime, "data": encoded},
                }
            )
        else:
            print(
                f"[extractor] unsupported attachment type {mime!r} for {path.name}, skipping",
                file=sys.stderr,
            )

    return documents, images


# System prompt


def build_system_prompt() -> str:
    """English R9 tier-1 prompt quoting FR canonical null-class tokens as data."""
    return (
        "You are the v1.4.0 extractor for the Genesis drop-zone skill. "
        "Read the attached documents and images, then output a SINGLE JSON "
        "object with exactly these top-level keys: "
        f"schema_version (integer, value {SCHEMA_VERSION}), "
        f"{', '.join(SEMANTIC_FIELDS)}. "
        "All values are strings. "
        "Use these EXACT FR canonical null-class tokens when a field is missing: "
        f'"{FR_CANONICAL_NULL_CORE}" for missing core fields (pour_qui, type, nom); '
        f'"{FR_CANONICAL_NULL_BONUS_MASC}" for missing masculine bonus fields '
        "(budget_ou_contrainte, hints_techniques); "
        f'"{FR_CANONICAL_NULL_BONUS_FEM}" for the feminine bonus field (prive_ou_public); '
        f'"{FR_CANONICAL_AMBIGUITY_TEMPLATE}" pattern for ambiguous fields '
        "(substitute concrete hypotheses for X and Y). "
        "Do not translate these tokens even if the source content is in English. "
        "For langue_detectee emit exactly one of: FR, EN, mixte. "
        "For attaches emit a short human descriptor such as "
        '"1 brief \'name.pdf\' + 1 photo \'logo.png\'" or "texte seul" if nothing dropped. '
        "Output ONLY the JSON object, no prose wrapper, no code fence."
    )


# API call and response shaping


def call_api(client, model: str, documents: list, images: list) -> tuple[dict, dict, dict]:
    """Send the extraction request and return (extracted, per_field_citations, usage)."""
    content_blocks = list(documents) + list(images) + [
        {"type": "text", "text": "Extract the 9-field intent schema from the attachments. Emit JSON only."}
    ]
    response = client.messages.create(
        model=model,
        max_tokens=MAX_TOKENS,
        system=build_system_prompt(),
        messages=[{"role": "user", "content": content_blocks}],
    )

    text_parts: list[str] = []
    block_citations: list = []
    for block in response.content:
        if getattr(block, "type", None) == "text":
            text_parts.append(block.text)
            citations = getattr(block, "citations", None) or []
            block_citations.extend(citations)

    joined = "".join(text_parts).strip()
    try:
        extracted = json.loads(joined)
    except json.JSONDecodeError as exc:
        print(f"[extractor] API returned non-JSON text: {exc}; raw: {joined[:200]!r}", file=sys.stderr)
        sys.exit(EXIT_OUTPUT_INVALID)

    if not isinstance(extracted, dict):
        print("[extractor] API output is not a JSON object", file=sys.stderr)
        sys.exit(EXIT_OUTPUT_INVALID)

    missing = [k for k in SEMANTIC_FIELDS if k not in extracted]
    if missing:
        print(f"[extractor] API output missing fields: {missing}", file=sys.stderr)
        sys.exit(EXIT_OUTPUT_INVALID)

    # Heuristic citation-to-field mapping: one citation per field in
    # emission order. The SDK attaches citations at the content-block level.
    per_field_citations: dict = {}
    for idx, field in enumerate(SEMANTIC_FIELDS):
        if idx < len(block_citations):
            per_field_citations[field] = _shape_citation(block_citations[idx])

    usage = _shape_usage(getattr(response, "usage", None))
    return extracted, per_field_citations, usage


def _shape_citation(raw) -> dict:
    """Normalize an SDK citation object to the spec's citation_object shape."""
    citation_type = getattr(raw, "type", None) or "none"
    mapped_type = {
        "page_location": "pdf_page_range",
        "char_location": "text_char_range",
    }.get(citation_type, citation_type)

    document_index = getattr(raw, "document_index", 0)
    if mapped_type == "pdf_page_range":
        start = getattr(raw, "start_page_number", 1)
        end = getattr(raw, "end_page_number", start)
    else:
        start = getattr(raw, "start_char_index", 0)
        end = getattr(raw, "end_char_index", start)

    cited_text = getattr(raw, "cited_text", "") or ""
    if len(cited_text) > 80:
        cited_text = cited_text[:77] + "..."

    return {
        "type": mapped_type,
        "document_index": int(document_index),
        "start": int(start),
        "end": int(end),
        "cited_text_preview": cited_text,
    }


def _shape_usage(raw) -> dict:
    """Normalize SDK usage to a plain dict."""
    if raw is None:
        return {}
    return {
        "input_tokens": getattr(raw, "input_tokens", 0),
        "cache_read_input_tokens": getattr(raw, "cache_read_input_tokens", 0),
        "cache_creation_input_tokens": getattr(raw, "cache_creation_input_tokens", 0),
        "output_tokens": getattr(raw, "output_tokens", 0),
    }


# Output assembly


def build_output(extracted: dict, per_field_citations: dict, usage: dict) -> dict:
    """Merge extraction + citations + usage into the final stdout dict."""
    output: dict = {"schema_version": SCHEMA_VERSION}
    for field in SEMANTIC_FIELDS:
        output[field] = extracted[field]
    for field, citation in per_field_citations.items():
        output[f"{field}_source_citation"] = citation
    output["usage"] = usage
    return output


# Main entry


def main() -> None:
    payload = read_stdin_payload()

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("[extractor] ANTHROPIC_API_KEY unset", file=sys.stderr)
        sys.exit(EXIT_NO_KEY)

    try:
        import anthropic  # type: ignore
    except ImportError as exc:
        print(f"[extractor] anthropic SDK not installed ({exc}); run: pip install anthropic", file=sys.stderr)
        sys.exit(EXIT_SDK_MISSING)

    model = os.environ.get("GENESIS_DROP_ZONE_MODEL") or payload.get("model") or DEFAULT_MODEL
    cache_ttl = os.environ.get("GENESIS_DROP_ZONE_CACHE_TTL") or DEFAULT_CACHE_TTL
    verbose = os.environ.get("GENESIS_DROP_ZONE_VERBOSE") == "1"

    try:
        documents, images = build_documents(payload["attachments"], payload["typed_text"], cache_ttl)
    except OSError as exc:
        print(f"[extractor] attachment read failed: {exc}", file=sys.stderr)
        sys.exit(EXIT_BAD_INPUT)

    if verbose:
        print(
            f"[extractor] model={model} cache_ttl={cache_ttl} documents={len(documents)} images={len(images)}",
            file=sys.stderr,
        )

    client = anthropic.Anthropic()

    try:
        extracted, per_field_citations, usage = call_api(client, model, documents, images)
    except anthropic.RateLimitError as exc:
        print(f"[extractor] rate limit after SDK retries: {exc}", file=sys.stderr)
        sys.exit(EXIT_RATE_LIMIT)
    except anthropic.APIStatusError as exc:
        print(f"[extractor] API status error: {exc}", file=sys.stderr)
        sys.exit(EXIT_API_ERROR)
    except anthropic.APIError as exc:
        print(f"[extractor] API error: {exc}", file=sys.stderr)
        sys.exit(EXIT_API_ERROR)

    print(f"[extractor] usage={json.dumps(usage)}", file=sys.stderr)

    output = build_output(extracted, per_field_citations, usage)
    json.dump(output, sys.stdout, ensure_ascii=False)
    sys.stdout.write("\n")
    sys.exit(EXIT_OK)


if __name__ == "__main__":
    main()
