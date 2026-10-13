# Voice Delivery

Voice Delivery validates the exact current Voice chain and decides whether the requested scope is ready. The default human-facing delivery remains the same versioned project HTML used by the PRD.

## Canonical owners

- Voice Requirements fields / Owner ID / Moment ID → `EXTRACTION.md` + `work/voice-requirements.md`;
- Voice Production wording/performance/duration/selection → `PERFORMANCE-WRITING.md` + `work/voice-production.md`;
- Production Assets presentation → `../production-assets/CONTRACT.md`;
- lifecycle/domain mechanical validation → `../validator/voice_validation.py`;
- validation CLI/public entrypoint → `../validator/validate_voice.py`;
- final Voice acceptance → `work/voice-acceptance.md`.

## Mechanical validation

Run:

```bash
python kits/prd-creator/validator/validate_voice.py workspace/active/<project>/
```

Every validatable Voice state first reruns PRD Handoff validation. Voice cannot remain current when upstream acceptance/delivery is stale.

Voice source identity is exact:

```text
source_prd_revision
+ source_prd_sha256
```

Lifecycle behavior:

```text
voice_requirements_ready
→ validate current PRD Handoff + exact PRD bytes + Voice Requirements topology

voice_script_ready | voice_validation | needs_revision
→ also validate Voice Production binding + Owner/Type/Speaker parity + HTML freshness when provided

voice_delivery_ready
→ additionally require current HTML, cast selection/profile for every speaker, and exact Voice Acceptance SHA
```

Mechanical validation proves:

- PRD Handoff still passes;
- accepted PRD version + exact Render Data SHA remain current;
- Voice state uses the strict schema and safe project-relative paths;
- Voice Requirements use valid Owner ID + Moment ID topology;
- Voice Production binds exact current Voice Requirements bytes;
- Owner ID / Type / Speaker parity is intact;
- HTML binds exact current Voice requirements + production bytes;
- each Voice ID renders on the correct Production Assets page inside its stable Moment;
- Prompt bytes match canonical performance text;
- final Voice acceptance binds exact current production bytes;
- at `voice_delivery_ready`, `context.md` matches current Voice Requirements and upstream PRD content, and `index.json` matches the context navigation.

Mechanical PASS does not prove semantic, naturalness, actor-continuity, expression, pronunciation, visual, or generated-audio quality.

## Semantic / craft readiness

Voice Delivery consumes the Voice Production craft result; it does not create another schema for it.

### Communication Conservation

PASS only when required communication remains present, exclusions are respected, project meaning is intact, source timing truth remains honored, and production polish introduced/deleted no material meaning.

### Voice Script Readiness

`Voice Script Readiness` is the single persisted semantic/craft decision. Internally it covers:

```text
Communication Conservation
+ Naturalness
+ Expression Conservation
+ Character Continuity Conservation when applicable
+ Pronunciation Conservation
+ timing / continuity / operator readiness
→ Voice Script Readiness
```

Review communication, listener fit, naturalness, actor continuity, expression, pronunciation/language, performance, timing, continuity, and operator usability once. Do not persist per-lens scorecards.

Preparation may establish text/craft readiness. Actual pronunciation approval and generated-audio quality require heard evidence.

## Project HTML review

Voice appears inside **Production Assets**. The generated document may display a numeric section ordinal for navigation; that number is presentation order only and is not another name for the capability.

When visual readiness is claimed, verify:

- accepted PRD navigation/page identity remains unchanged;
- Voice is under the page resolved from Owner ID;
- Moment ID resolves to the correct reader-facing moment;
- rendered resource maps to the correct Voice ID;
- copied Prompt remains exact;
- Voice Requirements/reasoning fields do not leak;
- no clipping/overlap prevents reading Production Assets AUDIO presentation.

```text
Project HTML Visual: PASS | FAIL | NOT PROVEN
```

## Acceptance record

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

Expression/character/pronunciation readiness remains inside the one Voice Script Readiness result rather than expanding the machine acceptance format.

## First wrong owner

```text
project/gameplay/story fact → Project Requirements / PRD Production
stale PRD acceptance → PRD Handoff
Voice scope / Owner / Moment / Speaker / Channel / Trigger / Purpose / communication / source timing → Voice Requirements
wording / actor fit / expression / pronunciation / Estimated Duration / cast → Voice Production
one weak generated take → candidate variance review before canonical rewrite
correct canonical Voice + stale/wrong Production Assets presentation → renderer/compositor
generated-audio-only issue → generation evidence/settings/voice/surface/context
```

## Delivery gate

Default non-audio `voice_delivery_ready` requires:

- current PRD Handoff Mechanical PASS;
- exact Voice source PRD revision + Render Data SHA match;
- lifecycle Mechanical PASS;
- Communication Conservation PASS;
- Voice Script Readiness PASS;
- current consolidated project HTML;
- cast selection/profile for every represented speaker;
- exact accepted Voice Production SHA;
- Project HTML Visual PASS when visual readiness is claimed;
- Critical = 0 and Major = 0;
- truthful optional audio evidence.

It does not imply client sign-off, implementation completion, generated-audio approval, pronunciation approval, or release.