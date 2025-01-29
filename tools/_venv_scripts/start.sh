#!/bin/bash

VENV_DIR=".venv"  # Keeping it hidden for neatness
ENV="$1"  # Environment passed as a parameter (dev or prod)

echo -e "Starting virtual environment for environment: \033[1;33m$ENV\033[0m"

# Check if virtual environment exists, create it if missing
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
else
    echo "Virtual environment already exists."
fi

# Ensure activation script exists
if [ ! -f "$VENV_DIR/bin/activate" ]; then
    echo -e "\033[1;31mError: Virtual environment activation script not found.\033[0m"
    exit 1
fi

# Activate and persist in the user's shell
echo "Activating virtual environment..."
case "$SHELL" in
    */bash)  exec bash --rcfile <(echo "source $VENV_DIR/bin/activate; exec bash") ;;
    */zsh)   exec zsh -i -c "source $VENV_DIR/bin/activate && exec zsh" ;;
    */fish)  exec fish -c "source $VENV_DIR/bin/activate; exec fish" ;;
    *)       echo -e "\033[1;33mVirtual environment started. Run: source $VENV_DIR/bin/activate\033[0m" ;;
esac