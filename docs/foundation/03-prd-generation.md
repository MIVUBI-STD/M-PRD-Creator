---
id: document.foundation.prd-production
class: DOCUMENT
domain: foundation
role: CONTRACT
authority: CANONICAL
lifecycle: ACTIVE
---

# PRD Production

Status: active policy

PRD Production turns one exact ready Project Requirements revision into canonical PRD meaning, strict render projection, and deterministic PRD output without inventing new project decisions.

## Entry

```text
Project Requirements = ready_for_prd
+ approved_requirement_sha256 is current
→ PRD Production
```

## Canonical outputs

```text
work/content.md
work/render-data.json
```

`content.md` owns readable PRD meaning. `render-data.json` is one strict machine projection bound to exact current content bytes.

## Design-to-specification responsibility

This flow **writes the design for a map that may not exist yet**. The
approved model is made actionable in existing PRD surfaces:

| PRD surface | Responsibility |
|---|---|
| Overview | Experience, audience, relevant constraints and scope |
| Gameplay Flow | End-to-end player journey and gameplay loop |
| Gameplay | Objectives, actions, conditions and visible results |
| Level Design | Space, routes, affordances and build requirements |
| Developer | Event guards, state ownership, result/reset/recovery behavior |

Follow the [semantic content contract](../../kits/prd-creator/document/CONTENT-CONTRACT.md).
Each material system should be coherent across its owning roles, with the
same approved actor, trigger, scope, outcome and relevant exception.
Details may be written and grouped; gameplay policy may not be fabricated
to fill a field. Actual blocks/scripts/runtime test results are not required.

## Authoring rule

Preserve approved meaning, including material conditions, values, exceptions, result/scoring behavior, reset/retry/interruption, build/spatial constraints, technical constraints, and role ownership.

Do not:

- copy another project's facts from the Golden/reference;
- add filler to match sample counts;
- merge distinct rules merely for compactness;
- invent missing decisions;
- use renderer fallbacks to repair incomplete meaning.

## Production Assets boundary

Production Assets are a separate bounded capability derived from the same approved project model. PRD Production may identify when concrete resources are required, but `production-assets/CONTRACT.md` owns their canonical resource requirements.

Generated PRD pages are not a second brainstorming source for Production Assets.

## Projection

```text
approved Project Requirements SHA
+ content.md SHA
→ strict render-data vocabulary
→ deterministic renderer
```

The renderer represents already-resolved meaning only.

## Completion

PRD Production is complete when:

- the Project Requirements revision is still current;
- `content.md` satisfies `document/CONTENT-CONTRACT.md`;
- `render-data.json` exactly binds current content and requirement bytes;
- no material decision was silently introduced;
- semantic cardinality is conserved;
- deterministic rendering succeeds;
- no unresolved placeholder remains.

Then continue to **PRD Handoff**. If project meaning is incomplete, return the affected slice to **Project Requirements**.
