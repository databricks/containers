
FROM databricksruntime/gpu-base:cuda11.8

WORKDIR /databricks

# Install python 3.10 from ubuntu.
# Install pip via get-pip.py bootstrap script and install versions that match Anaconda distribution.
RUN apt-get update \
  && apt-get install curl software-properties-common -y python3.10 python3.10-dev python3.10-distutils \
  && curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py \
  && /usr/bin/python3.10 get-pip.py pip==22.2.2 setuptools==58.0.4 wheel==0.37.0 \
  && rm get-pip.py


# virtualenv 20.0.24 introduced a periodic update feature, which attempts to update all
# seeder packages every 14 days. This launches background processes that may interfere
# with user cleanup and may allow users to inadvertently update pip to newer versions
# incompatible with Databricks. Instead, we patch virtualenv to disable periodic updates per
# https://virtualenv.pypa.io/en/latest/user_guide.html#embed-wheels-for-distributions. See
# ML-13720 for more details.
RUN /usr/local/bin/pip3.10 install --no-cache-dir virtualenv==20.16.3 \
    && sed -i -r 's/^(PERIODIC_UPDATE_ON_BY_DEFAULT) = True$/\1 = False/' /usr/local/lib/python3.10/dist-packages/virtualenv/seed/embed/base_embed.py \
    && /usr/local/bin/pip3.10 download pip==22.2.2 --dest \
    /usr/local/lib/python3.10/dist-packages/virtualenv_support/


# Install CUDA runtime libraries, plus cuBLAS, cuDNN, NCCL, and TensorRT.
# CUDA is installed twice, using apt-get and using conda. The apt-get version contains shared
# libraries as well as utilities such as the nvcc CUDA compiler. The conda version contains
# only shared libraries used by dependencies such as pytorch. The two CUDA installations should
# have the same version.
# CUDA runtime packages and versions are copied from CUDA's base, runtime and devel Dockerfiles.
# See https://gitlab.com/nvidia/container-images/cuda/-/tree/master/dist/11.8.0/ubuntu2204
RUN wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-ubuntu2204.pin \
    && mv cuda-ubuntu2204.pin /etc/apt/preferences.d/cuda-repository-pin-600 \
    && apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/3bf863cc.pub \
    && apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/7fa2af80.pub \
    # machine-learning repo on nvidia not available for ubuntu 22.04 yet, we are using ubuntu 20.04 for now.
    && apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu2004/x86_64/7fa2af80.pub \
    && add-apt-repository "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/ /" \
    && add-apt-repository "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/ /" \
    # machine-learning repo on nvidia not available for ubuntu 22.04 yet, we are using ubuntu 20.04 for now.
    && wget https://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu2004/x86_64/nvidia-machine-learning-repo-ubuntu2004_1.0.0-1_amd64.deb \
    && dpkg -i ./nvidia-machine-learning-repo-ubuntu2004_1.0.0-1_amd64.deb \
    && apt-get --allow-releaseinfo-change-origin update \
    # Find latest versions at https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/
    # and http://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu2004/x86_64
    # Note: Currently we did not find machine-learning repos under ubuntu2204/x86_64.
    && apt-get install --allow-downgrades --no-install-recommends -y --allow-change-held-packages \

      # https://gitlab.com/nvidia/container-images/cuda/-/blob/master/dist/11.8.0/ubuntu2204/runtime/Dockerfile
      cuda-libraries-11-8=11.8.0-1 \
      libnpp-11-8=11.8.0.86-1 \
      cuda-nvtx-11-8=11.8.86-1 \
      libcublas-11-8=11.11.3.6-1 \
      libcusparse-11-8=11.7.5.86-1 \
      libnccl2=2.15.5-1+cuda11.8 \

      # https://gitlab.com/nvidia/container-images/cuda/-/blob/master/dist/11.8.0/ubuntu2204/devel/Dockerfile
      cuda-cudart-dev-11-8=11.8.89-1 \
      cuda-command-line-tools-11-8=11.8.0-1 \
      cuda-minimal-build-11-8=11.8.0-1 \
      cuda-libraries-dev-11-8=11.8.0-1 \
      cuda-nvml-dev-11-8=11.8.86-1 \
      cuda-nvprof-11-8=11.8.87-1 \
      libnpp-dev-11-8=11.8.0.86-1 \
      libnccl-dev=2.15.5-1+cuda11.8 \

      # Popular models such as MPT and Databricks Dolly require several CUDA dev libraries
      # Find the versions here: https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/
      libcublas-dev-11-8=11.11.3.6-1 \
      libcusparse-dev-11-8=11.7.5.86-1 \
      libcusolver-dev-11-8=11.4.1.48-1 \
      libcurand-dev-11-8=10.3.0.86-1 \

      # CUPTI for TensorFlow: https://www.tensorflow.org/install/gpu
      cuda-cupti-11-8=11.8.87-1 \
      cuda-cupti-dev-11-8=11.8.87-1 \

      # TensorFlow requires libcusolver 11
      libcusolver-11-8=11.4.1.48-1 \

      # ibverbs-providers installs user-space drivers for RDMA support
      ibverbs-providers=39.0-1 \

      # Install cudnn
      # Reference: https://gitlab.com/nvidia/container-images/cuda/-/blob/master/dist/11.8.0/ubuntu2204/runtime/cudnn8/Dockerfile
      libcudnn8=8.9.0.131-1+cuda11.8 \
      libcudnn8-dev=8.9.0.131-1+cuda11.8 \
      
      # The dcgm-exporter binary has a runtime dependency on the DCGM library. The version we install
      # must be compatible with the DCGM-Exporter version. The expected DCGM version is the first version
      # number in the name of the DCGM-Exporter release (see
      # https://github.com/NVIDIA/dcgm-exporter/blob/main/Makefile); e.g. in `3.1.3-3.1.2-ubuntu20.04`,
      # the expected DCGM version is 3.1.3.
      datacenter-gpu-manager=1:3.1.3 \
          
      # Tensorflow 2.13 is built with TensorRT 8.4.3, but we verified that it also works with 8.5.3.
      # We install 8.5.3 here since 8.4.3 is built with cuda 11.6 not with 11.8.
      libnvinfer8=8.5.3-1+cuda11.8 \
      libnvinfer-plugin8=8.5.3-1+cuda11.8 \

    # We remove all GPU repos to avoid CUDA 11.8 incompatible upgrades.
    && add-apt-repository -r "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/ /" \
    && add-apt-repository -r "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/ /" \
    && apt-get remove --auto-remove --purge -y nvidia-machine-learning-repo-ubuntu2004
    

# https://gitlab.com/nvidia/container-images/cuda/-/blob/master/dist/11.8.0/ubuntu2204/base/Dockerfile
ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES compute,utility
ENV NVIDIA_REQUIRE_CUDA "cuda>=11.8 brand=tesla,driver>=450,driver<451 brand=tesla,driver>=470,driver<471 brand=unknown,driver>=470,driver<471 brand=nvidia,driver>=470,driver<471 brand=nvidiartx,driver>=470,driver<471 brand=geforce,driver>=470,driver<471 brand=geforcertx,driver>=470,driver<471 brand=quadro,driver>=470,driver<471 brand=quadrortx,driver>=470,driver<471 brand=titan,driver>=470,driver<471 brand=titanrtx,driver>=470,driver<471 brand=tesla,driver>=510,driver<511 brand=unknown,driver>=510,driver<511 brand=nvidia,driver>=510,driver<511 brand=nvidiartx,driver>=510,driver<511 brand=geforce,driver>=510,driver<511 brand=geforcertx,driver>=510,driver<511 brand=quadro,driver>=510,driver<511 brand=quadrortx,driver>=510,driver<511 brand=titan,driver>=510,driver<511 brand=titanrtx,driver>=510,driver<511 brand=tesla,driver>=515,driver<516 brand=unknown,driver>=515,driver<516 brand=nvidia,driver>=515,driver<516 brand=nvidiartx,driver>=515,driver<516 brand=geforce,driver>=515,driver<516 brand=geforcertx,driver>=515,driver<516 brand=quadro,driver>=515,driver<516 brand=quadrortx,driver>=515,driver<516 brand=titan,driver>=515,driver<516 brand=titanrtx,driver>=515,driver<516"

# temporarily using CUDA stubs at build time based on the suggestions from https://github.com/NVIDIA/nvidia-docker/wiki/Frequently-Asked-Questions#how-do-i-link-against-driver-apis-at-build-time-eg-libcudaso-or-libnvidia-mlso
RUN ldconfig /usr/local/cuda/targets/x86_64-linux/lib/stubs


# Create /databricks/python3 environment.
# We install pip and wheel so their executables show up under /databricks/python3/bin.
# We use `--system-site-packages` so python will fallback to system site packages.
# We use `--no-download` so virtualenv will install the bundled pip and wheel.
RUN virtualenv --python=/usr/bin/python3.10 /databricks/python3 --system-site-packages --no-download


# These python libraries are used by Databricks notebooks and the Python REPL
# You do not need to install pyspark - it is injected when the cluster is launched
# Versions are intended to reflect latest DBR: https://docs.databricks.com/release-notes/runtime/11.1.html#system-environment
RUN /databricks/python3/bin/pip install \
  six==1.16.0 \
  jedi==0.18.1 \
  # ensure minimum ipython version for Python autocomplete with jedi 0.17.x
  ipython==8.10.0 \
  numpy==1.21.5 \
  pandas==1.4.4 \
  pyarrow==8.0.0 \
  matplotlib==3.5.2 \
  jinja2==2.11.3 \
  ipykernel==6.17.1 \
  grpcio==1.48.1 \
  protobuf==3.19.4 \ 
  grpcio-status==1.48.1 \
  databricks-sdk==0.1.6

# Specifies where Spark will look for the python process
ENV PYSPARK_PYTHON=/databricks/python3/bin/python3

# Use pip cache purge to cleanup the cache safely
RUN /databricks/python3/bin/pip cache purge

