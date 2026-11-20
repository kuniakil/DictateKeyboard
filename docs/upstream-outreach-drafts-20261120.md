# Upstream Outreach Drafts (Fork Working Doc — Do NOT Include in PR)

> **Status (2026-11-20)**:
> - **Draft 1 (#483 comment)** → ✅ Posted: https://github.com/DevEmperor/DictateKeyboard/issues/483#issuecomment-7030540460
> - **Draft 2 (New Issue #492)** → ✅ Posted: https://github.com/DevEmperor/DictateKeyboard/issues/492 (screenshots hosted on orphan branch `kuniakil/DictateKeyboard@assets/zh-tw-screenshots`)
> - **Draft 3 (PR `kuniakil:pr/zh-tw-ui` → `DevEmperor:main`)** → ⏳ Ready to post after maintainer replies on `#492`.

---

## Draft 1 — Comment on Issue #483 (`Dictation in traditional chinese`)

**Target**: https://github.com/DevEmperor/DictateKeyboard/issues/483

```markdown
Hi @crazywing — I use Dictate daily for Traditional Chinese (zh-TW) dictation and got reliable output without Simplified Chinese characters using two built-in settings:

1. **Transcription style bias** (`Dictate → Formatting & vocabulary → Punctuation & style → Custom style prompt`):
   Add a Traditional Chinese instruction/example so Whisper/STT favors Traditional Chinese and full-width punctuation, for example:
   ```text
   以下是繁體中文的內容，請一律使用繁體中文與全形標點符號輸出，專有名詞維持英文原拼寫。
   ```
2. **Automatic Rewording safety net** (`Dictate → Rewording (AI) → Manage prompts`):
   Create a prompt instructing the model to output Traditional Chinese (Taiwan usage) and fix punctuation/homophones, and turn on **Apply automatically** so every dictation is cleanly converted.

*(Side note for @DevEmperor: I also noticed Taiwan users get English UI instead of Chinese because `values-zh-rTW` doesn't exist yet — I've put together a complete `zh-TW` UI localization with a Taiwan terminology glossary and will open a separate issue to share screenshots and details.)*
```

---

## Draft 2 — New Issue: `Traditional Chinese (zh-TW) UI translation`

**Target**: https://github.com/DevEmperor/DictateKeyboard/issues/new

**Title**:
```text
Traditional Chinese (zh-TW) UI translation
```

**Body** *(replace the `UPLOAD: <filename>` placeholders by dragging the matching `.jpg` files from Nextcloud `/mnt/kuniaki/文件/DictateKeyboard`)*:

```markdown
### Why Taiwan users currently see English UI

DictateKeyboard ships `values-zh-rCN/` and sets `projectMinSdk=26`. Because Android 7.0+ uses script-aware locale resolution, a device set to `zh-TW` resolves as `zh-Hant-TW`, which does **not** match `values-zh-rCN` (implicit `Hans`) and falls back directly to English `values/`.

This breaks down cleanly into two independent layers:

1. **Layer 1 — Resource directory (`values-zh-rTW`, no Kotlin changes):**
   Following the repo's `r<REGION>` naming (`zh-rCN`, `ko-rKR`, `pt-rBR`, `lv-rLV`), adding `values-zh-rTW/strings.xml` immediately gives Taiwan system-locale users Traditional Chinese UI (note that locales like `ast`, `sq`, `ur`, and `et` already ship as resources without being in the picker).
2. **Layer 2 — In-app language picker (1-line Kotlin change):**
   Adding `"zh-TW"` right after `"zh-CN"` in `OtherScreen.kt` lets users select `中文 (台灣)` in **Settings → Other → Settings language** regardless of system locale.

---

### What I've built & tested on a real device

I translated the full UI directly from the English base (`values/strings.xml`, not converted from `zh-rCN`) using Taiwan Traditional Chinese terminology:

- **100% key parity**: `app` (`2547` strings + `11` plurals) and `wear` (`69` strings), with `0` placeholder mismatches and all `1618` `comment="..."` translation hints preserved. *(Note: `wear` follows the watch's system locale rather than the phone in-app picker.)*
- **Clean branch preview**: https://github.com/kuniakil/DictateKeyboard/compare/DevEmperor:DictateKeyboard:main...kuniakil:DictateKeyboard:pr/zh-tw-ui

#### 3-Language Comparison (English vs. `zh-CN` vs. `zh-TW`)

| English (current fallback for `zh-TW` devices) | Simplified Chinese (`zh-CN`) | Traditional Chinese (`zh-TW`) |
| :---: | :---: | :---: |
| UPLOAD: Screenshot_2026-11-20-12-12-47-185_net.devemperor.dictate.debug.jpg | UPLOAD: Screenshot_2026-11-20-12-13-01-258_net.devemperor.dictate.debug.jpg | UPLOAD: Screenshot_2026-11-20-12-13-10-072_net.devemperor.dictate.debug.jpg |

#### Additional Screens (`zh-TW`)

| Language Picker (`中文 (台灣)`) | Dictate Settings | Learned Words (incl. latest strings) |
| :---: | :---: | :---: |
| UPLOAD: Screenshot_2026-11-20-12-07-51-076_net.devemperor.dictate.debug.jpg | UPLOAD: Screenshot_2026-11-20-12-09-10-648_net.devemperor.dictate.debug.jpg | UPLOAD: Screenshot_2026-11-20-12-12-02-360_net.devemperor.dictate.debug.jpg |

*(Optional extra screenshots available if helpful: Home `12-07-19`, Theme `12-08-41`, Clipboard `12-08-50`, AI Providers `12-09-42`, Groq dialog `12-09-52`, User Dictionary `12-11-55`.)*

---

### Avoiding Future Drift (Fitting Your AI Localization Workflow)

I noticed you keep all 20 active locales updated alongside feature commits via AI batch translation. To avoid handing you an unmaintainable static XML file, I also documented a concise **Taiwan glossary + prompt rule set** (`docs/zh-TW-ui-contribution.md`) so `zh-TW` can simply be added as one more target in your existing English-base batch workflow.

Would you like me to open a PR from `pr/zh-tw-ui`? (Happy to include `docs/zh-TW-ui-contribution.md`, move it, or drop it and submit only the resource files + 1-line picker change—whichever fits your repo best.)
```

---

## Draft 3 — Pull Request Description (Post ONLY After Issue Discussion)

**Compare**: `DevEmperor:main` ← `kuniakil:pr/zh-tw-ui`  
**Title**:
```text
l10n: add Traditional Chinese (zh-TW) UI translation
```

**Body**:
```markdown
Closes #492 (and relates to #483).

### Summary
Adds full Traditional Chinese (Taiwan, `zh-TW`) UI localization, translated directly from the English base (`values/strings.xml`) with Taiwan terminology rather than converted from `zh-rCN`.

### Files Changed (4 files only)
- `app/src/main/res/values-zh-rTW/strings.xml` — full translation (`2547` strings + `11` plurals, all `1618` `comment="..."` hints and placeholders preserved).
- `wear/src/main/res/values-zh-rTW/strings.xml` — full Wear OS translation (`69` strings). *(Note: `wear` uses the watch's system locale rather than the phone app's in-app picker.)*
- `app/src/main/kotlin/dev/patrickgold/florisboard/app/settings/advanced/OtherScreen.kt` — 1-line addition adding `"zh-TW"` after `"zh-CN"` in the in-app language picker (`中文 (台灣)`).
- `docs/zh-TW-ui-contribution.md` — concise Taiwan terminology glossary & AI batch prompt guide so `values-zh-rTW` stays in sync with future English `strings.xml` updates. *(Happy to remove this doc if you prefer keeping the PR strictly to `res/` + `OtherScreen.kt`.)*

### Verification
- Resource keys, plurals, placeholders, and `comment="..."` attributes match the English base (`0` missing, `0` extra, `0` placeholder mismatches).
- `xmllint --noout` passed on both `app` and `wear` XML files; built cleanly via Gradle `assembleDebug`.
- Real-device tested on Android (`中文 (台灣)` in-app switching, settings screens, providers, learned words).

### Screenshots (English vs. `zh-CN` vs. `zh-TW`)

| English | Simplified Chinese (`zh-CN`) | Traditional Chinese (`zh-TW`) |
| :---: | :---: | :---: |
| <img src="https://raw.githubusercontent.com/kuniakil/DictateKeyboard/assets/zh-tw-screenshots/other-en.jpg" width="260" alt="Other settings in English" /> | <img src="https://raw.githubusercontent.com/kuniakil/DictateKeyboard/assets/zh-tw-screenshots/other-zh-cn.jpg" width="260" alt="Other settings in Simplified Chinese" /> | <img src="https://raw.githubusercontent.com/kuniakil/DictateKeyboard/assets/zh-tw-screenshots/other-zh-tw.jpg" width="260" alt="Other settings in Traditional Chinese" /> |

| Language Picker (`中文 (台灣)`) | Dictate Settings | Learned Words |
| :---: | :---: | :---: |
| <img src="https://raw.githubusercontent.com/kuniakil/DictateKeyboard/assets/zh-tw-screenshots/language-picker-zh-tw.jpg" width="260" alt="Language picker showing 中文 (台灣)" /> | <img src="https://raw.githubusercontent.com/kuniakil/DictateKeyboard/assets/zh-tw-screenshots/dictate-settings-zh-tw.jpg" width="260" alt="Dictate settings in Traditional Chinese" /> | <img src="https://raw.githubusercontent.com/kuniakil/DictateKeyboard/assets/zh-tw-screenshots/learned-words-zh-tw.jpg" width="260" alt="Learned words screen in Traditional Chinese" /> |
```
