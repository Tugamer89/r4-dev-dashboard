"""Hardware telemetry extraction module."""

import subprocess
import sys
import time

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


BUILD_PROCESS_NAMES = {
    "make",
    "cmake",
    "ninja",
    "gcc",
    "g++",
    "clang",
    "clang++",
    "cargo",
    "rustc",
    "go",
    "msbuild",
    "dotnet",
    "javac",
    "mvn",
    "gradle",
    "tsc",
    "webpack",
    "vite",
    "rollup",
    "esbuild",
}

BLACKLIST_PROCESS_NAMES = {
    "GCC.exe",
}

_last_build_check_time = 0.0
_is_building_cache = False


def check_wsl_builds() -> bool:
    """Check if build processes are running inside WSL (Windows only)."""
    if sys.platform != "win32":
        return False

    try:
        # Prevent CMD console windows from flashing on Windows
        creation_flags = getattr(subprocess, "CREATE_NO_WINDOW", 0x08000000)

        # Ensure WSL is actually running to avoid booting the VM
        list_res = subprocess.run(
            ["wsl.exe", "-l", "--running", "-q"],
            capture_output=True,
            text=True,
            creationflags=creation_flags,
        )

        # wsl.exe outputs in UTF-16LE. If no distros are running, output is empty.
        if not any(c.isalnum() for c in list_res.stdout.replace("\x00", "")):
            return False

        # -e: all processes, -o comm=: output only command names (no headers)
        ps_res = subprocess.run(
            ["wsl.exe", "-e", "ps", "-e", "-o", "comm="],
            capture_output=True,
            text=True,
            timeout=0.5,
            creationflags=creation_flags,
        )

        if ps_res.returncode == 0:
            # Strip formatting to match securely against our set of build tools
            wsl_processes = {
                line.replace("\x00", "").strip().lower() for line in ps_res.stdout.splitlines()
            }
            return bool(wsl_processes.intersection(BUILD_PROCESS_NAMES))

    except Exception:
        # Fail gracefully
        pass

    return False


def is_build_running() -> bool:
    """Check if a common build process is currently running. Caches result for 1 second."""
    global _last_build_check_time, _is_building_cache
    current_time = time.time()

    # Throttle the process iteration to once per second
    if current_time - _last_build_check_time < 1.0:
        return _is_building_cache

    _last_build_check_time = current_time

    try:
        # Iterate over all running processes
        for proc in psutil.process_iter(["name"]):
            name = proc.info.get("name")
            if name and name not in BLACKLIST_PROCESS_NAMES:
                # Strip file extensions for Windows compatibility
                base_name = name.lower().split(".exe")[0]
                if base_name in BUILD_PROCESS_NAMES:
                    print(name)
                    _is_building_cache = True
                    return True
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        # Ignore processes that terminate or deny access during iteration
        pass

    # Fallback to check WSL
    if check_wsl_builds():
        _is_building_cache = True
        return True

    _is_building_cache = False
    return False
