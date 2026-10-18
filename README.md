# R4 Dev Dashboard

A professional, desk-mounted hardware monitor based on the Arduino Uno R4 WiFi. It leverages the 12x8 LED matrix to provide continuous, non-intrusive visual feedback during development sessions.

## Architecture Overview

This repository is split into two isolated, highly cohesive modules:

1. **Firmware (`/firmware`)**: C++ logic running on the Arduino R4. It uses a non-blocking State Machine (`MODE_IDLE`, `MODE_BUILD`, `MODE_CICD`) to handle dynamic LED matrix animations based on WebSocket events.
2. **Daemon (`/daemon`)**: A cross-platform Python service running on the host machine. It gathers hardware telemetry via `psutil`, intercepts local build processes, and monitors CI/CD pipelines, streaming state changes to the Arduino.

## Quick Start

We use a unified `Makefile` to manage the lifecycle of both the daemon and the firmware.

```bash
# 1. Setup the Python virtual environment and pre-commit hooks
make setup

# 2. Build and upload the C++ firmware (requires PlatformIO)
make upload

# 3. Start the background Python daemon
make run-daemon
```

### WSL Development Note

If you are developing inside Windows Subsystem for Linux (WSL), the native USB ports are not directly accessible. Before running `make upload`, you must bridge the Arduino to your Linux VM.
Run the provided PowerShell script from your Windows host (outside of VS Code/WSL):
`.\scripts\windows\attach_arduino.ps1`

## Tooling

- **Dependency Management:** `uv` for Python, `PlatformIO` for C++.
- **Code Quality:** `pre-commit` enforces `clang-format` (C++) and `ruff` (Python) rules locally. GitHub Actions validate these rules on every push.
