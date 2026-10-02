@echo off

echo Starting PocketSmart AI...

if not exist .venv (
    echo Creating virtual environment...
    python -m venv .venv
)

call .venv\Scripts\activate

echo Installing dependencies...
pip install -r requirements.txt

echo Starting server...
uvicorn app.main:app --reload

pause