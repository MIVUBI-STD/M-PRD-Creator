---
id: document.knowledge.boot-baseline
class: DOCUMENT
domain: knowledge
role: GUIDE
authority: CANONICAL
lifecycle: ACTIVE
---

# Boot and Routing Baseline

Updated: 2026-09-09

This baseline protects context recovery without turning boot into repository-wide reading. It is a small routing regression contract, not another workflow engine or telemetry system.

## Canonical production names

```text
Project Requirements
→ PRD Production
   └─ Production Assets when required
→ PRD Handoff
→ Voice Requirements
→ Voice Production
→ Voice Delivery
```

## Scenario A — new chat, observe/recover only

```text
AGENTS.md
→ GITHUB_RULES.md when GitHub work is material
→ CONTEXT.md
→ next-action.md
→ smallest owner needed
→ report understanding
→ STOP / NO EDIT
```

Pass when the agent can state current repository purpose, active boundary/next step, relevant constraints, and likely owner without starting implementation or asking the user to reconstruct recoverable history.

## Scenario B — non-trivial repository Development

```text
AGENTS.md
→ GITHUB_RULES.md
→ CONTEXT.md
→ next-action.md
→ development-brief
→ smallest relevant owner/source
→ implementation after grounding
```

## Scenario C — bounded mechanical Maintenance

```text
AGENTS.md
→ GITHUB_RULES.md when material GitHub work is involved
→ exact defect/owner
→ targeted proof
→ STOP
```

`CONTEXT.md` / `next-action.md` may be skipped only when they cannot materially change the decision.

## Scenario D — normal project Production Execution

```text
AGENTS.md
→ current project state/evidence
→ matching production specialist when needed
→ smallest canonical workflow owner
```

Normal production does not invoke `development-brief` merely because files are created or revised.

## Routing regression examples

| Example request | Expected route | Must not |
|---|---|---|
| `Amati repo ini dan jelaskan statusnya.` | Plan / observe only | edit files, start implementation, run broad CI |
| `Update Objective 3 using this approved project change.` | bounded Production Execution → affected canonical owner | re-audit all source or replay unrelated objectives |
| `Create Voice Production from the accepted PRD.` | PRD Handoff → Voice Requirements → Voice Production | treat as repository Development |
| `Fix this renderer class; canonical content is already correct.` | Maintenance → exact renderer implementation owner | reopen project semantics without evidence |
| `Change how incomplete project sources are recovered before PRD creation.` | Development → `development-brief` → Project Requirements owner | treat as a one-project content revision |
| `Change GitHub transfer/retry behavior.` | Development → `development-brief` + `GITHUB_RULES.md` owner | modify project production contracts |

## Pass Conditions

A route passes when:

- the user is not asked to repeat recoverable context;
- observe/recover requests remain read-only unless implementation is also requested;
- non-trivial Development recovers stable context + active continuation first;
- bounded work does not broad-read unrelated repository/history;
- the correct semantic/technical owner is reached without redundant skills;
- canonical workflow names are used consistently;
- backlog/reviews/old TODOs do not become active work automatically;
- evidence expectations match the execution channel;
- production revisions touch only invalidated scope unless expansion is proven;
- no ceremonial routing telemetry/session log/extra state system is created.