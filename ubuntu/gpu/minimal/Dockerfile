FROM databricksruntime/minimal:latest

## Copied from https://gitlab.com/nvidia/container-images/cuda/-/blob/master/dist/ubuntu16.04/10.1/base/Dockerfile
## with the 3-Clause BSD license: https://gitlab.com/nvidia/container-images/cuda/-/blob/master/LICENSE

# Copyright (c) 2019, NVIDIA CORPORATION. All rights reserved.

RUN apt-get update && apt-get install -y --no-install-recommends \
ca-certificates apt-transport-https gnupg-curl && \
    NVIDIA_GPGKEY_SUM=d1be581509378368edeec8c1eb2958702feedf3bc3d17011adbf24efacce4ab5 && \
    NVIDIA_GPGKEY_FPR=ae09fe4bbd223a84b2ccfce3f60f4b3d7fa2af80 && \
    apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/7fa2af80.pub && \
    apt-key adv --export --no-emit-version -a $NVIDIA_GPGKEY_FPR | tail -n +5 > cudasign.pub && \
    echo "$NVIDIA_GPGKEY_SUM  cudasign.pub" | sha256sum -c --strict - && rm cudasign.pub && \
    echo "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64 /" > /etc/apt/sources.list.d/cuda.list && \
    echo "deb https://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1604/x86_64 /" > /etc/apt/sources.list.d/nvidia-ml.list && \
    apt-get purge --auto-remove -y gnupg-curl && \
rm -rf /var/lib/apt/lists/*

ENV CUDA_VERSION 10.1.243

ENV CUDA_PKG_VERSION 10-1=$CUDA_VERSION-1

# For libraries in the cuda-compat-* package: https://docs.nvidia.com/cuda/eula/index.html#attachment-a
RUN apt-get update && apt-get install -y --no-install-recommends \
        cuda-cudart-$CUDA_PKG_VERSION \
cuda-compat-10-1 && \
ln -s cuda-10.1 /usr/local/cuda && \
    rm -rf /var/lib/apt/lists/*

# Required for nvidia-docker v1
RUN echo "/usr/local/nvidia/lib" >> /etc/ld.so.conf.d/nvidia.conf && \
    echo "/usr/local/nvidia/lib64" >> /etc/ld.so.conf.d/nvidia.conf

ENV PATH /usr/local/nvidia/bin:/usr/local/cuda/bin:${PATH}
ENV LD_LIBRARY_PATH /usr/local/nvidia/lib:/usr/local/nvidia/lib64

# nvidia-container-runtime
ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES compute,utility
ENV NVIDIA_REQUIRE_CUDA "cuda>=10.1 brand=tesla,driver>=384,driver<385 brand=tesla,driver>=396,driver<397 brand=tesla,driver>=410,driver<411"

## End of https://gitlab.com/nvidia/container-images/cuda/-/blob/master/dist/ubuntu16.04/10.1/base/Dockerfile

# Install the full CUDA Toolkit, NCCL, cuDNN, cuBLAS, and TensorRT.
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      cuda-toolkit-10-1 \
      libnccl2=2.6.4-1+cuda10.1 \
      libnccl-dev=2.6.4-1+cuda10.1 \
      libcudnn7=7.6.5.32-1+cuda10.1 \
      libcudnn7-dev=7.6.5.32-1+cuda10.1 \
      # Important: libcublas 10.2.1.243 matches CUDA 10.1 update 2 instead of CUDA 10.2
      libcublas10=10.2.1.243-1 \
      libcublas-dev=10.2.1.243-1 \
      libnvinfer6=6.0.1-1+cuda10.1 \
      libnvinfer-dev=6.0.1-1+cuda10.1
