# Project profile

Project name {{PROJECT_NAME}}

## Risk tier and operating mode

- Risk tier: `light` | `standard` | `strict`
- Execution mode: `multi-agent` | `single-session`
- Coordinator actor ID: `pm-coordinator`

## Canonical runtime pointers

Record authoritative version/status pointers read at runtime (never duplicate mutable counts or digests inside role skills).

| Domain | Canonical pointer path | Authority |
| --- | --- | --- |
| Project office register | `records/artifacts.json` | PM / designated approver |

## Active role and model routing

Keep this table synchronized with `TEAM.md` and current runtime checks (`list_subagent_models` or host capability probes).

| Role | Harness / channel | Provider & model | Reasoning / flags | Fallback or freeze rule |
| --- | --- | --- | --- | --- |

## Write-scope ownership and redlines

- Record per-role allowed write paths and forbidden paths.
- Shared registers and generated manifests have one designated writer.
- Never hardcode runtime counts or version tags into UI/API code.
- Never create symlinks or directory junctions inside or outside the project.

## Domain and legacy compatibility notes

Record domain-specific verification tools, long-running suite timeout budgets, known waived checks, or legacy rules queued for retirement.
