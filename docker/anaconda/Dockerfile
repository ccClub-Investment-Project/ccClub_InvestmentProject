# Use an official Anaconda runtime as a parent image
FROM continuumio/miniconda3:latest

# Set the working directory
WORKDIR /opt/ccclub/

# Install fonts-noto-cjk package for Noto CJK fonts
RUN apt update && \
    apt install -y \
    fonts-noto-cjk \
    fontconfig && \
    fc-cache -f -v

# Create a new environment with the specific Python version
RUN conda create -n ccclub python=3.10.14 -y

# Activate the environment
SHELL ["conda", "run", "-n", "ccclub", "/bin/bash", "-c"]

# 複製 requirements 文件到容器
COPY requirements_conda.txt .
COPY requirements_pip.txt .

# 更新 Conda
RUN conda update -n base -c defaults conda

# 更新 Pip
RUN conda run -n base /bin/bash -c "pip install --upgrade pip"

# 使用 conda 安裝 requirements_conda.txt 中的包
RUN conda install -c conda-forge --yes --file requirements_conda.txt

# 使用 pip 安裝 requirements_pip.txt 中的包
RUN pip install -r requirements_pip.txt

# Expose the Jupyter port
EXPOSE 8888

# Run all necessary commands to start Jupyter Lab and keep the container running
CMD ["/bin/bash", "-c", "source activate ccclub && jupyter-lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root && jupyter server list && sleep infinity"]

