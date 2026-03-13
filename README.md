# ReVanced Automated Build Scripts

[![Build Status](https://github.com/X-Abhishek-X/ReVanced-Automated-Build-Scripts/actions/workflows/build_apps.yml/badge.svg)](https://github.com/X-Abhishek-X/ReVanced-Automated-Build-Scripts/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![ReVanced](https://img.shields.io/badge/ReVanced-Community-blue)](https://github.com/ReVanced)

A powerful, fully automated GitHub Actions suite designed to build and release **ReVanced-patched** applications for YouTube, Google Photos, and Reddit. This repository monitors for new app versions and applies the latest community patches automatically.

---

## 🚀 What it does

- **📅 Daily Version Monitoring**: Scans for new supported versions of YouTube, Google Photos, and Reddit every 24 hours.
- **⚡ Smart Rebuilding**: Only triggers a build if a new app version or an updated patch set is detected.
- **📦 Clean APK Sourcing**: Automatically fetches standalone APKs from reliable sources (Uptodown), avoiding complex split-APK issues.
- **🛠️ Professional Patching**: Utilizes the official [ReVanced CLI](https://github.com/ReVanced/revanced-cli) for 100% compatibility.
- **🧹 Automated Releases**: Maintains a clean release history by automatically attaching the latest builds and removing outdated ones.

---

## 📥 Downloading & Installation

Access the **[Latest Releases](../../releases)** to download the pre-patched binaries.

### Quick Start Guide

#### 📺 YouTube ReVanced
1. **Required**: Install [ReVanced GmsCore](https://github.com/ReVanced/GmsCore/releases/latest) first to enable Google Account sign-in.
2. Install the YouTube ReVanced APK from the releases.
3. Open and enjoy ad-free playback.

#### 📸 Google Photos ReVanced
1. Install the Google Photos ReVanced APK.
2. Note: This installs as a **separate application** (`com.google.android.apps.photos.revanced`) and can coexist with the stock app.
3. Sign in to enable Pixel-exclusive unlimited storage features.

#### 🔴 Reddit ReVanced
1. (Optional) Uninstall the official Reddit app to avoid confusion.
2. Install the Reddit ReVanced APK.
3. Sign in to enjoy an ad-free experience and premium icons.

---

## 🛠️ Included Patches

### YouTube ReVanced
- **Ad Blocking & SponsorBlock integration**
- **Background Playback & PiP**
- **Return YouTube Dislike (RYD)**
- **Swipe Controls & Custom Themes**

### Google Photos ReVanced
- **Device Spoofing**: Unlocks Pixel-exclusive unlimited original quality backups.
- **DCIM Backup Control**: Granular folder selection for cloud sync.
- **Non-Root Support**: Fully compatible with MicroG/GmsCore.

### Reddit ReVanced
- **Client Spoofing**: Removes restrictions on 3rd party API usage.
- **Ad Removal**: Clean, sponsored-post-free feed.
- **Privacy Improvements**: Sanitized sharing links (removes tracking params).

---

## ⚙️ How it Works

The automation is powered by a sophisticated GitHub Actions workflow:

1. **Version Sync**: Queries the ReVanced API for the latest compatible app versions.
2. **Delta Check**: Compares detected versions against `.github/last_built_versions.json`.
3. **Automated Build**: If an update is found, it clones the CLI, patches the APKs, and signs them using a secure keystore.
4. **Deployment**: Uploads assets to a new GitHub Release.

---

## ⚠️ Disclaimer

This project provides automation scripts that modify third-party application binaries. Use of these scripts may violate the Terms of Service of the respective applications. This project is not affiliated with Google, YouTube, Reddit, or the official ReVanced team. Use at your own risk.

---
**Maintained by [X-Abhishek-X](https://github.com/X-Abhishek-X)**
olate Terms of Service of the respective applications.
