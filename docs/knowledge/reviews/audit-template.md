---
id: document.knowledge.reviews.audit-template
class: DOCUMENT
domain: knowledge
role: GUIDE
authority: REFERENCE
lifecycle: ACTIVE
---

# Review Template

Use only when a dedicated review adds durable evidence beyond a normal task diff.

```text
# <Review Title>

Captured: YYYY-MM-DD
Scope:
Current owner/source:

## Question / Failure

## Evidence Observed

## Findings

## What Could Disprove This

## Recommendation / Decision Boundary

## Implementation Status At Capture

## Follow-up Owner
```

Rules:

- separate observation from recommendation;
- do not promote reference/sample behavior into generic policy without evidence;
- do not rewrite the body after later implementation; update `review-graph.md` instead;
- current task status belongs in `next-action.md`, not in the review body.
