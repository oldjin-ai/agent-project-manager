# Review, verification, and delivery

## Artifact lifecycle

Use `missing → draft → in_review → accepted → superseded` as a compact lifecycle. A rejection goes to `rework`, and changed accepted content or inputs go to `stale`. Keep earlier versions and every review round. The project can map these states to an existing tracker.

Register the producer, required reviewers, version, milestone, dependencies, exact content reference, evidence, findings, and acceptance authority for every key output. Apply this to the management plan itself. A conditional review remains pending until its conditions are verified or the appropriate authority explicitly accepts a scoped exception permitted by the project plan.

Acceptance dependencies form a DAG. Candidate artifacts can be tested before acceptance. For tightly coupled release artifacts, bind the package, its acceptance report, and decision to the same candidate digest and batch. Avoid reciprocal acceptance prerequisites by making the tested package the report's input.

## Independent review

Use a separate reviewer session and preserve its actual identity, model, and raw report. Supply the requirements, candidate, relevant sources, and review rubric. Keep the review prompt neutral where practical. The PM routes disagreements to the designated domain or technical decision owner and preserves dissent and rationale.

The review records scope, artifact version/digest, method, evidence inspected, verdict, severity, actionable findings, limitations, and retest expectations. The producer handles corrections. The designated independent verifier closes each acceptance-blocking finding with actual evidence.

Define severity by impact on the agreed outcome. Blocking errors include a failed required user path, material domain/numerical errors, missing required content, fabricated evidence, unauthorized actions, or missing acceptance prerequisites. Smaller findings can have an owner and an explicitly accepted limitation when the project's plan permits it. Keep the user's required acceptance criteria in force.

## Verify the intended outcome

Choose checks that exercise the substantive outcome. For software, cover the actual entry points, meaningful user actions, data semantics and units, negative/degraded states, integration, and relevant recovery/deployment behavior. For research, verify primary sources, calculations, assumptions, coverage, and conclusions. For documents or design, check content completeness, audience fit, rendering, accessibility, and requested formats.

Record the command or inspection method, working directory, start/end times, environment, actor, exact code/data/config/package versions, result counts, failures, skips, raw log reference, and digest. Preserve actual failed results. Label static checks, automated behavior checks, human inspection, and inaccessible verification individually.

Test the package that will be handed over or deployed. A rebuild after testing changes that binding and needs relevant revalidation. An acceptance report should enumerate which requirement was exercised, where its evidence is, and what remains unresolved.

## Baseline and handover

Bind required reviewer approval and acceptance authority to the exact snapshot. Use immutable version paths, content-addressed storage, or pinned commits plus required configuration/data references. Keep large or restricted files in approved durable storage with accessible references and checksums. Keep the current pointer separate from preserved historical versions.

The delivery index should let the user find all required outputs and understand whether the project can be used for its intended purpose. Include a requirement-to-artifact-to-verification matrix, current artifact inventory, review/rework history, decisions, remaining limitations, acceptance records, package digests, usage instructions, and operations/recovery ownership where relevant.

Check reference resolution and file integrity before delivery. Apply external publication/deployment only within existing authorization and verify the resulting remote state. Record accepted project completion and any ongoing operational ownership separately.
