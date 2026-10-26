@echo off
title Social Pulse Analytics - SML Web Server
color 0b
echo ========================================================
echo   STARTING SML SOCIAL PULSE ANALYTICS WEB APPLICATION
echo ========================================================
echo.
echo Launching Flask Web Server on http://localhost:5000 ...
cd /d "%~dp0\.."
start "" http://localhost:5000
python app.py
pause
