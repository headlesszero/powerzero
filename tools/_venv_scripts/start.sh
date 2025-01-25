#!/bin/bash

VENV_DIR="venv"
REQ_DIR="requirements"
ENV="$1"  # Environment passed as a parameter (dev or prod)

echo -e "Starting virtual environment for environment: \033[1;33m$ENV\033[0m"

# Check if virtual environment exists
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv $VENV_DIR
else
    echo "Virtual environment already exists."
fi

# Activate the virtual environment
echo "Activating virtual environment..."
source $VENV_DIR/bin/activate
echo "Virtual environment started for $ENV."
