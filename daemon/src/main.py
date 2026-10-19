import asyncio
import importlib.metadata

from server_ws import broadcast_payload, start_server
from system_monitor import get_cpu_load, get_gpu_load, get_ram_usage


async def monitor_system() -> None:
    """Continuously monitor system metrics and broadcast them."""
    while True:
        payload = {
            "mode": "idle",
            "cpu": get_cpu_load(),
            "ram": get_ram_usage(),
            "gpu": get_gpu_load(),
        }
        broadcast_payload(payload)
        await asyncio.sleep(0.1)


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
