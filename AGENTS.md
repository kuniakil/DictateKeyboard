# AGENTS.md — DictateKeyboard 繁體中文（zh-TW）在地化

> **這是 opencode / Antigravity 進入 `~/DictateKeyboard/` 時自動注入的專案規則。**
> 全域常識見 `~/.config/opencode/GLOBAL.md`。
> 與其他 agent 共享 `~/DictateKeyboard/CLAUDE.md`（內容同步，可當交叉參考）。
>
> ⚠️ **本 repo 與 `~/kubernetes/` 叢集完全無關** —— 別套用那邊的 helm / kubectl / kustomize 守則。

---

## 📍 這是什麼

`DevEmperor/DictateKeyboard` 的 fork。**目前唯一的進行中工作：新增繁體中文（台灣）介面。**

Fork 的兩個目的：
1. **產 APK** —— 作者只在 Play 上架付費版、GitHub Releases 不附 APK。我們用 GitHub Actions 雲端編譯 debug APK（固定簽章 → 可覆蓋升級）。
2. **提 PR** —— 讓作者看到繁中方案可行；他若合併，以後我們就不用自己維護繁中 UI。

---

## 📖 立刻先讀

**`docs/worksheet-dictatekeyboard-zhtw-ui-20261120.md`** —— 完整工作表（686 行）。內含：

- Part 1 調查結果（三個決定性發現、工程事實、台灣用語表、2026-11-17 操盤歷史查證、簽章金鑰位置、分支架構）
- Part 2 計畫（Phase A–F，每項都是可勾選的 checkbox）
- Part 3 風險、Part 4 已定案事項、Part 5 可重跑的驗證指令

**不要重做調查** —— 關鍵事實都已在工作表內驗證過（上游 locale 結構、app 語言選擇器位置、2547 條資源數量、fork 分歧狀態、簽章金鑰位置…）。

---

## 🌿 Repo 拓撲

| remote | 指向 | 用途 |
|---|---|---|
| `origin` | `kuniakil/DictateKeyboard`（我們的 fork） | 推送分支、開 PR 的來源 |
| `upstream` | `DevEmperor/DictateKeyboard`（上游） | 追蹤上游更新、PR 的目標 |

| 分支 | 角色 | 能直接開 PR？ |
|---|---|---|
| `main` | 我們的**發行分支** = `upstream/main` + 我們的 CI + docs。已 merge 上游 2026-11-18（diff vs 上游只剩 2 個純新增檔案）。Actions 在此出正式 APK | ❌ 含 `build-apk.yml` |
| `feat/zh-tw-ui` | **當前工作分支**，基底 `upstream/main` + CI + 工作表 | ❌ 同上 |
| `pr/zh-tw-ui` | 提 PR 用（Phase E1 才建立），由 `upstream/main` 拉出後只帶在地化改動 | ✅ |

⚠️ **不要拿 `main` 或 `feat/zh-tw-ui` 直接開 PR** —— 作者已明確拒絕過社群提供的 APK 建置流程（上游 PR #286：「Dictate is distributed through Google Play, and that is deliberate」）。提 PR 必須走 `pr/zh-tw-ui` 剝離流程。

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
# 資源 key 集合與 placeholder 必須與 base 完全對齊（基準：base vs zh-rCN mismatch = 0）
#   工具待建立（Phase B0b / B5）
python3 tools/check-l10n.py

# XML 合法性
xmllint --noout app/src/main/res/values-zh-rTW/strings.xml

# lint（需本機 JDK 21 + Android SDK）
./gradlew :app:lintDebug

# 雲端編譯（Actions）
gh workflow run build-apk.yml --ref feat/zh-tw-ui
```

⚠️ Release 資產：**在分支上跑不會覆蓋 `v6.4.0-apk`**（已修：分支用獨立 tag `v6.4.0-apk-<分支名>`）。
只有**刻意在 `main` 上跑**才會 `--clobber` 掉 `v6.4.0-apk`（= 手機上裝的那個）→ 不要在 `main` 上隨手觸發。
（2026-11-20 複查修正：舊版「動手前先備份既有 asset」的說法已過時。）

---

## 🗣️ 與上游互動的關鍵背景

- 上游翻譯由**作者自己用 AI 批次生成**，每個功能 commit 同步更新全部 20 個 locale（同一 SHA）。
  → 靜態 zh-TW 檔案必然漂移 → **交付物要含「glossary + 後處理轉換器」**，而非只有檔案。
- 上游 open issue **#483「Dictation in traditional chinese」**（2026-11-15 開、0 回覆）= 我們的切入點。
- 作者的習慣：**先開 issue 談，再收 PR**（README 也這樣寫；PR #442 明確說「please open an issue」）。
- 社群翻譯 PR 有被關閉的先例（PR #97），但社群 PR 被合併的先例也有（#223/#216/#168/#167）。

---

## 📚 相關文件

| 檔案 | 內容 |
|---|---|
| `docs/worksheet-dictatekeyboard-zhtw-ui-20261120.md` | **主工作表** —— 調查結果 + 計畫 + 風險 |
| `docs/opentypeless-and-dictatekeyboard-stt-tuning-20261117.md` | 繁中 STT/潤色調校實戰（Mac OpenTypeless + 本 fork 雲端編譯） |
| `docs/zh-TW-setup.md` | 繁中 App 設定指南（已存在於 fork，供使用者複製貼上） |
| `CLAUDE.md` | 同一份規則的 Claude Code 版本（內容同步） |
