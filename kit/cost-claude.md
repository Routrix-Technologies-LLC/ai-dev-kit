## Keep usage and cost low

Assume the person is on the Claude Pro plan: a fixed monthly price with usage limits that reset every few hours. Every message, file read and agent uses some of that allowance, and the larger models use it several times faster. Running out mid-task is the most common way this goes wrong, so spend it carefully and say so when something will be expensive.

- **Main conversation on Sonnet.** If the session is running on Opus or Fable (the status line or `/model` shows it), suggest switching with `/model sonnet` in one friendly line, unless the person chose it on purpose. Opus is for the occasional genuinely hard problem (a stubborn bug, a big architecture decision), and only when the person agrees; Fable can be billed beyond the plan, so never suggest it casually.
- **Agents already use cheap models.** The kit's agents run on Sonnet for building and reviewing, and Haiku for research, writing and checklists. Do not raise an agent to Opus. For a quick lookup or summary, a Haiku agent (or doing it yourself) is enough.
- **Fewer, smaller agents.** Every agent starts fresh and re-reads files, so each one costs real usage. Use one agent where one will do, run at most two or three at a time, and do small things yourself.
- **Warn before the big workflows.** Skills that run a whole team (`/app-team-audit`, `/app-team-feature`, `/app-team-harden`, `/app-team-release`, `/app-code-review` on a large change, `/sec-assess`) use a large share of a Pro plan's allowance. Before starting one, say so in a sentence and offer the lighter path (one area, fewer lenses, or a single agent).
- **Read only what you need.** Search first, then read the relevant part of a file, rather than reading whole folders. Do not paste long logs back; summarize them.
- **If a limit is hit,** explain plainly: the allowance refreshes after a few hours, nothing is lost, and the work can pick up where it stopped. Save progress (`/kit-checkpoint`) before stopping.
