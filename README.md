# Morphe-Automated-Build-Scripts

[![Build Status](https://github.com/X-Abhishek-X/Morphe-Automated-Build-Scripts/actions/workflows/build_apps.yml/badge.svg)](https://github.com/X-Abhishek-X/Morphe-Automated-Build-Scripts/actions)

GitHub Actions pipeline that monitors for new app versions and automatically builds patched APKs using [Morphe](https://github.com/MorpheApp) and [De-ReVanced](https://github.com/RookieEnough/De-ReVanced) patches. Runs every 2 days — only rebuilds apps whose supported version has changed since the last run.

## Supported apps (37 total)

### Morphe native patches

| App | Package |
|-----|---------|
| YouTube | `com.google.android.youtube` |
| YouTube Music | `com.google.android.apps.youtube.music` |
| Reddit | `com.reddit.frontpage` |

### De-ReVanced patches

| | | | |
|--|--|--|--|
| Amazon Music | Amazon Shopping | Angulus | Bandcamp |
| Cricbuzz | Disney+ | Facebook | GMX Mail |
| Google News | Google Photos | Google Recorder | Hex Editor |
| Icon Pack Studio | Inshorts | irplus | Letterboxd |
| Messenger | Microsoft Lens | Nothing X | NU.nl |
| Peacock TV | Photomath | Photoshop Mix | Pixiv |
| Proton Mail | RAR | SoundCloud | Strava |
| Threads | TikTok | TikTok (JP) | Tumblr |
| Twitch | Viber | | |

## Download

Pre-built APKs are in [Releases](../../releases).

- **YouTube / YouTube Music** — install [ReVanced GmsCore](https://github.com/ReVanced/GmsCore/releases/latest) first for Google account sign-in
- **All other apps** — standalone install, no extra app needed

Verify your download:
```sh
sha256sum -c SHA256SUMS.txt
```

## How it works

```
Every 2 days (06:00 UTC)
        │
        ▼
Check latest morphe-cli + morphe-patches + de-revanced-patches
        │
        ▼
Compare supported versions against last_built_versions.json
        │
        ├── No change → skip (no release created)
        │
        └── Changed apps detected
                │
                ▼
          Download APK (APKPure → Uptodown fallback)
                │
                ▼
          Patch with Morphe CLI (-p morphe -p de-revanced)
                │
                ▼
          Re-sign with repo keystore
                │
                ▼
          Publish to GitHub Release + SHA256SUMS.txt
          Save artifact (90-day backup)
          Update last_built_versions.json [skip ci]
```

## Manual build

Trigger a build from the [Actions tab](../../actions/workflows/build_apps.yml) with these inputs:

| Input | Default | Description |
|-------|---------|-------------|
| `app` | `all` | Specific app key or `all` for auto-detection |
| `version_override` | _(empty)_ | Force a specific version (e.g. `19.16.39`) |
| `arch` | `arm64-v8a` | Target ABI: `arm64-v8a`, `armeabi-v7a`, `universal` |

App keys: `youtube`, `music`, `reddit`, `tiktok`, `tiktok_jp`, `twitch`, `facebook`, `messenger`, `threads`, `disney_plus`, `soundcloud`, `strava`, `tumblr`, `amazon_shop`, `amazon_music`, `google_photos`, `google_news`, `google_rec`, `proton_mail`, `ms_lens`, `viber`, `letterboxd`, `pixiv`, `cricbuzz`, `bandcamp`, `rar`, `photomath`, `peacock_tv`, `nothing_x`, `inshorts`, `icon_studio`, `hex_editor`, `gmx_mail`, `angulus`, `irplus`, `photoshop_mix`, `nu_nl`

## Patch sources

| Source | Repo | Apps |
|--------|------|------|
| Morphe | [MorpheApp/morphe-patches](https://github.com/MorpheApp/morphe-patches) | YouTube, YouTube Music, Reddit |
| De-ReVanced | [RookieEnough/De-ReVanced](https://github.com/RookieEnough/De-ReVanced) | 34 additional apps |

## Secrets required (for forks)

| Secret | Purpose |
|--------|---------|
| `KEYSTORE_BASE64` | Base64-encoded `.jks` keystore for APK signing |
| `GITHUB_TOKEN` | Auto-provided by Actions — no setup needed |

## Disclaimer

Not affiliated with Google, Meta, TikTok, Twitch, or any app developer. Patching APKs may violate app Terms of Service. Use at your own risk.

## License

MIT