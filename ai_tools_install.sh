#!/bin/bash
# Install Mangio-RVC-Fork in editable mode

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Installing Mangio-RVC-Fork in editable mode..."
cd "$SCRIPT_DIR"

if [[ -f "setup.py" ]] || [[ -f "pyproject.toml" ]]; then
    pip install -e .
else
    echo "Warning: No setup.py or pyproject.toml found in $SCRIPT_DIR"
    echo "Skipping installation for Mangio-RVC-Fork"
    exit 1
fi

echo "✓ Mangio-RVC-Fork installed successfully"
