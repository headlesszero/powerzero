#!/bin/bash

# Exit immediately on error
set -e

# Define venv directory
VENV_DIR="venv"

# Ensure the script is run from the correct directory
if [ "$(basename "$(pwd)")" != "proto" ]; then
    echo "Error: This script must be run from the project root directory (proto)."
    exit 1
fi

# Check if the venv exists
if [ -d "$VENV_DIR" ]; then
    echo "Activating virtual environment..."
    echo ""
    echo "Example: sudo venv/bin/python main.py"
    echo ""
    
    # Source the venv in the current shell
    exec bash --rcfile <(echo "source $VENV_DIR/bin/activate; exec bash")

else
    echo "Error: Virtual environment not found. Run './create_venv.sh' to create it."
    exit 1
fi
