---
id: document.foundation.voice-delivery
class: DOCUMENT
domain: foundation
role: CONTRACT
authority: CANONICAL
lifecycle: ACTIVE
---

# Voice Delivery

Status: active policy

Voice Delivery validates the exact current Voice chain and decides whether the requested scope is ready. The default human-facing delivery remains the same versioned project HTML used by the PRD.

## Inputs

```text
current PRD Handoff
+ Voice Requirements
+ Voice Production
+ current consolidated project HTML
→ Voice Delivery
```

## Mechanical validation

Voice validation must prove:

- PRD Handoff is still current;
- accepted PRD revision + exact render-data SHA still match;
- Voice Requirements use valid Owner ID + Moment ID topology;
- Voice Production binds exact current Voice Requirements bytes;
- Owner ID / Type / Speaker parity is intact;
- consolidated HTML binds exact current Voice sources;
- each Voice ID renders under the correct Owner + Moment;
- Prompt bytes match canonical performance text;
- final Voice acceptance binds exact current Voice Production bytes.

Mechanical PASS does not prove naturalness, actor continuity, expression, pronunciation, visual quality, or generated-audio quality.

## Semantic / craft readiness

`Voice Script Readiness` is the single semantic/craft result. It covers:

```text
Communication Conservation
+ Naturalness
+ Expression Conservation
+ Character Continuity Conservation when applicable
+ Pronunciation Conservation
+ timing / continuity / operator readiness
→ Voice Script Readiness
```

Do not add separate persisted acceptance fields merely to mirror Voice Production reasoning.

## Project HTML

Voice is presented inside **Production Assets** using the same stable Owner ID + Moment ID identity as other resources. The visible document may show a numeric section ordinal, but the capability name remains Production Assets.

Verify exact Prompt copy, correct Voice ID placement, no reasoning-field leakage, and readable presentation when visual readiness is claimed.

## Acceptance

`work/voice-acceptance.md` remains compact:

```text
# Voice Acceptance
Status: needs_revision | voice_delivery_ready
Mechanical: PASS | FAIL
Voice Script Readiness: PASS | FAIL
Communication Conservation: PASS | FAIL
Project HTML Visual: PASS | FAIL | NOT PROVEN
Audio Evidence: not_provided | partial_review | reviewed_passed | reviewed_with_findings
Findings: <only when findings exist>
Critical: N
Major: N
Accepted Voice Production SHA256: <exact current work/voice-production.md SHA-256>
```

## First wrong owner

```text
stale/wrong project fact or PRD acceptance → Project Requirements / PRD Production / PRD Handoff
Voice scope / communication intent → Voice Requirements
wording / actor fit / expression / pronunciation / duration / cast → Voice Production
one weak generated take → candidate variance review before canonical rewrite
correct canonical Voice + stale/wrong presentation → renderer/compositor
generated-audio-only issue → generation evidence/settings/voice/surface/context
```

## Delivery gate

`voice_delivery_ready` requires current PRD Handoff, lifecycle Mechanical PASS, Communication Conservation PASS, Voice Script Readiness PASS, current consolidated HTML, cast selection/profile for every represented speaker, exact accepted Voice Production SHA, visual PASS when claimed, Critical = 0, Major = 0, and truthful optional audio evidence.

It does not imply client sign-off, implementation completion, generated-audio approval, pronunciation approval, or release.