# See https://gitlab.com/nvidia/container-images/cuda/-/blob/master/dist/ubuntu18.04/10.1/runtime/Dockerfile
FROM nvidia/cuda:10.1-runtime-ubuntu18.04

# Disable NVIDIA repos to prevent accidental upgrades.
RUN cd /etc/apt/sources.list.d && \
    mv cuda.list cuda.list.disabled && \
    mv nvidia-ml.list nvidia-ml.list.disabled

# See https://github.com/databricks/containers/blob/master/ubuntu/minimal/Dockerfile
RUN apt-get update && \
    apt-get install --yes --no-install-recommends \
      openjdk-8-jdk-headless \
      iproute2 \
      bash \
      sudo \
      coreutils \
      procps \
      wget && \
    /var/lib/dpkg/info/ca-certificates-java.postinst configure && \
    rm -rf /var/lib/apt/lists/*

