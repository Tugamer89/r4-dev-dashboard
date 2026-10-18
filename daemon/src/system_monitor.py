"""Hardware telemetry extraction module."""

import psutil


def get_cpu_load() -> float:
    """Return the current CPU load percentage."""
    return psutil.cpu_percent(interval=None)


def get_ram_usage() -> float:
    """Return the current RAM usage percentage."""
    return psutil.virtual_memory().percent
