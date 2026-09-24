@echo off
title Push Project to GitHub
echo ==========================================================================
echo  Pushing Counselling Facial Emotion Tracker to GitHub
echo  Repository: https://github.com/sreenamanuzz/counselling-facial-emotion-tracker.git
echo ==========================================================================
echo.
echo Pushing commits to GitHub...
echo (If a GitHub sign-in window appears, please click "Sign in with your browser")
echo.

git push -u origin main

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ==========================================================================
    echo  SUCCESS! Your project has been pushed to GitHub successfully!
    echo ==========================================================================
) else (
    echo.
    echo ==========================================================================
    echo  Push failed or was cancelled. Please check your GitHub login and try again.
    echo ==========================================================================
)

echo.
pause
