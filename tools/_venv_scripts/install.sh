#!/bin/bash

VENV_DIR="venv"
REQ_DIR="requirements"
ENV="$1"  # Environment passed as a parameter (dev or prod)
REQ_FILE="$REQ_DIR/$ENV.txt"

echo -e "Preparing to install dependencies for environment: \033[1;33m$ENV\033[0m"

# Clean the virtual environment if it exists
if [ -d "$VENV_DIR" ]; then
    echo "Cleaning existing virtual environment..."
    rm -rf $VENV_DIR
    echo "Virtual environment removed."
fi

# Create a new virtual environment
echo "Creating new virtual environment..."
python3 -m venv $VENV_DIR

# Activate the virtual environment
echo "Activating virtual environment..."
source $VENV_DIR/bin/activate

# Check if requirements file exists
if [ ! -f "$REQ_FILE" ]; then
    echo "Error: Requirements file not found: $REQ_FILE"
    exit 1
fi

# Install dependencies
echo "Installing dependencies from $REQ_FILE..."
pip install --upgrade pip
pip install -r $REQ_FILE
echo "Dependencies installed for environment: $ENV."