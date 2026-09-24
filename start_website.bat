@echo off
title Facial Expression Tracking for Video Based Counselling Engagement
echo ==========================================================================
echo  Facial Expression Tracking for Video Based Counselling Engagement
echo ==========================================================================
echo Starting web server...
echo.

where python >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    python standalone_server.py
    goto end
)

if exist "C:\Users\HP\AppData\Local\Programs\Python\Python314\python.exe" (
    "C:\Users\HP\AppData\Local\Programs\Python\Python314\python.exe" standalone_server.py
    goto end
)

echo Python was not found on your system. Please ensure Python is installed.
pause

:end
