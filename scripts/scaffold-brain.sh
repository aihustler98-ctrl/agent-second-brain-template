#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 /path/to/agent/workspace" >&2
  exit 2
fi

TARGET="$1"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SRC="$REPO_ROOT/templates/brain"
DEST="$TARGET/brain"

if [ ! -d "$SRC" ]; then
  echo "Template not found: $SRC" >&2
  exit 1
fi

if [ -e "$DEST" ]; then
  echo "Refusing to overwrite existing brain: $DEST" >&2
  exit 1
fi

mkdir -p "$TARGET"
cp -R "$SRC" "$DEST"

TODAY="$(date +%F)"
find "$DEST" -type f -name '*.md' -print0 | xargs -0 sed -i.bak "s/YYYY-MM-DD/$TODAY/g"
find "$DEST" -type f -name '*.bak' -delete
if [ -f "$DEST/log/$TODAY.md" ]; then
  :
elif [ -f "$DEST/log/YYYY-MM-DD.md" ]; then
  mv "$DEST/log/YYYY-MM-DD.md" "$DEST/log/$TODAY.md"
fi

echo "Created $DEST"
