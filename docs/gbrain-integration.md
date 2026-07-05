# GBrain Integration

This template is designed to work with GBrain, not replace it.

## Recommended relationship

```text
./brain/ markdown files = clean source notebook
GBrain = source-pinned retrieval, semantic search, evals, contradiction checks
```

## Per-customer isolation

Each customer agent should get its own:

- `brain/` directory
- GBrain source/corpus
- profile/workspace
- connector/OAuth entities
- logs and cron jobs

Shared vendor infrastructure is okay only when approved. Shared memory/corpus/context is not the default.

## Sync policy

Index only the customer's own `brain/` files and approved source docs. Do not broad-import unrelated chats, private archives, or other customer folders.

Suggested source name pattern:

```text
customer-<slug>-brain
```

## Retrieval rule

Use direct file reads for startup-critical state:

- `customer.md`
- `constraints.md`
- `current.md`
- `_meta.md`

Use GBrain for broader recall:

- "what did we decide about X?"
- "what do we know about this customer's CRM?"
- "find the source for the approval rule"
- "summarize open loops across project notes"

## Eval rule

Before calling a customer brain ready, run recall checks against both file reads and GBrain retrieval:

1. Customer identity and company are correct.
2. Approval gates are retrievable.
3. Current top priority is correct.
4. Access status does not overclaim live connectors.
5. No cross-customer strings appear in retrieved excerpts.
6. Secrets are not present in indexed content.

## Failure posture

If GBrain retrieval conflicts with the markdown source files, the files win until source verification proves otherwise. Then fix the stale layer and re-index.
