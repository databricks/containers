FROM databricksruntime/gpu-venv:cuda11.8 

# Tensorflow would require extra cuda libaries been installed. Added as needed
RUN apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/3bf863cc.pub \
    && apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/7fa2af80.pub \
    && apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu2004/x86_64/7fa2af80.pub \
    && add-apt-repository "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/ /" \
    && add-apt-repository "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/ /" \
    && apt-get install --allow-downgrades --no-install-recommends -y \
     # https://gitlab.com/nvidia/container-images/cuda/-/blob/master/dist/11.8.0/ubuntu2204/devel/Dockerfile
      cuda-cudart-dev-11-8=11.8.89-1 \
      cuda-command-line-tools-11-8=11.8.0-1 \
      cuda-minimal-build-11-8=11.8.0-1 \
      cuda-libraries-dev-11-8=11.8.0-1 \
      cuda-nvml-dev-11-8=11.8.86-1 \
      cuda-nvprof-11-8=11.8.87-1 \
      libnpp-dev-11-8=11.8.0.86-1 \

      # CUPTI for TensorFlow: https://www.tensorflow.org/install/gpu
      cuda-cupti-11-8=11.8.87-1 \
      cuda-cupti-dev-11-8=11.8.87-1 \
       # TensorFlow requires libcusolver 11
      libcusolver-11-8=11.4.1.48-1


# install the tensorflow versions
RUN /databricks/python3/bin/pip install \
    tensorflow==2.13.0 \
    tensorboard==2.13.0