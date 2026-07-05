# GBrain Sync Recipe

Purpose: index each agent/customer Markdown brain into GBrain without turning memory into chat mush or leaking customer context.

## Architecture

```text
agent workspace ./brain/ markdown
  -> deterministic sync job
  -> isolated GBrain corpus
  -> source-pinned recall for that same agent/customer
```

## Hard rules

1. One agent/customer `brain/` maps to one isolated GBrain corpus.
2. Never index multiple customer brains into a shared customer corpus.
3. Never index secrets, tokens, passwords, full credentials, or full payment details.
4. Logs may be indexed only as summaries; never transcripts.
5. If GBrain recall conflicts with Markdown brain, verify against source files/live systems before acting.
6. Corpus metadata must include customer/agent id, source path, file path, content hash, and sync timestamp.

## Minimum sync steps

1. Validate template and pilot behavior:
   ```bash
   ./scripts/test-template.sh
   ./scripts/pilot-accelerated-test.py
   ```
2. Scan `brain/` for obvious secret patterns.
3. Chunk Markdown by file and heading.
4. Attach source metadata:
   - `agent_id`
   - `customer_id`
   - `brain_path`
   - `relative_file`
   - `heading_path`
   - `sha256`
   - `synced_at`
5. Upsert chunks into the isolated GBrain corpus for that exact agent/customer.
6. Run contamination checks: query customer A facts from customer B corpus and require no hit.

## Harvey dogfood corpus

Harvey pilot source path:

```text
/Users/claudbot/.hermes/profiles/harvey/brain-pilot/
```

Status: pilot only. GBrain remains primary.

Created: 2026-07-04
