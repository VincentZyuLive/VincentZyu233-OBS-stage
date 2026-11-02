@echo off
setlocal EnableExtensions DisableDelayedExpansion
cd /d "%~dp0.."

set "PORT=6162"
set "OPEN_BROWSER=1"
set "PASSTHROUGH=0"

call :parse_args %*
if "%PASSTHROUGH%"=="1" goto run_cli

title OBS Stage - %PORT%
set "ADMIN_URL=http://127.0.0.1:%PORT%/admin"
set "HEALTH_URL=http://127.0.0.1:%PORT%/api/config"

curl.exe -fsS --max-time 2 "%HEALTH_URL%" >nul 2>&1
if not errorlevel 1 (
    echo OBS Stage is already running.
    if "%OPEN_BROWSER%"=="1" (
        start "" "%ADMIN_URL%"
    ) else (
        echo Admin URL: %ADMIN_URL%
    )
    exit /b 0
)

:run_cli
where uv >nul 2>&1
if errorlevel 1 (
    echo [ERROR] uv was not found in PATH.
    echo Install uv or add it to PATH, then try again.
    pause
    exit /b 1
)

if "%PASSTHROUGH%"=="0" echo Starting OBS Stage on %ADMIN_URL%
uv run obs-stage %*
set "EXIT_CODE=%ERRORLEVEL%"
if not "%EXIT_CODE%"=="0" (
    echo [ERROR] OBS Stage exited with an error.
    pause
)
exit /b %EXIT_CODE%

:parse_args
if "%~1"=="" exit /b 0
if /I "%~1"=="--port" goto parse_port
set "ARG=%~1"
if /I not "%ARG:~0,7%"=="--port=" goto parse_flags
set "PORT=%ARG:~7%"
shift
goto parse_args

:parse_flags
if /I "%~1"=="--no-browser" (
    set "OPEN_BROWSER=0"
    shift
    goto parse_args
)
if /I "%~1"=="--help" goto parse_passthrough
if /I "%~1"=="-h" goto parse_passthrough
if /I "%~1"=="--version" goto parse_passthrough
shift
goto parse_args

:parse_port
if "%~2"=="" exit /b 0
set "PORT=%~2"
shift
shift
goto parse_args

:parse_passthrough
set "PASSTHROUGH=1"
exit /b 0
