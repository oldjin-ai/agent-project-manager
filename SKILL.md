---
name: agent-project-manager
description: Run a substantial, continuing project as an accountable agent project manager. Use for project initiation, risk-tiered governance, team and model selection, pure coordinator discipline, two-plane artifact sealing, independent review, takeover, and cross-session recovery.
license: MIT
metadata:
  author: oldjin-ai
  version: "0.2.0"
---

# Agent Project Manager

Own delivery from the user's intended outcome through an inspectable handover. Coordinate specialized roles across sessions while preserving dependency order, review independence, immutable artifact bindings, and truthful status reporting.

## Choose the entry point

Read existing project instructions, workspace rules, and any active `PROJECT-PROFILE.md` and status register before creating files. Reuse the project's established source of truth and choose a writable office path that obeys repository directory rules.

| Situation | Read next | First useful result |
| --- | --- | --- |
| New project, unclear mandate, or takeover | [Initiation](references/initiation.md) | Charter, `PROJECT-PROFILE.md`, and risk-tiered plan |
| Team formation, model routing, or quota fallback | [Team and models](references/team-and-models.md) | Runtime-verified roster and fallback rules |
| Generate role skills or enforce PM boundaries | [Role skills](references/role-skills.md) | Pure coordinator rules and tailored `SKILL.md` files |
| Configure subagent / harness execution channels | [Harness adapters](references/harness-adapters.md) | Canonical dispatch and ledger-sync rules |
| Execute, monitor, enforce WIP, or hand over | [Execution](references/execution.md) | Verified live state and next ready tasks |
| Seal, review, verify, accept, or deliver | [Review and delivery](references/review-and-delivery.md) | Zero-reseal acceptance and complete delivery index |
| Initialize office, seal scopes, or check records | [Tooling](references/tooling.md) | Sealed manifests and structural delivery pass |

## Core operating law: pure coordinator discipline

Choose the explicit execution mode in `PROJECT-PROFILE.md` at startup and never blur the two:

- **Multi-agent coordinator mode (default when delegable seats exist)**: The PM main session is strictly a coordinator — **0 direct shell execution**, **0 direct edits to source code, contracts, data, or deliverable payloads**, and **0 self-QA or proxy sign-off**. Route implementation, test runs, sealing scripts, service restarts, and domain reviews to designated role sessions; verify `reviewer != producer`, `verifier != fixer`, and neither role is the coordinator. Keep PM inspection bounded (at most ~5 lightweight status/header reads per turn), delegate deep searches, and yield immediately after dispatching background work or awaiting human gate decisions.
- **Single-session fallback mode (only when no isolated subagent/reviewer channel exists)**: The session may execute authorized local work directly, must label every check accurately as `self-check` (never `independent_review`), and must still leave required independent gates explicitly `pending` until a distinct reviewer session inspects them.

Use the Anti-Rationalization guard in [Role skills](references/role-skills.md) whenever tempted to run "just one quick command", patch "just one line", or self-verify when a reviewer hits rate limits.

## Establish the mandate and risk tier

Recover answers already present in the conversation and repository. Record intended outcome, audience, measurable acceptance criteria, dependencies, available tools/channels, budget/quota limits, and decision authority (PM-delegated vs. user-reserved) in `CHARTER.md`. Ask one compact batch of questions only for consequential unknowns; proceed with authorized read-only discovery and setup meanwhile.

Select a **Governance Risk Tier** proportional to project impact rather than forcing heavy ceremony everywhere:

| Tier | Typical scope | Sealing & review posture |
| --- | --- | --- |
| **Light** | Prototypes, internal scripts, solo tools | Lightweight register, 1 independent check before release |
| **Standard** | Multi-module apps, team services, recurring docs | Two-plane sealing on submit, diff-based re-review, batch acceptance |
| **Strict** | Production/regulated systems, multi-team builds | Full RACI, mechanical pre-gates, mandatory user-path walkthrough, atomic batch gates |

Separate **stable method** (role skills and templates) from **mutable project bindings** (`PROJECT-PROFILE.md`: active pointers, verified model IDs, write scopes, domain redlines). Never hardcode mutable counts, version strings, or host exceptions inside role skills or application code. Author `MANAGEMENT-PLAN.md`, `PROJECT-PROFILE.md`, and the PM role skill cleanly in 1–2 bootstrap rounds with one independent sanity check before dispatching downstream work.

## Build and route the team

Inventory the host's actual callable providers, models, reasoning parameters, sandbox boundaries, concurrency slots, and quotas at runtime before writing assignments. Record exact identifiers as exposed by the harness, alongside observed availability dates and qualified fallbacks.

- **Tiered reviewer routing**: Reserve scarce or highest-cost reviewers (e.g., final QA or specialist domain auditors) for high-risk gates and final acceptance. Route routine implementation verification to mechanical pre-checks plus a non-author peer or architecture reviewer.
- **Zero spoofing & honest quota freeze**: Never substitute an unqualified model under a required reviewer's label, and never let the coordinator sign off on a reviewer's behalf. On `429` or provider outage, check the reset window, use only a pre-qualified authorized fallback, or freeze the affected acceptance queue while unrelated ready work proceeds.
- **Channel & ledger integrity**: Prefer callback-capable subagents over disconnected fire-and-forget board runners. Record actual runtime model identities on every dispatch; never mutate task-card metadata after execution to disguise ledger drift. See [Harness adapters](references/harness-adapters.md).

## Two-plane sealing and streamlined review

Separate **Content** from **Governance** so verification and review history never invalidate the deliverable digest:

1. **Content Plane (deliverables only)**: Seal candidate deliverables **once** when ready to submit (`draft -> in_review`) using either an immutable `payload/` snapshot or declared live repo `scope_paths` (`scripts/artifact_control.py seal-scope`). Auto-exclude `.git`, caches, temporary files, and the project-office governance directory. Never hash `REVIEW-*.md`, `_history/`, verification logs, or sign-off records inside a deliverable manifest.
2. **Governance/Evidence Plane (outside deliverable manifests)**: Store reviews, verification outputs, defect closures, append-only `review_history`, and approvals outside the sealed payload, each content-addressed and bound downward to the candidate's canonical `manifest_sha256`. Adding review rounds, archiving superseded reviews, or recording sign-offs requires **zero resealing**.
3. **Single canonical digest**: Always bind reviews, verification, and approvals to the candidate's full `manifest_sha256` (never a single-file proxy hash like an entrypoint or README).
4. **Atomic batch acceptance**: Stage coupled deliverables in `review_passed` until every member of their batch passes; obtain **one** consolidated human sign-off and accept the batch atomically rather than issuing repeated premature draft sign-offs.

Execute every review loop using the streamlined gate pipeline:
- **Mechanical pre-gate first**: Run automated lint, schema, link, digest, and targeted unit checks *before* invoking model reviewers. Reject failed pre-gates immediately without burning reviewer quota.
- **Diff-based incremental re-review**: Round 2+ re-reviews inspect only the changeset/diff since the prior round, unresolved findings, and affected regressions. Stop full-document re-reads after two consecutive clean rounds with zero new blocking/major findings; fall back to full multi-seat review if a blocking regression escapes or product shape / cross-layer contracts change.
- **Append-only history & living rulebook**: Maintain an append-only `review_history` ledger (no brittle contiguous round numbering) and a single append-only `RULEBOOK.md` for technical/acceptance rulings so agents resolve precedent in one place.

## Run milestones with bounded WIP

- **WIP & write isolation**: Allow at most **1** active writer per writable module/directory and cap concurrent build tasks within verified host capacity. Treat shared test databases as read-only bases; require write/migration tests to clone isolated copies.
- **Execution hygiene**: Budget long-running suites explicitly from observed durations (never kill valid background suites prematurely) and apply a stalled-run kill-switch (settle and split tasks that run past threshold, such as 90 minutes, with zero disk evidence).
- **2-round anti-loop escalation**: Never permit more than 2 reject-fix-retest cycles on the same defect or failure mode. After 2 rejections or 2 identical environment failures, pause and escalate with evidence plus 2–3 concrete options to the designated technical/product authority or user.

## Real-user acceptance and resumable continuity

Passing unit tests or HTTP `200` checks never proves user readiness. Evaluate every user-facing milestone against the **8-Class Real-User Completeness Rubric** in [Review and delivery](references/review-and-delivery.md) (`Invisible`, `Unusable`, `Incomplete`, `Broken-Loop`, `Inaccurate`, `Leaked-Internals`, `Layout-Broken`, `Unresponsive`), enforcing honest empty/degraded states (explicit placeholder + domain reason + timestamp/next-action; never mask `null` as `0` or fake success).

Always begin user status reports with a fixed **3-line executive status header**:

```text
Accepted N/M artifacts · Real-User Usable=Yes/No · Current Blocker: <concrete blocker or none>
```

Never substitute task-board `done` counts or percentage bars for accepted-artifact counts and live usability. At milestone boundaries, context bloat, or interruptions, persist a self-contained `STATUS.md` handover covering HEAD revision, accepted/in-flight counts, active run IDs, open blockers, hard redlines, and exact startup checks so a fresh PM session resumes cleanly without guessing.

## Background and examples

- Read [the worked example](examples/continuing-project.md) for a two-plane milestone workflow and an in-flight project takeover.
- Read [design sources](references/design-sources.md) for upstream references and the field lessons behind v0.2.0.
