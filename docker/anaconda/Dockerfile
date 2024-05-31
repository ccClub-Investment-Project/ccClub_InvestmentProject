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

# Generate Jupyter config and disable token
# RUN conda run -n ccclub jupyter notebook --generate-config && \
# echo "c.NotebookApp.token = ''" >> ~/.jupyter/jupyter_notebook_config.py

# Expose the Jupyter port
EXPOSE 8888

# Start Jupyter Lab
RUN mkdir /opt/sh

# Copy the start script into the container
COPY start_jupyter.sh /opt/sh

# Make the script executable
RUN chmod +x /opt/sh/start_jupyter.sh

# Start Jupyter Lab and list servers
CMD ["/opt/sh/start_jupyter.sh"]
# CMD ["sleep", "infinity"]