# Modifications made by this fork

| | |
|---|---|
| **Fork** | `kuniakil/DictateKeyboard` — **unofficial**, not affiliated with or endorsed by the upstream author |
| **Upstream** | [`DevEmperor/DictateKeyboard`](https://github.com/DevEmperor/DictateKeyboard) — "Dictate Keyboard", Apache-2.0 |
| **Base commit** | `84adfa99` (2026-11-20) |
| **License** | Apache-2.0 — **unchanged**. See [`LICENSE`](../../LICENSE) and [`NOTICE`](../../NOTICE) |

This file exists to satisfy Apache-2.0 **§4(b)** ("cause any modified files to carry prominent notices stating that You changed the files") and **§4(d)** (include the attribution notices carried by the upstream `NOTICE` file) for the binaries this fork publishes. It is attached to every GitHub Release of this fork as `MODIFICATIONS.md`, next to `NOTICE.txt`.

## Summary

Everything below is **additive or zh-TW-scoped**. No upstream feature, code path, model download, telemetry or attribution was removed, disabled or redirected.

| # | Area | Change |
|---|---|---|
| 1 | App UI | New locale `values-zh-rTW` — a complete Traditional Chinese (Taiwan) translation: **2547 strings + 11 plurals**, every `comment="…"` translation hint from the base preserved |
| 2 | Watch UI | New locale `wear/…/values-zh-rTW/strings.xml` — **69 strings** |
| 3 | Language picker | `OtherScreen.kt` — **one line added**: the `"zh-TW"` tag to the app-language list (42 entries in total, `auto` included), so the app can be switched to 中文 (台灣) |
| 4 | Typing layout | New **Cangjie (倉頡)** radical character layout (`cangjie.json`, 112 lines) + its registration in the layouts extension |
| 5 | zh-TW typing defaults | The two `zh-TW-*` subtype presets (`boshiamy`, `cangjielarge`) now use the `$` currency set instead of `¥`; `zh-TW-cangjielarge` defaults to the new Cangjie layout |
| 6 | Build & release | `.github/workflows/build-apk.yml` — a GitHub Actions workflow that builds a **fixed-signature debug APK** and publishes it to this fork's Releases. The upstream project publishes no APK on GitHub; this is the only way to obtain a build from source here |
| 7 | Localisation toolchain | `tools/check-l10n.py`, `tools/build-zh-tw-strings.py`, `tools/l10n_batch.py`, `l10n/` — the scripts, translation data and Taiwan-usage glossary used to produce and verify the zh-TW strings |
| 8 | Documentation | `README-fork.md`, `docs/zh-TW-setup.md`, `docs/zh-TW-ui-contribution.md`, `docs/worksheet-dictatekeyboard-zhtw-ui-20261120.md`, `docs/opentypeless-and-dictatekeyboard-stt-tuning-20261117.md` — configuration guide, contribution notes, working notes |

## The seven shipped files

Everything that ends up inside the APK, plus the release automation:

```
app/src/main/res/values-zh-rTW/strings.xml                                                  (new — 2547 strings + 11 plurals)
wear/src/main/res/values-zh-rTW/strings.xml                                                 (new — 69 strings)
app/src/main/kotlin/…/app/settings/advanced/OtherScreen.kt                                  (+1 line — the "zh-TW" language tag)
app/src/main/assets/ime/keyboard/org.florisboard.layouts/layouts/characters/cangjie.json    (new — 112 lines)
app/src/main/assets/ime/keyboard/org.florisboard.layouts/extension.json                      (+6 lines — cangjie layout registration)
app/src/main/assets/ime/keyboard/org.florisboard.localization/extension.json                 (2 zh-TW subtype presets — currency set + default layout)
.github/workflows/build-apk.yml                                                              (release automation for this fork)
```

Everything else that differs from upstream lives under `l10n/`, `tools/` and `docs/`, plus `CLAUDE.md` / `AGENTS.md` — build-time tooling and documentation that is not part of the shipped application.

## Attribution

- **Dictate Keyboard** — © DevEmperor, Apache-2.0. All product names, logos and trademarks remain the property of their respective owners; this fork claims no trademark rights (Apache-2.0 §6) and is marked as unofficial everywhere it is published.
- **FlorisBoard** — © 2020-2026 The FlorisBoard Contributors, original author Patrick Goldinger, Apache-2.0. The upstream `NOTICE` file is kept **unchanged** in this repository and is attached to every release as `NOTICE.txt`.
- **Third-party components** keep their own licenses and are listed inside the app under *Settings → About → Open source licenses*, *Third-party licenses* and *Data & model attributions*. This fork changed none of those screens, and the Apache-2.0 text ships inside the APK (`app/src/main/assets/license/project_license.txt`).
- **On-device models** (Whisper, Parakeet, SenseVoice, Dolphin, Kroko ASR, …) are **downloaded at runtime from the upstream project's releases** — the URLs in `LocalModelCatalog.kt` and friends are untouched. This fork redistributes no model weights, so the model terms listed in `NOTICE` (FunASR Model License, CC-BY-SA, CC-BY-4.0, MIT, BSD-2-Clause, …) are unaffected.

## Relationship to the upstream project

This fork exists to make the app usable for Traditional Chinese (Taiwan) users. The zh-TW work is offered upstream as well — see the upstream issue on Traditional Chinese UI localization — and is expected to land there. Until it does, this fork keeps it available, free of charge and **not for sale**. The upstream author's own app remains the supported product: [buy it on Google Play](https://play.google.com/store/apps/details?id=net.devemperor.dictate) or [sponsor the author](https://github.com/sponsors/DevEmperor). Every donation link in the upstream README is preserved here unchanged.
