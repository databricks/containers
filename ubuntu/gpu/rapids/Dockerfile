FROM sarthfrey/gpu-python:cuda10.1

COPY spec-file.txt /databricks/.conda-env-def/rapids-spec-file.txt

RUN /databricks/conda/bin/conda env create --name rapids --file /databricks/.conda-env-def/rapids-spec-file.txt

ENV DEFAULT_DATABRICKS_ROOT_CONDA_ENV=rapids
ENV DATABRICKS_ROOT_CONDA_ENV=rapids
