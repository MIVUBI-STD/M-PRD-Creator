# PRD Semantic Review Calibration — Reference Key

This file contains the **expected answers** to `semantic-review-cases.md`.
Do not provide it to the reviewer before the three input answers have been recorded.
Do not include these synthetic rules in any real project specification.

## Reference decisions

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

## Comparison

- **A:** current `SRC-101` outranks superseded `SRC-102`; the PRD must retain the arena and restart unfinished progress.
- **B:** one missing precedence decision / unsupported assumption; no actual race or duplicate result has been observed.
- **C:** no material finding; player equipment and team bank are different state owners.
- Record the first factual or semantic mismatch and do not rewrite the reference answer to obtain a PASS.
- Never infer real-world PRD quality from these three examples alone.
