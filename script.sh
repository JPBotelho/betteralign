#!/usr/bin/env bash

set -euo pipefail

if [ "$#" -ne 1 ]; then
  echo "Usage: myutil <git-repo-url>" >&2
  exit 1
fi

URL="$1"
REPO_NAME="$(basename "$URL" .git)"

# Create a temporary directory for the repo
TMPDIR="$(mktemp -d)"

# Ensure cleanup on exit
cleanup() {
  rm -rf "$TMPDIR"
}
trap cleanup EXIT

# Clone repo quietly into temporary directory
git clone "$URL" "$TMPDIR/$REPO_NAME" >/dev/null 2>&1

# Run betteralign inside the temporary directory and fix paths, then apply sed
(
  go clean -cache
  cd "$TMPDIR/$REPO_NAME"
  COMMIT_SHA=$(git rev-parse HEAD)
  betteralign -repo "$REPO_NAME" -commit "$COMMIT_SHA" ./... 2>&1 \
    | sed "s|^$TMPDIR||" \
    | sed -E 's#^([^[:space:]]+):[[:space:]]+\{#{"location":"\1",#' \
    | grep -E '^\{.*\}$'
)
