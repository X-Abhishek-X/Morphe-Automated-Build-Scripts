@echo off
REM Google Photos ReVanced Patcher - FINAL VERSION

echo ========================================
echo Google Photos ReVanced Patcher
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

if not exist "google-photos-7.55.0.apk" (
    echo ERROR: google-photos-7.55.0.apk not found!
    pause
    exit /b 1
)

echo All files found!
echo.
echo Patching with all 3 features...
echo This will take 3-5 minutes.
echo.

java -jar revanced-cli-5.0.1-all.jar patch ^
    --exclusive ^
    -p patches-5.46.0.rvp ^
    -e "Spoof features" ^
    -e "Enable DCIM folders backup control" ^
    -e "GmsCore support" ^
    -o google-photos-revanced.apk ^
    google-photos-7.55.0.apk

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo SUCCESS!
    echo ========================================
    echo.
    echo Patched APK: google-photos-revanced.apk
    echo.
    echo Features: Unlimited storage + DCIM control
    echo.
) else (
    echo.
    echo PATCHING FAILED!
    echo Check errors above.
    echo.
)

pause
