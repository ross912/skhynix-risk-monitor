#!/usr/bin/env python3
"""把本地版 index.html 转成公网静态版，并拷贝最新 state.json。

公网端是 GitHub Pages 纯静态托管：
- /api/state  → ./state.json（加时间戳查询参数绕过 CDN 缓存）
- /api/refresh → 重新加载页面（公网端无法触发本地抓取）
"""
import shutil
from pathlib import Path

SRC_DIR = Path("/Users/midongkeji/Library/Application Support/SKHynixRiskMonitor")
SITE_DIR = Path(__file__).resolve().parent

html = (SRC_DIR / "index.html").read_text(encoding="utf-8")

REPLACEMENTS = [
    # 数据接口 → 静态 JSON
    (
        'fetch("/api/state", { cache: "no-store" })',
        'fetch("./state.json?t=" + Date.now(), { cache: "no-store" })',
    ),
    # 手动刷新按钮 → 重新加载页面
    (
        'var response = await fetch("/api/refresh", { method: "POST", cache: "no-store" });',
        'showToast("公网快照由本地服务定时发布，正在重新加载…"); location.reload(); return;',
    ),
    # 文案：去掉"本地服务"说法
    ("正在读取本地快照", "正在读取最新快照"),
    ("已读取最新本地快照", "已读取最新快照"),
    (
        '无法连接本地数据服务：" + error.message',
        '暂时无法加载公开快照：" + error.message',
    ),
    (
        "请点击右上角“立即刷新”，或确认本地服务正在运行。",
        "公网快照由本地预警服务定时发布，请稍后刷新重试。",
    ),
]

for old, new in REPLACEMENTS:
    if old not in html:
        raise SystemExit(f"patch failed, pattern not found: {old[:60]}")
    html = html.replace(old, new, 1)

# 个人监控页，避免被搜索引擎收录
if '<meta name="robots"' not in html:
    anchor = '<meta name="viewport" content="width=device-width, initial-scale=1">'
    if anchor not in html:
        raise SystemExit("patch failed: viewport meta not found")
    html = html.replace(
        anchor,
        anchor + '\n  <meta name="robots" content="noindex, nofollow">',
        1,
    )

(SITE_DIR / "index.html").write_text(html, encoding="utf-8")
shutil.copyfile(SRC_DIR / "data" / "state.json", SITE_DIR / "state.json")
print("site files updated")
