#!/bin/bash

# Detect if the script is running from the root folder
if [ "$(basename $(pwd))" != "powerzero" ]; then
    echo "Error: This script must be run from the project root /powerzero."
    exit 1
fi

clear

# Ensure the script takes at least one parameter
if [ -z "$1" ]; then
    echo "Usage: ./tools/venv.sh <action> [environment]"
    echo ""
    echo "Actions:"
    echo "  start      Create and activate the virtual environment"
    echo "  stop       Deactivate the virtual environment"
    echo "  clean      Remove the virtual environment"
    echo "  install    Install dependencies"
    echo ""
    echo "Environments:"
    echo "  dev        Development environment"
    echo "  prod       Production environment (default)"
    echo 
    exit 1
fi

# Parameters
ACTION="$1"                      # First parameter: the venv action
ENVIRONMENT="${2:-prod}"         # Second parameter: the environment (default to prod)
SCRIPT_DIR="./tools/_venv_scripts"

# Validate the action and corresponding script
if [ ! -f "$SCRIPT_DIR/$ACTION.sh" ]; then
    echo "Error: No script found for action '$ACTION' in $SCRIPT_DIR."
    exit 1
fi

# Validate the environment
if [[ "$ENVIRONMENT" != "dev" && "$ENVIRONMENT" != "prod" ]]; then
    echo "Error: Invalid environment specified. Use 'dev' or 'prod'."
    exit 1
fi

# Execute the corresponding script
"$SCRIPT_DIR/$ACTION.sh" "$ENVIRONMENT"