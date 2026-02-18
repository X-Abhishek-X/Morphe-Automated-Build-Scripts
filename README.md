# ReVanced APK Patcher Scripts

> **Easy-to-use Windows batch and PowerShell scripts for patching YouTube and Google Photos with ReVanced**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![ReVanced](https://img.shields.io/badge/ReVanced-Community-blue)](https://revanced.app)

Simplified wrapper scripts for the [ReVanced CLI](https://github.com/ReVanced/revanced-cli) that make patching Android apps easy on Windows. No complex commands needed!

---

## ⚠️ Important Notice

**This is NOT an official ReVanced project.** This repository only provides convenience scripts. All patching functionality comes from the official [ReVanced Team](https://github.com/ReVanced).

**Credits**: See [CREDITS.md](CREDITS.md) for full attribution to the ReVanced team.

---

## ✨ Features

- 🎯 **Simple Scripts**: Just double-click to patch
- 🎨 **Interactive Patch Selection**: Choose exactly which patches you want (YouTube)
- 📦 **Pre-configured Presets**: Recommended patches ready to go
- 🔧 **Windows Optimized**: Batch and PowerShell scripts for easy use
- 📝 **Clear Error Messages**: Know exactly what went wrong

---

## 📋 Prerequisites

### Required Software

1. **Java 17 or higher**

   - Download: [Adoptium JDK](https://adoptium.net/) or [Oracle JDK](https://www.oracle.com/java/technologies/downloads/)
   - Verify installation: Open PowerShell and run `java -version`

2. **Android Device**
   - Android 8.0 (Oreo) or higher
   - USB debugging enabled (for ADB installation) OR ability to install APKs manually

### Required Files (Download Separately)

This repository **does NOT include** the following files due to size and licensing. You must download them:

#### 1. ReVanced CLI

- **File**: `revanced-cli-X.X.X-all.jar`
- **Download**: [ReVanced CLI Releases](https://github.com/ReVanced/revanced-cli/releases)
- **Rename to**: `revanced-cli-5.0.1-all.jar` (or update script filenames)

#### 2. ReVanced Patches

- **File**: `patches-X.X.X.rvp`
- **Download**: [ReVanced Patches Releases](https://github.com/ReVanced/revanced-patches/releases)
- **Rename to**: `patches-5.50.2.rvp` (or update script filenames)

#### 3. Base APK Files

**YouTube**:

- **File**: `youtube-20.14.43.apk`
- **Download**: [APKMirror - YouTube](https://www.apkmirror.com/apk/google-inc/youtube/)
- **Version**: 20.14.43 (or check ReVanced compatibility)

**Google Photos**:

- **File**: `google-photos-7.55.0.apk`
- **Download**: [APKMirror - Google Photos](https://www.apkmirror.com/apk/google-inc/photos/)
- **Version**: 7.55.0 (or check ReVanced compatibility)

> **Note**: Always check the [ReVanced Patches compatibility](https://github.com/ReVanced/revanced-patches#-list-of-patches) for the latest supported versions.

---

## 🚀 Quick Start

### 1. Setup

1. **Download this repository** (Clone or download ZIP)
2. **Download required files** (see Prerequisites above)
3. **Place all files** in the same folder:
   ```
   📁 Revanced apk maker/
   ├── 📄 revanced-cli-5.0.1-all.jar
   ├── 📄 patches-5.50.2.rvp
   ├── 📄 youtube-20.14.43.apk
   ├── 📄 google-photos-7.55.0.apk
   ├── 📜 patch-youtube.bat
   ├── 📜 patch-youtube-custom.ps1
   └── 📜 patch-google-photos.bat
   ```

### 2. Patch YouTube

**Option A: Recommended Patches (Quick)**

```powershell
.\patch-youtube.bat
```

**Option B: Custom Patch Selection (Interactive)**

```powershell
.\patch-youtube-custom.ps1
```

This will ask you about each patch (Y/N):

- ✅ Video ads removal
- ✅ SponsorBlock
- ✅ Background playback
- ✅ Return YouTube Dislike
- ✅ AMOLED theme
- ✅ And 15+ more patches!

### 3. Patch Google Photos

```powershell
.\patch-google-photos.bat
```

Includes:

- 📸 Unlimited storage (spoofs Pixel features)
- 📁 DCIM folder backup control

### 4. Install on Android

#### For YouTube:

1. **Install MicroG first** (required for login):
   - Download: [ReVanced GmsCore Releases](https://github.com/ReVanced/GmsCore/releases)
   - Install `app-release.apk` on your device
2. **Install patched YouTube**:
   - Transfer `youtube-revanced.apk` (or `youtube-revanced-custom.apk`) to your device
   - Install it
3. **Uninstall official YouTube** if you get package conflicts

#### For Google Photos:

1. **Uninstall official Google Photos** (if installed)
2. **Install patched version**:
   - Transfer `google-photos-revanced.apk` to your device
   - Install it

---

## 📦 Available Patches

### YouTube Patches (Recommended Preset)

| Patch                     | Description                           |
| ------------------------- | ------------------------------------- |
| 🚫 Video ads              | Remove all video advertisements       |
| ⏭️ SponsorBlock           | Skip sponsored segments automatically |
| 🎵 Background playback    | Play videos with screen off           |
| 👍 Return YouTube Dislike | Show dislike counts                   |
| 👆 Swipe controls         | Volume/brightness gestures            |
| 📊 Seekbar                | Enhanced seekbar with thumbnails      |
| 🎨 Theme                  | AMOLED dark theme                     |
| 🎬 Video quality          | Set default video quality             |
| ⚡ Playback speed         | Custom playback speeds                |
| 🧩 Hide layout components | Customize UI elements                 |

### YouTube Patches (Additional - Custom Script)

| Patch                            | Description                       |
| -------------------------------- | --------------------------------- |
| 🎯 Navigation buttons            | Customize bottom navigation       |
| 🎨 Custom branding               | Change app icon and name          |
| 📱 Miniplayer                    | Enhanced miniplayer controls      |
| 🎬 Hide Shorts components        | Remove Shorts UI elements         |
| 📺 Open Shorts in regular player | Watch Shorts like normal videos   |
| 💾 Downloads                     | Enable video downloads            |
| 📝 Disable auto captions         | Turn off automatic captions       |
| 🔗 Sanitize sharing links        | Remove tracking from shared links |
| 🕰️ Spoof app version             | Access older UI features          |

### Google Photos Patches

| Patch                  | Description                        |
| ---------------------- | ---------------------------------- |
| ☁️ Spoof features      | Unlimited storage (Pixel features) |
| 📁 DCIM backup control | Control which folders to backup    |
| 🔐 GmsCore support     | Enable MicroG compatibility        |

---

## 🔧 Troubleshooting

### "Java is not recognized"

**Solution**:

1. Install Java 17+ from [Adoptium](https://adoptium.net/)
2. Restart PowerShell/Command Prompt
3. Verify: `java -version`

### "Package conflict" or "App not installed"

**Solution**:

1. Uninstall the official app first
2. Then install the patched version
3. For YouTube: Make sure MicroG is installed first

### "Patching failed" or errors during patching

**Solution**:

1. Check you have the correct APK version (see compatibility list)
2. Ensure all files are in the same folder
3. Try downloading fresh APK files from APKMirror
4. Check [ReVanced Patches Issues](https://github.com/ReVanced/revanced-patches/issues)

### YouTube won't login

**Solution**:

1. Install [ReVanced GmsCore (MicroG)](https://github.com/ReVanced/GmsCore/releases)
2. Make sure GmsCore support patch is enabled (it's automatic)
3. Clear YouTube app data and try again

### Script execution policy error (PowerShell)

**Solution**:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 🔄 Updating Components

### Updating ReVanced CLI and Patches

1. Download latest versions:
   - [ReVanced CLI](https://github.com/ReVanced/revanced-cli/releases)
   - [ReVanced Patches](https://github.com/ReVanced/revanced-patches/releases)
2. Replace old files with new ones
3. Update filenames in scripts if version numbers changed

### Updating Base APKs

1. Check [ReVanced Patches compatibility](https://github.com/ReVanced/revanced-patches#-list-of-patches)
2. Download compatible versions from [APKMirror](https://www.apkmirror.com/)
3. Replace old APK files

---

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Note**: This repository is only for wrapper scripts. For patch contributions, please contribute to the official [ReVanced Patches](https://github.com/ReVanced/revanced-patches) repository.

---

## 📄 License

This project (wrapper scripts only) is licensed under the MIT License - see [LICENSE](LICENSE) file.

**Important**: The ReVanced CLI and patches have their own licenses (GPL-3.0). See [CREDITS.md](CREDITS.md) for details.

---

## 🙏 Credits

This project is built on the amazing work of the **ReVanced Team**. See [CREDITS.md](CREDITS.md) for full attribution.

### Official ReVanced Resources

- 🌐 **Website**: [revanced.app](https://revanced.app)
- 💬 **Discord**: [ReVanced Discord](https://revanced.app/discord)
- 📚 **Documentation**: [ReVanced Docs](https://github.com/ReVanced/revanced-documentation)
- 🐙 **GitHub**: [ReVanced Organization](https://github.com/ReVanced)

---

## ⚖️ Disclaimer

- This project is **not affiliated with or endorsed by** ReVanced, Google, or YouTube
- Use at your own risk
- Patching apps may violate Terms of Service
- For educational purposes only
- The scripts are provided "as-is" without warranty

---

## 📞 Support

- **Script Issues**: [Open an issue](../../issues) in this repository
- **Patch Issues**: Report to [ReVanced Patches Issues](https://github.com/ReVanced/revanced-patches/issues)
- **General Help**: [ReVanced Discord](https://revanced.app/discord)

---

Made with ❤️ by the community, powered by [ReVanced](https://revanced.app)
