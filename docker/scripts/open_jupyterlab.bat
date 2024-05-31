@echo off

set CONTAINER_NAME=dev_env
set VENV_NAME=ccclub
set PORT=8887
set USE_JUPYTERLAB_DESKTOP=true

REM Check if the container is running
docker ps -q --filter "name=%CONTAINER_NAME%" --no-trunc | findstr /r "." >nul
if %ERRORLEVEL% equ 0 (
    echo container is running
) else (
    echo container(%CONTAINER_NAME%) is not running
    docker start anaconda
    echo Starting container(%CONTAINER_NAME%)...
    timeout /t 10
)

REM get jupyter url
for /f "delims=" %%i in ('docker exec %CONTAINER_NAME% bash -c "source /opt/conda/bin/activate %VENV_NAME% && jupyter lab list" ^| findstr /r "http://[^ ]*"') do set URL=%%i
for /f "tokens=1* delims=token=" %%a in ("%URL%") do set TOKEN=%%b

set FULL_URL=http://localhost:%PORT%/lab?%TOKEN%
echo %FULL_URL%

if "%USE_JUPYTERLAB_DESKTOP%" == "true" (
    where /q jlab
    if %ERRORLEVEL% equ 0 (
        start jlab "%FULL_URL%"
    ) else (
        echo JupyterLab Desktop is not installed or not found in PATH. Please manually open the following URL:
        echo %FULL_URL%
    )
) else (
    REM Open URL in default browser
    start "" "%FULL_URL%"
)