FROM databricksruntime/standard:latest

COPY env.yml /databricks/.conda-env-def/ml-gpu-env.yml

RUN /databricks/conda/bin/conda env create --file /databricks/.conda-env-def/ml-gpu-env.yml

# This environment variable must be set to indicate the conda environment to activate.
# Note that currently, we have to set both of these environment variables. The first one is necessary to indicate that this runtime supports conda.
# The second one is necessary so that the python notebook/repl can be started (won't work without it)
ENV DEFAULT_DATABRICKS_ROOT_CONDA_ENV=databricks-ml-gpu
ENV DATABRICKS_ROOT_CONDA_ENV=databricks-ml-gpu
