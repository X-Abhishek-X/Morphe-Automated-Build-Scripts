# Morphe-Automated-Build-Scripts

[![Build Status](https://github.com/X-Abhishek-X/Morphe-Automated-Build-Scripts/actions/workflows/build_apps.yml/badge.svg)](https://github.com/X-Abhishek-X/Morphe-Automated-Build-Scripts/actions)
[![Latest Release](https://img.shields.io/github/v/release/X-Abhishek-X/Morphe-Automated-Build-Scripts?label=latest)](../../releases/latest)
[![Total Apps](https://img.shields.io/badge/apps-23-blue)](#supported-apps)

Automatically patched APKs for **23 Android apps**, rebuilt every 2 days. Patches sourced from [Morphe](https://github.com/MorpheApp), [De-ReVanced](https://github.com/RookieEnough/De-ReVanced), [Piko](https://github.com/crimera/piko), and [hoo-dles](https://github.com/hoo-dles/morphe-patches).

## Download

**[→ Latest Release](../../releases/latest)**

- **YouTube / YouTube Music / Google Photos** — install [ReVanced GmsCore](https://github.com/ReVanced/GmsCore/releases/latest) first
- **Everything else** — install directly, no extras needed

## Supported Apps

| Patch Source | Apps |
|---|---|
| **Morphe** | YouTube, YouTube Music, Reddit |
| **Piko** | Instagram |
| **hoo-dles** | Amazon Prime Video, CamScanner, Duolingo, FotMob, Nova Launcher, Podcast Addict, ProtonVPN, SofaScore, Solid Explorer, Windy, WPS Office, Xodo PDF |
| **De-ReVanced** | Cricbuzz, Facebook, Google Photos, Icon Pack Studio, Pixiv, Proton Mail, SoundCloud, Threads, TikTok |

## What Gets Patched

### Ad removal + tracking block
YouTube, YouTube Music, Reddit, TikTok, Facebook, Threads, Instagram, SoundCloud, Duolingo, CamScanner, WPS Office, FotMob, Podcast Addict, SofaScore, Windy, Cricbuzz, Pixiv, Google Photos

### Premium / paid features unlocked
| App | What's unlocked |
|---|---|
| **YouTube** | Background play, video downloads, SponsorBlock, no Shorts |
| **YouTube Music** | Background play, no ads |
| **Instagram** | Plus subscriber perks |
| **SoundCloud** | Go+ features |
| **Duolingo** | Super Duolingo — unlimited hearts, no ads |
| **Solid Explorer** | Trial restrictions removed |
| **Xodo PDF** | Premium features |
| **Nova Launcher** | Nova Prime features |
| **Podcast Addict** | Premium features |
| **ProtonVPN** | Plus plan features |
| **Proton Mail** | Plus plan features |
| **WPS Office** | Premium features |
| **CamScanner** | Premium features |
| **Google Photos** | Unlimited storage, DCIM folder backup control, GmsCore support (needs ReVanced GmsCore) |

### Download / save media
| App | What you can download |
|---|---|
| **Instagram** | Posts, reels, stories, carousels, audio |
| **Reddit** | Images and videos |
| **YouTube** | Videos without Premium |
| **TikTok** | Videos without watermark |

### Privacy
| App | What's changed |
|---|---|
| **Instagram** | Read DMs anonymously, disable screenshot detection, make ephemeral media permanent |
| **TikTok** | Telemetry reduction |
| **Facebook / Threads** | Tracking reduction |
| **Twitter/X** | Login token import/export |

### UI customisation
| App | Options |
|---|---|
| **Instagram** | AMOLED theme, disable Reels scrolling, disable double-tap like, disable video autoplay, hide notes tray, customise story ring size, change like animation, remove empty bottom space, hide highlights, more options on posts and profiles |
| **YouTube** | Hide layout components, player overlay button, open channel from live avatar |

## Recent Patch Updates

<!-- PATCH-UPDATES-START -->
_Updated automatically — check back after the next scheduled run._
<!-- PATCH-UPDATES-END -->

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
