FROM databricksruntime/gpu-base:cuda10.1

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      wget \
      libdigest-sha-perl

ENV PATH /databricks/conda/bin:$PATH

RUN wget --quiet --output-document miniconda.sh https://repo.continuum.io/miniconda/Miniconda3-py37_4.8.2-Linux-x86_64.sh && \
    (echo '87e77f097f6ebb5127c77662dfc3165e  miniconda.sh' | md5sum -c) && \
    bash miniconda.sh -b -p /databricks/conda && \
    rm miniconda.sh && \
    # Source conda.sh for all login and interactive shells.
    ln -s /databricks/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". /etc/profile.d/conda.sh" >> ~/.bashrc && \
    # Set always_yes for non-interactive shells.
    conda config --system --set always_yes True

COPY gpu.yml /tmp/gpu.yml

RUN conda env create --file /tmp/gpu.yml && \
    rm -f /tmp/gpu.yml

# Set an environment variable used by Databricks to decide which conda environment to activate by default.
ENV DEFAULT_DATABRICKS_ROOT_CONDA_ENV=gpu
