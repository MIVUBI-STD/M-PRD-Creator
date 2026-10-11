---
id: document.knowledge.decisions.recording-policy
class: DOCUMENT
domain: knowledge
role: CONTRACT
authority: CANONICAL
lifecycle: ACTIVE
---

# Decision Recording Policy

Updated: 2026-08-10

Use this guide to decide **where a change decision belongs** and when ordinary bounded work should escalate into a durable cross-owner change contract.

## Source-Of-Truth Routing

- current active task/status → `docs/knowledge/next-action.md`;
- durable decision/reason → `docs/knowledge/decisions/README.md` or a dedicated note in `decisions/`;
- stable production policy → `docs/foundation/`;
- current implementation ownership → `docs/knowledge/ownership.md`;
- evidence/findings → `reviews/` or a focused operations proof note;
- future/non-active work → `operations/backlog.md`;
- project-specific state → the active `workspace/active/<project>/` owner.

Do not create a second planning/state hierarchy.

## When To Record A Durable Decision

Record a decision when at least one is true:

- the choice changes architecture/workflow across sessions;
- several owners depend on the same reason;
- a tradeoff/constraint must survive chat history;
- an old method is explicitly superseded/retired;
- future agents need the **why**, not only the resulting diff.

Do not create a decision entry for every wording fix, local bug fix, regenerated artifact, or obvious implementation detail.

## Decision Shape

Use this minimum shape:

```text
Context
Decision
Why
Tradeoffs / not chosen
Evidence / validation boundary
Follow-up owner
```

A short entry in `README.md` is preferred. Create a dedicated decision note only when the reasoning is too substantial or cross-linked to stay readable in the log.

## Cross-Owner Change Threshold

Ordinary bounded work does **not** need a formal change plan.

Escalate to a durable coordinated change note only when one of these is true:

- Project Document and Voice semantic owners must change as one coordinated contract;
- a migration/compatibility promise spans multiple phases or project packages;
- several developers/sessions need one shared architectural contract;
- changing one owner invalidates multiple downstream authority/state contracts;
- existing `next-action` + decision register cannot represent the tradeoff clearly.

A coordinated change note should define:

```text
Goal
Owners affected
Current contract
New contract
Migration / invalidation behavior
Out of scope
Acceptance criteria
Proof boundary
Roll-forward / rollback or retirement rule if relevant
```

## Do Not Escalate For

- one Flow rule correction;
- one renderer/builder defect;
- one documentation cleanup;
- one skill wording correction;
- speculative future support;
- a task that stays within one semantic owner.

## Change Rules

- solve the verified problem with the smallest complete change;
- reuse current owners before adding files/skills/abstractions;
- do not add fallback/compatibility layers without evidence;
- samples/references remain evidence, not generic contracts;
- unavailable runtime/browser/audio proof remains an evidence limitation rather than a reason to invent more process.

## Review Interaction

A review records evidence/reasoning. A decision records the chosen durable rule. Do not leave a durable product/architecture choice only inside review prose.

```text
review finding
→ decision (if a durable choice is required)
→ implementation owner
→ current status in next-action
```

## Related

- [Decision Register](README.md)
- [Review Register](../reviews/README.md)
- [Repository Ownership](../ownership.md)
