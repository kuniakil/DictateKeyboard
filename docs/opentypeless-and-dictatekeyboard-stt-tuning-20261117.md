---
title: "Mac OpenTypeless 辨識調校與 Android DictateKeyboard 雲端編譯實戰"
categories: [Tools, AI, Android]
tags: [opentypeless, dictatekeyboard, stt, groq, gemini, whisper, github-actions, android]
---

# Mac OpenTypeless 辨識調校與 Android DictateKeyboard 雲端編譯實戰

## 1. 背景與問題分析

在 Mac 上使用開源語音輸入法 **OpenTypeless (`v1.1.61`)**（倉庫：`tover0314-w/opentypeless`）時，相較付費版 Typeless，在中英夾雜技術詞彙與繁體中文準確度上仍有落差；同時需要一套在 Android 上也能使用相同 BYOK（自帶 API Key）架構的語音輸入法。

### 1.1 OpenTypeless 誤判來源診斷（STT vs 潤色引擎）

檢視本機設定與 SQLite 資料庫：
- 設定檔：`~/Library/Application Support/com.opentypeless.app/settings.json`
- 資料庫：`~/Library/Application Support/com.opentypeless.app/opentypeless.db`（`history` 表同時保存 `raw_text` 與 `polished_text`，共 1,041 筆）

比對結果顯示**主因在 STT 引擎（`groq-whisper` / `whisper-large-v3-turbo`）**：
1. **中英夾雜專有名詞音近誤判**：
   - `OpenClaw` → `OpenCloud`（51 次）、`OpenCrow`（10 次）、`OpenCraw`、`OpenCrawl`、`OpenCrofty`、`OpenCrawty`
   - `Hermes` → `Hermus`、`Hermis`、`Hermits`
   - `Technitium` → `Technician`、`Technitian`
   - `Docker` → `Darker`、`Dify` → `DIFI`、`Nextcloud` → `Nestcloud`、`PR` → `披押`、`著作權` → `著作前`
2. **大量簡體字與靜音幻覺**：近期 300 筆 `raw_text` 中有 230 筆含簡體字，且句尾偶爾出現 `谢谢` 幻覺。
3. **潤色端未補救的原因**：`dictionary` 與 `correction_rules` 皆為 **0 筆**，且 `llm_model` 使用極輕量的 `gemini-3.5-flash-lite`，無法從語境還原冷門專有名詞與部分同音字（例如 `監權` 被誤改為 `專利權`）。

> 註：透過檢查執行檔（`OpenTypeless.app/Contents/MacOS/opentypeless`），確認 v1.1.61 **不支援**「監聽貼上後手動修改並自動加入規則」的功能，且 `correction_rules` 啟用上限為 **100 條**。

---

## 2. Mac 版 OpenTypeless 修正方案

執行前已先退出 OpenTypeless，並將原始檔案備份至：
`~/Library/Application Support/com.opentypeless.app/backups/`（附 `README.md` 記錄還原與清理指令）。

### 2.1 資料庫調校（`opentypeless.db`）
- **`dictionary`（新增 31 筆高頻詞）**：`OpenClaw`, `Hermes`, `Dify`, `Antigravity`, `OpenTypeless`, `Gemini`, `n8n`, `K3s`, `K9s`, `Docker`, `Technitium`, `Nextcloud`, `Cloudflare`, `Traefik`, `Authentik`, `Immich`, `Instabox`, `Camofox`, `Oracle`, `N100`, `GitHub`, `PR`, `CLI`, `API`, `DNS`, `IPv4`, `IPv6`, `Clash Verge`, `WARP`, `WordPress`, `Telegram`。
- **`correction_rules`（新增 16 條啟用規則）**：
  - `OpenCloud` / `OpenCrow` / `OpenCraw` / `OpenCrawl` / `OpenCrofty` / `OpenCrawty` → `OpenClaw`
  - `Hermus` / `Hermis` / `Hermits` → `Hermes`
  - `Technician` / `Technitian` → `Technitium`
  - `Nestcloud` → `Nextcloud`、`Darker` → `Docker`、`DIFI` → `Dify`、`披押` → `PR`、`著作前` → `著作權`

### 2.2 設定調整（`settings.json`）
- **`llm_model`**：由 `gemini-3.5-flash-lite` 升級為 **`gemini-2.5-flash`**（兼顧速度與上下文糾錯力）。
- **`polish_custom_prompt`**：加入領域語境提示（Kubernetes `K3s`、Docker、GitHub PR、DNS/網路及 AI Agent `OpenClaw`、`Hermes`、`Dify`），要求依語境修錯字並一律輸出繁體中文。

---

## 3. STT 引擎與夜間延遲評估

- **夜間變慢原因**：台灣晚上 20:00–01:00 剛好撞上歐美工作尖峰（Groq 免費層排隊）、Gemini API 尖峰及台灣聯外海纜壅塞。可觀察 OpenTypeless 膠囊卡在 `Transcribing`（Groq）或 `Polishing`（Gemini）來定位瓶頸。
- **MediaTek `Breeze-ASR-25`**：官方僅 Apache 2.0 開源權重，無免費託管 API；且不建議將 Mac 輸入法接到 Instabox（有 30 分鐘休眠冷啟動問題），若要使用較適合在 Apple Silicon 本機跑。
- **Deepgram Nova-3**：新帳號贈送 $200 免費額度、支援 `zh-TW` 且夜間商用線路較穩，OpenTypeless 1.1.61 已原生支援，可隨時作為 Groq 替代測試。
- **付費版 Typeless 參考**：官方 Trust Center 列出的 AI 子處理商包含 Fireworks AI、Google Gemini、Microsoft Foundry 與 xAI。

---

## 4. Android 版解決方案：DictateKeyboard 雲端編譯

`tover0314-w/opentypeless` 目前無 Android APK 分支。Android 原生替代方案選用 **`DevEmperor/DictateKeyboard`**（基於 FlorisBoard，具備地球切換鍵、系統語音服務 `Dictate Voice Input` 與懸浮語音球）。

由於作者僅提供 Google Play 付費上架版本、GitHub Releases 未附預編譯 APK，且專案 `gradle.properties` 設定 `org.gradle.jvmargs=-Xmx6144m` 並需編譯 C++ 原生庫，不適合在 8 GB RAM 的 M1 Mac 本機編譯，因此改用 Fork + GitHub Actions 雲端打包：
- Fork 倉庫：`https://github.com/kuniakil/DictateKeyboard`
- Workflow：`.github/workflows/build-apk.yml`

### 4.1 編譯踩坑與修復紀錄
1. **`android-actions/setup-android@v3` 失敗（`Warning: Failed to find package 'tools'`）**：
   - 原因：`ubuntu-latest` 已預裝 Android SDK，舊版 action 嘗試安裝已被移除的 `tools` 套件。
   - 解法：移除該 action，改用預裝的 `sdkmanager --licenses` 接受授權。
2. **缺少 C++ 原生庫（`Missing libdictate_bergamot.so for arm64-v8a`）**：
   - 原因：專案在 `preBuild` 會檢查 `sherpa-onnx` 與 Mozilla Bergamot 離線翻譯引擎原生庫。
   - 解法：依 `gradle/tools.versions.toml` 安裝指定版本 `ndk;29.0.14206865` 與 `cmake;4.1.2`，並依序執行 `bash tools/fetch-sherpa-onnx.sh` 與 `bash tools/bergamot/build-android.sh`。
3. **固定簽章金鑰（實現覆蓋升級、保留手機設定）**：
   - 問題：每次 CI 產生的隨機 `~/.android/debug.keystore` 不同，更新 APK 會因簽章不一致被迫解除安裝。
   - 解法：用 OpenSSL 產生固定 2048-bit PKCS12 `debug.keystore`，Base64 編碼後存入 Repo Secret **`ANDROID_DEBUG_KEYSTORE_B64`**，每次 CI 編譯前還原至 `~/.android/debug.keystore`（首次從舊隨機簽章切換時需手動 Backup → 重裝 → Restore 一次，之後皆可直接覆蓋升級）。
4. **自動發佈至 GitHub Releases**：
   - Workflow 加入 `permissions: contents: write`，編譯完成後自動讀取 `gradle.properties` 版本號，將 APK 上傳至對應的 `v<version>-apk` Release Assets（已成功產出 `v6.4.0-apk` / `app-debug.apk`，約 166.25 MB），手機可直接從 Releases 頁面下載。

### 4.2 Android 端繁體中文設定要點與實測排錯
- **引擎分工**：Transcription 使用 **Groq**，Rewording 使用 **Gemini 3.8 Flash**（避開 Gemini Transcribe 走 Live WebSocket 易在行動網路/代理環境卡死的問題）。
- **關鍵開關**：僅填 `Rewording instruction` 不會自動執行潤色；必須進 **`Rewording (AI) → Manage prompts`** 新增繁中潤色 Prompt 並開啟 **`Apply automatically`**，才會每次講完自動轉繁體並修正專有名詞。
- **`Punctuation & style` 的決定性影響**：實測發現若只設定 Rewording 而未在 **`Punctuation & style` → `Custom style prompt`** 填入繁體中文引導句，Groq Whisper 原文仍會夾雜大量簡體字；補上繁中引導句後，輸出即穩定為繁體中文。
- **Backup / Restore 憑證剔除注意**：從 `BackupRedaction.kt` 可確認，若匯出備份時選擇不包含憑證（`without provider credentials`），還原後 `dictate__provider_accounts` 內的 API Key 會被清空，需重新確認 Gemini/Groq Key 與 Rewording Provider 設定。
- **詞庫與提示**：將技術詞庫填入 **`Custom words`**、錯字對照填入 **`Mappings`**。
- **Subtype 說明**：FlorisBoard 的 `Subtype` 僅為手動打字鍵盤佈局設定，不影響語音辨識語言。

### 4.3 設定指南文件化（Fork 倉庫留存）
已將完整可複製的繁體中文設定參數（`Punctuation & style`、`Custom words`、16 條 `Mappings`、`Rewording` 提示詞與升級流程，不含任何 API Key）整理並提交至 Fork 倉庫：
- `https://github.com/kuniakil/DictateKeyboard/blob/main/docs/zh-TW-setup.md`（Commit `a02b59c1`，獨立新檔不會影響未來 `Sync fork`）
