---
id: document.knowledge.maintenance
class: DOCUMENT
domain: knowledge
role: WORKFLOW
authority: CANONICAL
lifecycle: ACTIVE
---

# Maintenance Workflow

Updated: 2026-08-30

Use Maintenance for bugs, regressions, review/cleanup, stale documentation, broken routing, and behavior-preserving refactors.

```text
User reports bug/review/cleanup
→ boot repository memory
→ identify affected semantic owner
→ observe/reproduce or inspect concrete drift
→ cause/scope grounded?
   ├─ no → UNKNOWN / LOCAL PROOF REQUIRED / Perlu pemeriksaan
   └─ yes
      → smallest safe correction
      → targeted regression/proof
      → scope/diff review
      → update only the canonical owner whose state changed
```

## Categories

- **Bug** — observe/reproduce, diagnose cause, correct the smallest owner, add only useful regression proof.
- **Artifact defect** — determine whether cause is canonical content, projection/script, renderer/compositor, validator, template, or evidence before editing.
- **Small refactor** — preserve behavior; prefer deletion/simplification over new abstraction.
- **Cross-owner refactor** — pause and define a durable change contract only when multiple semantic owners must change together.
- **Documentation cleanup** — edit the current owner, remove stale/duplicate routing, verify affected links.
- **Historical review cleanup** — preserve review bodies as capture-time evidence; update the current meaning/routing in [`reviews/README.md`](../reviews/README.md) only when needed.

## Owner Routing

```text
source / requirement / PRD / project HTML / PRD validator defect
→ project-document-production owner

Voice requirement / canonical Voice production / Voice validator defect
→ voice-production owner

repository routing / ownership / review / decision-memory defect
→ root AGENTS + relevant docs/knowledge owner
```

Use a root specialist only when its procedure adds value. Maintenance does not automatically invoke `development-brief`.

## Root-Cause Rule

Before editing establish:

1. what is actually wrong;
2. where the first incorrect owner/state appears;
3. why the proposed fix addresses that cause;
4. what evidence can prove the defect no longer exists.

Do not patch a derived artifact when its canonical owner is wrong.

Examples:

```text
wrong project fact in output/v<document.version>/prd.html
→ inspect canonical content/projection first
→ do not hand-edit generated prd.html

Voice wording is wrong but the 04 AUDIO presentation matches it exactly
→ inspect voice-requirements.md / voice-production.md
→ do not change the compositor to hide a semantic defect

acceptance record says PASS but canonical content is wrong
→ fix/reopen the canonical owner
→ do not edit evidence to hide the defect
```

## Validation Economy

Run only proof invalidated by the change.

- docs/routing → exact path/link/owner check;
- canonical content → affected requirement/semantic acceptance;
- renderer/compositor → targeted structural render check; browser claims need browser evidence;
- Voice production → exact requirement/production parity + semantic check;
- project HTML presentation → regenerate from canonical sources + targeted validation/browser proof when visual behavior changed;
- audio behavior → actual audio evidence.

Do not rerun full unrelated production flows for a local maintenance fix.

## Scope Rules

- diagnose before patching;
- do not turn cleanup into feature work;
- do not add fallback/compatibility layers unless the cause proves they are needed;
- do not create new skills/modules because the current owner is inconvenient;
- stop repeating the same failed direction after two attempts without new evidence;
- `No change required` is valid when inspection disproves the reported defect.

## Maintenance Checklist

- [ ] affected owner identified;
- [ ] concrete drift/defect observed or evidence limitation stated;
- [ ] root cause grounded before edit;
- [ ] change stayed inside scope;
- [ ] derived artifacts regenerated instead of patched where applicable;
- [ ] smallest informative validation performed;
- [ ] no material claim exceeds actual proof;
- [ ] review/decision/next-action owner updated only if its state changed.

## Retirement Rule

A note/tool/path can be retired when its useful behavior has moved to the canonical owner or is no longer part of the current product contract. Preserve historical evidence when it explains why a decision exists; do not preserve live duplicate architecture solely for archaeology.

## Related

- [Work Routing](../work-routing.md)
- [Repository Ownership](../ownership.md)
- [Review Register](../reviews/README.md)
- [Decision Recording Policy](../decisions/recording-policy.md)
