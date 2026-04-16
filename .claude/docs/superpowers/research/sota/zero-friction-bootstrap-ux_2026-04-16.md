---
name: Zero-friction bootstrap UX patterns — cross-platform research
description: How v0.app, Bolt.new, Replit, create-next-app, @clack/prompts, Charm Gum, and others achieve zero-friction project creation. Conversational onboarding, single-prompt patterns, progressive disclosure, CLI UX toolkit.
type: sota
expires_at: 2026-04-23
researched_at: 2026-04-16
scope: universal
---

# Zero-friction bootstrap UX — 2026-04-16

## Gold standard: one prompt → running project

v0.app, Bolt.new, Replit Agent all converge on: user types one natural-language
description, system creates everything. 2 steps (sign up + describe).

## Key patterns

### 1. The meta-question (create-next-app v16)
"Use recommended defaults?" with 3 choices (yes / reuse previous / customize).
ONE branching question replaces N detail questions for the common case.

### 2. @clack/prompts — the state of the art for CLI wizards
`intro → group → spinner/tasks → outro`. The `group()` function chains prompts
as a single conversational unit with shared state. Used by SvelteKit's `sv create`.
Also exposes `stream` for LLM-native dynamic rendering.

### 3. Charm Gum — beautiful prompts without code
Single binary, cross-platform. `gum input`, `gum choose`, `gum confirm`,
`gum spin`, `gum style`. Build a full wizard from bash scripts.

### 4. Conversational form data
- One-question-at-a-time: 40-60% completion vs 15-20% for traditional forms
- 72% higher completion rates (Stacked Marketer)
- 25-35% conversion increase for SaaS switching to conversational format

### 5. Progressive disclosure
Derive, don't ask. From a project description, derive: slug, license, plugin flag,
stack hints. Only ask what cannot be derived: the idea, the name, the account.

### 6. Stored preferences (Yeoman/create-next-app)
After first run, remember GitHub account, language, etc. Second project: one question.

### 7. Terminal delight
- cli-spinners: 70+ styles (moon phases, bouncing dots)
- Terminal bell on completion: macOS `afplay`, Windows `[console]::beep`, Linux `paplay`
- GitHub Copilot CLI: semantic ANSI color roles, graceful degradation
- Warp: command blocks with visual boundaries

## Competitive landscape

| Tool | Input | Auth friction | Output |
|---|---|---|---|
| v0.app | One prompt | Google SSO | Deployed app |
| Bolt.new | One prompt | StackBlitz account | In-browser app |
| Replit | One prompt | Replit account | Cloud project |
| create-next-app | Template + flags | None (local) | Local project |
| Genesis v2 | Conversation | One OAuth click | YOUR GitHub repo |
