---
name: project-document-production
description: Semantic/product-contract specialist for Project Requirements, PRD Production, Production Assets, and PRD Handoff. Use when source recovery, project-model completion, canonical PRD meaning, resource requirement meaning, or PRD readiness/handoff semantics are the actual problem. Presentation-only Golden questions route to the design owner.
---

# Project Document Production

Own semantic judgment for the Project/PRD domain. Detailed procedure, visual mechanics, and executable routing stay with the nearest package owner.

## Authority

```text
originals + current user instruction + approved decisions
→ Project Requirements
→ PRD Production
   └─ Production Assets when required
→ PRD Handoff
```

Generated output never becomes project authority. Golden/reference material supplies representation/quality evidence, not another project's facts.

## Detailed owners

```text
Project Requirements
→ kits/prd-creator/intake/SOURCE-INTAKE.md

PRD Production semantics
→ kits/prd-creator/document/CONTENT-CONTRACT.md

Golden page/component grammar
→ kits/prd-creator/document/DESIGN-CONTRACT.md

Production Assets
→ kits/prd-creator/production-assets/CONTRACT.md

ElevenLabs non-dialogue Sound Effects craft
→ kits/prd-creator/production-assets/SOUND-EFFECTS.md

PRD Handoff
→ kits/prd-creator/document/VALIDATION.md

end-to-end execution
→ kits/prd-creator/SKILL.md
```

## Judgment rules

### Project Requirements

```text
current authority settles it → recover and continue
one necessary evidence-backed result exists → Completion and continue
multiple plausible material answers exist → one concrete Proposal → user review
no responsible proposal can be formed → Blocked / direct decision
```

Material AI Proposals require approval. Authoritative facts and evidence-backed Completions do not require redundant approval.

### PRD Production

Preserve current Project Requirements meaning without inventing product decisions or deleting independently actionable rules. Semantic cardinality follows meaning; do not add filler or compress distinct rules to imitate a reference.

### Production Assets / PRD Handoff

- Production Assets come from the same approved project model as the PRD; generated pages are not a second brainstorming source.
- Non-dialogue `AUDIO` stays in Production Assets; Voice stays in its own domain.
- Mechanical PASS does not prove semantic completeness or visual/audio quality.
- PRD Handoff reconciles current Project Requirements → canonical content → projection → visible PRD + Production Assets.

## Routing boundary

```text
project/resource meaning wrong → this specialist + nearest semantic owner
approved non-dialogue AUDIO meaning correct; SFX craft weak → production-assets/SOUND-EFFECTS.md
meaning correct; approved visual grammar wrong → document/DESIGN-CONTRACT.md
semantic + design contracts correct; executable behavior wrong → kits/prd-creator/AGENTS.md
```

## Requirement traceability

When required to prove completeness, inspect `tools/prd.py trace` output and the exact current Project Requirements register. An explicit REQ marker only establishes a content location. Compare source evidence with PRD meaning and cross-role Gameplay/Level Design/Developer outcomes before a human semantic readiness decision. Do not report semantic PASS because a marker or matching phrase exists.

## Proof economy

Start with the smallest current semantic owner/source, expand only for a dependency that can change the result, do not reconfirm already-authoritative facts, and stop when the requested semantic boundary is correct and sufficiently proven.

## Boundary

This skill owns Project Requirements / PRD Production / Production Assets / PRD Handoff semantic judgment only. Voice remains downstream.