FROM sarthfrey/ml-gpu-cuda:latest

RUN /databricks/conda/bin/conda install -n ${DATABRICKS_ROOT_CONDA_ENV} \
    -c rapidsai -c nvidia -c conda-forge -c defaults \
    rapids=0.13 python=3.7 cudatoolkit=10.1
