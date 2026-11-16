# Independent static review

Review date 2026-11-16.

Reviewed package `<skill-root>` in the separate `skill_independent_review` agent session.

| Reviewed file | SHA-256 at review |
| --- | --- |
| `SKILL.md` | `77b829d0478814aab92d4435f0db835fbfdaca58e88911757518e4fdc8bfc24c` |
| `scripts/init_project.py` | `660914a2ffcbacc847d5ae49ea9a83701ea29b5fb993049d7f904cb55bc00805` |
| `scripts/artifact_control.py` | `51fc28d2a0bb8a35731012c63b5e83807413a9f0f2d94d495a650ddaa6750b4d` |

## Scope and method

Read the actual skill entrypoint, both installation/use descriptions, lifecycle references, model/team guidance, role-skill guidance, templates, worked example, and optional utility implementations. Compared their decisions and outputs against the user's requested continuing-project PM workflow and skill-creator guidance. Inspected source control flow for the utility finding below.

This pass performs static assessment. It did not execute tools against sample artifacts, run another model, test a new host installation, or observe a long-duration project. Parent-owned utility tests and the separate forward-test remain their own evidence.

## Disposition

No blocking workflow-design finding in this review's scope. The package covers the user's requested mandate, resource discovery, current model research and project-specific probes, team formation, a tailored skill for each occupied role including PM, milestone execution, preserved outputs and review rounds, version-bound verification, and a navigable final handover.

The PM management plan and role skill receive independent review under `SKILL.md` line 34. Resource constraints preserve pending independent review under line 42. Current model claims require official sources and recorded uncertainty under line 38. Existing authority is retained under the mandate section. The references support in-flight takeover, manual dispatch, dependency reassessment, quota failures, partial/uncertain execution, and cross-session checkpoints.

## Findings

### F-01 — Minor — Initialization leaves an unretryable partial destination on an I/O failure

`scripts/init_project.py` creates the destination at line 34, creates child directories, then writes each document at line 38, decisions at line 39, and the register at line 43. A failure in any later write exits through the CLI error handler after earlier output has persisted. A rerun encounters `Destination already exists` at line 24 and refuses recovery. The operator must inspect and repair the incomplete office or select another location.

Provide recoverable initialization for files created by the operation, or create an explicit incomplete marker with a documented safe resume path. Preserve the existing-destination protection. Add a targeted injected-write-failure test proving that recovery retains user content and produces a coherent draft office. This finding comes from source control-flow inspection and has no executed failure reproduction in this review.

## Publication checks still pending at this snapshot

`README.md` line 66 links `docs/validation.md` and describes local tool tests and independent forward-testing. The validation document was still being authored during review. Before publication, ensure it exists, lists the actual commands and outcomes, identifies the simulated scope, and states remaining host/field uncertainty. The test command in README also needs its actual result recorded by the parent.

## Limits and follow-up

The optional checker validates local bytes and declared record bindings. The package already states that actor identities, authorization, substantive review quality, and domain acceptance depend on the host and evidence owners. These boundaries are appropriately disclosed in README and tooling guidance.

Cross-host installation, genuinely independent multi-model quality, prolonged monitoring, and continued-project outcome improvement require additional field use. This review supports a truthful initial extraction release when the publication checks and utility disposition are recorded.

## F-01 correction verification

The parent supplied a correction for independent recheck. The reviewed initializer now records its newly created destination, child directories, and exclusively created files. On `OSError`, it unwinds that list in reverse order using file unlink and empty-directory removal. Existing destinations remain protected. If cleanup cannot finish, the error identifies the partial office for inspection. Static inspection confirms that a failure during a file write is covered because the newly opened file is registered before `stream.write`.

The corrected `scripts/init_project.py` has SHA-256 `c067ce137b0b8e5d0c870cb422cecb8fd2f8c66322046e68aa6a799a5dab4b37`. The reviewed test file has SHA-256 `256b3c1ca03b03cd50e0de1266e0e12c141fa7eb62891ed48814e9e319e1ae52`.

Executed from the package's `tests` directory with `APM_TEST_TMPDIR` resolved and checked as `<isolated-test-root>`, and `PYTHONDONTWRITEBYTECODE=1`.

```text
<verified-python> -m unittest test_artifact_control.DeliveryTests.test_initializer_recovers_from_partial_write_failure test_artifact_control.DeliveryTests.test_initializer_preserves_existing_directory -v

test_initializer_recovers_from_partial_write_failure ... ok
test_initializer_preserves_existing_directory ... ok
Ran 2 tests in 0.069s
OK
```

The first test injects an error when opening `TEAM.md` after earlier documents have been created, verifies removal of the partial destination, then verifies a successful retry and register creation. The second test confirms that an existing office and its register remain intact. Exit code was 0.

**F-01 is closed for the inspected correction and these focused cases.** The full-suite count remains parent-owned evidence. The validation document and publication state remain outside this follow-up's verification scope.
