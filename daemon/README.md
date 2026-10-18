# Python System Daemon

## Overview

The daemon bridges OS metrics and development events to the Arduino R4 dashboard. It utilizes `psutil` to abstract OS-specific hardware calls securely and reliably.

## Tooling

* **Dependency Management**: `uv` is strictly used for managing the Python environment.
* **Linting**: Code quality and formatting are enforced with `ruff` via `pre-commit` hooks.

## Running the Daemon in WSL

**Crucial Note**: The `psutil` library reads the hardware of the environment it is executing in. If you run this daemon inside a WSL container, it will report the Linux virtual machine's metrics, not the physical Windows host. To monitor your actual hardware, run the daemon directly on the Windows host.
