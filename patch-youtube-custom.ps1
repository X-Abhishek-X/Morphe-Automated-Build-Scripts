# YouTube ReVanced - Custom Patch Selector (FINAL)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "YouTube Custom Patch Selector" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Set-Location -Path $PSScriptRoot

if (-not (Test-Path "revanced-cli-5.0.1-all.jar")) {
    Write-Host "ERROR: revanced-cli-5.0.1-all.jar not found!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

if (-not (Test-Path "patches-5.46.0.rvp")) {
    Write-Host "ERROR: patches-5.46.0.rvp not found!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

if (-not (Test-Path "youtube-20.14.43.apk")) {
    Write-Host "ERROR: youtube-20.14.43.apk not found!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Select patches (Y/N for each):" -ForegroundColor Yellow
Write-Host ""

$patches = @()

function Ask-Patch {
    param($num, $name, $desc)
    Write-Host "[$num/20] $name" -ForegroundColor Cyan
    Write-Host "    $desc" -ForegroundColor Gray
    $r = Read-Host "    Enable? (Y/N)"
    Write-Host ""
    return $r
}

if ((Ask-Patch 1 "Video ads" "Remove all ads") -eq "Y") { $patches += "Video ads" }
if ((Ask-Patch 2 "SponsorBlock" "Skip sponsored segments") -eq "Y") { $patches += "SponsorBlock" }
if ((Ask-Patch 3 "Remove background playback restrictions" "Play with screen off") -eq "Y") { $patches += "Remove background playback restrictions" }
if ((Ask-Patch 4 "Video quality" "Default video quality") -eq "Y") { $patches += "Video quality" }
if ((Ask-Patch 5 "Playback speed" "Custom speeds") -eq "Y") { $patches += "Playback speed" }
if ((Ask-Patch 6 "Theme" "AMOLED theme") -eq "Y") { $patches += "Theme" }
if ((Ask-Patch 7 "Hide layout components" "Hide UI elements") -eq "Y") { $patches += "Hide layout components" }
if ((Ask-Patch 8 "Navigation buttons" "Customize buttons") -eq "Y") { $patches += "Navigation buttons" }
if ((Ask-Patch 9 "Custom branding" "Change icon/name") -eq "Y") { $patches += "Custom branding" }
if ((Ask-Patch 10 "Return YouTube Dislike" "Show dislikes") -eq "Y") { $patches += "Return YouTube Dislike" }
if ((Ask-Patch 11 "Swipe controls" "Volume/brightness gestures") -eq "Y") { $patches += "Swipe controls" }
if ((Ask-Patch 12 "Seekbar" "Enhanced seekbar") -eq "Y") { $patches += "Seekbar" }
if ((Ask-Patch 13 "Miniplayer" "Customize miniplayer") -eq "Y") { $patches += "Miniplayer" }
if ((Ask-Patch 14 "Hide Shorts components" "Hide Shorts UI") -eq "Y") { $patches += "Hide Shorts components" }
if ((Ask-Patch 15 "Open Shorts in regular player" "Shorts in normal player") -eq "Y") { $patches += "Open Shorts in regular player" }
if ((Ask-Patch 16 "Downloads" "Video downloads") -eq "Y") { $patches += "Downloads" }
if ((Ask-Patch 17 "Disable auto captions" "No auto-captions") -eq "Y") { $patches += "Disable auto captions" }
if ((Ask-Patch 18 "Sanitize sharing links" "Remove tracking") -eq "Y") { $patches += "Sanitize sharing links" }
if ((Ask-Patch 19 "Spoof app version" "Old UI elements") -eq "Y") { $patches += "Spoof app version" }

Write-Host "[20/20] GmsCore support - REQUIRED" -ForegroundColor Green
$patches += "GmsCore support"
Write-Host ""

Write-Host "Selected $($patches.Count) patches" -ForegroundColor Green
Write-Host "Patching... (5-10 minutes)" -ForegroundColor Cyan
Write-Host ""

$cmd = "java -jar revanced-cli-5.0.1-all.jar patch --exclusive -p patches-5.46.0.rvp"
foreach ($p in $patches) { $cmd += " -e `"$p`"" }
$cmd += " -o youtube-revanced-custom.apk youtube-20.14.43.apk"

Invoke-Expression $cmd

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "SUCCESS!" -ForegroundColor Green
    Write-Host "File: youtube-revanced-custom.apk" -ForegroundColor White
    Write-Host ""
}
else {
    Write-Host ""
    Write-Host "FAILED!" -ForegroundColor Red
    Write-Host ""
}

Read-Host "Press Enter to exit"
