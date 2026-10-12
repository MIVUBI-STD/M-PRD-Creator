---
id: document.foundation.product-boundaries
class: DOCUMENT
domain: foundation
role: CONTRACT
authority: CANONICAL
lifecycle: ACTIVE
---

# Product Boundaries

Status: active policy

## Canonical workflow vocabulary

```text
Project Setup
→ Project Requirements
→ PRD Production
   └─ Production Assets when required
→ PRD Handoff
→ Voice Requirements when Voice is justified
→ Voice Production
→ Voice Delivery
```

These names are canonical for both repository-internal reasoning and user/operator communication. Numeric file prefixes and generated-document section numbers are ordering only.

## Design-before-build product definition

PRD-Creator helps design a Minecraft map **before any world exists**. An
approved brief, goals, constraints and optional references are enough to
begin. Project Requirements develops and resolves material Game Design
choices; PRD Production expresses the approved experience, game systems,
level needs and technical behavior as a buildable specification.

Existing maps can be optional reference evidence, not mandatory test fixtures
or sources of new project facts. Building a world, inspecting command blocks,
finding implementation bugs, running multiplayer sessions or measuring real
device performance are **not** PRD-Creator design outputs. Those belong to
downstream Map Development and Gameplay QA after PRD Handoff.

## Project / PRD Domain

Inside `kits/prd-creator/`, the Project/PRD domain owns:

- Project Requirements: project-source intake, requirement recovery, and Proposal/Completion/Blocked resolution;
- PRD Production: canonical PRD content and deterministic projection through the approved Golden grammar;
- Production Assets: same-project concrete resource requirements when justified;
- PRD Handoff: development-readiness validation, acceptance, and concise team handoff.

It does not own downstream Voice wording.

## Voice Domain

### Voice Requirements
- extract justified Voice moments from accepted PRD meaning;
- preserve Speaker/Channel/Trigger/Purpose and required facts;
- prevent redundant or unsupported Voice scope.

### Voice Production
- create final spoken wording and Eleven v3 performance direction;
- preserve actor identity, naturalness, expression, pronunciation strategy, timing intent, and continuity;
- own canonical `work/voice-production.md`.

### Voice Delivery
- validate exact Voice requirements/production/project-HTML integrity;
- decide Voice Script Readiness and delivery evidence truthfully;
- keep actual audio approval separate until heard evidence exists.

## Voice Domain Does Not Own

- repairing unresolved project/PRD decisions by invention;
- adding new Voice moments during script polishing or delivery review;
- rebuilding accepted PRD navigation/page identity;
- treating derived HTML as higher authority than canonical script/requirements.

## Shared Boundary Rule

Project/PRD and Voice are separate semantic domains inside one PRD-Creator package. When downstream work exposes a missing or contradictory upstream decision, reopen the correct canonical owner instead of hiding the decision inside polished prose or derived presentation.
