@echo off
title Khoi chay Streamlit Dashboard
echo Dang khoi chay giao dien Streamlit Dashboard...
"%~dp0.venv\Scripts\streamlit.exe" run "%~dp0app.py"
pause
