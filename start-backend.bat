@echo off
echo ========================================
echo ATS Resume Analyzer - Starting Backend
echo ========================================
echo.

cd backend

REM Check if venv exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate

REM Install/Update dependencies
echo Installing/Updating dependencies...
pip install --quiet flask flask-cors pdfplumber python-docx scikit-learn nltk numpy werkzeug

echo.
echo ========================================
echo Backend Server Starting...
echo ========================================
echo Server will be available at: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

REM Start Flask app
python app.py

pause
