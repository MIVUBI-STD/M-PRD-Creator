---
id: document.knowledge.decisions.adaptive-semantic-composition
class: DOCUMENT
domain: knowledge
role: CONTRACT
authority: CANONICAL
lifecycle: ACTIVE
---

# Adaptive Semantic Composition

Date: 2026-09-07
Status: current

## Context

The Golden Reference solved real historical regressions: generated PRDs had become thinner, generic, and structurally inconsistent even while appearing superficially similar to the approved reference. Exact Golden artifact retention and stable page/component grammar remain valuable safeguards.

A stronger production model introduces a different failure mode if the same reference is treated as a universal semantic mold: project meaning can be padded or compressed merely to match AFTERSHOCK's sample counts such as four flow cards, four note cards, or five compact gameplay steps.

Those counts describe the reference project. They are not inherently project semantics.

## Decision

Separate PRD semantic completeness from Golden presentation grammar:

```text
kits/prd-creator/document/CONTENT-CONTRACT.md
→ what project meaning must be communicated

kits/prd-creator/document/DESIGN-CONTRACT.md
→ where/how accepted meaning is presented
```

The exact approved Golden HTML remains retained byte-for-byte and continues to define the stable design system, page family, navigation, component vocabulary, and explicitly meaningful fixed slots.

Inside approved repeatable component families, child cardinality is now **data-driven**:

- Global Development Flow and Important Development Notes;
- Gameplay Overview compact Gameplay Flow;
- Level Design Flow and Important Build Notes;
- Developer Flow and Important Development Notes;
- Gameplay Flow narrative sections;
- requirement rows/groups, journey cards, and glossary items.

No filler may be invented to reach a reference count. Distinct material rules may not be merged merely to reduce to a reference count.

## What remains fixed

This decision does not loosen:

- source authority / Proposal approval;
- material conservation;
- page family and `6 + 4N` core page topology;
- stable Overview semantic facts;
- Gameplay Context / Main Objective / Result roles;
- six Gameplay Information meanings;
- stable requirement table meanings;
- Terms Used placement;
- page IDs/navigation/Golden DOM vocabulary;
- exact Golden/runtime template bytes;
- deterministic rendering and mechanical validation;
- browser evidence requirement for visual PASS.

## Proof model

`tests/test_prd_golden_reference.py` continues to prove the exact retained Golden artifact and therefore may assert AFTERSHOCK's exact counts.

Adaptive production is proven separately by `tests/test_prd_adaptive_composition.py`, which requires non-sample child counts to render and validate through the same approved component grammar.

## Refines

This decision refines `golden-reference-fidelity.md` only where that decision could be read as making reference-project child counts universal. It preserves that decision's exact Golden artifact retention, stable design vocabulary, and material-conservation rationale.

## Boundary

Adaptive composition means **variable children inside approved surfaces**, not arbitrary generated layouts. A genuinely new component/page family remains a design change and requires evidence/approval appropriate to that boundary.
