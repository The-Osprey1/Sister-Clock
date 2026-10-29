@echo off
setlocal
echo ==========================================================
echo          SisterClock - ESP8266 One-Click Flasher
echo ==========================================================
echo.

powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0flash.ps1" %*

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Flash script returned error code %ERRORLEVEL%.
    pause
    exit /b %ERRORLEVEL%
)

pause
