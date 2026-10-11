---
id: document.knowledge.router
class: DOCUMENT
domain: knowledge
role: ROUTER
authority: CANONICAL
lifecycle: ACTIVE
---

# Repository Knowledge

Updated: 2026-09-09

This directory is the navigation and operating-memory layer for PRD-Creator. It does not define a second boot policy or duplicate contracts owned by root/foundation/kits.

## Canonical workflow language

Current project-production references use:

```text
Project Requirements
→ PRD Production
   └─ Production Assets when required
→ PRD Handoff
→ Voice Requirements
→ Voice Production
→ Voice Delivery
```

Use the same boundary names in routing, ownership, continuation, and operator communication.

## Current owners

| Need | Owner |
|---|---|
| Active continuation / resume checkpoint | [next-action.md](./next-action.md) |
| Work routing | [work-routing.md](./work-routing.md) |
| Repository/code/procedure ownership | [ownership.md](./ownership.md) |
| Source/state authority | [source-authority.md](./source-authority.md) |
| Development lifecycle overview | [work-modes/development.md](./work-modes/development.md) |
| Maintenance workflow | [work-modes/maintenance.md](./work-modes/maintenance.md) |
| Skill inventory | [skills/README.md](./skills/README.md) |
| Ambiguous specialist selection | [skills/activation-matrix.md](./skills/activation-matrix.md) |
| Durable decision index | [decisions/README.md](./decisions/README.md) |
| Current validation evidence | [reviews/current-validation.md](./reviews/current-validation.md) |
| Historical review evidence | [reviews/history/](./reviews/README.md) |
| Future/non-active work | [operations/backlog.md](./operations/backlog.md) |
| Boot/routing regression scenarios | [operations/boot-baseline.md](./operations/boot-baseline.md) |

Root `../../AGENTS.md` owns boot/work modes/naming. GitHub execution remains owned by root `GITHUB_RULES.md`.

## Separation rule

```text
active continuation       → next-action.md
durable choice/reason     → decisions/
current proof             → reviews/current-validation.md
historical proof          → reviews/history/
future/non-active work    → operations/backlog.md
production policy         → ../foundation/
project-specific state    → external/local project package
```

Historical reviews/decisions are evidence and rationale, not automatic current work.