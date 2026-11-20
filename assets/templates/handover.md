# Current handover

Project {{PROJECT_NAME}}

```text
Accepted 0/0 artifacts · Real-User Usable=No · Current Blocker: initialization pending
```

## Snapshot and pointers

- Current `HEAD` revision and clean/dirty workspace summary (note any pre-existing untracked paths)
- Canonical pointers: `PROJECT-PROFILE.md`, `RULEBOOK.md`, `records/artifacts.json`

## Accepted outcomes, batches, and current candidates

List milestone state, batch staging (`review_passed` vs. `accepted`), and artifact/version/`manifest_sha256` with acceptance references.

## In-flight work and pending handoffs

List active subagent/task/run IDs, executing model identities, write scopes, last checkpoints, and manual prompts awaiting user return.

## Open findings, blockers, and redlines

List unresolved `blocking`/`major` findings, `429`/quota freezes, user-reserved decisions, and explicit redlines (what the incoming PM must NOT touch or promote).

## Next 3-step startup and ready actions

1. Load orchestrator skill + `agent-project-manager`.
2. Run runtime model discovery (`list_subagent_models` or host equivalent) and verify against `PROJECT-PROFILE.md`.
3. Read `PROJECT-PROFILE.md`, `STATUS.md`, and `records/artifacts.json`, then execute ordered ready tasks below.
