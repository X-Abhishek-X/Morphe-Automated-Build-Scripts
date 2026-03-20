# Morphe-Automated-Build-Scripts

[![Build Status](https://github.com/X-Abhishek-X/ReVanced-Automated-Build-Scripts/actions/workflows/build_apps.yml/badge.svg)](https://github.com/X-Abhishek-X/ReVanced-Automated-Build-Scripts/actions)

GitHub Actions suite that monitors for new app versions and automatically builds patched APKs using [Morphe](https://github.com/MorpheApp) and [De-ReVanced](https://github.com/RookieEnough/De-ReVanced) patches. Checks every 2 days — only rebuilds apps whose supported version has changed.

### Supported apps

**Morphe native patches** (YouTube, YouTube Music, Reddit)

| App | Package |
|-----|---------|
| 📺 YouTube | `com.google.android.youtube` |
| 🎵 YouTube Music | `com.google.android.apps.youtube.music` |
| 🟠 Reddit | `com.reddit.frontpage` |

**De-ReVanced patches** ([RookieEnough/De-ReVanced](https://github.com/RookieEnough/De-ReVanced))

| App | App | App |
|-----|-----|-----|
| 🎵 Amazon Music | 🛍️ Amazon Shopping | 🍺 Angulus |
| 🎸 Bandcamp | 🏏 Cricbuzz | 🏰 Disney+ |
| 📘 Facebook | 💬 Messenger | 🧵 Threads |
| 📰 Google News | 📸 Google Photos | 🎙️ Google Recorder |
| ✉️ GMX Mail | 🔷 Hex Editor | 🎨 Icon Pack Studio |
| 📰 Inshorts | 🎛️ irplus | 🎬 Letterboxd |
| 📐 Microsoft Lens | 📱 Nothing X | 🇳🇱 NU.nl |
| 📺 Peacock TV | 📷 Photoshop Mix | 📐 Photomath |
| 🎨 Pixiv | ✉️ Proton Mail | 📦 RAR |
| 🎶 SoundCloud | 🏃 Strava | 🎵 TikTok |
| 🎵 TikTok (JP) | 📝 Tumblr | 📺 Twitch |
| 📞 Viber | | |

### How it works

1. Runs on a schedule every 2 days
2. Fetches latest `morphe-cli`, `morphe-patches`, and `de-revanced-patches`
3. Checks which of the 37 supported apps has a new compatible version
4. Downloads only the changed apps' APKs from Uptodown and patches them
5. Signs with a secure keystore and publishes all rebuilt APKs to a GitHub Release

### Download

Pre-built APKs are in [Releases](../../releases).

- **YouTube / YouTube Music**: install [ReVanced GmsCore](https://github.com/ReVanced/GmsCore/releases/latest) first for Google account sign-in
- **All other apps**: standalone install — no extra app needed

### Patch sources

| Source | Repo | Apps |
|--------|------|------|
| Morphe | [MorpheApp/morphe-patches](https://github.com/MorpheApp/morphe-patches) | YouTube, YouTube Music, Reddit |
| De-ReVanced | [RookieEnough/De-ReVanced](https://github.com/RookieEnough/De-ReVanced) | 34 additional apps |

### Disclaimer

Not affiliated with Google, Meta, TikTok, Twitch, or any app developer. Modifying APKs may violate Terms of Service. Use at your own risk.

### License

MIT
