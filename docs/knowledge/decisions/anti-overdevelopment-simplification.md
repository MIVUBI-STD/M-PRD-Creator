---
id: document.knowledge.decisions.anti-overdevelopment
class: DOCUMENT
domain: knowledge
role: CONTRACT
authority: CANONICAL
lifecycle: ACTIVE
---

# Anti-Overdevelopment Simplification Decision

Date: 2026-08-10  
Status: current  
Clarified: 2026-09-07

## Context

The BuildIT-parity remediation began adding revision fingerprints/checksums and deeper derived-artifact integrity machinery to PRD and Voice production. The user identified that this was making the repository harder to use and was no longer aligned with the repository's anti-overdevelopment rules.

Later production regressions demonstrated one narrower failure class that is worth protecting mechanically: canonical or intermediate source bytes may change inside the same semantic project version while an already-generated dependent artifact remains stale.

## Decision

Prefer the simplest production chain that protects **demonstrated failures** without creating a second revision-management system.

```text
canonical source
→ derived artifact
→ narrow freshness/parity validation
→ semantic / visual / audio review only where required
```

A single deterministic source-binding may be used when it directly detects a real stale-derived-artifact failure. That binding is mechanical metadata, not another project version, approval state, operator workflow, registry, or semantic authority.

### Keep

- PRD structural validation and exact generated page-set checks;
- narrow current canonical-content → render-data freshness binding;
- narrow current render-data → generated PRD HTML freshness binding;
- narrow non-Voice Production Asset source → consolidated HTML freshness binding when that source exists;
- narrow current Voice Requirements → canonical Voice Production source binding because same-version requirement edits can otherwise leave an older script mechanically plausible;
- Voice ID/Type/Speaker and current revision parity;
- PRD script-safe glossary serialization and required shell-marker checks;
- focused CI that exercises actual renderer/validator paths;
- controlled failure for concrete malformed input;
- regressions for failure classes that have actually occurred or are directly exercised by the current deterministic chain.

These bindings are machine-owned. Operators should not maintain checksum tables or use hashes as project/release identifiers.

### Do not expand into

- a generic derived-artifact revision registry;
- operator-facing checksum tables or manual SHA bookkeeping;
- a second revision/fingerprint identity alongside `document.version`;
- checksums for every canonical or derived file merely for symmetry;
- script/output identifiers whose only purpose is proving that another checksum exists;
- dependency graphs, snapshot systems, similarity scores, or integrity frameworks without a demonstrated failure they uniquely solve;
- additional hardening phases merely because an audit lists theoretical possibilities.

A new freshness binding requires a concrete stale-state failure that cannot be protected more simply by an existing owner/state/version check.

## Empty Voice sections

A zero-entry `##` Voice section is invalid canonical Flow 6 input. The validator may reject it with a clear controlled error. No general Markdown parser framework is needed.

## Proof rule

Use the cheapest check that can falsify the changed boundary. Once the current production flow has enough evidence, stop.

A passing CI gate does not justify adding more machinery. `No change required` remains a valid and preferred result when the remaining risk is theoretical or cheaper to handle procedurally.
