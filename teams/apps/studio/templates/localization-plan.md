<!--
Template: localization-plan. Written by: localization-specialist with content-designer and ui-engineer. Skill: /app-i18n.
Lives at: docs/product/localization.md (override: paths.localization where the app maps it).
Rigor: minimal = locales and string source (or "English only, by decision"). standard = adds pipeline, pseudo-localization, formats, locale QA checklist. full = adds RTL plan, translation memory and glossary, per-store listing localization, and a per-locale release gate.
Delete this comment when the plan is created.
-->

# Localization plan

> **Date**: [YYYY-MM-DD]   **Owner**: [localization-specialist]
> **Status**: [English only by decision | Internationalization-ready | Localizing | Live in n locales]
> **Readiness verdict (from /app-i18n)**: [READY | GAPS | NOT READY | NOT ASSESSED]

## Locales

| Locale (BCP 47) | Language and region | Priority | Script / direction | Status | Owner of translations |
|---|---|---|---|---|---|
| [en-US] | [source language] | [source] | [Latin, LTR] | [Live] | [content-designer] |
| [de-DE] | | [Tier 1] | | [Planned] | |

Choose locales from user and market evidence, not guesswork. Note fallback chain (for example fr-CA to fr to en).

## String sources

| Surface | Where strings live | Format | Externalized | Count |
|---|---|---|---|---|
| [UI code] | [resource files / catalogs] | [ICU MessageFormat / gettext / platform resources] | [n of n] | [n] |
| [Server messages and emails] | | | | |
| [Store listings, release notes, onboarding] | | | | |
| [Docs and help] | | | | |

Rules: no concatenated sentences; use ICU placeholders and plural/select rules (languages have one to six plural forms); strings carry translator comments with context and character limits; no text inside images; stable string keys.

## Pipeline

1. Extract: [tool and command] produces [source catalog].
2. Translate: [in-house, vendor, community, machine plus human review]; glossary and style guide at `[path]`.
3. Import and validate: [placeholders intact, plural forms present, length limits, no missing keys].
4. Build: [locales bundled or downloaded]; missing keys fall back and are logged.
5. Release: [per-locale gate in the release checklist].

## Pseudo-localization

Pseudo-locale(s) enabled in debug builds: [for example accented-expanded and a mirrored RTL pseudo-locale]. Check: text expanded by about 30 to 40 percent does not clip or overlap; nothing hardcoded appears unaccented; concatenation bugs show up. Result: [date, findings].

## Right-to-left

[Not planned | Planned for locales: ...]. Mirroring rules: layout, navigation direction, icons that imply direction (arrows, progress) mirror; media controls, numerals-in-context and brand marks do not. Use logical (start/end) properties rather than left/right. Bidirectional text isolation for user-generated content. Test with a real RTL language, not only a mirror flag.

## Formats

| Item | Rule |
|---|---|
| Dates and times | Locale-aware APIs; store UTC; display in user time zone; calendar and first day of week |
| Numbers and currency | Locale-aware grouping and decimal separators; currency code explicit |
| Units | Metric/imperial by locale or user setting |
| Sorting and search | Locale-aware collation; case and accent folding |
| Names and addresses | No assumed first/last split or address format; flexible fields |
| Text input | IME composition, long words, emoji, combining marks |
| Fonts | Fallback coverage for target scripts; line height for tall scripts |

## Locale QA checklist

For each shipped locale (the platform matrix is in the test plan):
- [ ] No missing or placeholder strings; fallback log is empty
- [ ] Plurals and gendered forms correct for sample counts (0, 1, 2, 5, 11, 21, 100)
- [ ] No clipping, truncation or overlap at default and large text sizes
- [ ] Dates, numbers, currency and units formatted by locale
- [ ] Layout direction correct (RTL locales)
- [ ] Screenshots reviewed by a fluent reviewer, or marked NOT ASSESSED (an agent cannot judge translation quality or tone)
- [ ] Store listing, release notes and privacy text localized where the store requires
- [ ] Legal and age-rating text reviewed for the locale

## Open items

| Item | Owner | Due |
|---|---|---|
