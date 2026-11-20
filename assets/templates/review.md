verdict: PASS|CONDITIONAL|REJECT
blockers: 0
majors: 0
minors: 0
artifact: <ARTIFACT_ID@VERSION>
manifest_sha256: <FULL_64_HEX_MANIFEST_DIGEST>

# Independent review

- Review ID, round/history ID, date, reviewer actor / model / session
- Candidate artifact ID, version, `manifest_sha256` (single canonical digest — never single-file proxy)
- Review mode: `full` | `incremental_diff` (list diff scope if Round 2+)
- Mechanical pre-gate check result (exit code 0 required before model review)
- Criteria, `RULEBOOK.md` references, source inputs, and real-user completeness checks (`Invisible`..`Unresponsive`)
- Findings with stable IDs (`blocking` / `major` / `minor`), reproduction/evidence, expected fix, `fixer`, and `designated_verifier`
- Verdict and acceptance-blocking conditions (note: any open `blocking` -> `REJECT`; any open `major` forbids `PASS`)
- Limits, skipped checks, dissent, and independent retest evidence
