@echo off
title Model Training and Benchmarks Evaluation
echo ==========================================================================
echo  Training and Evaluating Models: RF, XGBoost, CRNN, Conformer, YOLOv12
echo ==========================================================================
echo.

where python >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    python train_and_evaluate.py
    pause
    goto end
)

if exist "C:\Users\HP\AppData\Local\Programs\Python\Python314\python.exe" (
    "C:\Users\HP\AppData\Local\Programs\Python\Python314\python.exe" train_and_evaluate.py
    pause
    goto end
)

echo Python was not found on your system.
pause

:end
