# Task dispatch

- Task / milestone ID & batch ID (if coupled)
- Outcome and requirement IDs
- Assigned role / actor / provider / model / reasoning setting / session or run ID (record at creation; never alter post-run)
- Role skill path and `PROJECT-PROFILE.md` / `RULEBOOK.md` bindings
- Pinned input artifact versions and `manifest_sha256` digests
- Allowed write paths and forbidden paths (`<= 1` active writer per scope; shared DB read-only)
- Mechanical pre-checks required before review submission
- Expected output artifact IDs, versions, paths, and sealing mode (`seal-scope` or `seal`)
- Self-check commands, timeout budget (`1.5x–2x` observed suite runtime), and retry/stall limits (`<= 2` failures / 90m zero-evidence settle)
- Required independent reviewer (`!= producer`, `!= coordinator`) and next recipient
- Existing authorization and user-reserved boundaries
- Final receipt (`record-external-outcome` summary, exit code, log path, and digest)
