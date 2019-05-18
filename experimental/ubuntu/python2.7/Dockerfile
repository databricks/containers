# Start with DBR base image, all installations for Python REPL need to be installed
FROM databricksruntime/minimal:latest

# Installs python 2.7 and virtualenv for Spark and Notebooks
RUN apt-get update \
  && apt-get install -y \
    python2.7 \
    python-dev \
    virtualenv \
# note that the subprocess32 package is used here as the REPL-required libraries require this to be installed; if using earlier major/minor versions of the libraries below, this can possibly be removed
    python-subprocess32 \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Initialize the default environment that Spark and notebooks will use
RUN virtualenv -p python2.7 --system-site-packages /databricks/python2

# These python libraries are used by Databricks notebooks and the Python REPL
# You do not need to install pyspark - it is injected when the cluster is launched
RUN /databricks/python2/bin/pip install \
  six==1.12.0 \
  ipython==5.0.0 \
  numpy==1.15.4 \
  pandas==0.23.4 \
  pyarrow==0.12.0 \
  matplotlib==2.0.2 \
  jinja2==2.10

# Specifies where Spark will look for the python process
ENV PYSPARK_PYTHON=/databricks/python2/bin/python2
