---
name: prd-creator
description: End-to-end Production Execution router for Project Requirements → PRD Production → Production Assets → PRD Handoff → optional Voice Requirements → Voice Production → Voice Delivery.
version: 3.1.3
---

# PRD Creator

Use for normal project Production Execution and bounded production revisions. Changes to PRD-Creator itself route to repository Development.

## Canonical workflow

```text
Project Requirements
→ PRD Production
   └─ Production Assets when required
→ PRD Handoff
→ Voice Requirements when Voice is justified
→ Voice Production
→ Voice Delivery
```

`Project Setup` is repository/session preparation and sits before this production sequence when needed.

Numbered stage aliases are retired from current workflow language. Generated PRD numbers are document ordinals only; **Production Assets** is the capability name.

## Route first

```text
new / materially uncertain project meaning → Project Requirements
bounded approved revision → first changed canonical owner → only invalidated downstream owners
meaning complete, presentation grammar wrong → document/DESIGN-CONTRACT.md
contracts correct, executable behavior wrong → package AGENTS.md → exact technical owner
```

Start from the smallest owner that can settle the issue. Expand context only for a real dependency or contradiction.

## Canonical sequence

```text
source / instruction
→ Project Requirements
→ material Proposal/conflict?
   yes → compact review → approval/correction
   no  → continue
→ exact requirement-revision binding
→ PRD Production: content.md + strict render-data projection
→ Production Assets when concrete resources are required
→ PRD Handoff: exact-byte acceptance + handoff_ready
→ Voice Requirements when justified
→ Voice Production
→ Voice Delivery
```

Production Assets is not a separate numbered stage. Non-dialogue `AUDIO` can use `production-assets/SOUND-EFFECTS.md`. Voice begins only from `handoff_ready`.

## Owners

| Boundary | Owner |
|---|---|
| Project Requirements | `intake/SOURCE-INTAKE.md` + `shared/intake.py` |
| PRD semantic meaning | `document/CONTENT-CONTRACT.md` |
| Golden visual/component grammar | `document/DESIGN-CONTRACT.md` |
| Production Assets meaning | `production-assets/CONTRACT.md` + `shared/assets.py` |
| non-dialogue SFX craft/generation | `production-assets/SOUND-EFFECTS.md` |
| PRD Handoff | `document/VALIDATION.md` |
| rendering/delivery | `renderer/CONTRACT.md` |
| Voice Requirements | `voice/EXTRACTION.md` |
| Voice Production | `voice/PERFORMANCE-WRITING.md` |
| Voice Delivery | `voice/VALIDATION.md` |
| file/mechanical routing | `AGENTS.md` |

## Non-negotiable invariants

### Authority decreases downstream

```text
user instruction / approved decisions / authoritative source
→ Project Requirements
→ canonical PRD / Production Assets / Voice sources
→ derived render/context/index/HTML/evidence
```

### Approval is exception-driven

Project Requirements always bind exact current requirement bytes to `approved_requirement_sha256`. User review is required only for a material AI Proposal/conflict.

### Projection is strict

```text
content.md bytes
→ canonical_content_sha256
→ one supported render-data vocabulary
→ deterministic renderer
```

### Stable Production Assets identity

```text
Owner ID → Moment ID → Asset ID | Voice ID
```

Display titles never perform machine joins.

### Acceptance stays exact

PRD Handoff binds current Render Data and optional Asset Requirements. Voice Delivery binds current Voice Production.

### Handoff stays minimal

```yaml
status: handoff_ready
accepted_prd_version: X.Y.Z
```

### Conditional behavioral intelligence

When project meaning includes material interacting gameplay mechanisms
or source-backed constraints for facilitator-operated sessions, use the
existing [semantic specialist](../../.agents/skills/project-document-production/SKILL.md)
with [Behavioral Working Model](document/reasoning/BEHAVIOR.md) and only
applicable [domain guidance](document/reasoning/CAPABILITIES.md).
This is internal Project Requirements / PRD semantic reasoning, not another
workflow, persisted project model, automatic approval, or mechanical PASS.

### Trace is evidence routing, not semantic scoring

REQ markers in `work/content.md` identify where approved requirements are represented, with the canonical grammar owned by `document/CONTENT-CONTRACT.md`. An explicit partial or malformed trace blocks mechanical validation; an unannotated legacy project remains compatible. The trace CLI exposes per-package cross-role review surfaces but never certifies semantic equality.

### Proof stays truthful

Mechanical checks prove mechanical contracts. Semantic review proves meaning. Visual PASS requires browser/render evidence. Audio quality requires actual audio evidence.

## First wrong owner

```text
project fact / requirement                  → Project Requirements
canonical PRD meaning                       → PRD Production
meaning correct, page grammar wrong         → DESIGN-CONTRACT
Production Assets meaning/identity          → Production Assets
PRD acceptance/freshness                    → PRD Handoff
Voice scope/intent                          → Voice Requirements
Voice wording/performance/surface strategy  → Voice Production
Voice acceptance/evidence                   → Voice Delivery
canonical sources correct, render wrong     → renderer/compositor
mechanical parity wrong                     → validator/shared owner
```

## Operator facade

```bash
python tools/prd.py impact <changed-path> ... --json
python tools/prd.py trace workspace/active/<project>/
python tools/prd.py revision workspace/active/<project>/ --before /path/to/previous-requirements.yaml
python tools/prd.py status workspace/active/<project>/ --json
python tools/prd.py build workspace/active/<project>/
python tools/prd.py validate workspace/active/<project>/
python tools/prd.py browser workspace/active/<project>/
python tools/prd.py handoff workspace/active/<project>/
python tools/prd.py voice workspace/active/<project>/
```

## Artifact lifecycle

```text
Project Requirements
  state/source-inventory.yaml
  state/requirement-register.yaml
  state/intake-state.yaml
  work/review.md                 # optional

PRD Production
  work/content.md
  work/render-data.json

Production Assets
  work/asset-requirements.md     # when required

PRD Handoff
  work/acceptance.md
  state/handoff-state.yaml

Voice Requirements / Production / Delivery
  work/voice-requirements.md
  work/voice-production.md
  work/voice-acceptance.md
  state/voice-state.yaml

Derived
  output/README.md
  output/v<version>/prd.html
  output/v<version>/context.md
  output/v<version>/index.json
```

Do not create duplicate schemas, registries, dashboards, approval layers, speculative modes, compatibility frameworks, or alternate workflow naming systems. Stop when requested scope is complete and evidence supports the claim.
