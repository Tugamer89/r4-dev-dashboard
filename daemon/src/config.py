"""Configuration management for the R4 Dev Dashboard daemon."""

import json
from pathlib import Path

# Use the user's home directory for a global configuration file
CONFIG_PATH = Path.home() / ".r4-dashboard.json"

DEFAULT_CONFIG = {
    "github_token": "",
    "default_repo": "",  # Fallback repository e.g., "Tugamer89/r4-dev-dashboard"
    "dynamic_tracking": True,  # Enable scanning for active IDEs to switch context automatically
    "polling_interval_sec": 15,  # How often to check GitHub API
}


def load_config() -> dict:
    """Load configuration from the home directory, creating defaults if missing."""
    if not CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH, "w", encoding="utf-8") as f:
                json.dump(DEFAULT_CONFIG, f, indent=4)
        except Exception as e:
            print(f"Failed to create config file: {e}")
        return DEFAULT_CONFIG

    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            user_config = json.load(f)

            # Merge with default config to ensure all keys exist
            merged_config = DEFAULT_CONFIG.copy()
            merged_config.update(user_config)
            return merged_config
    except Exception as e:
        print(f"Error reading config file {CONFIG_PATH}: {e}")
        return DEFAULT_CONFIG
