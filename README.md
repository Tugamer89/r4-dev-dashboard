# R4 Dev Dashboard

A developer dashboard based on the Arduino Uno R4 WiFi, designed for professional monitoring and CI/CD status display.

## Project Overview

* **/daemon/**: A cross-platform Python daemon utilizing `psutil` to extract and broadcast system and CI/CD metrics.
* **/firmware/**: C++ firmware for the Arduino Uno R4 WiFi, built on a robust, non-blocking state machine pattern.

## Guidelines & Core Principles

* **English Only**: ALL code, variables, comments, documentation, and commit messages MUST be in English. No exceptions.
* **Entry Point**: `Makefile` is the primary entry point for all operations (build, upload, run, lint).
* **CI/CD & Tooling**:
  * Python dependencies are managed via `uv`.
  * C++ dependencies and compilation are handled by `PlatformIO`.
  * Code quality is enforced via `pre-commit` hooks (`clang-format` for C++ and `ruff` for Python) and analyzed by `SonarCloud`.
  * Dependencies and GitHub Actions are continuously updated via `Dependabot`.

## Development Environment Setup

1. **VS Code Workspace**: Open the project using the Multi-root Workspace (`.code-workspace`) file. This is crucial for the PlatformIO extension to recognize the nested `/firmware` directory as a C++ project root and correctly resolve IntelliSense.
2. **WSL Development**:
    * **USB Bridging**: Flashing the Arduino from WSL requires `usbipd` to forward the COM port from the Windows host to Linux.
    * **Daemon Monitoring**: Note that running `psutil` inside WSL reads the VM's hardware, not the Windows host. Run the daemon on Windows directly to monitor the physical host.

## License

This project is licensed under the terms found in the `LICENSE` file. For contribution and behavioral guidelines, see `CONTRIBUTING.md` and `CODE_OF_CONDUCT.md`.
