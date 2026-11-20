# Optional tooling (`init_project.py` & `artifact_control.py`)

The included utilities use Python 3.10+ and the standard library only. Run them with the environment's verified Python executable, inside the runner seat when operating in multi-agent coordinator mode.

## Initialize a project office

```bash
python scripts/init_project.py /project/collaboration/project-office --name "Example project"
```

The destination must not already exist. `init_project.py` scaffolds:
- `CHARTER.md`, `MANAGEMENT-PLAN.md`, `PROJECT-PROFILE.md`, `RULEBOOK.md`, `TEAM.md`, `MODEL-EVALUATION.md`, `MILESTONES.md`, `STATUS.md`, `DECISIONS.md`
- `roles/`, `tasks/`, `artifacts/`, `reviews/`, `evidence/`, `records/artifacts.json`

On any write error, initialization rolls back only files and empty directories it created.

## Seal deliverables (Two-Plane modes)

Choose either **snapshot payload mode** (`seal`) or **live repository scope mode** (`seal-scope`). Both write an immutable `manifest.json` outside the deliverables and refuse to overwrite an existing manifest (bump candidate version `v1 -> v2` if content changes).

### Option A: Live scope sealing (`seal-scope`, recommended for code & docs in-repo)

```bash
python scripts/artifact_control.py seal-scope \
  /project/collaboration/project-office/artifacts/A09/v1/manifest.json \
  --root /project \
  --scope apps/backend/src apps/backend/tests \
  --exclude-prefix collaboration/project-office
```

`seal-scope` seals **only** the declared `scope_paths`, automatically skipping `.git`, `__pycache__`, `node_modules`, `.pytest_cache`, `.mypy_cache`, `.ruff_cache`, `*.pyc`, `*.pyo`, and `*.tmp`, plus any `--exclude-prefix`. It rejects symlinks/reparse points and refuses self-referential scopes where `manifest.json` lies inside a scoped directory.

### Option B: Snapshot payload sealing (`seal`, recommended for self-contained bundles)

Place the snapshot files inside `<office>/artifacts/A01/v1/payload/` and run:

```bash
python scripts/artifact_control.py seal \
  /project/collaboration/project-office/artifacts/A01/v1/payload
```

This creates `<office>/artifacts/A01/v1/manifest.json` with SHA-256 and byte counts for every file inside `payload/`.

### Governance plane stays outside the manifest

Store `reviews/`, `evidence/`, `reviews/_history/`, and `records/` **outside** both `payload/` and `scope_paths`. Bind them to the candidate's `manifest_sha256` inside `records/artifacts.json`. Adding reviews, archiving older rounds, or collecting final sign-offs never alters `manifest.json` and requires **zero resealing**.

## Register results (`records/artifacts.json`)

All paths inside `records/artifacts.json` are forward-slash paths relative to `<office>` (except `scope_paths`, which are relative POSIX paths under `--project-root`).

```json
{
  "schema_version": 1,
  "project": "Example project",
  "coordinator_actor": "pm-coordinator",
  "milestones": [
    {"id": "M1", "required_artifacts": ["A09@v1", "A10@v1"]}
  ],
  "batches": [
    {"id": "B-APP", "artifacts": ["A09@v1", "A10@v1"]}
  ],
  "artifacts": [
    {
      "id": "A09",
      "version": "v1",
      "state": "accepted",
      "producer": {"actor": "backend-dev", "session": "build-001"},
      "scope_paths": ["apps/backend/src", "apps/backend/tests"],
      "manifest": "artifacts/A09/v1/manifest.json",
      "manifest_sha256": "DIGEST_OF_MANIFEST",
      "dependencies": [],
      "required_reviewers": ["qa"],
      "reviews": [{
        "actor": "qa",
        "session": "qa-001",
        "verdict": "pass",
        "manifest_sha256": "DIGEST_OF_MANIFEST",
        "record": "reviews/A09-round-02.md",
        "sha256": "DIGEST_OF_REVIEW"
      }],
      "review_history": [{
        "id": "R01",
        "actor": "qa",
        "verdict": "reject",
        "manifest_sha256": "DIGEST_OF_PRIOR_MANIFEST",
        "record": "reviews/_history/A09-round-01.md",
        "sha256": "DIGEST_OF_OLD_REVIEW"
      }],
      "required_verification": ["behavioral"],
      "verification": [{
        "kind": "behavioral",
        "status": "pass",
        "method": "Targeted and integration test suite",
        "environment": "Isolated test runner",
        "actor": "host-runner",
        "exit_code": 0,
        "manifest_sha256": "DIGEST_OF_MANIFEST",
        "record": "evidence/A09-tests.log",
        "sha256": "DIGEST_OF_EVIDENCE"
      }],
      "allowed_approvers": ["sponsor"],
      "approval": {
        "actor": "sponsor",
        "authority_ref": "CHARTER.md / Decision authority",
        "manifest_sha256": "DIGEST_OF_MANIFEST",
        "record": "records/B-APP-signoff.md",
        "sha256": "DIGEST_OF_SIGNOFF"
      },
      "defects": []
    }
  ]
}
```

Key supported governance checks:
- **`coordinator_actor`**: If set at registry or artifact level, blocks that actor from appearing in `reviews[].actor` or closed `defects[].verifier`.
- **`batches`**: Every batch linked to the checked milestone's closure must have **all** batch members `accepted` together (preventing half-batch unilateral acceptance).
- **`review_history`**: Optional append-only ledger verifying that archived rounds still exist and match their recorded SHA-256 without requiring contiguous round numbers.
- **Draft entries**: During `draft`, `in_review`, or `review_passed`, record compact entries (e.g., `{"id": "A09", "version": "v1", "state": "draft"}`); `check` keeps exit code 1 for incomplete milestones until every required artifact and batch peer is `accepted`.

## Check the delivery register

```bash
python scripts/artifact_control.py check \
  /project/collaboration/project-office/records/artifacts.json \
  --milestone M1 \
  --project-root /project
```

Omit `--milestone` to check all declared milestones; omit `--project-root` when the project root is `office.parent` (or only `payload` manifests are used). Any drift, unsealed extra deliverable file, self-referential manifest entry, coordinator self-review, half-accepted batch, missing review history, open `blocking`/`major` defect, or unverified `closed` defect fails with exit code 1.
