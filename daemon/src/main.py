import asyncio
import importlib.metadata
import json

import psutil

try:
    import GPUtil
except ImportError:
    GPUtil = None

from server_ws import broadcast_payload, start_server


async def monitor_system() -> None:
    """Continuously monitor system metrics and broadcast them."""
    while True:
        cpu_percent = psutil.cpu_percent(interval=None)
        memory = psutil.virtual_memory()

        gpu_percent = 0.0
        if GPUtil is not None:
            gpus = GPUtil.getGPUs()
            if gpus:
                gpu_percent = gpus[-1].load * 100.0

        payload = {"mode": "idle", "cpu": cpu_percent, "ram": memory.percent, "gpu": gpu_percent}

        print(f"Telemetry payload: {json.dumps(payload)}")
        broadcast_payload(payload)

        await asyncio.sleep(1)


def get_daemon_version() -> str:
    """Retrieve the installed package version dynamically."""
    try:
        return importlib.metadata.version("r4-daemon")
    except importlib.metadata.PackageNotFoundError:
        return "development"


async def main() -> None:
    version = get_daemon_version()
    print(f"Starting R4 Dev Dashboard Daemon v{version}...")

    # Run the WebSocket server and the monitoring task concurrently
    await asyncio.gather(start_server(), monitor_system())


if __name__ == "__main__":
    asyncio.run(main())
