"""Send a compact Horizon daily digest to a Discord webhook.

Why this exists: Horizon's built-in webhook delivery either sends one big
message that exceeds Discord's 2000-char limit (summary mode) or N+1 separate
messages (summary_and_items mode). Neither matches the "single compact
message with clickable links" UX we want.

This script:
  1. Reads today's saved Markdown summary from data/summaries/
  2. Parses each item's title + real URL + AI score
  3. Converts Simplified Chinese → Traditional (Taiwan) via OpenCC s2twp
  4. Sends ONE Discord embed message (table-card feel, no link unfurls)

Run AFTER `horizon` (which produces the summary file).
Requires .env to be loaded for HORIZON_WEBHOOK_URL.
"""

from __future__ import annotations

import os
import re
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

import httpx
from dotenv import load_dotenv
from opencc import OpenCC

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

WEBHOOK_URL = os.environ.get("HORIZON_WEBHOOK_URL")
# 第二發送目的地（選用，例：另一個 Discord 頻道）。兩個都設就同時發。
WEBHOOK_URL_2 = os.environ.get("HORIZON_WEBHOOK_URL_2")
LANG = os.environ.get("DISCORD_DIGEST_LANG", "zh")
MAX_ITEMS = int(os.environ.get("DISCORD_DIGEST_MAX", "20"))
USERNAME = os.environ.get("DISCORD_DIGEST_USERNAME", "Horizon AI Daily")
TZ_HOURS = int(os.environ.get("DISCORD_DIGEST_TZ_HOURS", "8"))   # Asia/Taipei

# Embed color: a calm sunrise-blue (like the 🌅 vibe)
EMBED_COLOR = 0x5865F2

if not WEBHOOK_URL:
    print("HORIZON_WEBHOOK_URL not set", file=sys.stderr)
    sys.exit(2)

# Today in user's timezone (so 00:30 UTC = 08:30 Taipei still reads "today")
tz = timezone(timedelta(hours=TZ_HOURS))
today = datetime.now(tz).strftime("%Y-%m-%d")

summary_file = ROOT / "data" / "summaries" / f"horizon-{today}-{LANG}.md"
if not summary_file.exists():
    candidates = sorted((ROOT / "data" / "summaries").glob(f"horizon-*-{LANG}.md"))
    if not candidates:
        print(f"No summary file found in data/summaries/ for lang={LANG}", file=sys.stderr)
        sys.exit(3)
    summary_file = candidates[-1]
    print(f"Today's file missing, falling back to {summary_file.name}", file=sys.stderr)

text = summary_file.read_text(encoding="utf-8")

# Match item headings: ## [Title](https://...) ⭐️ 9.0/10
item_pattern = re.compile(
    r"^##\s+\[(?P<title>[^\]]+)\]\((?P<url>https?://[^)]+)\)\s+⭐️?\s*(?P<score>\d+\.\d+)/10",
    re.MULTILINE,
)
items = [
    {"title": m.group("title").strip(), "url": m.group("url"), "score": float(m.group("score"))}
    for m in item_pattern.finditer(text)
]

if not items:
    print(f"No items parsed from {summary_file.name}", file=sys.stderr)
    sys.exit(4)

items.sort(key=lambda it: it["score"], reverse=True)
top = items[:MAX_ITEMS]

# Convert Simplified → Traditional (Taiwan phrases). LANG must be "zh" for this
# to matter; if user adds zh-only output we always do s2twp to be safe.
cc = OpenCC("s2twp") if LANG == "zh" else None

def to_tw(s: str) -> str:
    return cc.convert(s) if cc else s

# Format B+1: "⭐ `9.0` | [標題](url)" — pipe separator visible like a table,
# score wrapped in inline code so digit widths align (9.0 vs 10.0 same width),
# clickable title link.
header_label = "🌅 Horizon AI 速遞" if LANG == "zh" else "🌅 Horizon AI Daily"
title = to_tw(f"{header_label} · {today}")
subtitle = to_tw(f"{len(top)} 條精選 · 按 AI 評分排序" if LANG == "zh" else f"{len(top)} items · sorted by AI score")

lines = []
for it in top:
    score_str = f"⭐`{it['score']:.1f}`"   # no space between emoji and score
    title_tw = to_tw(it["title"])
    lines.append(f"{score_str} | [{title_tw}]({it['url']})")

description = subtitle + "\n\n" + "\n".join(lines)

# Discord embed description limit is 4096 chars. Trim from bottom if needed.
while len(description) > 4000 and len(lines) > 3:
    lines.pop()
    description = subtitle + "\n\n" + "\n".join(lines) + "\n_…已截斷_"

embed = {
    "title": title,
    "description": description,
    "color": EMBED_COLOR,
    "footer": {"text": f"來源：Hacker News · Reddit · RSS · GitHub · OSSInsight · Powered by Horizon"},
    "timestamp": datetime.now(timezone.utc).isoformat(),
}

payload = {
    "username": USERNAME,
    "embeds": [embed],
}

# 發到所有設定的目的地（原 webhook + 選用的第二個）。逐一發送、逐一報狀態，
# 任一個失敗就 exit 5，但不影響其他目的地的發送。
targets = [u for u in (WEBHOOK_URL, WEBHOOK_URL_2) if u]
failed = 0
for i, url in enumerate(targets, 1):
    resp = httpx.post(url, json=payload, timeout=30.0)
    print(f"Discord POST [{i}/{len(targets)}] status={resp.status_code} desc_len={len(description)} items={len(top)}")
    if resp.status_code >= 300:
        print(f"  Response body [{i}]:", resp.text[:500], file=sys.stderr)
        failed += 1

if failed:
    sys.exit(5)
