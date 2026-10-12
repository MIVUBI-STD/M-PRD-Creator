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

## Product goal

Turn an initial map brief and its relevant sources into an **approved Game
Design / System Design** and a clear implementation-ready PRD. A playable
Minecraft world, map code or a previous map is **not a prerequisite**.
Creating, patching or runtime-testing a map is outside this production
workflow. Design decisions and implementation test evidence are different.

Game Design, System Design, Level Design and Technical Design are
responsibilities **within existing named flows**, not extra flow names.

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

**Input:** an authorized new-map brief or a clearly selected project.

**Work:** select the project, identify current sources and privacy boundary, recover the smallest relevant context. No existing world is required.

**Output:** one project working context; this is session/repository preparation, **not** the Game Design decision owner.

**Exit:** current project and source authority are unambiguous. No speculative files or unrelated sample-map selections.

## Project Requirements

**Input:** the project brief (which may be the only source), constraints, approved decisions and optional references.

**Work:** develop and reconcile the intended experience, audience, core gameplay loop, player journey, mechanisms and their material rules. Distinguish source facts from AI design choices; offer a grounded **Proposal** where the brief leaves multiple valid designs.

**Decision rule:** current authority → recover; one necessary consequence → Completion; multiple material choices → Proposal requiring approval; no responsible option → Blocked / decision requested.

**Output:** canonical `state/source-inventory.yaml`, `state/requirement-register.yaml`, and `state/intake-state.yaml`, with optional human-readable review.

**Exit:** no consequential unresolved design decisions; `ready_for_prd` binds the exact current approved requirement bytes. Do not create mechanics by silently borrowing from reference maps.

## PRD Production

**Input:** the current `ready_for_prd` Project Requirements model, **not** a completed map.

**Work:** specify approved Game Design and System Design in the existing PRD surfaces: Overview (intent/context), Gameplay Flow (journey), Gameplay (player rules/outcomes), Level Design (space/navigation/build needs), Developer (events, state ownership, results, reset/recovery). Use the [semantic content contract](../../kits/prd-creator/document/CONTENT-CONTRACT.md).

**Output:** `work/content.md` (canonical meaning), `work/render-data.json` (strict projection) and derived PRD pages.

**Exit:** the approved rules are actionable across relevant roles, source/content bindings are current and rendering succeeds. New material design choices return to Project Requirements; rendering does not establish semantic approval.

## Production Assets

**Input:** approved gameplay/build requirements that justify concrete production resources.

**Work:** identify the actual non-Voice assets and their Owner/Moment/Asset relationships, without inventing filler.

**Output:** optional `work/asset-requirements.md` and its derived presentation.

**Exit:** required resources are actionable, or the capability is omitted when no asset work is justified. Voice remains downstream and optional.

## PRD Handoff

**Input:** current Project Requirements, canonical PRD content/projection, and optional Production Assets.

**Work:** mechanical validation + source-to-design semantic reconciliation, cross-role coherence, Material Conservation and visual evidence only when claimed.

**Output:** exact-revision `work/acceptance.md`, current versioned delivery and `state/handoff-state.yaml` when accepted.

**Exit:** `development_ready` accepts the meaning for implementation; `handoff_ready` binds the accepted delivery. **Neither means a Minecraft world has been built or playtested.** The design process may stop here if Voice is not needed.

## Voice Requirements

**Input:** accepted `handoff_ready` PRD **only where player-facing Voice is justified**.

**Work:** identify Voice moments, speaker/trigger/placement and required communication, without writing final performance text.

**Output:** `work/voice-requirements.md` and stable Owner/Moment/Voice identity.

**Exit:** `voice_requirements_ready`, or an accepted `no_voice_required` decision. No Voice work is forced for a map that does not need it.

## Voice Production

**Input:** ready Voice Requirements.

**Work:** author spoken wording and actor, acting, pronunciation, duration and continuity direction without changing approved map meaning.

**Output:** `work/voice-production.md` bound to current Voice Requirements.

**Exit:** `voice_script_ready` only with the existing semantic/craft readiness checks; no generated-audio or implemented-game PASS is implied.

## Voice Delivery

**Input:** current accepted PRD Handoff and Voice Requirements/Production.

**Work:** validate exact Voice/source bindings, communication/identity parity and the consolidated project HTML.

**Output:** `work/voice-acceptance.md`, `state/voice-state.yaml` and derived delivery.

**Exit:** `voice_delivery_ready` where supported. Audio quality requires separate heard evidence; it is not proof of map implementation or release.

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

Production design may stop after accepted PRD Handoff. Voice is conditional;
Map Development and live gameplay/device QA happen outside PRD-Creator.
For a later design revision, revisit only the affected authoritative owner
and invalidated downstream work.

Do not invent numbered flow aliases, parallel schemas, extra workflow
states, new agent systems or speculative test-map requirements. Say exactly
what is proven: mechanical document checks, semantic design review, visual
presentation evidence, or separately observed runtime QA.
