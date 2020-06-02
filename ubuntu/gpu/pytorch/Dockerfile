FROM databricksruntime/gpu-python:cuda10.1

RUN conda install -n ${DATABRICKS_ROOT_CONDA_ENV} -c pytorch \
      pytorch=1.5.0 torchvision=0.6.0 cudatoolkit=10.1
