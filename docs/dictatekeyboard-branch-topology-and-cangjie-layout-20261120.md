---
title: "DictateKeyboard 雙層單向分支架構定案與倉頡字根鍵盤實作（2026-11-20）"
categories: [Android, GitOps]
tags: [dictatekeyboard, florisboard, git-workflow, cangjie, zh-tw, github-actions, troubleshooting]
---

# DictateKeyboard 雙層單向分支架構定案與倉頡字根鍵盤實作（2026-11-20）

## 1. 任務背景與目標

在完成 DictateKeyboard 繁體中文（zh-TW）介面在地化並於上游開立 Issue `#492` 等待作者回覆期間，面臨兩個工程需求：
1. **建立可長期擴展的 Fork 分支管理架構**：每個新功能需各自獨立在乾淨分支開發以便日後分別對上游提 PR，但同時我們自己的自用 APK 要能馬上整合所有已完成功能，且未來上游升版時能順利 `merge` 並保留全部客製改動。
2. **完成 Phase F2（倉頡字根鍵盤顯示 ＋ `zh-TW-*` 預設貨幣符號修正）**：上游內建 `zh-TW-cangjielarge` 輸入法，卻借用英文 `qwerty.json`，導致螢幕按鍵仍顯示 `q w e r t y` 而非倉頡字根；同時 `zh-TW-boshiamy` 與 `zh-TW-cangjielarge` 的預設貨幣集誤設為日圓 `yen`（¥）而非 `dollar`（$）。

---

## 2. 實施步驟與關鍵變更

### 2.1 定案「雙層單向分支架構」並寫入全域 Skill

捨棄過度複雜的「四層 `cherry-pick`＋臨時 `build/all`」方案，確立業界標準的 **Topic Branches (`pr/*`) ＋ Self-Use Integration Branch (`main`)** 雙層單向架構：

```text
                  ┌──► pr/zh-tw-ui       （功能 1：嚴格 4 檔，基於 upstream/main ──► PR #1）
                  │
upstream/main ────┼──► pr/cangjie-layout （功能 2：嚴格 3 檔，基於 upstream/main ──► PR #2）
 (作者原版)        │         │
      │           │         │ 單向 git merge pr/<feature>（不做反向 merge/rebase）
      │ (上游升版)  ▼         ▼
      └──────► 我們的 main（自用全功能整合主幹 = upstream/main + CI + l10n 工具鏈 + 工作表 + 所有已合入功能）
```

- **合併 `feat/zh-tw-ui` 進 `main`**（`56deb74b`）：讓 `main` 直接成為全功能繁中自用整合主幹（Actions 預設即編譯自用全功能 APK），保留 `l10n/` 與 `tools/` 翻譯工具鏈在 `main` 上運作；改詞時再以 `git checkout pr/zh-tw-ui && git checkout main -- <4 個目標檔>` 同步產出。
- **同步更新規則與全域 Skill**：更新 `~/DictateKeyboard/AGENTS.md`、`CLAUDE.md`、`docs/worksheet-dictatekeyboard-zhtw-ui-20261120.md`，並將這套架構（區分 Pattern A 持續追 `main` 的 `DictateKeyboard` 與 Pattern B 追官方 Release Tag `my-config-v*` 的 `OpenClaw` / `Hermes`）寫入 `~/.gemini/config/skills/upstream-pr-ops/SKILL.md`（透過 symlink 四端同步）。

### 2.2 新增 Gboard 標準倉頡字根配置與 `$` 貨幣修正（`pr/cangjie-layout`）

先檢查底層引擎程式碼後確認**無需修改 Kotlin**：
- `TextKeyData.kt` 將按鍵顯示文字（`label`，`isForDisplay = true`）與實際送出碼（`code`，`isForDisplay = false`）分離。
- `HanShapeBasedLanguageProvider.kt` 讀取 `han.sqlite3` 的 `cangjielarge` 資料表時，依 ASCII 小寫 `a`–`z` 前綴做 indexed range 查詢（`code >= ? AND code < ?`），且核對 `han.sqlite3` 後確認 26 鍵與 Gboard 標準倉頡映射 100% 一致。

從 `upstream/main` 切出乾淨獨立分支 `pr/cangjie-layout`（commit `3c3a7a5a`），僅修改 3 個 JSON 檔：

1. **新增 `app/src/main/assets/ime/keyboard/org.florisboard.layouts/layouts/characters/cangjie.json`**：
   - 採用 `case_selector`（與韓文 `korean.json` 同款設計）：
     - `lower`（一般狀態，因中文 `FlorisLocale.supportsCapitalization = false` 故預設皆處於此狀態）：鍵帽顯示 Gboard 標準 26 鍵倉頡字根（`手田水口廿卜山戈人心` / `日尸木火土竹十大中` / `重難金女月弓一`），送出小寫 ASCII `97`–`122`（`a`–`z`）。
     - `upper`（按下 Shift 時）：切換顯示大寫英文字母 `Q`–`M`（ASCII `65`–`90`），方便臨時輸入英文或對照鍵位。
2. **修改 `app/src/main/assets/ime/keyboard/org.florisboard.layouts/extension.json`**：
   - 於 `layouts.characters` 註冊 `"id": "cangjie"`、`"label": "倉頡 (Cangjie)"`。
3. **修改 `app/src/main/assets/ime/keyboard/org.florisboard.localization/extension.json`**：
   - 將 `zh-TW-cangjielarge` 的 `preferred.characters` 由 `org.florisboard.layouts:qwerty` 改為 `org.florisboard.layouts:cangjie`。
   - 將 `zh-TW-boshiamy` 與 `zh-TW-cangjielarge` 的 `currencySet` 由 `org.florisboard.currencysets:yen` 改為 `org.florisboard.currencysets:dollar`。

完成後單向執行 `git checkout main && git merge pr/cangjie-layout`，並觸發 GitHub Actions 建置出新版 APK。

### 2.3 技術背景補充：為何上游有倉頡卻沒有注音？

查證程式碼後發現三個原因：
1. **歷史繼承**：倉頡、嘸蝦米與鄭碼來自 FlorisBoard 內建的 `org.florisboard.hanshapebasedbasicpack`（`han.sqlite3`），全屬 **26 鍵英文字母形碼查表**，零排版改動即可運作。
2. **簡中拼音復用同一引擎**：作者於 issue #262 撰寫 `PinyinPackManager.kt`，動態下載 `net.devemperor.dictate.pinyin.flex`（約 3 MB / 17 萬筆），同樣以 26 鍵 `a`–`z` 查表；註解雖預留未來擴充繁中包，但尚未實作。
3. **注音門檻較高**：標準大千注音需要 37 個注音符號 ＋ 4 個聲調（41 鍵、4 排佈局需佔用數字排），且同音字極多，無法僅靠單字查表運作，需要整合詞庫斷詞／智慧選字引擎（如 `libchewing` 新酷音或 Rime）。

---

## 3. 踩坑記錄與解決方案 (Gotchas & Fixes)

### 坑 1：把 `l10n/` 生成工具與 `values-zh-rTW/` 拆在不同分支會讓工具鏈斷裂
- **現象**：若照「`main` 純放工具、功能全拆去 `pr/*` 再臨時開 `build/all` cherry-pick」的三層設計，改翻譯詞時在 `pr/zh-tw-ui` 上找不到 `l10n/` 與 `tools/`，在 `main` 上又沒有目標 `strings.xml`。
- **解決方案**：將 `main` 直接定義為自用全功能整合主幹（含工具鏈與所有功能），`pr/*` 嚴格保持單一功能乾淨 diff，所有流程單向匯入 `main`。

### 坑 2：手機安裝新版 APK 後「字元配置」仍看不到倉頡、仍顯示 `QWERTY`
- **根因**：
  1. 透過 `gh release view` 與解壓 APK 確認 `cangjie.json` 確實已打包進 `v6.4.0-apk/app-debug.apk`，但 GitHub Releases 頁面上較早編譯的 `v6.4.0-apk-feat-zh-tw-ui` 仍佔據 `Latest` 標籤導致下載到舊版，且手機下載資料夾可能與舊 `app-debug.apk` 同名混淆；另手機 Nextcloud App 因 Google 限制無法直接下載 `.apk`。
  2. 此外，手機 `SharedPreferences` 內的既有子類型會快取建立當時的 `qwerty` 設定，不會被新版 `extension.json` 的 `preferred` 自動覆蓋。
- **解決方案**：
  - 執行 `gh release edit v6.4.0-apk -R kuniakil/DictateKeyboard --latest` 將 `v6.4.0-apk` 設回 `Latest`。
  - 額外上傳具名資產 `app-debug-cangjie-20261120.apk` 至 `v6.4.0-apk`，透過手機 GitHub App 下載覆蓋安裝。
  - 至 App「設定 → 語言與配置 → 子類型」改選「倉頡 (Cangjie)」或刪除重加 `中文 (台灣) [CANGJIELARGE]`。

### 坑 3：倉頡打字時看不到選字清單，按空白鍵直接送出第一個字
- **根因（雙重遮蔽）**：
  1. 實機截圖顯示 Smartbar 中間正被作者的一次性推播 **`新 App：手錶上的 AI`（`DictateController.UiState.Promo` / `PromoKind.SAYOVA`）** 佔用；依 `Smartbar.kt` 邏輯，`isDictating`（非 `Idle`）時會隱藏 `CandidatesRow()`。
  2. 測試欄位為 Google 搜尋框，App 會對該欄位帶上 `TYPE_TEXT_FLAG_NO_SUGGESTIONS`，依 `EditorInstance.kt` 與 `AppPrefs.kt` 預設會關閉 composing/建議列（`ignoreAppSuggestionBlock = false`）。
- **解決方案**：點擊推播右側 `✕` 關閉一次性廣告，並於 App「設定 → 建議」開啟 **「忽略關閉建議的應用程式」**，倉頡候選字清單（含最多 32 字與拆碼提示）立即正常顯示，不需改動程式碼。

---

## 4. 驗證結果與後續 TODO

### 驗證結果
- **PR 分支純淨度**：
  - `git diff upstream/main..pr/zh-tw-ui --stat`：嚴格 4 檔（`+2997` 行），未受污染。
  - `git diff upstream/main..pr/cangjie-layout --stat`：嚴格 3 檔（`+121 / -3` 行），與 `pr/zh-tw-ui` 完全隔離。
- **雲端建置與簽章**：
  - Actions Run [`44747287202`](https://github.com/kuniakil/DictateKeyboard/actions/runs/44747287202) 於 `main`（`22248d26`）成功編譯（耗時 `13m51s`），發佈至 `v6.4.0-apk`（`174,484,075` bytes，SHA-256 `3477b89916a0eb485dc4369bfb465d73cb99fb92443da5371820e7487a402e12`），固定簽章指紋 `AD:52:6F:35:...74:31:A3` 完全一致。
- **實機驗收**：覆蓋安裝後繁中 UI、倉頡字根（一般顯示字根 / Shift 切換大寫字母）、`$` 貨幣符號與上方候選字選字列皆運作正常。

### 後續 TODO
- 等待上游作者 `DevEmperor` 回覆 `#492` 後，再決定是否分別以 `pr/zh-tw-ui` 與 `pr/cangjie-layout` 開立獨立 PR。
- 推進 Phase F 剩餘項目：**F1**（繁中實用 Rewording Prompts 投稿至 `prompt-library`）、**F3**（Dictation 詞彙進入 `LearnedWordsStore` 之 Feature Request）、**F4**（觀察並清理 Mac 端 OpenTypeless 舊備份）。
