# Execution, monitoring, and recovery

## Dispatch contract

Use `assets/templates/task.md`. Bind every task to a milestone, acceptance criteria, specific input versions, expected artifact IDs, write scope, resource budget, self-checks, designated reviewer, and output location. Include the assigned model, reasoning setting, session/run ID, and role skill revision.

Resolve upstream dependencies before dispatch. A provisional input needs a pinned version, an explicit experimental purpose, and the downstream revalidation condition. Schedule parallel tasks only when their outputs and write scopes are compatible. Assign a single writer to shared registers and generated views. Use short-lived code branches or worktrees according to repository rules and keep durable evidence in canonical project storage.

Track requested, acknowledged, running, submitted, review, rework, accepted, blocked, or cancelled states. An acknowledgement identifies the task/run and understood scope. A submitted artifact includes the actual output path, content version, self-check output, known limits, and next reviewer.

## Monitor through the completion condition

Use the host's supported wait or status channel. On meaningful progress, failure, or a needed user action, update the persistent status and the user. Polling cadence should reflect observed run duration and tool limits. Save checkpoints at task transitions and before session boundaries.

For a failed task, preserve the error, diagnose its specific cause, choose an in-scope correction, and rerun the affected operation. Bound retries by the action's semantics and the project's resource limits. Read current state before retrying uploads, writes, deployments, or other actions whose prior outcome is uncertain.

For quota exhaustion, inspect the reset time and reassess qualified fallbacks. For a missing credential or user decision, leave dependent work pending with an exact unblock action and continue other ready work. Escalate repeated failure with the evidence, attempted fixes, impact on the critical path, and a recommended decision.

On cancellation or timeout, inspect actual child/run state. Record whether work stopped, continued, or has an unknown outcome. Recover partial output and reconcile ownership before redispatch. A tool timeout alone leaves execution outcome uncertain.

## Resume or hand over

Read the current handover, charter, artifact register, active milestone, in-flight task IDs, and unresolved findings. Verify the relevant workspace and service/run state. Detect changed inputs, obsolete model assignments, and missing evidence. Restore a coherent next action before starting a new task.

Use `assets/templates/handover.md`. Include accepted outputs, pending reviews, task/run IDs, exact candidate versions, unfinished external actions, dependency blockers, resource status, next ready tasks, and user-reserved decisions. Link raw records. Keep the next-step list executable by a fresh PM session.

## Change and drift

For changed scope, interfaces, data, models, or acceptance criteria, record the reason, authority, affected artifact versions, downstream consumers, and required retests. Preserve the previous baseline and findings. Mark the affected evidence stale until the relevant revalidation completes.

Use content digests or pinned versions for binding. Scope digests to the inputs actually consumed so unrelated repository changes have proportionate impact. Record code revision plus dirty changes and configuration/data versions where they affect behavior. Plan a new candidate and its review for accepted content changes.
