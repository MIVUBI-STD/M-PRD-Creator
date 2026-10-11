---
id: document.foundation.production-flow
class: DOCUMENT
domain: foundation
role: WORKFLOW
authority: CANONICAL
lifecycle: ACTIVE
---

# Canonical Production Workflow

Status: active policy

## Naming contract

PRD-Creator uses one human workflow vocabulary:

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

Rules:

- numbered stage aliases are not workflow names;
- numeric prefixes on files in `docs/foundation/` are ordering only;
- numeric markers in generated PRD navigation are document-section ordinals only;
- machine statuses such as `ready_for_prd`, `handoff_ready`, `voice_requirements_ready`, and `voice_delivery_ready` remain unchanged because they are state vocabulary, not human stage names.

## Project Setup

Recover repository/project continuity and choose the smallest current owner. This is repository/session setup, not project meaning authoring.

## Project Requirements

```text
sources + current instruction + approved decisions
→ authority/provenance recovery
→ material requirements
→ Completion | Proposal | Blocked resolution
→ exact requirement revision binding
```

Output authority: `state/source-inventory.yaml`, `state/requirement-register.yaml`, `state/intake-state.yaml`.

## PRD Production

```text
approved Project Requirements
→ canonical work/content.md
→ strict work/render-data.json
→ deterministic PRD rendering
```

PRD Production preserves approved meaning; it does not invent missing product decisions.

## Production Assets

Production Assets is optional and bounded:

```text
approved project model
→ concrete resources somebody must prepare
→ work/asset-requirements.md when non-Voice resources exist
```

Voice resources join the same Production Assets presentation later through stable Owner ID + Moment ID + Voice ID.

## PRD Handoff

```text
current Project Requirements
+ PRD Production
+ Production Assets when present
→ mechanical validation
→ semantic reconciliation
→ exact-byte acceptance
→ handoff_ready
```

Only an accepted PRD Handoff may enter Voice Requirements.

## Voice Requirements

```text
accepted PRD Handoff
→ justified player-facing Voice moments
→ stable Owner/Moment/Voice identity
→ communication intent + required facts + timing truth
→ voice_requirements_ready | no_voice_required
```

Voice Requirements owns what must be communicated, not final performance wording.

## Voice Production

```text
Voice Requirements
→ Actor Baseline / Voice Fit
→ natural spoken wording
→ Expression Coverage / Audio Tags
→ pronunciation/language strategy
→ continuity + duration planning
→ Voice Script Readiness
→ voice_script_ready
```

Canonical output: `work/voice-production.md`.

## Voice Delivery

```text
current PRD Handoff
+ Voice Requirements
+ Voice Production
→ mechanical parity
→ semantic/craft readiness
→ current consolidated project HTML
→ exact Voice acceptance
→ voice_delivery_ready | needs_revision
```

Actual audio quality or pronunciation approval requires heard evidence.

## First wrong owner

```text
source / project decision → Project Requirements
PRD meaning / projection → PRD Production
resource requirement → Production Assets
PRD acceptance / freshness → PRD Handoff
Voice scope / communication intent → Voice Requirements
Voice wording / acting / pronunciation / generation strategy → Voice Production
Voice acceptance / delivery evidence → Voice Delivery
```

## Stop rule

Do not create parallel workflow names, aliases, compatibility terminology, or duplicate status systems. Use the canonical names above and stop when the current owner is correct and sufficiently proven.