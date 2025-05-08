@echo off
SETLOCAL

REM Check if python is installed
where python >nul 2>nul
IF %ERRORLEVEL% NEQ 0 (
    echo Python is not installed.
    echo Please install it from https://www.python.org/downloads/
    exit /b 1
)

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Install required packages
echo Installing required packages...
pip install ^
    certifi==2025.4.26 ^
    charset-normalizer==3.4.2 ^
    idna==3.10 ^
    instaloader==4.14.1 ^
    requests==2.32.3 ^
    urllib3==2.4.0

echo Installation complete.
echo To run the script:
echo     call venv\Scripts\activate
echo     python program.py

ENDLOCAL