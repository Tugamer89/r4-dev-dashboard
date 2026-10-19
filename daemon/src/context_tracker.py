"""Module to dynamically track the active developer context (IDE and Git repo)."""

import os
import subprocess

import psutil

# Known IDE and text editor process names
TARGET_IDES = {"code", "idea64", "clion", "nvim", "vim", "devenv", "pycharm", "rider"}


def _get_git_repo_from_dir(directory: str) -> str | None:
    """Run a git command in the target directory to extract the origin repository."""
    try:
        if not os.path.exists(os.path.join(directory, ".git")):
            return None

        creation_flags = (
            getattr(subprocess, "CREATE_NO_WINDOW", 0x08000000) if os.name == "nt" else 0
        )

        res = subprocess.run(
            ["git", "config", "--get", "remote.origin.url"],
            cwd=directory,
            capture_output=True,
            text=True,
            check=True,
            creationflags=creation_flags,
        )
        url = res.stdout.strip()

        # Parse standard GitHub remote formats
        if "github.com" not in url:
            return None

        parts = url.split("github.com")[-1]
        parts = parts.lstrip(":/")
        if parts.endswith(".git"):
            parts = parts[:-4]

        owner, repo = parts.split("/")[-2:]
        return f"{owner}/{repo}"
    except Exception:
        return None


def detect_active_repo() -> str | None:
    """
    Scans running processes for recognized IDEs and attempts to extract
    the GitHub repository associated with their current workspace.
    """
    for proc in psutil.process_iter(["name", "cmdline", "cwd"]):
        try:
            name = proc.info.get("name", "")
            if not name:
                continue

            base_name = name.lower().split(".exe")[0]
            if base_name in TARGET_IDES:
                # Check command line arguments (VS Code often passes workspace paths here)
                cmdline = proc.info.get("cmdline", []) or []
                for arg in cmdline:
                    if isinstance(arg, str) and os.path.isdir(arg):
                        repo = _get_git_repo_from_dir(arg)
                        if repo:
                            return repo

                # Fallback to the Current Working Directory of the IDE process
                cwd = proc.info.get("cwd", "")
                if cwd and os.path.isdir(cwd):
                    repo = _get_git_repo_from_dir(cwd)
                    if repo:
                        return repo

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    return None
