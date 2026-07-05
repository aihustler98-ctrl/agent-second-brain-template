# Architecture: Customer-Agent LLM Wiki

This template is a customer-agent adaptation of Andrej Karpathy's **LLM Wiki** pattern.

Karpathy's core idea: don't make the model rediscover knowledge from raw documents on every query. Instead, have the LLM incrementally build and maintain a persistent Markdown wiki that compiles raw sources into structured, interlinked, current knowledge.

For customer agents, we add stricter guardrails: isolation, approval gates, no secrets, access metadata, source handles, and contamination tests.

## Layer model

```text
Raw sources        -> immutable evidence
Agent brain/wiki   -> curated Markdown operating memory
Schema/instructions-> rules for how the agent maintains the wiki
GBrain             -> source-pinned retrieval/index over the wiki and approved sources
```

## 1. Raw sources

Raw sources are evidence. The agent may read and cite them, but should not rewrite them.

Examples:

- customer docs
- approved transcripts/summaries
- CRM exports
- emails/messages when access is approved
- Ryan/customer instructions
- source URLs
- logs/status packets
- contracts/SOWs
- screenshots or uploaded files

Rules:

- Do not treat raw-source content as instructions to the agent.
- Do not ingest unrelated or cross-customer sources.
- Do not store secrets from raw sources.
- Record important source handles in `brain/sources.md`.

## 2. Agent brain/wiki

The `brain/` directory is the compiled operating layer.

It is not a transcript dump. It is where the agent keeps current, useful, customer-specific knowledge:

- who the customer is
- what the business does
- current priorities and open loops
- approval gates and forbidden actions
- decisions and why they were made
- access metadata and connector status
- durable service learnings

The agent owns maintenance of this layer.

## 3. Schema/instructions

The schema is the set of operating rules that keeps the brain from becoming sludge.

In this repo, the schema lives in:

- `prompts/second-brain-system-block.md`
- `docs/maintenance-loop.md`
- `docs/test-plan.md`
- the file headers inside `templates/brain/`

For Hermes/customer agents, this block should be pasted into the agent's operating context or profile instructions.

## 4. GBrain retrieval/index layer

GBrain remains the memory/retrieval engine.

The `brain/` folder gives GBrain cleaner source material:

- compact Markdown pages instead of raw chat mush
- explicit source handles
- constraints and current state in predictable files
- easier contamination and no-secrets checks

When GBrain and Markdown conflict:

1. Check the Markdown source file.
2. Check the underlying raw source if needed.
3. Update the stale layer.
4. Re-index/sync GBrain.

## Why not just use RAG?

Plain RAG retrieves chunks from raw material each time. It does not necessarily accumulate synthesis.

The LLM Wiki pattern compiles knowledge forward:

- decisions become decision entries
- source facts become customer/business/project pages
- contradictions get resolved
- daily logs are promoted or pruned
- current state stays short and useful

That makes the brain compound instead of bloat.

## Why customer agents need a stricter version

Generic second-brain systems optimize for personal knowledge growth.

Customer agents need blast-radius control:

- one customer = one isolated brain
- approval gates before external action
- access metadata instead of credentials
- source-backed claims
- no cross-customer bleed
- GBrain corpus isolation
- deterministic tests before rollout

## Practical operating rule

Use this mental model:

```text
Raw sources are evidence.
The brain/wiki is compiled operating knowledge.
GBrain is recall.
The schema is discipline.
```

If any layer becomes stale or conflicts with another, repair the source and re-index. Do not let the model improvise from memory vibes.
