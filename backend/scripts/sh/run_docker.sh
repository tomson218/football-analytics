#!/bin/bash

echo "========================================"
echo "Checking Docker environment..."
echo "========================================"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "[ERROR] Docker is not installed on the system!"
    echo "Please install Docker following the official instructions:"
    echo "https://docs.docker.com/engine/install/"
    exit 1
fi

echo "[+] Docker is installed."
echo "Checking if Docker daemon is running..."

# Check if Docker daemon is responding
if ! docker info &> /dev/null; then
    echo "[-] Docker is not running. Trying to start..."
    
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo systemctl start docker
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        open -a Docker
    fi

    echo "Waiting for Docker to start..."
    until docker info &> /dev/null; do
        sleep 3
    done
    echo "[+] Docker has been started!"
else
    echo "[+] Docker is already running."
fi

echo "========================================"
echo "Starting containers (Docker Compose)..."
echo "========================================"
docker compose up --build