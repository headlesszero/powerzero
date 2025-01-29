#!/bin/bash

# Ensure the script runs from the project root
if [ "$(basename $(pwd))" != "powerzero" ]; then
    echo "Error: This script must be run from the project root /powerzero."
    exit 1
fi

clear

# Ensure at least one parameter is provided
if [ -z "$1" ]; then
    echo -e "\033[1;34mUsage:\033[0m tools/venv.sh <action> [environment]"
    echo ""
    echo -e "\033[1;33mThis is the virtual environment for your DEV MACHINE, not the Pi.\033[0m"    
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
ACTION="$1"                      # First parameter: action
ENVIRONMENT="${2:-prod}"         # Second parameter: environment (default: prod)
SCRIPT_DIR="./tools/_venv_scripts"

# Validate the action script
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

# If activating, ensure it happens automatically
if [[ "$ACTION" == "start" ]]; then
    VENV_PATH=".venv/bin/activate"

    if [ ! -f "$VENV_PATH" ]; then
        echo "Error: Virtual environment not found. Run 'tools/venv.sh install' first."
        exit 1
    fi

    # Detect user shell and activate the environment automatically
    case "$SHELL" in
        */bash)  exec bash --rcfile <(echo "source $VENV_PATH; exec bash") ;;
        */zsh)   exec zsh -i -c "source $VENV_PATH && exec zsh" ;;
        */fish)  exec fish -c "source $VENV_PATH.fish; exec fish" ;;
        *)       echo "Virtual environment created. Please restart your shell." ;;
    esac
fi