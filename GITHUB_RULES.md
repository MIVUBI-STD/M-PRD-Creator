# GitHub Rules

Canonical GitHub execution rules for AI/ChatGPT working in PRD-Creator. Repository/domain owners may narrow these rules but may not weaken integrity, proof, history, or STOP boundaries.

Use the seven core rules in order. Read only the conditional surface relevant to the current task.

```text
PIN
→ READ MINIMUM
→ DIAGNOSE
→ TOOL + TRANSFER GATE
→ WRITE ONCE
→ VERIFY + FAILURE POLICY
→ STOP
```

## 1. PIN — establish exact authority

Before a material GitHub action, know:

```text
repository
exact branch/ref
current HEAD when relevant
requested scope
target writability
```

- Direct branch/file fetch is current-state authority; search is discovery.
- Never silently fall back to the default branch.
- Every write targets the intended branch/ref explicitly when supported.
- Repository-designated stable/protected/release branches are read-only unless policy or explicit user intent authorizes the action.
- Re-check HEAD before a write only when concurrent movement could overwrite newer work.
- Existing-file replacement/deletion uses the current blob/content SHA for that exact branch.
- Keep commit SHA, tree SHA, blob SHA, ref/tag, run ID, and content SHA distinct.

## 2. READ MINIMUM — inspect only what can change the decision

Default:

```text
owner files   1–3
history       0
broad scans   0
```

- Prefer exact fetch when path/ref is known.
- Open history, reviews, generated output, or adjacent owners only for a concrete unresolved question.
- Truncated/paginated/partial results are incomplete evidence, not proof of absence.
- Verify an apparently missing target once against the exact repository/ref/access before concluding it is absent.
- Do not reread current state merely for reassurance after a mutation response already returns usable new state.

## 3. DIAGNOSE — fix the first wrong owner

```text
requirement / meaning wrong             → semantic owner
requirement correct, implementation wrong → implementation owner
implementation correct, test stale        → test
implementation/test correct, CI wrong      → workflow / repository policy
derived artifact wrong                    → upstream canonical owner
```

- Maintenance stays bounded to the observed defect.
- Do not add unrelated cleanup, compatibility work, dependency upgrades, abstractions, or documentation churn unless required for the result.
- CI failure is evidence to diagnose, not permission to weaken the gate.
- Historical failures are inactive unless the current system still reproduces them.
- `No change required` is valid.

## 4. TOOL + TRANSFER GATE — use a capability that fits the final state

Choose the simplest method that safely produces the requested repository state.

```text
current branch/file state
→ direct GitHub fetch

one bounded UTF-8 file + one logical change
→ Contents update/create

coherent multi-file change / atomicity needed / large or binary payload / real Git semantics
→ atomic Git workspace or Git data tree+commit capability

final artifact cannot be transferred safely by available capability
→ Manual Handoff

CI diagnosis
→ run → failing job/step → relevant log

browser/audio/runtime claim
→ matching real capability
```

### Transfer gate

Before the first write, establish:

```text
final content/artifact ready?
exact repo/ref/path known?
replacement/current SHA understood?
complete logical file set known?
chosen method can carry the real payload?
chosen method preserves acceptable history?
```

If any answer is no, do not start partial repository mutation.

### Hard prohibitions

Do not create architecture solely to bypass a connector/tool limitation. Never use:

- placeholder content at the final destination;
- transfer-only loaders/bootstrap files/fragments/manifests;
- base64 stand-ins for ordinary binary assets;
- temporary workflows/branches solely as transport;
- alternate repository structures solely for transfer;
- low-level blob/tree/ref chains merely to carry a payload that the active capability otherwise cannot support.

Also:

- never full-replace from partial file context;
- `update_file` replaces the complete file; it is not append/patch;
- do not mix incompatible transfer strategies to force one logical package through;
- force-push/history rewrite/destructive reset is never a workaround for stale state, CI failure, connector limits, or commit cleanup;
- do not use Actions as a remote shell substitute for missing local/browser/audio capability.

### Manual Handoff

Manual Handoff is valid when direct repository transfer is unsafe, unavailable, unreliable, or would damage history.

Finish and validate the exact artifact, deliver it directly to the user, and state:

```text
repository:
branch/ref:
repo root:
destination:
action: upload | replace | merge | extract
expected result:
repo state: unchanged | partially changed (exact paths)
```

Never claim repository presence until upload actually occurs.

## 5. WRITE ONCE — one coherent logical delivery

Prepare the complete intended logical state before the first mutation.

- Same-file/overlapping mutations are serial.
- One intentional write per file is the default, but one file write does not imply one commit.
- Coordinated multi-file work should use an atomic method when commit atomicity matters.
- Do not partially synchronize a baseline that must remain coherent.
- Preserve lockfiles/runtime constraints/action references unless they are the actual owner being changed.
- New files, workflows, abstractions, branches, PRs, issues, comments, releases, and other persistent side effects default to zero unless the requested result genuinely needs them.

### Commit discipline

A commit is a categorized logical delivery, not a save/checkpoint/tool call/CI trigger.

```text
prepare complete logical change
→ cheapest relevant pre-commit proof
→ review intended diff/state
→ one logical commit
→ push once
→ targeted evidence; manual CI only when explicitly requested or needed for approved promotion
→ STOP
```

Message format:

```text
<type>(<optional-scope>): <concise logical outcome>
```

Use `feat`, `fix`, `docs`, `refactor`, `test`, `ci`, `build`, `release`, or bounded `chore` according to the primary outcome.

For **material repository Development** commits, append concise, truthful continuity fields to the conventional subject:

```text
Work: <stable topic and canonical responsibility>
State: ACTIVE | BLOCKED | PAUSED | DONE
Decision: <rationale, only when material>
Proof: <exact source/test/CI evidence and NOT EXECUTED limits>
Unresolved: <specific unresolved question, if any>
Next: <one bounded next action, when not DONE>
```

`Work`, `State`, and `Proof` are required for material work. `DONE` closes the specific committed unit, not the entire upgrade. Git commit history is the continuity record: do not create heartbeat commits, mirrored progress registries, or duplicate next-action logs. On resume, match by **topic plus changed owner**, not merely the newest commit.

Split commits only for independent outcomes that can be reviewed/reverted/landed independently. Do not split by file, directory, tool call, work order, or transfer limitation.

Do not rewrite published/shared history merely to make it prettier. A fast-forward ref update from the pinned current HEAD is valid when the repository workflow permits it.

## 6. VERIFY + FAILURE POLICY — prove only what changed

### Minimum proof

- Run the cheapest check that can falsify the changed claim.
- Targeted proof is the default during iteration.
- Full suites belong at integration/promotion boundaries or when the changed public/executable contract can materially affect them.
- A completed successful run is PASS. Queued, running, pending, cancelled, skipped, neutral, or superseded states are not PASS.
- Inspect only the failing job/step and relevant error before editing.
- Do not weaken/delete/bypass a valid test or workflow merely to obtain green status.
- Static checks prove only the static/mechanical contracts they execute; they do not prove browser visuals, audio quality, deployment success, or another unexecuted capability.
- Remote GitHub source review can complete source-verifiable work without a user-PC checkout. Label its ceiling `SOURCE_REVIEWED`; it is not an executed test. Existing exact-HEAD CI results may provide stronger evidence.
- When browser, runtime, audio or local artifact execution is genuinely unavailable, finish independent source-valid scope and mark that **specific** result `NOT EXECUTED`; never invent a PASS or require an unrequested local-PC workaround.
- During an unfinished multi-owner architecture BUILD, inspect affected source/consumers first; defer routine fixture/test proliferation to one meaningful integration boundary. Exceptions: security, irreversible mutation, data-loss, or compatibility hazards require early checks.

### Failure policy

Retry ceilings are maximums, never quotas:

| Failure | Action |
|---|---|
| known capability mismatch | STOP method; 0 retries; choose fitting capability/handoff |
| permission/safety denial | STOP; 0 retries unless condition changes |
| capability genuinely uncertain | at most 1 bounded probe |
| malformed valid request / 422 | correct once if method still fits |
| missing/inaccessible / 404 | verify exact repo/ref/target once |
| stale/conflict / 409 | refetch relevant state once; retry from it |
| rate limit / 429 | honor server reset/retry guidance |
| 5xx/timeout/unknown mutation | inspect target state before any retry |
| same-cause operational failure with new evidence | maximum 2 attempts for that valid method |

Do not reinterpret a known capability mismatch as request-debugging work.

### Interrupted delivery

If current-task writes already occurred before a later block, perform at most one bounded recovery pass:

1. stop new transfer experiments;
2. identify exact current-task paths/commits;
3. separate legitimate changes from accidental transfer artifacts;
4. safely correct only accidental current-task state when possible;
5. preserve legitimate changes unless an all-or-nothing baseline would be misleading;
6. if cleanup cannot be completed cleanly, disclose exact remaining state and stop;
7. build any handoff against that actual state.

Never force-push published/shared history to hide an interrupted delivery.

## 7. STOP — completion is terminal

Stop when one of these is true:

```text
requested outcome + sufficient proof satisfied
→ STOP

confirmed capability mismatch + safe fallback delivered
→ STOP

Manual Handoff delivered with placement contract
→ STOP

authoritative permission/safety/policy boundary blocks action
→ report boundary → STOP
```

Do not automatically continue into unrelated cleanup, backlog, promotion, release, new issue/PR, more testing, or adjacent audits merely because more work is possible.

# Conditional GitHub surfaces

Read/apply only the section touched by the task.

## Branch and promotion

PRD-Creator branch roles are defined by root `AGENTS.md`/`CONTEXT.md`:

```text
develop → active Development
Local   → verified integration baseline
main    → stable history
```

- Routine work targets `develop` unless current authority says otherwise.
- `develop → Local` requires the repository Local promotion gate and squash merge.
- After promotion, synchronize `develop` to resulting `Local` HEAD before new Development.
- `Local → main` requires explicit stable promotion and the Stable release gate.
- A main stable merge marker is not synchronized back into lower branches.
- Do not bypass a failed gate by direct edits to another branch.

## Pull requests

Use a PR only when repository policy requires it or review/integration is the actual task. Before creating one, ensure the logical change already exists on the intended source branch and the base/head pair matches repository policy. Do not create a PR solely to make work look formal.

## CI and logs

On the updated branch, all five Actions workflows must run only via `workflow_dispatch`. Never trigger on push, PR, schedule or workflow completion. When promotion is approved, manually select the matching source branch and provide the open PR number; the gate checks exact source/target, PR head and GitHub test-merge SHA. Re-run the manual gate after either PR side changes. A source review is not an Actions PASS. Other branch versions and GitHub required-check settings remain independent until separately updated.

Use current commit/run state. Diagnose:

```text
relevant workflow run
→ failing job
→ failing step
→ smallest relevant log
→ first wrong owner
```

Do not inspect every job/log when one failing step already identifies the cause. Re-run only when the failure policy permits and new evidence can change the result.

## Tags and releases

Tags/releases are publishing actions, separate from branch promotion. Create them only when explicitly authorized and the repository's feature/capability release policy is satisfied. Maintenance/governance-only stable changes remain untagged unless current policy says otherwise.

## Repository artifacts and generated output

Canonical source must remain upstream of generated output. Never directly patch versioned project output to hide a source/renderer defect. Generated/binary-heavy deliverables must pass the transfer gate before any repository write.

## Evidence reporting

Final repository reports should distinguish:

```text
implemented
repository/static verified
integration verified
browser/runtime verified
audio verified
not verified
```

Claim only the strongest level actually proven.