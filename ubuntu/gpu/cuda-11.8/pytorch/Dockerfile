FROM databricksruntime/gpu-conda:cuda11.8 

COPY pytorch.yml /tmp/env.yml

RUN conda env create --file /tmp/env.yml && \
    rm -f /tmp/env.yml && \
    rm -rf $HOME/.cache/pip/*

# Set an environment variable used by Databricks to decide which conda environment to activate by default.
ENV DEFAULT_DATABRICKS_ROOT_CONDA_ENV=pytorch
ENV DATABRICKS_ROOT_CONDA_ENV=pytorch
