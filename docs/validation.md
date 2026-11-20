# Validation record

Date 2026-11-20. Package version 0.2.0.

## Local utility checks (v0.2.0)

Windows with Python 3.13.14. Run using the environment's verified interpreter with isolated temporary directories.

```text
python -m unittest discover -s tests -v
Ran 52 tests
OK
Exit code 0
```

The suite covers all 39 baseline payload-sealing/register checks from v0.1.0 plus 13 new tests for v0.2.0: `init_project.py` scaffolding (`PROJECT-PROFILE.md` and `RULEBOOK.md`), `seal-scope` live deliverable sealing with cache skipping and symlink/overwrite/self-reference refusal, zero-reseal governance additions outside sealed manifests, `review_history` append-only integrity, atomic `batches` enforcement across milestone scoping, `coordinator_actor` review/defect-verifier purity checks, and CLI `seal-scope` / `check --project-root` round-trips. Raw output is in [tool-tests.txt](validation/tool-tests.txt).

A package validation check also verifies skill directory/frontmatter name parity, allowed Agent Skills frontmatter keys, local Markdown link resolution across all documents, LF line endings, and zero private/environment identifiers.

## Earlier v0.1.0 evaluations

During v0.1.0 release preparation (2026-11-16):
- **Independent review**: A distinct reviewer session audited the instructions, references, templates, and Python utilities, surfacing an initializer rollback cleanup defect that was fixed and verified with focused recovery tests ([review report](validation/independent-review.md)).
- **Isolated forward-test**: A separate session executed a fictional multi-milestone project takeover scenario, surfacing host-hidden model metadata handling and folder/frontmatter naming rules ([forward-test report](validation/forward-test.md)).

## Remaining validation

Cross-host long-duration runs of v0.2.0 two-plane workflows, live multi-provider `429` quota fallback execution, and end-to-end field outcomes remain subject to ongoing project trials. The checked-in CI workflow tests Windows and Linux across Python 3.10 and 3.13.

The optional utilities verify structural file/record consistency and cryptographic digests. Substantive deliverable quality, authentic independent review, and real-user usability remain the responsibility of the designated reviewers and acceptance authority.
