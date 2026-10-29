# Checklist: discovery to definition

Question: is the problem worth solving, for a named user, with a first version small enough to define?

Legend: **R** required (absent, placeholder-only or failing is FAIL). **rec** recommended (absent is CONCERNS). **-** not checked at this rigor (the report lists it as "not checked at <rigor>", never as passed). Paths follow the app's `paths:` overrides. **R\*** required only at review mode `full`: it reads the outcome of a per-artifact gate, and `lean` and `solo` do not run those. At other modes report `not run: <mode> mode`, which is not a failure.

## Artifacts

| # | Item | Where | Proof beyond existence | minimal | standard | full |
|---|---|---|---|---|---|---|
| 1 | Product brief (minimal) or vision (standard, full) | `docs/product/brief.md`, `docs/product/vision.md` | Problem, target user, MVP list, what it is not, and a success measure are each filled with real text; Grep for leftover template markers and count them | R | R | R |
| 2 | Riskiest assumption named, with how and when it will be tested | the brief or vision | A named assumption plus a test, spike or research step that is planned or done | R | R | R |
| 3 | Platforms and rigor decided | `studio.yaml` | `platforms` is non-empty and every entry is a valid value; `modes.rigor` is set. `stack` may still be empty | R | R | R |
| 4 | Risk register started | `planning/risks.md` (template `risk-entry.md`) | At least the riskiest assumption is a row with an owner | - | R | R |
| 5 | Target users grounded | the vision | Personas or user descriptions say what is sourced and what is assumption | - | R | R |
| 6 | Domain and comparable-product research | the vision or a research note | Claims carry sources; written by `domain-researcher` or cited | - | rec | R |
| 7 | `PD-VISION` outcome recorded | the brief or vision header | A recorded `PD-VISION` verdict that is not REJECT, and not NOT ASSESSED. A CONCERNS line needs the user's recorded acceptance. `TD-FEASIBILITY` is optional here | - | R* | R* |

## Quality checks

None can run at this transition (no code is expected). Print "Quality checks: none apply (discovery has no build)" so the absence is visible. If code already exists and `commands.build` is set, run it and report the result as information only.

## Manual checks (ask the user; "no" is a failed item, "not sure" is NOT ASSESSED)

- Is the MVP list small enough that you would be willing to build all of it?
- Is the success measure something you will actually look at after release?

## Panel focus

`PD-PHASE-GATE`: is the product worth defining and the scope honest. `TD-PHASE-GATE`: is anything in the brief obviously infeasible. `DD-PHASE-GATE` (full): is the intended experience stated. `PG-PHASE-GATE`: are the risks owned.

## On PASS

Stage becomes `definition`. Next: `/app-spec` for each MVP feature, `/app-ux` for key flows, `/app-design-language` (standard and full), `/app-prototype` for the riskiest assumption if it is not yet tested.
