---
name: sec-engage
description: "Start or scope a security engagement with the Security Firm: confirm or create scope.yaml, run the ED-SCOPE authorization gate, and plan the run. Use at the start of any assessment, when pointing the firm at an asset, or when the user says 'scope this', 'set up an engagement', 'what can you test', or 'am I authorized to test X'."
argument-hint: "[asset or goal] [--intensity passive|active|exploit]"
user-invocable: true
---

# Security engagement setup

Entry point for the Security Firm. This gets the authorization right before any
testing runs. Driven by `engagement-director`.

## Steps

1. **Find or create scope.** Look for `.claude/netsec/scope.yaml`. If it is
   missing, copy `.claude/netsec/scope.example.yaml` to it and fill it from the
   infrastructure record (`infra_source`, for a home lab the `kit-homelab`
   notes repository) and the user's goal. Confirm with the user that everything under
   `in_scope` is theirs and authorized. Never add a target the user has not
   confirmed they own.
2. **Run `ED-SCOPE`** (`netsec/gates/ed-scope.md`). Resolve the requested asset or
   goal to `in_scope`. A missing, unauthorized, placeholder, or out-of-scope
   request is a BLOCK: say exactly what to add or fix, and stop. Nothing active
   runs until CLEAR.
3. **Set intensity.** Honour `--intensity` or `default_intensity`
   (passive / active-nondestructive / exploit-opt-in). Exploit needs targets
   flagged `exploit_safe`.
4. **Plan the run.** Pick the roster for this engagement (pointed, themed, or full
   baseline, see `netsec/orchestration.md`), name which assets and which ATT&CK
   tactics are in and out, and show the plan so the user sees the edges before it
   starts.
5. **Hand off.** For a full run, go to `/sec-assess`. For a pointed run, launch the
   relevant specialists directly per the plan.

## Output

An authorized, scoped engagement with a written plan, or a clear BLOCK naming what
the user must add to `scope.yaml` first.
