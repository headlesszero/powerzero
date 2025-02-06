#!/bin/bash

# Exit immediately on error
set -e

# Define venv directory and requirements file
VENV_DIR="venv"
REQ_FILE="requirements.txt"

# Required system dependencies (space-separated list)
DEPS="python3-dev python3-pip libasound2-dev ffmpeg sox"

# Ensure the script is run from the correct directory
if [ "$(basename "$(pwd)")" != "hello_sound" ]; then
    echo "Error: This script must be run from the project root directory (hello_sound)."
    exit 1
fi

# **Check if already inside a virtual environment**
if [ -n "$VIRTUAL_ENV" ]; then
    echo "Error: You are already inside a virtual environment!"
    echo "Run 'deactivate' to exit the virtual environment before running this script."
    echo ""
    exit 1
fi


# Check and install missing system dependencies
MISSING=""
for pkg in $DEPS; do
    if ! dpkg -s "$pkg" &> /dev/null; then
        MISSING+="$pkg "
    fi
done

if [ -n "$MISSING" ]; then
    echo "Installing missing dependencies: $MISSING"
    sudo apt update && sudo apt install -y $MISSING
else
    echo "All required dependencies are already installed. Skipping."
fi

# Create the virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR" --system-site-packages
    echo "Virtual environment created at $VENV_DIR."
else
    echo "Virtual environment already exists. Skipping creation."
fi

# Activate the virtual environment
echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# Upgrade pip to avoid dependency issues
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies if requirements.txt exists
if [ -f "$REQ_FILE" ]; then
    echo "Installing dependencies from $REQ_FILE..."
    pip install -r "$REQ_FILE"
    echo "Dependencies installed."
else
    echo "No requirements.txt file found. Skipping dependency installation."
fi

echo "Virtual environment setup complete."