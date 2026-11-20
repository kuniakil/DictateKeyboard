#!/usr/bin/env python3
"""build-zh-tw-strings.py — 從 base 資源檔 + 譯文 JSON 產生 values-zh-rTW/strings.xml。

設計原則：**以 base 檔為骨架做文字層替換**，而不是重新組出 XML。
好處是自動保留：
  - 所有 `comment="..."` 翻譯指引（1618 條）
  - 元素順序、XML 註解（77 條分段註解）
  - 內嵌標記（`<b>` / `<i>`）
  - `tools:ignore="MissingTranslation"` 等屬性

譯文來源：`l10n/translations/*.json`（每個檔案一批，格式 {"key": "譯文"}，
plurals 則為 {"key": {"one": "...", "other": "..."}}）。

用法：
    python3 tools/build-zh-tw-strings.py              # 產生資源檔
    python3 tools/build-zh-tw-strings.py --check      # 只檢查不寫檔
    python3 tools/build-zh-tw-strings.py --strict     # 有缺譯就失敗（B5 用）
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
BASE = REPO_ROOT / "app/src/main/res/values/strings.xml"
OUT = REPO_ROOT / "app/src/main/res/values-zh-rTW/strings.xml"
TRANSLATIONS_DIR = REPO_ROOT / "l10n/translations"
WEAR_BASE = REPO_ROOT / "wear/src/main/res/values/strings.xml"
WEAR_OUT = REPO_ROOT / "wear/src/main/res/values-zh-rTW/strings.xml"
WEAR_TRANSLATIONS = REPO_ROOT / "l10n/wear-zh-tw.json"

STRING_RE = re.compile(
    r'(?P<head><string\s+name="(?P<name>[^"]+)"(?P<attrs>[^>]*?)>)(?P<text>.*?)(?P<tail></string>)',
    re.S,
)
PLURALS_RE = re.compile(
    r'(?P<head><plurals\s+name="(?P<name>[^"]+)"(?P<attrs>[^>]*?)>)(?P<body>.*?)(?P<tail></plurals>)',
    re.S,
)
ITEM_RE = re.compile(
    r'(?P<head><item\s+quantity="(?P<q>[^"]+)"(?P<attrs>[^>]*?)>)(?P<text>.*?)(?P<tail></item>)',
    re.S,
)


def escape(text: str) -> str:
    """把譯文轉成 Android 資源檔可接受的形式，同時保留內嵌 <b>/<i>/<u> 標記。"""
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = re.sub(r"&lt;(/?[biu])&gt;", r"<\1>", text)
    # Android 要求撇號跳脫（否則 aapt 報 "Apostrophe not preceded by \\"）
    text = re.sub(r"(?<!\\)'", r"\\'", text)
    return text


def load_translations() -> dict:
    merged: dict = {}
    if not TRANSLATIONS_DIR.is_dir():
        return merged
    for path in sorted(TRANSLATIONS_DIR.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        for key, value in data.items():
            if key in merged:
                print(f"⚠️ 重複的 key（後者覆蓋前者）: {key}  （{path.name}）")
            merged[key] = value
    return merged


def build(translations: dict, base_text: str) -> tuple[str, list[str], list[str]]:
    """回傳 (產出內容, 缺少翻譯的 key, 找到但 base 沒有的 key)。"""
    missing: list[str] = []
    used: set[str] = set()

    def repl_string(match: re.Match) -> str:
        name = match.group("name")
        used.add(name)
        if name not in translations:
            missing.append(name)
            return match.group(0)  # 未翻譯者原樣保留（讓 base 值退回英文）
        value = translations[name]
        if not isinstance(value, str):
            raise TypeError(f"{name}: 譯文必須是字串")
        return match.group("head") + escape(value) + match.group("tail")

    def repl_plurals(match: re.Match) -> str:
        name = match.group("name")
        used.add(name)
        if name not in translations:
            missing.append(name)
            return match.group(0)
        items = translations[name]
        if not isinstance(items, dict):
            raise TypeError(f"{name}: plurals 譯文必須是 {{quantity: text}} 物件")

        def repl_item(item_match: re.Match) -> str:
            q = item_match.group("q")
            if q not in items:
                missing.append(f"{name}[{q}]")
                return item_match.group(0)
            return item_match.group("head") + escape(items[q]) + item_match.group("tail")

        body = ITEM_RE.sub(repl_item, match.group("body"))
        return match.group("head") + body + match.group("tail")

    out = STRING_RE.sub(repl_string, base_text)
    out = PLURALS_RE.sub(repl_plurals, out)

    extra = sorted(set(translations) - used)
    return out, missing, extra


def process_module(
    label: str,
    base_path: Path,
    out_path: Path,
    translations: dict,
    check: bool,
    strict: bool,
) -> bool:
    """建置並檢查單一模組的資源檔；回傳是否有缺譯。"""
    base_text = base_path.read_text(encoding="utf-8")
    out, missing, extra = build(translations, base_text)

    total = len(set(re.findall(r'<(?:string|plurals)\s+name="([^"]+)"', base_text)))
    print(f"[{label}] base 條目: {total}　已翻譯: {total - len([m for m in missing if '[' not in m])}　缺: {len(missing)}")

    if extra:
        print(f"⚠️ [{label}] 譯文檔有 {len(extra)} 個 base 沒有的 key: {extra[:10]}")
    if missing:
        print(f"[{label}] 尚未翻譯 {len(missing)} 條，例如: {missing[:8]}")

    if not check and not (strict and missing):
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(out, encoding="utf-8")
        print(f"✅ 已寫入 {out_path.relative_to(REPO_ROOT)}")

    return bool(missing)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="只檢查不寫檔")
    parser.add_argument("--strict", action="store_true", help="有缺譯就 exit 1")
    args = parser.parse_args()

    has_missing = process_module(
        "app", BASE, OUT, load_translations(), args.check, args.strict
    )

    if WEAR_TRANSLATIONS.is_file():
        wear_data = json.loads(WEAR_TRANSLATIONS.read_text(encoding="utf-8"))
        if process_module("wear", WEAR_BASE, WEAR_OUT, wear_data, args.check, args.strict):
            has_missing = True
    else:
        print(f"⚠️ [wear] 尚未建立 {WEAR_TRANSLATIONS.relative_to(REPO_ROOT)}，略過")
        if args.strict:
            has_missing = True

    if args.strict and has_missing:
        print("❌ strict 模式：仍有缺譯")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
