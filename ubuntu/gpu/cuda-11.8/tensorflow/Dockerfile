FROM databricksruntime/gpu-venv:cuda11.8 

# Enable NVIDIA repos to install cuda-toolkit required by tensorflow.
RUN cd /etc/apt/sources.list.d && \
    mv cuda-ubuntu2204-x86_64.list.disabled cuda-ubuntu2204-x86_64.list

# Tensorflow would require cuda-toolkit-11-8 been installed.
RUN apt-get update \
    && apt-get --no-install-recommends -y install cuda-toolkit-11-8

# Disable NVIDIA repos to prevent accidental upgrades.
RUN cd /etc/apt/sources.list.d && \
    mv cuda-ubuntu2204-x86_64.list cuda-ubuntu2204-x86_64.list.disabled

# install the tensorflow versions
RUN /databricks/python3/bin/pip install \
    tensorflow==2.13.0 \
    tensorboard==2.13.0