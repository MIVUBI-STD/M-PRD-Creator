# PRD Semantic Review Calibration (manual, non-executable)

This is a **synthetic evaluation aid**, not a project source, automated regression suite, or semantic PASS.
Use it only to calibrate changes to Project Requirements / PRD Production reasoning.
Read the input cases first; compare the reviewer response with the reference decisions afterward.
Do not include these invented game rules in any live PRD.

## Reviewer output

For each case, return: finding kind (or `NO MATERIAL FINDING`), relevant current `SRC` identity,
actor/event/scope, material consequence, smallest correction/question, and what was **not proven**.
Prefer one root finding over repeated warnings. Never report a runtime bug as reproduced.

## Input cases

### A — Superseded reconnect rule

- `SRC-101` (current authoritative): Disconnect ends the running attempt, clears unfinished progress,
  retains the player's assigned arena; reconnect starts a new attempt in that same arena.
- `SRC-102` (superseded): Reconnect resumes the previous checkpoint in a newly assigned arena.
- Candidate PRD: "After disconnect, assign a new arena and resume from the previous checkpoint."

### B — Competing completion triggers

- `SRC-201` (current authoritative): The match ends on flag capture **or** countdown expiry.
  Each finished match stores **one** result. No priority is specified for simultaneous events.
- Candidate PRD: "When flag capture and expiry occur together, flag capture always wins.
  Only one result is recorded."

### C — Separate reset ownership (control case)

- `SRC-301` (current authoritative): At round end, equipped items reset per player.
  A team bank persists across rounds and is cleared only at tournament end.
- Candidate PRD: "On round completion, clear each player's equipment and preserve
  the team's bank balance until the tournament ends."

## Reference decisions (open only after reviewing the inputs)

**A — One material contradiction:** The candidate contradicts `SRC-101` in *two* effects
of the same disconnect/reconnect rule: arena ownership and unfinished run progress.
`SRC-102` is superseded; do not treat it as a competing current authority.
Correct the PRD to keep arena assignment and restart the attempt. Do not invent
saved checkpoints, additional arena reassignment rules, or an observed reconnect bug.

**B — One missing decision / unsupported priority:** `SRC-201` establishes two
end conditions and an at-most-one-result invariant, but not their precedence when
they coincide. The candidate invents a capture-first priority. Route **one**
`MISSING_DECISION` to the existing Project Requirements owner; do not claim
that a duplicate-result race occurred or prescribe a synchronization architecture.

**C — No material finding:** Bank persistence and item reset concern different
owners and can coexist. Do not invent a wallet reset, shop, concurrency failure,
or additional approvals solely because both concepts use the word 'round'.

## Evaluation boundary

Check whether all material source disagreements were identified and whether the
review introduced any unsupported mechanic or false-positive blocker. A source
citation, a `REQ` marker, or an exact-byte hash is not semantic proof.
These authored answers are calibration expectations, **not independent measured
performance**; real production quality still requires review of actual project sources.
