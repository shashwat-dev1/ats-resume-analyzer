@echo off
echo ========================================
echo ATS Resume Analyzer - Starting Frontend
echo ========================================
echo.

cd frontend

REM Check if node_modules exists
if not exist "node_modules\" (
    echo Installing dependencies for the first time...
    call npm install
) else (
    echo Dependencies already installed.
)

echo.
echo ========================================
echo Frontend Server Starting...
echo ========================================
echo.
echo Frontend will be available at: http://localhost:5173
echo Make sure backend is running on: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

REM Start Vite dev server
npm run dev

pause
