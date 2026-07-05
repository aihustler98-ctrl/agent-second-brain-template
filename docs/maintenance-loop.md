# Weekly Maintenance Loop

Run this weekly per customer agent, or whenever `_meta.md` says the last review is older than 7 days.

## Goal

Keep the brain small, source-backed, and useful. The weekly loop prevents the `log/` folder from turning into a junk drawer.

## Steps

1. Read:
   - `brain/_meta.md`
   - `brain/current.md`
   - `brain/constraints.md`
   - `brain/decisions.md`
   - `brain/learnings.md`
   - last 7 days of `brain/log/`
2. Promote durable log items:
   - customer facts -> `customer.md`
   - approval/privacy/access rules -> `constraints.md` / `context/access.md`
   - source handles -> `sources.md`
   - project state -> `current.md` / `context/projects.md`
   - decisions -> `decisions.md`
   - repeated service patterns -> `learnings.md`
3. Remove or rewrite contradictions. Latest verified source wins.
4. Compress noisy logs. Keep enough audit trail to explain why current state changed.
5. Check for secrets by pattern and remove/quarantine any accidental credential material.
6. Update `_meta.md` with review date, next review due, known gaps, and stale-risk areas.
7. If GBrain is used, re-sync/re-index the `brain/` folder and run recall smoke questions.

## Recall smoke questions

Customize these per customer:

- Who is this customer and what do they want from the agent?
- What actions require explicit approval?
- What is the current top priority?
- What are the top open loops?
- What systems does the agent have access to, and which are unverified/expired?
- What decision changed the agent's operating mode most recently?

## Output

A weekly review should produce a compact summary:

```markdown
# Brain Review — YYYY-MM-DD
- Promoted:
- Pruned:
- Contradictions fixed:
- Secrets found: none / fixed
- GBrain sync: not used / synced / failed
- Known gaps:
- Next review:
```
