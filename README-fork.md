# About this fork (unofficial)

This repository is an **unofficial fork of [Dictate Keyboard](https://github.com/DevEmperor/DictateKeyboard)** by [DevEmperor](https://github.com/DevEmperor), maintained by [@kuniakil](https://github.com/kuniakil) for **Traditional Chinese (zh-TW / Taiwan)** users.

- **Not affiliated with or endorsed by the upstream author.** All product names, logos and trademarks remain the property of their respective owners; this fork claims no trademark rights (Apache-2.0 §6).
- **Free, and not for sale.** Nothing here is monetised. The author's own app is the supported product — if it helps you, [buy it on Google Play](https://play.google.com/store/apps/details?id=net.devemperor.dictate) or [sponsor the author](https://github.com/sponsors/DevEmperor). Every donation link in the upstream README is preserved here unchanged.
- **Licensed under Apache-2.0**, the same license as the original project. Apache-2.0 permits modification and redistribution, so this fork is lawful. The obligations of §4 are met as follows:
  - the license text ships **inside the app** (*Settings → About → Open source licenses*) and as [`LICENSE`](LICENSE) in this repository;
  - the upstream [`NOTICE`](NOTICE) is kept unchanged and is attached to **every release** as `NOTICE.txt`;
  - **every release states what this fork changed** — [`docs/fork/MODIFICATIONS.md`](docs/fork/MODIFICATIONS.md), attached as `MODIFICATIONS.md` and repeated in the release notes;
  - no trademark rights are claimed: the build is clearly marked unofficial, carries the application id `net.devemperor.dictate.debug`, and therefore **installs next to the official app instead of replacing it**.

## What this fork changes

Three things, all additive and zh-TW-related. The file-by-file list is in [`docs/fork/MODIFICATIONS.md`](docs/fork/MODIFICATIONS.md).

1. **A complete Traditional Chinese (Taiwan) UI** — a `values-zh-rTW` locale for the app (2547 strings + 11 plurals) and for the watch (69 strings), plus the `zh-TW` entry in the app's language picker (so it can be switched to 中文 (台灣)).
2. **Cangjie (倉頡) radical character layout** and `zh-TW-*` typing defaults that use `$` instead of `¥`.
3. **A build/release workflow** that produces a signed debug APK here on GitHub Releases — the upstream project publishes no APK on GitHub — together with the localisation toolchain used to produce and check the zh-TW strings.

Nothing about the transcription or rewording engines was changed, no model download was redirected, and no upstream behaviour was removed.

## Installing

1. Download `app-debug.apk` from the [Releases](https://github.com/kuniakil/DictateKeyboard/releases) page.
2. It is signed with a fixed debug key, so later builds of this fork install over each other — no uninstall in between.
3. Its application id is `net.devemperor.dictate.debug`, so it installs **side by side with** the official app: the official app, its settings and its purchases stay untouched.

Then follow the configuration guide: [`docs/zh-TW-setup.md`](docs/zh-TW-setup.md) — engine split (transcription vs rewording), the Traditional Chinese style prompt, the automatic rewording prompt, the word list and the offline replacement rules.

## Credits

- **[DevEmperor](https://github.com/DevEmperor)** — Dictate Keyboard, the original project. Everything in this repository is a derivative work of it, under Apache-2.0.
- **[The FlorisBoard Contributors](https://github.com/florisboard/florisboard/graphs/contributors)** — FlorisBoard by Patrick Goldinger, the keyboard foundation Dictate is built on (Apache-2.0).
- Every third-party component keeps its own license; the app lists them all under *Settings → About → Third-party licenses* and *Data & model attributions*.
