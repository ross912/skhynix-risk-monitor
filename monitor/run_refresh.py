#!/usr/bin/env python3
"""云端 Runner：不启动 HTTP 服务，只执行一轮抓取 + 计算并落盘 state.json。

在 GitHub Actions 中运行；monitor.py 是本地 server.py 的原样拷贝，
DATA_DIR 自动指向本目录下的 data/（随仓库提交，保证缓存与证据历史连续）。
"""
import shutil
import sys
from pathlib import Path

MONITOR_DIR = Path(__file__).resolve().parent
REPO_ROOT = MONITOR_DIR.parent
sys.path.insert(0, str(MONITOR_DIR))

import monitor  # noqa: E402

state = monitor.refresh_data(trigger="github-actions")
if not state.get("summary"):
    error = state.get("error") or (state.get("runtime") or {}).get("last_error")
    raise SystemExit(f"refresh failed: {error}")

shutil.copyfile(MONITOR_DIR / "data" / "state.json", REPO_ROOT / "state.json")
print("state generated_at:", state["generated_at"])
