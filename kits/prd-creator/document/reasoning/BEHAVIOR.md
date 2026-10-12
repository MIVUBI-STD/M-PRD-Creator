# Behavioral Working Model

Supporting method for [Project Requirements](../../intake/SOURCE-INTAKE.md) and
[PRD Production](../CONTENT-CONTRACT.md). This is a **temporary semantic model**,
not a new canonical source, disk schema, skill, approval state, or workflow stage.

## Entry and authority

Use a bounded reasoning pass when interactions, lifecycle, outcomes, ownership,
or source conflicts create a material design question. For simple, already
settled requirements, skip this pass rather than generating a model for ceremony.

Inputs: current user instruction, approved decisions, current authoritative
sources, and the smallest relevant `SRC-...` / `REQ-...` records. Supporting
material can clarify but not overrule those inputs. Never import gameplay facts
from Golden examples, other projects, generated HTML, or observed defects.

## In-memory representation

| Construct | Question | Example |
|---|---|---|
| Claim | Which behavior is asserted? | Disconnect resets the current run |
| Relation | What depends on what? | Completion precedes result delivery |
| Constraint | What must remain true? | A valid result is stored at most once |
| Open concern | What is consequential but unsettled? | Disconnect during finalization |

For each material claim record only known dimensions: subject/actor, scope
(player / team / arena / session / global), event, condition/guard, action or
effect, resulting state, exception, quantities, and source/requirement evidence.
Do not fill absent dimensions with plausible defaults. Split distinct effects
into distinct claims; preserve negation, ownership, units and temporal order.

Not all behaviors are state transitions. Resource transfers, spatial rules,
continuous values and intended experience may require different relations.

### Evidence classification — reasoning only

| Label | Allowed interpretation |
|---|---|
| `EXPLICIT` | Current authority states this |
| `EXPLICIT_NO` | Current authority explicitly excludes it |
| `DERIVED` | Necessary consequence of cited supported premises; explain chain |
| `HYPOTHESIS` | Possibility worth considering; never a project fact |
| `UNKNOWN` | Unstated or insufficiently grounded |
| `CONFLICTED` | Incompatible claims under matching scope/condition and authority |

These are **not** persisted `approval_status` or `recovery_class` values.
A written `evidence_locator` and a `PRD-TRACE` marker identify candidate
locations; neither proves that the source text agrees with the claim.

## Operating procedure

1. Recover the minimum authoritative source and approved requirement context.
2. Decompose independently actionable events, conditions, effects, exclusions,
   quantitative constraints and ownership. Keep source linkage.
3. Distinguish explicit rules from deductions, hypotheses and unknowns.
4. Compare apparently contradictory claims on identical actor/scope, event,
   condition, lifecycle and applicable source authority. Different triggers
   can produce different outcomes without contradiction.
5. Identify important missing outcomes or dependencies only when motivated by
   the actual mechanisms. Do not build a hypothetical world for its own sake.
6. Activate just the relevant [domain concerns](CAPABILITIES.md), then group
   overlapping issues around their **root decision**.
7. Route material findings to the existing Project Requirements
   Completion / Proposal / Blocked procedure. Otherwise continue authoring.

### Compact finding

Report: `kind` (CONTRADICTION | MISSING_DECISION |
UNSUPPORTED_ASSUMPTION | DESIGN_RISK), relevant `REQ`/`SRC` references,
scope/event, observed facts, explicitly hypothetical consequences and the
smallest useful correction or decision. A plausible conflict is only
**potential**, never a proven contradiction. A design risk is advisory
unless an approved goal or constraint is demonstrably violated.

Optional `work/review.md` may present material findings to humans, but must
not become another machine registry. Summarize 1–3 grouped decisions when
possible; more genuine blockers may be grouped but must not disappear.

## Worked contrast

Authoritative: "On disconnect during an active session, reset run progress
but retain the player's arena assignment."

- Claim A: disconnect + active session → reset run progress (`EXPLICIT`).
- Claim B: disconnect + active session → retain arena assignment (`EXPLICIT`).
- A separate "Exit Match → clear arena assignment" is not in conflict:
  the trigger differs.
- "Disconnect → clear assignment" under the same scope/condition would
  conflict with B, if both are current authoritative rules.
- "What if disconnect overlaps score finalization?" is a scenario question
  (`UNKNOWN`), not proof of a defect or authorization to invent a policy.

"No score" does NOT mean "score zero". Observed behavior does NOT become
approved design unless the source authority explicitly establishes it.

## Stop / proof boundary

Stop when material meaning is settled and further questions are speculative.
"No material findings" is valid. Do not claim a played simulation, formal
model check, semantic PASS, or validated runtime from these instructions.
