@echo off
REM YouTube ReVanced Patcher
REM Uses --include flag to apply ONLY selected patches

echo ========================================
echo YouTube ReVanced Patcher
echo ========================================
echo.

cd /d "%~dp0"

if not exist "revanced-cli-6.0.0-all.jar" (
    echo ERROR: revanced-cli-6.0.0-all.jar not found!
    echo Download from: https://github.com/ReVanced/revanced-cli/releases
    pause
    exit /b 1
)

if not exist "patches-5.48.0.rvp" (
    echo ERROR: patches-5.48.0.rvp not found!
    echo Download from: https://github.com/ReVanced/revanced-patches/releases
    pause
    exit /b 1
)

if not exist "youtube-20.14.43.apk" (
    echo ERROR: youtube-20.14.43.apk not found!
    echo Download from: https://www.apkmirror.com/apk/google-inc/youtube/
    echo Version: 20.14.43
    pause
    exit /b 1
)

echo All files found!
echo.
echo Patching with recommended settings...
echo This will take 5-10 minutes.
echo.

java -jar revanced-cli-6.0.0-all.jar patch ^
    --patch-bundle patches-5.48.0.rvp ^
    --include "Video ads" ^
    --include "SponsorBlock" ^
    --include "Remove background playback restrictions" ^
    --include "Return YouTube Dislike" ^
    --include "Swipe controls" ^
    --include "Seekbar" ^
    --include "Theme" ^
    --include "Video quality" ^
    --include "Playback speed" ^
    --include "Hide layout components" ^
    --include "GmsCore support" ^
    --out youtube-revanced.apk ^
    youtube-20.14.43.apk

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo SUCCESS!
    echo ========================================
    echo.
    echo Patched APK: youtube-revanced.apk
    echo.
    echo IMPORTANT: Install GmsCore (MicroG) first!
    echo Download from: https://github.com/ReVanced/GmsCore/releases
    echo.
) else (
    echo.
    echo PATCHING FAILED!
    echo Check errors above.
    echo.
)

pause
