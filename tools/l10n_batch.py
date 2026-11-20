#!/usr/bin/env python3
"""l10n_batch.py — 取出 base 資源檔中「尚未翻譯」的條目，供逐批翻譯。

用法：
    python3 tools/l10n_batch.py --start 0 --count 100    # 印出下一批（含英文原文與指引）
    python3 tools/l10n_batch.py --stats                  # 進度統計
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
BASE = REPO_ROOT / "app/src/main/res/values/strings.xml"
TRANSLATIONS_DIR = REPO_ROOT / "l10n/translations"

BLOCK_RE = re.compile(
    r'<string\s+name="(?P<name>[^"]+)"(?P<attrs>[^>]*)>(?P<text>.*?)</string>', re.S
)
PLURALS_RE = re.compile(
    r'<plurals\s+name="(?P<name>[^"]+)"(?P<attrs>[^>]*)>(?P<body>.*?)</plurals>', re.S
)
ITEM_RE = re.compile(r'<item\s+quantity="(?P<q>[^"]+)"[^>]*>(?P<text>.*?)</item>', re.S)


def load_done() -> set[str]:
    done: set[str] = set()
    if TRANSLATIONS_DIR.is_dir():
        for path in TRANSLATIONS_DIR.glob("*.json"):
            done.update(json.loads(path.read_text(encoding="utf-8")).keys())
    return done


def entries() -> list[dict]:
    text = BASE.read_text(encoding="utf-8")
    items: list[dict] = []
    for m in BLOCK_RE.finditer(text):
        attrs = m.group("attrs")
        comment = re.search(r'comment="([^"]*)"', attrs)
        items.append({
            "name": m.group("name"),
            "comment": comment.group(1) if comment else "",
            "en": m.group("text"),
            "type": "string",
        })
    for m in PLURALS_RE.finditer(text):
        attrs = m.group("attrs")
        comment = re.search(r'comment="([^"]*)"', attrs)
        items.append({
            "name": m.group("name"),
            "comment": comment.group(1) if comment else "",
            "en": {i.group("q"): i.group("text") for i in ITEM_RE.finditer(m.group("body"))},
            "type": "plurals",
        })
    return items


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--count", type=int, default=100)
    parser.add_argument("--stats", action="store_true")
    args = parser.parse_args()

    all_items = entries()
    done = load_done()
    pending = [i for i in all_items if i["name"] not in done]

    if args.stats:
        print(f"總計 {len(all_items)} 條　已翻 {len(all_items) - len(pending)}　待翻 {len(pending)}")
        return 0

    batch = pending[args.start: args.start + args.count]
    print(f"# 待翻批次：第 {args.start + 1}–{args.start + len(batch)} 條（共 {len(pending)} 條待翻）\n")
    for item in batch:
        print(f"### {item['name']}")
        if item["comment"]:
            print(f"# 指引: {item['comment']}")
        if item["type"] == "string":
            print(f"EN: {item['en']}")
        else:
            for q, t in item["en"].items():
                print(f"EN[{q}]: {t}")
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
