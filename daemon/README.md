# R4 Dev Dashboard - Daemon

A background service responsible for orchestrating data flow to the Arduino R4.

## Features

- **Hardware Telemetry**: Monitors CPU and RAM usage via `psutil`.
- **WebSocket Server**: Streams JSON payloads to the Arduino asynchronously.

## OS Context Warning

When running this daemon inside WSL (Windows Subsystem for Linux), `psutil` will report the metrics of the Linux Virtual Machine, not the Windows host. For accurate host telemetry, run this daemon natively on Windows.
