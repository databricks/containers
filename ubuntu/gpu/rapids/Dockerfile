FROM databricksruntime/gpu-python:cuda10.1

RUN conda install -n ${DATABRICKS_ROOT_CONDA_ENV} \
      -c rapidsai -c nvidia -c conda-forge -c defaults \
      rapids=0.13 cudatoolkit=10.1
