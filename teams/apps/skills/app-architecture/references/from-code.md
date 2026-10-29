# app-architecture: from-code mode

Loaded when the mode is `from-code`, in every phase. The aim is an architecture document that is true of the code today and honest about what the code cannot say.

## Provenance rules

- The document opens with the template's banner (`DOCUMENTED FROM CODE, NOT DESIGNED.`, filled in with the date, the agent and the commit) and keeps the template's `Provenance table`, one row per claim with its evidence and status (Observed, INTENT UNKNOWN, Confirmed by user). The banner is removed only when every INTENT UNKNOWN marker is resolved.
- Every statement of structure carries a source: a path, a manifest, a config file or a command output. Form: `Source: <path>`.
- Facts the repository cannot show (hosting, regions, who operates what, why a choice was made, traffic, SLOs) are never inferred. Write `NOT SOURCEABLE - <what> is not in the repository` or ask the user, and if `infra_record` in `studio.yaml` names a record, read it and cite it.
- Rationale is never invented. Where code shows a choice but not the reason, write `INTENT UNKNOWN` and ask the user in Phase 3. A confirmed answer is recorded with the date and marked Confirmed.
- Observed problems (cycles, layering violations, dead modules, duplicated stores) are recorded as findings in a separate "Observed issues" list, not smoothed into the design. Candidates for `/app-tech-debt`.

## Phase 2 for this mode

1. `modernization-engineer` runs first, alone. Brief: the repo path, `studio.yaml`, the instruction to enumerate: entry points and executables; build targets and manifests (package manifests, project files, Dockerfiles, compose files, CI workflows, installer definitions); runtime processes and how they communicate; data stores and migrations; external services called (from config, SDK use, URLs); authentication path; background jobs; feature flags; telemetry. Output `~/AgentScratch/app-architecture/reconstruction.md` with a source for every line.
2. The main session spot-checks at least five claims against the code (open the cited file, confirm the claim) and reports the count. Fewer than five claims available is itself reported.
3. `principal-engineer`, the platform leads and `security-lead` then review the reconstruction instead of proposing from scratch: confirm, correct, and list what is wrong or unexplained. Their files are `<agent>-review.md`.

## Phase 3 for this mode

For each section, show the reconstructed content with its sources and the open INTENT UNKNOWN items. Ask the user to confirm, correct or leave as unknown. Do not ask about items the code answers.

Containers and data stores are verified against the repository: the list in the document must match the build and deployment definitions found. A container in the document with no source, or a deployable in the repository missing from the document, is a defect to resolve before the section is written.

## Phase 5 for this mode

ADR audit adds a step: for each significant decision visible in the code with no ADR, propose a retrofit candidate (`/app-adr retrofit`) rather than a new decision. Do not retrofit here.

## Counts for the report

Claims sourced (with denominator of all structural claims), INTENT UNKNOWN count, NOT SOURCEABLE count, observed issues count, spot-checks performed and passed.
