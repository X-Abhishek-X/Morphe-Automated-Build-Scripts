# ReVanced Automated Build Scripts

> Fully automated GitHub Actions workflows to build and release ReVanced-patched apps for YouTube and Google Photos.

![GitHub License](https://img.shields.io/github/license/X-Abhishek-X/ReVanced-Automated-Build-Scripts)
![ReVanced](https://img.shields.io/badge/ReVanced-Community-blue)
![Automated](https://img.shields.io/badge/Build-Automated-green)

This repository automatically builds ReVanced-patched APKs daily using GitHub Actions — no manual work needed.

---

## What it does

- Checks for new versions of YouTube and Google Photos daily.
- Downloads the APK (handles split APKs/XAPKs automatically via APKEditor).
- Patches using the official [ReVanced CLI](https://github.com/ReVanced/revanced-cli) and [Patches](https://github.com/ReVanced/revanced-patches).
- Builds two versions: **ARM64-v8a** (64-bit, most modern devices) and **ARMv7** (32-bit, older devices), both nodpi.
- Creates a new GitHub Release every day with both APKs attached.
- Automatically deletes the previous day's release to keep things clean.

---

## Downloading the APKs

Go to the **[Releases](../../releases)** page and download the latest build for your device:

| App                    | ARM64-v8a (64-bit)                                             | ARMv7 (32-bit)                                                   |
| ---------------------- | -------------------------------------------------------------- | ---------------------------------------------------------------- |
| YouTube ReVanced       | `youtube-revanced-vX.X.X-arm64-v8a-nodpi-YYYY.MM.DD.apk`       | `youtube-revanced-vX.X.X-armeabi-v7a-nodpi-YYYY.MM.DD.apk`       |
| Google Photos ReVanced | `google-photos-revanced-vX.X.X-arm64-v8a-nodpi-YYYY.MM.DD.apk` | `google-photos-revanced-vX.X.X-armeabi-v7a-nodpi-YYYY.MM.DD.apk` |

Not sure which one to pick? Most Android phones from 2017 onwards use ARM64-v8a.

### Installing YouTube ReVanced

1. Install **GmsCore (MicroG)** first — this is required for Google account login.
   - [Download GmsCore here](https://github.com/ReVanced/GmsCore/releases).
2. Install the YouTube ReVanced APK for your architecture.
3. Open the app and sign in.

### Installing Google Photos ReVanced

1. Install the Google Photos ReVanced APK for your architecture.
2. It installs as a **separate app** alongside your original Google Photos — both can coexist.
3. Sign in to get free unlimited original quality backup.

---

## Patches included

### YouTube ReVanced

Ad blocking, SponsorBlock, Return YouTube Dislike, background playback, download support, hide Shorts, swipe controls, custom themes, and more. Full list is in each release's description.

### Google Photos ReVanced

- **Spoof features** — Enables Pixel-exclusive features including unlimited original quality backup.
- **Enable DCIM folders backup control** — Control which folders are backed up.
- **GmsCore support** — Works without root via MicroG.
- **Change package name** — Installs alongside the original app.

---

## How it works

Two GitHub Actions workflows run on a daily schedule:

- **`check_updates.yml`** — Handles Google Photos. Runs at midnight UTC.
- **`youtube_update.yml`** — Handles YouTube. Runs at 1 AM UTC.

Both workflows:

1. Run `scripts/check_updates.py` to fetch the latest ReVanced CLI and patches.
2. Download the APK via `apkeep`.
3. If the download is a split APK (XAPK), extract and merge it with APKEditor into separate ARM64 and ARMv7 builds.
4. Patch both builds using `revanced-cli`.
5. Publish a new dated GitHub Release.
6. Delete the previous day's release.

### Scripts

- `scripts/install_apkeep.py` — Downloads the correct `apkeep` binary for the GitHub Actions runner.
- `scripts/check_updates.py` — Fetches latest ReVanced CLI/patches versions and determines compatible app versions.

---

## Running your own builds

1. Fork this repository.
2. Go to the **Actions** tab in your fork and enable workflows.
3. Workflows run daily automatically, or you can trigger them manually via **Actions > Select Workflow > Run workflow**.

---

## Credits

This is a build wrapper around the tools made by the ReVanced team:

- [ReVanced CLI](https://github.com/ReVanced/revanced-cli)
- [ReVanced Patches](https://github.com/ReVanced/revanced-patches)
- [APKEditor](https://github.com/REAndroid/APKEditor) — for merging split APKs
- [apkeep](https://github.com/EFForg/apkeep) — for downloading APKs from the Play Store

---

## Disclaimer

This project is not affiliated with or endorsed by ReVanced, Google, or YouTube.
These scripts are for educational and personal use only. Use at your own risk.
Patching apps may violate Terms of Service of the respective applications.
