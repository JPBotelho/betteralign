#!/usr/bin/env bash
set -e

# Directory to store binaries
BIN_DIR="$HOME/betteralign/bin"
mkdir -p "$BIN_DIR"

# Source directory is the directory of this script
SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SRC_DIR"

# Ensure gvm is installed
if ! command -v gvm &> /dev/null; then
    echo "gvm not found. Please install gvm first: https://github.com/moovweb/gvm"
    exit 1
fi

# Loop over Go versions 1.12 → 1.25
for VER in $(seq 12 25); do
    GO_VER="1.$VER"
    echo "============================="
    echo "Building BetterAlign with Go $GO_VER"
    
    # Install/use Go version if needed
    if ! gvm list | grep -q "go$GO_VER"; then
        echo "Installing Go $GO_VER..."
        gvm install "go$GO_VER"
    fi
    gvm use "go$GO_VER"

    # Build binary
    OUTPUT="$BIN_DIR/betteralign$GO_VER"
    go build -o "$OUTPUT" ./cmd/betteralign
    echo "Built $OUTPUT"
done

# Add BIN_DIR to PATH if not already
if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    echo "export PATH=\"$BIN_DIR:\$PATH\"" >> "$HOME/.bashrc"
    export PATH="$BIN_DIR:$PATH"
    echo "Added $BIN_DIR to PATH"
fi

echo "Done! Binaries available in $BIN_DIR"
