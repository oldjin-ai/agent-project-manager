# Role skills and pure coordinator discipline

## Choose the operating mode explicitly

Declare the active operating mode in `PROJECT-PROFILE.md` before creating role skills:

- **Multi-agent coordinator mode (default)**: The PM main session owns scheduling, scope control, dependency tracking, ledger integrity, and escalation. It delegates **all** execution, coding, file sealing, testing, and substantive review to specialized role sessions.
- **Single-session fallback mode**: Used only when the host provides one session without subagents or independent reviewer channels. Every check run in that session must be labeled `self-check`, and required independent reviews remain `pending` until an external reviewer session completes them.

## Pure coordinator iron law (multi-agent mode)

In multi-agent mode, the PM main session enforces three non-negotiable boundaries:

1. **Zero direct shell execution**: Do not invoke bash/PowerShell/terminal tools directly for builds, tests, `curl` probes, service restarts, log grepping, or sealing/registry scripts. Route them to a dedicated execution runner seat.
2. **Zero direct edits to code, contracts, data, or deliverable artifacts**: Only update coordination status/handovers where delegated, or dispatch a governance/writer subagent so edits stay atomic and verified. Never hand-edit `CURRENT` pointers or manifests directly.
3. **Zero self-QA or proxy sign-off**: Never issue `REVIEW-*.md`, never mark yourself as `verifier` on a defect, and never mark a board card done without raw independent evidence (`artifacts/records` or `record-external-outcome`).

### Context budget and dispatch-and-yield

- Limit lightweight PM inspection reads/searches (`STATUS.md`, `PROJECT-PROFILE.md`, review conclusion headers) to at most **~5 calls per turn**. Delegate broad codebase scanning, diff audits, or multi-file hash verification to a read-only research/runner subagent returning a compact summary.
- **Dispatch and yield**: Once background subagents are launched (or manual handoff prompts are prepared for the user), stop calling tools for the current turn, report the active dispatches clearly, and wait for callback wakeups or user input. Never poll in a loop or run a second wave before the active wave settles.

### Anti-rationalization guard

When any of the following thoughts appear in multi-agent mode, treat it as a red flag and dispatch a subagent instead:

| Common PM excuse | Mandatory correction |
| --- | --- |
| "I'll just fix this 1-line typo / config / register line myself." | Dispatch the owning role subagent; even a 1-character direct edit breaks coordinator purity. |
| "I only want to run one quick `curl` or status command." | Dispatch a read-only runner subagent to execute and return the raw output + exit code. |
| "The playbook says 'PM may act autonomously' here." | Autonomy means no extra approval wait before dispatching — execution still goes through a worker subagent. |
| "Full tests/browser suites require host-level access." | Dispatch the host-runner subagent channel; host access belongs to the runner seat, not the PM main session. |
| "I'll quickly re-run `seal` or `promote` scripts myself." | Dispatch the runner subagent to run lint -> seal -> check sequentially and return exit codes. |
| "I'll poll until the server starts or the slow job finishes." | Bundle start/clean/run/verify inside one runner subagent; yield until it calls back. |
| "The reviewer hit `429`; I'll spot-check it myself to unblock." | Freeze the blocked acceptance queue or use a pre-qualified fallback; never self-verify. |
| "Let me scan 15 files first so my prompt is perfect." | Stay within 5 lightweight reads or dispatch 1 read-only research subagent first. |

## Generate project-specific role skills

Use `assets/templates/role-skill.md` to author one tailored `SKILL.md` per occupied role (including PM) under `<office>/roles/<role-name>/SKILL.md`.

- Use a lowercase alphanumeric-and-hyphen directory name (`<= 64` chars) matching frontmatter `name:` exactly.
- Bind each role skill to `CHARTER.md`, `MANAGEMENT-PLAN.md`, and `PROJECT-PROFILE.md` by reference rather than hardcoding volatile file counts, model IDs, or hashes inside the skill body.
- Define clear **Allowed Write Paths**, **Forbidden Paths**, **Self-Check Requirements**, **Independent Reviewer Recipient**, and **Escalation Triggers**.
- Check generated role skills for overlapping write ownership or accidental self-review loops before broad use, and verify the PM skill alongside `MANAGEMENT-PLAN.md` in the initial 1–2 round bootstrap review.
