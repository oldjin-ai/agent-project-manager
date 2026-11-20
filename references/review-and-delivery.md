# Review, two-plane sealing, and delivery

## Two-plane sealing (zero reseal storms)

Never seal governance records inside the deliverable manifest. Mixing deliverables with `REVIEW-*.md`, `_history/`, or `SIGNOFF` files creates self-referential reseal loops where every new review invalidates the tested manifest hash.

1. **Content Plane (deliverables only)**:
   - Seal **deliverable files only** via either an immutable `payload/` snapshot (`artifact_control.py seal`) or live repository `scope_paths` (`artifact_control.py seal-scope`, automatically excluding `.git`, `__pycache__`, `node_modules`, `*.tmp`, and the project-office governance directory).
   - **Seal-Once-on-Submit**: Iterate freely during `draft` with **zero seals**. Run mechanical pre-checks first, then seal **once** at `draft -> in_review`. Only bump version (`v1 -> v2`) and re-seal when deliverable content actually changes.
   - **Single canonical digest**: Always bind reviews, verification runs, defects, and approvals to the candidate's full `manifest_sha256` (never a single-file proxy hash like an entrypoint or README).
2. **Governance / Evidence Plane (outside the deliverable manifest)**:
   - Reviews, verification logs, defect closures, append-only `review_history`, and approvals live inside the project office (e.g., `reviews/`, `evidence/`, `records/`), individually SHA-256 bound downward to the candidate's `manifest_sha256`.
   - Adding new review rounds, archiving historical rounds, recording retests, or collecting final sign-offs requires **zero deliverable resealing**.

## Artifact lifecycle and atomic batch acceptance

Use `missing -> draft -> in_review -> review_passed -> accepted -> superseded` (with `rework` on rejection and `stale` when scoped deliverables or upstream accepted dependencies drift).

- **No premature draft sign-offs**: Do **not** collect human sign-off on an incomplete draft (`signed=true` while still `draft`), which causes repetitive re-signing whenever downstream batch peers change. Stage passing candidates in `review_passed`.
- **Atomic batch acceptance**: Group tightly coupled deliverables (e.g., backend + frontend, or acceptance report + deployment package) into named `batches` in `records/artifacts.json`. Collect **one** consolidated human approval and move the entire batch to `accepted` atomically once every batch member passes review and verification.

## Streamlined independent review protocol

1. **Mechanical pre-gate (zero model tokens wasted)**: Run lint, formatting, schema validation, link/heading consistency, digest checks, and targeted automated tests *before* dispatching any model reviewer. Reject failed pre-gates immediately back to the owner.
2. **Append-only review history**: Record every review round in `review_history` with explicit file path and SHA-256 (`reviews/_history/...`). Never delete or overwrite historical rounds, and never require brittle contiguous round numbering (`01, 02, 03...`) that breaks when rounds are cancelled or split.
3. **Diff-based incremental re-review**: Round 2+ re-reviews inspect only the changeset/diff since the prior sealed candidate, unresolved blocking/major findings, and affected regression areas instead of re-reading the entire deliverable from scratch.
4. **Convergence cap & full-review fallback**: After two consecutive incremental rounds introduce zero new `blocking` or `major` findings, stop full-document re-reads and settle minor polish. **Mandatory fallback**: immediately return to full multi-seat review if any blocking regression escapes to downstream gates or if a change alters cross-layer contracts or user-facing product shape.
5. **Single living rulebook (`RULEBOOK.md`)**: Record every cross-artifact technical, metric, or acceptance ruling in `RULEBOOK.md` (append-only, superseding old entries explicitly) so agents check one authoritative source.

## Severity policy and defect closure

Restrict finding severity to `blocking`, `major`, and `minor`:

- **Zero-waiver rule**: Any open `blocking` finding yields `reject`. Any open `major` finding forbids `accepted` (at best `conditional` / `rework`, blocking release). Cluster threshold (`>= 3` unresolved `major` findings on the same scope) triggers bulk rejection and a single consolidated fix card instead of piecemeal patching.
- **Independent defect closure**: Every finding is tracked in an explicit register with `fixer` and `designated_verifier`. Closing a defect requires `verifier != fixer`, `verifier != coordinator_actor`, and raw retest evidence bound to the current `manifest_sha256`.

## Real-user substantive completeness bar

Unit tests and `HTTP 200` responses do not guarantee user readiness. Audit user-facing milestones against eight blocking failure classes:

| Class | Failure | Examples |
| --- | --- | --- |
| `Invisible` | Feature/data exists in backend or code but users cannot reach or see it | Unwired routes, collapsed/hidden required panels, broken role visibility |
| `Unusable` | Entry loads but user actions fail or do nothing | Unclickable rows, dead search/filters, disabled actions with no explanation |
| `Incomplete` | Data is missing, stale beyond calendar SLA, or masked without disclosure | Stale feeds passing self-referential checks, unrendered API warning metadata |
| `Broken-Loop` | End-to-end state breaks across actions, roles, or refreshes | Writes lost on reload, broken cross-page drilldowns, cross-role permission leaks |
| `Inaccurate` | Displayed values, units, benchmarks, or rankings are wrong | Double-scaled percentages, wrong benchmark base, currency symbols on indices |
| `Leaked-Internals` | Raw internal tokens, task IDs, debug text, or API paths appear in UI | Stack internals, raw enum keys, deprecated tags, or demo switchers in prod |
| `Layout-Broken` | Visual hierarchy, contrast, or responsive viewports break usability | Invisible active tabs, horizontal overflow, clipped mobile/desktop controls |
| `Unresponsive` | Slow paths or stuck loading indicators block real usage | Persistent loading spinners, cold-start timeouts causing false errors |

### Honest empty and degraded state boundary

- Only objective case-level emptiness (new item with insufficient history, halted/filtered match, empty user collection, explicitly approved unimplemented method) may render an empty state — never use empty-state copy to hide system-wide outages or stale pipelines.
- Every valid empty/degraded state must show: (1) an explicit placeholder such as `—` (never `null`, `undefined`, `NaN`, or fake `0`), (2) a clear user-facing reason in the target language, (3) an authoritative timestamp/source anchor or next action, and (4) core sample coverage where data is expected.

## Final handover index

Deliver a navigable handover index linking:
- Requirement-to-artifact-to-verification traceability matrix
- Accepted artifact versions (`manifest_sha256`), batch approvals, and canonical pointers
- Preserved `review_history`, defect closures, and `RULEBOOK.md` rulings
- Known accepted minor limitations and operational/rollback runbooks
- Verification that all local references resolve and packaged contents match tested digests
