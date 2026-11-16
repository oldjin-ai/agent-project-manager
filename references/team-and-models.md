# Team formation and model evaluation

## Start with capabilities and available seats

Map the deliverables to required work such as product judgment, architecture, domain research, implementation, numerical reasoning, visual inspection, verification, operations, and coordination. Add specialists where their contribution addresses a real project need. A role is a responsibility with outputs and decision boundaries. The team can combine responsibilities according to capacity and risk.

Inventory the host's actual callable agents and tools. Record model identifiers exactly as exposed by the provider or harness. Record the ability to choose models, reasoning settings, tool permissions, session isolation, concurrent seats, quota, and manual handoff channels. Verify availability using a bounded probe where authorized. Keep provider claims and observed availability in separate fields.

When the host hides model identity or settings, record the exposed session/channel and mark the hidden fields `unavailable from host`. Preserve that uncertainty until metadata becomes observable. The available session can still complete authorized preparatory work.

## Research current strengths

Search official model documentation, model cards, release notes, and primary evaluation reports for the candidate models that are actually available. Record source URL, retrieval date, model/version, task relevance, methodology, and uncertainty. Inspect recent relevant primary evaluations where they add evidence. Vendor self-reports and benchmark aggregates require task-level judgment.

Use `assets/templates/model-evaluation.md`. Evaluate dimensions relevant to the role.

| Role | Candidate evidence |
| --- | --- |
| PM | Dependency reasoning, long-context instruction fidelity, uncertainty reporting, recovery planning |
| Product/domain | Requirement ambiguity, domain source fidelity, usable acceptance criteria |
| Architect | Tradeoffs, interface consistency, failure analysis, implementation feasibility |
| Builder | Repository-specific implementation, tool reliability, regression handling |
| QA/reviewer | Detecting a seeded defect, requirement coverage, independent reproduction |
| Operations | Deployment/recovery reasoning, environment diagnosis, permission awareness |
| Design | Visual judgment, accessibility, interaction completeness in the required modality |

Choose a short representative probe from the real project's domain. Give candidates comparable inputs and predeclared evaluation criteria. Save the prompt, input digest, exact settings, output, evaluator, observed defects, elapsed time, and reported usage when available. Protect production state and use authorized resources. Keep the probe bounded to the budget agreed for team formation.

If paid calls, tools, or model switching are unavailable, complete a documentation-backed provisional assignment with explicit uncertainty. Reassess after the first real task. Public documentation alone supports a hypothesis about fit.

## Assign and maintain

Record the chosen model/harness for each role, the observed reasons, limitations, constraints, and qualified fallback order. Include the PM in this evaluation. Use empirical task results to revise the assignments at milestone boundaries or after repeated role-specific failures. A fallback needs the capabilities and permissions required for that role.

For 429, authentication failures, missing tools, or unavailable reasoning settings, record the exact failure and affected work. Probe a qualified alternative once when authorized, then update the assignment and dispatch record. Reconcile unfinished calls before replacement. Keep review criteria and reviewer independence across replacements.

A review session receives the requirement, exact artifact, relevant raw inputs, and its role skill. Record the producer and reviewer execution identities. Multiple model vendors can diversify failure modes when available. Assess independence from the actual session and evidence handling.

## Execution channels

Use native subagents, a connected orchestrator, or a complete manual handoff prompt according to available authorization and host capabilities. Dispatch through one canonical channel. Supply role instructions explicitly if the host cannot discover project-local skills. Save acknowledgement or run ID and result location. If only one execution session is available, label self-checks accurately and arrange an independent review channel for gates that require it.
