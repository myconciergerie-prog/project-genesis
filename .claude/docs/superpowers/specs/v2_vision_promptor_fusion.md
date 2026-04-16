# Genesis v2 — Dis-moi ton idee. Je m'occupe du reste.

## The insight

Genesis v1 is an engineer's protocol that speaks to engineers.
Promptor is a conversational interface that speaks to humans.
v0.app, Bolt.new, and Replit proved that "one prompt → running project" is the
gold standard: 2 steps (sign up + describe), zero plumbing visible.

Genesis v2 = a Promptor that creates projects instead of prompts,
powered by the same 7-phase engine, with a v0/Bolt-grade surface.

## The Victor test

Victor, 77, has a magnificent idea. He opens Claude Code.
He says: "Je veux creer une appli pour que les gens de mon quartier
partagent leurs courses."

Three minutes later, his project exists on GitHub.
He never sees an SSH key, a PAT, a scope checkbox, or a config file.
He never leaves the conversation. He hears a soft chime when it's done.

---

## LAYER A — The Conversation (what Victor sees)

Structural skeleton: @clack/prompts pattern
(`intro → group → spinner/tasks → outro`), with Promptor's iteration loop.

### Etape 1 — L'Etincelle

Genesis greets warmly, then asks **at most 3 questions**.
Adaptive tone: if Victor writes casually, Genesis responds warmly with zero
jargon. If a senior engineer writes technically, Genesis matches.

```
 Bienvenue dans Genesis.

 Dis-moi ton idee — qu'est-ce que tu veux creer ?
 > Je veux un truc pour suivre mes depenses au quotidien

 Comment veux-tu appeler ce projet ?
 > Mon Budget

 Tu as un compte GitHub ?
   ● Oui, j'en ai un
   ○ Non, je veux en creer un
   ○ C'est quoi GitHub ?
```

The third option ("C'est quoi GitHub ?") triggers a one-sentence explanation:
"GitHub, c'est un coffre-fort en ligne pour ton projet — personne n'y touche
sauf toi. Je vais t'en creer un gratuitement."

**What Genesis derives silently** (the Promptor "Calibrage"):
- slug: `mon-budget` (from project name, lowercased, accents stripped)
- vision: Victor's words verbatim
- is-a-plugin: no (description doesn't mention Claude Code/skills)
- license: MIT (default)
- plan-tier: detected from current Claude session
- stack-hints: inferred from description (or deferred to v0.2.0)
- scope-locks: none (first project)

**The meta-question** (from create-next-app pattern):
For power users who want control, Genesis offers ONE branching question:
"Tu veux que je decide tout pour toi, ou tu preferes choisir les details ?"
- "Decide pour moi" → Victor path (3 questions, derive everything)
- "Je veux choisir" → Engineer path (show slug, license, stack, plugin flag)

### Etape 2 — La Creation

Genesis shows what it understood (Promptor Partie B — the mirror):

```
 Voila ce que j'ai compris :

  Projet    Mon Budget
  Idee      Suivre ses depenses au quotidien
  GitHub    mon-budget (prive, rien que pour toi)

  Je vais creer :
  • Un espace de travail structure
  • Un depot GitHub prive
  • Un systeme de memoire pour que je me souvienne de tout
  • Un point de depart pour commencer a construire

 Ca te va ?  oui / j'ajuste / stop
```

No jargon. No "memory architecture", no "R1-R10 rules", no "research cache."
Victor sees *what*, never *how*.

On "oui" — **the build starts silently**. Victor sees a progress stream:

```
 ◐ Je prepare ton espace de travail...
 ✓ Espace pret

 ◐ Je me connecte a GitHub...
   → Une page va s'ouvrir dans ton navigateur.
     Clique sur "Authorize" et reviens ici.
```

**This is the ONE moment Victor leaves the conversation.**
A browser tab opens (the right one — see Layer B for routing).
Victor sees a GitHub page with a green "Authorize" button.
He clicks it. The tab closes. Back to the terminal:

```
 ✓ GitHub connecte

 ◐ Je cree ton projet sur GitHub...
 ✓ Projet cree : github.com/victor/mon-budget

 ◐ Je structure la memoire...
 ✓ Memoire prete

 ◐ Premier enregistrement...
 ✓ Version 0.1.0 enregistree

 ♪ (soft chime)
```

### Etape 3 — Le Miroir (Promptor's auto-critique + iteration)

```
 C'est pret ! Voila ce qui existe maintenant :

  GitHub     github.com/victor/mon-budget
  Fichiers   README.md, memoire de projet, regles de travail
  Version    0.1.0

  Quelque chose a ajuster avant qu'on commence a construire ?
  > Non c'est bon

 Parfait. Dis-moi quand tu veux commencer la premiere
 fonctionnalite — je suis pret.
```

If Victor says "j'ajuste" → iteration loop (Promptor Etape 3).
If a senior engineer wants details → `inspect` shows the full file tree.

---

## LAYER B — The Engine (what Victor never sees)

The 7-phase protocol, unchanged in structure, rewritten at the auth layer.

### The auth revolution — 4 lines, 1 click

Research confirmed: `gh` CLI supports everything we need.

```bash
# Route OAuth to the correct Chrome profile
export GH_BROWSER="chrome.exe --profile-directory=\"Profile 2\""

# ONE user interaction: browser opens, user clicks "Authorize"
gh auth login --web --git-protocol https --scopes "repo,workflow,read:org"

# Wire git credential helper (silent, no interaction)
gh auth setup-git

# Create repo + push in one command (silent, no interaction)
gh repo create "$OWNER/$REPO" --private --source=. --remote=origin --push
```

**Zero SSH keys at bootstrap.** HTTPS + OAuth token handles everything.
Per-project SSH identity becomes a v0.2.0 optimization for engineers who
want key isolation — not a bootstrap gate.

**Zero PAT creation.** The OAuth token from `gh auth login` replaces the
fine-grained PAT. No scope checkboxes, no one-time copy, no `.env.local`
manual step.

**Zero repo creation UI.** `gh repo create` does it in one command.
No "don't check any initialization checkbox" instruction.

### What each v1 phase becomes in v2

| v1 Phase | v1 Surface | v2 Surface |
|---|---|---|
| -1 Dependencies | 3-mode ladder + consent cards | Silent — detect and auto-install, pause only at true security floor |
| 0 Seed loading | `config.txt` file parsing | Conversation parsing — Etape 1 answers become `bootstrap_intent.md` |
| 1+2 Rules + memory | Scaffold + consent | Silent — progress stream shows "Je prepare ton espace..." |
| 3 Git init | SSH keygen + host alias + paste key | `gh auth login --web` (ONE click) + `gh auth setup-git` |
| 4 Project seeds | master.md + README from intent | Same, but README uses Victor's words, zero dev jargon |
| 5.5 Auth preflight | 6 manual browser steps | ELIMINATED — absorbed into the single `gh auth login` |
| 6 Commit + push | `git push` + tag | `gh repo create --source=. --push` (ONE command, silent) |
| 7 Resume + archive | Resume prompt + session-post-processor | Progress stream outro + "Dis-moi quand tu veux commencer" |

### The GH_BROWSER solution for profile routing

v1 friction F16: `gh auth login --web` opens the OS default browser.
Solution: `GH_BROWSER` environment variable.

```bash
# Windows — Chrome Profile 2 (myconciergerie@gmail.com)
export GH_BROWSER='chrome.exe --profile-directory="Profile 2"'

# macOS
export GH_BROWSER='open -a "Google Chrome" --args --profile-directory="Profile 2"'
```

Genesis reads the Chrome profile map from Layer 0 and sets `GH_BROWSER`
automatically before calling `gh auth login`. Victor never knows.

### For users with no GitHub account

If Victor says "C'est quoi GitHub ?" or "Non, je veux en creer un":

1. Genesis explains in one sentence
2. `gh auth login --web` opens the GitHub login page
3. Victor sees "Create an account" → "Continue with Google" (Gmail as favorite)
4. Victor signs in with Google → account created → OAuth authorized
5. Back to terminal — Genesis continues silently

ONE flow. No separate "create account" then "create PAT" then "create repo."

---

## UX TOOLKIT — Making it funky

Research identified these tools for the terminal experience:

| Need | Tool | Why |
|---|---|---|
| Guided wizard | **@clack/prompts** | `intro → group → spinner → outro` maps 1:1 to Etape 1/2/3 |
| Beautiful prompts | **Charm Gum** | Arrow-key select, fuzzy filter, styled text — zero typing for Victor |
| Progress with personality | **cli-spinners** (70+ styles) | Moon phases, bouncing dots, not a dead cursor |
| Completion signal | **Terminal bell** / `PowerShell beep` | Victor hears "done" without watching the screen |
| Adaptive tone | **LLM-native** | Claude Code IS the LLM — tone adaptation is built in |
| Block output | **Warp-inspired** | Each step visually contained, not a wall of text |
| Cross-platform | **Semantic ANSI roles** | Degrade gracefully: Windows Terminal, VS Code, iTerm2 |

### The sound of Genesis

When the bootstrap completes:
- macOS: `afplay /System/Library/Sounds/Glass.aiff`
- Windows: `powershell "[console]::beep(880,200); [console]::beep(1108,300)"`
- Linux: `paplay /usr/share/sounds/freedesktop/stereo/complete.oga`

Two notes. A rising interval. The sound of something being born.

---

## WHAT PROMPTOR TEACHES GENESIS — the 6 principles

1. **Start with questions, not forms.** Promptor asks 2 questions before
   creating anything. Genesis v1 requires a pre-written config.txt.
   v2: conversation first, derive everything.

2. **Show your work, then critique it.** Promptor's 4-part response
   (calibrage + prompt + auto-critique + questions) builds trust through
   transparency. v2: the mirror step (Etape 2) shows Victor what Genesis
   understood BEFORE building.

3. **Iterate until perfect.** Promptor loops Etape 2 → 3 until 5 stars.
   Genesis v1 runs once, linearly. v2: "Ca te va ? oui / j'ajuste / stop"
   at every stage.

4. **Hide the plumbing.** Promptor never mentions "token window" or
   "system prompt architecture." v2: Victor never sees SSH, PAT, SPDX,
   YAML, git remotes, Chrome profiles, or scope checkboxes.

5. **Be warm.** "Es-tu pret ?" vs "Top-level consent card."
   v2: "Bienvenue dans Genesis" + soft chime on completion.

6. **Derive, don't ask.** Promptor's Partie A (calibrage) silently adapts
   to the target tool. v2: Genesis silently derives slug, license, plugin
   flag, plan tier from the conversation. The meta-question ("Tu veux
   decider ou je decide ?") is the ONLY branching point.

---

## COMPETITIVE POSITIONING

| Tool | Creates from | Auth friction | Target user |
|---|---|---|---|
| v0.app | One prompt | Vercel account (Google SSO) | Anyone |
| Bolt.new | One prompt | StackBlitz account | Anyone |
| Replit Agent | One prompt | Replit account | Anyone |
| create-next-app | Template + flags | None (local only) | Developers |
| Genesis v1 | config.txt + 6 manual steps | SSH + PAT + repo UI | Engineers |
| **Genesis v2** | **One conversation** | **One "Authorize" click** | **Anyone — Victor** |

Genesis v2's edge: it creates on YOUR machine, in YOUR GitHub, with YOUR
memory architecture. v0/Bolt/Replit own your project. Genesis gives it to you.

---

## ANTI-FRANKENSTEIN CHECK

This is NOT adding features. This is removing friction.
- 7 phases still exist → same engine
- 6 skills still exist → same skills
- Memory architecture stays → same 7 types
- Research cache stays → same R8 TTL

What changes:
- SURFACE: conversation replaces config.txt
- AUTH: OAuth replaces 6-step browser dance
- FEEDBACK: progress stream replaces consent cards
- TONE: warm and funky replaces bureaucratic
- SOUND: a chime says "c'est pret" without reading the terminal

The engine is the same. The experience is transcendent.

> "Dis-moi ton idee. Je m'occupe du reste."
