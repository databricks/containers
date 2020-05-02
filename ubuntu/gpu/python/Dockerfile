FROM databricksruntime/gpu-minimal:cuda10.1

RUN apt-get update && apt-get install --yes \
    wget \
    libdigest-sha-perl \
    bzip2

# Download miniconda 4.5.12, then upgrade it to 4.8.3.
RUN wget --quiet --output-document miniconda.sh https://repo.continuum.io/miniconda/Miniconda3-4.5.12-Linux-x86_64.sh \
    && (echo '866ae9dff53ad0874e1d1a60b1ad1ef8  miniconda.sh' | md5sum -c) \
    && (echo 'e5e5b4cd2a918e0e96b395534222773f7241dc59d776db1b9f7fedfcb489157a  miniconda.sh' | shasum -a 256 -c) \
    # Conda must be installed at /databricks/conda
    && /bin/bash miniconda.sh -b -p /databricks/conda \
    && rm miniconda.sh \
    && /databricks/conda/bin/conda install --name base conda=4.8.3

COPY env.yml /databricks/.conda-env-def/env.yml

# Create conda environment
RUN /databricks/conda/bin/conda env create --file /databricks/.conda-env-def/env.yml \

# Source conda.sh for all login shells
# Set always_yes to avoid needing -y flags, and improve conda experience in Databricks notebooks
RUN ln -s /databricks/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh \
    && /databricks/conda/bin/conda config --system --set always_yes True

# This environment variable must be set to indicate the conda environment to activate.
# Note that currently, we have to set both of these environment variables. The first one is necessary to indicate that this runtime supports conda.
# The second one is necessary so that the python notebook/repl can be started (won't work without it)
ENV DEFAULT_DATABRICKS_ROOT_CONDA_ENV=gpu
ENV DATABRICKS_ROOT_CONDA_ENV=gpu
