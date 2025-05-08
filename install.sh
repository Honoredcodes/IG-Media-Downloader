#!/bin/bash

if ! command -v python3 &> /dev/null
then
    echo "Python3 is not installed."
    echo "Please install it using your package manager or from https://www.python.org/downloads/"
    exit 1
fi

echo "Creating virtual environment..."
python3 -m venv venv

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing required packages..."
pip install \
    certifi==2025.4.26 \
    charset-normalizer==3.4.2 \
    idna==3.10 \
    instaloader==4.14.1 \
    requests==2.32.3 \
    urllib3==2.4.0

echo "Installation complete."
echo "Run: source venv/bin/activate && python3 program.py"