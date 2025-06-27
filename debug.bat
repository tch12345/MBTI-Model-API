@echo off
cd /d "C:\xampp\htdocs\API"
cmd /k "uvicorn main:app --host 0.0.0.0 --port 8000"
