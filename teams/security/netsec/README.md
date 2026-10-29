# netsec: the Security Firm's shared framework

Everything the agents share lives here. Read a section when your work needs it.

- `authorization.md`: the scope gate. The one rule above all others.
- `scope.example.yaml`: the engagement scope template. Copy to `scope.yaml` and
  fill in. `scope.yaml` is the authorization of record for a run.
- `roster.md`: the 29 agents, their practices, and the reporting lines.
- `coordination.md`: fan-out, resource discipline, how findings flow back.
- `orchestration.md`: how a full engagement and pointed runs are sequenced.
- `standards/`: `methodology.md`, `severity.md`, `evidence.md`,
  `rules-of-engagement.md`, `frameworks.md`.
- `gates/`: `ed-scope.md`, `finding-verified.md`, `rw-report.md` (and `README.md`).
- `templates/`: `finding.md`, `engagement-report.md`, `remediation-plan.md`,
  `detection-review.md`, `compliance-assessment.md`, `threat-model.md`.
- `shared/`: the blocks stitched into every agent. `common.md` for all, plus
  `director.md` / `lead.md` / `specialist.md` by tier.
- `tools/sync_shared.py`: restitch the shared blocks after editing `shared/`.

## Run an engagement

1. `python "$HOME/.ai-dev-kit/kit/install.py" project ~/Projects/<engagement> --team security` (or let `/kit-start` do it).
2. Fill `.claude/netsec/scope.yaml` with assets you own, from your infra record.
3. Open the folder in Claude Code. `/sec-engage` to scope, then `/sec-assess` (full)
   or a pointed `/sec-*` skill.

## Deliverables land in the engagement

Reports and plans go in the engagement's docs folder (from the templates); raw
scans and captures go in `~/AgentScratch/<engagement>/`, never in the repo.
