@echo off
REM CAD CI/CD Sandbox Simulation One-Click Runner (Windows)
echo ===================================================
echo   Running Local CAD CI/CD Sandbox Simulation...
echo ===================================================
python "%~dp0ci_sandbox.py" --all
if %ERRORLEVEL% NEQ 0 (
    echo [FAIL] CI/CD Sandbox Pipeline Failed!
    exit /b %ERRORLEVEL%
)
echo [PASS] Running Pytest Suite...
python -m pytest "%~dp0..\tests" -v
exit /b %ERRORLEVEL%
