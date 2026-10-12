# Context-Activated Domain Capabilities

Supporting method beneath [Behavioral Working Model](BEHAVIOR.md). This is a
selective reasoning menu, **not** a second root skill, plugin framework,
persisted registry, or `render-data.json` extension.

## Activation contract

Always start with the small core pass (evidence, scope/ownership, behavioral
consistency and observable outcome). Activate a specialized capability ONLY if
a current source-backed mechanism makes its questions material. A genre name,
sample map, hypothetical concern, or borrowed design is not enough.

All capabilities consume the **same** in-memory claims/relations/constraints,
and return grounded findings through `BEHAVIOR.md`. A capability cannot mutate
Project Requirements, approve Proposals, assert semantic PASS, or author new
game facts. Skip irrelevant domains entirely; do not generate empty N/A cards.

| Capability | Evidence required to activate | Focus | Must not assume |
|---|---|---|---|
| Session/lifecycle | Start, finish, retry, reset, reconnect or session described | ownership, lifecycle, cleanup, interruption, finalization | resume/retention policy |
| Multiplayer/concurrency | Interacting players or simultaneous sessions/arenas | isolation, disconnect, ownership, competing events | PvP, teams or economy |
| Competition/result | Win/loss, scored/completion outcomes, ranks, contest | result eligibility, ties, duplicates, fairness | every game has numeric scoring |
| Economy/resource | Actual acquire/spend/transfer/consume mechanics | resource creation/sinks, scarcity, exploit and persistence | shops or purchases |
| Time/progression | Timers, rounds, countdown, gates, ordered stages | trigger order, deadline, pause/expiry, retry | hard timeout |
| Puzzle/solvability | Puzzle gates, unlock dependencies, clues, logic | softlock, solvability, feedback, reset | single linear solution |
| Spatial/level design | Gameplay depends on spawns, paths, borders or plots | routing, permissions, boundary effects, accessibility | Minecraft-specific engine rules |
| Narrative/choice | Consequential choices, persistent branches | branch reachability, consistency, continuity | voiced dialogue |

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

Start by extending this menu. Split into a separate domain reference only
after it grows into a demonstrable maintenance problem. Do not add agent
swarm orchestration, generic dependency graphs, persistent state,
new approval steps or per-domain machine schemas.
