# Use an official Anaconda runtime as a parent image
FROM continuumio/miniconda3:latest

# Set the working directory
WORKDIR /opt/ccclub/

# Create a new environment with the specific Python version
RUN conda create -n ccclub python=3.10.14 -y

# Activate the environment
SHELL ["conda", "run", "-n", "ccclub", "/bin/bash", "-c"]

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN conda install -c conda-forge --yes --file requirements.txt

# Expose the Jupyter port
EXPOSE 8888

# Run all necessary commands to start Jupyter Lab and keep the container running
CMD ["/bin/bash", "-c", "source activate ccclub && jupyter-lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root && jupyter server list && sleep infinity"]

