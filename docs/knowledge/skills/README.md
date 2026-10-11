---
id: document.knowledge.skills.router
class: DOCUMENT
domain: knowledge
role: ROUTER
authority: CANONICAL
lifecycle: ACTIVE
---

# Skill Catalog

Use this note for the current root skill inventory and ownership boundary. Historical consolidation rationale stays in decisions/reviews.

## Canonical root skills

| Skill | Function |
|---|---|
| `development-brief` | front door for non-trivial repository/system Development |
| `project-document-production` | semantic judgment for Project Requirements, PRD Production, Production Assets, and PRD Handoff |
| `voice-production` | semantic judgment for Voice Requirements, Voice Production, and Voice Delivery |

The canonical root set is intentionally small.

## Relationship to the production package

```text
root AGENTS / development-brief
→ decide work mode + semantic vs technical boundary
→ optional one root semantic specialist
→ kits/prd-creator/SKILL.md or AGENTS.md
→ smallest domain / implementation owner
```

### Project / PRD domain

`project-document-production` owns reusable Project Requirements / PRD Production / Production Assets / PRD Handoff semantic judgment.

Exact owners:

```text
kits/prd-creator/intake/SOURCE-INTAKE.md
kits/prd-creator/document/CONTENT-CONTRACT.md
kits/prd-creator/production-assets/CONTRACT.md
kits/prd-creator/renderer/CONTRACT.md
kits/prd-creator/document/VALIDATION.md
```

### Voice domain

`voice-production` owns reusable Voice semantic judgment.

```text
kits/prd-creator/voice/EXTRACTION.md
kits/prd-creator/voice/PERFORMANCE-WRITING.md
kits/prd-creator/voice/VALIDATION.md
```

These correspond to Voice Requirements, Voice Production, and Voice Delivery respectively.

Project/PRD and Voice remain separate semantic domains even though they share one package.

## Naming rule

Describe root skills and package owners with the canonical semantic boundary names. Do not create a separate numbered/internal naming layer.

## Repository engineering is not a production skill

Dependency, test, CI, and repository-invariant mechanics remain direct repository engineering ownership.

## Skill freeze rule

Do not add/rename/split a root skill merely because a new file format, renderer/validator, Production Asset type, project-specific content, or one-off technical bug appears. Change the root skill set only when repeated work proves a genuinely distinct reusable semantic owner.