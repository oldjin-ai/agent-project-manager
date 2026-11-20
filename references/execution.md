# Execution, WIP control, recovery, and continuity

## Dispatch contract

Use `assets/templates/task.md`. Keep prompts self-contained because subagents generally start with zero parent-session memory (`inheritsParentContext=false`). Bind every task dispatch to:

- Task ID, milestone ID, and requirement IDs
- Assigned role, exact provider/model, reasoning setting, and role skill path
- Pinned input artifact versions/digests and explicit `RULEBOOK.md` entries
- Exact **Allowed Write Paths** and **Forbidden Paths**
- Mechanical pre-checks, expected output paths, and resource/timeout budget
- Next designated reviewer or handoff recipient

## WIP limits and shared-resource isolation

Unbounded parallelism causes write collisions, stale reviews, and wasted quota:

- **Single writer per writable path**: Never allow more than **1** active implementation task targeting the same directory, module, or generated contract at a time. Merge tiny edits in the same module into one bounded task card.
- **Global concurrency cap**: Keep simultaneous active construction tasks bounded (default `<= 2` active build tasks; read-only reviews and verification reads may run separately within quota limits).
- **Shared database / state protection**: Treat any shared baseline database or snapshot as strictly **read-only**. Tasks that mutate schemas, write records, or test failure injection must clone an isolated copy (or run inside isolated temp dirs) and clean up afterward.
- **Cross-module scheduling**: Only run tasks in parallel when their write scopes are provably disjoint or isolated in clean, short-lived code branches/worktrees (never store heavy data snapshots or symlinks inside worktrees).

## Monitoring, budgets, and stalled-run recovery

- **Match timeout budgets to observed runtimes**: When running heavy integration/E2E suites (for example 25–35 minute suites), launch in background with unbuffered logging and a `1.5x–2x` budget (45–60 minutes). Record exact elapsed durations so future dispatches budget realistically.
- **Stalled-run kill-switch**: If an async execution or board task runs past the project stall threshold (default **90 minutes**) with zero workspace edits, logs, or artifact output on disk, settle/cancel it cleanly, record the diagnostic state, and split it into smaller tasks.
- **Reconcile before retry**: On timeout, cancellation, or tool error, inspect actual child status and disk artifacts before re-dispatching. Never blindly retry writes, deployments, or pointer switches whose previous attempt may have succeeded partially.

## 2-round anti-loop escalation

Do not trap developer and reviewer agents in endless ping-pong loops:

1. Allow at most **2 reject-fix-retest cycles** on the same artifact/defect, or **2 consecutive identical environment/quota failures** (`429`, hangs, missing tool auth).
2. On hitting the limit, **stop re-dispatching the same prompt**.
3. Collect the task/artifact ID, raw failure logs from both rounds, root-cause diagnosis, and **2–3 concrete resolution options** (e.g., split scope, revise ruling in `RULEBOOK.md`, update contract, or pause queue), then escalate to the designated technical/product authority or the user.

## Handover and status discipline

Always start user progress reports with the fixed **3-line executive status header**:

```text
Accepted N/M artifacts · Real-User Usable=Yes/No · Current Blocker: <concrete blocker or none>
```

Never replace accepted-artifact progress and live usability with task-board `done` counts or percentage completion.

At milestone boundaries, context expansion, or session handoffs, update `STATUS.md` using `assets/templates/handover.md` so a fresh PM session starts cold with zero guesswork:

- Current `HEAD` commit + dirty workspace summary (distinguishing pre-existing untracked files)
- `Accepted N/M` breakdown, active batch status, and canonical pointers
- Active/pending task IDs and manual handoffs awaiting response
- Open blocking/major findings and redlines (what the handoff session must NOT do: e.g., never self-sign, never promote unreviewed candidates, never switch production pointers)
- **Exact 3-step startup sequence** for the next PM session: (1) load the orchestrator skill, (2) run runtime model discovery (`list_subagent_models` / host check), (3) read `PROJECT-PROFILE.md` + `STATUS.md` + `records/artifacts.json` before issuing any task.
