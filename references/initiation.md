# Initiation and management authority

## Intake

Recover answers already present in the conversation, repository, and current project records. Present a concise mandate to the user in their language.

| Area | Record |
| --- | --- |
| Intended outcome | Who uses the result, what changes for them, and the completion condition |
| Scope | Required deliverables, quantities, formats, quality, and explicit exclusions |
| Acceptance | Requirement IDs and observable evidence for each important outcome |
| Dependencies | Access, data, people, APIs, hardware, environment, licenses, and external dates |
| Resources | Available agents/models, tools, execution channels, concurrent seats, and storage |
| Limits | Budget, quota, deadline, availability, and permission boundaries |
| Authority | PM decisions, user-reserved decisions, and existing authorization references |
| Continuity | Current truth source, retention, handover location, and intended operating horizon |

Classify unknowns by which action they affect. Ask about material gaps together. A missing release credential can leave publication pending while research, implementation, and local validation continue. Record who must supply each dependency and a realistic checkpoint.

An explicit request to complete a defined project is the execution mandate within its stated boundaries. Present routine planning choices for visibility and continue. Ask for decisions where the missing answer changes a material commitment or where an action lacks permission.

## Management plan as a first deliverable

Use `assets/templates/management-plan.md`. Specify the artifact inventory, responsibilities, reviewer independence, accepted evidence, severity policy, change authority, escalation criteria, storage, cadence, and final handover format.

The PM authors the plan and their own role skill. A separate reviewer evaluates both against the user's mandate and host constraints. Record the plan revision, reviewer session, findings, corrections, and decision. Apply user approval to the boundaries they retain. Set interim coordination rules explicitly while this review is pending.

Size the process to risk. Reviews can cover a coherent group of artifacts in one session while recording a decision per version. Use existing issue trackers, file conventions, or artifact storage if they already serve the project. Keep one authoritative state record and derive summaries from it.

## Milestone planning

Work backward from the final outcome. For each milestone specify the usable result, required artifact versions, dependencies, critical-path tasks, capacity assumptions, quality gates, and decision owner. Include discovery or feasibility milestones when a dependency remains uncertain. Estimate time and cost using observed runs or labeled assumptions.

Define what can be explored using candidate inputs and what needs accepted inputs. Parallel work can use a pinned candidate when its provisional status and rework risk are recorded. Acceptance dependencies form an acyclic graph. For a deployment, create the candidate package first, test that package, then accept the package and report against the same digest.

Maintain one current milestone plan. Preserve earlier plans and record why priority, scope, resources, dates, or acceptance changed. User-requested work keeps its explicit completion condition throughout rescheduling.

## Taking over an existing project

Inventory the actual outputs, existing decisions, in-flight work, and open findings. Check a bounded sample of claimed passes against raw evidence. Label historical claims as reported, verified, missing, or superseded. Record which exact versions are currently being consumed.

Produce a gap list and a retrofit plan. Preserve the existing development trail and live services. Introduce independent review of the management plan and the highest-risk missing evidence. Set any temporary dependency exception with a named owner, affected consumers, expiry, and compensating verification. Exceptions carry a visible unresolved status until closure and require authority appropriate to their impact.
