#!/bin/bash

# Usage: cat repos.txt | ./download_repos.sh [target_directory]
# Each line should be a Git repo URL like: https://github.com/helm/helm

# Set target directory (default: current directory)
TARGET_DIR="${1:-.}"

# Create target directory if it doesn't exist
mkdir -p "$TARGET_DIR"

while IFS= read -r repo_url || [ -n "$repo_url" ]; do
    # Skip empty lines
    [[ -z "$repo_url" ]] && continue

    # Extract repo name, strip trailing .git if present
    repo_name=$(basename "$repo_url" .git)

    # Full path to where repo should be cloned
    repo_path="$TARGET_DIR/$repo_name"

    if [ -d "$repo_path" ]; then
        echo "Skipping '$repo_name', folder already exists in '$TARGET_DIR'."
    else
        echo "Cloning '$repo_name' into '$TARGET_DIR'..."
        git clone "$repo_url" "$repo_path"
    fi
done
