FROM sarthfrey/gpu-rapids:latest

COPY env.yml /databricks/.conda-env-def/rapids-env.yml

RUN /databricks/conda/bin/conda env update --name ${DATABRICKS_ROOT_CONDA_ENV} --file /databricks/.conda-env-def/rapids-env.yml
