---
name: app-i18n
description: "Check whether an app is ready to be localized (readiness mode) or run a localization pass for chosen locales (localize mode): string externalization, ICU messages and plurals, pseudo-localization, RTL, locale formats, fonts, and store listing strings. Use when the user asks about internationalization, localization, translations, supporting another language or region, RTL, pseudo-localization, or before shipping to new markets."
argument-hint: "[app] [readiness | localize <locale,...>] [--review solo|lean|full]"
user-invocable: true
---

# App internationalization and localization

Two modes with different inputs and outputs. `readiness` answers whether the app can be translated without code changes, and finds what blocks it. `localize` adds specific locales on top of a ready app: extract, brief, translate or receive translations, validate, and check the result on screen. Linguistic quality needs a fluent human; the skill says when that has not happened.

Writes: `docs/qa/i18n-<date>.md` (the report, both modes); string resource changes and locale files in the app's own resource location (localize mode, after approval); `docs/qa/evidence/i18n-<date>/` (pseudo-locale and RTL screenshots); a translator brief `docs/qa/i18n-<date>-brief-<locale>.md` when asked.
Next: `/app-dev-story` or `/app-plan` to fix externalization gaps, `/app-ux-review` for layout problems found, `/app-store-prep` for listing strings, `/app-gate` or `/app-release` consume the report.

## When to use and when not to

Use before the first translation, when adding locales, when adding UI text, and before a release that ships new markets. Not for: copy quality in the source language (`content-designer` via `/app-ux`), accessibility (`/app-a11y-audit`), or the whole store submission (`/app-store-prep`).

No mode in the argument: ask which. If `readiness` has never been run for this app and the user asks for `localize`, run `readiness` first and stop at its verdict if it is NOT READY.

## Inputs

- `studio.yaml` (required): `platforms`, `stack`, `commands`, `specialists`. Stop and offer `/app-adopt` or `/app-start` if absent.
- Target locales for `localize` (a list). Required. Ask; never choose markets for the user.
- Source language and the app's existing locale list, from the resource files. Unknown source language: ask.
- Optional: `docs/design/ux/` copy and character limits, `docs/design/design-language.md` (typography and font rules), existing translations or a glossary, the translation process in use (vendor, in-house, machine plus review).

## Phase 1: Plan and the stack's resource mechanism

Main session. Identify how the stack externalizes strings, from `docs/stack-reference.md`, the framework's current docs and the resource files in the repo. Never assume. Examples, not an exhaustive list:

| Platform | Typical mechanism |
|---|---|
| web | message catalogs with ICU MessageFormat or gettext through the framework's i18n library; `Intl` for formats; `lang` and `dir` attributes; locale in routing or negotiation |
| windows | resource files with the platform's resource loader, language-specific resource qualifiers |
| macos, ios | String Catalogs or `.strings` and `.stringsdict`, `Locale`, formatters, localized storyboards or SwiftUI localization |
| android | `res/values-<qualifier>/strings.xml`, plurals, `Locale`, per-app language preferences |
| linux | gettext or toolkit catalogs (GTK, Qt translation files) |
| cross-platform, hybrid | the framework's own (for example ARB files, i18n libraries) plus the host platform's locale APIs |
| backend | locale negotiation, localized error and email templates, locale-aware formatting, storage of times in UTC, collation |
| cli | message catalogs, locale-aware number and date output, non-ASCII input and output handling |

Announce the plan per `orchestration.md` section 2. Agents: `localization-specialist` (lead on this skill), `content-designer` (source copy clarity, context notes, glossary), and the builder for the platform UI layer chosen from `studio.yaml` `specialists` and `platforms` (`ui-engineer` for web, `windows-desktop-engineer`, `macos-engineer`, `ios-engineer`, `android-engineer`, `linux-desktop-engineer`, `hybrid-desktop-engineer`, `cross-platform-mobile-engineer`, or `backend-engineer` for services). Not spawned lists must say why. No gate runs in this skill (print `none run` accordingly); the review mode only affects which approvals are asked.

Check: the mechanism per platform is written down with its source, or marked UNKNOWN. UNKNOWN makes the externalization checks NOT ASSESSED.

## Mode A: readiness

### A1. Scan

Spawn `localization-specialist` (and the platform builder for a hard platform question) in parallel per orchestration sections 3 and 4. Output: `docs/qa/evidence/i18n-<date>/readiness-notes.md`. The brief names the code root, the mechanism from Phase 1, and these checks, each reported with a count and denominator (for example "38 hardcoded strings in 214 UI files"):

- Hardcoded user-facing strings: UI text, errors, notifications, tooltips, accessibility labels, validation messages, window titles, installer and menu text, server error messages shown to users.
- Concatenation and assembled sentences; word order assumptions; positional placeholders instead of named ones.
- Plurals, gender and ordinals done with `if count == 1` instead of the ICU or platform plural rules (languages have up to six plural categories).
- Locale-sensitive formatting: dates, times, time zones, numbers, currency, units, percentages, names and addresses, phone numbers, sorting and collation, case conversion (the Turkish dotless i), text segmentation.
- Text in images, icons, video or embedded in assets; screenshots in docs.
- Layout: fixed widths, truncation, clipped buttons; room for roughly 30 to 40 percent expansion and for tall scripts; multi-line wrapping.
- RTL: logical versus physical properties (start and end instead of left and right), mirroring of icons that imply direction, bidirectional text isolation for mixed content, number and punctuation handling.
- Fonts and scripts: glyph coverage for target scripts, fallback fonts, CJK line breaking, emoji, input method editor compatibility in text fields.
- Encoding and storage: UTF-8 end to end, database collation, file names, search.
- Locale identifiers: BCP 47 tags (`pt-BR`, `zh-Hant`), with fallback chains defined, not guessed from file names.
- Locale selection: detection, user override, persistence, per-app language settings where the platform has them, locale in URLs for web.
- Process: string keys with translator context and length limits, a string freeze practice, a place for glossary and do-not-translate terms.
- Store and marketing strings: listing text, screenshots, release notes, permission and consent copy.

A check with no sourced mechanism or an unresolvable code root is `NOT ASSESSED - <reason>`, never zero findings.

### A2. Pseudo-localization

If the stack supports a pseudo-locale (or one can be generated by transforming the source catalog with accents, expansion and brackets), build and run with it and, for RTL, a mirrored pseudo-locale, per section 10 without stealing focus. Capture the key screens into `docs/qa/evidence/i18n-<date>/`, view them, and record: strings that did not change (hardcoded), truncated or overlapping text, broken layouts, and unmirrored controls. If the app cannot be run or a pseudo-locale cannot be set up, this step is `NOT ASSESSED` with the reason, and readiness cannot be READY. A proposed change to build or config files needs the user's approval for the file set (section 3).

### A3. Report and verdict

Verify the findings the verdict turns on: re-read two hardcoded-string hits and one claimed-good screen yourself. Write `docs/qa/i18n-<date>.md`: mechanism, counts with denominators, findings by severity (CRITICAL, HIGH, MEDIUM, LOW per `standards/severity.md`), pseudo-locale evidence, a gap list ordered for fixing (proposed as stories for `/app-plan`), and NOT ASSESSED items.

Readiness verdicts, first match wins:

1. **NOT READY**: no string externalization mechanism exists, or user-facing strings in the core flows are hardcoded (the report gives the count), or the layout breaks under pseudo-localization in core flows, or text encoding cannot hold the target scripts.
2. **GAPS**: a mechanism exists and works for core flows, with remaining findings (non-core hardcoded strings, plural or format problems, RTL issues, missing context for translators).
3. **NOT ASSESSED**: no failures, but any check or the pseudo-locale run could not be done. Name each.
4. **READY**: mechanism present, no hardcoded user-facing strings found in the scanned scope (with the denominator), formats locale-aware, pseudo-locale and RTL runs clean, translator context present.

## Mode B: localize

Requires a readiness report that is not NOT READY (a recent report with READY, GAPS or NOT ASSESSED); if the latest report is NOT READY or absent, run Mode A first.

### B1. Freeze and extract

Ask the user whether source strings are frozen. A string changed after translation starts stale; record the freeze state (`frozen`, `not frozen`, `unknown`) in the report. `unknown` is shown as unknown, not as frozen. Spawn `localization-specialist` and `content-designer` to extract keys not yet in the catalog, add translator context (where it appears, character limit, placeholder meaning, plural or gender context), and propose the diff. List the files to be changed and ask once for the set before editing (section 3); new locale files are new artifacts, edits to existing resource files and code are approved as a set.

### B2. Brief and translate

Generate a translator brief on request: product summary, tone and voice, audience, glossary and do-not-translate list, placeholder reference, length limits, formality per locale. Source of translations, decided by the user:

- **Human or vendor translation** supplied back by the user: import and validate.
- **Machine draft** by an agent: allowed only when the user chooses it. Every drafted string is marked `needs-review` in the catalog or a sidecar. A paid translation service or API the app does not already use needs the user's yes first (section 6).
- **Leave to the user**: produce the brief and the catalog and stop.

### B3. Validate

Spawn `localization-specialist` to check each requested locale, reporting counts with denominators: completeness against the source, placeholder and tag mismatches, plural categories required by the locale versus provided, length violations against recorded limits, orphaned and stale keys, number, date and currency formats, encoding, and glossary adherence. Run the app in each locale and capture the key screens (section 10, no focus theft), RTL locales included. View them and note truncation, wrong fonts, missing glyphs, mirroring errors.

### B4. Store strings

If the app ships through stores, list the listing, release-note and permission strings per locale and hand them to `/app-store-prep`; this skill does not draft the whole listing.

### B5. Report and verdict

Write `docs/qa/i18n-<date>.md` with a per-locale table (total, translated, needs-review, stale, missing, validation findings, screens captured of N). 

Localize verdicts per run, first match wins:

1. **NOT READY**: the requested locale has missing or placeholder-broken strings in core flows, or the app breaks (crash, unreadable text) in that locale.
2. **GAPS**: the locale loads and core flows work, with remaining missing, stale, over-length or visually broken strings.
3. **NOT ASSESSED**: no failures, but linguistic quality was not reviewed by a fluent human (machine drafts, or no reviewer confirmed), the freeze state is unknown, or the locale could not be run on screen. Name each.
4. **READY**: complete, validated, seen on screen, and the user states a fluent human reviewed it.

## Rigor and review mode

| | minimal | standard | full |
|---|---|---|---|
| Readiness | externalization scan of core flows, one pseudo-locale run | all UI scan plus RTL pseudo-locale run | plus formats, fonts, input, backend and store strings |
| Localize | extract, validate, one screen set per locale | plus brief and all key screens | plus glossary check and a re-run after string freeze |

Rigor never lowers what must work: a locale that crashes is NOT READY at any rigor.

## Report

```
i18n: <app>   Mode: readiness | localize   Date: <date>   Source language: <lang|unknown>
Mechanism: <per platform | UNKNOWN>
Counts: <hardcoded strings N in M files>  <plural issues>  <format issues>  <layout issues>  (denominators given)
Pseudo-locale: ran | NOT ASSESSED (<why>)   RTL: ran | not applicable | NOT ASSESSED
Locales (localize): <locale: translated/total, needs-review n, stale n, screens captured k of N> ...
Human review: confirmed | not confirmed   Freeze: frozen | not frozen | unknown
Gaps proposed as stories: <n>
Decisions for you: <translation source, locales, freeze> | none
```

Then the closing block from `orchestration.md` section 8, with `Gates: none run (<mode>)`.

## Rules for this skill

- Never choose target locales or markets for the user.
- Never call a machine-drafted translation reviewed or ready; it needs a fluent human.
- Never report zero hardcoded strings from a scan of zero files or an unresolved code root; that is NOT ASSESSED.
- Never overwrite an existing translation; only add missing keys, and mark stale ones.
- Never edit resource files or code without the user's approval of the file set.
- Never use a paid translation service or API the app does not already use without a yes.
- Never claim RTL or a locale works without having run it on screen.
- Keep screenshots small and use test data.
