<!--
Template: release-notes. Written by: release-manager with content-designer. Skill: /app-release (store-length variants via /app-store-prep).
Lives at: inside docs/release/<version>.md under a "Release notes" heading, or docs/release/<version>-notes.md; the developer-facing record is CHANGELOG.md.
Rigor: minimal = a short list of what changed for users. standard = grouped sections, known issues, upgrade notes. full = adds localized variants, store-length versions and a support FAQ.
Delete this comment when the notes are created. Write for users, not developers: plain language, no ticket IDs, no internal names, no jargon, no blame.
-->

# [App name] [version]

*[Release date]*

[One or two sentences: the headline. What matters most to someone using the app.]

## New

- **[Feature name]**: [What you can now do, and why it helps. One sentence.]

## Improved

- [Something that is faster, clearer or easier, in terms of what the user notices.]

## Fixed

- [The problem as the user experienced it, now resolved. For example: "Fixed a crash when opening a file with an emoji in its name."]

## Good to know

- [Behavior changes, moved settings, removed features and what to do instead. Required action before or after updating, or "No action needed."]
- [Minimum supported OS or browser changes.]
- [Data or account migrations that run on first launch and how long they may take.]

## Known issues

- [Issue, who is affected, and a workaround if there is one. Say "None known" only if true.]

## Platforms

[Which platforms and versions this release covers, and any that ship later.]

## Need help?

[Support link or contact.]

---

Checks before publishing: every item matches CHANGELOG.md and what actually shipped; nothing promises unreleased work; no security fix details beyond what is safe to disclose (coordinate with security-lead); tone matches the app; reading level is plain; no em dashes or en dashes.
