#!/bin/bash

set -e

if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" ]]; then
    ACTIVATE_SCRIPT="venv\\Scripts\\activate"
    PYTHON_CHECK=where
else
    ACTIVATE_SCRIPT="venv/bin/activate"
    PYTHON_CHECK=command -v
fi

if $PYTHON_CHECK python3 &>/dev/null; then
    PYTHON=python3
elif $PYTHON_CHECK python &>/dev/null; then
    PYTHON=python
else
    echo "Python is not installed. Please install Python 3."
    exit 1
fi

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    $PYTHON -m venv venv
fi

echo "Activating virtual environment..."
source "$ACTIVATE_SCRIPT"

if [ -f "requirements.txt" ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

echo "Running main.py..."
$PYTHON main.py "$1" "$2"

echo "Deactivating virtual environment..."
deactivate