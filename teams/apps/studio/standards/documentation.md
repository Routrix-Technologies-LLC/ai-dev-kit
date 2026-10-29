# Documentation standards

Documentation is part of the product. It is written, reviewed and kept true like code.

## Principles

- **Docs as code.** Markdown, in the app's repo, next to what it describes (`layout.md` for paths), reviewed in the same change as the code it documents. Plain UTF-8, LF line endings unless the file already uses CRLF.
- **One job per document, one home per fact.** State a fact in one place and link to it. A second copy will drift.
- **Keep docs true when code changes.** A change that alters a command, path, flag, config key, behavior, API or UI also updates every doc that names it, in the same change. Before closing a story, search the docs for the old name (Grep, by folder). A wrong doc is worse than a missing one.
- **No em dashes or en dashes.** Use a colon, a comma, parentheses or two sentences. Scan human-facing text for U+2014 and U+2013 before finishing. A plain hyphen is fine inside compound words and for an empty table cell.
- **Plain and specific.** Short sentences, concrete nouns, exact commands and paths in code formatting. Define a term once. Gender-neutral wording. No filler, no marketing words.
- **Nothing secret.** No credentials, tokens, private keys, personal data or internal-only topology in a document that may be shared. Refer to secrets by name.

## Types (Diataxis)

Know which of the four a document is and do not mix them.

| Type | Reader's need | Shape | Example |
|---|---|---|---|
| Tutorial | Learn by doing | A guided lesson with a working result; every step succeeds | Getting started |
| How-to guide | Solve a specific task | Goal, prerequisites, numbered steps, how to verify, what to do if it fails | Deploy to staging, `runbook.md` |
| Reference | Look something up | Complete, accurate, neutral, structured the same way every time | API reference, config keys, CLI flags |
| Explanation | Understand why | Context, trade-offs, rationale, history | Architecture, ADRs, design language |

## Templates

Use the studio template for any artifact it covers (`templates/`): `product-brief.md`, `feature-spec.md`, `ux-spec.md`, `architecture.md`, `adr.md`, `api-contract.md`, `threat-model.md`, `privacy-review.md`, `test-plan.md`, `test-evidence.md`, `bug-report.md`, `runbook.md`, `incident-postmortem.md`, `release-notes.md`, `decision-log.md` and the rest. Required sections depend on rigor (`rigor.md`). Delete a template section that does not apply; do not leave it empty, and do not pad a minimal-rigor app with full-rigor ceremony.

## Authoring a long document

1. Ask the questions first; find what the repo and studio docs already answer.
2. Create the file with every section heading and an empty body.
3. Draft and settle one section at a time; write each section to the file as soon as it is agreed. The file is the memory, so a compaction loses nothing (`context.md`).
4. Requirements get IDs, acceptance criteria are binary and measurable, every number has a source or rationale.
5. End with open questions, each with an owner.
6. Read long documents by section when using them: Grep for headings, Read the range.

## Provenance for docs written from code

A document reverse-written from existing code (architecture overviews, API references, onboarding guides) says how it was made, so a reader can judge it:

- At the top: `Source: derived from code at commit <short hash> on <date>; not reviewed by the original authors.`
- Mark each claim you did not verify by running or reading the code path as `UNVERIFIED`.
- Mark intent you inferred (the why behind a design) as `INFERRED`, never as fact. Where the reason is unknown, write "reason not recorded", and ask the user.
- Cite files for non-obvious claims (`path:line`, or the module name).
- Claims about the outside world (standards, platform rules, competitors) cite their source.

## Decisions

A decision entry is dated and says why: `YYYY-MM-DD: Title`, then the decision, the reason, the alternatives rejected, and what would make it worth revisiting. At minimal rigor these live in `docs/decisions.md`; at higher rigor significant ones are ADRs (`adr.md`), numbered, never renumbered, superseded rather than edited. The user accepts an ADR.

## Review

- Before a doc ships, check every path, command, flag, link and version it names against the source.
- Documentation reviews use the existing `doc-council` skill in this workspace (seven lenses: editor, newcomer, executor, responder, factchecker, maintainer, gatekeeper). Run it only when the user asks, and one pass only. Do not re-run it on your own.
- `technical-writer` writes user and developer documentation and API reference; `principal-engineer` reviews developer docs and API reference for accuracy; `content-designer` owns in-product words; `release-manager` owns the CHANGELOG (Keep a Changelog format, semantic versions).
