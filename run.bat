@echo off
cd /d "%~dp0"

echo ===================================================
echo AI Student Chatbot Launcher
echo ===================================================

if not exist .venv (
    echo [INFO] Creating virtual environment...
    python -m venv .venv
)

echo [INFO] Activating environment...
call .venv\Scripts\activate

REM Use verbose flag to show progress
echo [INFO] Installing PyTorch (CPU version) to ensure speed...
REM Explicitly install CPU torch to avoid 2GB download if possible
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

echo [INFO] Installing other dependencies...
pip install -r requirements.txt -v

echo [INFO] Seeding data...
python seed_bulk.py

echo [INFO] Starting Server...
echo [INFO] WARNING: On the very first run, it will pause to download the AI Model.
echo [INFO] Check the terminal output for "Loading NLP model"...
python -m uvicorn app.main:app --reload

pause
