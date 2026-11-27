ARG cuda_image=nvidia/cuda:12.6.3-runtime-ubuntu24.04@sha256:2c8193530ecc423e0f123d0c85b68a15d1395adcddabfc943e2523dbfde172e1
FROM ${cuda_image}

ARG cudnn_version

COPY framework-constraints.txt /databricks/gpu-framework-constraints.txt

RUN apt-get update \
  && apt-get install --yes --no-install-recommends libcudnn9-cuda-12=${cudnn_version} \
  && rm -f /etc/apt/sources.list.d/cuda*.list /etc/apt/sources.list.d/cuda*.sources \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
