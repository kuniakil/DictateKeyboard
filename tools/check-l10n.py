#!/usr/bin/env python3
"""check-l10n.py — 驗證 values-zh-rTW 的資源檔與 base 完全對齊。

這是工作表 Phase B0b / B5 的驗證腳本（見 docs/worksheet-dictatekeyboard-zhtw-ui-20261120.md）。

檢查項目
--------
1. XML 合法性（每個檔案都要能 parse）
2. key 集合：locale 有沒有漏譯（missing）或多出 base 沒有的 key（extra）
3. placeholder：每個兩邊都有的 key，{name} / %1$s / %s 是否逐條一致
4. comment 屬性：base 有 comment 的條目，locale 是不是保留了（翻譯指引不能丟）
5. plurals：plurals 名稱與 quantity 結構是否一致

用法
----
    python3 tools/check-l10n.py                # app + wear，寬鬆（允許尚未翻完）
    python3 tools/check-l10n.py --strict       # 任何 missing / placeholder 不符 → exit 1
    python3 tools/check-l10n.py --module app   # 只驗 app
    python3 tools/check-l10n.py --locale values-zh-rTW

寬鬆模式是為了 B0 階段：最小可行資源檔本來就只含幾十條，其餘刻意留空讓未翻的退回英文。
B5 要用 --strict（key 集合必須與 base 完全一致）。
"""

from __future__ import annotations

import argparse
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# {app_name} / {count} / {size}
PLACEHOLDER_NAME = re.compile(r"\{[A-Za-z_][A-Za-z0-9_]*\}")
# %1$s / %2$d / %s / %d
PLACEHOLDER_POSITIONAL = re.compile(r"%(?:(\d+)\$)?[sdf]")
# Android 資源裡的轉義撇號 \' —— 不影響 placeholder 比對，但要先從比對字串裡排除
ANDROID_ESCAPED_QUOTE = re.compile(r"\\'")


class Module:
    """一個待驗證的模組（app 或 wear）。"""

    def __init__(self, name: str, base_dir: Path):
        self.name = name
        self.base_dir = base_dir


MODULES = [
    Module("app", REPO_ROOT / "app/src/main/res"),
    Module("wear", REPO_ROOT / "wear/src/main/res"),
]


class ParsedResource:
    """一個資源目錄的解析結果。"""

    def __init__(self, path: Path):
        self.path = path
        self.strings: dict[str, str] = {}
        self.plurals: dict[str, dict[str, str]] = {}
        self.comments: dict[str, str] = {}
        self.plural_comments: dict[str, str] = {}
        self.error: str | None = None

        try:
            root = ET.parse(path).getroot()
        except ET.ParseError as exc:
            self.error = f"XML 不合法: {exc}"
            return
        except FileNotFoundError:
            self.error = "檔案不存在"
            return

        for elem in root:
            if elem.tag == "string":
                name = elem.get("name")
                if name is None:
                    continue
                self.strings[name] = "".join(elem.itertext())
                comment = elem.get("comment")
                if comment:
                    self.comments[name] = comment
            elif elem.tag == "plurals":
                name = elem.get("name")
                if name is None:
                    continue
                items: dict[str, str] = {}
                for item in elem.findall("item"):
                    quantity = item.get("quantity")
                    if quantity is not None:
                        items[quantity] = "".join(item.itertext())
                self.plurals[name] = items
                comment = elem.get("comment")
                if comment:
                    self.plural_comments[name] = comment

    @property
    def total_comments(self) -> int:
        """string + plurals 合計的翻譯指引數。

        base 的 1618 是這個數（1614 條在 <string>、4 條在 <plurals>）。
        用 grep -o ' comment="' 數會把 XML 註解裡的字串也算進去，所以以本屬性為準。
        """
        return len(self.comments) + len(self.plural_comments)


def placeholders(text: str) -> set[str]:
    """取出文字中所有的 placeholder。

    回傳的集合用來比對「同一個 key 在 base 與 locale 是否用了相同的 placeholder」。
    """
    normalized = ANDROID_ESCAPED_QUOTE.sub("", text)
    found = set(PLACEHOLDER_NAME.findall(normalized))
    for match in PLACEHOLDER_POSITIONAL.finditer(normalized):
        index = match.group(1)
        kind = match.group(0)[-1]
        found.add(f"%{index or ''}${kind}")
    return found


def check_module(module: Module, locale_dirname: str, strict: bool) -> tuple[list[str], list[str]]:
    """回傳 (errors, warnings)。errors 非空代表驗證失敗。"""
    errors: list[str] = []
    warnings: list[str] = []

    base_path = module.base_dir / "values" / "strings.xml"
    locale_path = module.base_dir / locale_dirname / "strings.xml"

    if not base_path.is_file():
        errors.append(f"[{module.name}] 找不到 base 檔案: {base_path}")
        return errors, warnings

    base = ParsedResource(base_path)
    locale = ParsedResource(locale_path)

    if base.error:
        errors.append(f"[{module.name}] base 解析失敗: {base.error}")
        return errors, warnings

    # 寬鬆模式下 locale 檔案可能還不存在（尚未翻譯）
    if locale.error:
        if locale.error == "檔案不存在":
            msg = f"[{module.name}] locale 尚未建立: {locale_path}"
            (errors if strict else warnings).append(msg)
            return errors, warnings
        errors.append(f"[{module.name}] locale 解析失敗: {locale.error}")
        return errors, warnings

    # --- 1. key 集合 ---
    base_names = set(base.strings) | set(base.plurals)
    locale_names = set(locale.strings) | set(locale.plurals)
    missing = sorted(base_names - locale_names)
    extra = sorted(locale_names - base_names)

    if extra:
        errors.append(
            f"[{module.name}] locale 有 {len(extra)} 個 base 沒有的 key: "
            + ", ".join(extra[:10])
            + (" ..." if len(extra) > 10 else "")
        )

    if missing:
        msg = (
            f"[{module.name}] 有 {len(missing)} / {len(base_names)} 個 key 尚未翻譯"
            f"（base 共 {len(base.strings)} strings + {len(base.plurals)} plurals）"
        )
        if strict:
            errors.append(msg + " —— strict 模式要求 key 集合完全一致")
            errors.append("    缺少: " + ", ".join(missing[:15]) + (" ..." if len(missing) > 15 else ""))
        else:
            warnings.append(msg + " —— 寬鬆模式，這是預期中的（B0 階段刻意留空）")

    # --- 2. placeholder ---
    mismatch = 0
    for name in sorted(set(base.strings) & set(locale.strings)):
        base_ph = placeholders(base.strings[name])
        locale_ph = placeholders(locale.strings[name])
        if base_ph != locale_ph:
            mismatch += 1
            errors.append(
                f"[{module.name}] placeholder 不符 @ {name}: "
                f"base={sorted(base_ph)} locale={sorted(locale_ph)}"
            )
    # --- 3. comment 屬性保留 ---
    common = set(base.strings) & set(locale.strings)
    dropped = [n for n in sorted(common) if n in base.comments and n not in locale.comments]
    dropped += [
        n for n in sorted(set(base.plurals) & set(locale.plurals))
        if n in base.plural_comments and n not in locale.plural_comments
    ]
    if dropped:
        warnings.append(
            f"[{module.name}] {len(dropped)} 個已翻的條目丟掉了 base 的 comment 翻譯指引"
            f"（base 共 {base.total_comments} 條有指引）: " + ", ".join(dropped[:10])
            + (" ..." if len(dropped) > 10 else "")
        )

    # --- 4. plurals 結構 ---
    for name in sorted(set(base.plurals) & set(locale.plurals)):
        base_q = set(base.plurals[name])
        locale_q = set(locale.plurals[name])
        if base_q != locale_q:
            errors.append(
                f"[{module.name}] plurals quantity 不符 @ {name}: "
                f"base={sorted(base_q)} locale={sorted(locale_q)}"
            )
        for quantity, text in base.plurals[name].items():
            if quantity in locale.plurals[name]:
                base_ph = placeholders(text)
                locale_ph = placeholders(locale.plurals[name][quantity])
                if base_ph != locale_ph:
                    errors.append(
                        f"[{module.name}] plural placeholder 不符 @ {name}[{quantity}]: "
                        f"base={sorted(base_ph)} locale={sorted(locale_ph)}"
                    )

    # --- 摘要 ---
    print(
        f"  [{module.name}] base {len(base.strings)} strings + {len(base.plurals)} plurals"
        f"（comment {base.total_comments} 條）"
        f" | locale {len(locale.strings)} strings + {len(locale.plurals)} plurals"
        f"（comment {locale.total_comments} 條）"
        f" | 已對齊 {len(set(base.strings) & set(locale.strings))} strings"
        f" + {len(set(base.plurals) & set(locale.plurals))} plurals"
    )
    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="驗證 zh-TW 資源檔與 base 對齊")
    parser.add_argument("--strict", action="store_true", help="任何漏譯都視為錯誤（B5 用）")
    parser.add_argument("--module", choices=["app", "wear", "all"], default="all")
    parser.add_argument("--locale", default="values-zh-rTW", help="locale 資源目錄名稱")
    args = parser.parse_args()

    modules = [m for m in MODULES if args.module in ("all", m.name)]

    all_errors: list[str] = []
    all_warnings: list[str] = []

    print(f"檢查 locale 目錄: {args.locale}　模式: {'strict' if args.strict else '寬鬆'}")
    for module in modules:
        errors, warnings = check_module(module, args.locale, args.strict)
        all_errors.extend(errors)
        all_warnings.extend(warnings)

    if all_warnings:
        print("\n⚠️ 警告")
        for warning in all_warnings:
            print(f"  - {warning}")

    if all_errors:
        print("\n❌ 錯誤")
        for error in all_errors:
            print(f"  - {error}")
        print(f"\n驗證失敗：{len(all_errors)} 個錯誤")
        return 1

    print("\n✅ 驗證通過")
    return 0


if __name__ == "__main__":
    sys.exit(main())
