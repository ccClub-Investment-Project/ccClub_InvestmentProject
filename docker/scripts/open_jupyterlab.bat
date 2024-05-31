@echo off

set CONTAINER_NAME="dev_env"
set VENV_NAME="ccclub"
set PORT=8887
set USE_JUPYTERLAB_DESKTOP=true

rem Check if the container is running
docker ps -q --filter "name=%CONTAINER_NAME%" | findstr /r "." >nul
if %ERRORLEVEL% equ 0 (
    echo container is running
) else (
    echo test
    echo container^(%CONTAINER_NAME%^) is not running
    docker start %CONTAINER_NAME%
    echo Starting container^(%CONTAINER_NAME%^)...
    timeout /t 10 >nul
)


rem get jupyter url
for /f "tokens=*" %%i in ('docker exec %CONTAINER_NAME% bash -c "source /opt/conda/bin/activate %VENV_NAME% && jupyter lab list" ^| findstr /r "http://[^ ]*"') do (
    set "URL=%%i"
)

rem extract the token from the URL
for /f "tokens=2 delims=?" %%a in ("%URL%") do set "TOKEN_PART=%%a"
for /f "tokens=2 delims==::" %%b in ("%TOKEN_PART%") do set "TOKEN=%%b"

set FULL_URL=http://localhost:%PORT%/lab?token=%TOKEN%
echo %FULL_URL%

if "%USE_JUPYTERLAB_DESKTOP%" == "true" (
    where /q jlab
    if %ERRORLEVEL% equ 0 (
        jlab "%FULL_URL%"
    ) else (
        echo JupyterLab Desktop is not installed or not found in PATH. Please manually open the following URL:
    )
) else (
    where /q start
    if %ERRORLEVEL% equ 0 (
        start "" "%FULL_URL%"
    ) else (
        echo Unable to find a command to open the browser. Please manually open the following URL:
    )
)