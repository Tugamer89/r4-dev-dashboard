"""GitHub API interaction module to check CI/CD status."""

import json
import subprocess
import urllib.error
import urllib.request


def get_repo_info():
    """Extract the GitHub owner and repository name from the local git configuration."""
    try:
        res = subprocess.run(
            ["git", "config", "--get", "remote.origin.url"],
            capture_output=True,
            text=True,
            check=True,
        )
        url = res.stdout.strip()

        # Parse standard GitHub remote formats (HTTPS or SSH)
        if "github.com" not in url:
            return None, None

        parts = url.split("github.com")[-1]
        parts = parts.lstrip(":/")
        if parts.endswith(".git"):
            parts = parts[:-4]

        owner, repo = parts.split("/")[-2:]
        return owner, repo
    except Exception:
        return None, None


def get_latest_cicd_status(owner: str, repo: str, token: str = "") -> str:
    """
    Fetch the latest GitHub Actions workflow run status for the repository.
    Returns: 'in_progress', 'success', 'failure', or 'unknown'.
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/actions/runs?branch=main&per_page=5"

    req = urllib.request.Request(url)
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Accept", "application/vnd.github.v3+json")
    req.add_header("User-Agent", "r4-daemon")

    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            runs = data.get("workflow_runs", [])
            if not runs:
                return "unknown"

            # Group by head_sha to get all workflows triggered by the most recent push
            latest_sha = runs[0]["head_sha"]
            latest_runs = [r for r in runs if r["head_sha"] == latest_sha]

            statuses = [r["status"] for r in latest_runs]
            conclusions = [r["conclusion"] for r in latest_runs]

            # Evaluate aggregated status
            if "in_progress" in statuses or "queued" in statuses:
                return "in_progress"

            if (
                "failure" in conclusions
                or "timed_out" in conclusions
                or "action_required" in conclusions
            ):
                return "failure"

            if all(c in ["success", "skipped"] for c in conclusions if c):
                return "success"

            return "unknown"
    except urllib.error.HTTPError as e:
        if e.code == 403:
            print("GitHub API Rate Limit Exceeded. Please provide a token in ~/.r4-dashboard.json")
        return "unknown"
    except Exception as e:
        print(f"Failed to fetch GitHub status: {e}")
        return "unknown"
