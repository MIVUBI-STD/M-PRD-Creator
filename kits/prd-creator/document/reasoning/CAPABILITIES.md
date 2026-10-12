# Context-Activated Domain Capabilities

Supporting method beneath [Behavioral Working Model](BEHAVIOR.md). This is a
selective reasoning menu, **not** a second root skill, plugin framework,
persisted registry, or `render-data.json` extension.

## Activation contract

Always start with the small core pass (evidence, scope/ownership, behavioral
consistency and observable outcome). Specialized reasoning requires BOTH:
(1) an actual mechanism grounded in current user instruction or approved
source, and (2) a distinctive material consequence that the core pass alone
cannot settle. A genre, sample map, estimated duration, borrowed design,
hypothetical concern or observed defect is not sufficient.

Current user instruction may establish a mechanism before a REQ ID exists;
preserve that instruction as evidence instead of inventing an ID. External
engine documentation teaches methods, never another project's game rules.

All capabilities consume the **same** in-memory claims/relations/constraints,
and return grounded findings through `BEHAVIOR.md`. A capability cannot mutate
Project Requirements, approve Proposals, assert semantic PASS, or author new
game facts. Skip irrelevant domains entirely; do not generate empty N/A cards.

| Capability | Evidence required to activate | Focus | Must not assume |
|---|---|---|---|
| Session/lifecycle | Reconnect, retry, interruption, cleanup, or persistent session state | retention, reset, finalization, ownership | ordinary start/end implies complex lifecycle |
| Multiplayer/concurrency | Interacting players, shared state, or overlapping sessions/arenas | isolation, authority, disconnect, simultaneous effects | PvP, teams or one specific server topology |
| Competition/result | Score, win/loss, rank, persisted result, or exactly-once completion flag | eligibility, ties, duplicates, final result | completion always implies scoring |
| Economy/resource | Repeated acquisition/spend, scarce consumables, exchange, or transfers | source/sink, ownership, limits, persistence | decorative coins or one-use puzzle keys create an economy |
| Time/progression | Runtime timer/deadline, round timing, or condition-dependent gates | start/stop, expiry, ordering, interruption | estimated playtime is a countdown |
| Puzzle/solvability | Actual logic puzzle, gates, clues, or dependency sequence | reachability, dead ends, feedback, recovery | every puzzle has a collectible key |
| Spatial/level design | Navigation, zone permission, spawn, or placement materially constrains behavior | route, access, boundary, zone ownership | every named location needs a spatial audit |
| Narrative/choice | Choices, story flags, or branches that condition later outcomes | branch guard, continuity, reachability | a linear cutscene has branching state |

## Domain lifecycle

For every activated domain:

1. **Trigger:** cite the project mechanism and current `SRC`/`REQ`
   evidence; do not infer a domain from a label alone.
2. **Minimum context:** ask only for details that materially change this
   domain's analysis. Missing facts remain `UNKNOWN`.
3. **Targeted scenarios:** normal, meaningful boundary, interruption, and
   concurrent paths only when real actors/events justify them.
4. **Findings:** use the four shared finding kinds in `BEHAVIOR.md`, not
   one custom verdict set per domain.
5. **Exclusion:** omit the domain when the evidence does not support it.
6. **Merge:** combine multiple-domain findings that depend on the same
   missing decision instead of presenting duplicate warnings.

Example: a timed scored arena match with reconnect enables Session,
Multiplayer, Competition and Time. "Disconnect during result finalization"
is reviewed **once** across those contexts. Economy is inactive unless
resources are truly acquired/spent. A single-player timed puzzle activates
Time and Puzzle, not Multiplayer.

Avoid Cartesian explosion: don't enumerate all combinations of all events.
Prioritize behavior with consequential results, irreversible resources,
concurrent ownership or a concrete failure mechanism.


## Domain contrast patterns — illustrative, not project facts

Each example is invented to teach a **decision boundary**, not to supply
a template game rule. Apply its questions only to a relevant project source.
`Activate` means inspect the actual evidence, not force an approval request.

### Session / lifecycle

- **Activate:** "Disconnect resets run progress while the player's arena
  assignment survives." Separate run progress from assignment ownership.
  If a concurrently finalizing result can affect either state, examine the
  approved finalization policy; unresolved consequential behavior may
  justify `MISSING_DECISION`.
- **Skip:** "A player enters and leaves an isolated scene." Normal start
  and finish without state retention, retry or interruption ambiguity are
  handled by the core pass.
- **Do not infer:** Saved checkpoints, resumed waves, expiry or automatic
  reconnect behavior merely because the source mentions a session.

### Multiplayer / concurrency

- **Activate:** "Two arenas operate simultaneously with independent
  scores." Trace which arena/session owns each score. Ask about a shared
  update only when current sources actually describe a shared resource
  or operation; do not claim a reproduced race.
- **Skip:** "Two people take turns playing a single-player challenge."
  Multiple visitors do not imply concurrent player state.
- **Do not infer:** PvP, teams, shared shops, server-authoritative code,
  or a network architecture not present in the approved source.

### Competition / results

- **Activate:** "Completing a challenge stores one completion flag,
  without an objective score." Preserve the completion-only result
  model and its stated interruption/deduplication policy. A Developer
  section adding ten points would invent meaning and need correction.
- **Skip:** "Reaching the next room unlocks another scene." This alone
  does not create a scored contest or persisted completion record.
- **Do not infer:** Score=0 from "no score", a leaderboard, ties,
  ranking, or telemetry that the project did not require.

### Economy / resources

- **Activate:** "Players earn tokens per objective and spend them on
  upgrades." Identify token sources, sinks and ownership. Consider an
  approved reset only if it affects the token balance. Missing earning
  or pricing values remain unknown; never synthesize an optimal cost.
- **Skip:** Decorative coin models or a one-use puzzle key do not
  establish a repeatable acquisition/expenditure economy.
- **Do not infer:** Trading, shops, persistent wallets, player-specific
  distribution or real-money payments from a named resource.

### Time / progression

- **Activate:** "A capture ends the round, and a countdown ending at
  zero also finishes it." Determine whether both conditions can apply
  to the same result and whether ordering matters. A possible overlap
  is not automatically a proven race.
- **Skip:** "Expected playtime is ten minutes." A duration estimate is
  not evidence of a runtime deadline.
- **Do not infer:** Pause, overtime, timer resets, scheduling
  guarantees or tick-atomic updates without supporting rules.

### Puzzle / solvability

- **Activate:** "Three switches open the only exit, and resetting a
  switch closes it." Trace required switch reachability and documented
  recovery under the given route constraints. Only source-supported
  absence of every recovery path can justify a definite softlock.
- **Skip:** "Find a hidden button" does not establish button loss,
  irreversibility or a missing route.
- **Do not infer:** Consumable keys, hints, a linear solution path
  or checkpoints not actually specified.

### Spatial / level design

- **Activate:** "Players may place blocks inside an assigned plot but
  not inside a protected lobby." Trace zone scope and documented route
  crossing. Ask about border rules only where they affect approved
  play or actionable implementation.
- **Skip:** "The lobby has a blue wall." Decorative description
  alone does not imply complex collision or permission policy.
- **Do not infer:** Minecraft-specific dimensions, blocks, physics,
  teleport commands or engine limitations from an engine-neutral PRD.

### Narrative / choice

- **Activate:** "Protecting the village sets a flag that selects the
  later ending." Link choice, flag and ending guard. A branch requiring
  an unreachable flag is a candidate design inconsistency if the
  approved choices and guards exclude every route to that state.
- **Skip:** Linear narration describing the village does not imply
  branching choice mechanics.
- **Do not infer:** Alternate endings, voiced dialogue, persistent
  reputation or extra characters.

### Cross-domain contrast — one decision, not many warnings

**Hypothetical source:** "Each arena stores its result exactly once;
disconnect resets unfinished progress but retains arena assignment."

Session + Multiplayer + Results share one material question **only when**
current evidence supports overlapping disconnect/result finalization
and that overlap can alter validity or ownership of the result.
An unspecified ordering is `UNKNOWN`, not an observed duplicate-score bug.
If an approved finalization rule already resolves ordering, report
**no material finding**.

**Wrong approach:** Invent a global scoreboard, mandate new retry logic,
assume server-side race conditions, and produce separate approvals for
every activated domain. One root decision is enough, or none if settled.

## Cross-domain consequence selection

When several capabilities are active, they do **not** run independent
free-form audits of the same rule. Use the [bounded causal walk](BEHAVIOR.md)
once and select the domains that own the affected transitions/resources.

| Shared consequence | Consult only when supported |
|---|---|
| Disconnect changes run progress and assignment | Session + Multiplayer if multiple actors/sessions exist |
| Completion records a score as timer expires | Competition + Time; add Session only if a session boundary matters |
| Resource is spent while a level resets | Economy + Session or Spatial only if those specific mechanics are described |
| Puzzle changes which routes are reachable | Puzzle + Spatial only if navigation constraints are explicit |

For each cross-domain review, preserve the **same cited requirement**, actor,
trigger and outcome. Merge repeated warnings at the earliest consequential
decision. A domain may add a distinct question but cannot redefine a source
fact to match its typical design pattern.

### Targeted scenario budget

Prefer one normal flow, then only the highest-impact grounded boundary,
interruption, or concurrency case. During a focused revision inspect only
scenarios touched by the changed requirement or documented dependency.
Do not enumerate possible permutations or seek 100% edge coverage without
a formal, user-approved executable model.

Prioritize: irreversible result/resource changes; mutually competing effects
on the same owner; possible dead ends in an approved journey; then observed
player-facing or production ambiguity. No material concern means no scenario
report. Synthetic examples illustrate a question, not a reproduced issue.

### Negative activation cases

Apply the **Skip** and **Do not infer** counterparts above. Do not turn
a genre label or a hypothetical performance concern into evidence of
multiplayer, economy, synchronization or an actual implementation bug.

## Scenario and design criticism

A scenario may be written as Given / When / Then, but an unknown expected
outcome must remain `UNKNOWN`, not a fabricated Then. Scenario review
does not claim that a bug was reproduced.

Critique the player experience only when an intended goal is grounded:
readability, feedback, agency, pacing, challenge, fairness or navigation.
Explain the causal tradeoff and provide alternatives. A subjective preference
is a `DESIGN_RISK` at most, not an automatic blocker or change of difficulty,
time, rewards, monetization or creative intent.

## Extending the capability menu

Do not add a new domain file because a game genre is mentioned. A domain
extension is justified only by repeated project evidence of distinctive,
reusable concerns not addressed by current core or menu. Require:

- source-backed activation condition and minimum relevant facts;
- specific reasoning questions and explicit exclusions;
- shared finding/evidence behavior;
- one positive and one **negative** activation example.

Start by extending this menu and its contrasts. Split out a separate
domain reference only when repeated real projects demonstrate a
distinctive maintenance problem. No agent swarm, generic graph,
persistent state, additional approval, or per-domain machine schema.

## Method references — not project authority

- [Unity Netcode authority](https://docs.unity.cn/Packages/com.unity.netcode.gameobjects%402.13/manual/terms-concepts/authority.html):
  a useful lens for multiplayer authority, **not** a universal topology.
- [Unity economy guide](https://unity.com/how-to/what-game-economy-guide-part-1):
  defines sources/sinks and resource flows, **not** project prices.
- [inkle ink authoring guide](https://github.com/inkle/ink/blob/master/Documentation/WritingWithInk.md):
  illustrates conditional choice and branching/rejoining, **not**
  evidence that a given game contains narrative branches.

These references inspire analysis questions only. Current project
instructions and approved sources remain authoritative.
