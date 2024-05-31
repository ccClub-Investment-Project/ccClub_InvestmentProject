#!/bin/bash

# Activate the Conda environment
source activate ccclub

# Start Jupyter Lab
jupyter-lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root &

# List Jupyter servers
jupyter server list

# Wait for Jupyter Lab to start
sleep infinity


