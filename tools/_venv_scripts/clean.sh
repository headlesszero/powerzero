#!/bin/bash

VENV_DIR=".venv"  # Keeping it hidden for consistency with other scripts

echo -e "\033[1;34mCleaning up the virtual environment...\033[0m"

# Check if virtual environment exists
if [ -d "$VENV_DIR" ]; then
    echo -e "\033[1;33mRemoving virtual environment...\033[0m"
    rm -rf "$VENV_DIR"
    echo -e "\033[1;32mVirtual environment removed successfully.\033[0m"
    exit 0
else
    echo -e "\033[1;33mNo virtual environment found to clean.\033[0m"
    exit 1
fi