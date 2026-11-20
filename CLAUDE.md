# CLAUDE.md — DictateKeyboard 繁體中文（zh-TW）在地化

本 repo 是 `DevEmperor/DictateKeyboard` 的 fork。

> **⚠️ 當前狀態（2026-11-20）**：**繁體中文（台灣）介面已全部完成**（app 2547 strings + 11 plurals、wear 69 條、台灣用語校訂、實機驗收、雲端出包、簽章備份）。
> **上游互動停在「等作者回覆」**：已於 [#483](https://github.com/DevEmperor/DictateKeyboard/issues/483) 留言並開立 Issue **[#492](https://github.com/DevEmperor/DictateKeyboard/issues/492)**，**PR 尚未開立**（上游 `author:kuniakil` 的 PR 數 = 0）。
> **📌 已定案（2026-11-20）：不搶先開 PR，等作者回覆。** 分支 `pr/zh-tw-ui` 維持待命，作者回覆歡迎時再開（文案 = `docs/upstream-outreach-drafts-20261120.md` 的 **Draft 3**）。等待期間推進 Phase F。詳見工作表 Part 0「📌 2026-11-20 決策」節與「作者回覆後的應對決策表」（情境 1–7）。

> 相同內容另有 `AGENTS.md`（給 opencode / Antigravity 用）。兩份內容同步。

## 立刻先讀

**`docs/worksheet-dictatekeyboard-zhtw-ui-20261120.md`** —— 完整工作表。內含：

- **Part 0 交接說明** —— 當前狀態、下一步、不要再踩的坑 ⬅️ **先看這裡**
- Part 1 調查結果（三個決定性發現、工程事實、台灣用語表、2026-11-17 操盤歷史查證、簽章金鑰、分支架構）
- Part 2 計畫（Phase A–F，每項都是可勾選的 checkbox）
- Part 3 風險、Part 4 已定案事項、Part 5 可重跑的驗證指令

**不要重做調查** —— 關鍵事實都已在工作表內驗證過（上游 locale 結構、app 語言選擇器位置、2547 條資源數量、簽章金鑰位置…）。

## Repo 拓撲

| remote | 指向 | 用途 |
|---|---|---|
| `origin` | `kuniakil/DictateKeyboard`（我們的 fork） | 推送分支、開 PR 的來源 |
| `upstream` | `DevEmperor/DictateKeyboard`（上游） | 追蹤上游更新、PR 的目標 |

分支：
- `main` = 我們的**發行分支** = `upstream/main` + 我們的 CI workflow + docs。**已 merge 上游 2026-11-18**（diff vs 上游只剩 2 個純新增檔案）。Actions 在此出正式 APK。
- `feat/zh-tw-ui` = **當前工作分支**，基底 `upstream/main` + 我們的 CI workflow + 工作表 + 工具鏈。← 現在在這裡
- `pr/zh-tw-ui` = **提 PR 用的乾淨分支（已就緒）**，`e952b131`，基於 `upstream/main` `84adfa99`，`git diff upstream/main --stat` 嚴格只有 4 檔：
  `app/.../values-zh-rTW/strings.xml`、`wear/.../values-zh-rTW/strings.xml`、`OtherScreen.kt`（1 行）、`docs/zh-TW-ui-contribution.md`。已推 `origin`。
- `assets/zh-tw-screenshots` = 圖床分支（`465ad80a`），6 張截圖供 `#492` / PR 引用。

⚠️ **不要拿 `main` 或 `feat/zh-tw-ui` 直接開 PR** —— 兩者都含 `build-apk.yml`（作者已明確拒絕過，見 PR #286）。
提 PR 必須走 `pr/zh-tw-ui` 剝離流程。

## 硬規則

1. **改任何檔案前先更新工作表的 checkbox** —— 這是進度唯一的權威來源。
2. **翻譯基底是英文**（`values/strings.xml`），不是 `values-zh-rCN`。用 `values-zh-rCN` 再轉會變「二手 AI 轉譯」，與上游未來自做的 zh-TW 打架。
3. **必須保留** `comment="..."` 翻譯指引屬性（2026-11-20 實查 base 有 1618 條；**以當下 base 為準，不寫死數字**）與所有 placeholder（`{app_name}` / `%1$s` / `{count}`）。
4. **必改 Kotlin 一行**：`OtherScreen.kt` 的語言 tag 清單加 `"zh-TW"`（上游有 App 語言選擇器，40 個 tag + `auto`）。工作表裡原寫「不改 Kotlin 碼」是錯的，已更正。
5. **不要碰 `values/strings_dont_translate.xml`**（32 條）。
6. **不要用 `kubectl apply` / `helm` 之類** —— 本 repo 與叢集無關。
7. **wear 的語言跟「手錶系統語言」，不跟手機 App 的 in-app 語言選擇器**（wear 模組無任何 Locale/Configuration 覆寫）→ 走查 wear 畫面前先確認手錶系統語言，別誤判成「沒翻譯」。詳見工作表 1.2.1。

## 驗證（不可腦補）

```bash
# 資源 key 集合與 placeholder 必須與 base 完全對齊（app + wear 兩個模組）
python3 tools/check-l10n.py --strict --module all
# → app 2547 strings + 11 plurals（comment 1618 條）/ wear 69 strings 全對齊

# XML 合法性
xmllint --noout app/src/main/res/values-zh-rTW/strings.xml wear/src/main/res/values-zh-rTW/strings.xml

# lint（需本機 JDK 21 + Android SDK；本機無 → 走 Actions）
./gradlew :app:lintDebug

# 雲端編譯（Actions）
gh workflow run build-apk.yml --ref feat/zh-tw-ui
```

⚠️ Release 資產：**在分支上跑不會覆蓋 `v6.4.0-apk`**（已修：分支用獨立 tag `v6.4.0-apk-<分支名>`）。
只有**刻意在 `main` 上跑**才會 `--clobber` 掉 `v6.4.0-apk`（= 手機上裝的那個，Nextcloud `文件/app-debug.apk`）→ 不要在 `main` 上隨手觸發。
（此說明已與工作表 A4 同步，2026-11-20 複查修正。）

## 🔑 簽章金鑰（已固定並完成本機備份）

金鑰**不在 repo 裡、不會被 clone 回來**，存在於 GitHub Secret `ANDROID_DEBUG_KEYSTORE_B64`，且已於 2026-11-20 **加密匯出並備份至本機 `~/DictateKeyboard-secrets/debug.keystore`**（只存於這台 Mac，檔案 SHA-256 `92212e70...`、憑證指紋 `AD:52:6F:35:...74:31:A3`）。

`main` 與 `feat/zh-tw-ui` 兩條分支的 `.github/workflows/build-apk.yml` 皆已修好固定簽章機制（同時寫入 `$HOME/.android` 與 `$XDG_CONFIG_HOME/.android` 並注入 Gradle signing properties），日後建置的 APK 皆可直接覆蓋升級。詳見工作表 1.5 節。

## 與上游互動的關鍵背景

- 上游翻譯由**作者自己用 AI 批次生成**，每個功能 commit 同步更新全部 20 個 locale（同一 SHA）。
  → 靜態 zh-TW 檔案必然漂移 → **交付物要含「glossary + 後處理轉換器」**，而非只有檔案。
- 上游 issue **#483「Dictation in traditional chinese」** —— 我們**已留言**（含繁中 STT 解法 + 指向 #492）：https://github.com/DevEmperor/DictateKeyboard/issues/483#issuecomment-7030540460
- 上游 issue **#492「Traditional Chinese (zh-TW) UI translation」** —— 我們**已開立**（含 6 張對照截圖）：https://github.com/DevEmperor/DictateKeyboard/issues/492
  - **🚨 PR 尚未開立**（上游 `author:kuniakil` 的 PR 數 = 0）→ 現在卡在 **E2c 等作者回覆**。
- 作者的習慣：**先開 issue 談，再收 PR**。README 也這樣寫；PR #442 明確寫「please open an issue」。
- 社群翻譯 PR 有被關閉的先例（PR #97），但社群 PR 被合併的先例也有（#223/#216/#168/#167）。

## 相關文件

- `docs/worksheet-dictatekeyboard-zhtw-ui-20261120.md` — **主工作表**（Part 0 交接說明是進度權威來源）
- `docs/upstream-outreach-drafts-20261120.md` — `#483` / `#492` / **Draft 3（PR 文案）**
- `docs/zh-TW-ui-contribution.md` — 給作者的說明（會隨 PR 帶上）
- `docs/opentypeless-and-dictatekeyboard-stt-tuning-20261117.md` — 繁中 STT/潤色調校（Mac OpenTypeless + 本 fork 雲端編譯實戰）
- `docs/zh-TW-setup.md` — 繁中 App 設定指南（已存在於 fork）
