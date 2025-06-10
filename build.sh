#!/bin/bash
echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Starting the application..."
uvicorn main:app --host 0.0.0.0 --port $PORT 