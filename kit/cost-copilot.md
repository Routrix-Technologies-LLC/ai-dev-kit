## Keep usage and cost low

Assume the person is on an entry-level GitHub Copilot plan with a monthly allowance of premium requests. In the model picker, some models are included with the plan and others count as one or more premium requests per message, and the premium allowance runs out quickly with large models. Running out mid-task is the most common way this goes wrong, so spend it carefully and say so when something will be expensive.

- **Use the included models for everyday work.** If a premium or high-multiplier model is selected for routine work, suggest switching to an included model (or Auto) in one friendly line. Larger models are for the occasional genuinely hard problem, and only when the person agrees.
- **Fewer, smaller agents.** Every agent or subagent starts fresh and re-reads files, so each one costs real usage. Use one where one will do, run at most two or three at a time, and do small things yourself.
- **Warn before the big workflows.** Skills that run a whole team (`/app-team-audit`, `/app-team-feature`, `/app-team-harden`, `/app-team-release`, `/app-code-review` on a large change, `/sec-assess`) use a lot of requests. Before starting one, say so in a sentence and offer the lighter path (one area, fewer lenses, or a single agent).
- **Read only what you need.** Search first, then read the relevant part of a file. Do not paste long logs back; summarize them.
- **If the allowance runs out,** explain plainly what happened, that nothing is lost, and the options (wait for the monthly reset, use an included model, or upgrade the plan). Save progress (`/kit-checkpoint`) first.
