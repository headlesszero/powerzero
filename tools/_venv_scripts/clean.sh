#!/bin/bash

VENV_DIR="venv"

echo "Cleaning up the virtual environment..."

# Check if virtual environment exists
if [ -d "$VENV_DIR" ]; then
    echo "Removing virtual environment..."
    rm -rf $VENV_DIR
    echo "Virtual environment removed."
else
    echo "No virtual environment found to clean."
fi
