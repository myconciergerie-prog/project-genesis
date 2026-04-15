<!-- SPDX-License-Identifier: MIT -->
---
name: session-post-processor / redaction-patterns
description: The full regex pattern set the skill applies to every string field before writing the Markdown archive. Each pattern has a name, regex, rationale, and test vectors. Halt-on-leak verification re-checks the written output against the same set — any post-write match deletes the file.
---

# Redaction patterns

This file defines every secret pattern the `session-post-processor` skill redacts before writing a Markdown archive, and the same set is re-applied in the halt-on-leak verification gate after writing. Adding a new pattern requires adding a test vector and re-running the dogfood suite.

## Pattern format

Every pattern is a tuple of `(name, regex, rationale, test_vectors)`:

- **`name`** — short label, used in the `[REDACTED:<name>]` replacement and in hit-count logs
- **`regex`** — Python-compatible regular expression; case-sensitive by default unless rationale says otherwise
- **`rationale`** — one-sentence reason the pattern exists; points to a specific threat
- **`test_vectors`** — at least one known-good match and one known-good non-match

## Core pattern set

### GitHub PAT — fine-grained (2022+)

```
name: github_pat_finegrained
regex: \bgithub_pat_[A-Za-z0-9_]{82,}\b
rationale: Fine-grained PATs (the 2026 canonical scope — see Layer 0) carry full repo write access and must never appear in archives. Genesis uses these tokens every session via GH_TOKEN env override.
test_vectors:
  match: github_pat_11ABCDEFG0123456789ABCDEFG0123456789ABCDEFG0123456789ABCDEFG0123456789ABCDEFG0123456789_
  non-match: github_pat_short (too short)
  non-match: GITHUB_PAT_11... (uppercase prefix — not a real token format)
```

### GitHub PAT — classic tokens

```
name: github_classic_token
regex: \b(ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{36,}\b
rationale: Classic GitHub tokens (personal, OAuth, user-to-server, server-to-server, refresh). Layer 0 says never use classic tokens — but a user-machine can still have old ones lying around.
test_vectors:
  match: ghp_0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZa
  match: gho_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
  non-match: ghp_short
  non-match: githubpat_... (missing underscore)
```

### Anthropic API key

```
name: anthropic_api_key
regex: \bsk-ant-[a-zA-Z0-9\-_]{32,}\b
rationale: Anthropic API keys start with `sk-ant-`. Present in any session where the user configured the Claude API directly. Leaking one lets an attacker bill the user's account.
test_vectors:
  match: sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
  non-match: sk-ant- (empty body)
  non-match: sk-openai-... (different provider)
```

### OpenAI API key

```
name: openai_api_key
regex: \bsk-(?:proj-)?[a-zA-Z0-9\-_]{32,}\b
rationale: OpenAI keys historically start with `sk-`, newer project keys prefix with `sk-proj-`. Overlaps with Anthropic regex at the `sk-` prefix but is distinguished by the lack of `ant-` after it. Ordering matters — apply the Anthropic pattern first so `sk-ant-*` is caught as Anthropic, not OpenAI.
test_vectors:
  match: sk-proj-abcdefghijklmnopqrstuvwxyz01234567
  match: sk-0123456789abcdefghijklmnopqrstuvwxyz
  non-match: sk-ant-... (should be caught by anthropic_api_key first)
```

### Supabase PAT + secret keys

```
name: supabase_pat
regex: \bsbp_[a-f0-9]{40,}\b
rationale: Supabase PATs (`sbp_...`) grant org/project admin. Genesis uses these for Supabase MCP setups in downstream projects.
test_vectors:
  match: sbp_0123456789abcdef0123456789abcdef01234567
  non-match: sbp_short

name: supabase_secret_key
regex: \bsb_secret_[A-Za-z0-9_\-]{32,}\b
rationale: Supabase secret keys (2026 format), server-side only.
test_vectors:
  match: sb_secret_abcdefghijklmnopqrstuvwxyz01234567
  non-match: sb_publishable_... (publishable keys are public by design — see next pattern)
```

**Note**: Supabase publishable keys (`sb_publishable_...`) are intentionally public. Genesis **does not** redact them — leaking one is not a security incident. If a future downstream project decides to redact them anyway for paranoia, they can add a local pattern to their own skill copy.

### Stripe secret key

```
name: stripe_secret_key
regex: \bsk_(?:test|live)_[A-Za-z0-9]{24,}\b
rationale: Stripe secret keys. Any Genesis downstream project that wires Stripe needs these redacted — leaking a live key is a financial incident.
test_vectors:
  match: sk_live_0123456789abcdefghij0123
  match: sk_test_0123456789abcdefghij0123
  non-match: pk_live_... (Stripe publishable — public by design)
```

### AWS access key

```
name: aws_access_key
regex: \b(?:AKIA|ASIA|AIDA|ABIA|ACCA|AIPA|ANPA|ANVA|AROA|APKA|ASCA|ASIA)[A-Z0-9]{16}\b
rationale: AWS access keys have fixed 20-char length and a short list of known prefixes. AIDA is IAM user, ASIA is STS temporary, etc. Any of them in a session archive is a breach risk.
test_vectors:
  match: AKIAIOSFODNN7EXAMPLE
  match: ASIAIOSFODNN7EXAMPLE
  non-match: akia... (lowercase — not a valid AWS format)
```

### Google API key

```
name: google_api_key
regex: \bAIza[0-9A-Za-z\-_]{35}\b
rationale: Google API keys start with `AIza` and are 39 chars total. Present in any session that uses Gemini / Google Maps / Drive APIs.
test_vectors:
  match: AIzaSyABCDEFGHIJKLMNOPQRSTUVWXYZabcdefg
  non-match: AIza (too short)
```

### JWT (generic)

```
name: jwt_token
regex: \beyJ[A-Za-z0-9_\-]{10,}\.eyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}\b
rationale: Any JWT — the `eyJ...eyJ...<sig>` shape is unmistakable. Session tokens from OAuth flows, Supabase auth tokens, Auth0 tokens, internal service tokens all match.
test_vectors:
  match: eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.abcdefghijklmnop
  non-match: eyJsomething (missing the dot structure)
```

### SSH private key block

```
name: ssh_private_key_block
regex: (?s)-----BEGIN (OPENSSH|RSA|DSA|EC|ED25519) PRIVATE KEY-----.*?-----END \1 PRIVATE KEY-----
rationale: A multi-line private key block in a session archive means someone pasted one. Absolute must-redact. Uses `(?s)` for DOTALL so the body matches across newlines.
test_vectors:
  match: -----BEGIN OPENSSH PRIVATE KEY-----\nb3BlbnNzaC1rZXktdjEAAAA...\n-----END OPENSSH PRIVATE KEY-----
  non-match: -----BEGIN CERTIFICATE----- (public cert — not a private key)
```

### Generic "secret-shaped" long base64 / hex

```
name: generic_long_hex
regex: \b[a-f0-9]{64,}\b
rationale: A 64+ character hex string is almost always a hash, a key, or a signature. Emits false positives on SHA256 checksums (which are legitimately public), but the cost of a false positive is "session archive is slightly less useful" while the cost of a false negative is a key leak. Apply last, after the specific patterns, so a matched pattern with a better name wins.
test_vectors:
  match: 0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef
  non-match: deadbeef (too short)
  false_positive_acceptable: SHA256 hashes of files — OK to redact, user can re-compute from source

name: generic_long_base64
regex: \b[A-Za-z0-9+/]{40,}={0,2}\b
rationale: Base64-encoded strings ≥40 chars are usually keys, tokens, or encrypted blobs. Same false-positive calculus as hex — redact-heavy wins over leak-risk.
test_vectors:
  match: aGVsbG8tdGhpcy1pcy1hLXRlc3Qtc3RyaW5nLXRoYXQtaXMtbG9uZw==
  false_positive_acceptable: long source-code identifiers — rare and recoverable
```

### `.env.local` content paste-back

```
name: env_local_paste
regex: (?m)^\s*(GH_TOKEN|GITHUB_TOKEN|API_KEY|SECRET|PRIVATE_KEY|PASSWORD|DB_PASS|DB_PASSWORD|DATABASE_URL|ANTHROPIC_API_KEY|OPENAI_API_KEY|SUPABASE_SERVICE_KEY|STRIPE_SECRET)\s*=\s*.+$
rationale: If the user pastes the contents of a `.env.local` into a prompt, every value line matches. Redact the **value** only — keep the variable name so the archive still shows that an env was being edited. Uses `(?m)` for per-line anchoring.
test_vectors:
  match: GH_TOKEN=github_pat_11xxxxxxxxxxxxxxxx
  match:     API_KEY =abcdef
  non-match: GH_TOKEN=# comment (commented line with no value)
```

**Special handling**: this pattern replaces the match with `<VAR>=[REDACTED:env_local_paste]` instead of fully replacing the line, so the archive still shows which variable was assigned. The skill's redactor has one-off logic for this pattern name — see the Python pseudocode below.

## Application order

Patterns are applied in this order (specific before generic):

1. `ssh_private_key_block` — multi-line, most destructive if leaked
2. `github_pat_finegrained`
3. `github_classic_token`
4. `anthropic_api_key`
5. `openai_api_key`
6. `supabase_pat`
7. `supabase_secret_key`
8. `stripe_secret_key`
9. `aws_access_key`
10. `google_api_key`
11. `jwt_token`
12. `env_local_paste`
13. `generic_long_hex` — catches everything specific patterns missed
14. `generic_long_base64` — same

Earlier patterns that match a substring are not re-matched by later patterns. Each pattern logs its hit count; the sum of hit counts is surfaced in the archive frontmatter.

## Pseudocode

```python
REDACTION_PATTERNS = [
    ("ssh_private_key_block", re.compile(r"...", re.DOTALL), "..."),
    ("github_pat_finegrained", re.compile(r"\bgithub_pat_[A-Za-z0-9_]{82,}\b"), "..."),
    # ... etc ...
]

def redact(text: str, hit_counter: dict) -> str:
    for name, pattern, _ in REDACTION_PATTERNS:
        if name == "env_local_paste":
            def replace(match):
                hit_counter[name] = hit_counter.get(name, 0) + 1
                var = match.group(1)
                return f"{var}=[REDACTED:{name}]"
            text = pattern.sub(replace, text)
        else:
            def replace(match):
                hit_counter[name] = hit_counter.get(name, 0) + 1
                return f"[REDACTED:{name}]"
            text = pattern.sub(replace, text)
    return text
```

## Halt-on-leak verification

After the archive is written to disk, **re-open** the file and apply the full pattern set to its content. If any pattern hits, the verification is **RED**:

1. Log the pattern name (never the match) and its hit count
2. Delete the archive file
3. Surface the incident to the user: *"Archive halted — pattern `<name>` leaked through redaction (N hits). File deleted. Audit the redaction set and strengthen before retry."*
4. Do not auto-retry

The halt-on-leak gate is the skill's security floor and runs on every invocation.

## Testing the redaction set

Before any change to this file is merged, run the dogfood suite:

1. For every pattern, confirm the `match` test vector is redacted
2. For every pattern, confirm the `non-match` test vector is not redacted
3. Run the redactor against the current session's JSONL (the one this skill was written in) and inspect the output — there should be a non-trivial hit count on `github_pat_finegrained` because this very session used `GH_TOKEN` for PR creation

If any vector fails, block the merge.

## Adding new patterns

When a new token format is encountered:

1. Add the `(name, regex, rationale, test_vectors)` tuple to the list above, in the correct application order
2. Add at least one known-good match and one known-good non-match to `test_vectors`
3. Re-run the dogfood suite
4. Bump the skill version (new patterns are a functional change, not a cosmetic one)
5. Log the addition in the skill's CHANGELOG

## What this pattern set does NOT claim to catch

- **Handwritten "obvious" secrets** like `password=hunter2` without a known variable name prefix (the `env_local_paste` pattern catches the common ones but not every format)
- **Secrets embedded in URLs** like `https://user:pass@host/path` (a URL pattern could catch these but adds false positives on markdown links)
- **Secrets with unknown new prefixes** (will be added as they appear)
- **Secrets in binary attachments** (attachments are compressed to markers at classification — the skill never reads their content)

Users with specific additional patterns add them locally. The base set is the intersection of what every Genesis downstream project needs.
