# ReVanced-Automated-Build-Scripts

[![Build Status](https://github.com/X-Abhishek-X/ReVanced-Automated-Build-Scripts/actions/workflows/build_apps.yml/badge.svg)](https://github.com/X-Abhishek-X/ReVanced-Automated-Build-Scripts/actions)

GitHub Actions suite that monitors for new app versions and automatically builds ReVanced-patched APKs for YouTube, Google Photos, and Reddit. Also includes Windows scripts for local patching.

### How it works

1. Daily schedule checks for new supported app versions and updated patch sets
2. If an update is detected, fetches clean APKs from Uptodown and patches them using [ReVanced CLI](https://github.com/ReVanced/revanced-cli)
3. Signs and uploads patched APKs to a new GitHub Release

### Download

Pre-built APKs are available in [Releases](../../releases).

- **YouTube ReVanced**: Install [GmsCore](https://github.com/ReVanced/GmsCore/releases/latest) first for Google account sign-in
- **Google Photos ReVanced**: Installs as `com.google.android.apps.photos.revanced`, coexists with stock app
- **Reddit ReVanced**: Works standalone or alongside the official app

### Local patching (Windows)

Manual scripts in `local-scripts/` for patching on your own machine:

```
local-scripts/patch-youtube.bat          — one-click YouTube patch
local-scripts/patch-youtube-custom.ps1   — custom patch selection
local-scripts/patch-google-photos.bat    — Google Photos patch
```

Requires [ReVanced CLI](https://github.com/ReVanced/revanced-cli) and Java on PATH.

### Disclaimer

Not affiliated with Google, YouTube, Reddit, or the ReVanced team. Modifying APKs may violate application Terms of Service. Use at your own risk.

### License

MIT
