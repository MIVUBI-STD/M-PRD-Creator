---
id: document.knowledge.work-routing
class: DOCUMENT
domain: knowledge
role: WORKFLOW
authority: CANONICAL
lifecycle: ACTIVE
---

# Work Routing

Compact human reference only. Root `AGENTS.md` is the canonical work-mode, boot, authority, naming, and skill-budget owner.

## Mode map

| User intent | Mode | Primary route |
|---|---|---|
| Inspect, understand, decide, or recover context | Plan | current authority + smallest relevant owner |
| Create/revise Project Requirements, PRD Production, Production Assets, or PRD Handoff | Production Execution | smallest PRD owner; add `project-document-production` only when semantic judgment is needed |
| Create/revise Voice Requirements, Voice Production, or Voice Delivery | Production Execution | smallest Voice owner; add `voice-production` only when semantic/performance judgment is needed |
| Change PRD-Creator itself | Development | `development-brief` + first wrong owner |
| Fix bounded defect/regression/stale behavior | Maintenance | concrete failure or explicit target + first wrong owner |

The canonical production sequence is:

```text
Project Requirements
→ PRD Production
   └─ Production Assets when required
→ PRD Handoff
→ Voice Requirements
→ Voice Production
→ Voice Delivery
```

Do not translate these boundaries into a second numbered/internal stage vocabulary.

## Owner rule

Route by what is wrong, not by file type:

```text
project / PRD / resource meaning wrong
→ project-document-production + nearest semantic owner

Voice scope / communication / performance meaning wrong
→ voice-production + nearest Voice semantic owner

meaning correct; renderer / template / validator / CLI behavior wrong
→ kits/prd-creator/AGENTS.md → exact implementation owner

shared dependency / test / CI wrong
→ repository engineering owner
```

If the owner is already obvious, use it directly. Consult `ownership.md`, `source-authority.md`, or `skills/activation-matrix.md` only when the direct route remains genuinely ambiguous.

## Continuity

```text
current execution state → exact source + topic-related commit evidence
current/future development intent → ../../planning/development.md
future / non-active work → ../../planning/backlog.md
historical evidence → reviews/history/
durable rationale → decisions/
```

Historical TODOs, reviews, and backlog items do not become active work unless current user intent or current continuation promotes them.