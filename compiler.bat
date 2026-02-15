@echo off
setlocal EnableDelayedExpansion
title Python App Compiler
color 0A

cd /d "%~dp0"

echo.
echo  ╔══════════════════════════════════════════╗
echo  ║      PYTHON APP COMPILER                 ║
echo  ╚══════════════════════════════════════════╝
echo.

REM === Check Python ===
echo [1/2] Checking Python...
set "PY="
where python >nul 2>&1 && set "PY=python"
if not defined PY (where py >nul 2>&1 && set "PY=py -3")
if not defined PY (
    color 0C
    echo.
    echo  [ERROR] Python not found!
    echo  Download: https://python.org/downloads
    echo.
    pause
    exit /b 1
)
for /f "tokens=*" %%v in ('%PY% --version 2^>^&1') do echo   %%v OK
echo.

REM === Check PyInstaller ===
echo [2/2] Checking PyInstaller...
%PY% -c "import PyInstaller" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo   Installing PyInstaller...
    %PY% -m pip install pyinstaller -q
)
echo   PyInstaller ready
echo.

REM === Launch ===
echo ══════════════════════════════════════════
echo.
%PY% "%~dp0compiler.py"

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [!] Exited with error code: %ERRORLEVEL%
    pause
)

endlocal