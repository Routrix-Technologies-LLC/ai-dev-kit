# Rigor and review modes

**Rigor relaxes what must exist, never what must work.** At every level the build is green, the tests that exist pass, a user-visible change is run and looked at, saved data and public APIs stay compatible, and no secret is committed. Lower rigor means fewer documents and fewer gates, not fewer facts verified.

`modes.rigor` in `studio.yaml` sets the level; unset means `minimal`, the right default for solo and small apps. Raise it when the app has more than one contributor, handles money, accounts or sensitive data, ships to a store, or is hard to roll back. Raise it per app, not per task.

## What must exist

| | minimal | standard | full |
|---|---|---|---|
| Before code | `docs/product/brief.md` (one page: problem, user, scope, non-goals, platforms); `studio.yaml` with `commands`; a short story or a clear user request | Vision; a feature spec for each feature (requirement IDs, binary acceptance criteria); UX spec for new flows; design language for any app with a UI; architecture overview; ADRs for foundation and hard-to-reverse choices; threat model if the app touches auth, money, personal data, IPC, updates or the network; stack reference | Everything in standard; an ADR for every significant decision; privacy record; performance budgets; test plan; accessibility and localization plan; API contracts and migration plans before any build |
| Decisions | Dated entries in `docs/decisions.md` | ADRs for the significant ones, decision log for the rest | ADRs for all significant ones, each accepted by the user |
| Stories | Optional; a task list is enough | Stories with acceptance criteria linked to requirement IDs | Epics and stories with IDs, estimates and dependencies; sprint or batch plans |
| Evidence per change | The change type's required evidence (`testing.md`) | The same, retained under `docs/qa/evidence/` | The same, plus a signed-off test plan and regression checklist |
| Gates: build to hardening | None at solo; phase gates only if the user asks with `--review lean` or `full` | Phase gates per `gates/README.md`; `PE-CODE-REVIEW` at each `/app-story-done` for non-trivial changes (always-on in lean) | All phase gates; `PM-ACCEPTANCE`, `PE-CODE-REVIEW` and `QL-TEST-COVERAGE` on every closed story |
| Gates: release | Release checklist, tests green, run and observe done, CHANGELOG entry. No gate runs at solo, so the release report cannot be GO on gate evidence it did not collect (`gates/README.md`): it is CONCERNS or NOT ASSESSED unless the user explicitly accepts an unreviewed release | `RM-RELEASE-READY`, `QL-RELEASE-QUALITY` and `SL-SECURITY-REVIEW` at every `/app-release`; `SL-PRIVACY` when personal-data handling changed | Every release gate, `SL-PRIVACY`, accessibility audit, performance against budgets |
| Docs | README, run and build instructions, CHANGELOG | Plus architecture overview, API reference where there is an API, runbook if deployed | Plus user documentation, full API reference, runbooks and postmortems |

A document that exists but was never true is worse than one that was skipped. At any level, do not create a template-shaped file just to fill the table.

## Review modes

`modes.review` sets how much independent review runs. Unset follows rigor. A skill argument `--review solo|lean|full` overrides it for that run only.

| Mode | Default for | What runs |
|---|---|---|
| `solo` | `minimal` | No gates. The author runs build, lint and tests and does the run-and-observe step. The user is the reviewer. Skipped gates announce themselves (`<GATE-ID> skipped: solo mode`) |
| `lean` | `standard` | Phase gates and the always-on gates listed in `gates/README.md` (release, security, privacy, `PE-CODE-REVIEW` at `/app-story-done` for non-trivial changes, and a single-purpose review skill's own gate); every other gate is skipped and says so. `code-reviewer` on non-trivial changes written by an agent. `security-engineer` on security-sensitive changes |
| `full` | `full` | Every gate a skill defines. `code-reviewer` on every merge. Domain reviews in parallel (security, accessibility, performance) |

Some things are never relaxed by mode: security-sensitive changes (auth, money, personal data, IPC, updates, crypto, parsing of untrusted input) always get a security look before release, and anything destructive to user data always gets the user's explicit yes. Review mode decides who reviews, not whether the work was verified.

## Changing the level

Raise rigor when a risk or team change justifies it, and say what new artifacts that creates. Lower it only on the user's word, and never to get a failing check past a gate.
