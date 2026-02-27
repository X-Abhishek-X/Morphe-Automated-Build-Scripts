# ReVanced Automated Build Scripts

> Fully automated GitHub Actions workflows to build and release ReVanced-patched apps for YouTube, Google Photos, and Reddit.

![GitHub License](https://img.shields.io/github/license/X-Abhishek-X/ReVanced-Automated-Build-Scripts)
![ReVanced](https://img.shields.io/badge/ReVanced-Community-blue)
![Automated](https://img.shields.io/badge/Build-Automated-green)

This repository automatically builds ReVanced-patched APKs using GitHub Actions — triggered only when a new supported app version is detected, so you always get the latest compatible build without unnecessary runs.

---

## What it does

- Checks for new supported versions of **YouTube**, **Google Photos**, and **Reddit** daily.
- Compares against the last successfully built versions — **only rebuilds when something actually changed**.
- Downloads clean standalone APKs from Uptodown (no split/XAPK bundles).
- Patches using the official [ReVanced CLI](https://github.com/ReVanced/revanced-cli) and [Patches](https://github.com/ReVanced/revanced-patches).
- Creates a new GitHub Release with all three patched APKs attached.
- Automatically deletes the previous release to keep things clean.

---

## Downloading the APKs

Go to the **[Releases](../../releases)** page and download the latest build:

| App                       | Latest Filename                                |
| ------------------------- | ---------------------------------------------- |
| 📺 YouTube ReVanced       | `youtube-revanced-vX.X.X-YYYY.MM.DD.apk`       |
| 📸 Google Photos ReVanced | `google-photos-revanced-vX.X.X-YYYY.MM.DD.apk` |
| 🔴 Reddit ReVanced        | `reddit-revanced-vX.X.X-YYYY.MM.DD.apk`        |

### Installing YouTube ReVanced

1. Install **GmsCore (MicroG)** first — required for Google account login.
   - [Download GmsCore here](https://github.com/ReVanced/GmsCore/releases/latest).
2. Install the YouTube ReVanced APK.
3. Open the app and sign in.

### Installing Google Photos ReVanced

1. Install the Google Photos ReVanced APK.
2. It installs as a **separate app** alongside your original Google Photos — both can coexist.
3. Sign in to get free unlimited original quality backup.

### Installing Reddit ReVanced

1. Uninstall or keep the original Reddit app — Reddit ReVanced installs alongside it.
2. Install the Reddit ReVanced APK.
3. Sign in with your Reddit account.

---

## Patches included

### YouTube ReVanced

Ad blocking, SponsorBlock, Return YouTube Dislike, background playback, downloads, hide Shorts, swipe controls, custom themes, and more.

### Google Photos ReVanced

- **Spoof features** — Enables Pixel-exclusive features including unlimited original quality backup.
- **Enable DCIM folders backup control** — Control which folders are backed up.
- **GmsCore support** — Works without root via MicroG.
- **Change package name** — Installs alongside the original app.

### Reddit ReVanced

- **Spoof client** — Removes old Reddit API restrictions.
- **Premium icon** — Unlocks premium app icons.
- **Hide ads** — Removes ads from the feed.
- **Sanitize sharing links** — Removes tracking parameters from shared links.
- **Open links externally** — Opens external links in your default browser.
- **GmsCore support** — Works without root via MicroG.

---

## How it works

A single GitHub Actions workflow (`build_apps.yml`) runs daily:

1. **Job 1 — `check-versions`**: Fetches the latest ReVanced CLI and patches, queries compatible app versions for all three apps, and compares them to the last successfully built state.

2. **Job 2 — `build-and-release`** _(only runs if changes are detected)_:
   - Downloads APKs from Uptodown.
   - Patches each app with the relevant patches.
   - Creates a dated GitHub Release with all APKs attached.
   - Commits the updated state file so future runs know what was just built.

### Smart update detection

The workflow tracks built versions in `.github/last_built_versions.json`. On each check run, it compares:

- The latest supported app versions (per ReVanced patches)
- The patches version itself (new patches → rebuild everything)

If nothing changed, the build job is **skipped entirely** — no unnecessary work.

---

## Running your own builds

1. Fork this repository.
2. Go to the **Actions** tab in your fork and enable workflows.
3. Workflows run daily automatically at **2 AM UTC**, or trigger manually via **Actions → Build ReVanced Apps → Run workflow**.

---

## Credits

This is a build wrapper around the tools made by the ReVanced team:

- [ReVanced CLI](https://github.com/ReVanced/revanced-cli)
- [ReVanced Patches](https://github.com/ReVanced/revanced-patches)
- [apkeep](https://github.com/EFForg/apkeep) — for downloading APKs
- [Uptodown](https://uptodown.com) — standalone APK source

---

## Disclaimer

This project is not affiliated with or endorsed by ReVanced, Google, YouTube, or Reddit.
These scripts are for educational and personal use only. Use at your own risk.
Patching apps may violate Terms of Service of the respective applications.
