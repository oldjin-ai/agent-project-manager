# Initiation, risk tiers, and management authority

## Intake

Recover answers already present in the conversation, repository, and existing project records. Present a concise mandate to the user in their working language.

| Area | Record |
| --- | --- |
| Intended outcome | Who uses the result, what changes for them, and the completion condition |
| Scope | Required deliverables, quantities, formats, quality, and explicit exclusions |
| Acceptance | Requirement IDs and observable evidence for each important outcome |
| Dependencies | Access, data, people, APIs, hardware, environment, licenses, and external dates |
| Resources | Available agents/models, tools, execution channels, concurrent seats, and storage |
| Limits | Budget, quota, deadline, availability, and permission boundaries |
| Authority | PM-delegated decisions, user-reserved decisions, and existing authorization references |
| Continuity | Current truth source, retention, handover location, and operating horizon |

Classify unknowns by which action they affect. Ask one compact batch of questions for consequential unknowns. Leave downstream dependencies (such as missing release credentials) explicitly pending while authorized discovery, implementation, and local verification proceed.

An explicit request to complete a defined project is the execution mandate within its stated boundaries. Present routine planning choices for visibility and continue. Never assume permission for destructive operations, external releases, or boundary overrides.

## Risk-tiered governance sizing

Size governance rigor to project risk on day one instead of imposing one rigid pipeline on every task:

| Tier | When to use | Minimum deliverables & gates |
| --- | --- | --- |
| **Light** | Short utilities, internal analysis, small single-module prototypes | Compact `CHARTER.md` + `STATUS.md`; 1 independent check or user acceptance before declaring done |
| **Standard** | Multi-component software, recurring research portals, external documentation | Two-plane sealing on submit (`draft -> in_review`), mechanical pre-gate, diff-based re-review, batch sign-off |
| **Strict** | Production launches, multi-team pipelines, regulated/high-stakes releases | Full RACI, `PROJECT-PROFILE.md` + `RULEBOOK.md`, multi-seat independent review, live user-path walkthrough, atomic batch gates |

Write the selected tier and execution mode (`multi-agent` vs. `single-session`) into `PROJECT-PROFILE.md`.

## Two-layer setup and fast bootstrap

Separate **stable operating methodology** from **volatile project bindings**:

- **Stable layer (`MANAGEMENT-PLAN.md` + role `SKILL.md` files)**: Defines ownership, reviewer independence, sealing rules, escalation triggers, and completeness standards.
- **Mutable binding layer (`PROJECT-PROFILE.md`)**: Stores live canonical pointers, verified runtime model/provider names, write-scope boundaries, domain redlines, and any legacy compatibility notes. Role skills reference `PROJECT-PROFILE.md` instead of copying mutable file counts, hashes, or model IDs.

Use `assets/templates/management-plan.md` and `assets/templates/project-profile.md`. Author `MANAGEMENT-PLAN.md`, `PROJECT-PROFILE.md`, and the PM role skill cleanly, pass mechanical lint checks, and send them to a separate reviewer for a **1–2 round bootstrap check**. Incorporate substantive findings and record the baseline decision before unlocking broad downstream construction. Avoid spending 10+ review rounds polishing meta-governance before real deliverables move.

## Milestone planning

Work backward from the final outcome. For each milestone specify the usable result, required artifact versions, dependencies, critical-path tasks, capacity assumptions, quality gates, and acceptance authority.

- Define explicit **atomic batches** in `records/artifacts.json` (`batches`) when tightly coupled artifacts (e.g., backend + frontend, or acceptance report + deployment package) must be accepted together under one human sign-off.
- Keep acceptance dependencies acyclic. Candidate artifacts can be tested in parallel using pinned provisional inputs when the provisional status and revalidation trigger are recorded.
- Derive human-readable progress tables from the canonical JSON register rather than hand-copying counts and digests across multiple files.

## Taking over an existing project

Inventory actual outputs, existing decisions, in-flight tasks, and open findings before dispatching new construction. Sample claimed passes against raw logs and current files; label each claim accurately as `verified`, `reported`, `missing`, or `superseded`.

Where a legacy workspace already uses its own sealing or review scripts, document those legacy rules explicitly under **Legacy Compatibility Notes** in `PROJECT-PROFILE.md` (with a clear retirement path for the next major version) instead of breaking mid-flight pipelines. Prioritize closing missing outcome evidence, stabilizing broken gates, and halting premature draft sign-offs or repeated reseals.
