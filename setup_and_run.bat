@echo off
title Khoi tao va Chay Streamlit cho May moi
echo ========================================================
echo   HUONG DAN CHO THANH VIEN NHOM - DE TAI 1
echo ========================================================
echo Dang kiem tra Python tren may cua ban...

python --version >nul 2>&1
if %errorlevel% neq 0 (
    py --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo [CANH BAO]: May ban chua co Python trong PATH!
        echo Vui long vao https://www.python.org/downloads/ tai va cai Python 3.11 tro len
        echo (Luu y: NHO TICH VAO O "Add python.exe to PATH" khi cai dat).
        echo.
        pause
        exit /b 1
    ) else (
        set PY_CMD=py
    )
) else (
    set PY_CMD=python
)

if not exist ".venv" (
    echo Dang khoi tao moi truong ao (.venv)...
    %PY_CMD% -m venv .venv
    echo Dang cai dat cac thu vien can thiet (mat khoang 1-2 phut lan dau)...
    call .venv\Scripts\activate.bat
    python -m pip install --upgrade pip
    pip install -r requirements.txt
) else (
    call .venv\Scripts\activate.bat
)

echo.
echo ========================================================
echo   Dang khoi chay Streamlit Dashboard tren trinh duyet...
echo ========================================================
streamlit run app.py
pause
