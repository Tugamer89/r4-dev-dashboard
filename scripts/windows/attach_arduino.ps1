<#
.SYNOPSIS
Attaches an Arduino board or a USB serial device to WSL using usbipd-win.
#>

param(
    [string]$BusId = "",
    [string]$SearchPattern = "\(COM\d+\)|2341:|1a86:|10c4:|0403:|2e8a:|303a:|0483:|Arduino|CH340|CP210|FT232|RP2040|Pico|STM32|JLink|J-Link"
)

$ErrorActionPreference = "Continue"

# Check if user provided manual BUSID or search automatically
if ($BusId) {
    $targetBusId = $BusId
    Write-Host "Using manually specified BUSID: $targetBusId" -ForegroundColor Cyan
} else {
    Write-Host "Searching for connected USB serial devices via usbipd..."

    try {
        $usbipdOutput = usbipd list
    } catch {
        Write-Error "Failed to execute 'usbipd list'. Ensure usbipd-win is installed and added to Windows PATH."
        exit 1
    }

    $targetBusId = $null
    $targetDevice = $null

    foreach ($line in $usbipdOutput) {
        if ($line -match "(?i)($SearchPattern)") {
            if ($line -match "^\s*([\d]+-[\d]+)") {
                $targetBusId = $matches[1]
                $targetDevice = $line.Trim()
                break
            }
        }
    }

    if (-not $targetBusId) {
        Write-Host "No compatible USB serial device found. Current devices listed by usbipd:" -ForegroundColor Yellow
        $usbipdOutput | Write-Host
        Write-Host "`nDevice not automatically recognized." -ForegroundColor Red
        Write-Host "If your device is listed above, you can force the connection by specifying the BUSID." -ForegroundColor Cyan
        Write-Host "Example: .\attach_arduino.ps1 -BusId 8-3"
        exit 1
    }

    Write-Host "Device found:" -ForegroundColor Green
    Write-Host " -> $targetDevice"
    Write-Host " -> BUSID: $targetBusId"
}

# Binding device to usbipd (using --force to bypass USBPcap filter warnings)
Write-Host "`nExecuting 'usbipd bind' (may require Administrator privileges for initial bind)..."
usbipd bind --force --busid $targetBusId 2>$null

# Attaching device to WSL (usbipd v4+ requires --wsl flag)
Write-Host "Executing 'usbipd attach' to connect the board to WSL..."
Write-Host "NOTE: This window will stay open to auto-attach the board when it reboots during flashing. Press Ctrl+C to stop." -ForegroundColor Yellow
usbipd attach --wsl --auto-attach --busid $targetBusId

if ($LASTEXITCODE -eq 0 -or $?) {
    Write-Host "`nOperation completed successfully!" -ForegroundColor Green
    Write-Host "The board should now be accessible inside WSL (e.g., /dev/ttyACM0 or /dev/ttyUSB0)." -ForegroundColor Green
} else {
    Write-Host "`nError during attach." -ForegroundColor Red
    Write-Host "Ensure WSL is running. If the error persists, run PowerShell as Administrator and try again." -ForegroundColor Yellow
}
