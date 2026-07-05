# Agent Second Brain Template

A portable, per-agent/per-customer memory scaffold for AI agents.

This is intentionally boring: plain Markdown, per-customer isolation, hard approval gates, source handles, and a maintenance loop. It borrows the best public pattern from popular AI/Obsidian second-brain repos — especially Eugeniu Ghelbur's MIT-licensed `obsidian-second-brain` idea of an AI-maintained vault — but trims it down for customer agents where privacy, auditability, and live-action boundaries matter more than 40+ commands.

The goal: every customer agent gets a clean local `brain/` directory it can read, curate, prune, and sync/index into GBrain. Markdown is the source notebook. GBrain is the retrieval engine.

## Default architecture

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

Checked popular GitHub candidates before shaping this:

- `eugeniughelbur/obsidian-second-brain` — ~2.9k stars, MIT, strong AI-maintained vault concept. Best inspiration, but too broad/heavy for customer-agent provisioning.
- `coleam00/second-brain-starter` — ~650 stars, good PRD/memory layer ideas, no detected license from GitHub API.
- `voidashi/obsidian-vault-template` — ~300 stars, MIT, useful Obsidian/PARA-ish vault starter.
- `smixs/agent-second-brain` — ~290 stars, MIT, voice-to-Obsidian agent pattern.

Decision: do not copy a full public repo. Use the proven markdown-vault/self-curation pattern, then make a lean customer-agent-specific scaffold with stronger constraints, access hygiene, and GBrain integration.

## Files

- `templates/brain/` — copyable brain skeleton
- `prompts/second-brain-system-block.md` — drop-in system prompt block
- `scripts/scaffold-brain.sh` — local scaffolder
- `docs/maintenance-loop.md` — weekly review and pruning loop
- `docs/gbrain-integration.md` — recommended GBrain relationship

## License

MIT
