#!/bin/bash
# 把本地 SK海力士预警台的最新快照发布到 GitHub Pages。
# 由本地 server.py 每次刷新完成后自动调用，也可手动执行。
set -euo pipefail

export PATH="/Users/midongkeji/.agent-reach/tools/bin:/usr/bin:/bin:/usr/sbin:/sbin"

SITE_DIR="/Users/midongkeji/Documents/kimi/workspace/skhynix-public"
cd "$SITE_DIR"

python3 "$SITE_DIR/patch_site.py"

git add -A
if git diff --cached --quiet; then
  echo "no-change"
  exit 0
fi

STAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)
git commit -q -m "snapshot ${STAMP}"
git push -q origin main
echo "deployed ${STAMP}"
