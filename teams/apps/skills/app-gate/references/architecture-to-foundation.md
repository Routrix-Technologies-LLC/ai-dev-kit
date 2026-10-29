# Checklist: architecture to foundation

Question: is the design settled enough to build a walking skeleton on, with the hard-to-reverse choices made on purpose?

Legend: **R** required (absent, placeholder-only or failing is FAIL). **rec** recommended (absent is CONCERNS). **-** not checked at this rigor (listed, never counted as passed). **R\*** required only at review mode `full`: it reads the outcome of a per-artifact gate, and `lean` and `solo` do not run those. At other modes report `not run: <mode> mode`, which is not a failure.

## Artifacts

| # | Item | Where | Proof beyond existence | minimal | standard | full |
|---|---|---|---|---|---|---|
| 1 | Architecture covering stack, data, hosting or distribution, and deployment topology | `docs/architecture/architecture.md`; at minimal, dated entries in `docs/decisions.md` that cover those four may stand in | Context, components, data, deployment and trust boundaries sections have real content (standard and full). Every entry in `studio.yaml` `platforms` appears in it; report "N of N platforms covered" | R | R | R |
| 2 | Stack chosen and pinned | `studio.yaml` `stack`; `docs/stack-reference.md` | Versions in the reference match the lock files or manifests (open one and compare). Versions were verified from official sources, with a date | R (stack filled) | R | R |
| 3 | Foundation decisions recorded | `docs/architecture/adr/`, or `docs/decisions.md` at minimal | Every decision the architecture lists as needing an ADR is Accepted. An ADR that another artifact depends on and is still Proposed is FAIL. Count Accepted of listed | R (decision log) | R | R |
| 4 | Threat model | `docs/security/threat-model.md` | Required at standard if the app touches auth, money, personal data, IPC, updates or the network; if unknown, ask. At full always. Data-flow diagram, trust boundaries and mitigations present | - | R if sensitive | R |
| 5 | Budgets with numbers | architecture doc; `perf-budget.md` at full | Startup, latency, size or reliability targets stated as numbers, with the device or load they apply to. `standards/rigor.md` requires performance budgets at full; at standard they are recommended | - | rec | R |
| 6 | Environments and secrets handling | architecture doc, `studio.yaml` `stack.hosting` | Environments named (or "local only" with the reason); where secrets live and how they stay out of the repo | rec | R | R |
| 7 | Test strategy | architecture doc or `docs/qa/test-plans/` | Which change types are tested how (`standards/testing.md`), and the commands that run them | rec | rec | R |
| 8 | Observability sketch | architecture doc | Logs, crash reporting and (deployed) metrics named at least by intent | - | rec | R |
| 9 | Per-artifact gate outcomes recorded | architecture doc and ADR headers | `TD-ARCHITECTURE` and `PE-FEASIBILITY` on the architecture doc; `TD-ADR` on each foundation ADR ("N of N"); `TD-STACK` on the stack choice; `SL-THREAT-MODEL` on the threat model where item 4 applies. None may be REJECT or NOT ASSESSED; a CONCERNS line needs the user's recorded acceptance. `TD-CHANGE-IMPACT` is optional | - | R* | R* |

## Quality checks

- Open the architecture doc and each Accepted ADR; confirm every file or ADR link it names resolves (Glob). Report "N of N links resolve".
- If a manifest or lock file already exists, check it against the stack reference (item 2).
- No build exists yet; print "Quality checks: no build at this transition".

## Manual checks

- Is there a decision you made verbally that is not in an ADR or the decision log?
- Is any platform in `platforms` there only because it might happen later? (Remove it or explain it.)

## Panel focus

`TD-PHASE-GATE`: soundness, risk, reversibility. `PG-PHASE-GATE`: can the foundation be planned and sized. `PD-PHASE-GATE` (full): the architecture still serves the vision. `DD-PHASE-GATE` (full): the design language is implementable on every platform chosen.

## On PASS

Stage becomes `foundation`. Next: `/app-test-setup`, `/app-plan` (foundation stories first), then `/app-dev-story` for the walking skeleton.
