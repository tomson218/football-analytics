@echo off
chcp 65001 > nul
echo ========================================
echo  Statistical Analysis — Stats + Charts
echo ========================================
echo.

REM Check for Python
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH!
    pause
    exit /b 1
)

echo [+] Python found.
echo.

REM Activate virtual environment if it exists
if exist venv\Scripts\activate.bat (
    echo [+] Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo [-] No virtual environment found. Creating one...
    python -m venv venv
    call venv\Scripts\activate.bat
)

REM Install dependencies
echo [+] Installing/updating dependencies...
pip install -r requirements.txt --quiet

echo.
echo ========================================
echo  Step 1: Running Descriptive Statistics...
echo ========================================
python -m statistical_analysis.run_stats
if %errorlevel% neq 0 (
    echo [ERROR] Descriptive statistics failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo  Step 2: Generating Charts...
echo ========================================
python -m statistical_analysis.visualisation_data
if %errorlevel% neq 0 (
    echo [ERROR] Chart generation failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo  Statistical Analysis Completed!
echo ========================================
echo.
echo Results:
echo   - Descriptive stats printed to console
echo   - Correlation matrix saved to correlation_matrix.xlsx
echo   - 9 charts displayed one after another
echo.
pause
