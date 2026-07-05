# Agent Second Brain Template

A customer-agent adaptation of Andrej Karpathy's **LLM Wiki** pattern: raw sources stay immutable, the agent maintains a clean Markdown brain/wiki, and GBrain indexes that curated layer for source-pinned recall.

This is intentionally boring: plain Markdown, per-customer isolation, hard approval gates, source handles, and a maintenance loop. It borrows the public AI-maintained-vault idea from Karpathy's LLM Wiki and popular Obsidian second-brain repos, then trims it down for customer agents where privacy, auditability, and live-action boundaries matter more than a pile of commands.

The goal: every customer agent gets a clean local `brain/` directory it can read, curate, prune, and sync/index into GBrain. Markdown is the compiled source notebook. GBrain is the retrieval engine.

## Default architecture

Karpathy's pattern has three main layers: raw sources, a maintained wiki, and a schema/instruction file. Our customer-agent version adds GBrain as the retrieval/index layer over the maintained wiki.

```text
Raw sources        -> immutable evidence
./brain/ markdown  -> agent-maintained operating wiki
Schema/prompt      -> rules for maintaining the wiki
GBrain             -> retrieval/index over the wiki + approved sources
```

Operationally:

```text
Customer Agent
  -> reads/writes ./brain/ markdown
  -> nightly/weekly maintenance keeps it clean
  -> GBrain indexes/syncs the brain for semantic, source-pinned recall
```

## Why this exists

Agents lose value when memory becomes chat mush. This template gives every new agent:

- isolated customer memory
- visible source files Ryan/Harvey can audit
- approval gates and privacy constraints
- current-state dashboard
- decision history with reasoning
- daily working notes that get promoted or pruned
- a standard prompt block for self-curation

## Directory structure

```text
brain/
├── customer.md         # Who the customer/user is
├── constraints.md      # Approval gates, privacy rules, forbidden actions
├── current.md          # Active priorities, open loops, blockers, next actions
├── sources.md          # Canonical source handles, docs, links, systems of record
├── context/
│   ├── business.md     # Business model, terminology, key workflows
│   ├── projects.md     # Active/parked/retired projects
│   ├── tools.md        # Apps, tools, integrations, workflows
│   └── access.md       # Access ownership/status/locations; never secrets
├── decisions.md        # Meaningful decisions and WHY
├── learnings.md        # Durable service patterns discovered over time
├── log/
│   └── YYYY-MM-DD.md   # Dated working notes, one file per active day
└── _meta.md            # Brain health, reviews, gaps, stale-risk areas
```

## Install into a new agent workspace

```bash
./scripts/scaffold-brain.sh /path/to/agent/workspace
```

This creates `/path/to/agent/workspace/brain/` from `templates/brain/`.

## Test the maintenance rules

Run the static template checks:

```bash
./scripts/test-template.sh
```

Run the accelerated behavior simulation:

```bash
./scripts/pilot-accelerated-test.py
```

The accelerated test creates isolated throwaway brains under `/tmp/agent-second-brain-accelerated-pilot/`, simulates representative memory-maintenance events, and verifies that facts, decisions, access metadata, logs, untrusted content, and customer isolation are handled correctly.

## Add the agent prompt block

Paste `prompts/second-brain-system-block.md` into the agent's operating instructions/system prompt.

## Core rules

1. One customer agent gets one isolated `brain/` directory.
2. Never cross-mount customer brains.
3. Never store secrets, passwords, tokens, API keys, or full payment details.
4. Store where credentials live and who owns access, not the credential value.
5. Permanent memory files should be concise. Logs are scratchpad and audit trail.
6. If a fact changes, edit the old fact. Do not append contradictions.
7. GBrain should index this folder, not replace it.

## Startup read rule

At the start of a session, the agent should read:

1. `brain/customer.md`
2. `brain/constraints.md`
3. `brain/current.md`
4. `brain/_meta.md`

Read recent logs only when the request relates to ongoing work or `_meta.md` points to an active handoff.

## Promotion rule

- One-off observation -> today’s log
- Repeated pattern or customer correction -> `learnings.md`
- Safety/access/approval rule -> `constraints.md`
- Meaningful choice with consequence -> `decisions.md`
- Project state/next action -> `current.md` and/or `context/projects.md`
- Source/evidence handle -> `sources.md`
- Procedure/workflow -> skill/playbook, not brain memory

## GBrain integration stance

This repo intentionally does **not** replace GBrain.

Use this as the clean source layer. Then sync/index `brain/` into an isolated per-agent/customer GBrain corpus for semantic recall, evals, contradiction checks, and maintenance.

## Public repo research note

Checked Karpathy's LLM Wiki gist and popular GitHub second-brain candidates before shaping this.

Key source pattern:

- Andrej Karpathy's `LLM Wiki` gist — 5k+ stars/forks shown on GitHub gist page; the core pattern is raw sources -> LLM-maintained Markdown wiki -> schema/instructions. Strongest conceptual fit.

Popular implementation/reference repos found:

- `eugeniughelbur/obsidian-second-brain` — ~2.9k stars, MIT, strong AI-maintained vault concept. Best public implementation inspiration, but too broad/heavy for customer-agent provisioning.
- `coleam00/second-brain-starter` — ~650 stars, good PRD/memory layer ideas, no detected license from GitHub API.
- `voidashi/obsidian-vault-template` — ~300 stars, MIT, useful Obsidian/PARA-ish vault starter.
- `smixs/agent-second-brain` — ~290 stars, MIT, voice-to-Obsidian agent pattern.

Decision: do not copy a full public repo. Use the proven LLM Wiki / markdown-vault self-curation pattern, then make a lean customer-agent-specific scaffold with stronger constraints, access hygiene, source handles, contamination tests, and GBrain integration.

## Files

- `templates/brain/` — copyable brain skeleton
- `prompts/second-brain-system-block.md` — drop-in system prompt block
- `scripts/scaffold-brain.sh` — local scaffolder
- `docs/maintenance-loop.md` — weekly review and pruning loop
- `docs/gbrain-integration.md` — recommended GBrain relationship
- `docs/architecture.md` — Karpathy LLM Wiki mapping for customer agents
- `docs/test-plan.md` — layered validation plan
- `examples/simulation-prompts.md` — behavior simulation prompts

## Testing

Run deterministic scaffold/static checks:

```bash
./scripts/test-template.sh
```

Then use `examples/simulation-prompts.md` for agent-behavior testing and `docs/test-plan.md` for GBrain/contamination acceptance.

## License

MIT
