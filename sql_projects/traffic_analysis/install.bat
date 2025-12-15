@echo off
REM ==============================================
REM traffic_analysis Environment Setup (Windows)
REM ==============================================

echo Setting up Python virtual environment...

REM Define venv directory and paths
set VENV=.venv
set PYTHON=%VENV%\Scripts\python.exe
set PIP=%VENV%\Scripts\pip.exe

REM Create virtual environment if it doesn't exist
if not exist %VENV% (
    echo Creating virtual environment...
    python -m venv %VENV%
)

REM Upgrade pip inside the venv
echo Upgrading pip...
"%PYTHON%" -m pip install --upgrade pip

REM Install traffic_analysis in editable mode
echo Installing traffic_analysis in editable mode...
"%PIP%" install -e .[dev]

echo.
echo ✅ Environment setup complete!
echo Use the following Python executable when working in this environment:
echo     %PYTHON%
echo.
echo Example:
echo     "%PYTHON%" -m traffic_analysis
echo =====================================
