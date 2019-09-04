FROM databricksruntime/minimal:latest

# Installs python 3.5 and virtualenv for Spark and Notebooks
RUN apt-get update \
  && apt-get install -y \
    python3 \
    virtualenv \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Initialize the default environment that Spark and notebooks will use
RUN virtualenv -p python3 --system-site-packages /databricks/python3

# These python libraries are used by Databricks notebooks and the Python REPL
# You do not need to install pyspark - it is injected when the cluster is launched
RUN /databricks/python3/bin/pip install \
  six==1.12.0 \
  ipython==7.2.0 \
  numpy==1.15.4 \
  pandas==0.23.4 \
  pyarrow==0.12.0 \
  matplotlib==3.0.2 \
  jinja2==2.10

# Specifies where Spark will look for the python process
ENV PYSPARK_PYTHON=/databricks/python3/bin/python3
