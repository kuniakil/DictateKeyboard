# 專案工作表：DictateKeyboard 繁體中文（zh-TW）UI 在地化

- **建立時間**：2026-11-20 (Taipei Time)
- **本工作表所在 repo**：`~/DictateKeyboard`（= 我們的 fork `kuniakil/DictateKeyboard`）
- **上游專案**：`DevEmperor/DictateKeyboard`（Android 語音輸入法，Kotlin/Compose，Apache-2.0）
- **我們的 Fork**：`kuniakil/DictateKeyboard`（已完成雲端編譯、固定簽章、Release `v6.4.0-apk`）
- **相關既有文件**：`docs/opentypeless-and-dictatekeyboard-stt-tuning-20261117.md`（繁中 STT/潤色調校實戰）
- **目標**：讓繁體中文（台灣）使用者拿到正統的繁中介面，**並藉此探測上游作者對社群貢獻的態度**

---

## Part 0 — 交接說明（新 session 從這裡開始）

### 當前狀態（2026-11-20 持續更新）

| 項目 | 狀態 |
|---|---|
| 本機 repo | ✅ `~/DictateKeyboard`（origin = 我們的 fork，upstream = 上游） |
| 當前分支 | `main`（✅ **2026-11-20 架構升級**：已合併 `feat/zh-tw-ui`，升級為「自用全功能整合主幹」= `upstream/main` + CI + `l10n/` 工具鏈 + 工作表 + 繁中 UI） |
| PR 專用分支 | • `pr/zh-tw-ui`（`e952b131`，基於 `upstream/main` `84adfa99`，嚴格 4 檔乾淨 diff）<br>• `pr/cangjie-layout`（`3c3a7a5a`，基於 `upstream/main` `84adfa99`，嚴格 3 檔乾淨 diff：倉頡字根 `cangjie.json` + `zh-TW-*` 貨幣 `dollar`，已單向 `merge` 回 `main`） |
| Phase A | ✅ A0/A1/A2/A3 完成（`docs/zh-TW-ui-contribution.md` 已建立） |
| Phase B / D | ✅ **B0–B6、D1–D3 全數完成**（app 2547 strings + 11 plurals + 1618 comments；wear 69 strings；`--strict` 驗證通過） |
| Phase C | ✅ **C1–C4 全數完成**（picker 顯示名稱：`中文 (台灣)`；12 張實機截圖已核對，並建置乾淨圖床分支 `assets/zh-tw-screenshots`） |
| Phase E | 🔄 **E1a–E1e、E2a、E2b 已完成** —— 已於 #483 留言並開立 [#492](https://github.com/DevEmperor/DictateKeyboard/issues/492)，目前 **E2c 等待作者回覆**（`pr/zh-tw-ui` 已就緒待命）。📌 **2026-11-20 決策：不搶先開 PR，等作者回覆**（見 Part 0 決策節） |
| 🚨 **PR 開立狀態** | ⚠️ **尚未開立 PR** —— 上游目前只有 **Issue `#492`** 與 `#483` 的留言，**沒有我們的 Pull Request**。<br>實查（2026-11-20）：`gh search prs --repo DevEmperor/DictateKeyboard "Traditional"` → 0；`gh api "search/issues?q=repo:DevEmperor/DictateKeyboard+is:pr+author:kuniakil"` → `total_count = 0`；上游 PR 總數 38 筆無 ours。<br>`pr/zh-tw-ui`（`e952b131`）**已推到我們的 fork**，diff 乾淨（4 檔），PR 文案＝`docs/upstream-outreach-drafts-20261120.md` 的 **Draft 3** → 隨時可開。 |
| 簽章金鑰與 `main` | ✅ **`main` 已同步固定簽章 workflow**（`6a5a8112`）；**金鑰已加密匯出並備份至本機 `~/DictateKeyboard-secrets/debug.keystore`**（SHA-256 驗證通過，臨時分支與 run 已刪除） |
| 執行順序 | ⚠️ **以 2.0.1「權威執行順序」為準**，不是下方 Phase 的字母順序 |
| 2026-11-20 二次複查 | ✅ 已完成，9 項落差已修正（清單見下方「二次複查修正」表） |
| 2026-11-20 三次複查 | ✅ 已完成，**5 項落差已修正**（重點：確認**上游尚無我們的 PR**；清單見下方「三次複查修正」表） |

### 🔵 當前階段（2026-11-20，上游已接洽 → 等待 `DevEmperor` 回覆 `#492`）

| 步驟 | 狀態 |
|---|---|
| **B0–B6 + D1–D3** 全量翻譯 + glossary + wear + 用語校訂 | ✅ 完成（app 2558/2558、wear 69/69、`check-l10n.py --strict` 與 `xmllint` 通過） |
| **C1–C4** 語言選擇器 + 雲端出包 + 實機走查 + 截圖 | ✅ 完成（Run `44668198901`，固定簽章 `AD:52:6F:35:...74:31:A3`；實機顯示 `中文 (台灣)`） |
| **簽章備份與 `main` 同步** | ✅ 完成（`main` commit `6a5a8112` 不觸發 CI、`v6.4.0-apk` 未動；本機備份 `~/DictateKeyboard-secrets/debug.keystore` 雜湊驗證通過） |
| **A3 + E1a–E1e** 貢獻指南、草稿與乾淨分支 `pr/zh-tw-ui` | ✅ 完成（嚴格 4 檔，`e952b131` 已推 `origin/pr/zh-tw-ui`） |
| **E2a + E2b** #483 留言 + 開立新 Issue `#492` | ✅ 完成（[#483 留言](https://github.com/DevEmperor/DictateKeyboard/issues/483#issuecomment-7030540460) ＋ [#492](https://github.com/DevEmperor/DictateKeyboard/issues/492) 含 6 張對照截圖） |
| **E2c → E3 / F** 等待作者回覆後開 PR 或收尾 | ⏳ **交棒給下個 session**（見下方決策表）。⚠️ 複查確認：**上游仍無我們的 PR**，`pr/zh-tw-ui` 已就緒待命。📌 **已決定不搶先開 PR**（見上方決策節） |

### 📌 2026-11-20 決策：**不搶先開 PR，等作者回覆**

> **使用者決策（2026-11-20）**：既然已經開了 Issue `#492`，就**等作者回覆**，**不主動搶先開 PR**。
>
> **理由**（有實據，非憑空）：
> 1. 上游 README 明寫「The best way to help right now is to **open an issue**」→ 我們已經照做。
> 2. PR **#442** 被關閉時作者留言：「Nobody has asked for it so far, so I won't build it without a need. **If you want it, please open an issue**」→ 他要的是「先談」這個動作本身。
> 3. 作者的既有習慣是**先開 issue 談、再收 PR**（PR #286 / #442 都是關閉但附完整理由）。
> 4. **PR #97 的關閉有干擾因素**（基底大改版致 PR 失效）→ 提早提 PR 的「被關閉」機率，未必反映他對社群翻譯的態度，反而浪費一次機會。
>
> **因此**：
> - **E1f / E3a 維持未執行**，且**不再作為待決項反覆糾結** —— 不是「還沒決定」，是「已決定不主動開」。
> - `pr/zh-tw-ui`（`e952b131`）維持**待命**狀態（不 rebase、不改動），作者一旦回覆歡迎，隨時 5 分鐘內可開（見情境 1）。
> - **不主動 ping**（不留言催覆）—— 保持禮貌與低頻，僅在 **2 週後**（2026-12-04 之後）若仍無回覆，才考慮一次禮貌追蹤（情境 7）。
> - 等待期間**推進 Phase F**（F1–F4），不空轉。

### 🧭 作者回覆後的應對決策表（下個 session 接手指南）

> **下個 session 啟動 3 指令**（開工先檢查上游最新回覆與進度）：
> ```bash
> gh issue view 492 -R DevEmperor/DictateKeyboard --comments
> gh issue view 483 -R DevEmperor/DictateKeyboard --comments
> git fetch upstream && git log --oneline upstream/main -5
> ```

| 作者（`DevEmperor`）可能的回覆情境 | 下一步行動 | 具體做法 / 參考指令 |
|---|---|---|
| **情境 1：歡迎直接提 PR（含 `docs/zh-TW-ui-contribution.md`）** | 執行 **E1d → E1f / E3** | 若 `upstream/main` 有新 commit，將 `pr/zh-tw-ui` rebase 到最新 `upstream/main`（`git checkout pr/zh-tw-ui && git rebase upstream/main && git push --force-with-lease origin pr/zh-tw-ui`），確認仍只有 4 檔後對 `DevEmperor:main` 開 PR，文案直接用 `docs/upstream-outreach-drafts-20261120.md` 的 **Draft 3**。 |
| **情境 2：要收 PR，但希望只改資源檔 + `OtherScreen.kt`，不要 `docs/zh-TW-ui-contribution.md`** | 調整 `pr/zh-tw-ui` 後開 **E3** PR | 在 `pr/zh-tw-ui` 執行 `git rm docs/zh-TW-ui-contribution.md && git commit --amend --no-edit && git push --force-with-lease origin pr/zh-tw-ui`，再將 glossary / prompt 規則直接貼進 PR 內文即可。 |
| **情境 3：只願先收資源層 `values-zh-rTW/`，暫不改 `OtherScreen.kt`** | 調整 `pr/zh-tw-ui` 後開 PR | 從 `pr/zh-tw-ui` revert `OtherScreen.kt`（保留 `app/` 與 `wear/` 的 `values-zh-rTW/strings.xml`），確保 `git diff upstream/main --stat` 只剩 2 個 XML 檔後提 PR；我們自己的 `feat/zh-tw-ui` 仍保留 `OtherScreen.kt` 供自用。 |
| **情境 4：要求更換沒有左下角 AccuBattery 電流數字的截圖** | 補拍乾淨截圖覆蓋圖床 | 關閉 AccuBattery 浮動電流監控重拍同 6 張圖，推送覆蓋 `assets/zh-tw-screenshots` 分支（同一檔名，`#492` 與 PR 圖片會自動更新），再通知作者。 |
| **情境 5：回覆「我自己用 AI 批次流程重新產生 `values-zh-rTW`，謝謝你的 glossary」** | 關閉互動、視同達成目標 | 若他已採納 glossary 並加入 `values-zh-rTW`：感謝他、關閉 `#492`；等上游 commit 進來後，將 `main` merge `upstream/main` 並持續用自己的 APK 或追隨上游（不需再人工維護 2547 條）。 |
| **情境 6：對特定用語、標點或目錄命名（如 `values-zh-rTW` vs `values-b+zh+Hant`）提出調整意見** | 修改 `l10n/` → 重建 → 更新 `pr/zh-tw-ui` | 先在 `main` 修改 `l10n/translations/*.json`（或資料夾結構）並重跑 `python3 tools/build-zh-tw-strings.py --strict && python3 tools/check-l10n.py --strict`，再把產出同步到 `pr/zh-tw-ui` 推上（`git checkout pr/zh-tw-ui && git checkout main -- <目標檔>`）。 |
| **情境 7：超過 2 週未獲任何回覆** | 保持 fork 自用並推進 Phase F | 在 `#492` 禮貌 ping 一次或維持靜默；我們的 `main` 已整合繁中 UI 與固定簽章雲端出包能力，可定期 `git merge upstream/main` 同步新功能，並從 `upstream/main` 獨立切 `pr/*` 推進 **F1**（繁中 prompt 投稿）、**F2**（倉頡字根顯示 + `zh-TW-*` 預設貨幣 `yen`→`dollar`）後單向 `merge` 回 `main`。 |
| **收尾備忘（PR 合併後）** | 清理圖床與更新 `main` | 若 `#492` 與 PR 已結案，可視需要保留或刪除 `assets/zh-tw-screenshots`（建議保留，避免已關閉的 issue/PR 破圖），並將 `upstream/main` merge 回 `main`。 |

### C2 建置結果（2026-11-20）

| 項目 | 結果 |
|---|---|
| B0 驗證版 Actions run | `44660451431` → **success**（9 分 12 秒，commit `2d5c2f23`） |
| **全量版 Actions run** | `44668198901` → **success**（commit `be4913ed`） |
| 建置耗時 | **13 分 41 秒**（03:30:34 → 03:44:19 UTC） |
| 產物 | Release `v6.4.0-apk-feat-zh-tw-ui` → `app-debug.apk`（`174,483,318 bytes`） |
| 簽章指紋確認 | ✅ Restored keystore 與 AGP `Variant: debug` 皆為 `AD:52:6F:35:D6:3D:10:18:FA:BD:C0:8D:CA:54:18:7C:11:40:B6:F8:2A:15:0D:8B:5E:92:B5:DF:4D:74:31:A3` |
| `v6.4.0-apk`（main 的資產） | ✅ **完全未動**（仍是 2026-11-17 的 `174,324,306 bytes`）—— 分支獨立 tag 的機制生效 |
| APK 內的 zh-TW 資源 | ✅ B0 資源與全量資源皆通過 `--strict` 與 `aapt2` 建置驗證 |

> ℹ️ `gh` CLI 預設會把 workflow 認成**上游**的 repo（404）。觸發時必須加 `-R kuniakil/DictateKeyboard`。

### APK 層級的資源驗證（不用手機就能驗的部分）

直接解析 APK 內的 `resources.arsc`（自寫極簡 ResTable 解析器），確認：

| 檢查 | 結果 |
|---|---|
| 我們的 45 條譯值有進全域字串池 | ✅ 全部（位於 pool 尾端 `60839`–`60888` 一帶） |
| 譯值被 **zh-TW 的 type chunk** 引用 | ✅ `lang='zh' country='TW'`，chunk 位於 arsc 尾端（`6152548`–`6166604`） |
| 英文預設值仍被 **default chunk** 引用 | ✅ 40 條全對（英文介面沒被影響） |
| **zh-CN 簡中值**仍被 zh-CN chunk 引用 | ✅ 40 條全對（**簡中沒有被我們蓋掉**） |

> ⚠️ 這只能證明「**資源被打包進去、且掛在正確的 locale config 上**」，**不能**證明「執行時的 fallback 解析正確」→ 那一環仍然要靠 C3 實機。

> ℹ️ **為什麼跳過 A4（無改動冒煙測試）**：實查 `git log e4c41fe..upstream/main -- gradle/ build.gradle.kts app/build.gradle.kts wear/build.gradle.kts gradle.properties tools/bergamot tools/fetch-sherpa-onnx.sh` → **空**。上游自 2026-11-17 那次成功建置後沒動過任何建置相關檔案 → CI 路徑壞掉的機率很低 → 省一次建置時間，直接跑 C2。若 C2 失敗再回頭做 A4 判斷歸屬。
>
> ℹ️ **本機不能編譯**：無 JRE（`java -version` 失敗）、無 Android SDK（`~/Library/Android/sdk` 不存在）→ 只能走 Actions。
>
> ⚠️ **必須先 push 再觸發**：workflow 的 `actions/checkout` 抓的是遠端 `feat/zh-tw-ui`。

### 下一步（建議順序）

> ✅ **2026-11-20 複查：本節的 Step 1–3 已全部完成**（B0 → C1 → A4/C2 → C3 → Phase B 全量 → Phase D → Phase E 至 E2b）。
> **當前唯一下一步 = 等作者回覆 `#492`（E2c）**。⚠️ **2026-11-20 決策：不搶先開 PR**（已開 issue 就等回覆，見 Part 0「📌 2026-11-20 決策」節）；等待期間推進 Phase F。
> 下方 Step 1–3 保留作為**歷史決策脈絡**，不再是待辦。

**Step 1 — 先做「最小可行 zh-TW」驗證鏈路**（不要一開始就翻 2547 條）

理由：我們**從未在真機驗證過** `values-zh-rTW` 的目錄命名與 zh-Hant fallback 行為。
若命名或 fallback 跟預期不同（實質風險），要在只翻幾十條時就發現，而不是翻了 2547 條才發現。

```
B0  產出只含約 30–50 條核心字串的 values-zh-rTW/strings.xml（可從 base 挑 settings/dictate 常用字）
C1  OtherScreen.kt 的 tag 清單加 "zh-TW"（1 行）
A4  gh workflow run build-apk.yml --ref feat/zh-tw-ui
C3  裝機實測：設定 → 其他 → 語言 → 選「繁體中文」→ 確認 UI 立即切換、截圖
```

驗證通過 → 再回頭補完 2547 條（Phase B 全量）+ wear（69 條）。

**Step 2 — 補完全量翻譯**（Phase B 全量 → Phase D 用語校訂）

**Step 3 — 提 issue → 提 PR**（Phase E）

### 2026-11-20 二次複查修正（同日第二次 review，本節為權威）

| # | 落差 | 修正位置 |
|---|---|---|
| 1 | 驗證腳本檔名不一致（`tools/check_zh_tw.py` vs `tools/check-l10n.py`） | **統一為 `tools/check-l10n.py`**（要同時驗 app + wear 兩個模組）；CLAUDE.md 已同步 |
| 2 | Part 0 的建議順序與 Part 2 的 Phase 分組順序矛盾 | **新增 2.0.1 權威執行順序**，明訂「Phase 分組的排列順序不具權威性」 |
| 3 | B5 硬編碼「comment 保留數 = 1614」（1.2 已更新為 1618） | B5 改為**與 base 動態比對** |
| 4 | wear 的語言來源從未驗證 | 新增 **1.2.1**（wear 資源跟手錶系統語言，**不跟**手機 in-app 語言）；B3、C3 加註 |
| 5 | B0 驗收標準只有 `xmllint`（那是 B0b 的事） | B0 驗收改為**綁定 C3 的「B0 階段驗收」** |
| 6 | A4 與 C2 重疊（都是跑 build-apk.yml） | A4 定性為**無改動冒煙測試**、C2 定性為**帶改動的正式產出** |
| 7 | Part 4 Q5 引用的 `TODO.md` 不在 repo 裡 | Q5 補註位置待確認 |
| 8 | CLAUDE.md 的簽章警告與 A4 實情相反 | CLAUDE.md 已同步（A4 實情：分支 tag 已分離，**不必**備份 asset） |
| 9 | 「台灣使用者今天看到英文」與「加 picker 條目」被混為一談 | 新增 **2.4.1**：兩層論述拆開（系統語言命中 vs in-app 選擇器），E2b 開 issue 用得上 |

> 複查當下（2026-11-20）另確認：上游 `values-zh-rCN` 仍是唯一中文目錄、issue #483 仍 OPEN / 0 回覆、`minSdk=26`（≥24，script-aware fallback 保證成立）。

### 2026-11-20 三次複查修正（後續 session，本節為權威）

> **觸發**：使用者回頭查 `~/kubernetes/TODO.md` 與 Dify 知識庫，確認「是否真的提了 PR」。

| # | 落差 | 修正位置 |
|---|---|---|
| 10 | **狀態不明：上游到底有沒有我們的 PR？** → 實查確認**沒有**。`gh api "search/issues?q=repo:DevEmperor/DictateKeyboard+is:pr+author:kuniakil"` → `total_count = 0`；`gh search prs --repo DevEmperor/DictateKeyboard "Traditional"` → 0；上游 PR 總數 38 筆無 ours；`gh pr list -R kuniakil/DictateKeyboard` → 空。上游只有 **Issue `#492`** 與 `#483` 留言 | Part 0 新增「🚨 **PR 開立狀態**」列；E2c、E1f 各加註；E2c→E3 階段列加註 |
| 11 | **A4 checkbox 未勾**（實際被 C2 涵蓋，run `44668198901` success） | A4 勾選並註明「被 C2 涵蓋（N/A）」 |
| 12 | **B5「lint 無 MissingTranslation」未勾**（實際由 Actions `assembleDebug` / `aapt2` 資源合併驗證涵蓋） | B5 補勾並註明驗證來源 |
| 13 | **C3「wear 設定走查」未勾**（實際採 B3 方案②，限制說明已寫入 issue 與 contribution.md） | C3 補勾並註明限制說明位置 |
| 14 | **Part 4 Q5「TODO.md 不在 repo 內 → 應刪除」** → 已找到：`~/kubernetes/TODO.md`（第 52–65 行），且 P1 的 Kotlin 修正**早已寫入**（第 56 行） | Q5 改為「✅ 已結案」，並載明 TODO.md 確切位置 |

> 📌 **同步更新**：`~/kubernetes/TODO.md` 的 P1 狀態已由「進行中」改為「✅ 已完成（截至 E2）／⏳ 等作者回覆 #492 後開 PR」。

### 三個不要重新踩的坑

1. **不要拿 `main` 或 `feat/zh-tw-ui` 直接開 PR** —— 含 `build-apk.yml`，作者已明確拒絕過（PR #286）。必須走 `pr/zh-tw-ui` 剝離流程。
2. **不要用 `values-zh-rCN` 當翻譯基底** —— 會變「二手 AI 轉譯」，與上游未來自做的 zh-TW 打架。基底是英文 base。
3. **不要在未同步上游的情況下切分支開 PR** —— 基底落後會讓 diff 出現 16 個上游 Kotlin 檔案的「反向差異」，作者會以為你在刪他的程式碼。merge 上游後再切。

### 本 session 已完成的調查（別重做）

Part 1 的全部內容都經實查驗證過 —— 上游 locale 結構、app 語言選擇器位置與機制、2547 strings / 11 plurals / 36 條缺漏 / 1614 條 comment 指引、zh-Hant fallback 規則、簽章金鑰位置與單點故障風險、2026-11-17 全程網頁版操作的查證、Release tag 撞名修正。

---

## Part 1 — 調查結果（2026-11-20 實查）

### 1.1 三個決定性發現

#### 發現 1：台灣用戶現在拿到的是**英文**，不是簡體

上游只有 `values-zh-rCN`（2547 → 實際 2513 條），**沒有** `values-zh`、**沒有** `values-zh-rTW`、**沒有** `values-b+zh+Hant`。

依 Android 7.0+（API 24）的 script-aware 資源解析規則：

```
裝置 locale zh-TW  →  推導為 zh-Hant-TW
  → 找 values-zh-rTW      （無）
  → 找 values-b+zh+Hant  （無）
  → 找 values-zh-Hant    （無）
  → 找 values-zh         （無）→ AOSP 慣例是簡體，但上游根本沒有這個目錄
  → 落到預設 values/     → 英文
```

**`values-zh-rCN` 因為隱含 script=Hans，不會被 zh-Hant 裝置匹配到。** 舊版 Android（<7.0）才會掉進簡體。

後果：台灣使用者開 App 看到英文介面。這讓「做繁中 UI」的價值遠高於原本預估，也讓上游 issue #483「Dictation in traditional chinese」有了更強的落腳點。

> 依據：Android 官方 "Language and locale resolution overview" 與 "Correct localization on Android 7" 的中文 fallback 鏈說明。實機驗證列為 Phase A7。

#### 發現 2：上游的翻譯是**作者自己用 AI 批次生成**的，且與功能 commit 綁定

- `2f5c706`（2026-06-15）`l10n: translate Dictate UI into Japanese, Simplified Chinese and Arabic`
  作者 = DevEmperor，commit message 尾端寫著 `Co-Authored-By: Claude Opus 4.8`。
- 從那之後，**每個動到 `values/strings.xml` 的功能 commit，都同時更新全部 20 個 locale 目錄**。
  實測：`values-fr` / `values-ja` / `values-es` / `values-pt` / `values-de` / `values-zh-rCN` 的 last-modified SHA **完全相同**（`caa6fdf`, 2026-11-13）。

**後果**：一份靜態的 `values-zh-rTW` PR 會在**每一個上游 commit** 都立刻漂移。上游 11 月至今已改動 `strings.xml` **30 次**。

#### 發現 3：作者對「社群翻譯 PR」的態度有前例，但方向不明確

| 事件 | 結果 | 訊號 |
|---|---|---|
| PR #97（社群提日文翻譯 + app 語言清單，`ts2020-bot`，2026-05-07 開） | **2026-06-13 無留言關閉，從未合併** | ⚠️ 負面訊號（但有干擾因素，見下） |
| commit `2f5c706`（2026-06-15） | 作者自己把 ja / zh-rCN / ar 翻完 | ⚠️ 作者偏好自己生成 |
| PR #286（`build-apk.yml`，社群提） | 關閉，但附完整理由說明 Play 發行策略 | 中性：願意解釋 |
| PR #442（OpenCode Go preset） | 關閉，但明確寫「Nobody has asked for it so far, so I won't build it without a need. **If you want it, please open an issue that describes it**」 | ✅ **明確指向：先開 issue** |
| PR #223 / #216 / #215 / #210 / #209（MyButtermilk） | **合併** | ✅ 正面訊號：品質好就收 |
| PR #168 / #167（karaokedjodua） | **合併** | ✅ 正面訊號 |
| README | 「The best way to help right now is to **open an issue**」 | ✅ 明確指向 |

> ⚠️ PR #97 的關閉**不能當作「他拒絕社群翻譯」的證據** —— 它開在 2026-05-07，而 `266a1c0`（2026-06-11）import FlorisBoard base、`ba8d3e9`（2026-06-12）大改版，PR 在此期間已被基底變更失效。只能當作傾向訊號。

**綜合判斷**：直接提翻譯 PR 成功率低；「**先開 issue 談 + 我們自己先做一版真的能跑**」成功率最高。這正好符合「先做繁中 UI 來探作者反應」的直覺 —— 但要拆成「自己先用」與「上游怎麼談」兩條線。

---

### 1.2 關鍵工程事實

#### 上游有 app 語言選擇器（這改變了 P1 的性質）

`app/src/main/kotlin/dev/patrickgold/florisboard/app/settings/advanced/OtherScreen.kt:114-165`：

```kotlin
ListPreference(
    prefs.other.settingsLanguage,
    title = stringRes(R.string.pref__other__settings_language__label),
    entries = listPrefEntries {
        listOf("auto", "ar", "bg", "bs", "ca", "ckb", "cs", "da", "de", "el", "en",
               "eo", "es", "fa", "fi", "fr", "hr", "hu", "in", "it", "iw", "ja",
               "ko-KR", "ku", "lv-LV", "mk", "nds-DE", "nl", "no", "pl", "pt",
               "pt-BR", "ru", "sk", "sl", "sr", "sv", "tr", "uk", "zgh", "zh-CN")
            .map { ... }
    },
)
```

- **40 個語言 tag + `auto`**，用 `FlorisLocale.fromTag()` 產生顯示名稱。
- 儲存於 `prefs.other.settingsLanguage`（key = `other__settings_language`，預設 `auto`）。
- `FlorisAppActivity.kt:101-105` 監聽此 pref，用 `createConfigurationContext(config.setLocale(locale.base))` **即時切換整個 App 的 UI 語言**（不需重啟）。
- `AndroidManifest.xml` **沒有** `localeConfig`（實測 grep = 0）→ 走的是 App 內選擇器，不是系統 per-app language。

**結論**：要讓 zh-TW 生效，需要 **兩個改動**，不是一個：
1. 新增資源目錄 `values-zh-rTW/strings.xml`
2. **在 `OtherScreen.kt` 的 tag 清單加入 `"zh-TW"`**

第 2 項會動到 Kotlin 碼 → 與 TODO.md 原本寫的「零衝突、獨立目錄不改 Kotlin 碼」**不符**。這是本次調查推翻的舊假設，必須更正。

#### 資源盤點（實測數字）

| 項目 | 數值 |
|---|---|
| `values/strings.xml`（base，英文） | **2547 strings + 11 plurals** |
| `values-zh-rCN/strings.xml` | **2513 strings + 11 plurals** |
| zh-rCN 缺的條目 | **36 條**（全是最新 learned-words 功能，11/13 才加入） |
| plurals 缺漏 | 0 |
| base 帶 `comment="..."` 翻譯指引的條目 | **約 1614～1618 條**（2026-11-20 複查：`grep -o ' comment="'` = 1618，行數計 1617；上游持續變動，**以 B5 驗證腳本輸出為準**）。`<string ` 出現 2547 次（行數計 2546） |
| zh-rCN 帶 `comment="..."` 的條目 | 544 條（上游翻譯時**有丟掉 comment 屬性**） |
| placeholder（`{app_name}` / `%1$s` / `{count}`）不一致數 | **0** ✅ |
| `wear/src/main/res/values/strings.xml` | **69 strings** |
| `wear/.../values-zh-rCN/strings.xml` | 65 strings |
| `values/strings_dont_translate.xml` | 32 條（**不需翻譯**） |

#### 上游 locale 維護狀態分兩類

| 類別 | 數量 | 特徵 |
|---|---|---|
| **作者積極維護** | 20 個 | ar, bg, ca, cs, de, es, fr, hu, in, it, ja, lv-rLV, nl, pl, pt-rBR, pt, ru, tr, uk, zh-rCN |
| **FlorisBoard 遺留、作者未維護** | 20 個 | bs(68條), eo(705), no(480), mk(17), ckb, fi, hr, iw, ku, nds-DE, sk, sl, sr, sv, zgh, da, el, et-rEE, lv-rLV… |

> ⚠️ 2026-11-20 複查更正：實際 `values-*` 目錄比下表多，另有 `ast-rES`、`sq-rAL`、`ur-rPK`、`et-rEE`、`fa`；其中 `ast` / `sq` / `ur` / `et` **有資源目錄但不在 picker 清單**。且 `lv-rLV` 屬積極維護，下表誤列於遺留側。→ 上游並不要求 picker 與資源目錄一致，可作為 PR 論述。

實測 `values-bs` = 68 strings、`values-mk` = 17 strings、`values-eo` = 480、`values-no` = 480，**`dictate__` 前綴條目數 = 0** → 這些語言在 picker 裡可選，但 Dictate 功能本身完全沒翻譯。

**含意**：上游對語言的態度是「**字典網路，把 key 列出來但不一定翻**」。這降低了「一定要完整翻 2547 條」的門檻，但也意味著作者對翻譯完整度要求不高。

#### 我們的 Fork 分歧狀況（實測）

```
compare kuniakil:main...main  →  fork_ahead 4 / fork_behind 6
```

| 方向 | Commit | 內容 |
|---|---|---|
| **上游有、我們沒有**（4） | `9b3fe20` | Let a shared file through to a server of the user's own that has no key |
| | `46381a3` | Make Scribe v3 the ElevenLabs default |
| | `d09a673` | Replace the Gemini Live transcript (#488) |
| | `84adfa9` | Answer every system voice-input request (#489) |
| **我們有、上游沒有**（6） | `881f440` | ci: add manual Android Debug APK build workflow |
| | `30dfe8a` | ci: use preinstalled Android SDK and accept licenses |
| | `fee1165` | ci: install pinned NDK/CMake and build Bergamot native library |
| | `c89b926` | ci: use fixed debug keystore from GitHub Secrets for in-place upgrades |
| | `e4c41fe` | ci: publish built APK to GitHub Releases |
| | `a02b59c` | docs: add Traditional Chinese (zh-TW) setup and prompts guide |

**這 4 個上游 commit 沒有動 `strings.xml`** → 我們的翻譯基底不受影響，但 Phase A1 仍應先同步，避免後續衝突堆積。

#### 其他已確認事實

- 上游 **無** open PR 涉及 zh-rTW / 繁中（`gh search prs` 實查 = 0）。
- 上游 open issue **#483**「Dictation in traditional chinese」：2026-11-15 開、**0 回覆** —— 正好是我們的切入點。
- 上游 `prompt-library` branch 有 `submissions/` + `schema.json` + `validate.py` + `merge-submissions.yml`，現有 24 條 prompt **全為 `language: en`** → P3 機制就緒。
- 上游 `LearnedWordsStore.note()` **只被 `LatinLanguageProvider`（打字）呼叫**，dictation 文字確實沒進學詞庫 → P4 前提成立。
- 倉頡輸入：上游有 `zh_TW_cangjielarge` 形碼語言包（`hanShapeBasedKeyCode = "abcdefghijklmnopqrstuvwxyz&"`），但 `org.florisboard.layouts` 的 `characters/` 下 **沒有倉頡 layout**（只有 qwerty/dvorak/… 等 65 個西文/韓文 layout）→ P2 需自建 layout，難度比原估高。
- 上游 `tools/` **沒有** l10n/translation 腳本 → 翻譯流程不在 repo 裡，無法直接沿用。

#### 1.2.1 wear 的語言來源（2026-11-20 複查新查證）

`wear/src/main/kotlin/` 下**完全沒有** `Locale` / `Configuration` / `createConfigurationContext` 的使用（grep = 0 命中）。

→ **wear App 的資源解析跟的是「手錶自己的系統語言」，不會跟手機 App 的 in-app 語言選擇器。**

| 影響 | 說明 |
|---|---|
| **B3（wear 69 條）** | 翻完也不一定看得到 —— 只有當**手錶的系統語言**是 zh-TW 時才會命中 `wear/.../values-zh-rTW/` |
| **C3 走查「wear 設定」** | 若只看手機 in-app 切換後的 wear 畫面，會誤判成「wear 沒翻譯」。**必須另外用手錶系統語言驗一次** |
| **證據截圖（C4）** | wear 的截圖要標註「手錶系統語言 = 繁體中文（台灣）」，否則會誤導作者 |

> ⚠️ 這是**本次複查才發現**的落差，原工作表未涵蓋。**B3 開工前先決定驗證方式**（手錶系統語言 vs 放棄 wear 截圖）。

---

### 1.3 台灣用語對照表（機械轉換抓不到的部分）

實測 `values-zh-rCN` 內含的大陸用語統計。**這份表的用途已變**（見 2.3：翻譯基底改由英文翻）→ 它不再是「簡中轉繁中的對照表」，而是「**台灣慣用語 glossary 的種子**」：直接拿來當英文→台灣繁中的翻譯規範。簡體欄位保留是為了讓翻譯者知道「這個詞在大陸怎麼說、對應台灣該用哪個」。

| 簡體 | 出現次數 | 台灣用語 | 簡體 | 出現次數 | 台灣用語 |
|---|---|---|---|---|---|
| 设置 | 101 | 設定 | 用户 | 21 | 使用者 |
| 剪贴板 | 93 | 剪貼簿 | 导出 | 20 | 匯出 |
| 语音 | 49 | 語音 | 移动 | 19 | 行動 |
| 下载 | 42 | 下載 | 字体 | 14 | 字型 |
| 文件夹 | 45 | 資料夾 | 屏幕 | 12 | 螢幕 |
| 智能 | 40 | 智慧 | 反馈 | 11 | 意見回饋 |
| 默认 | 35 | 預設 | 信息 | 11 | 資訊 |
| 导入 | 33 | 匯入 | 网络 | 10 | 網路 |
| 麦克风 | 25 | 麥克風 | 账号 | 10 | 帳號 |
| 主题 | 25 | 佈景主題 | 识别 | 10 | 辨識 |
| 密码 | 22 | 密碼 | 上传 | 7 | 上傳 |
| 翻译 | 22 | 翻譯 | 登录 | 5 | 登入 |
| 收藏 | 5 | 收藏 | 注册 | 4 | 註冊 |
| 软件 | 4 | 軟體 | 插件 | 3 | 外掛 |
| 视频 | 3 | 影片 | 硬件 | 3 | 硬體 |
| 邮件 | 3 | 郵件 | 内存 | 2 | 記憶體 |
| 缓存 | 2 | 快取 | 数据库 | 2 | 資料庫 |
| 优化 | 1 | 最佳化 | 分享 | 18 | 分享 |

其餘約 10 組待 Phase B2 翻譯產出後再掃補齊。

### 1.4 2026-11-17 的 fork 是怎麼做的？（查證：全程 GitHub 網頁版，本機從無 clone）

起因：使用者記不清 fork 與 CI 是「GitHub 直接改」還是「抓回本機改」。以下為查證結果。

#### 三條獨立證據

**證據 1 — 提交署名與本機 git 不符**

| | author 名稱 | email |
|---|---|---|
| fork 的 6 個 commit | `kuniakil`（= GitHub login） | `kuniaki.lee@gmail.com` |
| 本機 git（`~/.gitconfig`） | `Michael Lee` | `kuniaki.lee@gmail.com` |

- GitHub 帳號 `kuniakil` 的 `name` 欄位為 **null**（`gh api user` 實查）→ 網頁版自動產生 commit 時會以 **login 名** + 公開 email 署名。
- 對照組：`my-k8s`、`mac-voice-input` 的所有本機 commit 署名皆為 `Michael Lee` → 兩者不同，證明 fork 的 commit **非本機 git 產生**。
- 額外佐證：fork 6 個 commit 的 `author_login == committer_login == kuniakil`（GitHub API 網頁版建立的 commit 會把 author 與 committer 都設為 PR/編輯者本人）。

**證據 2 — diff 型態符合網頁版「Add file」**

- `881f440`：`.github/workflows/build-apk.yml` **+36 / -0**（單檔全新增，零刪減）
- `a02b59c`：`docs/zh-TW-setup.md` **+79 / -0**

網頁版 "Add file" 產生的正是「單檔全新增、零刪除」diff。

**證據 3 — 本機確實沒有，且從未刪除**

| 查 searched | 結果 |
|---|---|
| `~` 下 maxdepth 7 所有 `.git` 的 `remote.origin.url` | 無任何指向 DictateKeyboard |
| Spotlight（`mdfind`）搜 `DictateKeyboard` / `build-apk.yml` | 零命中 |
| `~/.Trash` | 空（未曾刪除） |
| N100 主機 `find /root /home /data /opt` | 無 |
| `/Volumes/Data`（外接碟）、`/Volumes/OpenClaw_Base` | 無 |

#### Actions 執行時序（完全符合「網頁版迭代」節奏）

```
03:14:56  881f440  ci: add manual Android Debug APK build workflow
03:15:01  ↓ workflow_dispatch → FAILED      ← 剛建好，還沒修好
03:17:07  30dfe8a  ci: use preinstalled Android SDK and accept licenses
03:17:11  ↓ workflow_dispatch → FAILED
03:22:01  fee1165  ci: install pinned NDK/CMake and build Bergamot native library
03:22:05  ↓ workflow_dispatch → SUCCESS ✅
04:36:43  c89b926  ci: use fixed debug keystore from GitHub Secrets
04:38:42  e4c41fe  ci: publish built APK to GitHub Releases
04:38:46  ↓ workflow_dispatch → SUCCESS ✅  → v6.4.0-apk Release
06:41:36  a02b59c  docs: add Traditional Chinese (zh-TW) setup and prompts guide
```

**每個 commit 之後立刻手動觸發一次 Actions、看結果、再改下一個** —— 這是純網頁版迭代的節奏（本機也做得到，但本機無 clone 可證）。

#### 產物佐證

Nextcloud `文件/` 內有 `app-debug.apk`（174 MB，2026-11-17 03:30）與 `backup_net.devemperor.dictate.debug_142_*.zip`（11-18）→ 當年是**從 GitHub Release 下載裝機**，不是本機編譯。

#### 對本計畫的影響

| 面向 | 影響 |
|---|---|
| **本機 clone** | **本專案是第一次在本機擁有 repo** → Phase A0 新增 clone 步驟 |
| **翻譯方式** | 網頁版逐條編輯對 2547 條完全不現實 → 翻譯必須在本機做，本機 repo 是**必需品** |
| **編譯方式** | 沿用 Actions（`build-apk.yml` 已驗證 `workflow_dispatch` 可用），不變 |
| **網頁版的定位** | 只用於最後向作者開 issue / 提 PR（PR 描述要貼截圖，本來就得上網頁版編輯） |

### 1.5 簽章金鑰在哪？（決定未來能否覆蓋升級）

#### 位置

**不在 repo 裡、不會被 clone 回來。** 它只存在於 **GitHub Secret**：

| 項目 | 值（實查） |
|---|---|
| Secret 名稱 | `ANDROID_DEBUG_KEYSTORE_B64` |
| 建立時間 | 2026-11-17T04:36:06Z（`c89b926` 那個 commit 當下） |
| 更新時間 | 2026-11-17T04:36:25Z |
| 存放處 | GitHub Actions Secrets（`repos/kuniakil/DictateKeyboard/actions/secrets`） |
| repo 內是否有簽章檔 | ❌ 無。`git log --all --diff-filter=A` 只找到 `keystore.properties.template` |
| `.gitignore` | 已排除 `*.jks` / `*.keystore` / `keystore.properties`（第 55–57 行） |

#### ⚠️ 簽名一致的機制 —— **原推論已被實測推翻（2026-11-20）**

> ❌ **舊版寫法（從 workflow 內容推論、從未實測）**：
> ```
> 1. build-apk.yml「Restore fixed debug keystore」步驟
>      printf "%s" "$KEYSTORE_B64" | base64 -d > ~/.android/debug.keystore
> 2. app/build.gradle.kts 的 debug buildType 沒有指定 signingConfig
>      → Gradle 自動採用預設的 ~/.android/debug.keystore
> 3. 結果：每次 Actions build 產生的 debug APK 簽名完全一致  ← ❌ 錯的
> ```
>
> **2026-11-20 實測**（自寫 APK v2 簽章區塊解析器，抽出憑證 DER 後算 SHA-256）：
>
> | APK | 來源 | 憑證 SHA-256 |
> |---|---|---|
> | `build-0322.apk` | run `44009692941`（11-17 03:22，**還沒有**金鑰還原步驟）＝ Nextcloud `文件/app-debug.apk`（03:30）＝ **使用者手機上原本裝的那個** | `70b532e408b7741366c592b690ff925ac9632e1dc7af2c8da1d4a9be06ca3b4c` |
> | `build-0438.apk` | run `44018608499`（11-17 04:38）＝ Release `v6.4.0-apk` 的資產 | `99ff6f6eaf6c70c856bb36dd7a4bbbae74ba9dea314ef448cdb1dd1ffc0d176d` |
> | `new-branch.apk` | run `44660451431`（11-20 02:23，分支 `feat/zh-tw-ui`）＝ `v6.4.0-apk-feat-zh-tw-ui` | `aea57f700f2ec5da2f1ba2f3acbc03611e06902291a7fac6f26b546805e11626` |
>
> **三份 APK、三個不同憑證。** 且 Secret 的 `updated_at` 自 2026-11-17T04:36:25Z 起**從未改變**（`gh api .../actions/secrets` 實查）→ 不是 secret 被換掉。
>
> **結論（待 CI 診斷 run 最終確認）**：「還原金鑰」步驟寫進了 `$HOME/.android/debug.keystore`，但 **AGP 並沒有用那一把**（推測是 `ANDROID_USER_HOME` 指向 runner 映像裡的另一個路徑，AGP 便在每次全新 runner 上自動產生新的 debug 金鑰）→ **每次 build 的簽章都不同** → **每次升級都得 uninstall**，App 設定與自訂詞庫每次都會消失。
>
> **後果（已發生）**：使用者 2026-11-20 從 `v6.4.0-apk-feat-zh-tw-ui` 覆蓋安裝失敗，必須先 uninstall 再裝 → App 設定與自訂詞庫**已遺失一次**。
>
> **修法（不改 app 程式碼，避免污染 PR diff）**：
> - 建置時加上 Gradle 的簽章注入參數，把簽章明確指到還原回來的金鑰：
>   `-Pandroid.injected.signing.store.file=... -Pandroid.injected.signing.store.password=android`
>   `-Pandroid.injected.signing.key.alias=androiddebugkey -Pandroid.injected.signing.key.password=android`
> - 並設 `ANDROID_USER_HOME=$HOME/.android`
> - 修正後的憑證會是**第四把鑰** → 手機上目前那把（`aea57f70…`）又不匹配 → **還需要再 uninstall 一次**。所以要在大量迭代之前一次修好。
> - 修好後應把金鑰**備份到本機**（`~/DictateKeyboard-secrets/`）—— 原本「暫緩」的 1.5 節備份作業因此有了實質理由（GitHub Secret 不可逆讀取）。

> 註：`keystore.properties.template` 是**上游給 Play 發行用的 upload key** 模板，與我們這把 debug 金鑰是**兩把不同的鑰匙**，別搞混。上游的 upload key 不在我們手上，也不該有。

#### ✅ 金鑰備份已補齊（2026-11-20 更新）

原本 **GitHub Secret 是不可逆的（write-only）** —— 實測 `GET /actions/secrets/{name}/value` 回 **404 Not Found**，本機與 Nextcloud 原本也皆無副本。

**2026-11-20 已透過臨時一次性非對稱加密流程完成備份與雙向雜湊驗證**：
1. 本機產生一次性 RSA-4096 金鑰對，僅將公鑰放進臨時分支 `tmp/backup-keystore` 的一次性 workflow。
2. Runner 還原 Secret、輸出檔案 SHA-256 與憑證指紋後，以 CMS AES-256 加密上傳 artifact。
3. 本機下載解密至 `~/DictateKeyboard-secrets/debug.keystore`（權限 `600`，`2714` bytes），驗證檔案 SHA-256 與 runner 一致（`92212e7009491e07ec8f14dcf65383422374ff41cd38c7fe079b6300f91f58da`）、憑證指紋 `AD:52:6F:35:D6:3D:10:18:FA:BD:C0:8D:CA:54:18:7C:11:40:B6:F8:2A:15:0D:8B:5E:92:B5:DF:4D:74:31:A3`。
4. 隨即刪除臨時私鑰、臨時 workflow 分支 `tmp/backup-keystore`（遠端與本機）與該次 Actions run（`44675406201`），並已同步固定簽章修復版 `.github/workflows/build-apk.yml` 回 `main`（commit `6a5a8112`）。

> **目前資產位置**：`~/DictateKeyboard-secrets/debug.keystore` + `README.txt`（僅存本機 Mac，不入 git、不傳雲端）。

### 1.6 分支架構的最終定案（2026-11-20 已實作）

#### 我們比上游多的東西，分兩塊

| 塊 | 內容 | 能否進上游 PR |
|---|---|---|
| **A. GitHub build apk** | 5 個 commit，**全部只動 `.github/workflows/build-apk.yml` 一個檔案**（+36 → +71 行） | ❌ **不能**。作者已明確拒絕過（PR #286：「Dictate is distributed through Google Play, and that is deliberate」—— 不要社群 APK 分發，會繞過 Play 的自動更新與簽章驗證） |
| **B. 我們的 docs** | `docs/zh-TW-setup.md`（+79，繁中設定指南） | ⚠️ 可保留但**須重新包裝**成給作者看的 `docs/zh-TW-ui-contribution.md` |

#### 關鍵教訓：基底不同步會讓 PR diff 被汙染

實測「若直接拿 fork 的 `main` 開 PR」會看到的 diff：

```
git diff upstream/main origin/main   →  20 個檔案, +190 / -305
```

其中 **16 個是上游 Kotlin 檔案** —— 那不是我們改的，而是**上游那 4 個 commit 的反向差異**（我們的 `main` 基底停在 2026-11-17）。
作者看到會以為「這個人在刪我的程式碼」→ **這種 PR 必被關閉**。

✅ **已修正**：`main` 已 merge `upstream/main`，現在 diff 只剩 **2 個純新增檔案**。

#### 最終架構（2026-11-20 升級定案：Topic Branches `pr/*` ＋ Self-Use Integration Branch `main`）

```text
                  ┌──► pr/zh-tw-ui          （功能 1：嚴格 4 檔 ──► 獨立向作者提 PR #1）
                  │
upstream/main ────┼──► pr/<feature-2>       （功能 2：獨立功能 ──► 獨立向作者提 PR #2）
 (作者原版)        │
      │           └──► pr/<feature-3>       （功能 3：獨立功能 ──► 獨立向作者提 PR #3）
      │                     │
      │ (作者升版時 merge)    │ (做完後單向 merge 進 main，不等作者回覆即可自用)
      ▼                     ▼
  我們的 main  ◄────────────┘
 (自用全功能整合主幹 = upstream/main + CI + l10n/工具鏈 + 工作表 + 所有已合入功能 ──► 直接跑 Actions 出 APK)
```

> ℹ️ **2026-11-20 演進說明**：初期階段（Phase A–E）曾以 `feat/zh-tw-ui` 作為開發分支、`main` 留作英文鏡像；待繁中 UI 驗收完成並準備擴展多個獨立改進（如 F2 貨幣符號 / 倉頡字根）後，已於同日將 `feat/zh-tw-ui` 合併入 `main`，正式定案為 **「`pr/*` 各自從 `upstream/main` 切出獨立提 PR ＋ 單向 `merge` 回 `main` 自用整合」** 的兩層架構。

**日常運作（方向永遠單向：`upstream/main` ➔ `pr/<feature>` ➔ `main`）**
1. **做新改進**：一律從 `upstream/main` 切出乾淨分支 `git checkout -b pr/<feature> upstream/main`（彼此完全隔離，不含 CI 與工作表）。
2. **立即自用出包**：切回 `main`，執行 `git merge pr/<feature>` 把功能收進自用主幹，直接在 `main` 觸發 Actions 出含全部功能的繁中 APK（`v6.4.0-apk`）。**嚴禁**把 `main` 反向合回或 rebase 到 `pr/<feature>`。
3. **翻譯生成檔同步**：`l10n/` 與 `tools/` 工具鏈留在 `main`；若需修改繁中用語，先在 `main` 跑生成腳本，再以 `git checkout pr/zh-tw-ui && git checkout main -- <目標 4 檔>` 同步到 PR 分支。
4. **上游升版**：執行 `git fetch upstream && git checkout main && git merge upstream/main`，Git 三方合併會自動把上游新版融合進來並保留我們的所有功能；尚在審核中的 `pr/*` 僅在需要對齊上游時執行 `git rebase upstream/main`。
5. **作者合併後**：該功能的 `pr/<feature>` 可功成身退刪除；`main` 下次 `merge upstream/main` 即自動對齊，維護負擔降為例行 merge。

> 📌 作者合併後**仍需跟上游** —— GitHub 的 fork 不會自動同步。我們的長期維護負擔從
> 「每個上游 commit 都要重做翻譯」降級為「定期 merge 上游」，這才是提 PR 的真正收益。

#### ⚠️ 已修正的 Release tag 撞名問題

兩條分支 `projectVersionName` 都是 `6.4.0` → workflow 的 `TAG="v${VERSION}-apk"` 相同 →
**在分支上跑 Actions 會 `--clobber` 掉 main 的 Release 資產**。

✅ 已修正（commit `82739341` / cherry-pick `7843e539`）：

```bash
BRANCH="${GITHUB_REF_NAME:-main}"
TAG="v${VERSION}-apk"
if [ "$BRANCH" != "main" ]; then
  SAFE_BRANCH=$(echo "$BRANCH" | sed 's/[^A-Za-z0-9._-]/-/g')
  TAG="v${VERSION}-apk-${SAFE_BRANCH}"
fi
```

實測：`main` → `v6.4.0-apk`（既有資產不動）／`feat/zh-tw-ui` → `v6.4.0-apk-feat-zh-tw-ui`

---

## Part 2 — 計畫（2026-11-20 修訂版）

### 2.0 修訂要點（依使用者決策）

| 決策 | 內容 | 對計畫的影響 |
|---|---|---|
| **D1** | **自己先做**（不先問上游） | Phase A 獨立推進，不等上游回應 |
| **D2** | **要開分支**，未來可行時提 PR 用 | 分支策略重新設計 → 見 2.1 |
| **D3** | **翻譯基底由英文翻**（不用 zh-rCN 再轉） | 見 2.3 的取捨分析 |
| **D4** | **先證明可用 → 提 issue → 提 PR 附證據** | 證據鏈升格為正式交付項 → 見 2.4 |

### 2.0.1 權威執行順序（2026-11-20 複查新增）

> ⚠️ **本節的順序優先於下方 Phase 分組的排列順序。** Phase A→B→C→D→E→F 只是**工作分類**，不是執行先後 —— 照字母順序走會先翻完 2547 條才驗證資源目錄命名，把風險押到最後。

| # | 步驟 | 對應 checkbox | 為什麼在這個位置 |
|---|---|---|---|
| 1 | 產出最小可行 zh-TW 資源（30–50 條） | **B0** | 便宜的第一次實機驗證 |
| 2 | 建驗證腳本 | **B0b** | 後面每一批翻譯都要靠它擋錯 |
| 3 | picker 加 `"zh-TW"`（1 行 Kotlin） | **C1** | 與 B0 一起構成最小可測組合 |
| 4 | 雲端編譯**冒煙測試**（無改動） | **A4** | 先確認 Actions 這條路本身是通的 |
| 5 | 雲端編譯 + 裝機實測（帶改動） | **C2 → C3** | **B0 的真正驗收點**：命名與 fallback 生效才算過 |
| 6 | 台灣用語 glossary | **B1** | 全量翻譯前先立規範 |
| 7 | 全量翻譯 app | **B2** | 分批，每批過 B0b |
| 8 | 翻譯 wear | **B3** | 見 1.2.1 的語言來源限制 |
| 9 | 用語校訂 | **D1–D3** | 全量完成後才有意義 |
| 10 | 與上游接觸 | **E1–E3** | 需要 5 的實機截圖證據 |
| 11 | 之後才做 | **F1–F4** | — |

**硬規則**：第 5 步（C3 的「B0 階段驗收」）**未通過前，不得進入第 7 步（B2 全量）**。

### 2.1 分支策略（D2 的落實 → 2026-11-20 升級為 `pr/*` + `main` 雙層架構）

> **📌 2026-11-20 架構升級定案**：
> Phase A–E 初期採用「單分支 `feat/zh-tw-ui` + 提 PR 前剝離 `pr/zh-tw-ui`」；待繁中 UI 驗收完成並準備獨立開發多個改進（F1–F3 等）後，已將 `feat/zh-tw-ui` 合併進 **`main`**，正式改採業界標準的 **「`pr/*` 獨立主題分支 ＋ `main` 自用整合主幹」** 雙層架構（完整拓撲見 1.6 節）：
> - **新功能開發與提 PR**：一律從 `upstream/main` 切出 `pr/<feature>`（如 `pr/zh-tw-ui`、`pr/fix-zhtw-currency`），互不干擾、各自獨立對上游開 PR。
> - **自用全功能出包**：做完的功能以 `git checkout main && git merge pr/<feature>` 單向合進 `main`（**絕不**把 `main` 反向 merge/rebase 回 `pr/*`），並直接於 `main` 觸發 Actions 出 APK。
> - **上游升級**：在 `main` 執行 `git fetch upstream && git merge upstream/main`，Git 三方合併自動保留所有自用功能；尚待審核的 `pr/*` 視需要 `git rebase upstream/main`。
>
> （以下保留 Phase A 當時的歷史策略設計與指令紀錄供查考。）

#### 問題

我們的 fork `main` 與上游已分歧：`fork_ahead 4 / fork_behind 6`。我們多出的 6 個 commit 是 5 個 CI + 1 個 docs，**上游不需要**（PR #286 已證明作者不想要社群提供的 APK 建置流程）。若直接用 fork `main` 提 PR，diff 會被這 6 個 commit 汙染。

#### 解法：雙分支

```
upstream/main
    │
    ├─► branch: feat/zh-tw-ui          ← 乾淨基底，專供將來提 PR
    │     （從 upstream/main 拉，diff 只有在地化改動）
    │     （CI workflow 需一併帶入，否則無法出 APK 驗證）
    │
    └─► branch: feat/zh-tw-ui-build    ← 驗證用，含我們自己的 CI workflow
          （= feat/zh-tw-ui + 我們 6 個 CI/docs commit）
          → 出 APK → 裝機驗證 → 截圖當證據
```

#### 兩分支的維護成本評估

| 做法 | 成本 | 評估 |
|---|---|---|
| **雙分支平行**（上圖） | 每次上游更新要同步兩邊 | ❌ 冗餘、易漏 |
| **單分支 + 乾淨基底 + 最後剝離** ✅ | 開發時只管一個分支；提 PR 前再 rebase | ✅ **採用** |

**採用方案（單分支，最後剝離）**：

- 開發分支 `feat/zh-tw-ui` 從**上游 `main`** 拉出，並**一併帶入我們的 CI workflow**（因為要出 APK 驗證）。
  - 帶入方式（**已實作**）：直接取 `origin/main` 的最終版 workflow 檔 →
    `git checkout origin/main -- .github/workflows/build-apk.yml`
  - 理由（**已查證**）：我們那 5 個 CI commit（`881f440` → `30dfe8a` → `fee1165` → `c89b926` → `e4c41fe`）
    **全部只動 `.github/workflows/build-apk.yml` 這一個檔案**（+36 → 逐步修到 +71 行），
    所以合成 1 個 commit 與 cherry-pick 5 次**結果完全相同**，但歷史乾淨、PR 剝離只需排除 1 個檔案。
- **提 PR 前**（Phase E1）另開一條乾淨分支，從 `upstream/main` 拉出，只帶 **在地化改動**（新 resource 目錄 + `OtherScreen.kt` 一行 + 給作者的說明文件），把 CI commit 排除。
- 兩條分支的差異僅限 **1 個** `.github/workflows/build-apk.yml` → 剝離成本極低。

#### 分支操作草稿（✅ A0/A1/A2 已實作）

```bash
# ✅ A0 取得本機 clone + 上游參考（已完成）
git clone https://github.com/kuniakil/DictateKeyboard.git ~/DictateKeyboard
cd ~/DictateKeyboard
git remote add upstream https://github.com/DevEmperor/DictateKeyboard.git
git fetch upstream

# ✅ A1 開發分支基底 = 上游 main（已完成）
git checkout -b feat/zh-tw-ui upstream/main

# ✅ A2 帶入我們的 CI workflow（1 個 commit，非 5 次 cherry-pick）
git checkout origin/main -- .github/workflows/build-apk.yml
git commit -m "ci: add manual Android Debug APK build workflow"

# E1 提 PR 前剝離（另開乾淨分支，只留在地化改動）
git checkout -b pr/zh-tw-ui upstream/main
git checkout feat/zh-tw-ui -- \
    app/src/main/res/values-zh-rTW/ \
    wear/src/main/res/values-zh-rTW/ \
    app/src/main/kotlin/.../OtherScreen.kt \
    docs/zh-TW-ui-contribution.md
git commit -m "..."
git push origin pr/zh-tw-ui
# → 對 DevEmperor/DictateKeyboard 開 PR
```

> ⚠️ 已驗證：上游那 4 個我們缺的 commit（`9b3fe20` / `46381a3` / `d09a673` / `84adfa9`）**都沒有動 `OtherScreen.kt`**，所以我們改的那一行不會立刻衝突。

### 2.2 Phase A — 分支與骨架

> ℹ️ **前置事實（2026-11-20 查證）**：**本機從來沒有 DictateKeyboard 的 clone。** 2026-11-17 建立 fork 與 CI 的全過程，是在 **GitHub 網頁版直接編輯**完成的（見 1.4）。因此本專案是**第一次**在本機擁有 repo。

- [x] **A0** `git clone` 到本機 → `~/DictateKeyboard`
      ```bash
      git clone https://github.com/kuniakil/DictateKeyboard.git ~/DictateKeyboard
      cd ~/DictateKeyboard
      git remote add upstream https://github.com/DevEmperor/DictateKeyboard.git
      git fetch upstream
      ```
      ✅ 已完成（2026-11-20）。`origin` = 我們的 fork，`upstream` = 上游。
- [x] **A1** 由 `upstream/main` 拉出 `feat/zh-tw-ui`
      ✅ 已完成。分支基底 = `upstream/main`（含上游那 4 個我們缺的 commit）。
- [x] **A2** 帶入我們的 CI workflow（讓 Actions 可出 APK）
      ✅ 已完成。**實作上優於原計畫的 cherry-pick 5 次**：已查證那 5 個 CI commit
      （`881f440` / `30dfe8a` / `fee1165` / `c89b926` / `e4c41fe`）**全部只動
      `.github/workflows/build-apk.yml` 這一個檔案**，故直接取最終版本即可：
      ```bash
      git checkout origin/main -- .github/workflows/build-apk.yml
      git commit -m "ci: add manual Android Debug APK build workflow"
      ```
      結果與 5 次 cherry-pick 等價，但**歷史乾淨、且 PR 剝離時只需排除 1 個檔案**。
- ℹ️ **注意**：`docs/zh-TW-setup.md` 只存在於 `main`，**`feat/zh-tw-ui` 上沒有**。要引用前先 `git checkout origin/main -- docs/zh-TW-setup.md`；E1b 的 PR 檔案清單不得帶入。
- ℹ️ **B5 補充**：`app/lint.xml` 把 `ExtraTranslation` 設為 warning，lint 不保證擋住缺漏 → 驗證要靠自寫的 key／placeholder 比對腳本，不靠 lint。
- ℹ️ **同步上游**：B2 開工前先 `git merge upstream/main`（上游 `strings.xml` 11 月改了 30 次），並以當下 base 重算基準數字。
- [x] **A3** 建 `docs/zh-TW-ui-contribution.md`（給作者看的說明；未來 PR 會帶上去）
- [x] **A4** 確認 Actions 可出 APK（**無改動的冒煙測試**）：`gh workflow run build-apk.yml --ref feat/zh-tw-ui`
      ✅ **2026-11-20 補勾：被 C2 涵蓋**（N/A）—— C2 run `44668198901` 已 success，等同驗證「Actions 這條路本身通不通」；
      若 C2 失敗才需回頭補跑 A4 判斷歸屬。**未另外執行無改動冒煙測試。**
      ✅ 2026-11-20 修正：tag 撞名已修（`7843e539`）。在 `feat/zh-tw-ui` 跑會發到
      `v6.4.0-apk-feat-zh-tw-ui`，**不會**動 `v6.4.0-apk`（舊版，仍指向 `e4c41fe`）。
      只有在 `main` 上跑才會 `--clobber` 掉 `v6.4.0-apk`。**無需特別備份 asset。**
      ℹ️ 與 C2 的分工：**A4 = 這條 CI 路徑本身通不通**（不含 zh-TW 改動）；**C2 = 帶 zh-TW 改動的正式產出**。兩者都會跑同一支 workflow，但目的不同。
      ℹ️ debug 版 applicationId 有 `.debug` 後綴，與 Play 版是兩個獨立 App，設定需另外輸入。

### 2.3 Phase B — 翻譯（D3：基底由英文翻）

#### 取捨分析：為什麼選「英文 base」

| | 方案甲：英文 base（採用） | 方案乙：zh-rCN 再轉 |
|---|---|---|
| 品質 | **高**。直接對英文原文翻，可精準對應 `comment="..."` 的翻譯指引 | 中。需先理解簡中譯文再改寫，語意繞路 |
| 與上游未來自做的相容性 | **高**。上游 20 個 locale 就是 AI 從英文 base 生的（`2f5c706`），我們同法同源 | 低。會變成「二手 AI 轉譯」，與他未來的 zh-TW 打架 |
| 補 36 條缺漏 | **自然**。base 2547 條全在，直接翻 | 要另外處理，且缺的那 36 條是最新功能，無參考譯文 |
| 保留 `comment` 指引 | **可保留 1614 條完整指引** | zh-rCN 只剩 544 條 comment，指引已流失 |
| 成本 | 較高（2547 條從零翻） | 較低 |
| 工具鏈 | 需自建英文→繁中流程 | 需 s2tw 轉換 + 台灣用語校正表 |

**結論：採方案甲。** 關鍵理由是**相容性** —— 上游的翻譯工作流就是「AI 從英文 base 翻」，我們用同法產出的 `values-zh-rTW` 才有機會被上游直接接受或合併進他的流程。

#### 流程

- [x] **B0** 最小可行驗證（先於 B1–B6；目的：證明 `values-zh-rTW` 命名與 fallback 可用）
  - ✅ 2026-11-20 完成：`app/src/main/res/values-zh-rTW/strings.xml` —— **45 strings + 3 plurals**（含 42 條 base 的 comment 指引、含 `{app_name}` / `{count}` / `{size}` / `{license_name}` / `%1$s` / `%2$s` / `%3$s` 各式 placeholder、1 組 plurals）
  - 涵蓋範圍：設定首頁、「其他」畫面（**語言選擇器所在**）、Dictate 浮動按鈕、Dictate 鍵盤、通用動作、單位複數
  - **刻意只放 45 條**，其餘留空 → 裝機後可驗「已翻顯示繁中、未翻退回英文」
  - 建 `app/src/main/res/values-zh-rTW/strings.xml`，只含約 40 條：`pref__other__settings_language__label`、設定首頁標題、Dictate 主要頁面標題、含 `%1$s` / `{app_name}` 的字串、1 個 plural
  - 保留 `comment` 屬性與 placeholder；其餘未翻條目**刻意不放**（用來驗證退回英文）
  - 語法層：`xmllint --noout` 通過
  - **⚠️ 真正的驗收不在這裡**：語法通過**不等於**命名有效。**B0 的驗收點 = C3 的「B0 階段驗收」**（見 2.4）—— 裝機後確認「已翻條目顯示繁中、未翻條目退回英文、無崩潰」。
    → 依 2.0.1，C3 未通過前不得進入 B2 全量。
- [x] **B0b** 建驗證腳本 **`tools/check-l10n.py`**：比對 key 集合、placeholder、`comment` 保留數、plurals
  - ✅ 2026-11-20 完成。用法：`python3 tools/check-l10n.py`（寬鬆，B0 階段）/ `--strict`（B5）/ `--module app|wear|all` / `--locale <dirname>`
  - 檢查：XML 合法性、key 集合（missing/extra）、placeholder（`{name}` 與 `%N$s`）、comment 保留、plurals quantity 結構
  - 負向測試已做：多出 key ✅ 抓到、placeholder 不符 ✅ 抓到、comment 被丟 ✅ 抓到
  - ⚠️ **基準數字以本腳本輸出為準**：`grep -o ' comment="'` 會把「XML 註解裡出現的同樣字面文字」也算進去 —— base 兩種算法都是 1618（1614 條在 `<string>`、4 條在 `<plurals>`），但我們的 zh-rTW 檔頭註解裡有 `comment="..."` 這段字 → grep 會算成 42、script 算 41（41 才對）
  - ⚠️ **檔名已統一為 `tools/check-l10n.py`**（2026-11-20 複查修正；原 CLAUDE.md 寫的 `tools/check_zh_tw.py` 已改）。理由：要同時驗 app + wear 兩個模組，名字得是通用的。
  - **基準數字一律動態取自當下的 base**（不要寫死任何數字 —— 上游還在動，`strings.xml` 11 月改了 30 次）。輸出為準。
- [x] **B1** 建立台灣用語 glossary（英文 → 台灣繁中），以 1.3 對照表為底（已建立 `l10n/glossary-zh-tw.json`）
- [x] **B2** 批次翻譯 `values/strings.xml` → `values-zh-rTW/strings.xml`（`000`–`036` 共 37 批，2558 / 2558 條全數譯完）
  - 執行方式：由 agent 分批直接翻（每批約 100–200 條），每批過 `tools/check-l10n.py`，不使用外部翻譯 API
  - 輸入：英文原文 + `comment="..."` 翻譯指引（1614 條）
  - **必須保留**：`comment` 屬性、placeholder（`{app_name}` / `%1$s` / `{count}`）、XML 轉義
  - 輸出結構與 base 完全對齊（**數字動態取自當下 base**；2026-11-20 實查 = 2547 strings + 11 plurals）
- [x] **B3** 翻譯 `wear/src/main/res/values/strings.xml` → `values-zh-rTW/strings.xml`（`l10n/wear-zh-tw.json`，69 / 69 條）
  - ⚠️ **wear 的資源跟「手錶系統語言」，不跟手機 App 的 in-app 語言選擇器**（見 1.2.1，wear 模組無任何 Locale/Configuration 覆寫）
  - **開工前先決定驗證方式**：① 手錶系統語言設為 zh-TW 實測；或 ② 放棄 wear 截圖，只交付資源檔並在 PR 說明中標註此限制
  - 若走 ①，截圖須標註「手錶系統語言 = 繁體中文（台灣）」，避免誤導作者
- [x] **B4** `strings_dont_translate.xml`（32 條）**不翻**（已確認原封不動，且 `values-zh-rTW/` 不建立同名檔案）
- [x] **B5** 驗證：
  - [x] key 集合與 base 完全一致（當下 base 的 string + plurals 全數；數字動態取，不得寫死 2547 / 11）
  - [x] placeholder 逐條比對，mismatch = 0（基準：base vs zh-rCN 實測為 0）
  - [x] `comment` 屬性保留數 **= base 的當下 comment 數**（動態比對；實查 `app` = 1618 / 1618、`wear` = 0 / 0）
  - [x] XML 合法（`xmllint`）
  - [x] lint 無 `MissingTranslation`（本機無 JDK/Android SDK；改由 Actions `assembleDebug` / `aapt2` 資源合併驗證）
        ✅ **2026-11-20 補勾**：C2 run `44668198901`（`assembleDebug` + `aapt2` 資源合併）已 success，
        且 APK 內 `resources.arsc` 已解析確認 zh-TW chunk 正確掛載（見 Part 0「APK 層級的資源驗證」）
        → 資源合併層級的 `MissingTranslation` 已被 Actions 建置驗證涵蓋。
  - [x] wear 模組同樣跑一次 `tools/check-l10n.py`（`--strict` 通過）
- [x] **B6** 台灣用語複查（掃描殘留大陸用語，歸零；並統一 `長壓` → `長按`、修正 `024` 未譯片段與錯字）

### 2.4 Phase C — 讓繁中介面真的出現（D4 的關鍵：證明可用）

> 這是整個計畫的**樞紐**。沒有這一步，後面的 issue 與 PR 都只是「我打算做」。

- [x] **C1** 在 `OtherScreen.kt` 的語言 tag 清單加入 `"zh-TW"`（清單目前 40 個 tag，`zh-CN` 在最後）
  - ✅ 2026-11-20 完成：`OtherScreen.kt:162`（緊接 `"zh-CN",` 之後）。tag 數 40 → **41**（+ `auto` = 42 項），已確認無重複
  - `FlorisLocale.fromTag("zh-TW")` 會解析成 `Locale("zh","TW")` ✅（複查確認：`DELIMITER_SPLITTER` 同時接受 `-` 與 `_`；`languageTag()` 回傳 `"zh-TW"`，與既有 `"zh-CN"` 同一格式）
  - 顯示名稱由 `locale.displayName()` 產生，無需自訂
  - `FlorisAppActivity.kt:101-105` 已監聽 `prefs.other.settingsLanguage` 並即時 `createConfigurationContext` → **不需重啟 App 即生效**
  - ℹ️ 插入位置：`OtherScreen.kt:161` 的 `"zh-CN",` 之後（清單為字母序，`zh-TW` 應在 `zh-CN` 後）
- [x] **C2** 走 Actions 出 APK（本機未確認有 Android SDK，不採本機建置）—— **帶 zh-TW 改動的正式產出**
  - ✅ 2026-11-20 完成全量版建置：run `44668198901`（commit `be4913ed`，耗時 `13m41s`），發佈至 Release `v6.4.0-apk-feat-zh-tw-ui`（`174,483,318` bytes），並驗證固定簽章 SHA-256 `AD:52:6F:35:D6:3D:10:18:FA:BD:C0:8D:CA:54:18:7C:11:40:B6:F8:2A:15:0D:8B:5E:92:B5:DF:4D:74:31:A3`
  - 我們的 `build-apk.yml` 是 `workflow_dispatch` 手動觸發 ✅
  - 分支建置發到 `v6.4.0-apk-<分支名>`，不會覆蓋 `v6.4.0-apk`（已修正，見 A4）
  - 與 A4 的分工見 2.0.1：A4 是無改動冒煙測試，本項是正式產出
- [x] **C3** 裝機實測（證據鏈起點）
  - [x] App → 設定 → 其他 → 語言 → 選「中文 (台灣)」→ 確認 UI 立即切換
  - [x] 走查：設定首頁 / Dictate / providers / 佈景主題 / 剪貼簿 / 使用者字典 / learned words
  - [x] **wear 設定走查**：⚠️ wear 跟的是**手錶系統語言**，不跟手機 in-app 選擇器（見 1.2.1）→ 本輪略過實錶走查，於 issue/PR 說明此限制（採用 B3 方案②）
        ✅ **2026-11-20 補勾**：採用 B3 方案② —— 資源檔已交付（69/69 條），限制說明已寫入 `#492` issue 與 `docs/zh-TW-ui-contribution.md`（PR 會一併帶上）。
        若日後拿到實錶、且手錶系統語言可設為 zh-TW，可再補實錶截圖（見 Part 0 情境 4）。
  - [x] 確認無殘留英文、placeholder 顯示正常（`%1$s` / `{v}` 插值）、無崩潰
  - [x] **B0 階段驗收（= B0 的正式驗收點，見 2.0.1）**：全量繁中實測通過，無崩潰；picker 顯示名稱實測為 **`中文 (台灣)`**
- [x] **C4** **產出證據（截圖集）**（已存於 Nextcloud `/mnt/kuniaki/文件/DictateKeyboard`，共 12 張，隱私已檢查無外洩）
  - 語言選擇器（拍到「中文 (中國)」與「中文 (台灣)」並列）
  - 設定首頁（繁中）
  - Dictate 設定頁（繁中）
  - providers / 佈景主題 / 剪貼簿 / 使用者字典 頁（繁中）
  - learned words 頁（繁中）
  - **對照組**：同一「其他」頁的英文版、簡中版與繁中版三語對照（`12-12-47` / `12-13-01` / `12-13-10`）
  - ⚠️ wear 截圖（若有）：必須標註「手錶系統語言 = 繁體中文（台灣）」，不可讓人誤以為是手機 in-app 選擇器帶動的（本輪略過）

> 💡 證據的呈現方式：issue 用截圖，PR 用截圖 + 說明。**重點是讓作者一眼看出「這是台灣使用者實際看到的畫面」，而不是抽象的翻譯檔案。**

#### 2.4.1 兩層論述要拆開（2026-11-20 複查新增 —— E2b 開 issue 時直接用）

原工作表把「台灣使用者今天看到英文」與「要加 picker 條目」混為一件事。實際上是**兩層**，混著講會被作者挑掉：

| 層 | 命題 | 需要什麼才能成立 |
|---|---|---|
| **層 1 — 資源層（不需改 Kotlin）** | 台灣使用者（**系統語言 = zh-TW**）打開 App 看到的是**英文**，因為上游只有 `values-zh-rCN`，而 zh-rCN 隱含 script=Hans，**不會**被 zh-Hant 裝置匹配 | 只需新增 `values-zh-rTW/` 資源目錄。**與 picker 無關** |
| **層 2 — 選擇器層（需改 1 行 Kotlin）** | 即使系統語言不是中文，使用者也**無法**在 App 內把介面切成繁中 —— picker 的 40 個 tag 裡沒有 zh-TW | 需要 C1 那 1 行 |

→ **層 1 是 issue 的主論點**（不需要作者先接受任何 Kotlin 改動，純資源貢獻）；**層 2 是 PR 的完整度訴求**。
→ 另可佐證層 1：`minSdk = 26`（≥ API 24）→ script-aware 資源解析保證成立，不存在「舊 Android 掉進簡體」的例外。

### 2.5 Phase D — 台灣用語校訂

- [x] **D1** 依 1.3 對照表 + glossary 逐條套用
- [x] **D2** 重新掃描殘留大陸用語，確認歸零（另清除殘留英語片語與 Big5/繁體字元外之簡體字）
- [x] **D3** 依 `comment="..."` 的語氣要求複查（`dictate__*` 長度/用詞一致性已抽查核對）

### 2.6 Phase E — 與上游接觸（D4：issue → PR 附證據）

#### 關於「以 fork 身分提 PR」的流程確認 ✅

**是的，fork 提 PR 是完全正常、也是 GitHub 預設的貢獻途徑**，沒有任何問題：

- 我們的 fork `kuniakil/DictateKeyboard` 是上游 `DevEmperor/DictateKeyboard` 的 fork（GitHub 會自動設定 `parent` 關係，已實查確認 `fork: true`）。
- PR 開法：從 **我們 fork 的分支** 對 **上游的 `main`** 開（GitHub 網頁版：「New pull request」→ compare 選 `DevEmperor:main` ← `kuniakil:<branch>`）。
- GitHub 會自動標示「`kuniakil` wants to merge 1 commit into `DevEmperor:main` from `kuniakil:pr/zh-tw-ui`」。
- **作者端只需按一次 merge**（他可以 squash / rebase / merge 皆可）。
- 這正是上游自己鼓勵的方式：README 的 Contributing 段落寫「The best way to help right now is to **open an issue**」，
  且社群 PR（MyButtermilk #223/#216/#215/#210、karaokedjodua #168/#167）**都是這樣被合併的**。

**唯一的注意事項**：PR 的 diff 必須乾淨。我們的 fork `main` 有 6 個上游不需要的 commit（5 個 CI + 1 個 docs），
若直接拿 `origin/main` 開 PR，那 6 個 commit 會全部混進 diff → 作者幾乎必然關閉（PR #286 的先例）。
所以 Phase E1 的「剝離」是**必要步驟**，不是可選項。

#### E1 — 提 PR 的乾淨分支準備（可與 Phase C 並行準備，最後才推）

- [x] **E1a** 從 `upstream/main` 拉出 `pr/zh-tw-ui`
- [x] **E1b** 只帶入在地化改動（排除我們的 CI commit）：
      `app/src/main/res/values-zh-rTW/`、`wear/src/main/res/values-zh-rTW/`、`OtherScreen.kt`（1 行）、`docs/zh-TW-ui-contribution.md`
- [x] **E1c** 驗證 diff 乾淨：`git diff upstream/main --stat` 應只有上述 4 項
- [x] **E1d** rebase 到最新 `upstream/main`（已於最新 `upstream/main` `84adfa99` 上切出，無新 commit）
- [x] **E1e** 推上去：`git push origin pr/zh-tw-ui`（推到**我們的 fork**）
- [ ] **E1f** 開 PR：compare `DevEmperor:main` ← `kuniakil:pr/zh-tw-ui`（⚠️ 待 E2 issue 討論後再執行；文案見 `docs/upstream-outreach-drafts-20261120.md`）
  - ⚠️ **2026-11-20 複查：尚未執行**。分支已就緒（`origin/pr/zh-tw-ui` = `e952b131`，基於 `upstream/main` `84adfa99`，diff 嚴格 4 檔，無需 rebase）。
  - 📌 **2026-11-20 使用者決策：已決定「不搶先開 PR，等作者回覆 #492」** → 本項**不是待決項**，是刻意不執行。作者回覆歡迎時才執行（見 Part 0 決策表情境 1）。

#### E2 — 先在 issue #483 留言建立連結

- [x] **E2a** 在 **#483「Dictation in traditional chinese」**（2026-11-15 開，原 0 回覆，作者 `crazywing`）留言
  - ✅ 2026-11-20 已發佈：https://github.com/DevEmperor/DictateKeyboard/issues/483#issuecomment-7030540460
  - 給出繁中 STT 的實際解法：`Punctuation & style → Custom style prompt` 填繁中引導句 + `Rewording → Manage prompts` 開 `Apply automatically`
  - 這正是 `docs/zh-TW-setup.md` 驗證過的組合 → **展示我們真的在用這個 App**
  - 附帶說明我們已完成 zh-TW UI 介面並附上 `#492` 連結
- [x] **E2b** **新開 issue**「Traditional Chinese (zh-TW) UI translation」
  - ✅ 2026-11-20 已開立：https://github.com/DevEmperor/DictateKeyboard/issues/492 （圖床分支：`assets/zh-tw-screenshots`）
  1. 台灣用戶目前拿到**英文**（附資源解析規則與 `createConfigurationContext` 機制）
     - ⚠️ **依 2.4.1 拆成兩層寫**：層 1（資源層，不需要改 Kotlin）是主論點；層 2（picker 少一個 tag）才是需要動 Kotlin 的部分
     - 佐證：上游已有 20 個 locale 目錄，但 `ast` / `sq` / `ur` / `et` **有資源卻不在 picker 清單** → 上游並不要求 picker 與資源目錄一致，可作為「資源層先行」的論述
  2. 我們已做好的 zh-TW 介面 + **實機截圖證據**（三語並列 3 張 + 語言選擇器 + Dictate 設定 + 已學習的字詞，共 6 張）
  3. 我們的維護方案（見 2.7，`docs/zh-TW-ui-contribution.md`）
- [ ] **E2c** 等待作者回應（作者活躍，issue 與 PR 都有回覆；他的習慣是先談再收；回應後的對策見 Part 0「作者回覆後的應對決策表」）
  - ⚠️ **2026-11-20 複查：上游目前沒有我們的 PR**（`author:kuniakil` 的 PR 數 = 0；上游 PR 總數 38 筆無 ours）。只有 Issue `#492` + `#483` 留言。
  - 📌 **2026-11-20 決策：已開 issue 就等回覆，不主動開 PR、不主動 ping**
  - 📌 若 2 週內無回覆（**2026-12-04** 之後）→ 依 Part 0 情境 7 處理（維持 fork 自用、推進 Phase F、或在 `#492` 禮貌 ping 一次）。

#### E3 — 提 PR

- [ ] **E3a** 由 `pr/zh-tw-ui` 對 `DevEmperor/DictateKeyboard:main` 開 PR
- [ ] **E3b** PR 內容必含：
  - [ ] **實機截圖證據**（繁中 vs 英文 vs 簡中三語對照）
  - [ ] 說明維護方案（見 2.7）→ 這是 PR 能否被接受的關鍵
  - [ ] 明確標示只改資源檔 + 1 行 Kotlin，無其他變更
- [ ] **E3c** 依作者回覆調整（他關閉 PR 時通常會附完整理由 —— 見 PR #286 / #442 的先例）

### 2.7 維護方案（D4 的核心：讓上游能長期接受）

這是整份計畫**最需要說服作者**的一點。

上游的模型是「**作者自己 + AI 批次生成**，每個功能 commit 同步更新全部 20 個 locale」。因此：

- ❌ **靜態 `values-zh-rTW` 檔案** → 他無法維護（每個上游 commit 都會漂移；上游 11 月改了 `strings.xml` **30 次**）
- ✅ **可插入他既有流程的轉換器** → 永不漂移

**因此 PR 的交付物應包含：**

1. `values-zh-rTW/strings.xml`（完整成品，供他直接採用）
2. **台灣用語 glossary**（英文 → 台灣繁中的對照表，機器可讀，如 JSON/YAML）
3. **翻譯 prompt／流程說明**：他的 AI 批次流程是「英文 base → 各 locale」，與 D3 同源。我們交付「zh-TW 翻譯 prompt（內含 glossary 與台灣用語規則）」，他只要在批次流程多加一個 locale 目標，就能得到與 base 同步的 zh-TW。
   - **關鍵優勢：不需要他改流程架構，只多一個 locale + 一份 glossary。**
   - ⚠️ 2026-11-20 修正：原寫「zh-rCN → zh-TW 後處理腳本」與 D3（不從 zh-rCN 轉）矛盾，已改為英文 base 直譯。
   - 另附自動驗證腳本（B5：key／placeholder 比對），可接進他的流程。

> ⚠️ 若他回覆「我自己用 AI 翻就好」（依 1.1 發現 2 這可能性不低），則：
> - 我們仍保有自己 fork 的 zh-TW 版本（對我們自己有用）
> - glossary 對他仍有價值（AI 不會自動知道「剪貼簿」「資料夾」「智慧」這些台灣慣用語）
> - 這不算失敗 —— **我們自己拿到繁中介面就是主要目標**

### 2.8 Phase F — 之後才做（順序不變）

- [ ] **F1**（原 P3）繁中實用 Rewording Prompts → 依 `schema.json` 放進 `prompt-library` 的 `submissions/` → 提 PR（CI 跑 `validate.py`）。**注意：此項與 Phase E 的上游互動經驗直接相關，應在 E 之後。**
- [x] **F2**（原 P2）倉頡字根顯示 + `zh-TW-*` 預設貨幣修正 ✅ **2026-11-20 完成實作（分支 `pr/cangjie-layout`，commit `3c3a7a5a`，已單向合入 `main`）**
  - 經實查現有引擎（`TextKeyData.kt`、`HanShapeBasedLanguageProvider.kt`、`han.sqlite3`）後確認**無需修改 Kotlin 碼**，只新增/調整 3 個 JSON 設定檔：
    1. 新增 `app/src/main/assets/ime/keyboard/org.florisboard.layouts/layouts/characters/cangjie.json`：採選項 A（`case_selector`）—— 一般狀態顯示標準 Gboard 倉頡字根（手田水口廿卜山戈人心 / 日尸木火土竹十大中 / 重難金女月弓一）並送出小寫 ASCII `a`–`z`；按 Shift 時切換顯示大寫英文字母 `Q`–`M`（`A`–`Z`）。
    2. `app/src/main/assets/ime/keyboard/org.florisboard.layouts/extension.json`：在 `layouts.characters` 註冊 `"id": "cangjie", "label": "倉頡 (Cangjie)"`。
    3. `app/src/main/assets/ime/keyboard/org.florisboard.localization/extension.json`：將 `zh-TW-cangjielarge` 的 `preferred.characters` 改為 `org.florisboard.layouts:cangjie`，並將 `zh-TW-boshiamy` 與 `zh-TW-cangjielarge` 的 `currencySet` 由 `org.florisboard.currencysets:yen` 改為 `org.florisboard.currencysets:dollar`。
  - 獨立乾淨分支 `pr/cangjie-layout` 已推上 `origin`（隨時可開獨立 PR），並已單向 `merge` 進 `main` 供自用出包（裝機後舊有子類型需於「設定 → 語言與配置 → 字元配置」改選「倉頡 (Cangjie)」或重加子類型）。
  - ✅ **雲端建置驗證（2026-11-20）**：於 `main`（`22248d26`）觸發 Actions run `44747287202` → **success**（耗時 `13m51s`），已發布含**繁中 UI ＋ 倉頡字根 ＋ `$` 貨幣**之 `app-debug.apk`（`174,484,075` bytes，SHA-256 `3477b89916a0eb485dc4369bfb465d73cb99fb92443da5371820e7487a402e12`）至 Release `v6.4.0-apk`，固定簽章指紋完全吻合（`AD:52:6F:35:...74:31:A3`），待實機覆蓋安裝測試。
- [ ] **F3**（原 P4）Feature request：dictation 文字進學詞庫 + 社群共享字典。前提已驗證成立（`LearnedWordsStore.note()` 只被 `LatinLanguageProvider` 呼叫）。
- [ ] **F4** OpenTypeless 備份清理（`~/Library/Application Support/com.opentypeless.app/backups/`，實測 4.4 MB，2026-11-17 建立）→ 觀察 1–2 週穩定後可刪

---

## Part 3 — 風險

| 風險 | 說明 | 緩解 |
|---|---|---|
| **上游漂移**（高） | 靜態 `values-zh-rTW` 檔案在每個上游 commit 都會過期（上游 11 月改了 30 次） | 2.7：交付 glossary + 後處理腳本，而非只有靜態檔案；我們自己的 fork 不受影響 |
| **分支污染**（高） | 我們的 6 個 CI commit 若混進 PR，diff 會被汙染 → 作者可能直接關閉 | 2.1：單分支開發 + 提 PR 前剝離（`pr/zh-tw-ui`）；E1c 有明確驗證點 |
| **翻譯品質／一致性**（中） | 2547 條從零翻，可能有前後不一致（同一概念不同譯法） | glossary 先行（B1）；複查階段（D1–D3）；我們有 `zh-TW-setup.md` 的既有慣用語可沿用 |
| **作者自己翻**（中） | 依 1.1 發現 2，他的模型就是自己 + AI 生成 | 交付 glossary（AI 不會自動知道台灣慣用語）；主要目標是我們自己拿到繁中介面，非必被接受 |
| **Release 資產被覆蓋**（極低） | 僅在 `main` 上跑 workflow 才會 `--clobber` `v6.4.0-apk`；分支已用獨立 tag | 不要在 `main` 上隨手觸發 |
| **PR #97 的先例**（低） | 社群翻譯 PR 曾被無留言關閉 | 先開 issue 建立關係（D4）；且 2.7 的交付型態與 #97（純檔案）不同 |
| **`values-zh-rTW` 涵蓋範圍**（低） | `zh-rTW` 隱含 script=Hant，但 **zh-HK / zh-MO 不會匹配** | 跟上游全用 legacy `r<REGION>` 命名（`zh-rCN` / `ko-KR` / `pt-BR` / `lv-LV`）的慣例一致 → 先用 `values-zh-rTW`；取捨在 E2b 跟作者談 |
| **上游 Kotlin 碼衝突**（低） | 改 `OtherScreen.kt` 會與上游未來改動衝突 | 已驗證上游那 4 個 commit 都没動 `OtherScreen.kt`；E1d 提 PR 前 rebase |
| **wear 語言來源**（低-中） | wear 資源跟**手錶系統語言**，不跟手機 App 的 in-app 語言選擇器 → 翻了可能看不到，C3 走查易誤判 | 見 1.2.1：B3 前先定驗證方式（手錶系統語言實測，或放棄 wear 截圖並在 PR 說明）；截圖需標註語言來源 |

---

## Part 4 — 已定案事項（2026-11-20）

| # | 事項 | 決策 |
|---|---|---|
| Q1 | 翻譯基底 | ✅ **由英文 base 翻**（理由見 2.3：與上游 AI 批次流程同源，相容性高） |
| Q2 | 分支 | ✅ **2026-11-20 升級為「`pr/*` 獨立主題分支 ＋ `main` 自用整合主幹」雙層架構**（見 1.6、2.1 節）：初期採單分支 `feat/zh-tw-ui` + 剝離出 `pr/zh-tw-ui`；同日已將 `feat/zh-tw-ui` 併回 `main` 作為全功能整合主幹，未來每個新功能直接從 `upstream/main` 切乾淨 `pr/<feature>` 分支獨立開發與提 PR，並單向 `merge` 回 `main` 自用 |
| Q3 | 執行順序 | ✅ **自己先做 → 證明可用 → 提 issue → 提 PR 附證據**（D4） |
| Q4 | wear（69 條） | ✅ 一併做（B3），但排在主 App 之後。⚠️ 補充（2026-11-20 複查）：wear 資源跟**手錶系統語言**，不跟手機 in-app 選擇器 → B3 前先定驗證方式（見 1.2.1） |
| Q5 | TODO.md 的 P1 條目 | ✅ **已結案（2026-11-20 補勾）**<br>**TODO.md 位置已確認**：不在本 repo，而在 **`~/kubernetes/TODO.md`**（第 52–65 行的 DictateKeyboard 區塊）。<br>「零衝突不改 Kotlin 碼」的錯誤假設**早已修正並寫入** `~/kubernetes/TODO.md` 第 56 行（明載需動 `OtherScreen.kt` 一行）→ 本項實質工作已完成。<br>（同日亦已把該處 P1 狀態由「進行中」更新為「✅ 已完成（截至 E2）／⏳ 等作者回覆 #492 後開 PR」。） |
| Q6 | 驗證腳本檔名 | ✅ **統一為 `tools/check-l10n.py`**（2026-11-20 複查；原 CLAUDE.md 的 `tools/check_zh_tw.py` 已同步更正） |
| Q7 | Release 資產備份 | ✅ **不必備份**（2026-11-20 複查）：分支建置已用獨立 tag `v6.4.0-apk-<分支名>`，不會動 `v6.4.0-apk`；只有刻意在 `main` 上跑才會 clobber。CLAUDE.md 的舊警告已同步移除 |

---

## Part 5 — 已驗證事實索引（可重跑）

```bash
# 上游 locale 是否有 zh-rTW
gh api repos/DevEmperor/DictateKeyboard/contents/app/src/main/res --jq '[.[].name] | map(select(test("zh")))'
# → ["values-zh-rCN"]

# 上游 app 語言清單（缺 zh-TW）
gh api repos/DevEmperor/DictateKeyboard/contents/app/src/main/kotlin/dev/patrickgold/florisboard/app/settings/advanced/OtherScreen.kt

# fork 分歧
gh api repos/DevEmperor/DictateKeyboard/compare/kuniakil:main...main --jq '{ahead:.ahead_by,behind:.behind_by}'
# → {"ahead":4,"behind":6}

# 上游有無 zh-rTW 相關 PR
gh search prs --repo DevEmperor/DictateKeyboard "zh-rTW OR traditional" --json number,title,state
# → []

# issue #483
gh issue view 483 -R DevEmperor/DictateKeyboard --json title,state,comments
# → "Dictation in traditional chinese" / OPEN / 0 comments

# 我們的 build workflow 是手動觸發（提 PR 分支也能出 APK）
gh api repos/kuniakil/DictateKeyboard/contents/.github/workflows/build-apk.yml --jq '.content'
# → on: workflow_dispatch

# 上游那 4 個 commit 有沒有動 OtherScreen.kt
for c in 9b3fe20 46381a3 d09a673 84adfa9; do
  gh api repos/DevEmperor/DictateKeyboard/commits/$c --jq '[.files[].filename]|map(select(test("OtherScreen")))'
done
# → 全部空 → 不衝突

# fork 6 個 commit 的署名（證明是網頁版，非本機 git）
gh api repos/kuniakil/DictateKeyboard/commits --jq '.[] | "\(.sha[0:7]) \(.commit.author.name) \(.author.login)"'
# → kuniakil kuniakil（login 名署名；本機 git 會是 "Michael Lee"）

# 本機 git 署名對照組
cd ~/kubernetes && git log --format="%an <%ae>" -1
# → Michael Lee <kuniaki.lee@gmail.com>

# fork 的 Actions 執行時序（每個 commit 後手動觸發）
gh api repos/kuniakil/DictateKeyboard/actions/runs --jq '.workflow_runs[] | "\(.created_at) \(.head_sha[0:7]) \(.conclusion)"'

# 本機確實沒有 clone（應為空）
find ~ -maxdepth 7 -name ".git" -type d -not -path "*/Library/*" 2>/dev/null \
  | while read g; do git --git-dir="$g" config --get remote.origin.url; done | grep -i dictate
mdfind "kMDItemFSName == '*ictate*'c" | grep -v kubernetes
```

### 2026-11-20 二次複查新增的可重跑指令

```bash
# wear 模組是否有任何 Locale / Configuration 覆寫（答案：沒有 → wear 跟手錶系統語言）
grep -rn "Locale\|createConfigurationContext\|setLocale" wear/src/main/kotlin --include="*.kt"
# → 0 命中

# picker 的 tag 清單（zh-CN 在最後一行，插 "zh-TW" 在其後）
grep -n '"zh-CN"' app/src/main/kotlin/dev/patrickgold/florisboard/app/settings/advanced/OtherScreen.kt
# → 161:  "zh-CN",

# FlorisLocale.fromTag 的分隔符規則（- 與 _ 都接受 → "zh-TW" 可用）
grep -n "DELIMITER_SPLITTER\|DELIMITER_LANGUAGE_TAG" \
  app/src/main/kotlin/dev/patrickgold/florisboard/lib/FlorisLocale.kt

# minSdk（≥24 才保證 script-aware 資源解析）
grep -n "projectMinSdk" gradle.properties
# → projectMinSdk=26

# base / zh-rCN 的 key 集合差異（動態取數，不寫死）
python3 - <<'EOF'
import re
def names(p):
    return set(re.findall(r'<(?:string|plurals)\s[^>]*name="([^"]+)"', open(p,encoding='utf-8').read()))
b = names('app/src/main/res/values/strings.xml')
c = names('app/src/main/res/values-zh-rCN/strings.xml')
print('base:',len(b),'zh-CN:',len(c),'missing:',len(b-c),'extra:',len(c-b))
EOF

# comment 屬性數量（動態取數）
grep -o ' comment="' app/src/main/res/values/strings.xml | wc -l
# → 1618（2026-11-20）

# 上游現況（複查當下）
gh api repos/DevEmperor/DictateKeyboard/contents/app/src/main/res --jq '[.[].name]|map(select(test("zh")))'
# → ["values-zh-rCN"]
gh issue view 483 -R DevEmperor/DictateKeyboard --json state,comments --jq '{s:.state,c:(.comments|length)}'
# → {"s":"OPEN","c":0}
```

---

*本文件由 Claude Code 撰寫，數據皆為 2026-11-20 實查。Part 2 於同日依使用者決策（D1–D4）修訂，並於同日第二次 review 補上 9 項落差修正（見 Part 0「2026-11-20 二次複查修正」），第三次 review 再補上 5 項（見 Part 0「2026-11-20 三次複查修正」；其中確認**上游尚無我們的 PR**，僅有 Issue #492）。*
