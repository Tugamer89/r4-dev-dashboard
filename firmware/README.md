# Firmware (Arduino Uno R4 WiFi)

## Architecture

The firmware strictly follows a non-blocking architecture using `millis()`. `delay()` is NEVER used. The logic is governed by an enum-based state machine designed to cleanly accommodate future expansions (e.g., physical hardware buttons).

Core states include:

* `MODE_IDLE`: Default standby or standard dashboard mode.
* `MODE_BUILD`: Indicates an active local or remote build process.
* `MODE_CICD`: Displays continuous integration/continuous deployment statuses.

## Tooling & Flashing

* **PlatformIO**: Manages the build environment via `platformio.ini`.
* **Make**: Always use the commands in the root `Makefile` to trigger builds and uploads rather than invoking PlatformIO directly.
* **Linting**: C++ code must be formatted with `clang-format`.

## WSL Specifics

If you are developing inside WSL, use `usbipd` to attach the Arduino COM port to your Linux distribution before uploading the compiled firmware.
