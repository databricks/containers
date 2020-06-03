FROM databricksruntime/gpu-python:cuda10.1

# Databricks recommends using official RAPIDS images instead of installing directly via conda.
# Because RAPIDS depends on conda-forge channel that is unstable.
COPY --from=rapidsai/rapidsai:0.13-cuda10.1-base-ubuntu16.04-py3.7 /opt/conda /opt/conda

RUN conda config --system --append envs_dirs /opt/conda/envs && \
    conda config --system --append pkgs_dirs /opt/conda/pkgs

# Set environment variables used by Databricks to decide which conda environment to activate.
ENV DEFAULT_DATABRICKS_ROOT_CONDA_ENV=rapids
ENV DATABRICKS_ROOT_CONDA_ENV=rapids
