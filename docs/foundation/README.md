---
id: document.foundation.router
class: DOCUMENT
domain: foundation
role: ROUTER
authority: CANONICAL
lifecycle: ACTIVE
---

# Production Foundation

This folder owns durable workflow/product policy. Active repository work state is routed separately; durable product policy belongs here.

## Current notes

Numeric filename prefixes are **ordering only**. Current workflow names are semantic and are used consistently in policy, routing, handoff, and operator communication.

| File | Canonical boundary |
|---|---|
| [00-product-boundaries.md](./00-product-boundaries.md) | Product Boundaries |
| [01-production-flow.md](./01-production-flow.md) | Canonical Workflow |
| [02-source-intake-recovery.md](./02-source-intake-recovery.md) | Project Requirements |
| [03-prd-generation.md](./03-prd-generation.md) | PRD Production |
| [04-prd-validation-handoff.md](./04-prd-validation-handoff.md) | PRD Handoff |
| [05-voice-requirement-extraction.md](./05-voice-requirement-extraction.md) | Voice Requirements |
| [06-elevenlabs-script-production.md](./06-elevenlabs-script-production.md) | Voice Production |
| [07-voice-validation-delivery.md](./07-voice-validation-delivery.md) | Voice Delivery |

Production Assets is a bounded capability used when the project requires concrete resources. Numeric section markers may appear in the generated PRD as visual ordering only; they are not capability names.

Do not use numbered stage aliases as active workflow terminology.

## Rule

Read only the note relevant to the active boundary. Do not use foundation files as running task logs.