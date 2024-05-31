#!/bin/bash

CONTAINER_NAME="dev_env"
VENV_NAME="ccclub"
PORT="8887"
USE_JUPYTERLAB_DESKTOP=true

# Check if the container is running
if docker ps -q --filter "name=$CONTAINER_NAME" | grep -q .; then
    echo "container is running"
else
    echo "container($CONTAINER_NAME) is not running"
    docker start anaconda
    echo "Starting container($CONTAINER_NAME)..."
    sleep 10
fi

# get jupyter url
URL=$(docker exec $CONTAINER_NAME bash -c "source /opt/conda/bin/activate $VENV_NAME && jupyter lab list" | grep -o 'http://[^ ]*')
#TOKEN=$(echo $URL | grep -o 'token=\K[^&]+')
TOKEN=$(echo $URL | sed -n 's/.*token=\([^&]*\).*/\1/p')

FULL_URL="http://localhost:$PORT/lab?token=$TOKEN"
echo "$FULL_URL"


if [ "$USE_JUPYTERLAB_DESKTOP" = true ]; then
    if command -v jlab > /dev/null; then
        jlab "$FULL_URL"
    else
        echo "JupyterLab Desktop is not installed or not found in PATH. Please manually open the following URL:"
    fi
else
    # xdg-open = Linux環境; open = macOS環境
    if command -v xdg-open > /dev/null; then
        xdg-open "$FULL_URL"
    elif command -v open > /dev/null; then
        open "$FULL_URL"
    else
        echo "Unable to find a command to open the browser. Please manually open the following URL:"
    fi
fi