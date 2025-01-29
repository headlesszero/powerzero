#!/bin/bash

echo "Stopping the virtual environment..."

# Check if a virtual environment is active
if [ -n "$VIRTUAL_ENV" ]; then
    echo "Deactivating virtual environment..."
    deactivate
    echo "Virtual environment stopped."

    # Ensure we exit back to the original shell
    exec "$SHELL"
else
    echo "No active virtual environment to deactivate."
fi