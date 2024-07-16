@echo off
echo Installing dependencies...
pip install -r requirements.txt
echo Dependencies installed successfully.
echo.
echo Running Discord Log Bot...
python main.py
pause
