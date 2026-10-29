# Checklist: definition to architecture

Question: is the first version defined well enough to design a system for?

Legend: **R** required (absent, placeholder-only or failing is FAIL). **rec** recommended (absent is CONCERNS). **-** not checked at this rigor (listed in the report, never counted as passed). A "UI platform" is any of web, windows, macos, linux, ios, android, extension in `studio.yaml` `platforms`. For backend, cli and library apps the UI items read `N/A: no UI platform` in the report (a cli still needs its command and output design in the spec). **R\*** required only at review mode `full`: it reads the outcome of a per-artifact gate, and `lean` and `solo` do not run those. At other modes report `not run: <mode> mode`, which is not a failure.

## Artifacts

| # | Item | Where | Proof beyond existence | minimal | standard | full |
|---|---|---|---|---|---|---|
| 1 | MVP list with one binary acceptance line per item | brief or vision | Count MVP items and acceptance lines; report "N of N" | R | R | R |
| 2 | A feature spec for every MVP feature | `docs/product/specs/*.md` | Count specs against the MVP feature list (denominator); each has requirement IDs `REQ-<feature>-NNN` | - | R | R |
| 3 | IDs unique, criteria binary | the specs | Grep all `REQ-` IDs; a duplicate ID is FAIL. Read two criteria per spec; "fast", "intuitive" or "works well" with no threshold is a finding | - | R | R |
| 4 | No unresolved blocking questions | the specs | Grep for `TBD`, `OPEN QUESTION`, `TODO` and count with the number of files scanned. Each hit is either non-blocking (say why) or a failed item | rec | R | R |
| 5 | Spec review with no open MAJOR REVISION | `docs/product/reviews/` | Newest review per spec; verdict not MAJOR REVISION | - | rec | R |
| 6 | UX spec for each key flow, every state covered | `docs/design/ux/*.md` | Loading, empty, error, offline and permission-denied states appear where they apply; UI platforms only | - | R | R |
| 7 | Design language | `docs/design/design-language.md` | Tokens, type, color, components, theming and per-platform adaptation sections have content; UI platforms only. `standards/rigor.md` requires it at full; at standard it is recommended (absent is CONCERNS) | - | rec | R |
| 8 | Data inventory started | `docs/security/privacy.md` | Lists what personal data the MVP collects, or says "none" with the reason | - | rec | R |
| 9 | Per-artifact gate outcomes recorded | spec, UX spec and design language headers | `PD-SPEC-ALIGN` on each spec (count "N of N specs"), `DD-UX-SPEC` on each UX spec ("N of N flows"), `DD-DESIGN-LANGUAGE` on the design language, each with a verdict that is not blocking. `TD-FEASIBILITY` and `QL-STORY-READY` are optional here | - | R* | R* |

## Quality checks

None can run (documents only). Print "Quality checks: none apply (definition has no build)". If a prototype exists in `prototypes/`, read its report: a KILL verdict on something a spec depends on is a finding.

## Manual checks

- Would you be comfortable handing these specs to someone who has never spoken to you? If no, name what is missing.
- For each UI platform: is there a flow nobody has specified yet that the MVP needs?

## Panel focus

Required at standard: `PD-PHASE-GATE` (do the specs match the vision and the non-goals), `DD-PHASE-GATE` (flows and design language coherent; for an app with no UI platform it reports N/A), `TD-PHASE-GATE` (anything specified that cannot be built within the likely stack). `PG-PHASE-GATE` (scope is sized for the team and time) is optional at standard and runs at full rigor.

## On PASS

Stage becomes `architecture`. Next: `/app-stack`, `/app-architecture`, `/app-adr`, `/app-threat-model` (standard and full), `/app-api` and `/app-data-migration` where the specs imply them.
