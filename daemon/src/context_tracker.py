"""Module to dynamically track the active developer context (IDE and Git repo)."""

import os
import subprocess
import sys
import urllib.parse

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


def _get_repo_from_wsl_unc_path(unc_path: str) -> str | None:
    """Extract repo using native WSL git if the path is a WSL UNC share."""
    parts = unc_path.replace("/", "\\").split("\\")

    if len(parts) >= 5 and parts[2].lower() in ("wsl.localhost", "wsl$"):
        distro = parts[3]
        wsl_path = "/" + "/".join(parts[4:])

        creation_flags = (
            getattr(subprocess, "CREATE_NO_WINDOW", 0x08000000) if os.name == "nt" else 0
        )

        git_cmd = [
            WSL_EXE,
            "-d",
            distro,
            "-e",
            "bash",
            "-c",
            f"cd '{wsl_path}' && git config --get remote.origin.url",
        ]

        try:
            res = subprocess.run(
                git_cmd, capture_output=True, text=True, creationflags=creation_flags
            )
            return _parse_github_url(res.stdout.strip())
        except Exception:
            pass
    return None


def _get_git_repo_from_dir(directory: str) -> str | None:
    """Run a git command in the target directory to extract the origin repository."""
    # Bypass dubious ownership and UNC restrictions for WSL network shares
    if directory.startswith(r"\\wsl.localhost") or directory.startswith(r"\\wsl$"):
        repo = _get_repo_from_wsl_unc_path(directory)
        if repo:
            return repo

    try:
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


def _get_wsl_active_repo() -> str | None:
    """Scan native WSL processes for any active git repository."""
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

        # Find all unique CWDs of running WSL processes that contain a .git directory
        bash_script = (
            "for p in /proc/[0-9]*; do "
            "cwd=$(readlink $p/cwd 2>/dev/null); "
            'if [[ -n "$cwd" && -d "$cwd/.git" ]]; then echo "$cwd"; fi; '
            "done | sort -u"
        )

        ps_res = subprocess.run(
            [WSL_EXE, "-e", "bash", "-c", bash_script],
            capture_output=True,
            text=True,
            creationflags=creation_flags,
        )

        for cwd in ps_res.stdout.splitlines():
            cwd = cwd.strip()
            if not cwd:
                continue

            git_cmd = [
                WSL_EXE,
                "-e",
                "bash",
                "-c",
                f"cd '{cwd}' && git config --get remote.origin.url",
            ]

            git_res = subprocess.run(
                git_cmd, capture_output=True, text=True, creationflags=creation_flags
            )

            repo = _parse_github_url(git_res.stdout.strip())
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

        # Decode URL encoded arguments
        decoded_arg = urllib.parse.unquote(arg)

        # Handle VS Code attached to WSL
        if "vscode-remote://wsl+" in decoded_arg:
            try:
                uri = decoded_arg.split("vscode-remote://wsl+")[1]
                uri = uri.split("?")[0].split("#")[0]
                distro = uri.split("/")[0]
                wsl_path = uri[len(distro) :]

                if wsl_path.endswith(".code-workspace"):
                    wsl_path = wsl_path.rsplit("/", 1)[0]

                # Query git natively inside WSL to bypass Windows UNC/dubious ownership locks
                creation_flags = (
                    getattr(subprocess, "CREATE_NO_WINDOW", 0x08000000) if os.name == "nt" else 0
                )

                git_cmd = [
                    WSL_EXE,
                    "-d",
                    distro,
                    "-e",
                    "bash",
                    "-c",
                    f"cd '{wsl_path}' && git config --get remote.origin.url",
                ]

                res = subprocess.run(
                    git_cmd, capture_output=True, text=True, creationflags=creation_flags
                )

                repo = _parse_github_url(res.stdout.strip())
                if repo:
                    return repo
            except Exception:
                pass

        # Handle standard Windows paths
        elif os.path.isdir(arg) or arg.endswith(".code-workspace"):
            try:
                check_dir = os.path.dirname(arg) if arg.endswith(".code-workspace") else arg
                if os.path.isdir(check_dir):
                    repo = _get_git_repo_from_dir(check_dir)
                    if repo:
                        return repo
            except Exception:
                pass

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
