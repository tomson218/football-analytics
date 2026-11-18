@echo off
chcp 65001 > nul
echo ========================================
echo Checking Docker environment...
echo ========================================

REM Check if Docker is installed
where docker >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Docker is not installed!
    echo Please download and install Docker Desktop from:
    echo https://www.docker.com/products/docker-desktop/
    pause
    exit /b 1
)

echo [+] Docker is installed.
echo Checking if Docker daemon is running...

REM Check if Docker daemon is running
docker info >nul 2>nul
if %errorlevel% neq 0 (
    echo [-] Docker Desktop is not running. Trying to start it...
    start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe"
    
    echo Waiting for Docker to start (this may take a moment)...
    :WAIT_LOOP
    docker info >nul 2>nul
    if %errorlevel% neq 0 (
        timeout /t 5 >nul
        goto WAIT_LOOP
    )
    echo [+] Docker has been successfully started!
) else (
    echo [+] Docker is already running.
)

echo ========================================
echo Starting containers (Docker Compose)...
echo ========================================
docker compose up --build

pause