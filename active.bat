@echo off
cd /d "C:\xampp\htdocs\API"
start "" /min cmd /c "uvicorn main:app --host 0.0.0.0 --port 8000"

