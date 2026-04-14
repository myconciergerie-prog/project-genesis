<!-- SPDX-License-Identifier: MIT -->

# memory/themes/

Per-topic memory files land here as the project grows. Themes are tags like `auth`, `plugin-distribution`, `session-history`, `pepite-routing`, `multidevice`, etc. Each theme gets its own markdown file that consolidates related project-level knowledge.

## When to create a theme file

Promote a topic from `project/` to `themes/` when:

- Three or more `project/` entries touch the same topic
- The topic warrants its own stable reference page that captures the cumulative knowledge
- A session-open check would benefit from loading the theme file directly

## Format

Standard memory frontmatter:

```yaml
---
name: <theme name>
description: <one-line summary of what this theme covers>
type: theme
---

<body — structured documentation of everything we know about this topic>
```

## Currently populated themes

*(None — the project is fresh. Themes will accumulate as Étape 5 work generates multi-entry patterns.)*
