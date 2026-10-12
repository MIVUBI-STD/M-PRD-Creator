---
id: document.foundation.prd-handoff
class: DOCUMENT
domain: foundation
role: CONTRACT
authority: CANONICAL
lifecycle: ACTIVE
---

# PRD Handoff

Status: active policy

PRD Handoff validates and accepts one exact current PRD revision for implementation and optional downstream Voice work.

## Inputs

```text
current Project Requirements revision
+ work/content.md
+ work/render-data.json
+ Production Assets source when present
+ current deterministic project delivery
```

## Acceptance of a pre-build design

Evaluate the **specification**, not a non-existent implemented map.
A valid schema, current hashes and render success prove mechanical
document integrity only. Semantic readiness depends on source-to-design
fidelity, complete material decisions, actionable Gameplay / Level Design /
Developer responsibilities and non-contradictory results.

Design acceptance does **not** imply working Minecraft gameplay, tested
server capacity, stable performance or successful classroom sessions.
Those claims require later observations of an actual implementation.
Return any consequential unapproved design policy to Project Requirements.

## Validation

PRD Handoff combines:

- canonical mechanical validation;
- integrated semantic reconciliation;
- Material Conservation;
- visual evidence when visual readiness is claimed;
- exact-byte acceptance.

Mechanical PASS does not prove semantic fidelity or browser visual quality.

## Semantic reconciliation

Compare:

```text
Project Requirements
→ canonical PRD meaning
→ strict render projection
→ visible PRD + Production Assets
```

Look for material loss, contradiction, unsupported meaning, ambiguity, or cross-role drift.

## Acceptance

`work/acceptance.md` binds exact current bytes:

```text
Accepted Render Data SHA256: <sha256>
Accepted Asset Requirements SHA256: <sha256 | none>
```

`development_ready` means current PRD/Production Assets meaning is accepted for implementation.

`handoff_ready` additionally proves the accepted revision matches current versioned delivery and may enter **Voice Requirements**.

## Handoff state

```yaml
status: handoff_ready
accepted_prd_version: <X.Y.Z>
```

Artifact locations remain deterministic and are not duplicated into handoff state.

## Bounded revision

```text
approved change
→ first wrong owner
→ affected canonical source
→ deterministic rerender
→ mechanical validation
→ semantic/visual review only where invalidated
→ new exact-byte acceptance
→ stop
```

Do not replay unaffected Project Requirements, Golden review, or Voice work for ceremony.
