import asyncio
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


async def main() -> None:
    print("Starting R4 Dev Dashboard Daemon...")
    await monitor_system()


if __name__ == "__main__":
    asyncio.run(main())
