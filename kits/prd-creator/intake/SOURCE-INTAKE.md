# Project Requirements

Project Requirements converts project evidence into one production-ready requirement state before PRD Production writes the canonical PRD. It owns source authority, material requirement recovery, unresolved material choices, cross-role coherence, and the approval boundary only when a real Proposal requires it.

## Canonical state

```text
state/source-inventory.yaml
state/requirement-register.yaml
state/intake-state.yaml
```

`work/review.md` is optional human-readable support. Machine contracts live in `shared/intake.py`.

## Source inventory

Give every material source/instruction stable provenance. Supported source roles remain:

```text
authoritative | supporting | reference | generated
```

Current repository-retained sources use safe project-relative paths and matching SHA-256 bytes. Do not ask users to maintain source IDs, hashes, YAML, or workspace mechanics.

## Requirement register

Create explicit requirement entries only for material rules that benefit from traceability: high-impact constraints, exclusions, quantitative invariants, lifecycle/topology rules, conflict resolutions, or AI Completion/Proposal decisions.

Do not turn ordinary descriptive detail or every source sentence into separate records.

## Recovery rule

Recover explicit facts, removals, exclusions, topology, terminology, quantitative rules, lifecycle behavior, and necessary Production Assets implications first.

```text
existing authority settles it → recover
one necessary evidence-backed result exists → Completion
multiple plausible material answers exist → one concrete Proposal
no responsible proposal is possible → Blocked / direct user decision
```

Material Proposals require user approval. Authoritative facts and evidence-backed Completions do not.

## Optional evidence pointers

The existing requirement-register fields `evidence_locator` and `evidence_status` may preserve a source-specific pointer or unresolved/conflicting evidence note without inventing a new source. Source IDs and current authoritative status remain mechanically checked by `shared/intake.py`. A locator written by AI is a claim to inspect, not proof that the referenced passage exists or agrees with the requirement.

Requirement location in PRD production is separate from source provenance; see `../document/CONTENT-CONTRACT.md`. Do not turn an AI-generated evidence pointer or a REQ marker into an approval flag.

### Source-to-requirement evidence review

When an evidence locator or source fidelity changes a material decision,
inspect the **actual passage** before judging the requirement or PRD wording.
The existing read-only `tools/prd.py trace` report exposes each cited
source's declared role, current/superseded status, inspection scope,
retention, and project-relative path when available. These are navigation
cues, not verified quotations or semantic agreement. A retained source's
SHA-256 proves byte identity only; an external or missing source passage
cannot be silently filled in by AI.

Compare the source passage with the requirement's actor, event/guard, scope,
negation, quantities, exceptions and outcome, then compare the material
claim with its actual representation in `work/content.md`. If the passage
cannot be inspected, mark the claim unresolved in the existing review
workflow rather than calling it confirmed. Resolve a material discrepancy
at its first authoritative owner; reuse Completion / Proposal / Blocked
instead of adding a semantic approval status or a separate evidence registry.

## Integrated completeness

Before PRD Production, reason once across the complete applicable model:

```text
player journey
→ Gameplay
→ Level Design
→ Developer lifecycle/state/data
→ Production Assets implications
→ success/fail/interruption/retry/reset/result/handoff
```

Routine wording, grouping, ordering, and decomposition remain downstream craft.

## Conditional behavioral understanding

For material gameplay interactions or unresolved causal consequences, use
[Behavioral Working Model](../document/reasoning/BEHAVIOR.md) to distinguish
evidence-backed events/effects from hypotheses. Apply only
[source-activated domains](../document/reasoning/CAPABILITIES.md), not a
generic checklist for every genre. Inspect actor/scope, ownership, lifecycle
and outcome without guessing unstated policy.

This pass is in-memory and uses existing `SRC`/`REQ` identities. Merge
duplicate root concerns, keep design criticism advisory, and route only
material missing decisions through existing Completion / Proposal / Blocked.
If nothing material is missing, continue without extra approvals or files.

## Conditional review

When no material Proposal or unresolved conflict exists:

```text
recover requirements
→ bind exact requirement revision
→ status: ready_for_prd
→ PRD Production
```

When a material Proposal exists, show one compact user-facing review, then bind the exact accepted requirement revision.

## Revision binding

```text
requirement-register.yaml bytes
→ approved_requirement_sha256
```

If requirement bytes change after readiness, the old binding becomes stale. Reconcile only affected meaning before PRD Production continues.

## Readiness

`ready_for_prd` requires:

- current material sources are sufficiently inspected;
- retained source bytes still match recorded hashes;
- requirement provenance is valid;
- normal requirements have authoritative grounding;
- material Proposals are approved;
- no active blocked/pending requirement remains;
- topology, lifecycle, quantities, terminology, and role ownership are coherent;
- `approved_requirement_sha256` matches exact current requirement-register bytes.

PRD Production consumes this exact revision and must not invent new project meaning to repair incomplete Project Requirements.
