Write-Host "Searching for Arduino Uno R4 and bridging to WSL..." -ForegroundColor Cyan

# Find the string corresponding to the Arduino device
$usb_list = usbipd list
$target = $usb_list | Select-String -Pattern "Arduino|USB Serial Device" -SimpleMatch

if ($target) {
    # Extract the BUSID (e.g., "2-1") from the first column
    $busid = ($target -split '\s+')[0]

    Write-Host "Device found at BUSID: $busid" -ForegroundColor Green

    # Bind the device to usbipd (requires admin privileges on first run)
    Write-Host "Binding device to usbipd..."
    usbipd bind --busid $busid

    # Attach to the WSL instance
    Write-Host "Attaching device to WSL..."
    usbipd attach --wsl --busid $busid

    Write-Host "Success! You can now run 'make upload' from VS Code inside WSL." -ForegroundColor Green
} else {
    Write-Host "No Arduino found. Please ensure it is connected to the PC." -ForegroundColor Red
}

Write-Host "Press any key to exit..."
$Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
