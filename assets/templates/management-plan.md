# Project management plan

Project name {{PROJECT_NAME}}

## Risk tier, mode, and responsibilities

- Risk tier (`light` / `standard` / `strict`) and execution mode (`multi-agent` / `single-session`) — kept aligned with `PROJECT-PROFILE.md`.
- Pure coordinator boundaries (`0` direct shell / `0` direct edits / `0` self-QA in multi-agent mode).
- Owners, tiered independent reviewers, acceptance authority, escalation triggers, and bootstrap review (1–2 rounds max) of this plan and PM skill.

## Delivery inventory, sealing, and batches

- Required artifact types, milestone gates, and atomic acceptance `batches` (no premature draft sign-offs).
- Two-Plane Sealing mode (`seal-scope` or `seal`): deliverables sealed once on `draft -> in_review`; reviews/evidence/history live outside the deliverable manifest bound to `manifest_sha256`.

## Evidence, pre-gates, and review

- Mechanical pre-gates (lint, schema, digest, targeted tests) mandatory before invoking model reviewers.
- Diff-based incremental re-review on Round 2+ (2 clean rounds stop full re-reads; fallback to full review on blocker escape or contract/shape change).
- Severity policy (`blocking` / `major` / `minor`; zero open `blocking` or `major` at acceptance; `verifier != fixer` and `verifier != coordinator`).
- 8-class real-user completeness rubric and honest empty/degraded state checks.

## Execution, WIP, and recovery

- WIP limits (`<= 1` writer per writable scope, bounded global concurrency, read-only shared DB base + isolated clones).
- Long-suite timeout budgeting, stalled-run kill-switch (90m zero-evidence settle), `429` freeze/fallback (never spoof reviewer), and 2-round anti-loop escalation.

## Change control and status cadence

- Authoritative rulings recorded in append-only `RULEBOOK.md`.
- Fixed 3-line executive status header (`Accepted N/M artifacts · Real-User Usable=Yes/No · Current Blocker`) and cross-session handover cadence.

## Plan review record

Record revision, independent reviewer/session, findings, corrections, acceptance evidence, and any pending authority decision.
