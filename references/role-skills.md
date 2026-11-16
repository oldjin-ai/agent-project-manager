# Generate project-specific role skills

Use `assets/templates/role-skill.md` to create one skill per occupied role, including PM. Store them in the project's permitted location, for example `<office>/roles/<project-role-name>/SKILL.md`. Choose a lowercase alphanumeric-and-hyphen name of at most 64 characters and use that exact name for both the directory and frontmatter `name`. Record the skill revision or digest in TEAM and task dispatches. Discoverability varies by host. Pass the file path and relevant instructions explicitly to each assigned session.

Resolve the template into concrete project instructions. State the role's objective, authoritative inputs, outputs, acceptance evidence, write paths, decision limits, collaborators, escalation, and completion receipt. Use stable IDs and references to current records. Load only the role's necessary context. Give domain specialists the evidence and calculation conventions their work requires.

## Role-specific obligations

| Role | Tailor these obligations |
| --- | --- |
| PM | Charter and authority, team selection, dependency graph, dispatch, resource limits, artifact inventory, milestone status, recovery, final handover |
| Product owner | Requirement IDs, user paths, domain semantics, scope decisions, acceptance scenarios, change impact |
| Architect | Component and data boundaries, interfaces, alternatives, feasibility, failure/recovery design, technical decisions |
| Builder | Pinned inputs, normal entry points, implementation scope, output snapshot, relevant self-checks, change summary |
| Domain expert | Primary-source verification, provenance, units, assumptions, uncertainty, reproducibility |
| QA/reviewer | Independent session, artifact binding, adversarial cases, actual user-path verification, findings and retest evidence |
| Operations | Target environment, packaging, deployment authorization, smoke checks, observability, rollback, operational handover |

Add roles for the project's actual work. For research, useful roles may include investigator, domain reviewer, analyst, and editor. A model occupies the role with its own tools and capability limits. Keep role instructions aligned with the real channel.

## PM boundaries

The PM owns coordination and delivery accounting. They route substantive judgments to the designated role, resolve authorized routine choices, and escalate reserved decisions with a concrete evidence package. They preserve review findings and keep acceptance conditions intact. The PM's management plan, role skill, and substantive authored outputs receive independent review. The PM records who accepted a risk and the scope of that decision.

## Review role skills before broad use

Check conflicts, unreachable responsibilities, overlapping write ownership, accidental release authority, and missing review obligations. Have a separate reviewer inspect the PM skill and management plan together. Update affected dispatches when role constraints change. Preserve earlier revisions for interpreting historical work.
