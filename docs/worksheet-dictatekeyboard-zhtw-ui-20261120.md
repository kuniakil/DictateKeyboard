# 專案工作表：DictateKeyboard 繁體中文（zh-TW）UI 在地化

- **建立時間**：2026-11-20 (Taipei Time)
- **本工作表所在 repo**：`~/DictateKeyboard`（= 我們的 fork `kuniakil/DictateKeyboard`）
- **上游專案**：`DevEmperor/DictateKeyboard`（Android 語音輸入法，Kotlin/Compose，Apache-2.0）
- **我們的 Fork**：`kuniakil/DictateKeyboard`（已完成雲端編譯、固定簽章、Release `v6.4.0-apk`）
- **相關既有文件**：`docs/opentypeless-and-dictatekeyboard-stt-tuning-20261117.md`（繁中 STT/潤色調校實戰）
- **目標**：讓繁體中文（台灣）使用者拿到正統的繁中介面，**並藉此探測上游作者對社群貢獻的態度**

---

## Part 0 — 交接說明（新 session 從這裡開始）

### 當前狀態（2026-11-20 結束時）

| 項目 | 狀態 |
|---|---|
| 本機 repo | ✅ `~/DictateKeyboard`（origin = 我們的 fork，upstream = 上游） |
| 當前分支 | `feat/zh-tw-ui`（工作區乾淨，已與 `origin/feat/zh-tw-ui` 同步） |
| `main` | ✅ 已 merge `upstream/main`（diff vs 上游只剩 2 個純新增檔案） |
| Phase A | ✅ A0/A1/A2 完成；⬜ A3（給作者的說明文件）、A4（Actions 實跑驗證）未做 |
| Phase B–F | ⬜ 全部未開始 |
| 工作區 | 乾淨，無未提交改動 |

### 下一步（建議順序）

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

#### 簽名一致的機制（為什麼每次 build 出來的 APK 都能覆蓋升級）

```
1. build-apk.yml「Restore fixed debug keystore」步驟
     printf "%s" "$KEYSTORE_B64" | base64 -d > ~/.android/debug.keystore
     （每次 CI 都從 secret 還原同一把金鑰到同一個路徑）
2. app/build.gradle.kts 的 debug buildType **沒有指定 signingConfig**
     → Gradle 自動採用預設的 ~/.android/debug.keystore
3. 結果：每次 Actions build 產出的 debug APK 簽名完全一致
   → 手機上可直接覆蓋安裝，App 設定（API Key、Custom words、學詞庫…）全部保留
```

> 註：`keystore.properties.template` 是**上游給 Play 發行用的 upload key** 模板，與我們這把 debug 金鑰是**兩把不同的鑰匙**，別搞混。上游的 upload key 不在我們手上，也不該有。

#### ⚠️ 風險：金鑰是單點故障，且零備份

**GitHub Secret 是不可逆的（write-only）** —— 實測 `GET /actions/secrets/{name}/value` 回 **404 Not Found**（該端點對一般 token 不開放讀取）。

且已查證：
- 本機**沒有**任何副本（`find ~ -maxdepth 6 -name "*.keystore" -o -name "*.jks"` → 只找到 OneDrive 的無關檔案）
- Nextcloud `文件/` **沒有**任何簽章檔
- `~/.android/` **不存在**

**若金鑰遺失**（GitHub 帳號被鎖 / secret 被誤刪 / 無法登入）：
→ 只能重新產生一把新金鑰 → 簽名不一致 → **手機上必須 uninstall 重裝** → **App 內所有設定與自訂詞庫全毀**
→ 且既有 `v6.4.0-apk` Release 資產的簽章將無法再生產。

#### 使用者決策（2026-11-20）

**暫緩建立備份，先做 zh-TW 主線。** 之後若要補，指定存放位置為：**只放本機（不離開這台 Mac）**。

補備份的做法（需另開 workflow 事後刪除）：
1. 臨時加一支 workflow：還原金鑰 → 加密（用一個只有我們知道的 passphrase）→ 上傳成 Release asset 或 `workflow_dispatch` artifact
2. 本機下載後解密存到 `~/DictateKeyboard-secrets/`
3. 刪除該臨時 workflow

> **待辦提醒**：這是本專案唯一「遺失即永久損失」的資產。zh-TW 完成後應優先回頭處理。

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

#### 最終架構

```
upstream/main ──┬──► feat/zh-tw-ui   開發中（基底 = upstream/main + 我們的 CI + 工作表 + [未來: zh-TW 改動]）
                 │
                 ├──► main            我們的發行分支（= upstream/main + 我們的 CI + docs）→ Actions 在此出 APK
                 │
                 └──► pr/zh-tw-ui      提 PR 用（Phase E1 建立，只含在地化改動）
```

**日常運作**
1. 在 `feat/zh-tw-ui` 開發 → 定期 `git merge upstream/main`（解衝突）
2. 要出 APK → 在 `feat/zh-tw-ui` 觸發 Actions（tag 帶分支名，不會蓋掉 main 的資產）
3. 要提 PR → 從 `upstream/main` 切 `pr/zh-tw-ui`，只 checkout 在地化改動 → 對上游開 PR
4. 作者合併 → 我們 `git merge upstream/main` 回來 → 維護負擔從「維護 2547 條翻譯」降級為「例行 merge」

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

### 2.1 分支策略（D2 的落實）

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
- [ ] **A3** 建 `docs/zh-TW-ui-contribution.md`（給作者看的說明；未來 PR 會帶上去）
- [ ] **A4** 確認 Actions 可出 APK：`gh workflow run build-apk.yml --ref feat/zh-tw-ui`
      ✅ 2026-11-20 修正：tag 撞名已修（`7843e539`）。在 `feat/zh-tw-ui` 跑會發到
      `v6.4.0-apk-feat-zh-tw-ui`，**不會**動 `v6.4.0-apk`（舊版，仍指向 `e4c41fe`）。
      只有在 `main` 上跑才會 `--clobber` 掉 `v6.4.0-apk`。無需特別備份。
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

- [ ] **B0** 最小可行驗證（先於 B1–B6；目的：證明 `values-zh-rTW` 命名與 fallback 可用）
  - 建 `app/src/main/res/values-zh-rTW/strings.xml`，只含約 40 條：`pref__other__settings_language__label`、設定首頁標題、Dictate 主要頁面標題、含 `%1$s` / `{app_name}` 的字串、1 個 plural
  - 保留 `comment` 屬性與 placeholder；其餘未翻條目**刻意不放**（用來驗證退回英文）
  - 驗收：`xmllint --noout` 通過
- [ ] **B0b** 建驗證腳本 `tools/check-l10n.py`：比對 key 集合、placeholder、`comment` 保留數、plurals（B5 的前置；基準數字以其輸出為準）
- [ ] **B1** 建立台灣用語 glossary（英文 → 台灣繁中），以 1.3 對照表為底
- [ ] **B2** 批次翻譯 `values/strings.xml` → `values-zh-rTW/strings.xml`
  - 執行方式：由 agent 分批直接翻（每批約 100–200 條），每批過 `tools/check-l10n.py`，不使用外部翻譯 API
  - 輸入：英文原文 + `comment="..."` 翻譯指引（1614 條）
  - **必須保留**：`comment` 屬性、placeholder（`{app_name}` / `%1$s` / `{count}`）、XML 轉義
  - 輸出結構與 base 完全對齊（2547 strings + 11 plurals）
- [ ] **B3** 翻譯 `wear/src/main/res/values/strings.xml` → `values-zh-rTW/strings.xml`（base 69 條）
- [ ] **B4** `strings_dont_translate.xml`（32 條）**不翻**
- [ ] **B5** 驗證：
  - [ ] key 集合與 base 完全一致（2547 + 11 plurals）
  - [ ] placeholder 逐條比對，mismatch = 0（基準：base vs zh-rCN 實測為 0）
  - [ ] `comment` 屬性保留數 = base 的 1614
  - [ ] XML 合法（`xmllint`）
  - [ ] lint 無 `MissingTranslation`
- [ ] **B6** 台灣用語複查（掃描殘留大陸用語，歸零）

### 2.4 Phase C — 讓繁中介面真的出現（D4 的關鍵：證明可用）

> 這是整個計畫的**樞紐**。沒有這一步，後面的 issue 與 PR 都只是「我打算做」。

- [ ] **C1** 在 `OtherScreen.kt` 的語言 tag 清單加入 `"zh-TW"`（清單目前 40 個 tag，`zh-CN` 在最後）
  - `FlorisLocale.fromTag("zh-TW")` 會解析成 `Locale("zh","TW")` ✅
  - 顯示名稱由 `locale.displayName()` 產生，無需自訂
  - `FlorisAppActivity.kt:101-105` 已監聽 `prefs.other.settingsLanguage` 並即時 `createConfigurationContext` → **不需重啟 App 即生效**
- [ ] **C2** 走 Actions 出 APK（本機未確認有 Android SDK，不採本機建置）
  - 我們的 `build-apk.yml` 是 `workflow_dispatch` 手動觸發 ✅
  - 分支建置發到 `v6.4.0-apk-<分支名>`，不會覆蓋 `v6.4.0-apk`（已修正，見 A4）
- [ ] **C3** 裝機實測（證據鏈起點）
  - [ ] App → 設定 → 其他 → 語言 → 選「繁體中文」→ 確認 UI 立即切換
  - [ ] 走查：設定首頁 / Dictate / providers / prompts / backup / learned words / wear 設定
  - [ ] 確認無殘留英文、placeholder 顯示正常（`%1$s` 插值）、無崩潰
  - [ ] **B0 階段驗收**：選繁中後，已翻條目顯示繁中、未翻條目退回英文、無崩潰；順便記錄 picker 顯示名稱（如「Chinese (Taiwan)」或「中文（台灣）」）
- [ ] **C4** **產出證據（截圖集）**
  - 語言選擇器（含 "繁體中文（台灣）" 選項）
  - 設定首頁（繁中）
  - Dictate 設定頁（繁中）
  - providers / prompts 頁（繁中）
  - learned words 頁（繁中）
  - **對照組**：同一頁的英文版與簡中版（用 `zh-CN` 切一次）→ 三語並列最有說服力

> 💡 證據的呈現方式：issue 用截圖，PR 用截圖 + 說明。**重點是讓作者一眼看出「這是台灣使用者實際看到的畫面」，而不是抽象的翻譯檔案。**

### 2.5 Phase D — 台灣用語校訂

- [ ] **D1** 依 1.3 對照表 + glossary 逐條套用
- [ ] **D2** 重新掃描殘留大陸用語，確認歸零
- [ ] **D3** 依 `comment="..."` 的語氣要求複查（1614 條中與 Dictate 功能相關者優先）

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

- [ ] **E1a** 從 `upstream/main` 拉出 `pr/zh-tw-ui`
- [ ] **E1b** 只帶入在地化改動（排除我們的 CI commit）：
      `app/src/main/res/values-zh-rTW/`、`wear/src/main/res/values-zh-rTW/`、`OtherScreen.kt`（1 行）、`docs/zh-TW-ui-contribution.md`
- [ ] **E1c** 驗證 diff 乾淨：`git diff upstream/main --stat` 應只有上述 4 項
- [ ] **E1d** rebase 到最新 `upstream/main`（消除 C 階段期間上游的新 commit）
- [ ] **E1e** 推上去：`git push origin pr/zh-tw-ui`（推到**我們的 fork**）
- [ ] **E1f** 開 PR：compare `DevEmperor:main` ← `kuniakil:pr/zh-tw-ui`

#### E2 — 先在 issue #483 留言建立連結

- [ ] **E2a** 在 **#483「Dictation in traditional chinese」**（2026-11-15 開，0 回覆，作者 `crazywing`）留言
  - 給出繁中 STT 的實際解法：`Punctuation & style → Custom style prompt` 填繁中引導句 + `Rewording → Manage prompts` 開 `Apply automatically`
  - 這正是 `docs/zh-TW-setup.md` 驗證過的組合 → **展示我們真的在用這個 App**
  - 附帶說明我們已完成 zh-TW UI 介面、正在準備貢獻
- [ ] **E2b** **新開 issue**「Traditional Chinese (zh-TW) UI translation」，內容：
  1. 台灣用戶目前拿到**英文**（附資源解析規則與 `createConfigurationContext` 機制）
  2. 我們已做好的 zh-TW 介面 + **實機截圖證據**
  3. 我們的維護方案（見 2.7）
- [ ] **E2c** 等待作者回應（作者活躍，issue 與 PR 都有回覆；他的習慣是先談再收）

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
- [ ] **F2**（原 P2）倉頡字根顯示 → **先開 issue 討論再寫碼**。需自建 `characters/cangjie.json`（label=字根、code=字母）+ 接進 `extension.json` + 確認 Kotlin 版 layout loader 行為。上游本來就沒倉頡 layout，屬「上游可能不收」類型。
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

---

## Part 4 — 已定案事項（2026-11-20）

| # | 事項 | 決策 |
|---|---|---|
| Q1 | 翻譯基底 | ✅ **由英文 base 翻**（理由見 2.3：與上游 AI 批次流程同源，相容性高） |
| Q2 | 分支 | ✅ **開分支，專供未來提 PR**；採單分支 + 提 PR 前剝離（2.1） |
| Q3 | 執行順序 | ✅ **自己先做 → 證明可用 → 提 issue → 提 PR 附證據**（D4） |
| Q4 | wear（69 條） | ✅ 一併做（B3），但排在主 App 之後 |
| Q5 | TODO.md 的 P1 條目 | ⬜ 待更新（原文「零衝突不改 Kotlin 碼」需更正為「需動 `OtherScreen.kt` 一行」） |

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

---

*本文件由 Claude Code 撰寫，數據皆為 2026-11-20 實查。Part 2 於同日依使用者決策（D1–D4）修訂。*
