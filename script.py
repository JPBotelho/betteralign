#!/usr/bin/env python3
import subprocess
import sys
from datetime import datetime, timedelta, UTC
import signal
import os
def run(cmd, cwd=None, time_cmd=False):
    if time_cmd:
        start = time.time()

    result = subprocess.run(
        cmd,
        shell=True,
        text=True,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    if time_cmd:
        elapsed = time.time() - start
        print(f"Completed in {elapsed:.2f} seconds: {cmd}")

    return result.stdout.strip(), result.stderr.strip()
def get_current_branch(repo_path=None):
    """Return the current branch name."""
    result, _ = run("git rev-parse --abbrev-ref HEAD", cwd=repo_path)
    return result

def git_latest_commit_before(date_str, branch, repo_path=None):
    """Return the latest commit SHA before a given date."""
    cmd = f'git rev-list -n 1 --before="{date_str}" {branch}'
    result, _ = run(cmd, cwd=repo_path)
    return result

def git_first_commit_date(branch, repo_path=None):
    """Return the first commit date as YYYY-MM."""
    result, _ = run(f'git log --reverse --format=%ad --date=short {branch} | head -1', cwd=repo_path)
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

def handle_sigint(signum, frame):
    run(f"git checkout {branch} && git pull", cwd=repo_path)    
    sys.exit(0)  # or perform cleanup

signal.signal(signal.SIGINT, handle_sigint)

year, month = 2020, 1
run(f"git checkout {branch} && git pull", cwd=repo_path)

# Last fully completed month
today = datetime.now(UTC)
folder_path = sys.argv[1].rstrip("/")  # remove trailing slash if any
bottom_level = folder_path.split("/")[-1]
#run(f"git checkout {branch}")
while (year, month) <= (today.year, today.month):
    date_str = f"{year:04d}-{month:02d}-01 00:01"
    sha = git_latest_commit_before(date_str, branch, repo_path)
    if sha:
        print(f"[{bottom_level}] Processing {year:04d}-{month:02d}-01 {sha}")
        run(f"git checkout {sha}", cwd=repo_path)
        short_sha = sha[:5]
        _, output = run(f"betteralign -repo {bottom_level}-{year:04d}-{month:02d}-01-{sha[:5]} ./...", cwd=repo_path, time_cmd=True)
        if not "analysis skipped" in output:
            with open(f"results/{bottom_level}-{year:04d}-{month:02d}-01-{sha[:5]}", "w") as f:
                f.write(output)
        run(f"git checkout {branch}", cwd=repo_path)

    year, month = add_month(year, month)

# Latest commit
latest_sha = run(f"git rev-parse HEAD", cwd=repo_path)
print(f"[{bottom_level}] Processing {today.year:04d}-{today.month:02d}-{today.day:02d} {latest_sha}")
_, output = run(f"betteralign -repo {today.year:04d}-{today.month:02d}-{today.day:02d}-{latest_sha[:5]} ./...", cwd=repo_path, time_cmd=True)
if not "analysis skipped" in output:
    with open(f"results/{bottom_level}-{year:04d}-{month:02d}-01-{sha[:5]}", "w") as f:
        f.write(output)
run(f"git checkout {branch}", cwd=repo_path)
#run(f"git checkout {latest_sha}", cwd=repo_path)
#run(f"betteralign ./... > {today.year:04d}-{today.month:02d}-{today.day:02d}-{latest_sha[:5]}.txt 2>&1", cwd=repo_path)
#run(f"git checkout {branch}", cwd=repo_path)