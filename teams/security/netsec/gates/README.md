# Gates

A gate is a named check with a fixed set of verdict words. When a brief names a
gate, read its file first and return its verdict on the first line, then the
rationale (see `shared/common.md`, "Gates and verdicts").

| Gate | Owner | Purpose | Verdicts |
|---|---|---|---|
| `ED-SCOPE` | engagement-director | Authorization and scope are valid before anything runs | CLEAR, BLOCK, NOT ASSESSED |
| `FINDING-VERIFIED` | any lead/reviewer | One finding survives an adversarial re-check | CONFIRMED, PLAUSIBLE, REFUTED |
| `RW-REPORT` | report-writer | The assessment is evidenced, scoped, and honest before delivery | READY, CONCERNS, NOT ASSESSED |

`NOT ASSESSED` is always available when a named input was not provided or could
not be read. A problem you found takes the gate's own word even if an input was
also missing; name the missing input in the rationale.
