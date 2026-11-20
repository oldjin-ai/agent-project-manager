# Team formation and model evaluation

## Start with capabilities and runtime seats

Map deliverables to required capabilities: product/domain judgment, architecture, domain research, implementation, verification/QA, operations, and coordination. Combine roles on small or `Light`/`Standard` projects while preserving independent review for critical outputs.

Inventory the host's actual callable agents, subagent providers, CLI wrappers, and tools **at runtime** (e.g., via `list_subagent_models` or equivalent host discovery). Record:

- Exact provider and model identifiers as exposed by the harness
- Exact parameter schema required per tool (`provider` + `model` split vs. combined `"provider/model"`, `reasoning_effort` vs. `reasoningEffort`, or flags that must be omitted)
- Reasoning settings, sandbox restrictions, concurrency limits, and quota rules
- Verified availability date and tested probe status

If the host hides model metadata, record the exposed channel and mark hidden fields `unavailable from host`. Never invent provider names or guess CLI model slugs.

## Research and bounded probing

Use `assets/templates/model-evaluation.md`. Consult official model documentation, release notes, and relevant evaluations for available candidates, then run a short representative probe from the real project domain when authorized:

| Role | What to verify |
| --- | --- |
| PM coordinator | Dependency ordering, strict tool-schema adherence, no-shell discipline, recovery planning |
| Product / domain | Ambiguity detection, source fidelity, real-user path & UX judgment |
| Architect | Interface consistency, failure/recovery design, concise technical rulings |
| Builder | Repository edits within write scope, self-check execution, regression discipline |
| QA / reviewer | Detecting seeded defects, requirement traceability, independent reproduction |
| Operations | Packaging, environment/path hygiene, rollback & smoke verification |

Save the probe prompt, settings, raw result, observed defects, and elapsed duration inside the office or ignored scratch storage. Reassess assignments at milestone boundaries or after repeated role-specific failures.

## Tiered reviewer routing and quota resilience

Treat high-rigor and scarce reviewers as constrained capacity rather than running heavy multi-seat reviews on every minor change:

- **Final & high-risk gates**: Reserve the strongest independent QA / domain seats for milestone-final verification, data/release pointer changes, security/auth changes, and deployment acceptance.
- **Routine tasks & defect retests**: Route routine defect closures and non-A-level code changes to **mechanical gate evidence + an independent non-author reviewer** (an uninvolved peer builder or architect), keeping `reviewer != producer` and `verifier != fixer`.
- **Fallback rule on quota exhaustion (`429`) or provider outage**:
  1. Inspect the stated reset window and preserve the exact error.
  2. Switch only to a **pre-qualified authorized fallback** of comparable rigor recorded in `PROJECT-PROFILE.md` / `TEAM.md`.
  3. **Never spoof a required reviewer seat** by disguising another model under that seat's identity, and **never let the PM self-verify or self-sign** to clear a blocked queue.
  4. When no qualified fallback is available, freeze only the blocked acceptance queue, log the block, and keep unrelated ready work moving.

## Anti-ledger-drift rule

Bind the assigned `model` and reasoning level at task creation and subagent dispatch. If a subagent runs under a fallback or different actual model than planned, record the **true executing model and identity** in the completion receipt and board ledger (`record-external-outcome`). Never call an update tool during or after execution to retroactively rewrite a card's `model` field to cover up a mismatch.
