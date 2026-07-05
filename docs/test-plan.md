# Test Plan

This repo is tested with boring deterministic checks first. Agent behavior and GBrain retrieval are tested as higher layers.

## Layer 1 — Static/scaffold tests

Run:

```bash
./scripts/test-template.sh
```

Covers:

- required repo files exist
- scaffold script is executable
- no obvious secret-looking content exists in templates/docs/scripts
- scaffold creates a complete dated `brain/`
- scaffold refuses to overwrite an existing brain
- system prompt names required startup files
- constraints/access templates include safety guardrails
- GBrain integration doc defines conflict behavior

## Layer 2 — Agent behavior simulation

Use `examples/simulation-prompts.md` against a test agent or coding agent. Expected behavior:

- customer preference -> `customer.md`
- approval/privacy rule -> `constraints.md`
- project status -> `current.md` / `context/projects.md`
- meaningful choice -> `decisions.md`
- source handle -> `sources.md`
- daily note -> `log/YYYY-MM-DD.md`, summarized not transcribed

## Layer 3 — Maintenance loop test

Seed a fake dirty brain with:

- duplicate facts
- stale project status
- old logs
- one changed preference
- one open loop

Run the weekly maintenance prompt from `docs/maintenance-loop.md`.

Pass criteria:

- durable facts promoted
- contradictions removed
- `_meta.md` review date updated
- `current.md` stays short
- old logs compressed or summarized
- no secrets introduced

## Layer 4 — GBrain retrieval test

Index a test brain into an isolated customer corpus.

Smoke questions:

1. Who is this customer?
2. What actions require approval?
3. What is the current top priority?
4. What access is expired or unverified?
5. Why did we decide X?
6. What source backs that?

Pass criteria:

- answers cite the right brain files/source handles
- no other customer content appears
- if GBrain conflicts with markdown, markdown wins and stale retrieval is repaired

## Layer 5 — Contamination test

Create two fake customers with unique facts:

- Acme Plumbing: `blue wrench`
- Bright Dental: `silver molar`

Index/read them separately.

Pass criteria:

- Acme queries never retrieve Bright Dental facts
- Bright Dental queries never retrieve Acme facts
- no shared brain directory, corpus, connector entity, or runtime state

## V1 acceptance bar

Do not call this ready for customer-agent default rollout until:

- `./scripts/test-template.sh` passes
- 10/10 simulated memory writes land in the right file
- weekly maintenance cleans a dirty fixture brain
- GBrain answers recall smoke questions from the correct corpus
- contamination test passes both directions
- one internal pilot runs 3–5 days without becoming a transcript/junk drawer
