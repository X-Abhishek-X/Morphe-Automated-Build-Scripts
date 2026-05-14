# Morphe-Automated-Build-Scripts

[![Build Status](https://github.com/X-Abhishek-X/Morphe-Automated-Build-Scripts/actions/workflows/build_apps.yml/badge.svg)](https://github.com/X-Abhishek-X/Morphe-Automated-Build-Scripts/actions)
[![Latest Release](https://img.shields.io/github/v/release/X-Abhishek-X/Morphe-Automated-Build-Scripts?label=latest)](../../releases/latest)
[![Total Apps](https://img.shields.io/badge/apps-23-blue)](#supported-apps)

Automatically patched APKs for **23 Android apps**, rebuilt every 2 days. Patches sourced from [Morphe](https://github.com/MorpheApp), [De-ReVanced](https://github.com/RookieEnough/De-ReVanced), [Piko](https://github.com/crimera/piko), and [hoo-dles](https://github.com/hoo-dles/morphe-patches).

## Download

**[→ Latest Release](../../releases/latest)**

- **YouTube / YouTube Music** — install [ReVanced GmsCore](https://github.com/ReVanced/GmsCore/releases/latest) first
- **Everything else** — install directly, no extras needed
- SHA256 checksums included in every release

## Supported Apps

| Patch Source | Apps |
|---|---|
| **Morphe** | YouTube, Reddit |
| **Piko** | Instagram |
| **hoo-dles** | Amazon Prime Video, CamScanner, Duolingo, FotMob, Nova Launcher, Podcast Addict, ProtonVPN, SofaScore, Solid Explorer, Windy, WPS Office, Xodo PDF |
| **De-ReVanced** | Cricbuzz, Facebook, Icon Pack Studio, Pixiv, Proton Mail, SoundCloud, Threads, TikTok |

## How It Works

1. Every 2 days, a GitHub Actions workflow checks for new supported app versions
2. Changed apps are downloaded from APKPure, signature-verified, and patched
3. Unchanged apps are carried over from the previous release automatically
4. Every release always contains all 23 apps

## Request an App

Open an [App Request issue](../../issues/new?template=app_request.yml) — if the app is supported by one of the patch bundles above, I'll add it.

## Disclaimer

Not affiliated with, endorsed by, or associated with any app developer or company whose apps appear here. All patches are from independent open-source projects — I did not create them.

**Not responsible for:** account bans, device damage, data loss, or ToS violations. Use at your own risk.
