# See https://gitlab.com/nvidia/container-images/cuda/-/blob/master/dist/11.0.3/ubuntu18.04-x86_64/runtime/cudnn8/Dockerfile
FROM nvidia/cuda:11.3.0-cudnn8-runtime-ubuntu20.04

# See https://github.com/databricks/containers/blob/master/ubuntu/minimal/Dockerfile
RUN apt-get update \
  && apt-get -y upgrade \
  && apt-get install --yes \
    openjdk-8-jdk \
    iproute2 \
    bash \
    sudo \
    coreutils \
    procps \
    wget \
  && /var/lib/dpkg/info/ca-certificates-java.postinst configure \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
