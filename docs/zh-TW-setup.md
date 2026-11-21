# DictateKeyboard 繁體中文（台灣）＋技術詞彙設定指南

本文件整理自實測調校結果，方便日後重裝或換機時直接複製貼上（不含任何 API Key）。

---

## 1. 引擎分工（Providers）

- **Transcription（語音轉文字）**：`Groq`（速度快、免費額度高）
- **Rewording（AI 潤色）**：`Google Gemini`（推薦 `Gemini 3.8 Flash` 或 `Gemini 2.5 Flash`）
  > ⚠️ 不建議將 Transcription 設為 Gemini（會走 Live WebSocket，在行動網路或代理環境容易卡住）。

---

## 2. Punctuation & style（給 STT 的風格提示）

在 **Dictate 設定 → Formatting / Punctuation & style → Custom style prompt** 貼入以下繁體中文引導句（可大幅減少 Groq Whisper 輸出簡體字）：

```text
以下是繁體中文的技術對話與筆記，請一律使用繁體中文與全形標點符號輸出，專有名詞維持英文原拼寫（例如 OpenClaw、Hermes、Dify、K3s、Docker、GitHub PR）。
```

---

## 3. Custom words（個人詞庫）

在 **Dictate 設定 → Custom words** 直接貼入（逗號分隔）：

```text
OpenClaw, Hermes, Dify, Antigravity, OpenTypeless, Gemini, n8n, K3s, K9s, Docker, Technitium, Nextcloud, Cloudflare, Traefik, Authentik, Immich, Instabox, Camofox, Oracle, N100, GitHub, PR, CLI, API, DNS, IPv4, IPv6, Clash Verge, WARP, WordPress, Telegram
```

---

## 4. Mappings（固定錯字離線替換）

在 **Dictate 設定 → Mappings** 新增以下精準替換規則（離線、零延遲）：

| 聽錯詞（Pattern） | 替換為（Replacement） |
| :--- | :--- |
| `OpenCloud` | `OpenClaw` |
| `OpenCrow` | `OpenClaw` |
| `OpenCraw` | `OpenClaw` |
| `OpenCrawl` | `OpenClaw` |
| `OpenCrofty` | `OpenClaw` |
| `OpenCrawty` | `OpenClaw` |
| `Hermus` | `Hermes` |
| `Hermis` | `Hermes` |
| `Hermits` | `Hermes` |
| `Technician` | `Technitium` |
| `Technitian` | `Technitium` |
| `Nestcloud` | `Nextcloud` |
| `Darker` | `Docker` |
| `DIFI` | `Dify` |
| `披押` | `PR` |
| `著作前` | `著作權` |

---

## 5. Rewording (AI) 自動潤色設定

1. 確認 **`Enable rewording`** 開關為 **開啟**。
2. **`Rewording instruction`（全域系統指令）** 貼入：

```text
請一律使用繁體中文（台灣用語）輸出，不要使用簡體中文字。內容常涉及 Kubernetes (K3s)、Docker、GitHub PR、DNS/網路及 AI Agent (OpenClaw、Hermes、Dify) 等技術詞彙，請依語境自動修正同音或音近錯字。
```

3. 進入 **`Manage prompts` → 新增 Prompt**（例如命名為 `繁中潤色`）：
   - Prompt 內容可貼入上方相同指令（或精簡為「轉為繁體中文（台灣用語），修正標點與同音技術錯字，保留英文專有名詞原拼寫」）。
   - **關鍵**：務必開啟該 Prompt 內的 **`Apply automatically`**（每次講完自動執行潤色）。

---

## 6. 升級與備份說明

- **下載新版 APK**：直接到本倉庫的 [Releases](https://github.com/kuniakil/DictateKeyboard/releases) 下載 `app-debug.apk`（已使用固定簽章金鑰打包，日後可直接覆蓋升級保留設定）。
- **上游同步**：在 GitHub 點右上角 `Sync fork` → `Update branch`，再到 Actions 執行 `Build Android APK` 即可。
- **備份提醒**：App 內的 Backup 若未勾選包含憑證，還原後需重新填入 Groq 與 Gemini API Key。

---

## 7. 本地（離線）轉錄的限制

若把 Transcription 改成**本地模型**（例如 SenseVoice Small）：

- **風格提示對本地模型無效** —— `Custom style prompt` 是送給雲端 STT 的 `prompt` 欄位（Whisper 家族的「前文偏置」）；本地引擎（sherpa-onnx 的離線 SenseVoice / Whisper）**沒有**這個輸入欄位，app 也不會把提示詞交給它。
- **本地輸出必然是簡體** —— SenseVoice 的中文權重就是簡體，且 app 目前**沒有**簡→繁轉換功能。
- **但改寫層照樣有效** —— 步驟 5 的「自動套用」提示是跑在**轉錄完成之後**的，與轉錄服務商無關（本地／雲端一視同仁），所以「本地轉錄 ＋ Gemini 潤色」一樣會輸出繁體中文。
- **純離線（連改寫都不用雲端）**：只能用第 4 步的 Mappings 做簡→繁逐詞替換（離線、精準、零 token），但覆蓋率有限，一對多的字（如 髮/發、乾/幹）仍會錯。

> 延伸閱讀：本 repo 的 `docs/worksheet-dictatekeyboard-zhtw-ui-20261120.md` §1.7 記錄了完整的實查證據（app 層／引擎層／模型層），Phase F 的 **F5** 則是「加一個轉繁體開關」的待辦。
