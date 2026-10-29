<#
.SYNOPSIS
    One-click flashing script for SisterClock on ESP8266 D1 Mini.
.DESCRIPTION
    Flashes precompiled firmware.bin directly to your ESP8266 board via esptool.
.PARAMETER Port
    Serial COM port (e.g. COM3). If omitted, automatically detects connected COM port.
.PARAMETER Baud
    Flashing baud rate (default: 460800).
.PARAMETER Erase
    Erase entire flash memory before flashing.
#>
[CmdletBinding()]
param(
    [string]$Port = "",
    [int]$Baud = 460800,
    [string]$Python = "",
    [switch]$Erase
)

$ErrorActionPreference = "Stop"

Write-Host "==========================================================" -ForegroundColor Magenta
Write-Host "         SisterClock - ESP8266 One-Click Flasher          " -ForegroundColor Yellow
Write-Host "==========================================================" -ForegroundColor Magenta
Write-Host ""

# Verify firmware file exists
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$FirmwareBin = Join-Path $ScriptDir "dist\firmware.bin"

if (-not (Test-Path $FirmwareBin)) {
    Write-Host "[ERROR] Firmware binary not found at: $FirmwareBin" -ForegroundColor Red
    Write-Host "Please run 'pio run' first or check the dist folder." -ForegroundColor Yellow
    exit 1
}

$fwSize = (Get-Item $FirmwareBin).Length
Write-Host "[OK] Located firmware: $FirmwareBin ($([math]::Round($fwSize/1KB, 1)) KB)" -ForegroundColor Green

# Detect or validate COM port
if ([string]::IsNullOrWhiteSpace($Port)) {
    Write-Host "Searching for connected serial ports..." -ForegroundColor Cyan
    $availablePorts = @([System.IO.Ports.SerialPort]::GetPortNames() | Sort-Object -Unique)
    
    if ($availablePorts.Count -eq 0) {
        Write-Host "[ERROR] No serial COM ports detected!" -ForegroundColor Red
        Write-Host "Make sure your ESP8266 D1 Mini is plugged in via a USB data cable (with CH340 or CP2102 driver installed)." -ForegroundColor Yellow
        exit 1
    } elseif ($availablePorts.Count -eq 1) {
        $Port = $availablePorts[0]
        Write-Host "[OK] Automatically detected: $Port" -ForegroundColor Green
    } else {
        Write-Host "Multiple COM ports detected: $($availablePorts -join ', ')" -ForegroundColor Yellow
        Write-Host "Specify the clock port with -Port COMx and retry." -ForegroundColor Yellow
        exit 1
    }
} else {
    Write-Host "Using specified port: $Port" -ForegroundColor Cyan
}

# Locate an interpreter; -Python accepts a full path when Python is not on PATH.
if (-not $Python) {
    $candidates = @((Join-Path $env:USERPROFILE "anaconda3/python.exe"))
    $found = Get-Command python.exe -ErrorAction SilentlyContinue
    if ($found) { $candidates += $found.Source }
    foreach ($candidate in $candidates) {
        if (Test-Path $candidate) {
            & $candidate -m esptool version 2>$null | Out-Null
            if ($LASTEXITCODE -eq 0) { $Python = $candidate; break }
        }
    }
}
if (-not $Python -or -not (Test-Path $Python)) {
    Write-Host "[ERROR] Python with esptool not found. Install esptool and pass -Python with the interpreter path." -ForegroundColor Red
    exit 1
}
& $Python -m esptool version
if ($LASTEXITCODE -ne 0) { Write-Host "[ERROR] esptool is unavailable in $Python" -ForegroundColor Red; exit 1 }
    exit 1
}
& $Python -m esptool version
if ($LASTEXITCODE -ne 0) { Write-Host "[ERROR] esptool is unavailable in $Python" -ForegroundColor Red; exit 1 }

# Optional flash erase
if ($Erase) {
    Write-Host ""
    Write-Host "Erasing flash memory on $Port..." -ForegroundColor Yellow
    & $Python -m esptool --chip esp8266 --port $Port erase_flash
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] Flash erase failed." -ForegroundColor Red
        exit $LASTEXITCODE
    }
    Write-Host "[OK] Flash erased successfully." -ForegroundColor Green
}

# Flash firmware
Write-Host ""
Write-Host "Flashing SisterClock firmware to $Port at $Baud baud..." -ForegroundColor Magenta
& $Python -m esptool --chip esp8266 --port $Port --baud $Baud write_flash --flash_size detect 0x0 $FirmwareBin

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "[ERROR] Flashing failed!" -ForegroundColor Red
    Write-Host "Tips:" -ForegroundColor Yellow
    Write-Host "  1. Unplug and replug the USB cable." -ForegroundColor Yellow
    Write-Host "  2. Try a lower baud rate: .\flash.ps1 -Baud 115200" -ForegroundColor Yellow
    Write-Host "  3. Hold FLASH/BOOT button during plug-in if board does not auto-reset." -ForegroundColor Yellow
    exit $LASTEXITCODE
}

Write-Host ""
Write-Host "==========================================================" -ForegroundColor Green
Write-Host "            SisterClock Flashed Successfully!             " -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. The display will power on and show a pulsing heart <3." -ForegroundColor White
Write-Host "  2. Connect your phone or laptop to WiFi network:" -ForegroundColor White
Write-Host "       SSID:     SisterClock-Setup" -ForegroundColor Yellow
Write-Host "       Password: bestbrother" -ForegroundColor Yellow
Write-Host "  3. Open browser to: http://192.168.4.1 or http://sisterclock.local" -ForegroundColor White
Write-Host "  4. Set up your home WiFi & surprise your sister! <3" -ForegroundColor White
Write-Host ""
