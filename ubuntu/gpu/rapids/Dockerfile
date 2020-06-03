FROM databricksruntime/gpu-python:cuda10.1

COPY rapids-spec.txt /tmp/rapids-spec.txt

RUN conda create --name rapids --file /tmp/rapids-spec.txt && \
    rm -f /tmp/rapids-spec.txt

# Set environment variables used by Databricks to decide which conda environment to activate.
ENV DEFAULT_DATABRICKS_ROOT_CONDA_ENV=rapids
ENV DATABRICKS_ROOT_CONDA_ENV=rapids
