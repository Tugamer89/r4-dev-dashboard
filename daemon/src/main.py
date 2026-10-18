import asyncio
import importlib.metadata
import json

import psutil


async def monitor_system() -> None:
    while True:
        cpu_percent = psutil.cpu_percent(interval=None)
        memory = psutil.virtual_memory()

        payload = {"mode": "idle", "cpu": cpu_percent, "ram": memory.percent}

        print(f"Telemetry payload: {json.dumps(payload)}")
        # TODO: Send via WebSockets to Arduino R4

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
    await monitor_system()


if __name__ == "__main__":
    asyncio.run(main())
