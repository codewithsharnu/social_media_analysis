@echo off
title SML - Statistical Analysis CLI Engine
color 0a
echo ========================================================
echo   RUNNING FULL STATISTICAL ANALYSIS & EDA ENGINE (SML)
echo ========================================================
echo.
cd /d "%~dp0\.."
python social_media_analysis.py
echo.
echo ========================================================
echo Analysis complete. Press any key to exit.
pause >nul
