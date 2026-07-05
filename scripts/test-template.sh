#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMP="${TMPDIR:-/tmp}/agent-second-brain-template-test-$$"
TODAY="$(date +%F)"

fail() {
  echo "FAIL: $*" >&2
  exit 1
}

pass() {
  echo "PASS: $*"
}

cleanup() {
  rm -rf "$TMP"
}
trap cleanup EXIT

cd "$ROOT"

required_repo_files=(
  README.md
  LICENSE
  .gitignore
  prompts/second-brain-system-block.md
  docs/maintenance-loop.md
  docs/gbrain-integration.md
  scripts/scaffold-brain.sh
  templates/brain/customer.md
  templates/brain/constraints.md
  templates/brain/current.md
  templates/brain/sources.md
  templates/brain/context/business.md
  templates/brain/context/projects.md
  templates/brain/context/tools.md
  templates/brain/context/access.md
  templates/brain/decisions.md
  templates/brain/learnings.md
  templates/brain/log/YYYY-MM-DD.md
  templates/brain/_meta.md
)

for f in "${required_repo_files[@]}"; do
  [[ -f "$f" ]] || fail "missing required file: $f"
done
pass "required repo files exist"

[[ -x scripts/scaffold-brain.sh ]] || fail "scaffold script is not executable"
pass "scaffold script executable"

# Template should not contain obvious secret material. This is intentionally conservative.
secret_pattern='(sk-[A-Za-z0-9_-]{20,}|gh[pousr]_[A-Za-z0-9_]{20,}|xox[baprs]-[A-Za-z0-9-]{20,}|AKIA[0-9A-Z]{16}|-----BEGIN (RSA |OPENSSH |EC |DSA )?PRIVATE KEY-----|password\s*[:=]\s*[^[:space:]<]+|api[_-]?key\s*[:=]\s*[^[:space:]<]+|token\s*[:=]\s*[^[:space:]<]+)'
if grep -REIn "$secret_pattern" templates prompts docs scripts README.md .gitignore LICENSE >/tmp/agent_second_brain_secret_hits.$$ 2>/dev/null; then
  cat /tmp/agent_second_brain_secret_hits.$$ >&2
  rm -f /tmp/agent_second_brain_secret_hits.$$
  fail "potential secret-like content found"
fi
rm -f /tmp/agent_second_brain_secret_hits.$$
pass "no obvious secret-like content"

mkdir -p "$TMP"
scripts/scaffold-brain.sh "$TMP/workspace" >/tmp/agent_second_brain_scaffold.$$ || fail "scaffold script failed"
grep -q "Created $TMP/workspace/brain" /tmp/agent_second_brain_scaffold.$$ || fail "scaffold output did not report created brain"
rm -f /tmp/agent_second_brain_scaffold.$$

required_brain_files=(
  customer.md
  constraints.md
  current.md
  sources.md
  context/business.md
  context/projects.md
  context/tools.md
  context/access.md
  decisions.md
  learnings.md
  log/${TODAY}.md
  _meta.md
)

for f in "${required_brain_files[@]}"; do
  [[ -f "$TMP/workspace/brain/$f" ]] || fail "scaffold missing brain file: $f"
done
pass "scaffold creates required brain files"

if grep -R "YYYY-MM-DD" "$TMP/workspace/brain" >/tmp/agent_second_brain_date_hits.$$ 2>/dev/null; then
  cat /tmp/agent_second_brain_date_hits.$$ >&2
  rm -f /tmp/agent_second_brain_date_hits.$$
  fail "scaffold left YYYY-MM-DD placeholders"
fi
rm -f /tmp/agent_second_brain_date_hits.$$
pass "scaffold replaces date placeholders"

# Refuse overwrite.
if scripts/scaffold-brain.sh "$TMP/workspace" >/tmp/agent_second_brain_overwrite.$$ 2>&1; then
  cat /tmp/agent_second_brain_overwrite.$$ >&2
  rm -f /tmp/agent_second_brain_overwrite.$$
  fail "scaffold overwrote existing brain"
fi
rm -f /tmp/agent_second_brain_overwrite.$$
pass "scaffold refuses overwrite"

# Startup prompt must name the required startup files.
for f in customer.md constraints.md current.md _meta.md; do
  grep -q "brain/$f" prompts/second-brain-system-block.md || fail "prompt missing startup file brain/$f"
done
pass "system prompt includes startup read files"

# Constraints must include the most important customer-agent guardrails.
grep -qi "approval" templates/brain/constraints.md || fail "constraints template missing approval language"
grep -qi "Never store secrets" templates/brain/constraints.md || fail "constraints template missing no-secrets language"
grep -qi "untrusted content" templates/brain/constraints.md || fail "constraints template missing untrusted-content language"
pass "constraints template includes core guardrails"

# Access template must be metadata-only.
grep -qi "Never paste secrets" templates/brain/context/access.md || fail "access template missing secret warning"
grep -qi "Credential location" templates/brain/context/access.md || fail "access template missing credential-location column"
pass "access template is metadata-only"

# GBrain doc must state markdown wins on conflict.
grep -qi "files win" docs/gbrain-integration.md || fail "gbrain doc missing conflict rule"
pass "GBrain conflict rule documented"

echo "ALL TESTS PASSED"
