# CLAUDE.md — DictateKeyboard 繁體中文（zh-TW）在地化

本 repo 是 `DevEmperor/DictateKeyboard` 的 fork。**目前唯一的進行中工作：新增繁體中文（台灣）介面。**

## 立刻先讀

**`docs/worksheet-dictatekeyboard-zhtw-ui-20261120.md`** —— 完整工作表。內含：

- Part 1 調查結果（三個決定性發現、工程事實、台灣用語表、2026-11-17 操盤歷史查證）
- Part 2 計畫（Phase A–F，每項都是可勾選的 checkbox）
- Part 3 風險、Part 4 已定案事項、Part 5 可重跑的驗證指令

**不要重做調查** —— 關鍵事實都已在工作表內驗證過（上游 locale 結構、app 語言選擇器位置、2547 條資源數量、fork 分歧狀態…）。

## Repo 拓撲

| remote | 指向 | 用途 |
|---|---|---|
| `origin` | `kuniakil/DictateKeyboard`（我們的 fork） | 推送分支、開 PR 的來源 |
| `upstream` | `DevEmperor/DictateKeyboard`（上游） | 追蹤上游更新、PR 的目標 |

分支：
- `main` = 我們的**發行分支** = `upstream/main` + 我們的 CI workflow + docs。**已 merge 上游 2026-11-18**（diff vs 上游只剩 2 個純新增檔案）。Actions 在此出正式 APK。
- `feat/zh-tw-ui` = **當前工作分支**，基底 `upstream/main` + 我們的 CI workflow + 工作表。← 現在在這裡
- `pr/zh-tw-ui` = 提 PR 用的乾淨分支（Phase E1 才建立），由 `upstream/main` 拉出後只帶在地化改動。

⚠️ **不要拿 `main` 或 `feat/zh-tw-ui` 直接開 PR** —— 兩者都含 `build-apk.yml`（作者已明確拒絕過，見 PR #286）。
提 PR 必須走 `pr/zh-tw-ui` 剝離流程。

## 硬規則

1. **改任何檔案前先更新工作表的 checkbox** —— 這是進度唯一的權威來源。
2. **翻譯基底是英文**（`values/strings.xml`），不是 `values-zh-rCN`。用 `values-zh-rCN` 再轉會變「二手 AI 轉譯」，與上游未來自做的 zh-TW 打架。
3. **必須保留** `comment="..."` 翻譯指引屬性（base 有 1614 條）與所有 placeholder（`{app_name}` / `%1$s` / `{count}`）。
4. **必改 Kotlin 一行**：`OtherScreen.kt` 的語言 tag 清單加 `"zh-TW"`（上游有 App 語言選擇器，40 個 tag + `auto`）。工作表裡原寫「不改 Kotlin 碼」是錯的，已更正。
5. **不要碰 `values/strings_dont_translate.xml`**（32 條）。
6. **不要用 `kubectl apply` / `helm` 之類** —— 本 repo 與叢集無關。

## 驗證（不可腦補）

```bash
# 資源 key 集合與 placeholder 必須與 base 完全對齊
python3 tools/check_zh_tw.py    # 待建立（Phase B5）

# lint
./gradlew :app:lintDebug        # 需本機 JDK 21 + Android SDK

# 雲端編譯（Actions）
gh workflow run build-apk.yml --ref feat/zh-tw-ui
```

⚠️ `build-apk.yml` 會 `gh release upload --clobber` 到 `v6.4.0-apk` → **覆蓋既有 Release 資產**。
手機上裝的就是那個（Nextcloud `文件/app-debug.apk`）。動手前先備份 asset。

## 🔑 簽章金鑰（單點故障，零備份）

金鑰**不在 repo 裡、不會被 clone 回來**，只存在於 GitHub Secret `ANDROID_DEBUG_KEYSTORE_B64`。
GitHub Secret 不可逆讀取（API 回 404），且**本機與 Nextcloud 都沒有任何副本**。

遺失的後果：無法再生產相同簽章 → 手機上必須 uninstall 重裝 → **App 設定與自訂詞庫全毀**。

使用者的指示：**暫緩補備份，先做 zh-TW；之後要補時只放本機**（`~/DictateKeyboard-secrets/`）。
→ 詳見工作表 1.5 節（含補備份的做法）。

## 與上游互動的關鍵背景

- 上游翻譯由**作者自己用 AI 批次生成**，每個功能 commit 同步更新全部 20 個 locale（同一 SHA）。
  → 靜態 zh-TW 檔案必然漂移 → **交付物要含「glossary + 後處理轉換器」**，而非只有檔案。
- 上游 open issue **#483「Dictation in traditional chinese」**（0 回覆）= 我們的切入點。
- 作者的習慣：**先開 issue 談，再收 PR**。README 也這樣寫。
- 社群翻譯 PR 有被關閉的先例（PR #97），但社群 PR 被合併的先例也有（#223/#216/#168/#167）。

## 相關文件

- `docs/worksheet-dictatekeyboard-zhtw-ui-20261120.md` — 主工作表
- `docs/opentypeless-and-dictatekeyboard-stt-tuning-20261117.md` — 繁中 STT/潤色調校（Mac OpenTypeless + 本 fork 雲端編譯實戰）
- `docs/zh-TW-setup.md` — 繁中 App 設定指南（已存在於 fork）
