FROM databricksruntime/gpu-base:cuda10.1

# Databricks recommends using official RAPIDS images instead of installing directly via conda.
# Because RAPIDS depends on conda-forge channel that is unstable.
COPY --from=rapidsai/rapidsai:0.13-cuda10.1-base-ubuntu16.04-py3.7 /opt/conda /opt/conda

ENV PATH /databricks/conda/bin:$PATH

RUN mkdir -p /databricks && \
    ln -s /opt/conda /databricks/conda && \
    # Source conda.sh for all login and interactive shells.
    ln -s /databricks/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". /etc/profile.d/conda.sh" >> ~/.bashrc && \
    # Set always_yes for non-interactive shells.
    conda config --system --set always_yes True

# Set environment variables used by Databricks to decide which conda environment to activate.
ENV DEFAULT_DATABRICKS_ROOT_CONDA_ENV=rapids
ENV DATABRICKS_ROOT_CONDA_ENV=rapids
