# Design sources and field provenance

Research date 2026-11-16 (v0.1.0), updated 2026-11-20 (v0.2.0). Links refer to upstream material studied during extraction. Repository instructions and utilities are original implementations.

| Source | Observed mechanism | Application here |
| --- | --- | --- |
| [BMAD Method](https://github.com/bmad-code-org/BMAD-METHOD), especially [planning inside an organization](https://github.com/bmad-code-org/BMAD-METHOD/blob/main/docs/plan/plan-inside-an-organization.md) | Role-owned planning documents, explicit signoff, durable context, process scaled to the work | Ownership, risk-tiered governance sizing, proportionate milestone gates |
| [MetaGPT](https://github.com/FoundationAgents/MetaGPT) | Product, architecture, project management, and engineering roles coordinated through SOPs | Explicit role outputs, pure coordinator separation, and handoff contracts |
| [Spec Kit](https://github.com/github/spec-kit) | Structured specifications, reusable templates, and customizable agent workflows | Requirement-to-deliverable traceability and reusable project templates |
| [Superpowers](https://github.com/obra/superpowers) | Composable skills, task planning, independent review, and verification before completion | Generated role skills, bounded tasks, and evidence-bearing review loops |
| [Deep Agents](https://github.com/langchain-ai/deepagents) | Planning, filesystem context, subagents, persistence, and configurable execution | Explicit checkpoints, harness adapters, and cross-session recovery |
| [Agent Skills specification](https://github.com/agentskills/agentskills/blob/main/docs/specification.mdx) | Named skill directory with YAML frontmatter, instructions, and optional resources | Portable `SKILL.md` entrypoint with progressively loaded references |

## Field evolution (v0.1.0 -> v0.2.0)

Subsequent multi-day live execution across heterogeneous agent harnesses surfaced six concrete failure modes that shaped v0.2.0:

1. **Reseal storms**: Including `REVIEW-*.md` and archived history inside deliverable manifests forced repeated re-sealing and re-signing of unchanged code/docs after every review pass. v0.2.0 introduces **Two-Plane Sealing** (`seal-scope` + external governance plane) and **Seal-Once-on-Submit**.
2. **Premature draft sign-offs**: Collecting human sign-offs while coupled peers remained in draft forced repeated re-signing. v0.2.0 introduces `review_passed` staging and **atomic batch acceptance** (`batches`).
3. **Coordinator drift & ledger mismatch**: PM sessions running direct shell/edits, polling disconnected board runners, or retroactively editing card models corrupted audit trails. v0.2.0 codifies the **Pure Coordinator Iron Law**, callback subagent priority, and `record-external-outcome` ledger discipline.
4. **Governance over-engineering**: Spending 10–20 review rounds polishing playbooks and enforcing rigid contiguous round numbers slowed delivery. v0.2.0 adds **Risk Tiers (`Light`/`Standard`/`Strict`)**, `PROJECT-PROFILE.md` separation, mechanical pre-gates, diff-based incremental re-review, and append-only `review_history`.
5. **Quota bottlenecks**: Routing every minor defect through a scarce top-tier reviewer stalled delivery on rate limits. v0.2.0 adds **tiered reviewer routing**, non-spoofing `429` freeze rules, and explicit harness CLI traps.
6. **Shallow pass illusion**: `HTTP 200` and isolated unit tests still left empty/broken user flows. v0.2.0 embeds the **8-Class Real-User Completeness Rubric** and fixed **3-line executive status header**.
