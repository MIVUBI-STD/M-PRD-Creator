---
id: document.knowledge.skills.activation-matrix
class: DOCUMENT
domain: knowledge
role: GUIDE
authority: CANONICAL
lifecycle: ACTIVE
---

# Skill Activation Matrix

Use only when root `AGENTS.md` plus the nearest obvious owner still leave the semantic/technical boundary ambiguous.

## Activation

| Actual problem | Add specialist? |
|---|---|
| Project Requirements, PRD Production meaning, Production Assets meaning, or PRD Handoff semantics | `project-document-production` |
| Voice Requirements, Voice Production meaning, or Voice Delivery semantics | `voice-production` |
| Semantics correct; renderer/template/validator/compositor/CLI mechanics wrong | No → `kits/prd-creator/AGENTS.md` |
| Shared dependency/test/CI mechanics wrong | No → repository engineering |

Do not select a semantic specialist merely because HTML, Python, ElevenLabs, renderer, validator, or another implementation technology appears in the task.

For non-trivial repository/system Development, `development-brief` remains the front door. Normal Production Execution and bounded Maintenance do not load it merely because tools or generated files are involved.

## Ambiguity test

1. What exact contract is wrong?
2. Is the defect about meaning or executable mechanics?
3. Which canonical workflow owner would still own it if file format/language changed?
4. Does a root specialist add judgment beyond root policy + nearest owner?

If the owner is obvious, route directly.

## Canonical boundary language

Use only:

```text
Project Requirements
PRD Production
Production Assets
PRD Handoff
Voice Requirements
Voice Production
Voice Delivery
```

Do not introduce a second numbered/internal stage vocabulary.

## Root skill set

```text
.agents/skills/development-brief
.agents/skills/project-document-production
.agents/skills/voice-production
```

Do not add/split/rename a root skill unless repeated work proves a distinct reusable semantic ownership gap.