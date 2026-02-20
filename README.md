# ReVanced Automated Build Scripts

> **Fully automated GitHub Actions workflows to build and release ReVanced-patched apps (YouTube & Google Photos).**

![GitHub License](https://img.shields.io/github/license/X-Abhishek-X/ReVanced-Automated-Build-Scripts)
![ReVanced](https://img.shields.io/badge/ReVanced-Community-blue)
![Automated](https://img.shields.io/badge/Build-Automated-green)

This repository contains intelligent automation scripts that:

1.  **Check for updates** daily.
2.  **Download the optimal APKs** (handling Split APKs/XAPKs automatically).
3.  **Patch them** using the official [ReVanced CLI](https://github.com/ReVanced/revanced-cli) and [Patches](https://github.com/ReVanced/revanced-patches).
4.  **Release the ready-to-install APKs** via GitHub Releases.

---

## ✨ Features

- 🤖 **Zero Manual Work:** The workflows run automatically on a schedule.
- 📹 **YouTube ReVanced:**
  - Includes **AdBlocking, SponsorBlock, Background Playback, Return YouTube Dislike**, and more.
  - **Split APK Support:** Automatically detects and merges Split APKs (XAPKs) using `APKEditor` to ensure successful patching.
- 📷 **Google Photos ReVanced:**
  - Enables **Pixel-exclusive features** (Unlimited Storage spoofing).
  - **Side-by-Side Installation:** Changes the package name so you can install it alongside the official Google Photos app.
- 🛡️ **Robust automation:**
  - Custom Python scripts (`install_apkeep.py`) to safely fetch dependencies.
  - Error detection for missing resources or compatible versions.

---

## 🚀 How to Get the Apps

You don't need to run any code. Just download the latest build:

1.  Go to the **[Releases](../../releases)** page of this repository.
2.  Expand the latest **Assets** section.
3.  Download the APK you need:
    - `youtube-revanced-v20.14.43.apk`
    - `google-photos-revanced-vlatest.apk`

### Installation Instructions

#### For YouTube ReVanced:

1.  **Install GmsCore (MicroG)** first. This is required to log in.
    - [Download GmsCore here](https://github.com/ReVanced/GmsCore/releases).
2.  Install the `youtube-revanced-v20.14.43.apk` you downloaded.

#### For Google Photos ReVanced:

1.  Install `google-photos-revanced-vlatest.apk`.
2.  It will install as a separate app (thanks to the package rename patch). You can keep the original app if you wish.

---

## 🛠️ How It Works (For Developers)

This repository uses **GitHub Actions** to orchestrate the build process.

### Workflows

- **`check_updates.yml`**:
  - Checks for Google Photos updates.
  - Downloads the latest APK.
  - Patches it with "Spoof features" and "Change package name".
  - Releases the APK.
- **`youtube_update.yml`**:
  - Checks for YouTube updates.
  - Downloads the latest version (often a Split APK/XAPK).
  - **Extracts & Merges** the split APKs into a single `merged.apk`.
  - Patches it with a comprehensive list of features.
  - Releases the APK.

### Scripts

- `scripts/install_apkeep.py`: A robust Python script to download the correct `apkeep` binary (MUSL build) to avoid dependency errors on Linux runners.
- `scripts/check_updates.py`: Logic to determine if a new version needs to be built.

---

## 🤝 Forking & Building Your Own

If you want to run this yourself:

1.  **Fork** this repository.
2.  Go to the **Actions** tab in your fork and enable workflows.
3.  The scripts will run on the defined schedule (daily).
4.  You can manually trigger a build by going to **Actions** -> Select Workflow -> **Run workflow**.

---

## 🙏 Credits

This project is merely a wrapper for the amazing work done by the ReVanced Team. Using this repo relies on their tools:

- [ReVanced CLI](https://github.com/ReVanced/revanced-cli)
- [ReVanced Patches](https://github.com/ReVanced/revanced-patches)
- [ReVanced Integrations](https://github.com/ReVanced/revanced-integrations)
- [APKEditor](https://github.com/REAndroid/APKEditor) (for merging split APKs)
- [apkeep](https://github.com/EFForg/apkeep) (for downloading APKs)

---

## ⚖️ Disclaimer

- This project is **not affiliated with or endorsed by** ReVanced, Google, or YouTube.
- These scripts are for **educational and archival purposes only**.
- Use at your own risk. Patching apps may violate Terms of Service.
