# Design sources and field provenance

Research date 2026-11-16. Links refer to the upstream material read during this extraction. Upstream branches evolve. These are design influences, with original implementation and wording in this repository.

| Source | Observed mechanism | Application here |
| --- | --- | --- |
| [BMAD Method](https://github.com/bmad-code-org/BMAD-METHOD), especially [planning inside an organization](https://github.com/bmad-code-org/BMAD-METHOD/blob/main/docs/plan/plan-inside-an-organization.md) | Role-owned planning documents, explicit signoff, durable context, process scaled to the work | Ownership, project-specific management plan, proportionate milestone gates |
| [MetaGPT](https://github.com/FoundationAgents/MetaGPT) | Product, architecture, project management, and engineering roles coordinated through SOPs | Explicit role outputs and handoffs across the project lifecycle |
| [Spec Kit](https://github.com/github/spec-kit) | Structured specifications, reusable templates, and customizable agent workflows | Requirement-to-deliverable traceability and reusable project templates |
| [Superpowers](https://github.com/obra/superpowers) | Composable skills, task planning, independent review, and verification before completion | Generated role skills, bounded tasks, and evidence-bearing review loops |
| [Deep Agents](https://github.com/langchain-ai/deepagents) | Planning, filesystem context, subagents, persistence, and configurable execution | Explicit checkpoints, execution-channel adaptation, and session recovery |
| [Agent Skills specification](https://github.com/agentskills/agentskills/blob/main/docs/specification.mdx) | A named skill directory with YAML frontmatter, instructions, and optional resources | Portable `SKILL.md` entrypoint with progressively loaded references |

The workflow also draws from an ongoing multi-model software/data project. Its observed practices included differentiated project roles, task cards, independent domain and technical review, decision logs, artifact inventories, content-bound evidence, and deployment checks. Its management playbook was still under independent review during extraction. The artifact register then recorded zero formally accepted artifacts out of fourteen, alongside functioning engineering outputs and unfinished formalization.

That field experience informed explicit PM accountability, review of the management system itself, current model availability checks, a complete delivery index, and separate evidence for substantive user outcomes. The reusable skill generalizes these mechanisms to the host environment and project domain. The public package includes generalized templates and original tools. Private project material remains in its owning storage.

Published validation distinguishes local tool checks, isolated agent trials, host compatibility, and field outcomes. Future case reports should identify the task, environment, observation period, artifacts, failures, and completion evidence.
