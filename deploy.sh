#!/bin/bash
# 把本地 SK海力士预警台的最新快照发布到 GitHub Pages。
# 由本地 server.py 每次刷新完成后自动调用，也可手动执行。
set -euo pipefail

export PATH="/Users/midongkeji/.agent-reach/tools/bin:/usr/bin:/bin:/usr/sbin:/sbin"

SITE_DIR="/Users/midongkeji/Library/Application Support/SKHynixRiskMonitor/public-site"
cd "$SITE_DIR"

python3 "$SITE_DIR/patch_site.py"

git add -A
if git diff --cached --quiet; then
  echo "no-change"
  exit 0
fi

STAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)
git commit -q -m "snapshot ${STAMP}"

# 云端 GitHub Actions 也会推同一仓库：先合并再推，冲突时以本地新快照为准，最多重试 3 次
for i in 1 2 3; do
  if git pull --no-rebase -X ours --no-edit -q origin main && git push -q origin main; then
    echo "deployed ${STAMP}"
    exit 0
  fi
  sleep 5
done
echo "push failed after retries" >&2
exit 1
