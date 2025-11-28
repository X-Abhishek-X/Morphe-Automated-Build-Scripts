@echo off
REM YouTube ReVanced Patcher - FINAL VERSION
REM Uses --exclusive flag to ensure ONLY selected patches are applied

echo ========================================
echo YouTube ReVanced Patcher
echo ========================================
echo.

cd /d "%~dp0"

if not exist "revanced-cli-5.0.1-all.jar" (
    echo ERROR: revanced-cli-5.0.1-all.jar not found!
    pause
    exit /b 1
)

if not exist "patches-5.46.0.rvp" (
    echo ERROR: patches-5.46.0.rvp not found!
    pause
    exit /b 1
)

if not exist "youtube-20.14.43.apk" (
    echo ERROR: youtube-20.14.43.apk not found!
    pause
    exit /b 1
)

echo All files found!
echo.
echo Patching with recommended settings...
echo This will take 5-10 minutes.
echo.

REM Use --exclusive flag to ONLY apply selected patches
java -jar revanced-cli-5.0.1-all.jar patch ^
    --exclusive ^
    -p patches-5.46.0.rvp ^
    -e "Video ads" ^
    -e "SponsorBlock" ^
    -e "Remove background playback restrictions" ^
    -e "Return YouTube Dislike" ^
    -e "Swipe controls" ^
    -e "Seekbar" ^
    -e "Theme" ^
    -e "Video quality" ^
    -e "Playback speed" ^
    -e "Hide layout components" ^
    -e "GmsCore support" ^
    -o youtube-revanced.apk ^
    youtube-20.14.43.apk

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo SUCCESS!
    echo ========================================
    echo.
    echo Patched APK: youtube-revanced.apk
    echo.
    echo IMPORTANT: Install MicroG first!
    echo Download from: https://github.com/ReVanced/GmsCore/releases
    echo.
) else (
    echo.
    echo PATCHING FAILED!
    echo Check errors above.
    echo.
)

pause
