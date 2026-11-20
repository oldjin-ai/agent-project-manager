# Harness adapters and runtime traps

This skill runs across different agent hosts (callback-capable subagent orchestrators, task-board ledgers, CLI wrappers, and sandboxed runners). Map the workflow onto your host's actual capabilities instead of assuming uniform tool schemas.

## 1. Execution channel priority

1. **Callback-capable subagent (default, non-blocking yield)**: Prefer delegation primitives that return final output, exit state, and artifacts directly to the coordinator session when finished (`run_in_background: true`). **Never call blocking wait tools such as `wait_agent` after launching background subagents** — report what was dispatched immediately and end the turn so the host wakes the coordinator on completion instead of freezing the UI.
2. **Task-board / async ledger (`create` + `record-external-outcome`)**: When the host exposes a task board whose runner starts an isolated, non-callback session, separate **execution** from **bookkeeping**:
   - Create a board card with the intended model/reasoning fields to reserve the slot and track dependencies.
   - Execute the work through the callback subagent channel (or authorized CLI runner).
   - Close the board card using `record-external-outcome` (or equivalent structured completion action) attaching the **actual** executing identity, model, command output path, exit code, and SHA-256 digest.
   - Never use a bare "move to done" action that skips verification evidence.
3. **Disconnected runner / cron / explicit handover**: Reserve disconnected board runners for scheduled recurring jobs (cron) or explicitly requested cross-session PM handovers.
4. **Manual handoff channel**: When a required specialist or reviewer cannot be invoked programmatically (quota policy, sandbox boundary, or missing provider route), generate a self-contained dispatch prompt, pause dependent work cleanly, and ingest the returned raw report via `record-external-outcome`.

## 2. Runtime discovery and parameter hygiene

- **Discover before dispatching**: Call the host's model/agent discovery tool (such as `list_subagent_models`) at the start of every new or resumed PM session. Record the exact provider ID, model slug, and supported reasoning levels in `PROJECT-PROFILE.md` and `TEAM.md`.
- **Keep parameter schemas exact**: Different tools in the same host often enforce incompatible parameter shapes (for example, one tool requiring a combined `"<provider>/<model>"` string with camelCase `reasoningEffort`, while another requires split `"provider"` and `"model"` fields with snake_case `reasoning_effort`). Never guess; copy verified tool schemas into the host section of `PROJECT-PROFILE.md`.
- **Honor model-specific reasoning constraints**: Some models reject `"medium"` and accept only `"max"` or `"high"`, while orchestrator wrapper models reject any `--effort` flag altogether (requiring the flag to be omitted via an explicit empty environment variable rather than passing `--effort ""`). Document exact working invocations after a single bounded probe.
- **Prevent ledger drift**: Always bind the model and reasoning setting at task creation/dispatch. Never overwrite a task card's `model` field during or after execution to disguise which model actually ran.

## 3. Stalled runs, timeouts, and environment traps

- **Long-suite timeout budgeting**: Measure actual full-suite runtimes (for example, 30+ minute integration suites) and set background job timeouts to `1.5x–2x` observed duration with unbuffered output (`PYTHONUNBUFFERED=1` or equivalent). Do not terminate valid slow suites prematurely.
- **Stalled-run kill-switch**: If an async or board-run task produces zero workspace, artifact, or log changes on disk past a generous threshold (default: **90 minutes**), settle/cancel the stalled run, preserve diagnostics, and split the task into smaller verifiable slices.
- **Sandbox home / log-path isolation**: On Windows and restricted sandboxes, CLI sub-agents that write auth tokens or logs under the user's home directory may falsely report "not logged in" or hang. Redirect CLI `HOME`/`USERPROFILE` and `--log-file` paths into an ignored in-workspace scratch directory, and quote model names containing spaces.
- **Cross-platform clean archive trap**: On Windows, `git archive` (via `bsdtar`) can fail with empty pathname errors on repositories containing non-ASCII paths. Use `zip` or `git checkout-index` when exporting clean source snapshots on Windows.
- **No symlinks or directory junctions**: Never create symlinks or NTFS directory junctions (`mklink /j`) inside or across workspaces; recursive cleanup or tooling checks can traverse or reject them. Always use real copies or configured paths.
