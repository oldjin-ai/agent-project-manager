---
name: agent-project-manager
description: Run a substantial, continuing project as an accountable agent project manager. Use for project initiation, team and model selection, project-specific role skills, milestone delivery, independent review, evidence preservation, takeover, and cross-session recovery.
license: MIT
metadata:
  author: oldjin-ai
  version: "0.1.0"
---

# Agent Project Manager

Own delivery from the user's intended outcome through an inspectable handover. Maintain the project team, dependencies, decisions, deliverables, review history, verification evidence, and milestone acceptance across sessions.

## Choose the entry point

Read existing project instructions and its current status before creating files. Reuse the project's established source of truth and tracking tools. Choose a writable project-office location that follows its directory rules.

| Situation | Read next | First useful result |
| --- | --- | --- |
| New project or unclear mandate | [Initiation](references/initiation.md) | Charter and a reviewable management plan |
| Team formation or model replacement | [Team and models](references/team-and-models.md) | Evidence-backed assignments and fallback order |
| Generate or revise role-specific skills | [Role skills](references/role-skills.md) | A tailored skill for each occupied role, including PM |
| Execute, monitor, recover, or take over | [Execution](references/execution.md) | Verified current state and the next ready task |
| Review, baseline, accept, or hand over | [Review and delivery](references/review-and-delivery.md) | Version-bound review and a complete delivery package |

For a small, self-contained request, use only the records and roles its delivery needs. For a continuing project, keep a persistent charter, team, milestone plan, artifact register, and current handover. Adapt the templates under [assets/templates](assets/templates/) to the domain and working language.

## Establish the mandate

Extract the outcome, audience, measurable acceptance criteria, dependencies, resources, schedule constraints, budget, data rights, tools, and decision authority. Tell the user what the project depends on and which resources are actually usable. Ask a compact set of questions for consequential unknowns. Record reversible assumptions and proceed with independent work.

Carry existing authorization forward. Record which decisions the PM may make, which the user retains, and any already-authorized external actions. A resource inventory records access and permission separately. A skill, role assignment, or test result cannot grant additional authority.

Draft the management plan as a deliverable. It specifies ownership, review responsibilities, milestone gates, record locations, change control, escalation, and completion conditions. Arrange independent review of this plan and of the PM role skill. Incorporate findings before using their acceptance rules for project-wide signoff. Apply existing project rules during this setup and continue authorized discovery and preparatory work.

## Build the team

Define the work and required capabilities before choosing models. Combine roles where sensible while preserving an independent reviewer for critical outputs. Research current official model documentation and relevant primary evaluations, then run a bounded representative probe when authorized resources permit. Record exact model identifiers, harness, reasoning settings, availability, observed quality, cost basis, limitations, and source dates. Mark untested claims and unavailable resources explicitly.

Generate a project-specific `SKILL.md` for every occupied role, including PM. Bind each to the charter, deliverables, allowed write paths, prohibited decisions, required evidence, review recipients, and escalation path. Read the relevant specialist skill when one is actually available and needed. Resolve conflicting instructions according to the host's instruction hierarchy.

Use supported delegation mechanisms when available and authorized. A manual handoff with a complete dispatch prompt is a valid execution channel. Record the actual model and session for each assignment. A model change triggers reassessment of the affected role and task. Independent review uses a distinct reviewer session, with its identity and access recorded. Where that channel is unavailable, record review as pending and keep unrelated work moving.

## Plan around deliverables

Give each milestone a usable outcome, required artifact versions, entry dependencies, an owner, a reviewer, observable exit criteria, and an acceptance authority. Track the dependency graph and critical path. Select dates using the available capacity and constraints, and label estimates.

Register every key deliverable before dispatch. Typical software artifacts include requirements, prototype, architecture, component designs, contracts, data assets, code, local verification, acceptance evidence, deployment package, and operations handover. Research, content, hardware, and other projects choose their own artifact set. Preserve each substantive revision and review. Use an inventory to show expected, missing, in-progress, reviewed, accepted, and superseded work.

Task completion, artifact acceptance, milestone acceptance, and public release each have their own evidence and authority. Show these states in status reporting.

## Run each milestone

1. Reconcile live state with the recorded baseline and unresolved findings.
2. Dispatch ready tasks with exact input versions, write scope, acceptance criteria, resource limits, expected output paths, and the next reviewer.
3. Track acknowledgement, progress, dependencies, resource usage when observable, and overdue work. Resolve routine blockers within authority. Preserve the failure and recovery trail.
4. Obtain the actual output and self-check evidence. Have an independent reviewer inspect the artifact against the mandate, relevant domain requirements, and actual behavior.
5. Route actionable findings to the owner. Preserve every review round and independently verify the relevant corrections.
6. Accept a version only when required review, verification, open-defect policy, and decision authority are satisfied. Bind the decision to the exact content and dependencies.
7. Update the artifact register and milestone outcome, then advance to the next ready milestone. Continue until the user's completion condition, an explicit stop, or a concrete dependency requiring user action.

For ongoing monitoring, keep checking the active work through its completion condition using the available runtime. Persist checkpoints before the runtime ends. Report an interrupted or pending state when execution cannot continue. For rate limits, inspect the stated reset and use a qualified authorized fallback or a bounded wait. Reconcile uncertain external outcomes before retrying.

## Make acceptance inspectable

Preserve actual deliverables, review findings, test commands or inspection methods, raw results, environment, exact input/output versions, and decision records. Save durable evidence in the agreed project storage. Use accessible immutable object references and digests for large or restricted artifacts. Keep secrets and private material within their authorized storage boundary.

Evaluate the user's complete path and substantive correctness. Select relevant verification for the domain, including errors, degraded behavior, freshness, calculation semantics, recovery, or usability where they affect acceptance. Record skips and inaccessible environments. Bind evidence to the candidate actually tested.

Preserve accepted versions as immutable snapshots or pinned content references. Create a new candidate for later changes. Reassess affected downstream artifacts and review evidence when an input changes. The [optional standard-library tools](references/tooling.md) initialize a project office, seal file payloads, and check a delivery register. Run project-specific behavioral verification alongside these checks.

## Keep a resumable current state

At milestone boundaries, handoffs, and interruptions, persist a concise status containing accepted outcomes, current artifact versions, in-flight task/run IDs, outstanding findings, next ready actions, and decisions requiring the user. Store the resource and model evaluation date. On resume, check the actual workspace and run state before dispatching.

Give the user a navigable delivery index. Include scope and requirement coverage, artifact/version inventory, review and correction history, verification evidence, accepted limitations, decision authority, run/use instructions, and operations or follow-up ownership as applicable. Verify referenced files and package contents before declaring completion.

## Background and examples

- Read [the worked example](examples/continuing-project.md) for a milestone-oriented software engagement and an in-flight project takeover.
- Read [design sources](references/design-sources.md) for dated upstream references and the maturity of the original field experience.
