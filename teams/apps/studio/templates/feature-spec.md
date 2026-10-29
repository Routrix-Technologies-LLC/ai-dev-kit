# Feature Spec: [Feature name]

<!--
WRITTEN BY: product-manager with business-analyst; ux-designer consulted; the relevant lead checks feasibility. Skill: /app-spec.
LIVES AT: docs/product/specs/<feature>.md (override: paths.specs in studio.yaml). The <feature> slug is also the <feature> in REQ-<feature>-NNN.
RIGOR: minimal = sections 1, 3, 4 (briefly) and 12 only: a short overview, the behavior, the states that matter and a few testable criteria; the brief is the rest.
       standard = sections 1 to 14 filled or marked "N/A: reason"; every requirement has an ID and every ID has a criterion.
       full = standard plus feasibility sign-off (TD-FEASIBILITY), traceability from each REQ to stories and tests, and an independent /app-spec-review.
GATES: PD-SPEC-ALIGN (does it serve the vision and pillars), TD-FEASIBILITY (full), PM-ACCEPTANCE at story close.
Write behavior, not implementation. A spec says what the user can do and what the system guarantees; how it is built is for the architecture doc and ADRs.
Never delete a requirement ID; mark it Withdrawn. IDs are never reused or renumbered.
-->

**Status:** [Draft | In review | Approved | Implemented | Withdrawn]   **Owner:** [role]   **Last updated:** [YYYY-MM-DD]
**Serves:** [vision pillar IDs and job IDs, or brief MVP item]   **Related:** [UX spec path, ADRs, other specs]

## 1. Overview
<!-- Two to five sentences: what the feature is, who uses it, the problem it solves, and why now. Then one line each for scope in and scope out. A reader should be able to stop here and know whether this is the right document. -->
**Summary:** [text]
**In scope:** [text]   **Out of scope:** [text, with the reason]

## 2. User stories or jobs
<!-- Each is "When [situation], I want to [action], so I can [outcome]" or "As a [role], I want ..., so that ...". Good: one actor, one outcome, testable. Bad: "As a user I want a better experience." Number them U1, U2 ... and map each to the requirements that deliver it. -->
| ID | Story or job | Priority (P0 to P3) | Requirements |
|---|---|---|---|
| U1 | [story] | [P1] | REQ-[feature]-001 |

## 3. Detailed behavior
<!-- The normal flow, step by step, then the rules. Name every business rule, calculation, limit, default and ordering rule exactly: numbers, units, rounding, time zones, sort order. State what is true after each action, not only what the user does. Cross-reference the UX spec for layout and copy instead of duplicating them. Where a rule has several cases, use a decision table. -->
### 3.1 Main flow
1. [Step: trigger, action, system response]

### 3.2 Rules
| ID | Rule | Example |
|---|---|---|
| REQ-[feature]-001 | The system must [verifiable statement]. | [input gives output] |

## 4. States
<!-- Every state the feature or its data can be in, and how it moves between them: empty, loading, partial, populated, editing, saving, saved, error, offline, permission denied, stale, conflict. A state diagram or table; each state says what the user sees and can do. A missing state is a future bug. -->
| State | Entered when | User can | Leaves to |
|---|---|---|---|

## 5. Edge cases and failure behavior
<!-- Write the ones that hurt: zero items, a very large number, long or unusual text (right-to-left, emoji, accents), concurrent edits, interrupted operations (crash, kill, sleep, network drop mid-save), duplicate submission, clock changes, limits hit, partial failure in a batch, data from an older version. For each, say what happens and what the user is told. -->
| Case | Expected behavior | User-visible message or outcome |
|---|---|---|

## 6. Platform variants
<!-- Only what differs per platform in studio.yaml: input (touch, pointer, keyboard), navigation conventions, OS integration (share, notifications, shortcuts, menus, widgets), lifecycle (background, suspend, resume), limits, and anything unavailable on a platform with the chosen fallback. Write "same on all platforms" if true. -->
| Platform | Difference or constraint | Fallback if unsupported |
|---|---|---|

## 7. Data and API needs
<!-- Entities and fields the feature reads and writes (name, type, required, limits, who owns it), new or changed endpoints, commands or IPC messages (link the API contract), retention, and migration impact (link a data-migration plan if existing data changes). Flag anything that changes a stored format. -->
| Data / endpoint | Reads or writes | Fields and limits | Owner | Notes |
|---|---|---|---|---|

## 8. Permissions and access
<!-- Who may do what: roles, ownership, sharing, admin. OS permissions requested (camera, location, notifications, files) with the moment of the request and the denied-state behavior. Sensitive data touched, for the privacy review. Write "single user, no roles" if true. -->
| Actor or permission | Allowed actions | Denied behavior |
|---|---|---|

## 9. Analytics events
<!-- Only events that answer a product question, linked to the metric they feed. Name, trigger, properties. Full definitions live in tracking-plan.md; list the names here. Write "none" for apps without telemetry. -->
| Event | Trigger | Question it answers |
|---|---|---|

## 10. Accessibility
<!-- Requirements specific to this feature beyond the project baseline: keyboard path and focus order, screen reader names and announcements for dynamic changes, touch target sizes, contrast of any new color use, no information by color alone, reduced motion, time limits, error identification and recovery. Target: WCAG 2.2 AA unless the project states otherwise. -->
- [Requirement, e.g. REQ-[feature]-0NN: ...]

## 11. Localization
<!-- Strings externalized; plural and gender handling; formats for dates, numbers, currency, units; text expansion allowance (assume +30 to 40 percent); right-to-left layout; sorting and search rules; content that must not be translated. Write the initial language set. -->
- [Requirement]

## 12. Acceptance criteria
<!-- Binary, observable, one behavior each, in Given/When/Then. Every REQ ID has at least one criterion; every criterion cites its REQ. Include failure and edge paths, not only the happy path. "Works correctly" is not a criterion. Criteria become story acceptance criteria and test cases without rewording. -->
| REQ ID | Criterion |
|---|---|
| REQ-[feature]-001 | **Given** [precondition], **When** [action], **Then** [observable result]. |
| REQ-[feature]-002 | **Given** [precondition], **When** [failure or edge action], **Then** [observable result]. |

## 13. Configuration and feature flags
<!-- Settings the user can change (name, default, range, where shown) and flags the team uses to roll out or kill the feature (name, default, owner, removal date or condition). Every flag has an exit plan. -->
| Name | Kind (setting / flag) | Default | Range | Owner and removal condition |
|---|---|---|---|---|

## 14. Dependencies
<!-- Other features, specs, services, libraries, ADRs, design assets, legal or store requirements. Say what is blocked and what blocks. -->
- [Dependency, status, what it blocks]

## 15. Open questions
<!-- Each with an owner and a date it must be answered by, and which REQ it affects. A spec with unresolved questions that block a requirement is not Approved. -->
| # | Question | Owner | Needed by | Affects |
|---|---|---|---|---|

## Change log
| Date | Change | Requirement IDs affected |
|---|---|---|
