# R4 Dev Dashboard - Firmware

The C++ firmware for the Arduino Uno R4 WiFi.

## Architecture Notes

- **State Machine**: The core logic relies on an enum-based state machine defined in `StateMachine.h`.
- **Non-blocking Loop**: The `loop()` function strictly uses `millis()` for timing. The `delay()` function is forbidden to ensure the ESP32-S3 coprocessor can process incoming WebSocket payloads immediately.

## Build Instructions

Rely on the root Makefile or use PlatformIO directly:

```bash
pio run
pio run --target upload
```
