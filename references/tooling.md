# Optional tooling

The tools use Python 3.10+ and its standard library. Run with the verified interpreter for the environment. Choose the office path under the project's directory rules. The tools implement a compact local-file record format. Existing trackers or durable object stores can use their own format and equivalent bindings.

## Initialize

```bash
python scripts/init_project.py /project/collaboration/project-office --name "Example project"
```

The destination must be new. The initializer creates draft charter, plan, team/model/milestone records, status, decisions, and empty storage directories. It leaves substantive role skills and project decisions to the PM. Resolve the templates according to the actual project.

## Seal a candidate

Place a complete artifact snapshot inside `<office>/artifacts/A01/v1/payload/`. Then run

```bash
python scripts/artifact_control.py seal /project/collaboration/project-office/artifacts/A01/v1/payload
```

This creates `artifacts/A01/v1/manifest.json` with every payload file's SHA-256 and byte count, and prints its SHA-256. It refuses an existing manifest, empty payload, and linked/reparse entries. Give the payload one writer and stop its edits while sealing, testing, and reviewing. For changes, create a new version and preserve the previous candidate and its reports.

Reviews, test logs, and acceptance records live outside the payload. They bind to the manifest digest. This keeps the candidate content stable while review records accumulate. Put every substantive artifact input in its payload or declare its accepted artifact dependency. Include code/data/configuration bindings in verification reports as appropriate.

## Register the result

Edit `<office>/records/artifacts.json`. All record paths are forward-slash paths relative to `<office>`. Paths must resolve inside the office and be ordinary local files/directories. Keep a version history of the register in the project's canonical storage. Each `id@version` is unique.

The following is an illustrative accepted entry. Replace digest markers with real hashes and records, and derive authority from the actual charter. The checker compares files and declared bindings. Host permissions and the independent reviewers establish who authored the records.

```json
{
  "schema_version": 1,
  "project": "Example project",
  "milestones": [{"id": "M1", "required_artifacts": ["A01@v1"]}],
  "artifacts": [{
    "id": "A01",
    "version": "v1",
    "state": "accepted",
    "producer": {"actor": "product", "session": "producer-session-001"},
    "payload": "artifacts/A01/v1/payload",
    "manifest": "artifacts/A01/v1/manifest.json",
    "manifest_sha256": "DIGEST_OF_MANIFEST",
    "dependencies": [],
    "required_reviewers": ["qa"],
    "reviews": [{
      "actor": "qa",
      "session": "reviewer-session-001",
      "verdict": "pass",
      "manifest_sha256": "DIGEST_OF_MANIFEST",
      "record": "reviews/R01.md",
      "sha256": "DIGEST_OF_REVIEW"
    }],
    "required_verification": ["inspection"],
    "verification": [{
      "kind": "inspection",
      "status": "pass",
      "method": "Inspect each requirement against the source interview",
      "environment": "Pinned interview transcript and candidate v1",
      "actor": "qa",
      "exit_code": null,
      "manifest_sha256": "DIGEST_OF_MANIFEST",
      "record": "evidence/E01.md",
      "sha256": "DIGEST_OF_EVIDENCE"
    }],
    "allowed_approvers": ["sponsor"],
    "approval": {
      "actor": "sponsor",
      "authority_ref": "CHARTER.md / Decision authority",
      "manifest_sha256": "DIGEST_OF_MANIFEST",
      "record": "records/S01.md",
      "sha256": "DIGEST_OF_SIGNOFF"
    },
    "defects": []
  }]
}
```

Each dependency has `artifact` set to an exact `id@version` and `manifest_sha256` matching that accepted input. Reached dependencies are checked recursively. Cycles, missing versions, and drift fail.

During drafting, record a compact entry with `id`, `version`, `state`, and a `current_draft_path` plus `current_draft_sha256` when a file exists. For example, `{"id":"A01","version":"v1","state":"draft","current_draft_path":"CHARTER.md","current_draft_sha256":"ACTUAL_DRAFT_DIGEST"}` records a draft without inventing acceptance. List the planned `A01@v1` in its milestone's required artifacts. The delivery checker rejects its draft state until the complete acceptance record is present. Draft-only metadata supports human/PM tracking and is outside the acceptance checker’s file-binding scope.

Current acceptance uses one passing review per reviewer. Preserve previous rounds in the reviews directory and link them from the current report. Required reviewers and the producer have distinct actor and session identities. The project plan decides which reviewer roles are required.

Verification kinds are `static`, `behavioral`, and `inspection`. The project selects required kinds per artifact. Each current verification has `status=pass`, the candidate digest, nonempty `actor`, `method`, and `environment`, plus the raw report path/digest. Command checks require integer `exit_code=0`. Inspections accept `null` or integer `0`. Choose kinds that actually cover the outcome.

Defects carry `id`, `severity`, and `status`. This tool's compact gate requires `blocking` and `major` findings to be closed. A closed finding includes distinct `fixer` and `verifier`, the verified `manifest_sha256`, and retest `record`/`sha256`. A `minor` finding can be `accepted_risk` with authorized `actor`, bound `manifest_sha256`, and acceptance `record`/`sha256`. Keep fuller history, ownership, dates, and designated-verifier rules in the management plan and linked records. A project with a different policy can use its own checker.

## Check the delivery register

```bash
python scripts/artifact_control.py check /project/collaboration/project-office/records/artifacts.json --milestone M1
```

Omit `--milestone` to check all declared milestones. Empty milestone requirements, unknown milestones, required missing artifacts, incomplete acceptance, open blocking/major findings, self-review identities, stale bindings, file drift, extra payload files, unsafe paths, and malformed records fail with exit code 1. The check is read-only. It checks the selected milestone's required artifacts and their dependency closure. Future drafts can remain in the same register.

A structural pass establishes file and declared-record consistency within that scope. The PM still evaluates the correctness and authenticity of the inputs, the adequacy of the tests, compliance with the user's mandate, and required human or external acceptance.
