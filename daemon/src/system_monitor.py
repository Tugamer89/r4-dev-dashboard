"""Hardware telemetry extraction module."""

import psutil

try:
    import GPUtil
except ImportError:
    GPUtil = None


def get_cpu_load() -> float:
    """Return the current CPU load percentage."""
    return psutil.cpu_percent(interval=None)


def get_ram_usage() -> float:
    """Return the current RAM usage percentage."""
    return psutil.virtual_memory().percent


def get_gpu_load() -> float:
    """Return the current GPU load percentage, if available."""
    if GPUtil is not None:
        gpus = GPUtil.getGPUs()
        if gpus:
            return gpus[-1].load * 100.0
    return 0.0
