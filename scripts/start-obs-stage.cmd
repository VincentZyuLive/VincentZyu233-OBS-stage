@echo off
setlocal
title OBS Stage - 6162
cd /d "%~dp0.."

curl.exe -fsS --max-time 2 "http://127.0.0.1:6162/api/config" >nul 2>&1
if not errorlevel 1 (
    echo OBS Stage is already running.
    start "" "http://127.0.0.1:6162/admin"
    exit /b 0
)

where uv >nul 2>&1
if errorlevel 1 (
    echo [ERROR] uv was not found in PATH.
    echo Install uv or add it to PATH, then try again.
    pause
    exit /b 1
)

echo Starting OBS Stage on http://127.0.0.1:6162/admin
uv run obs-stage
if errorlevel 1 (
    echo [ERROR] OBS Stage exited with an error.
    pause
)
