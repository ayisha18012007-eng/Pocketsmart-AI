#!/bin/bash

echo "Starting PocketSmart AI..."

if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

source .venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Starting server..."
uvicorn app.main:app --reload