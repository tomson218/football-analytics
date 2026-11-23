@echo off
chcp 65001 > nul
echo ========================================
echo  ML Pipeline — HomeNoLose Classification
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
echo  Step 1: Preparing Data from Data Warehouse...
echo ========================================
python ml_exploratory_analysis\prepare_data.py
if %errorlevel% neq 0 (
    echo [ERROR] Data preparation failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo  Step 2: Processing Features (Scaling + Target)...
echo ========================================
python ml_exploratory_analysis\data_processing.py
if %errorlevel% neq 0 (
    echo [ERROR] Data processing failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo  Step 3: Training CatBoost Model (5-fold CV)...
echo ========================================
python ml_exploratory_analysis\train_models.py
if %errorlevel% neq 0 (
    echo [ERROR] Model training failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo  Step 4: Testing Model on Test Set...
echo ========================================
python ml_exploratory_analysis\testing.py
if %errorlevel% neq 0 (
    echo [ERROR] Model testing failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo  ML Pipeline Completed Successfully!
echo ========================================
echo.
echo Results:
echo   - Models saved: ml_exploratory_analysis\models\catboost_base.cbm, catboost_10feat.cbm, catboost_6feat.cbm
echo   - Metrics: ml_exploratory_analysis\results\model_comparison.json, binary_results.json
echo   - Confusion matrix: ml_exploratory_analysis\results\confusion_matrix.png
echo   - Feature importance: ml_exploratory_analysis\results\feature_importance_base.png, feature_importance_10feat.png, feature_importance_6feat.png
echo   - Sample predictions: ml_exploratory_analysis\results\sample_matches_test.csv
echo.
pause
