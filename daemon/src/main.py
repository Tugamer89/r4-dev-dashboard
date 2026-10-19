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


async def _resolve_target_repo(config: dict) -> str:
    """Determine the repository to track based on config or dynamic IDE detection."""
    target_repo = config.get("default_repo", "")
    if config.get("dynamic_tracking", True):
        detected = await asyncio.to_thread(detect_active_repo)
        if detected:
            target_repo = detected
    return target_repo


async def _fetch_and_update_cicd(target_repo: str, token: str) -> None:
    """Fetch the latest status from GitHub and update global state."""
    global cicd_state, active_repo

    if target_repo and target_repo != active_repo:
        print(f"Switching CI/CD monitoring context to: {target_repo}")
        active_repo = target_repo

    if not active_repo or "/" not in active_repo:
        cicd_state = "unknown"
        return

    owner, repo = active_repo.split("/")
    new_status = await asyncio.to_thread(get_latest_cicd_status, owner, repo, token)
    if new_status != "unknown":
        cicd_state = new_status


async def monitor_github() -> None:
    """Continuously monitor GitHub CI/CD status based on configuration and context."""
    while True:
        config = load_config()
        interval = config.get("polling_interval_sec", 15)
        token = config.get("github_token", "")

        target_repo = await _resolve_target_repo(config)
        await _fetch_and_update_cicd(target_repo, token)

        await asyncio.sleep(interval)


def _determine_system_mode(current_cicd: str, success_timestamp: float) -> str:
    """State machine priority logic to decide dashboard rendering mode."""
    if is_build_running():
        return "build"

    if current_cicd in ("in_progress", "failure"):
        return "cicd"

    if current_cicd == "success":
        # Display the success animation for 15 seconds, then return to idle
        if time.time() - success_timestamp < 15.0:
            return "cicd"

    return "idle"


async def monitor_system() -> None:
    """Continuously monitor system metrics, evaluate priorities, and broadcast payload."""
    global cicd_state
    last_cicd_state = "unknown"
    cicd_success_timestamp = 0.0

    while True:
        # Track when CI/CD successfully completes to show it temporarily
        if cicd_state != last_cicd_state:
            if cicd_state == "success":
                cicd_success_timestamp = time.time()
            last_cicd_state = cicd_state

        current_mode = _determine_system_mode(cicd_state, cicd_success_timestamp)

        payload = {
            "mode": current_mode,
            "cicd_state": cicd_state,
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
