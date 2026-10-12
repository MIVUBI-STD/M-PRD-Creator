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


### Bounded causal propagation

Do **not** simply compare requirement sentences. For a material interaction,
trace the smallest supported chain:

```text
authoritative event/condition
→ effect on one owned state/resource
→ necessary dependent behavior
→ observable outcome or unresolved boundary
```

For each arrow, distinguish a **source-supported dependency** from a merely
plausible effect. An unsupported link is a `HYPOTHESIS`; it must never become
a `DERIVED` fact because the proposed outcome seems typical of games.

1. **Anchor:** Start from one current `REQ`/`SRC` fact and its actor,
   event, guard, state/resource owner, and explicit effect.
2. **Trace:** Follow only directly affected claims or relations. An outcome
   is dependent only when current authority supplies the link or the outcome
   logically follows from an unambiguous condition.
3. **Bound:** Normally inspect the immediate effect and one downstream
   consumer. Follow further only when cited evidence establishes a concrete
   additional dependency. This two-link budget is a review heuristic, not a
   correctness guarantee or a persistent graph-depth setting.
4. **Stop at uncertainty:** If a dependency, trigger, order, or owner is
   unknown, record the precise missing decision; do not choose a default.
5. **Cross-role:** Compare the same consequence across Gameplay, Level
   Design, Developer, and applicable Production Assets, without requiring
   each role to repeat identical sentences.
6. **Consequences:** Identify what could change for the player or production.
   Distinguish guaranteed violations from hypothetical failure modes.
7. **Merge:** Consolidate all related observations under their first
   unresolved root decision before presenting a review.

Material impact is high when a confirmed inconsistency can invalidate an
approved goal, make a primary route impossible, lose or duplicate accepted
results/resources, violate ownership/isolation, or make implementation
indeterminate. A speculative usability concern stays advisory unless it
contradicts an approved player-experience goal. Do not assign arbitrary
percentage confidence or risk scores.

### Conflict adjudication and temporal uncertainty

A contradiction requires **both rules to apply simultaneously** to the
same subject/resource, lifecycle window, event/guard, and comparable current
authority, with effects that cannot coexist. A difference in wording,
implementation detail, event, owner, or stage is not itself a contradiction.

| Situation | Appropriate finding |
|---|---|
| Same event/guard/owner; one rule retains assignment, another clears it | Candidate contradiction; confirm both sources are current |
| Disconnect retains assignment; explicit Exit Match clears it | No contradiction: different events |
| A newer approved instruction supersedes an older behavior | Use the current authority; do not invent a live conflict |
| Source says "no objective score"; downstream writes score=0 | Unsupported changed meaning, not a harmless synonym |
| Two events may overlap, but finalization order is unspecified | Missing decision **only if** the order affects a material outcome |
| One rule is an observed implementation detail, not an approved decision | Treat as evidence to inspect, not authoritative gameplay |

For event ordering distinguish: explicitly **before**, explicitly **after**,
permitted to overlap, mutually exclusive by an approved guard, and unknown.
Do not infer atomicity, cancellation, retries, shared ownership, or storage
consistency merely because an implementation might usually supply them.
Two events being conceivable does not prove a race condition.

### Reviewer-facing materiality gate

Before surfacing an open concern ask:

1. Does it come from a real activated mechanism and current evidence?
2. Is its missing outcome necessary to interpret or implement an approved
   requirement, or does it materially change player-visible behavior?
3. Has an approved rule, valid exclusion, or higher-authority decision
   already settled it?
4. Is this one root decision already represented by another finding?

Only if the answers justify action, route the concern to existing Project
Requirements. Ordinary tuning ideas and preference disagreements are optional
design critique. If no consequential gap remains, say **no material finding**
and proceed; never manufacture an approval request to make analysis appear
comprehensive.

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


### Three bounded contrast cases

**Scored multiplayer, result finalization.** Sources say a disconnect resets
run progress and that valid completed runs record one result. Without a
decision about overlapping disconnect/completion, the storage outcome is
`UNKNOWN`. If those events can affect the same result, ask **one** material
question about when a result becomes final; do not report duplicate scores as
an observed bug or automatically choose "result wins".

**Puzzle key and exit.** A source-backed key unlocks the exit. A hypothetical
"the player might lose the key" is not enough to assert a softlock unless
the source also permits loss of the only key or rules out recovery. Otherwise
the proposed failure is a `HYPOTHESIS` and should not force a decision.
If an approved mechanic explicitly consumes the only key *before* it can
unlock the exit, compare the exact sequence and recovery rules.

**Currency versus inventory reset.** The project says coins persist across
rounds and inventory items reset at round end. These rules can coexist when
currency and inventory are different resources. Do not manufacture an economy
conflict from the word "reset"; request ownership clarification only if
the actual source maps coins to the same reset-owned inventory.

A small [manual semantic calibration set](../../../../tests/semantic-review-cases.md)
illustrates source precedence, unresolved event ordering, and a no-finding
control. For a blind manual calibration, provide only the case inputs,
record the review, and open the separate reference key afterward. Exposing the
key in advance contaminates the result. These synthetic answers are not
executable test results or evidence of empirical model accuracy.

## Stop / proof boundary

Stop when material meaning is settled and further questions are speculative.
"No material findings" is valid. Do not claim a played simulation, formal
model check, semantic PASS, or validated runtime from these instructions.

Reference methods, not runtime dependencies:
[Stately state/events/guards](https://stately.ai/docs/editor-states-and-transitions),
[Cucumber Gherkin scenarios](https://cucumber.io/docs/gherkin/reference/), and
[GraphWalker model-based paths](https://graphwalker.github.io/graphwalker-rs/model-based-testing).
These approaches inform reasoning; no statechart interpreter, path generator
or automated gameplay test is introduced here.
