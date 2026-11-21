---
title: "DictateKeyboard 自行 fork 發布的 Apache-2.0 合規補強"
categories: [Android, 開源授權]
tags: [dictatekeyboard, apache-2.0, fork, github-actions, release, 踩坑紀錄]
---

# DictateKeyboard 自行 fork 發布的 Apache-2.0 合規補強

## 1. 任務背景與目標
- 上游作者尚未回覆繁中 UI（#483 / #492）。使用者考慮自己 fork 並免費發布 APK 給繁中使用者，想確認是否違反授權。
- 結論：上游與 FlorisBoard 皆為 Apache-2.0，允許修改與再散布（含商用），不需作者同意。上游 issue #420 也有作者吸收 fork（Dictate-Extended）成果的先例。
- Apache-2.0 §4 的義務有兩個缺口：(b) 未標示修改內容、(d) NOTICE 未隨 Release 散布。另外要明示「非官方」（§6 不授予商標權）。

## 2. 實施步驟與關鍵變更
- 新增 `README-fork.md`：非官方聲明、免費不販售、署名、與上游關係。
- 新增 `docs/fork/MODIFICATIONS.md`：逐檔改動清單。
- `README.md` 開頭加非官方 fork 的 NOTE，並保留上游的 Play、sponsor 連結。
- `.github/workflows/build-apk.yml`：每次 Release 自動附上 `NOTICE.txt` 與 `MODIFICATIONS.md`，release notes 帶 §4(b) 改動摘要與 §4(d) 署名說明。
- commit `838fb008` 已推到 `main`，只動 `main`，不碰 `pr/*`。
- 手動觸發 Actions（run 44856724389）後成功，`v6.4.0-apk` 已有 `app-debug.apk`、`NOTICE.txt`、`MODIFICATIONS.md` 與新 notes。

## 3. 踩坑記錄與解決方案 (Gotchas & Fixes)
- 前一個 agent 在 5 小時 token 上限時中斷，檔案已寫好但未 commit。`build-apk.yml` 最後一次編輯留有瑕疵：重複的 `gh release create ... \` 行和舊的 `--notes`。檢查時發現檔案內容已乾淨，並以 PyYAML 驗證語法。
- 重建置的原因：workflow 只在發布時才附檔和改 notes，所以舊 Release 要補合規資訊就得跑一次 workflow，也順便驗證 workflow 沒壞。不重編的替代做法是手動 `gh release upload` 與 `gh release edit`。
- applicationId 帶 `.debug` 後綴（`net.devemperor.dictate.debug`），可與 Play 付費版並存。不要改成無後綴的 release build，否則會與 Play 版撞 package 且簽章不同。
- 模型權重不由本 fork 散布（下載來源仍指向上游 release），所以各模型授權義務不落在我們身上。

## 4. 驗證結果與後續 TODO
- Actions 成功，Release 資產與 notes 均確認。
- 可選：刪除 Release 內舊資產 `app-debug-cangjie-20261120.apk`（不影響授權）。
- 作者若回覆，依工作表 Part 0 的情境表處理；本地 STT 繁中輸出仍為 Phase F / F5 TODO。
