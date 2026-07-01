# Morphe-Automated-Build-Scripts

[![Build Status](https://github.com/X-Abhishek-X/Morphe-Automated-Build-Scripts/actions/workflows/build_apps.yml/badge.svg)](https://github.com/X-Abhishek-X/Morphe-Automated-Build-Scripts/actions)
[![Latest Release](https://img.shields.io/github/v/release/X-Abhishek-X/Morphe-Automated-Build-Scripts?label=latest)](../../releases/latest)
[![Total Apps](https://img.shields.io/badge/apps-53-blue)](#supported-applications)

53 Android apps, patched and rebuilt every two days. No setup, no command line, just grab the APK and install it.

> [!IMPORTANT]
> Personal build pipeline, no affiliation with Google, YouTube, Meta, Amazon, ByteDance, or anyone else. Use at your own risk — account bans, device issues, and ToS violations are your problem, not mine.

---

## Quick start

### 1. Install GmsCore — YouTube, YouTube Music, Google Photos only
All three spoof Google services internally. [ReVanced GmsCore](https://github.com/ReVanced/GmsCore/releases/latest) has to be on your phone first or sign-in will break.

### 2. Download
[Latest Release](../../releases/latest) — find the APK you want, download it, install it.

---

## Supported applications

53 apps across four patch sources. Expand a section to see package names and what got changed.

<details>
<summary><b>1. Morphe patches (3 apps)</b></summary>

| App | Package | Changes |
|---|---|---|
| YouTube | `com.google.android.youtube` | Ad blocking, background play, SponsorBlock, layout customisation |
| YouTube Music | `com.google.android.apps.youtube.music` | Ad blocking, background play, premium audio controls |
| Reddit | `com.reddit.frontpage` | Ad blocking, media downloader, tracking removed |

</details>

<details>
<summary><b>2. Piko patches (2 apps)</b></summary>

| App | Package | Changes |
|---|---|---|
| Instagram | `com.instagram.android` | Ad blocking, AMOLED theme, anonymous story/DM viewing, reels auto-scroll off, high-res downloads |
| Twitter / X | `com.twitter.android` | Ad blocking, telemetry removed, login token import/export |

</details>

<details>
<summary><b>3. hoo-dles patches (16 apps)</b></summary>

| App | Package | Changes |
|---|---|---|
| AdGuard | `com.adguard.android` | Subscription features unlocked |
| Amazon Prime Video | `com.amazon.avod.thirdpartyclient` | Tracker blocking, interface cleanup |
| Duolingo | `com.duolingo` | Super Duolingo features, unlimited hearts, ad blocking |
| MyFitnessPal | `com.myfitnesspal.android` | Premium features unlocked |
| Nova Launcher | `com.teslacoilsw.launcher` | Nova Prime features unlocked |
| Solid Explorer | `pl.solidexplorer2` | Trial limitations removed |
| Xodo PDF | `com.xodo.pdf.reader` | Premium PDF tools unlocked |
| Ibis Paint X | `jp.ne.ibis.ibispaintx.app` | Premium drawing tools unlocked |
| WPS Office | `cn.wps.moffice_eng` | Premium tools unlocked |
| CamScanner | `com.intsig.camscanner` | Ad blocking, premium processing, clean exports |
| FotMob | `com.mobilefootie.wc2010` | Ad blocking, premium features |
| Pandora | `com.pandora.android` | Premium audio playback |
| Podcast Addict | `com.bambuna.podcastaddict` | Premium ad-free mode |
| ProtonVPN | `ch.protonvpn.android` | Subscription features unlocked |
| Windy | `com.windyty.android` | Premium weather tools |
| SofaScore | `com.sofascore.results` | Ad blocking, tracking removed |

</details>

<details>
<summary><b>4. De-ReVanced / De-Vanced patches (32 apps)</b></summary>

| App | Package | Changes |
|---|---|---|
| TikTok | `com.zhiliaoapp.musically` | Ad blocking, no download watermarks, seek bar enabled, reels auto-scroll |
| TikTok JP | `com.ss.android.ugc.trill` | Ad blocking, no watermarks |
| Twitch | `tv.twitch.android.app` | Live ad blocking, auto channel point claims, playback speed, chat customisation |
| Facebook | `com.facebook.katana` | Feed/story ad blocking, video downloading, telemetry removed |
| Messenger | `com.facebook.orca` | Ad blocking, tracking removed |
| Threads | `com.instagram.barcelona` | Ad blocking, tracking params stripped, media downloads |
| Disney+ | `com.disney.disneyplus` | Analytics and tracker blocking |
| SoundCloud | `com.soundcloud.android` | Ad blocking, background play, skip limits removed |
| Strava | `com.strava` | Ad blocking, extra stats visible |
| Tumblr | `com.tumblr` | Dashboard ad blocking, tracking removed |
| Amazon Shopping | `com.amazon.mShop.android.shopping` | Ad blocking, telemetry removed |
| Amazon Music | `com.amazon.mp3` | Ad blocking, background play |
| Google Photos | `com.google.android.apps.photos` | Unlimited backup via Pixel spoof, DCIM backup controls, GmsCore support |
| Google News | `com.google.android.apps.magazines` | Ad blocking, premium overlays removed |
| Google Recorder | `com.google.android.apps.recorder` | Offline transcription, installs on non-Pixel devices |
| ProtonMail | `ch.protonmail.android` | Plus features unlocked, tracking removed |
| Viber | `com.viber.voip` | Ad blocking, telemetry removed |
| Letterboxd | `com.letterboxd.letterboxd` | Ad blocking, premium features |
| Pixiv | `jp.pxv.android` | Ad blocking, high-res illustration search |
| Cricbuzz | `com.cricbuzz.android` | Ad blocking, premium features |
| Bandcamp | `com.bandcamp.android` | Premium play, media downloading |
| RAR | `com.rarlab.rar` | Ad blocking, premium tools |
| Photomath | `com.microblink.photomath` | Plus features, detailed step-by-step solutions |
| Peacock TV | `com.peacocktv.peacockandroid` | Tracker blocking, reduced ad load |
| Nothing X | `com.nothing.smartcenter` | Nothing device features on non-Nothing phones |
| Inshorts | `com.nis.app` | Ad blocking, premium features |
| Icon Pack Studio | `ginlemon.iconpackstudio` | Pro tier unlocked |
| Hex Editor | `com.myprog.hexedit` | Ad blocking, Pro features |
| GMX Mail | `de.gmx.mobile.android.mail` | Ad blocking, tracking removed |
| Angulus | `com.drinkplusplus.angulus` | Premium features unlocked |
| IRplus | `net.binarymode.android.irplus` | Ad blocking, Pro features |
| NU.nl | `nl.sanomamedia.android.nu` | Ad blocking, tracking removed |

</details>

---

## Recent patch updates

<!-- PATCH-UPDATES-START -->
_Last checked: 2026-07-01_

### [Morphe v1.32.0](https://github.com/MorpheApp/morphe-patches/releases/tag/v1.32.0)
* **YouTube - Bypass link redirects:** Resolve patch not working on community posts and video descriptions ([#1755](https://github.com/MorpheApp/morphe-patches/issues/1755))
* **YouTube - Change form factor:** Prevent app crash when using tablet mode in `onResume` state ([#1803](https://github.com/MorpheApp/morphe-patches/issues/1803))
* **YouTube - Disable player popup panels:** Patch doesn't work in some circumstances
* **YouTube - Hide layout components:** Resolve "Hide horizontal shelves" hiding other components ([#930](https://github.com/MorpheApp/morphe-patches/issues/930))
* **YouTube - Sanitize sharing links:** Live links are not sanitized
* **YouTube - Navigation bar:** Prevent navigation bar animation when swiping to dismiss miniplayer ([#1800](https://github.com/MorpheApp/morphe-patches/issues/1800))
* **YouTube - Override YouTube Music buttons:** Target app opens when clicking on 'YouTube Music' button inside explore menu ([#1707](https://github.com/MorpheApp/morphe-patches/issues/1707))
* **YouTube - Reload video:** App exits after pressing back button ([#1740](https://github.com/MorpheApp/morphe-patches/issues/1740))

### [De-ReVanced v1.0.4](https://github.com/RookieEnough/De-Vanced/releases/tag/v1.0.4)
* avoid forcing Photos frictionless login
* release v1.0.4 (Photos account persistence + TikTok defaults)
* stabilize Google Photos GmsCore support
* Enable **all** TikTok patches by default on **43.6.2** and **43.8.3**.
* Keep **Settings** + **Enable Open Debug** as **43.6.2-only** (not compatible with 43.8.3).

### [De-Vanced v1.0.4](https://github.com/RookieEnough/De-Vanced/releases/tag/v1.0.4)
* avoid forcing Photos frictionless login
* release v1.0.4 (Photos account persistence + TikTok defaults)
* stabilize Google Photos GmsCore support
* Enable **all** TikTok patches by default on **43.6.2** and **43.8.3**.
* Keep **Settings** + **Enable Open Debug** as **43.6.2-only** (not compatible with 43.8.3).

### [Piko v3.7.0](https://github.com/crimera/piko/releases/tag/v3.7.0)
* **Instagram:** Fix `Allow user network certificate` being shown on Settings even without including
* **Instagram:** Fix `Change like animation` enum class injection issue
* **Instagram:** Fix `Disable typing status` on v435
* **Instagram:** Fix `User profile action bar` logic
* **Instagram:** Fix button press key check
* **Instagram:** Fix button press key check (again)
* **Instagram:** Fix ghost eye icon position on DM action bar
* **Instagram:** Fix inverse issue of `Hide reshare button`

### [hoo-dles v1.38.1](https://github.com/hoo-dles/morphe-patches/releases/tag/v1.38.1)
* **Duolingo:** Update patches to support v6.85.7

<!-- PATCH-UPDATES-END -->

---

## How it works

Runs every 48 hours. When a patch bundle updates, the pipeline downloads the affected APKs from APKMirror, Uptodown, or APKPure, in that order. If none of them have the exact version indexed, it falls back to a version-free pull from APKPure. Before anything gets patched, every APK goes through `apksigner` and SHA-256 cert pinning against [.github/cert_pins.json](.github/cert_pins.json). Fail either check and it gets dropped. Unchanged apps carry over from the last release so you always get all 53.

```mermaid
graph TD
    A[Cron / 48 hrs] --> B[Check patch bundle versions]
    B --> C[Resolve APK versions]
    C --> D[Download from mirrors]
    D --> E[apksigner + cert pin check]
    E -->|Pass| F[Patch via morphe-cli]
    E -->|Fail| X[Drop — not patched]
    F --> G[Carry over unchanged APKs]
    G --> H[Publish release]
```

## Requesting an app

Open an [App Request Issue](../../issues/new?template=app_request.yml). Gets added if it's supported by one of the four patch bundles.
