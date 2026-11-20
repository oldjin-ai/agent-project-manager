---
name: {{ROLE_SKILL_NAME}}
description: {{PROJECT_SPECIFIC_ROLE_DESCRIPTION}}
---

# {{ROLE_TITLE}}

## Objective and authority

State this role's project outcome, delegated decisions, reserved decisions, and authorization references. (For PM in multi-agent mode: enforce 0 shell, 0 direct code/artifact edits, 0 self-QA, `<= 5` inspection reads/turn, dispatch-and-yield.)

## Authoritative inputs

Bind `CHARTER.md`, `MANAGEMENT-PLAN.md`, `PROJECT-PROFILE.md`, `RULEBOOK.md`, and required upstream artifacts by canonical reference (never hardcode mutable counts, digests, or model lists here).

## Deliverables and write scope

Specify output artifacts, exact **Allowed Write Paths**, **Forbidden Paths**, shared-resource isolation (`<= 1` active writer per scope; read-only DB clones), and downstream consumers.

## Execution and evidence

Specify the role's verified harness channel, mechanical pre-checks before submission, long-suite timeout budgeting, self-check evidence retention, and honest failure/uncertainty reporting.

## Review and handover

Specify Two-Plane Sealing responsibility (seal deliverables only, once on submit), independent reviewer recipient, diff-based rework loop (`<= 2` cycles before escalation), completion receipt (`record-external-outcome`), and cross-session checkpoint.
