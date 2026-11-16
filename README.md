# Agent Project Manager

[简体中文](README.zh-CN.md) · [Skill instructions](SKILL.md) · [Worked example](examples/continuing-project.md)

An open-source skill for running substantial, continuing projects with an accountable agent PM, a purpose-built team, and reviewed milestone deliverables.

The PM clarifies the mandate, evaluates available models, writes project-specific role skills, coordinates execution, preserves outputs and review history, and assembles a traceable delivery package. Project records support handover across sessions and changes in the team.

## What it covers

- Project initiation with dependencies, resources, budget, authority, and measurable acceptance.
- Current model research and bounded project-relevant evaluation, including the PM assignment.
- A tailored `SKILL.md` for each occupied role and independent review of the PM's management plan.
- Milestone dependencies, task dispatch, monitoring, recovery, and in-flight project takeover.
- Version-bound artifacts, independent review, correction verification, acceptance, and final handover.
- Optional Python standard-library tools for scaffolding, payload sealing, and structural delivery checks.

## Install

Clone the repository into a skill directory supported by your host. Choose an unused destination. For a Codex installation that uses `~/.codex/skills`, an example is

```bash
git clone https://github.com/oldjin-ai/agent-project-manager.git ~/.codex/skills/agent-project-manager
```

For another Agent Skills host, place this directory in its configured skill location. If automatic discovery is unavailable, give the agent the path to `SKILL.md` and ask it to follow the skill. Confirm local host conventions before choosing a project-level skill path.

The instruction layer uses Markdown and YAML. The optional tools require Python 3.10+ and have no third-party dependencies. The environment supplies file access, an execution/delegation channel, and any authorized research tools. Model availability and execution permissions come from your host.

## Use

```text
Use $agent-project-manager to run this project through milestone delivery.
Outcome: a research portal that our team can operate for the next six months.
Available resources: this repository, three agent seats, and the approved data API.
Constraints: preserve existing services and stay within the stated budget.
Start with the project charter, resource/model assessment, team role skills,
and a management plan that receives independent review. Continue within my
authorization and ask about consequential missing inputs.
```

For a project already underway

```text
Use $agent-project-manager to take over this continuing project.
Verify current progress, inventory artifacts and review evidence, preserve
existing work, and close the most important delivery gaps milestone by milestone.
```

Generated role skills belong to the managed project. The PM supplies each role's instructions through the actual host channel and records the assigned model/session. A manual dispatch prompt supports environments where automatic delegation is unavailable.

## Optional tools

Run the scripts with your environment's verified Python executable. These portable examples assume it is available as `python`.

```bash
python scripts/init_project.py /path/to/project/collaboration/project-office --name "Research portal"
python scripts/artifact_control.py seal /path/to/project/collaboration/project-office/artifacts/A01/v1/payload
python scripts/artifact_control.py check /path/to/project/collaboration/project-office/records/artifacts.json
```

The initializer creates draft records. A delivery check fails until the declared required artifacts have sufficient records and verified file bindings. See [tooling and register format](references/tooling.md).

## Maturity

Version 0.1.0 is an initial reusable extraction of an actively evolving field workflow, with local tool tests and independent forward-testing documented in [validation](docs/validation.md). Its originating project was still completing management-plan review and artifact formalization when this extraction began. Cross-host operation and long-duration effectiveness need further field evidence.

The skill instructs a host agent. The host provides scheduling, execution, persistent storage, permissions, and session lifecycle. The optional checker verifies record consistency and bytes. Review authenticity, substantive quality, and business acceptance require the designated people or agent sessions and their recorded evidence.

## Design sources

The research considered BMAD Method, MetaGPT, Spec Kit, Superpowers, Deep Agents, and the Agent Skills format. The [source notes](references/design-sources.md) explain the specific design influences and retrieval date. This repository contains original instructions and utilities.

## Contribute

Open an issue with a concrete project scenario, expected behavior, observed result, and scrubbed evidence. For a change, include the affected workflow and relevant checks. Preserve user intent, explicit authority, evidence quality, and an appropriately sized process.

```bash
python -m unittest discover -s tests -v
```

MIT licensed. Copyright 2026 oldjin-ai.
