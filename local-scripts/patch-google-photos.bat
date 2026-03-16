@echo off
REM Google Photos ReVanced Patcher
REM Patches: Spoof features, DCIM backup control, GmsCore support, Change package name
REM Side-by-side: Installs alongside original Google Photos

echo ========================================
echo Google Photos ReVanced Patcher
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

if not exist "google-photos-7.60.0.apk" (
    echo ERROR: google-photos-7.60.0.apk not found!
    echo Download from: https://www.apkmirror.com/apk/google-inc/photos/
    echo Version: 7.60.0 arm64-v8a
    pause
    exit /b 1
)

echo All files found!
echo.
echo Patching with all 4 features...
echo   [+] Spoof features          (Pixel unlimited storage)
echo   [+] DCIM backup control     (per-folder backup)
echo   [+] GmsCore support         (sign-in without root)
echo   [+] Change package name     (side-by-side with original)
echo.
echo This will take 3-5 minutes.
echo.

java -jar revanced-cli-6.0.0-all.jar patch ^
    --patch-bundle patches-5.48.0.rvp ^
    --include "Spoof features" ^
    --include "Enable DCIM folders backup control" ^
    --include "GmsCore support" ^
    --include "Change package name" ^
    --out google-photos-revanced.apk ^
    google-photos-7.60.0.apk

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo SUCCESS!
    echo ========================================
    echo.
    echo Patched APK: google-photos-revanced.apk
    echo.
    echo SETUP:
    echo   1. Install ReVanced GmsCore on your phone first:
    echo      https://github.com/ReVanced/GmsCore/releases
    echo   2. Open GmsCore and add your Google account
    echo   3. Install google-photos-revanced.apk
    echo   4. Both original and ReVanced Photos will coexist
    echo.
) else (
    echo.
    echo PATCHING FAILED!
    echo Check errors above.
    echo.
)

pause
