# Validation record

Date 2026-11-16. Package version 0.1.0.

## Local utility checks

Windows with Python 3.13.14. The actual command was run using the environment's verified interpreter with isolated temporary output.

```text
python -m unittest discover -s tests -v
Ran 39 tests
OK
Exit code 0
```

The suite exercises both script entrypoints and accepted/rejected structural delivery cases. Cases include empty requirements, missing artifacts, milestone scoping, self-review identities, conditional review, missing approval, changed payloads/manifests/reports, stale evidence, skipped checks, boolean exit codes, dependency closure/cycles, duplicate records, unsafe paths, open major findings, independent defect verification, risk acceptance, initialization failure recovery, and overwrite protection. Fixtures are synthetic. Raw output is in [tool-tests.txt](validation/tool-tests.txt).

The skill-creator frontmatter validator returned `Skill is valid!`. A package check also verifies the skill directory/frontmatter name match, local Markdown references, and the publication file inventory.

## Independent review

A distinct reviewer session inspected the actual instructions, references, templates, documentation, and utility source. It found a minor initializer recovery issue. The correction rolls back only initialization-owned files and empty directories on write failure and preserves existing destinations. The reviewer inspected that correction and independently ran two focused recovery/preservation tests successfully. The [review report](validation/independent-review.md) preserves the finding and closure with inspected source digests.

## Isolated forward-test

A separate session used the skill for a fictional in-flight volunteer-handbook project with three milestones, one available session, zero budget for further model calls, missing prior-draft evidence, and a pending reviewer channel. It produced an initiation/takeover package, two role skills, a task dispatch, a 12-slot outline, source-gap matrix, and handover.

Five focused structural self-checks passed and six local Markdown links resolved. The delivery checker returned exit code 1 for the draft milestone, retaining pending acceptance. The trial surfaced two usability ambiguities, which led to explicit handling of host-hidden model metadata and a compact draft-register example.

Inspection of the generated role packages also found an initial folder/frontmatter name mismatch. The source instructions now specify exact equality. A follow-up produced corrected role packages that passed frontmatter validation and explicit directory-name assertions, while preserving the original trial files. The [forward-test report](validation/forward-test.md) records the original gap and follow-up.

Both evaluating sessions inherited the parent discussion. Their work provides separate-session evidence with contextual exposure. It covers preparation, takeover, role packaging, structural controls, and resumable records.

## Remaining validation

Long-duration monitoring, live heterogeneous-model selection, substantive completion of an entire managed project, outcome improvement, and additional host integrations require field trials. The checked-in CI matrix targets Windows and Linux with Python 3.10 and 3.13. Its remote run status belongs to the repository's Actions history after publication.

The optional tools establish consistency of local files and declared acceptance records. The designated reviewer and acceptance authority remain responsible for authentic review, adequate verification, and substantive project correctness.
