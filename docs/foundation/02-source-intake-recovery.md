---
id: document.foundation.source-intake
class: DOCUMENT
domain: foundation
role: CONTRACT
authority: CANONICAL
lifecycle: ACTIVE
---

# Project Requirements

Status: active policy

Project Requirements converts project evidence into one production-ready requirement state before PRD Production writes the canonical PRD.

## Authority

```text
current user instruction
+ approved decisions
+ authoritative/supporting/reference sources
→ source inventory
→ material requirement recovery
→ integrated project model
```

It owns source authority, provenance, material requirement recovery, unresolved material choices, cross-role coherence, and the approval boundary only when a real Proposal requires it.

## Canonical state

```text
state/source-inventory.yaml
state/requirement-register.yaml
state/intake-state.yaml
```

`work/review.md` is optional human-readable support. Machine parsing belongs to `kits/prd-creator/shared/intake.py`.

## Resolution ladder

```text
existing authority settles it → recover
one necessary evidence-backed result exists → Completion
multiple plausible material answers exist → one concrete Proposal
no responsible proposal is possible → Blocked / direct user decision
```

Material Proposals require approval. Authoritative facts and evidence-backed Completions continue without redundant review.

## Integrated completeness

Before PRD Production, reason across all material implementation concerns:

```text
player journey
→ Gameplay
→ Level Design
→ Developer lifecycle/state/data
→ Production Assets implications
→ success/fail/interruption/retry/reset/result/handoff
```

Routine wording/grouping/order remains downstream craft.

## Readiness

`ready_for_prd` requires current material sources to be sufficiently inspected, requirement provenance to remain valid, material Proposals to be approved, no active Blocked/Pending item to remain, and `approved_requirement_sha256` to match exact current `state/requirement-register.yaml` bytes.

```text
Project Requirements ready
→ PRD Production
```

Do not ask users to maintain SRC/REQ IDs, YAML, hashes, or machine status vocabulary.

## Change rule

If requirement bytes change after readiness, the old revision binding is stale. Reconcile only affected meaning, then continue to PRD Production. Do not let downstream prose silently repair an upstream requirement defect.