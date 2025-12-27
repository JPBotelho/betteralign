#!/usr/bin/env python3
import subprocess
import sys
from datetime import datetime, timedelta, UTC

# --- Helper functions ---
def run(cmd, cwd=None):
    """Run a shell command and return stdout as string."""
    return subprocess.check_output(cmd, shell=True, text=True, cwd=cwd).strip()

def get_current_branch(repo_path=None):
    """Return the current branch name."""
    return run("git rev-parse --abbrev-ref HEAD", cwd=repo_path)

def git_latest_commit_before(date_str, branch, repo_path=None):
    """Return the latest commit SHA before a given date."""
    cmd = f'git rev-list -n 1 --before="{date_str}" {branch}'
    return run(cmd, cwd=repo_path)

def git_first_commit_date(branch, repo_path=None):
    """Return the first commit date as YYYY-MM."""
    result = run(f'git log --reverse --format=%ad --date=short {branch} | head -1', cwd=repo_path)
    return result[:7]  # YYYY-MM

def add_month(year: int, month: int):
    """Increment year/month by one month."""
    month += 1
    if month > 12:
        month = 1
        year += 1
    return year, month

# --- Parse optional repository path ---
repo_path = sys.argv[1] if len(sys.argv) > 1 else None

# --- Main script ---
branch = get_current_branch(repo_path)
#print(f"Current branch detected: {branch}")

first_month_str = git_first_commit_date(branch, repo_path)
year, month = map(int, first_month_str.split("-"))

# Last fully completed month
today = datetime.now(UTC)

while (year, month) <= (today.year, today.month):
    date_str = f"{year:04d}-{month:02d}-01 00:01"
    sha = git_latest_commit_before(date_str, branch, repo_path)
    if sha:
        print(f"{year:04d}-{month:02d}-01 {sha}")

    year, month = add_month(year, month)

# Latest commit
latest_sha = run(f"git rev-parse HEAD", cwd=repo_path)
print(f"{today.year:04d}-{today.month:02d}-{today.day:02d} {latest_sha}")
