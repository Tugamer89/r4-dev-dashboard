"""Module to dynamically track the active developer context (IDE and Git repo)."""

import os
import subprocess
import sys

import psutil

# Known IDE and text editor process names
TARGET_IDES = {"code", "idea64", "clion", "nvim", "vim", "devenv", "pycharm", "rider"}
GITHUB_URL = "github.com"
WSL_EXE = "wsl.exe"


def _parse_github_url(url: str) -> str | None:
    """Extract owner and repo from a GitHub remote URL."""
    if GITHUB_URL not in url:
        return None
    parts = url.split(GITHUB_URL)[-1].lstrip(":/")
    if parts.endswith(".git"):
        parts = parts[:-4]

    # Needs at least owner/repo
    split_parts = parts.split("/")
    if len(split_parts) < 2:
        return None

    owner, repo = split_parts[-2:]
    return f"{owner}/{repo}"


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
        return _parse_github_url(res.stdout.strip())
    except Exception:
        return None


def _check_wsl_process_for_repo(line: str, creation_flags: int) -> str | None:
    """Parse a WSL process line and attempt to extract its git repository."""
    parts = line.strip().split(maxsplit=1)
    if len(parts) != 2:
        return None

    comm, cwd = parts
    if comm.lower() not in TARGET_IDES:
        return None

    git_cmd = [
        WSL_EXE,
        "-e",
        "bash",
        "-c",
        f"cd '{cwd}' && git config --get remote.origin.url",
    ]

    try:
        git_res = subprocess.run(
            git_cmd, capture_output=True, text=True, creationflags=creation_flags
        )
        return _parse_github_url(git_res.stdout.strip())
    except Exception:
        return None


def _get_wsl_active_repo() -> str | None:
    """Scan native WSL processes for terminal editors (vim, nvim)."""
    if sys.platform != "win32":
        return None
    try:
        creation_flags = getattr(subprocess, "CREATE_NO_WINDOW", 0x08000000)
        # Check active WSL distros
        res = subprocess.run(
            [WSL_EXE, "-l", "--running", "-q"],
            capture_output=True,
            text=True,
            creationflags=creation_flags,
        )
        if not any(c.isalnum() for c in res.stdout.replace("\x00", "")):
            return None

        # Get command and CWD of all WSL processes
        ps_res = subprocess.run(
            [WSL_EXE, "-e", "ps", "-eo", "comm,cwd"],
            capture_output=True,
            text=True,
            creationflags=creation_flags,
        )
        for line in ps_res.stdout.replace("\x00", "").splitlines():
            repo = _check_wsl_process_for_repo(line, creation_flags)
            if repo:
                return repo
    except Exception:
        pass
    return None


def _extract_repo_from_cmdline(cmdline: list) -> str | None:
    """Scan command line arguments to detect active workspace paths."""
    for arg in cmdline:
        if not isinstance(arg, str):
            continue

        # Handle VS Code attached to WSL
        if "vscode-remote://wsl+" in arg:
            try:
                uri = arg.split("vscode-remote://wsl+")[1]
                distro = uri.split("/")[0]
                wsl_path = uri[len(distro) :]
                bs_char = "\\"
                unc_path = f"\\\\wsl.localhost\\{distro}{wsl_path.replace('/', bs_char)}"
                repo = _get_git_repo_from_dir(unc_path)
                if repo:
                    return repo
            except Exception:
                pass
        elif os.path.isdir(arg):
            repo = _get_git_repo_from_dir(arg)
            if repo:
                return repo
    return None


def _check_process_for_repo(proc: psutil.Process) -> str | None:
    """Inspect a single process to see if it represents an IDE in a git repository."""
    name = proc.info.get("name", "")
    if not name:
        return None

    base_name = name.lower().split(".exe")[0]
    if base_name not in TARGET_IDES:
        return None

    # Check command line arguments for paths
    cmdline = proc.info.get("cmdline", []) or []
    repo = _extract_repo_from_cmdline(cmdline)
    if repo:
        return repo

    # Fallback to the Current Working Directory of the IDE process
    cwd = proc.info.get("cwd", "")
    if cwd and os.path.isdir(cwd):
        return _get_git_repo_from_dir(cwd)

    return None


def detect_active_repo() -> str | None:
    """
    Scans running processes for recognized IDEs and attempts to extract
    the GitHub repository associated with their current workspace.
    """
    for proc in psutil.process_iter(["name", "cmdline", "cwd"]):
        try:
            repo = _check_process_for_repo(proc)
            if repo:
                return repo
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    # Check if a native terminal editor is running inside WSL
    return _get_wsl_active_repo()
