#!/bin/bash

echo "Stopping the virtual environment..."

# Check if a virtual environment is active
if [ -n "$VIRTUAL_ENV" ]; then
    echo "Deactivating virtual environment..."
    deactivate
    echo "Virtual environment stopped."
else
    echo "No active virtual environment to deactivate."
fi
