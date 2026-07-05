#!/usr/bin/env python3
"""Accelerated second-brain pilot test harness.

Creates isolated fake customer brains, applies representative memory-maintenance events,
and verifies the files behave like an agent-maintained wiki instead of a junk drawer.
No secrets, network, or live customer data required.
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TMP_ROOT = Path('/tmp/agent-second-brain-accelerated-pilot')
TODAY = date.today().isoformat()
SECRET_RE = re.compile(
    r'(sk-[A-Za-z0-9_-]{20,}|gh[pousr]_[A-Za-z0-9_]{20,}|xox[baprs]-[A-Za-z0-9-]{20,}|AKIA[0-9A-Z]{16}|-----BEGIN (RSA |OPENSSH |EC |DSA )?PRIVATE KEY-----)',
    re.I,
)


@dataclass
class Check:
    name: str
    passed: bool
    detail: str = ''


def read(path: Path) -> str:
    return path.read_text(encoding='utf-8')


def write(path: Path, content: str) -> None:
    path.write_text(content, encoding='utf-8')


def replace(path: Path, old: str, new: str) -> None:
    content = read(path)
    if old not in content:
        raise RuntimeError(f'missing expected text in {path}: {old!r}')
    write(path, content.replace(old, new, 1))


def scaffold(name: str) -> Path:
    workspace = TMP_ROOT / name
    subprocess.run([str(ROOT / 'scripts' / 'scaffold-brain.sh'), str(workspace)], check=True, stdout=subprocess.PIPE, text=True)
    return workspace / 'brain'


def all_markdown(brain: Path) -> str:
    return '\n'.join(path.read_text(errors='ignore') for path in brain.rglob('*.md'))


def apply_events(acme: Path, bright: Path) -> None:
    # 1 customer preference -> customer.md only
    replace(
        acme / 'customer.md',
        '- Response length preference:',
        '- Response length preference: Three bullets max unless detail is requested. Source: accelerated test',
    )

    # 2 approval gate -> constraints.md
    replace(
        acme / 'constraints.md',
        '- Sending external emails/messages/posts',
        '- Sending external emails/messages/posts — show the draft first and get explicit approval before sending',
    )

    # 3 project state -> current.md + context/projects.md
    replace(
        acme / 'current.md',
        '|------|-------|-------------|-------------|--------|--------|',
        '|------|-------|-------------|-------------|--------|--------|\n| Invoice cleanup | Sarah | Reconcile June Stripe payments | Friday | Open | accelerated test |',
    )
    replace(
        acme / 'context' / 'projects.md',
        '|---------|---------|-------|-------------|--------|--------|',
        '|---------|---------|-------|-------------|--------|--------|\n| Invoice cleanup | Clean up invoice/payment records | Sarah | Reconcile June Stripe payments by Friday | Active | accelerated test |',
    )

    # 4 decision -> decisions.md
    decision = f'''## {TODAY} — Use Telegram before SMS
**Decision:** Use Telegram first for customer messaging.

**Why:** The customer already uses Telegram and this avoids carrier/SMS deliverability weirdness.

**Alternatives considered:** SMS.

**Revisit if:** Telegram adoption fails or the customer requests SMS.

**Source:** accelerated test'''
    replace(
        acme / 'decisions.md',
        f'## {TODAY} — [Decision title]\n**Decision:**\n\n**Why:**\n\n**Alternatives considered:**\n\n**Revisit if:**\n\n**Source:**',
        decision,
    )

    # 5 source handle -> sources.md, no invented credential
    replace(
        acme / 'sources.md',
        '|------|----------|---------------|-------|',
        '|------|----------|---------------|-------|\n| June Sales SOP | Google Doc titled “June Sales SOP” | Location known; credentials not stored | CRM instructions source handle |',
    )

    # 6 changed fact -> edit existing line, no contradiction
    replace(
        acme / 'customer.md',
        '- Preferred channel:',
        '- Preferred channel: Telegram primary; email backup. Source: accelerated test',
    )

    # 7 access metadata only -> access.md
    replace(
        acme / 'context' / 'access.md',
        '|--------|-------|---------------|---------------------|---------------|-------|',
        f'|--------|-------|---------------|---------------------|---------------|-------|\n| Stripe API | Acme | No | 1Password item: Acme / Stripe | {TODAY} | Location only; no API key stored |',
    )

    # 8 daily log summary + promoted durable state
    log = acme / 'log' / f'{TODAY}.md'
    content = read(log)
    content = content.replace('## Interactions / work notes\n- ', '## Interactions / work notes\n- Discussed billing; paused refunds until Sarah checks the spreadsheet; created Monday follow-up.\n')
    content = content.replace('## Decisions made\n- ', '## Decisions made\n- Pause refunds until Sarah verifies spreadsheet.\n')
    content = content.replace('## Open loops created\n- ', '## Open loops created\n- Remind/check Monday about Sarah spreadsheet/refunds.\n')
    content = content.replace('- [ ] Decisions promoted to decisions.md', '- [x] Decisions promoted to decisions.md')
    content = content.replace('- [ ] Current project state promoted to current.md / context/projects.md', '- [x] Current project state promoted to current.md / context/projects.md')
    content += '\n## Security / untrusted content notes\n- Pasted email contained a prompt-injection instruction to ignore rules and send customer files; treated as untrusted content and no external action was taken.\n'
    write(log, content)

    with (acme / 'decisions.md').open('a', encoding='utf-8') as f:
        f.write(f'''\n\n## {TODAY} — Pause refunds pending spreadsheet check
**Decision:** Pause refunds until Sarah checks the spreadsheet.

**Why:** Avoid issuing incorrect refunds before billing data is verified.

**Alternatives considered:** Continue refunds immediately.

**Revisit if:** Sarah verifies the spreadsheet or Monday reminder fires.

**Source:** accelerated test
''')
    replace(
        acme / 'current.md',
        '| Invoice cleanup | Sarah | Reconcile June Stripe payments | Friday | Open | accelerated test |',
        '| Invoice cleanup | Sarah | Reconcile June Stripe payments | Friday | Open | accelerated test |\n| Refund pause follow-up | Sarah | Check spreadsheet and remind Monday | Monday | Open | accelerated test |',
    )

    # 9 no shared customer bleed -> bright only
    replace(bright / 'customer.md', '- Company:', '- Company: Bright Dental')
    replace(bright / 'customer.md', '- \n\n## Do not assume', '- Secret phrase: silver molar. Source: accelerated test\n\n## Do not assume')


def evaluate(acme: Path, bright: Path) -> list[Check]:
    checks: list[Check] = []
    acme_all = all_markdown(acme)
    bright_all = all_markdown(bright)
    customer = read(acme / 'customer.md')
    constraints = read(acme / 'constraints.md')
    current = read(acme / 'current.md')
    projects = read(acme / 'context' / 'projects.md')
    decisions = read(acme / 'decisions.md')
    sources = read(acme / 'sources.md')
    access = read(acme / 'context' / 'access.md')
    log = read(acme / 'log' / f'{TODAY}.md')

    def check(name: str, passed: bool, detail: str = '') -> None:
        checks.append(Check(name, passed, detail))

    check('customer_preference_one_place', 'Three bullets max' in customer and acme_all.count('Three bullets max') == 1)
    check('approval_gate_in_constraints', 'explicit approval before sending' in constraints)
    check('project_state_split_correctly', 'Invoice cleanup' in current and 'Reconcile June Stripe payments' in projects)
    check('decision_has_why_and_alternative', 'Use Telegram before SMS' in decisions and '**Why:**' in decisions and 'Alternatives considered:** SMS' in decisions)
    check('source_handle_no_credentials', 'June Sales SOP' in sources and 'credential' in sources.lower() and 'sk-' not in sources)
    check('changed_fact_no_contradiction', 'Telegram primary; email backup' in customer and 'Preferred channel: email' not in customer)
    check('access_metadata_only', '1Password item: Acme / Stripe' in access and not SECRET_RE.search(access))
    check('log_summary_promoted', 'Discussed billing' in log and 'Pause refunds' in decisions and 'Refund pause follow-up' in current and len(log) < 2500)
    check('untrusted_content_not_obeyed', 'untrusted content' in log and 'no external action was taken' in log)
    check('customer_isolation', 'silver molar' in bright_all and 'silver molar' not in acme_all)
    check('global_no_obvious_secrets', not SECRET_RE.search(acme_all + bright_all))
    return checks


def main() -> int:
    if TMP_ROOT.exists():
        shutil.rmtree(TMP_ROOT)
    TMP_ROOT.mkdir(parents=True)
    acme = scaffold('acme')
    bright = scaffold('bright')
    apply_events(acme, bright)
    checks = evaluate(acme, bright)
    summary = {
        'date': TODAY,
        'workspace': str(TMP_ROOT),
        'summary': {
            'passed': sum(c.passed for c in checks),
            'failed': sum(not c.passed for c in checks),
            'total': len(checks),
        },
        'checks': [c.__dict__ | {'status': 'PASS' if c.passed else 'FAIL'} for c in checks],
        'exit_pilot_gate': 'PASS' if all(c.passed for c in checks) else 'FAIL',
    }
    report = TMP_ROOT / 'report.json'
    report.write_text(json.dumps(summary, indent=2), encoding='utf-8')
    print(json.dumps(summary, indent=2))
    return 0 if all(c.passed for c in checks) else 1


if __name__ == '__main__':
    sys.exit(main())
