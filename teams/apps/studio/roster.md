# App Studio roster

Sixty-eight agents in three tiers, organized the way a large product organization staffs one application: directors who own the why, the how, the experience and the delivery; leads who own a discipline or a platform; and specialists who do the deep work. Every agent runs on Sonnet (`model: sonnet`). None can spawn other agents: the main session (or a studio skill running in it) orchestrates.

The user is the owner and has the final word on everything. Directors advise the user; leads advise directors; specialists advise leads. Authority to decide flows down only as far as the user delegates it.

How to read the tables: **Reports to** is the shared parent for escalation (`coordination.md`). **Class** decides the collaboration protocol stamped into the agent (director, lead, builder, author, reviewer).

## Tier 1: Direction

| Agent | Owns | Use when | Reports to | Class |
|---|---|---|---|---|
| `product-director` | Product vision, pillars, target users, positioning, what the product is not; scope arbitration; product identity | A decision changes what the product is or who it is for; product and design or product and engineering deadlock on intent; cuts that touch identity | the user | director |
| `technical-director` | Architecture, technology and platform choices, cross-system contracts, technical risk, performance, reliability and security budgets with security-lead; reviews ADRs (TD-ADR) and recommends acceptance, which only the user grants through `/app-adr accept` | Architecture or stack decisions, cross-team technical conflicts, adopting a framework or dependency, budget violations | the user | director |
| `design-director` | Experience quality across every platform: design language and system, interaction and visual identity, the design quality bar; design review | The look, feel or flow of the product as a whole; design disciplines disagree; a design system decision | the user | director |
| `program-director` | Delivery: roadmap, milestones, sequencing, capacity, the risk register, cross-team coordination, change propagation, retrospectives | Planning what happens in what order, a change that ripples across teams, schedule or scope risk, status | the user | director |

## Tier 2: Leads

| Agent | Owns | Use when | Reports to | Class |
|---|---|---|---|---|
| `product-manager` | Feature specs and PRDs, requirements with IDs, acceptance criteria, prioritization, the backlog | Turning an idea into a buildable spec; deciding what is in a release; acceptance of finished work | `product-director` | lead |
| `principal-engineer` | Code-level architecture across the codebase, engineering standards, code review, module boundaries and internal APIs, refactoring strategy; assigns work to engineers | Structuring a change before it is built, reviewing code, standards questions, choosing which specialist builds what | `technical-director` | lead |
| `web-lead` | Web client architecture: rendering strategy (SPA, SSR, SSG, islands), state, routing, framework choice within the approved stack, web performance budgets | Any architectural question about a browser-based client or web UI | `technical-director` | lead |
| `desktop-lead` | Desktop architecture on Windows, macOS and Linux: native versus hybrid, OS integration strategy, distribution and update strategy | Building or changing a desktop app; choosing a desktop framework; cross-desktop consistency | `technical-director` | lead |
| `mobile-lead` | Mobile architecture on iOS, iPadOS and Android: native versus cross-platform, lifecycle, offline, permissions, device matrix, store strategy | Building or changing a phone or tablet app; choosing a mobile stack | `technical-director` | lead |
| `backend-lead` | Services, APIs, data architecture, integrations, background processing, scaling | Server-side design; anything with a database, an API or a queue | `technical-director` | lead |
| `platform-lead` | Build and CI/CD, environments, infrastructure and hosting (cloud or self-hosted), observability strategy, cost | How code gets built, tested, deployed, hosted and watched | `technical-director` | lead |
| `security-lead` | The security and privacy program: threat models, security and privacy review gates, secure defaults, stop-ship calls (escalated to the user) | Before building anything that touches auth, money, personal data, IPC, updates or the network; before any release | `technical-director` | lead |
| `qa-lead` | Test strategy, story testability, evidence standards, bug triage and severity, the release quality bar | Planning how a change will be proven, triaging bugs, deciding if quality is good enough | `program-director` | lead |
| `release-manager` | Versioning, release process and checklists, release notes, rollout and rollback, hotfix process, store and channel coordination | Cutting a release, shipping a hotfix, planning a staged rollout | `program-director` | lead |

## Tier 3: Specialists

### Product and research (report to `product-manager`)

| Agent | Owns | Use when | Reports to | Class |
|---|---|---|---|---|
| `business-analyst` | Requirements elicitation, process and domain modeling, business rules, decision tables, edge-case matrices, data dictionaries | A feature has complex rules, states or workflows that must be pinned down before building | `product-manager` | author |
| `domain-researcher` | Sourced facts about the problem domain: standards, regulations, real-world workflows, competitor and comparable products | A decision depends on how the real world works, what a standard says, or what competitors do | `product-manager` | author |
| `analytics-specialist` | Product metrics, event taxonomy, privacy-first telemetry design and implementation, experiments, dashboards | Defining success metrics, adding instrumentation, designing an A/B test | `product-manager` | builder |
| `monetization-specialist` | Pricing and licensing models, trials, in-app purchases and subscriptions, store billing rules, paywall design ethics | Deciding how the product makes money or is licensed | `product-manager` | author |

### Design (report to `design-director`)

| Agent | Owns | Use when | Reports to | Class |
|---|---|---|---|---|
| `ux-designer` | User flows, information architecture, wireframes, interaction specs, platform conventions (Apple HIG, Fluent, Material, web patterns) | Designing how a feature works for the user, screen by screen and state by state | `design-director` | author |
| `ui-designer` | Visual design: design tokens, type, color, spacing, iconography, component specs, theming (light, dark, high contrast), motion | Defining how things look and the component library's visual spec | `design-director` | author |
| `ux-researcher` | Research plans, heuristic evaluations, usability test scripts, evidence-based personas and journeys, synthesis | Testing whether a design works, evaluating an existing UI, understanding users | `design-director` | author |
| `content-designer` | UX writing: voice and tone, microcopy, error and empty states, terminology, notifications | Any words in the product: labels, messages, onboarding, errors | `design-director` | author |
| `accessibility-specialist` | WCAG 2.2 and platform accessibility APIs (ARIA, UI Automation, NSAccessibility, Android accessibility), screen readers, keyboard, contrast, motion, audits and fixes | Before and after building UI; any accessibility audit or fix | `design-director` | builder |
| `localization-specialist` | Internationalization architecture, string externalization, ICU messages, plurals, RTL, locale formats, pseudo-localization, translation pipeline | Preparing an app for more than one language or region | `design-director` | builder |
| `technical-writer` | User documentation, help, READMEs, API reference, tutorials, release-notes copy, in-app help | Anything a user or developer reads to learn the product | `design-director` | author |

### Web (report to `web-lead`)

| Agent | Owns | Use when | Reports to | Class |
|---|---|---|---|---|
| `frontend-engineer` | Web feature implementation: views, state, data fetching, forms and validation, routing, loading, empty and error states | Building or fixing a feature in a web client | `web-lead` | builder |
| `ui-engineer` | Component library and design-system implementation, CSS architecture, responsive layout, theming, motion, cross-platform UI consistency | Building components, styling, layout and theming work | `web-lead` | builder |
| `web-platform-engineer` | Browser APIs, PWAs, service workers, offline and storage, workers, WebAssembly, browser extensions (Manifest V3), cross-browser compatibility | Work that lives close to the browser itself, or any extension | `web-lead` | builder |
| `web-framework-specialist` | React and Next.js, Vue and Nuxt, Svelte and SvelteKit, Angular, Solid, Astro, Remix; SSR, SSG, hydration, routing, Vite and other build tooling | Framework-specific design, upgrades, rendering and build problems | `web-lead` | builder |

### Desktop (report to `desktop-lead`)

| Agent | Owns | Use when | Reports to | Class |
|---|---|---|---|---|
| `windows-desktop-engineer` | Windows apps: WinUI 3 and the Windows App SDK, WPF, WinForms, Win32 UI; shell integration (tray, taskbar, jump lists, toasts, file and protocol associations, startup, single instance), DPI, theming, package identity | Building or fixing a Windows desktop app's UI and OS integration | `desktop-lead` | builder |
| `win32-systems-specialist` | Low-level Windows: Win32, COM and WinRT, hooks and input, services, registry, IPC and named pipes, elevation and UAC, ETW, crash dumps, P/Invoke and windows-rs | Anything below the UI layer on Windows, or a hard Windows-specific bug | `desktop-lead` | builder |
| `macos-engineer` | macOS apps: AppKit and SwiftUI on the Mac, menu bar apps, sandbox and entitlements, hardened runtime, launch agents, privacy permissions | Building or fixing a Mac app or its OS integration | `desktop-lead` | builder |
| `linux-desktop-engineer` | Linux desktop: GTK and Qt, freedesktop specs (desktop entries, XDG dirs, D-Bus, notifications, portals), Wayland and X11, distro differences | Building or fixing a Linux desktop app | `desktop-lead` | builder |
| `hybrid-desktop-engineer` | Web-tech and cross-platform desktop shells: Tauri, Electron, WebView2 and WKWebView hosts, Flutter desktop, .NET MAUI and Avalonia, Qt Quick; IPC security, capabilities, native bridges, footprint | Desktop apps built on a webview or a cross-platform toolkit | `desktop-lead` | builder |
| `desktop-packaging-engineer` | Installers and distribution: MSIX, MSI and WiX, Inno Setup, NSIS, pkg and dmg, Flatpak, Snap, AppImage; code signing and notarization; auto-update; winget, Homebrew and Chocolatey | Making a desktop app installable, signed, updatable and listed | `desktop-lead` | builder |

### Mobile (report to `mobile-lead`)

| Agent | Owns | Use when | Reports to | Class |
|---|---|---|---|---|
| `ios-engineer` | iOS and iPadOS: Swift, SwiftUI, UIKit, app lifecycle, background tasks, APNs, permissions, Keychain, extensions and widgets, SwiftData and Core Data, XCTest | Building or fixing a native Apple mobile app | `mobile-lead` | builder |
| `android-engineer` | Android: Kotlin, Jetpack Compose, Views, lifecycle, WorkManager, FCM, permissions, Room, Hilt, Gradle, device fragmentation | Building or fixing a native Android app | `mobile-lead` | builder |
| `cross-platform-mobile-engineer` | React Native and Expo, Flutter and Dart, .NET MAUI, Kotlin Multiplatform, Capacitor; native modules, platform channels, performance | Mobile apps that share code across iOS and Android | `mobile-lead` | builder |
| `app-store-specialist` | App Store Connect, Google Play Console, Microsoft Store, Mac App Store: review guidelines, privacy labels and data safety forms, listings and screenshot specs, test tracks, phased rollout, ratings | Preparing a store submission, answering a rejection, store policy questions | `mobile-lead` (and `release-manager` for releases) | author |

### Backend and data (report to `backend-lead`)

| Agent | Owns | Use when | Reports to | Class |
|---|---|---|---|---|
| `backend-engineer` | Service implementation: business logic, request handling, validation, error handling, background jobs | Building or fixing server-side features | `backend-lead` | builder |
| `api-designer` | API contracts: REST, GraphQL, gRPC, WebSocket and IPC; OpenAPI and schemas; versioning, pagination, errors, idempotency, compatibility, contract tests | Designing or changing any interface another program depends on | `backend-lead` | builder |
| `database-engineer` | Schemas, migrations (reversible, forward-compatible), indexing, query performance, transactions, embedded and local storage, file and save formats, backups, data integrity | Anything that stores data, on a server or on a device | `backend-lead` | builder |
| `data-engineer` | Pipelines, ETL and ELT, event ingestion, warehouses, search indexes, data quality, retention jobs | Moving, transforming or analyzing data at volume | `backend-lead` | builder |
| `distributed-systems-engineer` | Concurrency, queues, caching, realtime (WebSockets, SSE), consistency, retries and backoff, rate limiting, scaling, sync and offline-first conflict resolution | Anything concurrent, realtime, synced or under load | `backend-lead` | builder |
| `integrations-engineer` | Third-party APIs and SDKs, OAuth client flows, webhooks, rate limits, vendor resilience (payments, messaging, streaming, cloud and AI provider APIs) | Connecting to a service the team does not own | `backend-lead` | builder |
| `identity-specialist` | Authentication and authorization: OAuth 2 and OIDC, sessions and tokens, passkeys and WebAuthn, MFA, roles and permissions, account lifecycle, platform sign-in | Sign-in, accounts, permissions, or tokens anywhere | `backend-lead` (and `security-lead` for review) | builder |
| `ai-features-engineer` | LLM and ML features: model and provider choice, prompts, tool use, retrieval, evals, cost and latency, safety, on-device models, speech | Building any feature that uses a model | `backend-lead` | builder |

### Languages (report to `principal-engineer`)

| Agent | Owns | Use when | Reports to | Class |
|---|---|---|---|---|
| `typescript-specialist` | TypeScript and JavaScript, Node, Deno and Bun runtimes, tsconfig, type design, module systems, package management | Language-level quality, typing and runtime questions in JS or TS code | `principal-engineer` | builder |
| `python-specialist` | Modern Python: typing, packaging (uv, pip, Poetry), asyncio, FastAPI, Django and Flask idioms, performance, pytest | Language-level quality and tooling in Python code | `principal-engineer` | builder |
| `dotnet-specialist` | C# and .NET: async, nullable reference types, DI, EF Core, ASP.NET Core, MSBuild, NuGet, trimming and AOT | Language-level quality and tooling in .NET code | `principal-engineer` | builder |
| `rust-specialist` | Rust: ownership and lifetimes, error handling, async (Tokio), unsafe and FFI, cargo workspaces and features, clippy, platform crates, Rust GUI toolkits | Language-level quality and tooling in Rust code | `principal-engineer` | builder |
| `go-specialist` | Go: idioms, concurrency, modules, net/http, context, testing, profiling | Language-level quality and tooling in Go code | `principal-engineer` | builder |
| `jvm-specialist` | Java and Kotlin on the JVM and shared Kotlin: Gradle and Maven, Spring and Ktor, coroutines, JVM tuning | Language-level quality and tooling in Java or Kotlin code | `principal-engineer` | builder |
| `cpp-specialist` | C and modern C++: CMake, vcpkg and Conan, RAII and memory safety, ABI, sanitizers, Qt C++ | Language-level quality and tooling in C or C++ code | `principal-engineer` | builder |

### Quality (report to `qa-lead` unless noted)

| Agent | Owns | Use when | Reports to | Class |
|---|---|---|---|---|
| `test-engineer` | Unit and integration tests, fixtures, test design, coverage gaps, test cases, bug reports, regression checklists | Writing or fixing tests, reporting a bug properly | `qa-lead` | builder |
| `test-automation-engineer` | End-to-end and UI automation for web (Playwright), desktop (UI Automation, FlaUI, WinAppDriver, XCUITest for Mac), mobile (XCUITest, Espresso, Maestro, Detox, Appium); visual regression; flakiness | Automating a user journey, screenshot capture, flaky suites | `qa-lead` | builder |
| `performance-engineer` | Performance budgets and profiling: startup, memory, CPU, rendering and jank, Web Vitals, bundle size, battery, network, load testing | Measuring or fixing anything slow, heavy or power-hungry | `qa-lead` (budgets set with `technical-director`) | builder |
| `code-reviewer` | Independent, adversarial pre-merge review of a diff for correctness, security, data loss and maintainability. Read-only | Any change before it merges, especially from another agent | `principal-engineer` | reviewer |

### Trust (report to `security-lead`)

| Agent | Owns | Use when | Reports to | Class |
|---|---|---|---|---|
| `security-engineer` | Application security reviews and audits (OWASP Top 10 and ASVS, MASVS for mobile, desktop specifics), dependency and supply-chain audit, secret scanning, hardening and fixes | Auditing code or a design for security, fixing a vulnerability | `security-lead` | builder |
| `privacy-specialist` | Data inventory and flows, minimization, consent, retention, user rights, privacy notices and store privacy declarations (drafts), telemetry review | Anything that collects, stores, shares or infers personal data | `security-lead` | author |
| `compliance-specialist` | Open-source license compliance and notices, SBOMs, third-party attribution, platform and store policy compliance, terms (drafts) | Adding dependencies or assets, preparing a release, policy questions | `security-lead` | author |

### Platform (report to `platform-lead` unless noted)

| Agent | Owns | Use when | Reports to | Class |
|---|---|---|---|---|
| `build-engineer` | Build systems and toolchains, CI pipelines (GitHub, Gitea, GitLab, Azure), caching, reproducible builds, version stamping, cross-compilation, signing in CI | Builds that are slow, broken, unreproducible or not automated | `platform-lead` | builder |
| `infrastructure-engineer` | Containers and Compose, Kubernetes, infrastructure as code (Terraform and OpenTofu, Ansible, Bicep), cloud and self-hosted hosting, networking, reverse proxies, TLS, DNS, environments | Where and how a service runs | `platform-lead` | builder |
| `site-reliability-engineer` | Observability (logs, metrics, traces, crash reporting), SLOs, alerting, runbooks, incident response, backups and disaster recovery, capacity, postmortems | Keeping a running service healthy, or recovering it | `platform-lead` | builder |
| `tools-engineer` | Internal developer tooling: scripts, code generators, dev environment setup, linter and formatter config, task runners, Claude Code tooling for an app | The team needs a tool, a script or a smoother dev loop | `principal-engineer` | builder |

### Engineering support (report to `principal-engineer`)

| Agent | Owns | Use when | Reports to | Class |
|---|---|---|---|---|
| `prototyper` | Throwaway spikes that answer one question fast, isolated from production code, ending in a recommendation | A risky idea or unknown technology needs proving before committing | `principal-engineer` | builder |
| `modernization-engineer` | Understanding existing codebases, reverse-documenting architecture, incremental refactors, major framework, runtime and dependency upgrades, strangler-fig migrations | Taking over or improving an app that already exists | `principal-engineer` | builder |
| `escalation-engineer` | The hardest bugs: reproduce, isolate, bisect, debuggers and crash dumps, races, leaks and corruption; root-cause write-up and regression test | A bug that others could not fix, a crash, anything intermittent | `principal-engineer` | builder |

## Picking agents

- **One discipline, one agent.** Brief the specialist directly; the lead reviews if the change is non-trivial.
- **A platform plus a language.** A Rust desktop app on Windows gets `windows-desktop-engineer` or `win32-systems-specialist` for the platform and `rust-specialist` for language quality. A React Native app gets `cross-platform-mobile-engineer` plus `typescript-specialist`. The app's `studio.yaml` `specialists:` list records the usual pairing.
- **Cross-cutting work** goes through the lead who owns the most of it, with the others consulted (`coordination.md`).
- **Before merge,** `code-reviewer` reviews any non-trivial change it did not write. Security-sensitive changes also get `security-engineer`.

## Not on the roster, on purpose

- **Game development roles** (game, level, narrative, audio design; engine specialists): games have their own studio template. Use that for games.
- **Sales, marketing, legal counsel, HR, support operations:** outside engineering. `technical-writer`, `content-designer`, `privacy-specialist` and `compliance-specialist` draft the product-facing pieces; a human signs off.
- **A dedicated scrum master or engineering manager:** `program-director` covers delivery, `principal-engineer` covers engineering assignment.

## Adding an agent

1. Write `.claude/agents/<name>.md` following `authoring.md` (frontmatter, role body, the `<!-- studio-shared: <class> -->` marker).
2. Add its row here, in the right tier and section.
3. Run `python studio/tools/sync_shared.py` from the package root to stamp the shared sections and check the roster.
4. Re-export to the projects and the user-wide install that should get it (see `README.md`, "Put it to work").
