@echo off
chcp 65001 > nul
echo ========================================
echo  ETL Pipeline — Raw CSV to Data Warehouse
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
echo  Step 1: Creating database schema...
echo ========================================
python database\main_dw_db.py
if %errorlevel% neq 0 (
    echo [ERROR] Schema creation failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo  Step 2: Running ETL (CSV to Data Warehouse)...
echo ========================================
python database\etl\etl_raw_to_dw.py
if %errorlevel% neq 0 (
    echo [ERROR] ETL failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo  ETL Pipeline Completed Successfully!
echo ========================================
echo.
echo Data warehouse (football_dw) is ready with:
echo   - 5 dimension tables (dim_country, dim_division, dim_team, dim_season, dim_date)
echo   - 1 fact table (fact_matches)
echo   - 2 raw staging tables (raw_eloRatings, raw_Matches)
echo   - CSV exports in csv/raw/ and csv/clean/
echo.
pause
