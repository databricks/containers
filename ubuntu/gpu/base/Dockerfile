ARG cuda_image=nvidia/cuda:12.9.1-runtime-ubuntu24.04@sha256:1199283a7fd5fc7dcb472ea4c6b6d8eb378ef8c0b9aae5e731491c01a219ca43
FROM ${cuda_image}

ARG cudnn_version

COPY framework-constraints.txt /databricks/gpu-framework-constraints.txt

RUN apt-get update \
  && apt-get install --yes --no-install-recommends libcudnn9-cuda-12=${cudnn_version} \
  && rm -f /etc/apt/sources.list.d/cuda*.list /etc/apt/sources.list.d/cuda*.sources \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
