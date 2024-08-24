# Use the NVIDIA CUDA image as the base image
ARG BASE_IMAGE="nvidia/cuda:12.4.0-devel-ubuntu22.04"
FROM ${BASE_IMAGE}

# Set the host environment variable to allow access within the container if needed
ENV HOST=0.0.0.0

# Update package list and upgrade packages, then install necessary dependencies
RUN apt-get update && apt-get upgrade -y \
    && apt-get install -y git build-essential \
    python3 python3-pip gcc wget \
    ocl-icd-opencl-dev opencl-headers clinfo \
    libclblast-dev libopenblas-dev \
    && mkdir -p /etc/OpenCL/vendors && echo "libnvidia-opencl.so.1" > /etc/OpenCL/vendors/nvidia.icd

# Copy the current directory contents into the container at /workspace
# COPY . /workspace

# Set the working directory
# WORKDIR /workspace

# Upgrade pip and install necessary Python packages
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install pytest cmake scikit-build setuptools fastapi uvicorn sse-starlette pydantic-settings starlette-context langchain langchain-community transformers pandas
RUN python3 -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124

# Set the environment variable to enable CUDA support in llama-cpp-python
ENV GGML_CUDA=1

# Install llama-cpp-python with CUDA support
RUN CMAKE_ARGS="-DGGML_CUDA=on" pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/124

# Command to run when the container starts (you can adjust this to fit your development needs)
CMD [ "python3" ]
