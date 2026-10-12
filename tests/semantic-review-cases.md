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

## Two-pass manual evaluation

1. Give the reviewer **this file only**. Record the original answer to all three cases before opening any reference.
2. For each answer check the relevant current source, event/scope, root finding, correction, and unsupported claims.
3. Only after the answer is recorded, open `tests/semantic-review-key.md` to compare with the independently authored key.
4. Mark each case `MATCH`, `MISMATCH`, or `INCOMPLETE` and keep the concrete reasoning difference.

**Pilot acceptance:** all three cases must match their root decision and authority; no invented game mechanic,
duplicate blocker, or alleged reproduced runtime defect. This is a calibration check, not a confidence
score or real-project semantic quality proof. If the reviewer has already seen the key, mark the
attempt `CONTAMINATED` and do not report it as a blind measurement.

## Evaluation boundary

Check whether all material source disagreements were identified and whether the
review introduced any unsupported mechanic or false-positive blocker. A source
citation, a `REQ` marker, or an exact-byte hash is not semantic proof.
These authored answers are calibration expectations, **not independent measured
performance**; real production quality still requires review of actual project sources.
