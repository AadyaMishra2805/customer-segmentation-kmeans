@echo off

cd /d "D:\customer segmentation"

start http://127.0.0.1:5000

"%CD%\\.venv\\Scripts\\python.exe" app.py

pause