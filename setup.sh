#!/bin/bash
# Setup script for hailo-agent
# Creates resources symlink and installs the package

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RESOURCES_TARGET="/usr/local/hailo/resources"

echo "=== hailo-agent Setup ==="
echo

# Create resources symlink
if [ -L "$SCRIPT_DIR/resources" ]; then
    echo "✓ Resources symlink already exists"
elif [ -e "$SCRIPT_DIR/resources" ]; then
    echo "⚠ Warning: 'resources' exists but is not a symlink"
    echo "  Please remove it manually if you want to create the symlink"
else
    if [ -d "$RESOURCES_TARGET" ]; then
        ln -s "$RESOURCES_TARGET" "$SCRIPT_DIR/resources"
        echo "✓ Created resources symlink -> $RESOURCES_TARGET"
    else
        echo "⚠ Warning: $RESOURCES_TARGET does not exist"
        echo "  Make sure Hailo resources are installed first"
    fi
fi

# Create/activate virtual environment
if [ -d "$SCRIPT_DIR/venv" ]; then
    echo "✓ Virtual environment exists"
else
    echo "Creating virtual environment..."
    python3 -m venv "$SCRIPT_DIR/venv"
    echo "✓ Created virtual environment"
fi

# Activate and install
echo
echo "Installing hailo-agent..."
source "$SCRIPT_DIR/venv/bin/activate"
pip install -e "$SCRIPT_DIR" --quiet

echo
echo "=== Setup Complete ==="
echo
echo "To activate the environment:"
echo "  source venv/bin/activate"
echo
echo "To run the agent:"
echo "  python -m hailo_agent.agent --tool math"
echo
echo "Available models in resources/models/hailo10h/:"
if [ -d "$SCRIPT_DIR/resources/models/hailo10h" ]; then
    ls "$SCRIPT_DIR/resources/models/hailo10h/"*.hef 2>/dev/null | xargs -n1 basename | sed 's/.hef$//' | head -10
else
    echo "  (resources not linked)"
fi
