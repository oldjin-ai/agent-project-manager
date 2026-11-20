# Worked example

This is a fictional engagement illustrating the v0.2.0 workflow across two-plane sealing, risk-tiered review, and project takeover. Model identifiers come from an actual runtime host check (`list_subagent_models` or equivalent) when executing.

## New continuing software/data project (Standard/Strict tier)

The user wants a research portal that a small team can operate for six months without breaking existing services. Three agent seats, a callback subagent orchestrator, and an approved data API are available. Budget and production release credentials need user confirmation.

1. **Initiate with two-layer separation**: The PM recovers known requirements, inventories repo/tools, asks one compact question on budget and deployment credentials, and writes `CHARTER.md`, `MANAGEMENT-PLAN.md` (Standard/Strict tier), `PROJECT-PROFILE.md` (runtime model roster, pointers, write scopes), `RULEBOOK.md`, and project-specific role skills in 1–2 rounds with one independent bootstrap review.
2. **Coordinate purely**: In multi-agent mode, the PM main session does zero direct shell runs or code edits. It dispatches `backend`, `frontend`, and `host-runner` subagents sequentially/disjointly (`<= 1` writer per directory) using self-contained prompts and waits for callback completions.
3. **Seal once on submit (Two-Plane)**:
   - Backend finishes API endpoints; `host-runner` runs lint, schema validation, and targeted tests *first*.
   - Once pre-gates pass, `host-runner` seals `apps/backend/src` and `apps/backend/tests` **once** (`seal-scope` -> `v1/manifest.json`) excluding `collaboration/project-office`.
   - QA runs an independent review (`reviews/A09-r1.md`), binds to `manifest_sha256`, and finds one export filter omission (`major`). No reseal happens for the review file.
   - Backend patches the code, `host-runner` seals `v2/manifest.json`, and QA runs a **diff-based incremental re-review** (`reviews/A09-r2.md` -> `pass`, archiving `A09-r1.md` inside `review_history`).
4. **Atomic batch acceptance**: Backend (`A09@v2`) and Frontend (`A10@v1`) both stage in `review_passed`, pass the 8-class real-user walkthrough (`Invisible` through `Unresponsive`), and receive **one** consolidated user sign-off + atomic batch acceptance (`batches: [{"id": "B-APP", "artifacts": ["A09@v2", "A10@v1"]}]`).
5. **Report and hand over**: Every status update opens with `Accepted 6/8 artifacts · Real-User Usable=Yes · Current Blocker: awaiting production release credentials`. At milestone end, `STATUS.md` records `HEAD`, active batch state, and the exact 3-step startup sequence for the next PM session.

## Taking over an existing project

The inherited board claims 80 tasks are `done`, deliverables were repeatedly re-sealed every time a review markdown file changed, and three files sit in `signed` draft limbo.

1. The PM freezes new construction, runs a read-only runner to verify current `HEAD`, live tests, and raw evidence against claimed passes, and marks each claim as `verified`, `reported`, `missing`, or `superseded`.
2. The PM records legacy sealing/gate behavior under **Legacy Compatibility Notes** in `PROJECT-PROFILE.md` so active checks remain unbroken, immediately halts premature draft sign-offs, batches remaining fixes by module (`<= 1` writer per directory), and schedules migration to `seal-scope` Two-Plane Separation in the next milestone.
3. Unresolved blockers and missing user-path walkthroughs are closed in priority order, verified independently (`verifier != fixer`, `verifier != coordinator`), and indexed cleanly in the final delivery package.
