<!--
Template: store-listing. Written by: app-store-specialist with privacy-specialist, content-designer and monetization-specialist. Skill: /app-store-prep.
Lives at: docs/release/store/<store>.md (one file per store: apple, google-play, microsoft, others). These are DRAFTS; the user submits.
Rigor: minimal = name, descriptions, screenshots list, privacy answers. standard = adds keywords, age rating answers, review notes, in-app purchase details. full = adds localization per locale, A/B variants, rejection history and responses.
Never put real credentials, API keys or personal data in this file. Verify current character limits, image sizes and policies against the store's official documentation when drafting, because they change.
Delete this comment when the listing is created.
-->

# Store listing: [store name] for [app name]

> **Store**: [Apple App Store | Google Play | Microsoft Store | other]
> **Version being submitted**: [version and build]   **Date drafted**: [YYYY-MM-DD]
> **Status**: [READY TO SUBMIT | GAPS | NOT ASSESSED]
> **Policy and limits checked against**: [official doc URLs, date read]

## Identity

| Field | Value | Limit | Length |
|---|---|---|---|
| App name | [...] | [per store] | [n] |
| Subtitle or short description | [...] | [per store] | [n] |
| Category (primary / secondary) | [...] | | |
| Bundle ID / package name / product ID | [...] | | |
| Support URL | [...] | | |
| Marketing URL | [...] | | |
| Privacy policy URL | [...] | required | |
| Contact for the store | [role email, not personal] | | |

## Descriptions

**Short / promotional text**
[...]

**Full description**
[Lead with what the app does for the user in the first two lines (often the only part shown). Then key features, then who it is for. No unverifiable claims, no competitor names, no keyword stuffing, no references to other platforms' stores where forbidden.]

**What's new (this version)**
[From release-notes.md, trimmed to the store limit.]

## Keywords and search terms

[Comma-separated, within the character limit, no repeats of words already in the name. Not applicable where the store does not use a keyword field.]

## Screenshots and media spec

| Device class | Required size or ratio | Count (min / max) | Orientation | Captions | Source |
|---|---|---|---|---|---|
| [phone small / large] | [per store docs] | [n / n] | | | `[docs/release/store/shots/...]` |
| [tablet] | | | | | |
| [desktop / window] | | | | | |
| [promo graphic / icon] | | | | | |
| [preview video] | | | | | |

Screenshots show the real app, current build, no placeholder or personal data, no device frames the store forbids, and match what ships. Localized sets: [locales].

## Privacy declarations

| Declaration | Answer | Source |
|---|---|---|
| Data collected (by category, linked to identity?, used for tracking?) | [...] | `docs/security/privacy.md` |
| Third-party SDKs and what they collect | [...] | |
| Data safety / privacy label / privacy manifest | [complete / gaps] | |
| Permissions requested and the in-app reason for each | [...] | |
| Account and data deletion path | [in-app location, web URL] | |
| Children's data | [not directed to children / details] | |

The declarations must match actual behavior including SDKs. Mismatch is a common rejection reason.

## Age rating answers

| Question | Answer |
|---|---|
| [violence, mature themes, gambling, user-generated content, web access, unrestricted chat, purchases, location sharing, ...per the store's questionnaire] | [Yes/No/Frequency] |

Resulting rating: [...]

## Pricing and in-app purchases

[Price tier, free/paid, subscriptions and products with IDs, trial terms, restore-purchases behavior, store billing rules satisfied.]

## Review notes

[What a reviewer needs: how to reach main features, special hardware, background behavior justification, entitlement or permission explanations, region restrictions.]

**Test account notes**: [Describe how a reviewer gets access, for example "a demo account is created with the Sign in as reviewer button" or "credentials are entered by the user in the store console". Do not write usernames, passwords or tokens here.]

## Compliance checklist

- [ ] Content, branding and trademarks cleared; licenses in `license-inventory.md`
- [ ] Export compliance, encryption and regional regulatory answers
- [ ] Payments, subscriptions and external-link rules satisfied
- [ ] Accessibility claims accurate (only claim what the audit supports)
- [ ] Signing, build number and target SDK/API requirements met

## Rejection response (fill if rejected)

| Date | Reason cited (store's words) | Our response | Change made | Resubmitted |
|---|---|---|---|---|
