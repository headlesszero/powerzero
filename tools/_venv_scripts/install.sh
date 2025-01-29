#!/bin/bash

VENV_DIR=".venv"  # Keeping it hidden for neatness
REQ_DIR="requirements"
ENV="$1"  # Environment passed as a parameter (dev or prod)
REQ_FILE="$REQ_DIR/$ENV.txt"

echo -e "Preparing to install dependencies for environment: \033[1;33m$ENV\033[0m"

# Ensure an environment is specified
if [[ -z "$ENV" ]]; then
    echo -e "\033[1;31mError: No environment specified. Use 'dev' or 'prod'.\033[0m"
    exit 1
fi

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo -e "\033[1;31mError: Python3 is not installed.\033[0m"
    exit 1
fi

# Clean the virtual environment if it exists
if [ -d "$VENV_DIR" ]; then
    echo "Cleaning existing virtual environment..."
    rm -rf "$VENV_DIR"
    echo "Virtual environment removed."
fi

# Create a new virtual environment
echo "Creating new virtual environment..."
python3 -m venv "$VENV_DIR" || { echo "Error: Failed to create virtual environment."; exit 1; }

# Check if requirements file exists
if [ ! -f "$REQ_FILE" ]; then
    echo -e "\033[1;31mError: Requirements file not found: $REQ_FILE\033[0m"
    exit 1
fi

# Activate and install dependencies
echo "Activating virtual environment and installing dependencies..."
source "$VENV_DIR/bin/activate"
pip install --upgrade pip
pip install -r "$REQ_FILE"

echo -e "\033[1;32mDependencies installed for environment: $ENV.\033[0m"

# Ensure the user is placed inside the virtual environment
echo -e "\033[1;34mSwitching to virtual environment...\033[0m"

# Automatically switch the user's shell to the venv
case "$SHELL" in
    */bash)  exec bash --rcfile <(echo "source $VENV_DIR/bin/activate; exec bash") ;;
    */zsh)   exec zsh -i -c "source $VENV_DIR/bin/activate && exec zsh" ;;
    */fish)  exec fish -c "source $VENV_DIR/bin/activate; exec fish" ;;
    *)       echo -e "\033[1;33mVirtual environment created. Run: source $VENV_DIR/bin/activate\033[0m" ;;
esac