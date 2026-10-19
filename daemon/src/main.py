import asyncio
import importlib.metadata
import time

from config import load_config
from context_tracker import detect_active_repo
from github_monitor import get_latest_cicd_status
from server_ws import broadcast_payload, start_server
from system_monitor import get_cpu_load, get_gpu_load, get_ram_usage, is_build_running

# Global state for CI/CD
cicd_state = "unknown"
active_repo = None


async def monitor_github() -> None:
    """Continuously monitor GitHub CI/CD status based on configuration and context."""
    global cicd_state, active_repo

    while True:
        config = load_config()
        token = config.get("github_token", "")
        interval = config.get("polling_interval_sec", 15)

        target_repo = config.get("default_repo", "")

        # Dynamic tracking overrides the default repository if an IDE is found
        if config.get("dynamic_tracking", True):
            detected = await asyncio.to_thread(detect_active_repo)
            if detected:
                target_repo = detected

        if target_repo and target_repo != active_repo:
            print(f"Switching CI/CD monitoring context to: {target_repo}")
            active_repo = target_repo

        if active_repo and "/" in active_repo:
            owner, repo = active_repo.split("/")
            new_status = await asyncio.to_thread(get_latest_cicd_status, owner, repo, token)
            if new_status != "unknown":
                cicd_state = new_status
        else:
            cicd_state = "unknown"

        await asyncio.sleep(interval)


async def monitor_system() -> None:
    """Continuously monitor system metrics, evaluate priorities, and broadcast payload."""
    global cicd_state, active_repo
    last_cicd_state = "unknown"
    cicd_success_timestamp = 0.0

    while True:
        # Track when CI/CD successfully completes to show it temporarily
        if cicd_state != last_cicd_state:
            if cicd_state == "success":
                cicd_success_timestamp = time.time()
            last_cicd_state = cicd_state

        # State Machine Priority Logic
        current_mode = "idle"

        if is_build_running():
            current_mode = "build"
        else:
            if cicd_state == "in_progress":
                current_mode = "cicd"
            elif cicd_state == "failure":
                current_mode = "cicd"
            elif cicd_state == "success":
                # Display the success animation for 15 seconds, then return to idle
                if time.time() - cicd_success_timestamp < 15.0:
                    current_mode = "cicd"
                else:
                    current_mode = "idle"

        payload = {
            "mode": current_mode,
            "cicd_state": cicd_state,
            "active_repo": active_repo or "None",
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

    # Run the WebSocket server and monitoring tasks concurrently
    await asyncio.gather(start_server(), monitor_system(), monitor_github())


if __name__ == "__main__":
    asyncio.run(main())
