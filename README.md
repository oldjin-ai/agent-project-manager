# Agent Project Manager

![Agent project manager](assets/illustrations/hero.png)

[简体中文](README.zh-CN.md) · [Skill instructions](SKILL.md) · [Worked example](examples/continuing-project.md)

An open-source skill (`v0.2.1`) for running substantial, continuing projects with an accountable pure-coordinator PM, a purpose-built agent team, zero-reseal artifact control, and reviewed milestone delivery.

The PM establishes the mandate and risk tier, verifies callable models at runtime, keeps mutable bindings in `PROJECT-PROFILE.md`, generates project-specific role skills, coordinates bounded parallel execution without self-QA, and delivers an inspectable handover package across sessions.

## What is new in v0.2.x

- **Non-blocking coordinator & minimal user gates (`v0.2.1`)**: Dispatches background subagents (`run_in_background: true`) and yields immediately without `wait_agent` UI hangs; advances routine execution autonomously and pauses the user only on a strict 4-class gate shortlist.
- **Two-plane sealing (`seal-scope` + external governance)**: Deliverable payloads/scopes never hash reviews, archived rounds, or sign-offs. Adding reviews or approvals requires **zero resealing**.
- **Pure coordinator iron law**: Multi-agent PM sessions enforce zero direct shell execution, zero direct edits to deliverables, zero self-QA, and bounded inspection reads.
- **Risk-tiered governance (`Light` / `Standard` / `Strict`)**: Proportional process rigor with 1–2 round bootstrap checks, single append-only `RULEBOOK.md`, and `PROJECT-PROFILE.md` separation.
- **Atomic batch acceptance & seal-once-on-submit**: Coupled deliverables stage in `review_passed` and receive one consolidated sign-off + atomic batch acceptance, ending repeated premature draft sign-offs.
- **Streamlined review & quota resilience**: Mechanical pre-gates before spending model tokens, diff-based incremental re-reviews, tiered reviewer routing, `429` queue freezes without seat spoofing, and 2-round anti-loop escalation.
- **Real-user substantive bar & harness adapters**: 8-class real-user completeness rubric (`Invisible` through `Unresponsive`), fixed 3-line executive status header, and cross-host runtime adapter guidance.

## Install

Clone the repository into a skill directory supported by your host. Choose an unused destination. For Codex (`~/.codex/skills`), run:

```bash
git clone https://github.com/oldjin-ai/agent-project-manager.git ~/.codex/skills/agent-project-manager
```

For DeepSeek Harness (`~/.dsh/skills`) or any other Agent Skills host, place a real copy of this directory (never a symlink or junction) in its configured skill location, or pass the path to `SKILL.md` explicitly.

The instruction layer uses Markdown and YAML. The optional tools require Python 3.10+ using the standard library only. Model availability, callback delegation, and execution permissions come from your host.

## Use

```text
Use $agent-project-manager to run this project through milestone delivery.
Outcome: a research portal that our team can operate for the next six months.
Available resources: this repository, three agent seats, and the approved data API.
Constraints: preserve existing services and stay within the stated budget.
Start with the project charter, PROJECT-PROFILE.md, runtime model inventory,
team role skills, and a risk-tiered management plan. Continue within my
authorization and ask about consequential missing inputs.
```

For a project already underway:

```text
Use $agent-project-manager to take over this continuing project.
Verify current progress against raw evidence, preserve existing services and
compatible legacy gates, adopt two-plane sealing where supported, and close
delivery gaps milestone by milestone.
```

![Purpose-built agent team](assets/illustrations/team.png)

## Optional tools

Run the scripts with your environment's verified Python executable (`python` below is a portable placeholder).

```bash
python scripts/init_project.py /path/to/project/collaboration/project-office --name "Research portal"
python scripts/artifact_control.py seal-scope /path/to/project/collaboration/project-office/artifacts/A09/v1/manifest.json --root /path/to/project --scope apps/backend/src apps/backend/tests --exclude-prefix collaboration/project-office
python scripts/artifact_control.py seal /path/to/project/collaboration/project-office/artifacts/A01/v1/payload
python scripts/artifact_control.py check /path/to/project/collaboration/project-office/records/artifacts.json --project-root /path/to/project
```

`init_project.py` creates draft templates including `PROJECT-PROFILE.md` and `RULEBOOK.md`. `artifact_control.py check` enforces deliverable integrity, two-plane external evidence bindings, coordinator purity (`coordinator_actor`), append-only `review_history`, atomic `batches`, and independent defect closure. See [tooling and register format](references/tooling.md).

![Reviewed milestone delivery](assets/illustrations/delivery.png)

## Maturity

Version 0.2.1 builds on v0.2.0's field hardening from multi-model software/data delivery runs, adding non-blocking turn yields and a 4-class user-gate shortlist alongside two-plane sealing, atomic batch acceptance, and pure coordinator enforcement. See [validation](docs/validation.md) for current automated check scope and observed limits.

The host supplies scheduling, execution channels, storage, and permissions. The optional checker verifies structural consistency and cryptographic bindings; authentic review and real-user acceptance remain the responsibility of designated reviewers and human approvers.

## Design sources

Research considered BMAD Method, MetaGPT, Spec Kit, Superpowers, Deep Agents, and the Agent Skills specification, combined with field provenance documented in [design sources](references/design-sources.md).

## Contribute

Open an issue with a concrete project scenario, expected behavior, observed result, and scrubbed evidence. Before submitting changes, run:

```bash
python -m unittest discover -s tests -v
```

MIT licensed. Copyright 2026 oldjin-ai.
