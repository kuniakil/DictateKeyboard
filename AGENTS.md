# AGENTS.md — DictateKeyboard 繁體中文（zh-TW）在地化

> **這是 opencode / Antigravity 進入 `~/DictateKeyboard/` 時自動注入的專案規則。**
> 全域常識見 `~/.config/opencode/GLOBAL.md`。
> 與其他 agent 共享 `~/DictateKeyboard/CLAUDE.md`（內容同步，可當交叉參考）。
>
> ⚠️ **本 repo 與 `~/kubernetes/` 叢集完全無關** —— 別套用那邊的 helm / kubectl / kustomize 守則。

---

## 📍 這是什麼

`DevEmperor/DictateKeyboard` 的 fork。

> **⚠️ 當前狀態（2026-11-20）**：**繁體中文（台灣）介面已全部完成**（app 2547 strings + 11 plurals、wear 69 條、台灣用語校訂、實機驗收、雲端出包、簽章備份）。
> **上游互動停在「等作者回覆」**：已於 [#483](https://github.com/DevEmperor/DictateKeyboard/issues/483) 留言並開立 Issue **[#492](https://github.com/DevEmperor/DictateKeyboard/issues/492)**，**PR 尚未開立**（上游 `author:kuniakil` 的 PR 數 = 0）。
> **📌 已定案（2026-11-20）：不搶先開 PR，等作者回覆。** 分支 `pr/zh-tw-ui` 維持待命，作者回覆歡迎時再開（文案 = `docs/upstream-outreach-drafts-20261120.md` 的 **Draft 3**）。等待期間推進 Phase F。詳見工作表 Part 0「📌 2026-11-20 決策」節與「作者回覆後的應對決策表」（情境 1–7）。

Fork 的兩個目的：
1. **產 APK** —— 作者只在 Play 上架付費版、GitHub Releases 不附 APK。我們用 GitHub Actions 雲端編譯 debug APK（固定簽章 → 可覆蓋升級）。
2. **提 PR** —— 讓作者看到繁中方案可行；他若合併，以後我們就不用自己維護繁中 UI。

---

## 📖 立刻先讀

**`docs/worksheet-dictatekeyboard-zhtw-ui-20261120.md`** —— 完整工作表（983 行）。內含：

- **Part 0 交接說明** —— 當前狀態、**作者回覆後的應對決策表（情境 1–7）**、不要再踩的坑 ⬅️ **先看這裡**
- Part 1 調查結果（三個決定性發現、工程事實、台灣用語表、2026-11-17 操盤歷史查證、簽章金鑰位置、分支架構）
- Part 2 計畫（Phase A–F，每項都是可勾選的 checkbox）
- Part 3 風險、Part 4 已定案事項、Part 5 可重跑的驗證指令

**不要重做調查** —— 關鍵事實都已在工作表內驗證過（上游 locale 結構、app 語言選擇器位置、2547 條資源數量、fork 分歧狀態、簽章金鑰位置…）。

---

## 🌿 Repo 拓撲（雙層單向架構：`pr/*` 獨立功能分支 ＋ `main` 自用整合主幹）

| remote | 指向 | 用途 |
|---|---|---|
| `origin` | `kuniakil/DictateKeyboard`（我們的 fork） | 推送分支、開 PR 的來源 |
| `upstream` | `DevEmperor/DictateKeyboard`（上游） | 追蹤上游更新、PR 的目標 |

| 分支 | 角色 | 能直接開 PR？ |
|---|---|---|
| `main` | **自用全功能整合主幹（Integration Branch）** = `upstream/main` + 我們的 CI（`build-apk.yml`）+ 翻譯工具鏈（`l10n/`、`tools/`）+ 工作表/文件 + 所有自用功能（已合入 `feat/zh-tw-ui` 繁中 UI）。Actions 直接在此出全功能繁中 APK（`v6.4.0-apk`）；上游升版時直接在此 `git fetch upstream && git merge upstream/main` | ❌ 含 `build-apk.yml` 與多項自用內容 |
| `pr/<feature>`（目前：`pr/zh-tw-ui`） | **提 PR 專用乾淨分支（Topic Branches）**，一律從 `upstream/main` 切出，嚴格只含單一功能改動（不含 CI、不含工作表、不含其他功能）。`pr/zh-tw-ui`（`e952b131`）基於 `upstream/main` `84adfa99`，diff 嚴格 4 檔（app XML / wear XML / `OtherScreen.kt` 1 行 / `docs/zh-TW-ui-contribution.md`）。做完後單向 `git merge pr/<feature>` 進 `main` 即可自用，無需等作者回覆；各功能獨立提 PR | ✅ |
| `feat/zh-tw-ui` | 階段性開發分支（已於 2026-11-20 合併入 `main`；歷史 Release `v6.4.0-apk-feat-zh-tw-ui` 指向此分支，日常作業已轉回 `main`） | ❌ 同 `main` |
| `assets/zh-tw-screenshots` | 圖床分支（`465ad80a`），6 張截圖供 `#492` / PR 引用 | — |

**日常流向（嚴格單向：`upstream/main` ➔ `pr/<feature>` ➔ `main`）**：
1. 做新改進：一律從 `upstream/main` 切 `pr/<feature>` 開發（與其他功能完全隔離）。
2. 自用出包：切回 `main`，執行 `git merge pr/<feature>` 合入自用主幹後直接由 `main` 觸發 Actions（**禁止**把 `main` 反向合回或 rebase 到 `pr/<feature>`）。
3. 翻譯生成檔例外：`l10n/` 與 `tools/` 留在 `main`，改詞時在 `main` 跑完生成腳本，再以 `git checkout pr/zh-tw-ui && git checkout main -- <那 4 個目標檔>` 同步到 PR 分支。
4. 上游升版：`git fetch upstream && git checkout main && git merge upstream/main`（保留所有自用功能）；仍在審核中的 `pr/*` 僅在需要對齊時才執行 `git rebase upstream/main`。

⚠️ **不要拿 `main` 或 `feat/zh-tw-ui` 直接開 PR** —— 作者已明確拒絕過社群提供的 APK 建置流程（上游 PR #286：「Dictate is distributed through Google Play, and that is deliberate」）。提 PR 必須由乾淨的 `pr/<feature>`（如 `pr/zh-tw-ui`）開立。

---

## ✏️ 硬規則

1. **改任何檔案前先更新工作表的 checkbox** —— 那是進度唯一的權威來源。
2. **翻譯基底是英文**（`values/strings.xml`），**不是** `values-zh-rCN`。用 zh-rCN 再轉會變「二手 AI 轉譯」，與上游未來自做的 zh-TW 打架。
3. **必須保留** `comment="..."` 翻譯指引屬性（2026-11-20 實查 base 有 **1618** 條；**以當下 base 為準，不寫死數字**）與所有 placeholder（`{app_name}` / `%1$s` / `{count}`）。
4. **必改 Kotlin 一行**：`app/src/main/kotlin/dev/patrickgold/florisboard/app/settings/advanced/OtherScreen.kt` 的語言 tag 清單（上游有 App 語言選擇器，40 個 tag + `auto`，靠 `createConfigurationContext` 即時切換）→ 加 `"zh-TW"`。
   > 工作表裡原寫「不改 Kotlin 碼、零衝突」是**錯的**，已更正。
5. **不要碰 `values/strings_dont_translate.xml`**（32 條）。
6. **本 repo 與叢集無關** —— 沒有 helm / kubectl / kustomize 這回事。
7. **wear 的語言跟「手錶系統語言」，不跟手機 App 的 in-app 語言選擇器**（wear 模組無任何 Locale/Configuration 覆寫）→ 走查 wear 畫面前先確認手錶系統語言，別誤判成「沒翻譯」。詳見工作表 1.2.1。

---

## 🔑 簽章金鑰（已固定並完成本機備份）

金鑰**不在 repo 裡、不會被 clone 回來**，存在於 GitHub Secret `ANDROID_DEBUG_KEYSTORE_B64`，且已於 2026-11-20 **加密匯出並備份至本機 `~/DictateKeyboard-secrets/debug.keystore`**（只存於這台 Mac，檔案 SHA-256 `92212e70...`、憑證指紋 `AD:52:6F:35:...74:31:A3`）。

`main` 與 `feat/zh-tw-ui` 兩條分支的 `.github/workflows/build-apk.yml` 皆已修好固定簽章機制（同時寫入 `$HOME/.android` 與 `$XDG_CONFIG_HOME/.android` 並注入 Gradle signing properties），日後建置的 APK 皆可直接覆蓋升級。詳見工作表 1.5 節。

---

## ✅ 驗證（不可腦補）

```bash
# 資源 key 集合與 placeholder 必須與 base 完全對齊（app + wear 兩個模組）
python3 tools/check-l10n.py --strict --module all
# → app 2547 strings + 11 plurals（comment 1618 條）/ wear 69 strings 全對齊

# XML 合法性
xmllint --noout app/src/main/res/values-zh-rTW/strings.xml wear/src/main/res/values-zh-rTW/strings.xml

# lint（需本機 JDK 21 + Android SDK；本機無 → 走 Actions）
./gradlew :app:lintDebug

# 雲端編譯（Actions：日常於 main 出自用全功能繁中 APK）
gh workflow run build-apk.yml --ref main -R kuniakil/DictateKeyboard
```

⚠️ Release 資產：在 **`main`** 上跑會更新正式自用版 `v6.4.0-apk`（現在已含完整繁中 UI 與所有合入的功能）；若在側分支上跑則會發布到獨立 tag `v6.4.0-apk-<分支名>`，不會覆蓋 `v6.4.0-apk`。
（2026-11-20 複查與架構升級同步：`main` 已合併 `feat/zh-tw-ui`，成為全功能繁中整合主幹。）

---

## 🗣️ 與上游互動的關鍵背景

- 上游翻譯由**作者自己用 AI 批次生成**，每個功能 commit 同步更新全部 20 個 locale（同一 SHA）。
  → 靜態 zh-TW 檔案必然漂移 → **交付物要含「glossary + 後處理轉換器」**，而非只有檔案。
- 上游 issue **#483「Dictation in traditional chinese」** —— 我們**已留言**（含繁中 STT 解法 + 指向 #492）：https://github.com/DevEmperor/DictateKeyboard/issues/483#issuecomment-7030540460
- 上游 issue **#492「Traditional Chinese (zh-TW) UI translation」** —— 我們**已開立**（含 6 張對照截圖）：https://github.com/DevEmperor/DictateKeyboard/issues/492
  - **🚨 PR 尚未開立**（上游 `author:kuniakil` 的 PR 數 = 0）→ 現在卡在 **E2c 等作者回覆**。
- 作者的習慣：**先開 issue 談，再收 PR**（README 也這樣寫；PR #442 明確說「please open an issue」）。
- 社群翻譯 PR 有被關閉的先例（PR #97），但社群 PR 被合併的先例也有（#223/#216/#168/#167）。

---

## 📚 相關文件

| 檔案 | 內容 |
|---|---|
| `docs/worksheet-dictatekeyboard-zhtw-ui-20261120.md` | **主工作表** —— 交接說明 + 調查結果 + 計畫 + 風險（Part 0 是進度權威來源） |
| `docs/upstream-outreach-drafts-20261120.md` | `#483` / `#492` / **Draft 3（PR 文案）** |
| `docs/zh-TW-ui-contribution.md` | 給作者的說明（會隨 PR 帶上） |
| `docs/opentypeless-and-dictatekeyboard-stt-tuning-20261117.md` | 繁中 STT/潤色調校實戰（Mac OpenTypeless + 本 fork 雲端編譯） |
| `docs/zh-TW-setup.md` | 繁中 App 設定指南（已存在於 fork，供使用者複製貼上） |
| `CLAUDE.md` | 同一份規則的 Claude Code 版本（內容同步） |
