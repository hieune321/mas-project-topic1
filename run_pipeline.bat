@echo off
title Chay Pipeline Phan Tich Du Lieu
echo Dang chay pipeline phan tich du lieu thuc te va xuat bao cao...
"%~dp0.venv\Scripts\python.exe" "%~dp0main.py" --input "%~dp0data\raw\student_scores.csv"
pause
