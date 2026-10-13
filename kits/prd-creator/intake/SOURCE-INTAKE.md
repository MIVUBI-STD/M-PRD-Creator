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

## Pre-build Game Design from a brief

A current user brief is enough to begin designing a new map; an existing
`.mcworld`, implemented gameplay or a testable arena is not required.
Recover explicit design goals, audience, experience, constraints and
exclusions. Identify material undecided gameplay choices and generate
one grounded option or a concise tradeoff between viable alternatives.
A new AI-proposed mechanic, result, timing, capacity or recovery rule
is a **Proposal** when the brief does not determine it, not source
recovery or evidence-backed Completion.

Group repeated consequences under their root decision; do not demand
approval for cosmetic drafting, trivial decomposition, or already
authoritative rules. Once material design choices are accepted, keep
the approved project model in the existing requirement register and
let PRD Production express it in Gameplay, Level Design and Developer.
No separate concept document, design decision register or workflow
status is necessary.

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

An exact `evidence_status` marker of `conflict`, `conflicted`, `unresolved`, or `blocked`
is an explicit **open concern**. An ordinary source/Completion requirement
cannot reach `ready_for_prd` while that marker remains. Even a declared
approved Proposal does not override `blocked` or `unresolved` evidence.

For `conflict` or `conflicted` only, an already approved material Proposal
retains its existing declared-approval route and warning that user consent has
not been independently authenticated. Inspect the real decision before
clearing the concern. This guard is **not** an automatic semantic conflict
detector. Other free-form notes remain review hints rather than new machine
states. Do not rewrite a marker solely to obtain PASS.

Requirement location in PRD production is separate from source provenance; see `../document/CONTENT-CONTRACT.md`. Do not turn an AI-generated evidence pointer or a REQ marker into an approval flag.

For current, repository-retained UTF-8 text, an optional exact locator
such as `source-note.md#L2-L4` lets `tools/prd.py trace` display that
passage directly with its line numbers. The path must match the registered
source path; a preview is limited to eight lines and 2,400 characters.
External, superseded, inaccessible, ambiguous, or out-of-range pointers
receive no generated quote. A displayed excerpt confirms only the text at
those lines, **not** that it supports the requirement or that the PRD agrees.
Keep using the existing `evidence_locator` field; do not create a new status.

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

## Source-grounded operating context before map design

When an approved project source describes an operated session (for example a
facilitated class, club, or workshop), recover the **operating conditions**
before treating a gameplay description as implementable. Inspect only the
material source-backed dimensions:

- intended participants, skill mix, facilitator presence/permissions,
  usable session time, supported devices and essential input methods;
- simultaneous player/group capacity, admission after start, team assignment,
  independent sessions, reconnect location versus run progress;
- ready/start conditions, cancellation and override authority;
- recovery from a stuck group, scope of any restart/return command, and the
  journey for early finishers or departing players;
- in-world guidance, safe routes, device constraints and observable end state.

Keep source facts, observed session problems, suggested solutions, and
unresolved project decisions distinct. A source checklist is evidence of
**desired design**, not evidence that an implementation already works.
Do not turn an example count, timeout, team composition or control scheme
into a default for another map. An absolute requirement such as admitting
every late arrival still needs an approved policy for actual capacity limits;
a fragmentary sentence cannot become a complete requirement by AI inference.
Request only consequential missing decisions through the existing
Completion / Proposal / Blocked process.

Classroom-specific project instructions are authoritative only for the
project that adopts them. Keep client originals and production facts in the
approved private project workspace, not this public system repository.
For cross-role concerns, use the existing [facilitated-session reasoning](
../document/reasoning/CAPABILITIES.md) selectively; do not create another
project schema, operator role section, or universal classroom checklist.

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

## Approval evidence boundary

The existing `approval_status: approved` and `preview_approved: true`
are **declared project state**, not an authenticated record of a user
action. Their presence and matching SHA-256 values prove only that the
persisted fields and requirement revision agree. The mechanical validator
emits a non-blocking warning when a material Proposal uses these declarations;
it does not impersonate an approval provider or change legacy state formats.

Before moving a consequential AI-designed rule into PRD Production,
compare the proposal with the user's actual approval in the active
conversation or another legitimate source of approved decisions. If
that approval cannot be established, keep the decision open using the
existing Proposal / pending or Blocked process. Never fill the approval
fields merely to make a validator green; do not treat AI-authored notes
as independent user consent.

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
