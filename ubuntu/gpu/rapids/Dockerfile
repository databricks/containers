FROM databricksruntime/gpu-python:cuda10.1

COPY --from=rapidsai/rapidsai:0.13-cuda10.1-base-ubuntu16.04-py3.7 /opt/conda /opt/conda
RUN rm -rf /databricks/conda && \
    ln -s /opt/conda /databricks/conda

# Set environment variables used by Databricks to decide which conda environment to activate.
ENV DEFAULT_DATABRICKS_ROOT_CONDA_ENV=rapids
ENV DATABRICKS_ROOT_CONDA_ENV=rapids
